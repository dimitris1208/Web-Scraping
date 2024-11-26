import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import csv  # For CSV quoting
from concurrent.futures import ThreadPoolExecutor
from categories_attributes_stromata import stromata_structure, stroma_feature, stroma_material, stroma_dimensions

# Define constants
BASE_URL = "https://www.fylliana.gr"
OUTPUT_FILE = "fylliana_STROMATA.csv"
NUM_THREADS = 4
MAX_RETRIES = 5
RETRY_DELAY = 10  # seconds

# WooCommerce CSV headers
HEADERS = [
    "sku",
    "post_title",
    "post_excerpt",
    "post_content",
    "regular_price",
    "manage_stock",
    "images",
    "tax:product_cat",
    "tax:product_tag",
    "attribute:Υλικό",
    "attribute:Διαστάσεις",
    "attribute:Χαρακτηριστικά",
]


def fetch_page(url):
    """
    Fetch a page's content using requests with retries.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}. Retrying ({attempt + 1}/{MAX_RETRIES})...")
            if attempt + 1 < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    print(f"Failed to fetch URL after {MAX_RETRIES} attempts: {url}")
    return None


def scrape_description_and_images(product_url):
    """
    Scrape the description and all images of a product from its detail page.
    """
    print(f"Fetching description and images from: {product_url}")
    html = fetch_page(product_url)
    if not html:
        return "No description available.", ""

    soup = BeautifulSoup(html, "html.parser")

    # Extract description
    description_element = soup.find("p", class_="sdesc")
    description = description_element.text.strip() if description_element else "No description available."

    # Extract all image URLs
    images = []
    image_section = soup.find("div", id="primgms")
    if image_section:
        for img_tag in image_section.find_all("a", href=True):
            image_url = img_tag["href"]
            if image_url.startswith("/"):  # Ensure it's a full URL
                image_url = BASE_URL + image_url
            images.append(image_url)

    # Return the description and comma-separated images for WooCommerce
    images_csv_format = ",".join(images)
    return description, images_csv_format


def fetch_product_data(url, category_path, material=None, feature=None, dimension=None, products_dict=None):
    """
    Fetch product data from a given URL, handle pagination, and consolidate attributes.
    """
    if products_dict is None:
        products_dict = {}
    page_number = 1

    while True:
        paginated_url = url.replace("{page_number}", str(page_number))
        print(f"Fetching products from: {paginated_url}")
        html = fetch_page(paginated_url)
        if not html:
            break

        soup = BeautifulSoup(html, "html.parser")
        product_list = soup.select("div.prdv")

        if not product_list:
            print(f"No products found on page {page_number}.")
            break

        for product in product_list:
            try:
                title = product.find("h2").text.strip()
                price = product.find("p", class_="prc").text.strip()
                sku = product.find("h4").text.strip()
                product_url = BASE_URL + product.find("a", href=True)["href"]

                # Scrape description and images
                description, images_csv_format = scrape_description_and_images(product_url)

                # Map attributes
                material_name = stroma_material.get(material, material or "")
                feature_name = stroma_feature.get(feature, feature or "")
                dimension_name = stroma_dimensions.get(dimension, dimension or "")

                # Consolidate attributes for duplicate SKUs
                if sku in products_dict:
                    existing_product = products_dict[sku]
                    if feature_name and feature_name not in existing_product["attribute:Χαρακτηριστικά"]:
                        existing_product["attribute:Χαρακτηριστικά"] += f",{feature_name}"
                else:
                    # Create a new product entry
                    products_dict[sku] = {
                        "sku": sku,
                        "post_title": title,
                        "post_excerpt": description[:100],
                        "post_content": description,
                        "regular_price": price,
                        "manage_stock": "no",
                        "images": images_csv_format,
                        "tax:product_cat": category_path,
                        "tax:product_tag": f"{material_name}, {dimension_name}, {feature_name}".strip(", "),
                        "attribute:Υλικό": material_name,
                        "attribute:Διαστάσεις": dimension_name,
                        "attribute:Χαρακτηριστικά": feature_name,
                    }

            except Exception as e:
                print(f"Error processing product: {e}")

        # Check for pagination
        if not soup.find("a", class_="next"):
            break

        page_number += 1

    return products_dict


def scrape_category(main_category, subcategory_name, details, products_dict):
    """
    Wrapper function to scrape a category.
    """
    base_url = details["url"]
    category_path = f"{main_category} > {subcategory_name}"
    urls = generate_urls(base_url, details, prioritize_dimensions=(subcategory_name == "Στρώματα"))

    for url, material, feature, dimension in urls:
        fetch_product_data(url, category_path, material, feature, dimension, products_dict)


def generate_urls(base_url, filters, prioritize_dimensions=False):
    """
    Generate a list of URLs by combining base URL with attribute filters.
    """
    urls = []
    dimensions = filters.get("valid_dimensions", [])
    materials = filters.get("valid_materials", [])
    features = filters.get("valid_features", [])

    # If prioritizing dimensions (e.g., for "Στρώματα")
    if prioritize_dimensions:
        for dimension in dimensions or [None]:
            for material in materials or [None]:
                for feature in features or [None]:
                    filter_params = []
                    if dimension:
                        filter_params.append(f"filter-{dimension}")
                    if material:
                        filter_params.append(f"filter-{material}")
                    if feature:
                        filter_params.append(f"filter-{feature}")
                    filter_query = "&".join(filter_params)
                    full_url = f"{base_url}?p={{page_number}}&{filter_query}"
                    urls.append((full_url, material, feature, dimension))
    else:
        for material in materials or [None]:
            for feature in features or [None]:
                filter_params = []
                if material:
                    filter_params.append(f"filter-{material}")
                if feature:
                    filter_params.append(f"filter-{feature}")
                filter_query = "&".join(filter_params)
                full_url = f"{base_url}?p={{page_number}}&{filter_query}"
                urls.append((full_url, material, feature, None))

    return urls


def write_csv(products_dict, filename):
    """
    Write consolidated products to a CSV file using pandas.
    """
    data = list(products_dict.values())
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)


def main():
    products_dict = {}

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for main_category, subcategories in stromata_structure.items():
            for subcategory_name, details in subcategories.items():
                futures.append(executor.submit(scrape_category, main_category, subcategory_name, details, products_dict))

        for future in futures:
            future.result()

    write_csv(products_dict, OUTPUT_FILE)
    print(f"Scraping completed. Data saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

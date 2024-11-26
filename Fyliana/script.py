import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import os
from categories_and_attributes import category_structure, color_dict, material_dict, features_dict
from concurrent.futures import ThreadPoolExecutor

# Base URL for the website
BASE_URL = "https://www.fylliana.gr"

# WooCommerce CSV headers
HEADERS = [
    "sku",
    "post_title",
    "post_excerpt",
    "post_content",
    "regular_price",
    "sale_price",
    "stock",
    "manage_stock",
    "weight",
    "images",
    "tax:product_cat",
    "tax:product_tag",
    "attribute:Color",
    "attribute:Material",
    "attribute:Feature"
]

# Output CSV file
OUTPUT_FILE = "fylliana_products.csv"

# Retry settings
MAX_RETRIES = 5
RETRY_DELAY = 10  # seconds

# Number of threads
NUM_THREADS = 4

# Dictionary for translating main categories to Greek
MAIN_CATEGORY_TRANSLATIONS = {
    "epipla": "Έπιπλα",
    "diakosmitika": "Διακοσμητικά",
    "stromata-leyka-eidi": "Στρώματα και Λευκά Είδη",
    "yfasma": "Υφάσματα",
    "fotismos": "Φωτισμός",
    "eidi-kipou": "Είδη Κήπου"
}


def fetch_page(url):
    """
    Synchronously fetch a page's content using requests with retries.
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


def fetch_product_data(url, main_category, subcategory, color=None, material=None, feature=None):
    """
    Fetch product data from a given URL, handling pagination if present,
    and consolidating attributes for each product.
    """
    products = {}
    page_number = 1
    main_category_greek = MAIN_CATEGORY_TRANSLATIONS.get(main_category, main_category)

    while True:
        # Construct the paginated URL
        if "?" in url:
            paginated_url = url.replace("?", f"?p={page_number}&")
        else:
            paginated_url = f"{url}?p={page_number}"

        print(f"Fetching products from: {paginated_url}")
        response = requests.get(paginated_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Locate the product container
        category_div = soup.find("div", id="ctg")
        if not category_div:
            break

        product_container = category_div.find("div", id="prdsc")
        if not product_container:
            break

        product_list = product_container.find_all("div", class_="prdv")
        if not product_list:
            print(f"No products found on page {page_number} at {paginated_url}.")
            break

        # Notify only if products are found
        print(f"Found {len(product_list)} products on page {page_number}.")

        for product in product_list:
            try:
                # Title
                title_element = product.find("h2")
                title = title_element.text.strip() if title_element else "N/A"

                # Price
                price_element = product.find("p", class_="prc")
                price = price_element.text.strip() if price_element else "N/A"

                # SKU
                sku_element = product.find("h4")
                sku = sku_element.text.strip() if sku_element else "N/A"

                # Product URL
                product_link_element = product.find("a", href=True)
                product_url = BASE_URL + product_link_element["href"] if product_link_element else "N/A"

                # Scrape description and images
                description, images_csv_format = scrape_description_and_images(product_url)

                # Map attributes to human-readable names
                color_name = color_dict.get(color, color or "")
                material_name = material_dict.get(material, material or "")
                feature_name = features_dict.get(feature, feature or "")

                # Tags and Category
                tags = []
                if color_name:
                    tags.append(color_name)
                if material_name:
                    tags.append(material_name)
                tags = ",".join(tags)

                category_path = f"{main_category_greek} > {subcategory}"

                # Add a new product entry
                if sku in products:
                    existing_product = products[sku]
                    if feature_name and feature_name not in existing_product["attribute:Feature"]:
                        existing_product["attribute:Feature"] += f",{feature_name}"
                else:
                    products[sku] = {
                        "sku": sku,
                        "post_title": title,
                        "post_excerpt": description[:100],
                        "post_content": description,
                        "regular_price": price,
                        "sale_price": "",
                        "stock": "",
                        "manage_stock": "no",
                        "weight": "",
                        "images": images_csv_format,
                        "tax:product_cat": category_path,
                        "tax:product_tag": tags,
                        "attribute:Color": color_name,
                        "attribute:Material": material_name,
                        "attribute:Feature": feature_name,
                    }

            except Exception as e:
                print(f"Error fetching product: {e}")

        # Check for pagination
        pagination_div = soup.find("div", id="pagination")
        if not pagination_div or not pagination_div.find("div", class_="pagination"):
            break

        pagination_links = pagination_div.find_all("a", class_="num")
        if not pagination_links or page_number >= len(pagination_links):
            break

        page_number += 1

    return list(products.values())


def scrape_category(main_category, subcategory_name, details):
    """
    Wrapper function to scrape a category.
    """
    products = []
    if "url" in details:
        base_url = details["url"]
        urls = generate_urls(base_url, details)
        for url, color, material, feature in urls:
            products.extend(fetch_product_data(url, main_category, subcategory_name, color, material, feature))
    else:
        for deep_subcategory_name, deep_details in details.items():
            base_url = deep_details["url"]
            urls = generate_urls(base_url, deep_details)
            for url, color, material, feature in urls:
                products.extend(fetch_product_data(url, main_category, f"{subcategory_name} > {deep_subcategory_name}", color, material, feature))
    return products


def generate_urls(base_url, filters):
    """
    Generate a list of URLs by combining base URL with attribute filters.
    """
    urls = []
    for color in filters["valid_colors"] or [None]:
        for material in filters["valid_materials"] or [None]:
            for feature in filters["valid_features"] or [None]:
                filter_params = []
                if material:
                    filter_params.append("filter-"+material)
                if color:
                    filter_params.append("filter-"+color)
                if feature:
                    filter_params.append("filter-"+feature)
                filter_query = "&".join(filter_params)
                full_url = f"{base_url}?{filter_query}" if filter_query else base_url
                urls.append((full_url, color, material, feature))
    return urls


def consolidate_products(products):
    """
    Consolidate duplicate products by SKU and combine their features into a comma-separated list.
    """
    consolidated = {}
    for product in products:
        sku = product["sku"]
        if sku in consolidated:
            existing_product = consolidated[sku]
            existing_feature = existing_product["attribute:Feature"]
            new_feature = product["attribute:Feature"]
            if new_feature and new_feature not in existing_feature:
                consolidated[sku]["attribute:Feature"] = f"{existing_feature},{new_feature}".strip(",")
        else:
            consolidated[sku] = product
    return list(consolidated.values())


def main():
    all_products = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for main_category, subcategories in category_structure.items():
            for subcategory_name, details in subcategories.items():
                futures.append(executor.submit(scrape_category, main_category, subcategory_name, details))

        for future in futures:
            all_products.extend(future.result())

    # Deduplicate and consolidate products
    all_products = consolidate_products(all_products)

    # Save all products to a CSV file
    df = pd.DataFrame(all_products)
    if not os.path.exists(OUTPUT_FILE):
        df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(OUTPUT_FILE, mode="a", header=False, index=False, encoding="utf-8-sig")

    print(f"Scraping completed. Data saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Set up Selenium WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # or webdriver.Firefox() if using Firefox

# Define the base URL of the e-commerce page
base_url = "https://lambrostoys.gr/product-category/girl/page/"

print("Start of the web scraping of Lambros Toys")


# Function to sanitize the handle by replacing special characters with "-"
def sanitize_handle(title):
    handle = title.lower().replace(" ", "-")
    handle = re.sub(r'[^a-zα-ωάέήίόύώ0-9-]', '-', handle, flags=re.UNICODE)
    return handle


# Function to scrape product information from a single product container
def extract_product_info(product):
    # Extract the title
    title_element = product.find("h3", class_="woocommerce-loop-product__title")
    title = title_element.get_text(strip=True) if title_element else "N/A"

    # Use the title as the description
    description = title

    # Extract the price
    price_element = product.find("span", class_="woocommerce-Price-amount")
    price = price_element.get_text(strip=True) if price_element else "N/A"

    # Extract the SKU (found in the "add to cart" link data attribute)
    sku_element = product.find("a", class_="add_to_cart_read_more")
    sku = sku_element["data-product_sku"] if sku_element and sku_element.has_attr("data-product_sku") else "N/A"

    # Extract the image URL
    image_element = product.find("div", class_="product-image").find("img")
    image_url = image_element.get("src") if image_element else "N/A"

    # Sanitize the handle
    handle = sanitize_handle(title)

    # Initialize tags and type lists
    tags = []
    product_type = "Παιχνίδι"  # Default type

    # Extract and process tags from the category list
    category_list = product.find("span", class_="category-list")
    if category_list:
        for tag_element in category_list.find_all("a", rel="tag"):
            tag_text = tag_element.get_text(strip=True)
            # Separate tags by content
            if tag_text in ["Αγόρι", "Κορίτσι"]:
                tags.append(tag_text)
            else:
                product_type = tag_text  # Use the last non-boy/girl tag as the product type

    # Compile the data into a dictionary
    product_data = {
        "Handle": handle,
        "Title": title,
        "Body (HTML)": description,
        "Vendor": "Λάμπρος Παιχνίδια",
        "Variant Price": price,
        "Image Src": image_url,
        "Tags": ", ".join(tags) if tags else "N/A",
        "SKU": sku,
        "Type": product_type
    }

    return product_data


# List to hold all product data
all_products = []

# Iterate through pages using Selenium
for page_number in range(1, 305):  # Adjust page range as needed
    url = f"{base_url}{page_number}"
    print(f"Scraping page {page_number}: {url}")

    # Use Selenium to load the page
    driver.get(url)
    time.sleep(2)  # Give time for JavaScript to load content

    # Parse the loaded page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_list = soup.find("ul", class_=lambda value: value and "products" in value)

    if product_list:
        product_containers = product_list.find_all("li", class_="product-col")
        for product in product_containers:
            product_data = extract_product_info(product)
            if product_data:
                all_products.append(product_data)
    else:
        print(f"Product list not found on page {page_number}. Check the HTML structure.")

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_products)

# Save to CSV
output_filename = "lambros_toys_girls.csv"
df.to_csv(output_filename, index=False)

print(f"Data from all products has been saved to {output_filename}")
print("Done")

# Close the Selenium driver
driver.quit()

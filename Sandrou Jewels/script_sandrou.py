import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# Define the base URL of the e-commerce page



####---------------------------------------------------####
#MODIFY THIS VVVV  , The URL should look like this : https://kosmimasandrou/.../page/

base_url = "https://kosmimasandrou.gr/product-category/rologia/vogue/page/"

####---------------------------------------------------####

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print("Start of the web scraping of Sandrou Jewels")


import re

# Function to sanitize the handle by replacing special characters with "-"
def sanitize_handle(title):
    # Convert to lowercase and replace spaces with hyphens
    handle = title.lower().replace(" ", "-")
    # Replace any character that is not a Greek or Latin letter, number, or hyphen with "-"
    handle = re.sub(r'[^a-zα-ωάέήίόύώ0-9-]', '-', handle, flags=re.UNICODE)
    return handle


# Function to scrape product information from a single product container
def extract_product_info(product):
    # Extract the stock status
    stock_status_element = product.find("p", class_="wd-product-stock")
    stock_status = stock_status_element.get_text(strip=True) if stock_status_element else "Out of stock"

    # Only proceed if the product is in stock
    if stock_status != "In stock":
        return None  # Skip this product if it's out of stock

    # Extract the title
    title_element = product.find("h3", class_="wd-entities-title")
    title = title_element.get_text(strip=True) if title_element else "N/A"

    # Use the title as the description
    description = title

    # Extract the price
    price_element = product.find("span", class_="woocommerce-Price-amount")
    price = price_element.find("bdi").get_text(strip=True) if price_element else "N/A"

    # Extract the SKU
    sku_element = product.find("div", class_="wd-product-sku")
    sku = sku_element.find_all("span")[1].get_text(strip=True) if sku_element else "N/A"

    # Extract the image URL from 'data-lazy-src' or 'src'
    image_element = product.find("div", class_="product-element-top").find("img")
    image_url = image_element.get("data-lazy-src") or image_element.get("src") if image_element else "N/A"

    # Sanitize the handle
    handle = sanitize_handle(title)

    # Compile the data into a dictionary
    ####---------------------------------------------------####
    # MODIFY THIS VVVV


    product_data = {
        "Handle": handle,
        "Title": title,
        "Body (HTML)": description,
        "Vendor": "Sandrou jewels & more",
        "Variant Price": price,
        "Image Src": image_url,
        "Tags": "Vogue",
        "SKU": sku,
        "Type": "Ρολόγια"
    }

    ####---------------------------------------------------####

    return product_data


# List to hold all product data
all_products = []

# Iterate through pages
####---------------------------------------------------####
#MODIFY THIS VVVV


for page_number in range(1, 5):

####---------------------------------------------------####


    # Construct the page-specific URL
    url = f"{base_url}{page_number}"
    print(f"Scraping page {page_number}: {url}")

    # Send a request to the page and parse it
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product containers
    product_containers = soup.find_all("div", class_="product-grid-item")

    # Loop through each product container and extract its information
    for product in product_containers:
        product_data = extract_product_info(product)
        if product_data:  # Only add product data if it's not None
            all_products.append(product_data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_products)

####---------------------------------------------------####
#MODIFY THIS VVVV

# Define the CSV file name
output_filename = "sandrou_jewel_roloi_vogue.csv"

####---------------------------------------------------####

# Append to the CSV if it exists; otherwise, create it
if os.path.isfile(output_filename):
    df.to_csv(output_filename, mode='a', header=False, index=False)
else:
    df.to_csv(output_filename, mode='w', header=True, index=False)

print(f"Data from all products has been appended to {output_filename}")
print("Done")

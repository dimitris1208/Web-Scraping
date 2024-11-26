import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# Define the base URL of the e-commerce page
base_url = "https://louizidis.gr/katigoria/paidika-2/page/"

# Define the query parameters that follow the page number
query_suffix = "/?filters=product_cat[414]"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to sanitize the handle by replacing special characters with "-"
def sanitize_handle(title):
    handle = title.lower().replace(" ", "-")
    handle = re.sub(r'[^a-zα-ωάέήίόύώ0-9-]', '-', handle, flags=re.UNICODE)
    return handle

# Function to scrape product information from a single product container
def extract_product_info(product):
    # Extract the title
    title_element = product.find("h2", class_="wd-entities-title")
    title = title_element.get_text(strip=True) if title_element else "N/A"

    # Use the title as the description
    description = title

    # Extract the price
    price_element = product.find("span", class_="woocommerce-Price-amount")
    price = price_element.find("bdi").get_text(strip=True) if price_element else "N/A"

    # Extract the image URL
    image_element = product.find("div", class_="product-element-top").find("img")
    image_url = image_element.get("src") if image_element else "N/A"

    # Sanitize the handle
    handle = sanitize_handle(title)

    # Extract sizes
    sizes_container = product.find("div", class_="dc-size-loop-wrapper")

    sizes_container = product.find("div", class_="dc-size-loop-wrapper")
    sizes = (
        [size.get_text(strip=True) for size in sizes_container.find_all("span", class_="dc-size-loop")]
        if sizes_container
        else ["One Size"]  # Default to "One Size" if no sizes are listed
    )

    # Define Tags and Type
    tags = "Παιδικά-Κορίτσι"  # Modify or dynamically set tags as needed
    product_type = "Αξεσουάρ"  # Modify or dynamically set product type as needed

    # Create product variants
    product_variants = []
    for idx, size in enumerate(sizes):
        product_data = {
            "Handle": handle,
            "Title": title if idx == 0 else "",  # Leave blank for all rows except the first
            "Body (HTML)": description if idx == 0 else "",  # Leave blank for subsequent rows
            "Vendor": "Louizidis" if idx == 0 else "",
            "Tags": tags if idx == 0 else "",  # Leave blank for subsequent rows
            "Type": product_type if idx == 0 else "",  # Leave blank for subsequent rows
            "Image Src": image_url if idx == 0 else "",  # Leave blank for subsequent rows
            "Variant Price": price,  # Price is the same for all variants
            "Option1 Name": "Size",  # Shopify-compatible size field
            "Option1 Value": size,  # Specific size for the variant
        }
        product_variants.append(product_data)
    return product_variants


# List to hold all product data
all_products = []

# Iterate through pages
for page_number in range(1, 2):  # Change the range as needed for the total number of pages
    # Construct the page-specific URL
    url = f"{base_url}{page_number}{query_suffix}"
    print(f"Scraping page {page_number}: {url}")

    # Send a request to the page and parse it
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product containers
    product_containers = soup.find_all("div", class_="product-grid-item")

    # Loop through each product container and extract its information
    for product in product_containers:
        product_data_list = extract_product_info(product)
        all_products.extend(product_data_list)  # Add all size variants for each product

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_products)

# Define column order for the output
column_order = [
    "Handle", "Title", "Body (HTML)" , "Vendor" , "Tags", "Type", "Image Src",
    "Variant Price", "Option1 Name", "Option1 Value"
]

# Reorder the DataFrame columns
df = df[column_order]

# Define the CSV file name
output_filename = "louizidis_koritsi_accessories.csv"

# Write to the CSV file
df.to_csv(output_filename, index=False, encoding='utf-8-sig')  # UTF-8-sig for Greek characters

print(f"Data from all products has been saved to {output_filename}")
print("Done")

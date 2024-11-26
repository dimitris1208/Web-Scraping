import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

####---------------------------------------------------####
# MODIFY THIS VVVV

# Define the base URL of the e-commerce page
base_url = "https://louizidis.gr/katigoria/gynaikeia/page/"

####---------------------------------------------------####

# Define the query parameters that follow the page number
query_suffix = "/?filters=product_cat[416]"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print("Start of the web scraping process")

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

    ####---------------------------------------------------####
    # MODIFY THIS VVVV

    # Define Tags and Type
    tags = "Γυναικεία"  # Modify or dynamically set tags as needed
    product_type = "Τσάντες"  # Modify or dynamically set product type as needed

    ####---------------------------------------------------####


    # Compile the data into a dictionary
    product_data = {
        "Handle": handle,
        "Title": title,
        "Body (HTML)": description,
        "Vendor" : "Louizidis" ,
        "Tags": tags,
        "Type": product_type,
        "Image Src": image_url,
        "Variant Price": price
    }

    return product_data

# List to hold all product data
all_products = []

####---------------------------------------------------####
# MODIFY THIS VVVV

# Iterate through pages
for page_number in range(1, 14):  # Change the range as needed for the total number of pages

####---------------------------------------------------####

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
        product_data = extract_product_info(product)
        if product_data:  # Only add product data if it's not None
            all_products.append(product_data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_products)

####---------------------------------------------------####
# MODIFY THIS VVVV

# Define the CSV file name
output_filename = "louizidis_gynaikeia_tsantes.csv"

####---------------------------------------------------####

# Append to the CSV if it exists; otherwise, create it
if os.path.isfile(output_filename):
    df.to_csv(output_filename, mode='a', header=False, index=False)
else:
    df.to_csv(output_filename, mode='w', header=True, index=False)

print(f"Data from all products has been appended to {output_filename}")
print("Done")


# Web Scraping Script for Lambros Toys E-Shop

This repository contains a Python script designed to scrape product data from the Lambros Toys e-shop. The scraped data is formatted for analysis or import into other platforms. **This script is tailored for a specific e-shop and requires modifications for use with other stores.**

---

## Script Overview

### `script_lampros_toys.py`
- **Purpose:** Scrapes product data from the "Girls" category of the Lambros Toys e-shop.
- **Default Store:** Targets the "Girls" section of the e-shop at [lambrostoys.gr](https://lambrostoys.gr/).
- **Features:**
  - Extracts product title, price, SKU, image URL, category tags, and product type.
  - Utilizes Selenium to handle JavaScript-loaded pages.
  - Generates a CSV file with all the scraped product data.
- **Output File:** `lambros_toys_girls.csv`

---

## How to Use

### Step 1: Install Dependencies
Ensure you have Python installed. Install the required libraries by running:
```bash
pip install selenium beautifulsoup4 pandas
```

Additionally, ensure you have the **Chrome WebDriver** installed (or the WebDriver corresponding to your preferred browser). Make sure the WebDriver is in your system's PATH.

---

### Step 2: Modify the Script for a New Store
Open the script and update the following:
- **`base_url`:** Change to the base URL of the new store.
- **Product-specific logic:** Adjust the HTML selectors for product details (e.g., title, price, image) to match the new store's structure.

---

### Step 3: Run the Script
Run the script using Python:
```bash
python script_lampros_toys.py
```

---

### Step 4: Review Output
The generated CSV file, `lambros_toys_girls.csv`, will be saved in the same directory as the script. It contains the following fields:
- `Handle`: A unique identifier for each product.
- `Title`: The product name.
- `Body (HTML)`: A brief product description (same as the title).
- `Vendor`: Set as "Λάμπρος Παιχνίδια" by default.
- `Variant Price`: The product price.
- `Image Src`: The product image URL.
- `Tags`: Categories or tags associated with the product.
- `SKU`: The product SKU.
- `Type`: The product type (e.g., "Παιχνίδι").

---

## Notes
- The script uses Selenium to handle pages that load content dynamically using JavaScript.
- Ensure the structure of the target website (HTML, CSS classes) matches the script logic. Adjust selectors if necessary.
- If the website contains more pages, update the `range()` function in the script to scrape all pages.

---

## Disclaimer
This script is intended for **personal or educational use only**. Ensure you have obtained permission from the store owner before scraping their website.

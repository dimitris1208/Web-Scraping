
# Web Scraping Script for Sandrou Jewels E-Shop

This repository contains a Python script designed to scrape product data from the Sandrou Jewels e-shop. The scraped data is formatted for analysis or import into other platforms. **This script is tailored for a specific e-shop and requires modifications for use with other stores.**

---

## Script Overview

### `script_sandrou.py`
- **Purpose:** Scrapes product data from the "Vogue Watches" category of the Sandrou Jewels e-shop.
- **Default Store:** Targets the "Vogue Watches" section of the e-shop at [kosmimasandrou.gr](https://kosmimasandrou.gr/).
- **Features:**
  - Extracts product title, price, SKU, image URL, and stock status.
  - Skips products that are out of stock.
  - Generates a CSV file with all the scraped product data.
- **Output File:** `sandrou_jewel_roloi_vogue.csv`

---

## How to Use

### Step 1: Install Dependencies
Ensure you have Python installed. Install the required libraries by running:
```bash
pip install requests beautifulsoup4 pandas
```

---

### Step 2: Modify the Script for a New Store
Open the script and update the following:
- **`base_url`:** Change to the base URL of the new store.
- **Product-specific logic:** Adjust the HTML selectors for product details (e.g., title, price, image, stock status) to match the new store's structure.
- **`Tags` and `Type`:** Update the default tags and product type in the `product_data` dictionary to match the new store's categories.

---

### Step 3: Run the Script
Run the script using Python:
```bash
python script_sandrou.py
```

---

### Step 4: Review Output
The generated CSV file, `sandrou_jewel_roloi_vogue.csv`, will be saved in the same directory as the script. It contains the following fields:
- `Handle`: A unique identifier for each product.
- `Title`: The product name.
- `Body (HTML)`: A brief product description (same as the title).
- `Vendor`: Set as "Sandrou jewels & more" by default.
- `Variant Price`: The product price.
- `Image Src`: The product image URL.
- `Tags`: Default set as "Vogue."
- `SKU`: The product SKU.
- `Type`: The product type (e.g., "Ρολόγια").

---

## Notes
- This script is designed for static HTML structures. Ensure the structure of the target website (HTML, CSS classes) matches the script logic. Adjust selectors if necessary.
- If the website contains more pages, update the `range()` function in the script to scrape all pages.

---

## Disclaimer
This script is intended for **personal or educational use only**. Ensure you have obtained permission from the store owner before scraping their website.

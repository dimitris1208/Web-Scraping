
# Web Scraping Scripts for E-Shop Data Extraction

This repository contains two Python scripts designed to scrape product data from an e-shop. The scraped data is formatted correctly for import into Shopify. **These scripts are tailored for a specific e-shop and require modifications for use with other stores.**

---

## Scripts Overview

### 1. `louizidis_script_with_sizes.py`
- **Purpose:** Scrapes product data including multiple size variants.
- **Default Store:** Targets the "Children's Accessories" section of the e-shop at [louizidis.gr](https://louizidis.gr/).
- **Features:**
  - Scrapes product title, price, image URL, and sizes.
  - Generates Shopify-compatible CSV with size variants for each product.
- **Output File:** `louizidis_koritsi_accessories.csv`

---

### 2. `louizidis_script.py`
- **Purpose:** Scrapes product data without size variants.
- **Default Store:** Targets the "Women's Bags" section of the e-shop at [louizidis.gr](https://louizidis.gr/).
- **Features:**
  - Scrapes product title, price, and image URL.
  - Generates Shopify-compatible CSV without size variants.
- **Output File:** `louizidis_gynaikeia_tsantes.csv`

---

## How to Use

### Step 1: Install Dependencies
Ensure you have Python installed. Install the required libraries by running:
```bash
pip install -r requirements.txt
```

---

### Step 2: Modify the Script for a New Store
Open the script and update the following:
- **`base_url`:** Change to the base URL of the new store.
- **`query_suffix`:** Adjust query parameters as per the new store's filters.
- **`tags` and `product_type`:** Update product tags and type to match the new categories.

---

### Step 3: Run the Scripts
Run either of the scripts using Python:
```bash
python louizidis_script_with_sizes.py
```
or
```bash
python louizidis_script.py
```

---

### Step 4: Review Output
The generated CSV files will be saved in the same directory as the script. These files can be imported directly into Shopify.

---

## Notes
- These scripts are customized for the specific e-shop `louizidis.gr`. They **must be modified** to scrape data from other stores.
- Ensure the structure of the target website (HTML, CSS classes) matches the script logic. Adjust selectors if necessary.
- If the website contains more pages, update the `range()` function in the script to scrape all pages.

---

## Shopify Compatibility
The generated CSV files are formatted to comply with Shopify's import structure. Fields include:
- `Handle`
- `Title`
- `Body (HTML)`
- `Vendor`
- `Tags`
- `Type`
- `Image Src`
- `Variant Price`
- `Option1 Name` (e.g., "Size")
- `Option1 Value` (e.g., individual size options)

---

## Disclaimer
These scripts are intended for **personal or educational use only**. Ensure you have obtained permission from the store owner before scraping their website.

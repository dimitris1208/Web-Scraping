# WooCommerce Web Scraping Repository 📦🛠️

Welcome to the **WooCommerce Web Scraping Repository**! This collection of scripts is designed to scrape data from websites and generate WooCommerce-compatible CSV files. Whether you're populating a WooCommerce store with products or managing extensive product catalogs, these scripts aim to save you time and effort.

---

## What’s Inside? 🚀
This repository includes scripts divided into two main categories:
1. **General Products**: Handles most product types like furniture, decor, and lighting.
2. **Mattresses**: A specialized category due to their unique attributes like dimensions and materials.

### Folder Structure:
- **`categories_and_attributes.py`**: Contains pre-defined dictionaries for categories and their associated attributes (e.g., color, material, features) for general products.
- **`categories_attributes_stromata.py`**: Similar to the above but tailored specifically for mattresses.
- **`scrape_attributes.py`**: Scrapes categories and attributes dynamically from the website and creates dictionaries. Used for general products.
- **`scrape_stromata_attributes.py`**: Similar to `scrape_attributes.py` but specialized for mattresses.
- **`script.py`**: Generates WooCommerce CSV files for general products using the data from `categories_and_attributes.py`.
- **`script_stromata.py`**: Similar to `script.py` but processes mattresses using `categories_attributes_stromata.py`.

---

## Why Two Separate Pipelines? 🛏️🔄
Mattresses have unique attributes like dimensions that require a distinct approach:
1. **General Products**: Scrapes and processes attributes like colors, materials, and features.
2. **Mattresses**: Adds additional attributes such as dimensions and prioritizes them during CSV generation.

---

## How It Works 🧠
Here’s an overview of how each script contributes to the process:

### Step 1: Scraping Attributes
1. **`scrape_attributes.py`**:
   - Dynamically scrapes categories, subcategories, and their attributes (color, material, features).
   - Outputs structured dictionaries (`categories_and_attributes.py`).

2. **`scrape_stromata_attributes.py`**:
   - Similar to `scrape_attributes.py` but tailored for mattresses.
   - Outputs structured dictionaries (`categories_attributes_stromata.py`).

### Step 2: Generating CSVs
1. **`script.py`**:
   - Uses the dictionaries from `categories_and_attributes.py`.
   - Scrapes product details (title, price, SKU, images) and combines them with the attributes.
   - Outputs a WooCommerce-compatible CSV file.

2. **`script_stromata.py`**:
   - Focuses on mattresses, leveraging `categories_attributes_stromata.py`.
   - Handles attributes like dimensions more effectively.
   - Outputs a WooCommerce-compatible CSV file for mattresses.

---

## Usage Instructions 📋
1. **Install Dependencies**:
   - Ensure you have Python installed.
   - Install required libraries:
     ```bash
     pip install -r requirements.txt
     ```

2. **Scrape Attributes**:
   - Run `scrape_attributes.py` to generate attribute dictionaries for general products:
     ```bash
     python scrape_attributes.py
     ```
   - Run `scrape_stromata_attributes.py` for mattresses:
     ```bash
     python scrape_stromata_attributes.py
     ```

3. **Modify Dictionaries**:
   - Check and manually adjust the generated dictionaries (`categories_and_attributes.py` or `categories_attributes_stromata.py`) if necessary.

4. **Generate CSVs**:
   - For general products:
     ```bash
     python script.py
     ```
   - For mattresses:
     ```bash
     python script_stromata.py
     ```

5. **Review Output**:
   - The generated CSV files will be saved in the root folder, ready for WooCommerce import.

---

## Important Notes ⚠️
- **Permissions**: Do not scrape data from websites without permission.
- **Adjustments**: You may need to adjust the HTML selectors or category URLs if the website structure changes.
- **WooCommerce Specific**: These scripts are tailored for WooCommerce CSV formats and may not work directly with other platforms.

---

## FAQs 🤔
### 1. Why do I need to scrape attributes separately?
Attributes like color, material, and dimensions are scraped first to ensure they are consistent across all products. This minimizes errors and manual edits during CSV generation.

### 2. What if the website changes its structure?
You’ll need to update the HTML selectors in the scripts (`scrape_attributes.py` or `script.py`).

### 3. Can I use this for Shopify?
Nope! These scripts generate WooCommerce-compatible CSVs. Check our other repository for Shopify-specific tools.

---

## Disclaimer 🚨
These scripts are for **educational purposes**. Always get permission from the website owner before scraping their data.

---

## Need Help? Reach Out! 🤝
Got questions about scraping? Need help customizing the scripts? Feel free to ask—we’re here to help! 🎉

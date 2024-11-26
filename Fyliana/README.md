# WooCommerce Web Scraping Repository

This repository contains a collection of scripts designed to scrape data from a **furniture wholesale website** and generate WooCommerce-compatible CSV files. These scripts are custom-built for this specific website but can be adapted for other websites with modifications. The primary goal is to simplify the process of importing product data into WooCommerce, saving time and effort.

---

## What’s Included
The repository is divided into two main pipelines:
1. **General Products**: For most product types such as furniture, decor, and lighting.
2. **Mattresses**: A specialized pipeline to handle unique attributes like dimensions and materials.

### Repository Structure
- **`categories_and_attributes.py`**: Pre-defined dictionaries for categories and their associated attributes (e.g., color, material, features) for general products.
- **`categories_attributes_stromata.py`**: Similar to the above but specifically for mattresses.
- **`scrape_attributes.py`**: Dynamically scrapes categories and attributes from the website and generates dictionaries. Used for general products.
- **`scrape_stromata_attributes.py`**: Similar to `scrape_attributes.py` but designed for mattresses.
- **`script.py`**: Generates WooCommerce-compatible CSV files for general products using data from `categories_and_attributes.py`.
- **`script_stromata.py`**: Generates CSV files for mattresses using data from `categories_attributes_stromata.py`.

---

## Why Separate Pipelines?
Mattresses have unique characteristics such as dimensions that require a specialized approach:
1. **General Products**: Focuses on attributes like colors, materials, and features.
2. **Mattresses**: Adds support for dimensions and prioritizes these attributes during CSV generation.

---

## How It Works
### Step 1: Scraping Attributes
1. **`scrape_attributes.py`**:
   - Scrapes categories, subcategories, and their attributes (color, material, features) from the furniture wholesale website.
   - Outputs structured dictionaries into `categories_and_attributes.py`.

2. **`scrape_stromata_attributes.py`**:
   - Scrapes categories and attributes specifically for mattresses.
   - Outputs structured dictionaries into `categories_attributes_stromata.py`.

### Step 2: Generating CSVs
1. **`script.py`**:
   - Uses the attribute dictionaries from `categories_and_attributes.py`.
   - Scrapes product details such as titles, prices, SKUs, and images.
   - Combines product data with attributes to create a WooCommerce-compatible CSV file.

2. **`script_stromata.py`**:
   - Similar to `script.py` but tailored for mattresses.
   - Handles additional attributes like dimensions more effectively.
   - Produces WooCommerce-compatible CSV files specifically for mattresses.

---

## Usage Instructions
1. **Install Dependencies**:
   - Ensure Python is installed.
   - Install the required libraries:
     ```bash
     pip install -r requirements.txt
     ```

2. **Scrape Attributes**:
   - For general products, run:
     ```bash
     python scrape_attributes.py
     ```
   - For mattresses, run:
     ```bash
     python scrape_stromata_attributes.py
     ```

3. **Modify Attribute Dictionaries**:
   - Review and adjust the generated dictionaries in `categories_and_attributes.py` or `categories_attributes_stromata.py` as necessary.

4. **Generate CSV Files**:
   - For general products, run:
     ```bash
     python script.py
     ```
   - For mattresses, run:
     ```bash
     python script_stromata.py
     ```

5. **Review Output**:
   - The CSV files will be saved in the root folder. These files are formatted for direct import into WooCommerce.

---

## Key Considerations
- **Custom for a Furniture Wholesale Website**: These scripts are tailored to the structure of a specific furniture wholesale website. To use them for other websites, you will need to modify the URLs, HTML selectors, and logic.
- **Permissions Required**: Always ensure you have explicit permission to scrape data from any website.
- **Dynamic Adjustments**: These scripts are functional for the current website but may require updates if the website structure changes.

---

## FAQ
### Why are attributes scraped separately?
Scraping attributes like color, material, and dimensions first ensures consistency and minimizes errors when generating the final product data.

### What happens if the website changes its structure?
You will need to update the HTML selectors in the scripts (`scrape_attributes.py`, `script.py`, etc.) to match the new structure.

### Can these scripts be used for Shopify?
No, these scripts are specifically designed to generate WooCommerce-compatible CSV files.

---

## Disclaimer
These scripts are provided for **educational purposes**. Ensure that you obtain permission from the website owner before scraping any data. Misuse of these scripts may violate terms of service or laws governing data usage.

---

This README provides a detailed explanation of the repository's functionality and requirements. If you have questions or need assistance, feel free to reach out.

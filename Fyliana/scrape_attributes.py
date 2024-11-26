import requests
from bs4 import BeautifulSoup

# Base URL for the website
BASE_URL = "https://www.fylliana.gr"

# Main categories to scrape
MAIN_CATEGORIES = [
    "epipla",
    "diakosmitika",
    "stromata-leyka-eidi",
    "yfasma",
    "fotismos",
    "eidi-kipou"
]

# Nested dictionary to store the entire structure
category_structure = {}
color_dict={}
material_dict ={}
features_dict={}


def extract_subcategories(main_category_url):
    """
    Extract subcategories and their URLs from a main category page.
    """
    print(f"Extracting subcategories from: {main_category_url}")
    response = requests.get(main_category_url)
    soup = BeautifulSoup(response.content, "html.parser")

    subcategories = {}

    # Locate subcategories in the provided HTML structure
    subcategory_section = soup.find("div", id="indstc")
    if subcategory_section:
        for subcategory in subcategory_section.find_all("a", class_="ctg"):
            subcategory_name = subcategory.find("h2").text.strip()
            subcategory_url = BASE_URL + subcategory["href"]
            subcategories[subcategory_name] = subcategory_url

    return subcategories


def extract_deep_subcategories(subcategory_url):
    """
    Extract deeper subcategories (e.g., from 'Καναπέδες') if available.
    """
    print(f"Checking for deeper subcategories in: {subcategory_url}")
    response = requests.get(subcategory_url)
    soup = BeautifulSoup(response.content, "html.parser")

    deep_subcategories = {}

    # Locate deeper subcategories in the provided HTML structure
    deep_subcategory_section = soup.find("div", class_="box")
    if deep_subcategory_section.find("h3"):
        if deep_subcategory_section and "Κατηγορίες" in deep_subcategory_section.find("h3").text:
            for subcategory in deep_subcategory_section.find_all("a"):
                deep_subcategory_name = subcategory.text.strip()
                deep_subcategory_url = BASE_URL + subcategory["href"]
                deep_subcategories[deep_subcategory_name] = deep_subcategory_url

    return deep_subcategories


def scrape_filters(subcategory_url):
    """
    Scrape attribute filters (Χρώμα, Υλικό, Χαρακτηριστικά) from a subcategory URL
    and extract only the portion after 'filter-' from the URLs.
    """
    print(f"Scraping filters for subcategory: {subcategory_url}")
    response = requests.get(subcategory_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Locate the filter section
    filter_section = soup.find("div", id="sdb")  # The main filter container
    if not filter_section:
        print(f"No filters found for {subcategory_url}")
        return {"valid_colors": [], "valid_materials": [], "valid_features": []}

    # Initialize dictionaries for filters
    filters = {"valid_colors": [], "valid_materials": [], "valid_features": []}

    # Extract filters
    filter_boxes = filter_section.find_all("div", class_="box")
    for filter_box in filter_boxes:
        filter_name = filter_box.find("h3")
        if not filter_name:
            continue  # Skip this filter box if no header is found

        filter_name = filter_name.text.strip()
        filter_items = filter_box.find_all("li")

        for item in filter_items:
            label = item.find("label")
            if not label:
                continue  # Skip this item if no label is found

            label_text = label.text.strip()
            value = label_text.split("(")[0].strip()  # Get the name before the count
            filter_input = item.find("input")
            if not filter_input or "value" not in filter_input.attrs:
                continue  # Skip this item if no input element with a value is found

            filter_id = filter_input["value"]  # Extract the filter value for URL construction

            # Construct the filter portion
            filter_param = f"{filter_name}[]={filter_id}"

            # Store in the appropriate list
            if "Χρώμα" in filter_name:
                filters["valid_colors"].append(filter_param)
                color_dict[filter_param] = value  # Map URL extension to human-readable name
            elif "Υλικό" in filter_name:
                filters["valid_materials"].append(filter_param)
                material_dict[filter_param] = value  # Map URL extension to human-readable name
            elif "Χαρακτηριστικά" in filter_name:
                filters["valid_features"].append(filter_param)
                features_dict[filter_param] = value  # Map URL extension to human-readable name

    return filters


def build_nested_structure():
    """
    Build the nested dictionary structure with main categories, subcategories, and attributes.
    """
    for main_category in MAIN_CATEGORIES:
        main_category_url = f"{BASE_URL}/{main_category}"
        subcategories = extract_subcategories(main_category_url)

        # Add the main category
        category_structure[main_category] = {}

        # Iterate through subcategories
        for subcategory_name, subcategory_url in subcategories.items():
            print(f"Processing subcategory: {subcategory_name}")

            # Check if deeper subcategories exist
            deep_subcategories = extract_deep_subcategories(subcategory_url)
            if deep_subcategories:
                category_structure[main_category][subcategory_name] = {}
                for deep_subcategory_name, deep_subcategory_url in deep_subcategories.items():
                    print(f"Processing deeper subcategory: {deep_subcategory_name}")
                    attributes = scrape_filters(deep_subcategory_url)
                    category_structure[main_category][subcategory_name][deep_subcategory_name] = {
                        "url": deep_subcategory_url,
                        **attributes,
                    }
            else:
                # If no deeper subcategories, scrape attributes for the current subcategory
                attributes = scrape_filters(subcategory_url)
                category_structure[main_category][subcategory_name] = {
                    "url": subcategory_url,
                    **attributes,
                }


def main():
    # Build the nested structure
    build_nested_structure()

    # Print the entire structure in copy-pasteable format
    print("\nCategory Structure:")
    for main_category, subcategories in category_structure.items():
        print(f'"{main_category}": {{')
        for subcategory, details in subcategories.items():
            if isinstance(details, dict) and "url" not in details:
                print(f'    "{subcategory}": {{')
                for deep_subcategory, deep_details in details.items():
                    print(f'        "{deep_subcategory}": {deep_details},')
                print("    },")
            else:
                print(f'    "{subcategory}": {details},')
        print("},")

    print(color_dict)
    print(material_dict)
    print(features_dict)

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup

# Base URL for the website
BASE_URL = "https://www.fylliana.gr"

# Main categories to scrape
MAIN_CATEGORIES = [
    "stromata",  # Focus on the "stromata" category as an example
]

# Nested dictionary to store the entire structure
category_structure = {}
color_dict = {}
material_dict = {}
features_dict = {}
dimensions_dict = {}


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


def scrape_filters(subcategory_url):
    """
    Scrape attribute filters (Χρώμα, Υλικό, Χαρακτηριστικά, Διαστάσεις) from a subcategory URL.
    """
    print(f"Scraping filters for subcategory: {subcategory_url}")
    response = requests.get(subcategory_url)
    soup = BeautifulSoup(response.content, "html.parser")

    filters = {"valid_colors": [], "valid_materials": [], "valid_features": [], "valid_dimensions": []}

    # Locate the filter section
    filter_section = soup.find("div", id="sdb")
    if not filter_section:
        print(f"No filters found for {subcategory_url}")
        return filters

    # Extract filters
    filter_boxes = filter_section.find_all("div", class_="box")
    for filter_box in filter_boxes:
        filter_name = filter_box.find("h3")
        if not filter_name:
            continue
        filter_name = filter_name.text.strip()

        for item in filter_box.find_all("li"):
            label = item.find("label")
            if not label:
                continue
            label_text = label.text.split("(")[0].strip()
            input_element = item.find("input", {"name": True, "value": True})
            if not input_element:
                continue

            filter_id = f"{filter_name}[]={input_element['value']}"

            # Categorize filters
            if "Χρώμα" in filter_name:
                filters["valid_colors"].append(filter_id)
                color_dict[filter_id] = label_text
            elif "Υλικό" in filter_name:
                filters["valid_materials"].append(filter_id)
                material_dict[filter_id] = label_text
            elif "Χαρακτηριστικά" in filter_name:
                filters["valid_features"].append(filter_id)
                features_dict[filter_id] = label_text
            elif "Διαστάσεις" in filter_name:
                filters["valid_dimensions"].append(filter_id)
                dimensions_dict[filter_id] = label_text

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
            attributes = scrape_filters(subcategory_url)

            # Keep filters in the format like 'Χρώμα[]=10'
            category_structure[main_category][subcategory_name] = {
                "url": subcategory_url,
                **attributes,
            }


def format_output():
    """
    Format the nested dictionary for display.
    """
    formatted_output = ""
    for main_category, subcategories in category_structure.items():
        formatted_output += f'"{main_category}": {{\n'
        for subcategory_name, details in subcategories.items():
            formatted_output += f'    "{subcategory_name}": {{\n'
            formatted_output += f'        "url": "{details["url"]}",\n'
            formatted_output += f'        "valid_colors": {details["valid_colors"]},\n'
            formatted_output += f'        "valid_materials": {details["valid_materials"]},\n'
            formatted_output += f'        "valid_features": {details["valid_features"]},\n'
            formatted_output += f'        "valid_dimensions": {details["valid_dimensions"]}\n'
            formatted_output += f'    }},\n'
        formatted_output += f'}},\n'
    return formatted_output


def main():
    # Build the nested structure
    build_nested_structure()

    # Print the entire structure in copy-pasteable format
    print("\nCategory Structure:")
    print(format_output())

    print("\nColor Dictionary:")
    print(color_dict)

    print("\nMaterial Dictionary:")
    print(material_dict)

    print("\nFeatures Dictionary:")
    print(features_dict)

    print("\nDimensions Dictionary:")
    print(dimensions_dict)


if __name__ == "__main__":
    main()

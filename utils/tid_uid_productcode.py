import os
import json
import requests

# Constants
URLS = [
    "https://raw.githubusercontent.com/hax0kartik/3dsdb/refs/heads/master/jsons/list_GB.json",
    "https://raw.githubusercontent.com/hax0kartik/3dsdb/refs/heads/master/jsons/list_JP.json",
    "https://raw.githubusercontent.com/hax0kartik/3dsdb/refs/heads/master/jsons/list_KR.json",
    "https://raw.githubusercontent.com/hax0kartik/3dsdb/refs/heads/master/jsons/list_TW.json",
    "https://raw.githubusercontent.com/hax0kartik/3dsdb/refs/heads/master/jsons/list_US.json"
]
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "tid_uid_productcode.json")

def fetch_json_data(url):
    """Fetch JSON data from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def extract_tid_uid_productcode(data):
    """Extract TitleID (tid), UID, and Product Code from JSON data."""
    return {
        item["TitleID"]: {
            "UID": item["UID"],
            "Product Code": item.get("Product Code", "N/A")
        }
        for item in data if "TitleID" in item and "UID" in item
    }

def save_to_file(data, file_path):
    """Save data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {file_path}")
    except IOError as e:
        print(f"Error saving data to {file_path}: {e}")

def main():
    """Main function to fetch, process, and save tid-uid-productcode data."""
    tid_uid_productcode_map = {}

    for url in URLS:
        print(f"Processing {url}...")
        json_data = fetch_json_data(url)
        tid_uid_productcode_map.update(extract_tid_uid_productcode(json_data))

    save_to_file(tid_uid_productcode_map, OUTPUT_FILE)

if __name__ == "__main__":
    main()

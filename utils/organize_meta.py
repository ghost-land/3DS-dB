import os
import json
from collections import OrderedDict


def reorganize_json(file_path):
    """
    Reorganize the JSON file by prioritizing certain keys.
    The keys are reordered based on the defined key order,
    while keeping the remaining keys at the end.
    """
    try:
        # Load the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Define the desired order of keys
        key_order = [
            "tid", "uid", "name", "formal_name", "description",
            "release_date_on_eshop", "product_code", "platform_name",
            "region", "genres", "features", "languages",
            "rating_system", "version", "disclaimer", "descriptors"
        ]

        # Reorganize the JSON data with OrderedDict
        reordered_data = OrderedDict()
        for key in key_order:
            if key in data:
                reordered_data[key] = data[key]

        # Add remaining keys not in the predefined order
        for key in data:
            if key not in reordered_data:
                reordered_data[key] = data[key]

        # Check if the data has changed (order-sensitive comparison)
        if list(reordered_data.keys()) != list(data.keys()):
            # Save the reordered JSON back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(reordered_data, file, ensure_ascii=False, indent=4)
            print(f"✔️  Updated and saved: {file_path}")
            return True  # File was updated
        else:
            print(f"ℹ️  No changes needed: {file_path}")
            return False  # No changes needed

    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON in file: {file_path}. Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error processing file: {file_path}. Error: {e}")
        return False


def process_all_meta_json(base_dir):
    """
    Traverse the directory and process all 'meta.json' files.
    """
    print(f"🔍 Scanning directory: {os.path.abspath(base_dir)}")
    total_files = 0
    updated_files = 0
    skipped_files = 0
    error_files = 0

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == "meta.json":
                total_files += 1
                file_path = os.path.abspath(os.path.join(root, file))
                try:
                    print(f"➡️  Processing: {file_path}")
                    if reorganize_json(file_path):
                        updated_files += 1
                    else:
                        skipped_files += 1
                except Exception as e:
                    error_files += 1
                    print(f"❌ Error processing file: {file_path}. Error: {e}")

    # Summary of processing
    print("\n🔔 Processing Complete!")
    print(f"📂 Total files scanned: {total_files}")
    print(f"✔️  Files updated: {updated_files}")
    print(f"ℹ️  Files skipped (no changes): {skipped_files}")
    print(f"❌ Errors encountered: {error_files}")


if __name__ == "__main__":
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the base directory relative to the script's location
    base_directory = os.path.join(script_directory, "../db/3ds/")
    
    # Run the script to process all 'meta.json' files
    process_all_meta_json(base_directory)

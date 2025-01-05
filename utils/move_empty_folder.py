import os
import shutil
import json

# Relative paths for source and destination
SOURCE_PATH = os.path.join(os.path.dirname(__file__), "../db/3ds")
DESTINATION_PATH = os.path.join(os.path.dirname(__file__), "../missing_db/3ds")

def move_empty_directories(source, destination):
    """
    Moves empty directories from the source path to the destination path,
    maintaining the folder structure, with detailed logging.
    
    Parameters:
        source (str): The root directory to search for empty directories.
        destination (str): The root directory where empty directories will be moved.
    """
    print(f"Starting the process...\nSource: {source}\nDestination: {destination}\n")

    if not os.path.exists(source):
        print(f"[ERROR] Source path '{source}' does not exist.")
        return

    if not os.path.exists(destination):
        os.makedirs(destination, exist_ok=True)
        print(f"[INFO] Created destination directory: {destination}")

    empty_dirs_found = 0
    for root, dirs, files in os.walk(source, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)

            if not os.listdir(dir_path):  # Check if directory is empty
                empty_dirs_found += 1
                relative_path = os.path.relpath(dir_path, source)
                destination_dir = os.path.join(destination, os.path.dirname(relative_path))
                os.makedirs(destination_dir, exist_ok=True)

                destination_path = os.path.join(destination_dir, dir_name)
                if os.path.exists(destination_path):
                    print(f"[SKIPPED] Destination already exists: {destination_path}")
                else:
                    shutil.move(dir_path, destination_path)
                    print(f"[MOVED] {dir_path} -> {destination_path}")

    if empty_dirs_found == 0:
        print("[INFO] No empty directories found.")
    else:
        print(f"[INFO] Total empty directories moved: {empty_dirs_found}")


def generate_missing_files(destination):
    """
    Generates individual missing_<category>.txt files for each category 
    and a global missing.json file listing all categories and their missing TIDs.

    Parameters:
        destination (str): The root directory of the moved empty folders.
    """
    print("\n[INFO] Generating missing files...")
    missing_data = {}
    category_files = {}

    # Traverse the destination folder to categorize TIDs
    for root, dirs, files in os.walk(destination):
        # Check if the current folder contains only TID folders (final subcategory)
        if dirs and not any(os.listdir(os.path.join(root, d)) for d in dirs):
            category = os.path.relpath(root, destination)  # Relative category path
            category_name = category.replace("\\", "-").replace("/", "-")  # Normalize category name
            missing_data[category] = []

            tid_list = []  # Store TIDs for the current category
            for item in dirs:
                missing_data[category].append(item)
                tid_list.append(item)

            # Write missing_<category>.txt for the current category
            category_txt_path = os.path.join(destination, f"missing_{category_name}.txt")
            category_files[category_name] = category_txt_path
            with open(category_txt_path, "w") as f:
                f.write("\n".join(tid_list))
            print(f"[INFO] Written {category_txt_path} with {len(tid_list)} TIDs.")

    # Write the master missing.json file
    missing_json_path = os.path.join(destination, "missing.json")
    with open(missing_json_path, "w") as f:
        json.dump(missing_data, f, indent=4)
    print(f"[INFO] Written global {missing_json_path} with {len(missing_data)} categories.")

    return category_files


if __name__ == "__main__":
    print("[INFO] Script started.")
    move_empty_directories(SOURCE_PATH, DESTINATION_PATH)
    category_files = generate_missing_files(DESTINATION_PATH)
    print("\n[INFO] Generated the following category files:")
    for category, file_path in category_files.items():
        print(f"  - {category}: {file_path}")
    print("[INFO] Script completed.")

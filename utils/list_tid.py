import os
import json

def collect_tids_by_folder(base_path):
    """Collects all valid TIDs grouped by folder from the given directory."""
    tid_dict = {}

    for root, dirs, _ in os.walk(base_path):
        folder_name = os.path.basename(root)
        if folder_name not in tid_dict:
            tid_dict[folder_name] = []

        for dir_name in dirs:
            # Check if the directory name is a valid TID (16 alphanumeric characters)
            if len(dir_name) == 16 and dir_name.isalnum():
                tid_dict[folder_name].append(dir_name)

    # Remove empty entries
    tid_dict = {k: v for k, v in tid_dict.items() if v}

    return tid_dict

def save_to_json(data, file_path):
    """Saves the given data to a JSON file."""
    output_dir = os.path.dirname(file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data successfully saved to {file_path}")

def main():
    # Define paths relative to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, '../db/3ds/')
    output_file = os.path.join(script_dir, '../data/tid_list.json')

    # Check if the base directory exists
    if not os.path.exists(base_path):
        print(f"The directory {base_path} does not exist.")
        return

    # Collect TIDs grouped by folder
    tid_dict = collect_tids_by_folder(base_path)

    # Save the TIDs to a JSON file
    save_to_json(tid_dict, output_file)

if __name__ == "__main__":
    main()

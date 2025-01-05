import os
import json

# Folders to process
FOLDERS_TO_PROCESS = ["games", "dlc", "dsiware", "updates", "videos", "virtual-console"]

def parse_filename(filename, region):
    """
    Parse a file name to extract metadata such as TID, game name, product code, version, and region.
    
    :param filename: The name of the file.
    :param region: The region determined by the parent folder.
    :return: A dictionary containing the extracted metadata.
    """
    try:
        parts = filename.split(" ")
        tid = parts[0]
        name_start_idx = 1
        product_code = None
        version = None
        region_tag = None

        # Identify the product code and adjust the name index
        for i, part in enumerate(parts[1:], start=1):
            if part.startswith("(CTR-") or part.startswith("("):
                product_code = part.strip("()")
                name_start_idx = i
                break

        # Extract version and region information
        for part in parts:
            if part.startswith("(v"):
                version = part.strip("()")
            elif part.startswith("(E)") or part.startswith("(U)") or part.startswith("(J)"):
                region_tag = part.strip("()")

        # Extract the game name
        name = " ".join(parts[1:name_start_idx])

        return {
            "tid": tid,
            "name": name,
            "product_code": product_code,
            "version": version,
            "region": region or region_tag
        }
    except Exception as e:
        print(f"Error parsing file {filename}: {e}")
        return None

def process_folder(base_path, folder_name, output_path, total_counts):
    """
    Process a specific folder to extract file metadata and generate a JSON file.
    
    :param base_path: The base input path provided by the user.
    :param folder_name: The name of the folder to process.
    :param output_path: The directory where JSON files will be saved.
    :param total_counts: A dictionary to track total counts for each folder.
    """
    folder_path = os.path.join(base_path, folder_name)
    output_file = os.path.join(output_path, f"{folder_name}.json")

    data = []

    # Walk through the folder and process files
    for root, dirs, files in os.walk(folder_path):
        region = os.path.basename(root)  # Region is the name of the parent folder
        for file in files:
            if file.endswith(".cia"):  # Only process .cia files
                metadata = parse_filename(file, region)
                if metadata:
                    data.append(metadata)

    # Update the total count for this folder
    total_counts[folder_name] += len(data)

    # Save the extracted data to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Generated JSON file: {output_file} ({len(data)} items)")

def main():
    """
    Main function to process all specified folders and generate JSON files.
    """
    # Ask the user for the input folder
    base_path = input("Enter the path to the input folder: ").strip()
    if not os.path.isdir(base_path):
        print(f"Error: The path '{base_path}' is not a valid directory.")
        return

    # Set the output path relative to the input folder
    output_path = os.path.join(base_path, "../data/initial_data")
    os.makedirs(output_path, exist_ok=True)

    # Initialize total counts
    total_counts = {folder: 0 for folder in FOLDERS_TO_PROCESS}

    # Process each folder
    for folder in FOLDERS_TO_PROCESS:
        process_folder(base_path, folder, output_path, total_counts)

    # Print totals
    print("\nProcessing complete. Summary:")
    for folder, count in total_counts.items():
        print(f"{folder.capitalize()}: {count} items found.")

if __name__ == "__main__":
    main()

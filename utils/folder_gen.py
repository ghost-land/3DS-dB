import os
import shutil

# Network path
network_path = r"\\"

# Destination folder
destination_base = os.path.join(os.getcwd(), "db_generated")

def create_tid_folders():
    if not os.path.exists(network_path):
        print(f"The network path {network_path} is inaccessible.")
        return

    # Create the db_generated folder if it doesn't exist
    if not os.path.exists(destination_base):
        os.makedirs(destination_base)

    # Traverse the network directory
    for root, _, files in os.walk(network_path):
        for file in files:
            if file.endswith(".cia"):
                # Extract the TID from the file name
                tid = file.split(" ")[0]
                tid_folder = os.path.join(destination_base, tid)

                # Create a folder for this TID if it doesn't exist
                if not os.path.exists(tid_folder):
                    os.makedirs(tid_folder)

                print(f"Folder created for TID: {tid}")

if __name__ == "__main__":
    create_tid_folders()
    print("Script completed.")

import os
import subprocess
import sys
import zipfile
import tarfile
import gzip
import shutil
import py7zr
import re
import logging

def show_ascii_art():
    print("""
   .--.
  |o_o |
  |:_/ |
 //   \ \\
(|     | )
/'\_   _/`\\
\___)=(___/
    """)
    print("Welcome to the extraction script!")

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def add_to_path(path):
    if path not in os.environ['PATH']:
        os.environ['PATH'] += os.pathsep + path
        print(f"Added {path} to PATH")
        logging.info(f"Added {path} to PATH")

# Set up logging
def setup_logging(log_file_path):
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    logging.getLogger('').addHandler(console_handler)

# Check and install required libraries
required_packages = ['zipfile', 'tarfile', 'gzip', 'shutil', 'py7zr']

for package in required_packages:
    try:
        __import__(package)
        logging.info(f"Library {package} is installed.")
    except ImportError:
        install(package)
        logging.info(f"Library {package} was not installed. Installing now.")

# Add required scripts to PATH
script_paths = [
    os.path.join(os.path.expanduser("~"), "AppData", "Local", "Packages", "PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0", "LocalCache", "local-packages", "Python311", "Scripts")
]

for path in script_paths:
    add_to_path(path)

import zipfile
import tarfile
import gzip
import shutil
import py7zr

def extract_files(directory):
    log_file_path = os.path.join(directory, 'asup_parse_log.txt')
    setup_logging(log_file_path)

    logging.info(f"Starting extraction in directory: {directory}")
    print(f"Starting extraction in directory: {directory}")

    body_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if "body" in file.lower() and file.endswith(('.zip', '.tar', '.gz', '.7z')):
                body_files.append(file)
                logging.info(f"Found body file: {file}")
                print(f"Found body file: {file}")

    if not body_files:
        logging.info("No body files found.")
        print("No body files found.")
        return

    extracted_dirs = []

    for body_file in body_files:
        file_path = os.path.join(root, body_file)
        output_dir = os.path.join(root, f"{body_file}_extracted")
        os.makedirs(output_dir, exist_ok=True)

        try:
            logging.info(f"Extracting {file_path} to {output_dir}")
            print(f"Extracting {file_path} to {output_dir}")

            if body_file.endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
            elif body_file.endswith(".tar"):
                with tarfile.open(file_path, 'r') as tar_ref:
                    tar_ref.extractall(output_dir)
            elif body_file.endswith(".gz"):
                with gzip.open(file_path, 'rb') as gz_ref:
                    with open(file_path[:-3], 'wb') as out_file:
                        shutil.copyfileobj(gz_ref, out_file)
                    with tarfile.open(file_path[:-3], 'r') as tar_ref:
                        tar_ref.extractall(output_dir)
            elif body_file.endswith(".7z"):
                with py7zr.SevenZipFile(file_path, 'r') as z:
                    z.extractall(output_dir)

            logging.info(f"Successfully extracted {file_path} to {output_dir}")
            print(f"Successfully extracted {file_path} to {output_dir}")

            extracted_dirs.append(output_dir)
        except Exception as e:
            logging.error(f"Failed to extract {file_path}: {e}")
            print(f"Failed to extract {file_path}: {e}")
            continue

        # Check for sysconfig-a.txt in the output directory
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if re.search(r'sysconfig-a\.txt', file, re.IGNORECASE):
                    logging.info(f"sysconfig-a.txt found in {output_dir}")
                    print(f"sysconfig-a.txt found in {output_dir}")
                    sysconfig_path = os.path.join(root, file)
                    found_serial_number = False
                    with open(sysconfig_path, 'r') as f:
                        logging.info("Looking for the string 'System Serial Number' in sysconfig-a.txt")
                        print("Looking for the string 'System Serial Number' in sysconfig-a.txt")
                        for line in f:
                            if re.search(r'system serial number', line, re.IGNORECASE):
                                logging.info(f"Found in sysconfig-a.txt: {line.strip()}")
                                print(f"Found in sysconfig-a.txt: {line.strip()}")
                                match = re.search(r'System Serial Number: (\d+)\s*\(([^)]+)\)', line, re.IGNORECASE)
                                if match:
                                    serial_number = match.group(1)
                                    alphanumeric = match.group(2)
                                    folder_name = f"SN {serial_number} {alphanumeric}"
                                    new_path = os.path.join(directory, folder_name)
                                    os.makedirs(new_path, exist_ok=True)
                                    logging.info(f"Created folder: {new_path}")
                                    print(f"Created folder: {new_path}")

                                    # Copy contents from output directory to new folder
                                    for item in os.listdir(output_dir):
                                        src = os.path.join(output_dir, item)
                                        dest = os.path.join(new_path, item)
                                        if os.path.isdir(src):
                                            shutil.copytree(src, dest)
                                        else:
                                            shutil.copy2(src, dest)
                                    logging.info(f"Copied contents from {output_dir} to {new_path}")
                                    print(f"Copied contents from {output_dir} to {new_path}")

                                    found_serial_number = True
                    if not found_serial_number:
                        logging.error(f"Error: 'System Serial Number' not found in {sysconfig_path}")
                        print(f"Error: 'System Serial Number' not found in {sysconfig_path}")

    # Cleanup unneeded files
    for output_dir in extracted_dirs:
        try:
            shutil.rmtree(output_dir)
            logging.info(f"Cleaned up unneeded directory: {output_dir}")
            print(f"Cleaned up unneeded directory: {output_dir}")
        except Exception as e:
            logging.error(f"Failed to clean up directory {output_dir}: {e}")
            print(f"Failed to clean up directory {output_dir}: {e}")

def check_path():
    # Ensure that the necessary scripts are in the user's PATH
    paths_to_check = [
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "Packages", "PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0", "LocalCache", "local-packages", "Python311", "Scripts")
    ]
    for path in paths_to_check:
        add_to_path(path)

if __name__ == "__main__":
    show_ascii_art()
    check_path()
    directory = input("Enter the directory to search: ")
    extract_files(directory)
    input("Press Enter to close...")

# Body.zip Extractor

Welcome to the Body.zip Extractor Script! This script is designed to recursively search a directory for files containing "body" in their name and ending with various compression formats such as `.zip`, `.tar`, `.gz`, and `.7z`. The script then extracts these files, searches for `sysconfig-a.txt` within the extracted contents, and performs several operations based on the extracted data.

## Features

- **Recursive Search:** Searches the specified directory and its subdirectories for target files.
- **Multi-format Extraction:** Supports extraction of `.zip`, `.tar`, `.gz`, and `.7z` files.
- **Config Parsing:** Looks for a `sysconfig-a.txt` file and reads the "System Serial Number" from it.
- **Directory Management:** Creates new directories based on the serial number and alphanumeric characters found in `sysconfig-a.txt`.
- **Logging:** Logs all actions and results to both the console and a log file `asup_parse_log.txt`.

## Prerequisites

- Python 3.x
- Required Python Libraries:
  - `zipfile`
  - `tarfile`
  - `gzip`
  - `shutil`
  - `py7zr`
  - `re`

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/joe0121/body.zip-extractor.git
   cd body.zip-extractor
   ```

2. Install required libraries:
   ```sh
   pip install py7zr
   ```

## Usage

1. Run the script:
   ```sh
   python asup_parser.py
   ```

2. Enter the directory to search when prompted.

## Output

- **Logs:** All actions and results are logged in `asup_parse_log.txt` in the specified search directory.
- **Extracted Content:** Extracted files are moved to new directories named using the serial number and alphanumeric characters from `sysconfig-a.txt`.
- **Cleanup:** The script cleans up the initial extraction directories after processing.

## Example

After running the script, the log file will contain detailed information about the steps taken and their results. For example:
```
Starting extraction in directory: /path/to/search
Found body file: body_example.zip
Extracting /path/to/search/body_example.zip to /path/to/search/body_example.zip_extracted
Successfully extracted /path/to/search/body_example.zip to /path/to/search/body_example.zip_extracted
sysconfig-a.txt found in /path/to/search/body_example.zip_extracted
Looking for the string 'System Serial Number' in sysconfig-a.txt
Found in sysconfig-a.txt: System Serial Number: 1234567890 (ABCDEF123)
Created folder: /path/to/search/SN 1234567890 ABCDEF123
Copied contents from /path/to/search/body_example.zip_extracted to /path/to/search/SN 1234567890 ABCDEF123
Deleted original directory: /path/to/search/body_example.zip_extracted
```

## Notes

- Make sure to run the script with appropriate permissions, especially when dealing with system files and directories.
- Adjust the script as needed to fit your specific environment or requirements.

## License

This project is licensed under the MIT License.

## Acknowledgments

Big thanks to Tux the Penguin for leading the charge! 🐧


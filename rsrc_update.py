# Haven't been checked

import os
import sys
import shutil
import requests
import zipfile
from pathlib import Path

skip_download = False

rsrc_url = "https://github.com/MaaAssistantArknights/MaaResource/archive/refs/heads/main.zip"
maa_dir = "MAA-v5.5.11452-win-x64"

maarsrc_dir = "MaaResource-main"
zip_file = f"{maarsrc_dir}.zip"

# Function to clean up temporary files
def clean_up():
    print("Cleaning up")
    if os.path.isfile(zip_file):
        os.remove(zip_file)
    if os.path.isdir(maarsrc_dir):
        shutil.rmtree(maarsrc_dir)

# Function to download the file
def download_file():
    print(f"Downloading from {rsrc_url} ...")
    try:
        response = requests.get(rsrc_url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        with open(zip_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"[error] Download failed: {e}")
        sys.exit(1)

# Function to unzip the file
def unzip_file():
    print("Unzipping the file ...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall()
    except zipfile.BadZipFile as e:
        print(f"[error] Unzip failed: {e}")
        clean_up()
        sys.exit(1)

# Function to process files
def process_file():
    print(f"Copying cache/ and resource/ to {maa_dir}")
    if not os.path.exists(maa_dir):
        os.makedirs(maa_dir)
    for subdir in ["cache", "resource"]:
        src_path = Path(maarsrc_dir) / subdir
        dest_path = Path(maa_dir) / subdir
        if src_path.exists():
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
    print("Finished.")

# Parse command line arguments
def parse_args(args):
    global skip_download
    while args:
        if args[0] in ("-s", "--skip-download"):
            skip_download = True
            args.pop(0)
        elif args[0] in ("-h", "--help"):
            print("Usage: script.py [-s|--skip-download] [-h|--help]")
            print("  -s, --skip-download    Skip downloading operation")
            print("  -h, --help             Show help information")
            sys.exit(0)
        else:
            print(f"Invalid argument: {args[0]}")
            sys.exit(1)

# Main logic
if __name__ == "__main__":
    parse_args(sys.argv[1:])

    if skip_download:
        print("Skip Downloading zip file")
    else:
        download_file()

    unzip_file()
    process_file()
    clean_up()
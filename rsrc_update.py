import shutil
import requests # need pip installation
import zipfile
from pathlib import Path

rsrc_url = "https://github.com/MaaAssistantArknights/MaaResource/archive/refs/heads/main.zip"
# maa_dir = Path("MAA-v5.5.11452-win-x64")
maa_dir = Path("test")
maarsrc_dir = Path("MaaResource-main")
zip_file = maarsrc_dir.with_suffix(".zip")

# Function to clean up temporary files
def clean_up():
    print("Cleaning up")
    if zip_file.exists():
        zip_file.unlink()
    if maarsrc_dir.exists():
        shutil.rmtree(maarsrc_dir)

# Function to download the file
def download_file():
    print(f"Downloading from {rsrc_url} ...")
    try:
        response = requests.get(rsrc_url, stream=True)
        response.raise_for_status()
        with zip_file.open('wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"[error] Download failed: {e}")
        raise

# Function to unzip the file
def unzip_file():
    print("Unzipping the file ...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall()
    except zipfile.BadZipFile as e:
        print(f"[error] Unzip failed: {e}")
        clean_up()
        raise

# Function to process files
def process_file(maa_dir):
    print(f"Copying cache/ and resource/ to {maa_dir}")
    maa_dir.mkdir(parents=True, exist_ok=True)
    for subdir in ["cache", "resource"]:
        src_path = maarsrc_dir / subdir
        dest_path = maa_dir / subdir
        if src_path.exists():
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
    print("Finished.")

# Main logic
def main(skip_download):
    if skip_download:
        print("Skip Downloading zip file")
    else:
        download_file()
    
    unzip_file()
    process_file(maa_dir)
    clean_up()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download and process Maa resources.")
    parser.add_argument("-s", "--skip-download", action="store_true", help="Skip downloading operation")
    args = parser.parse_args()
    
    try:
        main(args.skip_download)
    except KeyboardInterrupt:
        print("\n[info] Detected Ctrl+C, preparing to exit...")
    finally:
        clean_up()
        print("Program Terminated.")
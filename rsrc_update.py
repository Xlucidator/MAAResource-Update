import shutil
import requests # need pip installation
import zipfile
from pathlib import Path
from tqdm import tqdm # need pip installation

rsrc_url = "https://github.com/MaaAssistantArknights/MaaResource/archive/refs/heads/main.zip"
maa_dir = Path("MAA-v5.5.11452-win-x64")
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

        total_size = int(response.headers.get('content-length', 0)) # tqdm: for size
        with zip_file.open('wb') as file, tqdm(total=total_size, unit='B', unit_scale=True, desc=zip_file.name) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # write and update bar only when chunk isn't null
                    file.write(chunk)
                    bar.update(len(chunk))  # tqdm: update bar
                    
    except requests.RequestException as e:
        print(f"[error] Download failed: {e}")
        raise

# Function to unzip the file
def unzip_file():
    print("Unzipping the file ...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            total_size = sum(file.file_size for file in zip_ref.infolist()) # tqdm: for size
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Extracting") as bar:
                for file_info in zip_ref.infolist():
                    zip_ref.extract(file_info, maarsrc_dir)
                    bar.update(file_info.file_size)  # tqdm: update bar
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
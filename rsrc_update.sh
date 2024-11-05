#!/bin/bash

skip_download=false

rsrc_url=https://github.com/MaaAssistantArknights/MaaResource/archive/refs/heads/main.zip
maa_dir=MAA-v5.5.11452-win-x64

maarsrc_dir=MaaResource-main
zip_file=${maarsrc_dir}.zip
# zip_file=$(basename "$rsrc_url")

if [ ! -d "$maa_dir" ]; then
    echo "[error] Target MAA directory do not exist"
    exit 1
fi

clean_up() {
    echo "Cleanning up"
    if [ -f "$zip_file" ]; then
        rm -f "$zip_file"
    fi
    if [ -d "$maarsrc_dir" ]; then
        rm -rf "$maarsrc_dir"
    fi
}

download_file() {
    echo "Downloading from $rsrc_url ..."
    wget -O "$zip_file" "$rsrc_url"
    if [ $? -ne 0 ]; then
        echo "[error] Download failed"
        exit 1
    fi
}

unzip_file() {
    echo "Unzipping the file ..."
    if command -v pv > /dev/null 2>&1; then
        unzip "$zip_file" | pv > /dev/null
    else
        unzip "$zip_file" | awk 'BEGIN {ORS=" "} {if(NR%100==0)print "."}' && echo ""
    fi
    
    if [ $? -ne 0 ]; then
        echo "[error] Unzip failed"
        clean_up
        exit 1
    fi
}

process_file() {
    echo "Copying cache/ and resource/ to $maa_dir"
    cp -r "$maarsrc_dir/cache" "$maa_dir"
    cp -r "$maarsrc_dir/resource" "$maa_dir"
    echo "Finished."
}

trap clean_up SIGINT

while [ $# -gt 0 ]; do
    case $1 in
        -s|--skip-download)    
            skip_download=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [-s|--skip-download] [-h|--help]"
            echo "  -s, --skip-download    跳过下载操作"
            echo "  -h, --help             显示帮助信息"
            exit 0
            ;;
        *)
            echo "Invalid argument:$1" 1>&2
            exit 1
            ;;
    esac
done

if [ "$skip_download" = true ]; then
    echo "Skip Downloading zip file"
else
    download_file
fi

unzip_file
process_file
clean_up
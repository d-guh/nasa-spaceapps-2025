#!/usr/bin/env python3
"""
download.py - Fetches GLDAS_NOAH025_M .nc4 files for a date range
"""

import os
import earthaccess

from config import DATA_DIR

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_filename(record):
    if "data_links" in record and record["data_links"]:
        return os.path.basename(record["data_links"][0])
    elif "meta" in record and "filename" in record["meta"]:
        return record["meta"]["filename"]
    elif "umm" in record and "RelatedUrls" in record["umm"]:
        for url in record["umm"]["RelatedUrls"]:
            if "URL" in url and url["URL"].endswith(".nc4"):
                return os.path.basename(url["URL"])
    return None

def main():
    ensure_dir(DATA_DIR)

    results = earthaccess.search_data(
        short_name="GLDAS_NOAH025_M",
        temporal=("2000-01-01", "2025-09-01")
    )

    print(f"Found {len(results)} results")

    for r in results:
        filename = get_filename(r)
        if not filename:
            print("[WARN] Filename not found")
            continue
        local_path = f"{DATA_DIR}{filename}"
        if not os.path.exists(local_path):
            print(f"Downloading: {filename}")
            downloaded_files = earthaccess.download(r, local_path=DATA_DIR)
            file = downloaded_files[0]
        else:
            file = local_path
            print(f"Exists: {file}")
    
    print("Files OK")

if __name__ == "__main__":
    main()

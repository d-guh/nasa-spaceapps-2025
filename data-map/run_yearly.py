#!/usr/bin/env python3
"""
run_yearly.py — run main.py in 1-year blocks and zip the output

Usage:
    python run_yearly.py

(I was running out of memory)
"""

import subprocess
import datetime
import shutil
import os

# Configuration
START_YEAR = 2000
END_YEAR = 2025
OUTPUT_DIR = "./bloom_maps"
ZIP_NAME = "bloom_maps.zip"

def run_yearly_jobs():
    for year in range(START_YEAR, END_YEAR + 1):
        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 1)
        print(f"\n=== Running {year} ===")
        cmd = [
            "./.venv/scripts/python", "main.py",
            "--start", start.isoformat(),
            "--end", end.isoformat(),
            "--save-maps"
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] Error running for {year}: {e}")
            continue

def zip_results():
    if not os.path.exists(OUTPUT_DIR):
        print(f"[!] Output directory not found: {OUTPUT_DIR}")
        return
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)
    print(f"\nZipping {OUTPUT_DIR} -> {ZIP_NAME} ...")
    shutil.make_archive(ZIP_NAME.replace(".zip", ""), 'zip', OUTPUT_DIR)
    print("Compression complete.")

if __name__ == "__main__":
    run_yearly_jobs()
    zip_results()

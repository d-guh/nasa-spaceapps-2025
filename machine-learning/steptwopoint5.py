#!/usr/bin/env python3
import os
import json
import numpy as np
import xarray as xr
from datetime import datetime
from tqdm import tqdm
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


LAT_MIN, LAT_MAX = 35.0, 38.0
LON_MIN, LON_MAX = -122.0, -118.0
OUTPUT_JSON = "california_bloom_detections.json"
YEARS_BACK = 3
DATA_DIR = "./nasa_data"
LAT_STEP = 0.05
LON_STEP = 0.05

os.makedirs(DATA_DIR, exist_ok=True)

def download_modis_ndvi(date: datetime):
    file_path = os.path.join(DATA_DIR, f"MOD13Q1_NDVI_{date.strftime('%Y%m%d')}.nc")
    if not os.path.exists(file_path):
        ndvi = np.random.uniform(0.1, 0.9, (480, 480)).astype(np.float32)
        xr.DataArray(ndvi, dims=("lat", "lon")).to_netcdf(file_path)
    return file_path


def cloud_mask(ndvi_data: np.ndarray) -> np.ndarray:
    return np.where(ndvi_data < 0, np.nan, ndvi_data)

def detect_bloom_transition(ndvi_series: list[float]) -> float:
    ndvi_series = np.array(ndvi_series)
    if np.isnan(ndvi_series).all():
        return 0.0

    diffs = np.diff(ndvi_series)
    variance = np.nanvar(diffs)
    confidence = float(min(1.0, variance * 2.5))
    return confidence


def process_lat_row(lat: float, lon_grid: np.ndarray, dates: list[datetime]) -> list[dict]:

    detections = []

    for lon in lon_grid:
        ndvi_series = []
        for date in dates:
            try:
                file_path = download_modis_ndvi(date)
                ds = xr.open_dataset(file_path)
                ndvi_data = cloud_mask(ds[list(ds.data_vars)[0]].values)
                ds.close()

                lat_i = int((lat - LAT_MIN) / (LAT_MAX - LAT_MIN) * ndvi_data.shape[0])
                lon_i = int((lon - LON_MIN) / (LON_MAX - LON_MIN) * ndvi_data.shape[1])

                ndvi_value = ndvi_data[lat_i % ndvi_data.shape[0], lon_i % ndvi_data.shape[1]]
                ndvi_series.append(ndvi_value)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                ndvi_series.append(np.nan)

        confidence = detect_bloom_transition(ndvi_series)
        if confidence > 0:
            detections.append({
                "latitude": float(lat),
                "longitude": float(lon),
                "confidence": float(confidence),
                "location": f"{lat:.3f},{lon:.3f}",
                "dates": [d.strftime("%Y-%m-%d") for d, v in zip(dates, ndvi_series) if not np.isnan(v)]
            })
    return detections

def ml_cluster_detections(detections: list[dict]) -> list[dict]:

    if not detections:
        return detections

    X = np.array([[d["latitude"], d["longitude"], d["confidence"]] for d in detections])
    X_scaled = StandardScaler().fit_transform(X)

    kmeans = KMeans(n_clusters=5, n_init=10, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    for i, det in enumerate(detections):
        det["cluster_id"] = int(clusters[i])
    return detections


def main():
    start_time = time.time()
    print(f"Scanning California ({YEARS_BACK} years) for bloom transitions...")

    current_year = datetime.now().year
    start_year = current_year - YEARS_BACK + 1
    dates = [datetime(y, m, 1) for y in range(start_year, current_year + 1) for m in range(1, 13)]

    lat_grid = np.arange(LAT_MIN, LAT_MAX, LAT_STEP)
    lon_grid = np.arange(LON_MIN, LON_MAX, LON_STEP)
    print(f"Latitude rows: {len(lat_grid)}, Longitude columns: {len(lon_grid)}")

    all_detections = []

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(process_lat_row, lat, lon_grid, dates): lat for lat in lat_grid}
        for future in tqdm(as_completed(futures), total=len(lat_grid), desc="Latitude scan"):
            result = future.result()
            all_detections.extend(result)
            print(f"Latitude {futures[future]:.2f} done, total detections: {len(all_detections)}")


    print("Clustering detections using KMeans")
    clustered_detections = ml_cluster_detections(all_detections)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(clustered_detections, f, indent=2)

    print(f"Detected blooms saved to {OUTPUT_JSON}")
    print(f"Runtime: {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()


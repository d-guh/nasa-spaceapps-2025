#!/usr/bin/env python3
"""
main.py - compute bloom habitability
- concat monthly GLDAS files
- convert units: soil -> volumetric (m3/m3), precip -> mm/day, temp -> °F
- clamp-and-normalize each variable using sensible min/max ranges
- combine using weights from config.PARAMS
"""

import os
import glob
import argparse
from datetime import datetime
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from config import DATA_DIR, PARAMS

# Yes I know there's 3 normalize functions, I was messing with all of them, 
def normalize(value, ideal, range_):
    """Convert deviation from ideal to 0-1 score (left as-is)."""
    return np.clip(1 - np.abs(value - ideal) / range_, 0, 1)

def sigmoid_norm(x, ideal, range_):
    return 1 / (1 + np.exp(5 * np.abs(x - ideal)/range_ - 2.5))

def clamp_and_normalize(arr, vmin, vmax):
    """Clip to [vmin, vmax] and scale to 0..1"""
    arr_clipped = arr.clip(min=vmin, max=vmax)
    return (arr_clipped - vmin) / (vmax - vmin)

def find_var(ds, preferred, fallbacks=()):
    if preferred in ds:
        return preferred
    for v in fallbacks:
        if v in ds:
            return v
    return None

def sanitize_array(arr):
    """Replace common fill values with NaN and ensure floats."""
    arr = arr.astype(float)
    # replace extremely large fill values
    arr = arr.where(np.isfinite(arr))
    if hasattr(arr, "attrs"):
        fv = arr.attrs.get("_FillValue", None)
        if fv is not None:
            arr = arr.where(arr != fv)
        mv = arr.attrs.get("missing_value", None)
        if mv is not None:
            arr = arr.where(arr != mv)
    return arr

def open_datasets_for_range(files, start_date=None, end_date=None):
    ds_list = []
    for f in sorted(files):
        # try to infer the file date via filename (AYYYYMM) and filter by start/end
        base = os.path.basename(f)
        date = None
        parts = base.split(".")
        for part in parts:
            if part.startswith("A") and len(part) >= 7 and part[1:7].isdigit():
                yyyymm = part[1:7]
                date = datetime(year=int(yyyymm[:4]), month=int(yyyymm[4:6]), day=1)
                break
        if start_date and date and date < start_date:
            continue
        if end_date and date and date > end_date:
            continue

        ds = xr.open_dataset(f, engine="netcdf4")
        ds_list.append(ds)
    return ds_list


def main():
    parser = argparse.ArgumentParser(description="Compute bloom habitability (old-style).")
    parser.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD)")
    parser.add_argument("--save-maps", action="store_true", help="Save per-month maps to ./bloom_maps/")
    args = parser.parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d") if args.start else None
    end_date = datetime.strptime(args.end, "%Y-%m-%d") if args.end else None

    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.nc4")))
    if not files:
        print("No .nc4 files found in data directory.")
        return

    print(f"Found {len(files)} files; filtering by date range...")
    ds_list = open_datasets_for_range(files, start_date, end_date)
    if not ds_list:
        print("No datasets after date filtering.")
        return

    print(f"Loaded {len(ds_list)} dataset objects, concatenating along time...")
    merged = xr.concat(ds_list, dim="time", data_vars="minimal", coords="minimal", compat="override")

    # Get var names + fallbacks
    soil_pref = PARAMS["soil_moisture"]["var"]
    precip_pref = PARAMS["precipitation"]["var"]
    temp_pref = PARAMS["temperature"]["var"]
    veg_pref = PARAMS["vegetation"]["var"]

    soil_var = find_var(merged, soil_pref, fallbacks=("SoilMoi0_10cm_inst", "SoilMoi0_10cm"))
    precip_var = find_var(merged, precip_pref, fallbacks=("Rainf_f_tavg", "Rainf_tavg", "Rainf_f_tavg"))
    temp_var = find_var(merged, temp_pref, fallbacks=("Tair_f_inst", "Tair_f"))
    veg_var = find_var(merged, veg_pref, fallbacks=("CanopInt_inst",))

    if soil_var is None or precip_var is None or temp_var is None:
        print("WARNING: One or more expected variables not found. Available keys:", list(merged.keys()))

    # --- sanitize and convert units ---
    # Soil: kg/m² over 0-10cm -> volumetric m³/m³: divide by (depth_m * rho_water)
    depth_m = 0.10
    rho_water = 1000.0

    norm_parts = {}

    if soil_var and soil_var in merged:
        merged[soil_var] = sanitize_array(merged[soil_var])
        merged["Soil_vol"] = merged[soil_var] / (depth_m * rho_water)  # m3/m3
        merged["Soil_vol"].attrs["units"] = "m3/m3"
        print(f"Converted {soil_var} -> Soil_vol (m3/m3); sample mean:",
              float(merged["Soil_vol"].mean(skipna=True).values))

    # Precip: kg/m²/s -> mm/day -> multiply by 86400
    if precip_var and precip_var in merged:
        merged[precip_var] = sanitize_array(merged[precip_var])
        merged["Precip_mmday"] = merged[precip_var] * 86400.0
        merged["Precip_mmday"].attrs["units"] = "mm/day"
        print(f"Converted {precip_var} -> Precip_mmday (mm/day); sample mean:",
              float(merged["Precip_mmday"].mean(skipna=True).values))

    # Temp: K -> °F
    if temp_var and temp_var in merged:
        merged[temp_var] = sanitize_array(merged[temp_var])
        merged["Tair_F"] = (merged[temp_var] - 273.15) * 9/5 + 32
        merged["Tair_F"].attrs["units"] = "°F"
        print(f"Converted {temp_var} -> Tair_F (°F); sample mean:",
              float(merged["Tair_F"].mean(skipna=True).values))

    # Vegetation cover
    if veg_var and veg_var in merged:
        VEG_MIN, VEG_MAX = 0.0, 0.3
        veg_n = clamp_and_normalize(merged[veg_var], VEG_MIN, VEG_MAX)
        norm_parts["vegetation"] = veg_n

    # Clamps, may want tweaking, honestly scuffed
    SOIL_MIN, SOIL_MAX = 0.00, 0.40      # volumetric m3/m3
    PRECIP_MIN, PRECIP_MAX = 0.0, 7.5   # mm/day average
    TEMP_MIN_F, TEMP_MAX_F = 30.0, 90.0 # °F

    # Normalized fields
    if "Soil_vol" in merged:
        soil_n = clamp_and_normalize(merged["Soil_vol"], SOIL_MIN, SOIL_MAX)
        norm_parts["soil_moisture"] = soil_n
    else:
        print("[WARN] Soil_vol not found; soil will be skipped in bloom calculation.")

    if "Precip_mmday" in merged:
        precip_n = clamp_and_normalize(merged["Precip_mmday"], PRECIP_MIN, PRECIP_MAX)
        norm_parts["precipitation"] = precip_n
    else:
        print("[WARN] Precip_mmday not found; precipitation will be skipped in bloom calculation.")

    if "Tair_F" in merged:
        temp_n = clamp_and_normalize(merged["Tair_F"], TEMP_MIN_F, TEMP_MAX_F)
        norm_parts["temperature"] = temp_n
    else:
        print("[WARN] Tair_F not found; temperature will be skipped in bloom calculation.")
        

    # Weighted bloom map
    total_weight = 0.0
    bloom_components = []
    for key in ("soil_moisture", "precipitation", "temperature", "vegetation"):
        cfg = PARAMS.get(key)
        if cfg is None:
            continue
        w = float(cfg.get("weight", 0.0))
        # Double check normalized part
        if key in norm_parts:
            bloom_components.append(w * norm_parts[key])
            total_weight += w
        else:
            print(f"[INFO] parameter '{key}' not available in data, skipping weight {w}.")

    if total_weight == 0:
        raise RuntimeError("No parameters available to compute bloom map (total weight == 0).")

    bloom_map = sum(bloom_components) / total_weight
    # clip to [0,1]
    bloom_map = bloom_map.clip(0.0, 1.0)
    bloom_map.name = "Bloom_Likelihood"

    print(f"Global mean bloom chance (mean over time+space): {float(bloom_map.mean(skipna=True).values) * 100:.2f}%")

    # Uncomment if wanted, kinda funky
    # ---- Time Series (global average) ----
    # Use cosine latitude weighting (as in the old script)
    # lat = merged["lat"]
    # weights = np.cos(np.deg2rad(lat))
    # # xarray's weighted requires a DataArray with a dim matching "lat" dimension name
    # # compute weighted mean along lat/lon for each normalized component
    # series = {}
    # for key, arr in norm_parts.items():
    #     # arr dims: time, lat, lon (expected)
    #     # compute area weight: pass weights with dims ('lat',)
    #     try:
    #         avg = arr.weighted(weights).mean(dim=("lat", "lon"))
    #     except Exception:
    #         # fallback: simple mean if weighted fails
    #         avg = arr.mean(dim=("lat", "lon"))
    #     series[key] = avg

    # # compute time-series bloom average using the same weight normalization
    # bloom_avg = sum(series[k] * PARAMS[k]["weight"] for k in series.keys()) / sum(PARAMS[k]["weight"] for k in series.keys())

    # # plot normalized components + bloom_avg
    # plt.figure(figsize=(12, 6))
    # times = merged["time"].values
    # # choose colors & names
    # map_label = {"soil_moisture": "Soil (norm)", "precipitation": "Precip (norm)", "temperature": "Temp (norm)"}
    # for k, avg in series.items():
    #     plt.plot(times, avg, label=map_label.get(k, k))
    # plt.plot(times, bloom_avg, label="Bloom Likelihood (weighted)", linewidth=3, color="magenta")
    # plt.xlabel("Time")
    # plt.ylabel("Normalized Value (0-1)")
    # plt.title("Environmental Factors vs Bloom Likelihood")
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()

    # ---- Map visualization for each month ----
    out_dir = "./bloom_maps"
    if args.save_maps:
        os.makedirs(out_dir, exist_ok=True)

    for t_idx in range(len(merged["time"])):
        month = str(merged["time"].values[t_idx])[:10]

        # Width roughly twice height
        width_inch = 56
        height_inch = width_inch / 2  # 2:1 aspect
        fig, ax = plt.subplots(figsize=(width_inch, height_inch), facecolor="black")
        fig.patch.set_facecolor("black")
        
        data = bloom_map.isel(time=t_idx).values
        cmap = LinearSegmentedColormap.from_list(
            "bloom_cmap",
            [
                (0.0, "black"),
                (0.30, "black"),
                (0.65, "gold"),
                (1.00, "purple")
            ]
        )

        pad_top = 0
        pad_bottom = 120
        data_padded = np.pad(data, ((pad_bottom, pad_top), (0,0)), constant_values=np.nan)
        
        # show image
        ax.imshow(data_padded, cmap=cmap, vmin=0, vmax=1, origin="lower", aspect="auto")
        
        # remove axes
        ax.set_axis_off()
        ax.set_facecolor("black")
        
        if args.save_maps:
            out_file = os.path.join(out_dir, f"bloom_{month}.png")
            plt.savefig(out_file, dpi=200, bbox_inches='tight', pad_inches=0, facecolor="black")
            plt.close(fig)
            print("Saved:", out_file)
        else:
            plt.show()
            plt.close(fig)


    for ds in ds_list:
        try:
            ds.close()
        except Exception as e:
            print(f"ERROR: Error closing dataset: {e}")
            pass


if __name__ == "__main__":
    main()

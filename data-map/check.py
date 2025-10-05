#!/usr/bin/env python3
"""
check.py - Check data structure
"""

from netCDF4 import Dataset
import numpy as np
import sys

np.set_printoptions(threshold=100, edgeitems=5, linewidth=120)

def explore_nc(path):
    print(f"[i] Exploring {path}")
    ds = Dataset(path, 'r')
    print("\nVariables:")
    for var in ds.variables:
        v = ds.variables[var]
        print(f" - {var}: {v.dimensions} ({v.shape})")
        print(f"   Units: {getattr(v, 'units', 'N/A')}")
        sample = v[0].mean() if v.ndim > 1 else v[:]
        print(f"   Example: {sample}\n")
    ds.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <file.nc4>")
        sys.exit(1)
    explore_nc(sys.argv[1])

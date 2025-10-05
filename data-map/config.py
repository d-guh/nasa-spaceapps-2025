# config.py
"""
Don't actually run this script, its imported in relevant files.
Also ideal/range are only used when using certain normalize functions.
"""

DATA_DIR = "./data/ground/"

PARAMS = {
    "temperature": {
        "var": "Tair_f_inst",
        "ideal": 74,         # °F
        "range": 15,         # ±20°F
        "weight": 0.30,      # 0.20  # equator lol
    },
    "precipitation": {
        "var": "Rainf_tavg",
        "ideal": 22,         # in/year
        "range": 15,         # ±15 in/yr
        "weight": 0.35,      # 0.10  # only counts in tropics lol
    },
    "soil_moisture": {
        "var": "SoilMoi0_10cm_inst",
        "ideal": 35,         # kg m-2 ≈ mm
        "range": 20,         # ±30 mm
        "weight": 0.25,      # 0.25  # HOLY GREENLAND BRO, any except desert
    },
    "vegetation": {
        "var": "CanopInt_inst",
        "ideal": 0.20,       # adjust depending on what you consider healthy coverage
        "range": 0.15,       # ±range
        "weight": 0.10,      # relative to soil, temp, precip  # NO GREENLAND, northern forests
    },
}

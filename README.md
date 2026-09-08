# Evaluating the Role of Land Surface Temperature in Post-Fire Vegetation Recovery: A Case Study of Mount Kenya

BSc Geomatic Engineering & Geospatial Information Systems (GEGIS) final year project — Jomo Kenyatta University of Agriculture and Technology, 2025.

> Can Land Surface Temperature (LST) — a variable largely overlooked in post-fire recovery models — help explain why some burned slopes of Mount Kenya recover and others don't?

**[View the interactive story map →](https://loventaanyango.github.io/post-fire-vegetation-recovery-mt-kenya/)** 
---

## Overview

This project investigates post-fire vegetation recovery (PVR) on Mount Kenya using a decade of Landsat imagery (2011–2021), integrating Land Surface Temperature with burn severity, topography, climate, and soil organic carbon into a Random Forest regression model. The model predicts the Normalized Burn Ratio (NBR) — a proxy for vegetation recovery — following the March 2012 fire that burned over 8,000 hectares of forest.

The study classifies burn severity into seven classes using the Differenced Normalized Burn Ratio (dNBR), validates results against Kenya Forest Service field data and the MODIS MCD64A1 burned-area product, and identifies LST's non-linear relationship with recovery — with a narrow thermal "sweet spot" around 299–300 K favouring regrowth.

## Key Results

| Metric | Test Set | 10-Fold Cross-Validation |
|---|---|---|
| R² | 0.9013 | 0.8753 (avg.) |
| RMSE | 0.0280 | 0.0406 (avg.) |

- **ANOVA** across burn severity classes: F = 12.16, p < 0.001 — recovery differs significantly by severity class.
- **Top predictors** (Random Forest feature importance): pre-fire NBR, soil total organic carbon, and dNBR, followed by temperature variables and LST.
- **2012 fire extent validation**: Landsat estimate (23,400 ha) closely matches MCD64A1 (22,388 ha); KFS field data reports a narrower 9,878 ha.

## Repository Structure

```
├── data/                    # Raw & processed datasets — Landsat-derived indices, climate (WorldClim),
│                              soil total organic carbon (AFSIS), SRTM topography, KFS field validation data
├── gee/                     # Google Earth Engine scripts — NBR/dNBR calculation and LST retrieval
│                              from Landsat 7 ETM+ / Landsat 8 OLI-TIRS
├── qgis/
│   └── polygon_vector/      # QGIS project files and the vectorized burn-severity classification
│                              (Polygon_vectors.shp + .dbf/.shx/.prj/.cpg) — raster-to-polygon output
│                              used for zonal statistics
├── python/                  # Random Forest model training, hyperparameter tuning, k-fold cross-validation,
│                              ANOVA / Tukey HSD, partial dependence, and plotting scripts
├── outputs/                 # Generated burn severity maps, time series, correlation matrix, residual plots,
│                              performance metrics, and validation maps (Figures 6–20 in the report)
├── docs/                    # Interactive HTML story map — a visual companion to the written report
└── README.md
```


## Study Area

Mount Kenya (0°07′–0°20′S, 37°03′–37°30′E), Africa's second-highest peak and a UNESCO World Heritage Site, supplying approximately 40% of Kenya's water and 60% of its hydropower. The study focuses on the March 2012 fire, which burned over 8,000 hectares of upper montane forest and bamboo.

## Data Sources

| Dataset | Source | Resolution | Use |
|---|---|---|---|
| Landsat 7 ETM+ / Landsat 8 OLI-TIRS | USGS Earth Explorer | 30 m | NBR / dNBR / LST |
| MCD64A1 Burned Area | NASA (MODIS) | 500 m | Burn extent validation |
| SRTM DEM | USGS | 30 m | Elevation, slope, aspect |
| Climate (temperature, precipitation) | WorldClim.org | ~1 km | Climatic predictors |
| Soil Total Organic Carbon | AFSIS | 250 m | Soil predictor |
| Field validation | Kenya Forest Service | — | Burn extent ground-truthing |

## Methodology

1. **Pre-processing** — Landsat imagery (2011 pre-fire baseline → 2021) cloud-masked and clipped in Google Earth Engine.
2. **Burn severity classification** — dNBR thresholds applied per USGS standards, reclassified into 7 severity/regrowth classes.
3. **Vectorization** — reclassified raster converted to polygons in QGIS for zonal statistics per class, per year.
4. **Zonal statistics** — LST, climate, soil, and topographic variables extracted per burn-severity polygon.
5. **Model training** — Random Forest regression (100 trees, 80/20 train-test split) predicting NBR from LST, dNBR, and environmental predictors.
6. **Validation** — 10-fold cross-validation, ANOVA + Tukey HSD across severity classes, and cross-checking against MCD64A1 and KFS field data.

## Reproducing the Analysis

```bash
# Clone the repository
git clone https://github.com/loventaanyango/post-fire-vegetation-recovery-mt-kenya.git
cd post-fire-vegetation-recovery-mt-kenya

# Python environment
pip install -r requirements.txt

# Run the model
python python/Final_RF.py   # update to your actual script name(s)
```

The Earth Engine scripts in `gee/` are written for the [GEE Code Editor](https://code.earthengine.google.com/) — open them there directly, or adapt with the `earthengine-api` Python package for local execution. The QGIS project in `qgis/polygon_vector/` can be opened directly in QGIS ≥ 3.x.

## Interactive Story Map

The `docs/` folder contains a standalone HTML story map summarizing the study's methodology and findings with interactive charts and maps, built with Leaflet and Chart.js. To publish it as a live site: **Settings → Pages → source: `main` branch, folder: `/docs`.**

## Citation

If referencing this work, please cite:

> Otieno, L. A. (2025). *Evaluating the Role of Land Surface Temperature and Other Key Variables in Post-Fire Vegetation Recovery: A Case Study of Mt. Kenya.* BSc project report, Department of Geomatic Engineering and Geospatial Information Systems, Jomo Kenyatta University of Agriculture and Technology.

## Author & Supervisor

- **Author:** Otieno Loventa Anyango (ENC221-0100/2019)
- **Supervisor:** Dr. Harison Kipkulei, PhD, Tutorial Fellow, GEGIS
- **Department:** Geomatic Engineering and Geospatial Information Systems, JKUAT

## License

The code in this repository (`python/`, `gee/`, `qgis/`) is licensed under the **MIT License** — see [`LICENSE`](./LICENSE) for the full text. In short: anyone may use, copy, modify, and redistribute it, provided the original copyright notice is retained.

## Acknowledgements

Data providers: USGS Earth Explorer, NASA/MODIS, WorldClim.org, Africa Soil Information Service (AFSIS), and the Kenya Forest Service. Developed as part of the GEGIS BSc programme at JKUAT.

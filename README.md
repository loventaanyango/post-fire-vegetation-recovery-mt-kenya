# post-fire-vegetation-recovery-mt-kenya
## Overview
This project analyzes post-fire vegetation recovery in the Mt. Kenya ecosystem using satellite remote sensing and machine learning techniques. The study evaluates how Land Surface Temperature (LST) and other environmental variables influence vegetation recovery following wildfire events.

A hybrid geospatial workflow was implemented, integrating QGIS for DNBR calculation and visualization, Google Earth Engine for large-scale satellite data processing and feature extraction, and Python for machine learning modeling and evaluation.

---

## Objectives
- Calculate DNBR and classify burn severity levels
- Analyze post-fire vegetation recovery trends over time
- Evaluate the role of Land Surface Temperature in vegetation recovery
- Develop a Random Forest regression model to predict vegetation recovery
- Assess model performance using statistical evaluation metrics

---

## Study Area
The study focuses on the Mt. Kenya region, a critical montane ecosystem characterized by diverse vegetation types and high ecological importance. The area has experienced wildfire events that provide a suitable case for analyzing post-fire recovery dynamics.

---

## Data Sources
- Landsat 7 and Landsat 8 imagery (2011–2023)
- MCD64A1
- WorldClimate.org
- Africa Soil Information Service (AFSIS)
- Shuttle Radar Topography Mission (SRTM)
- Kenya Forest Service

---

## Methodology Overview

### 1. DNBR Calculation and Burn Severity Mapping (QGIS)
- Pre- and post-fire NBR rasters were used to compute DNBR
- DNBR values were classified into seven burn severity classes
- Spatial visualization and map layouts were produced in QGIS

### 2. Satellite Data Processing (Google Earth Engine)
- Landsat imagery was processed at scale
- Predictor variables were derived and extracted
- Zonal statistics were exported for further analysis

### 3. Machine Learning Modeling (Python)
- Random Forest regression was used to model vegetation recovery
- Predictor variables included LST and other environmental factors
- Model performance was evaluated using RMSE and R² metrics

---

## Tools and Technologies
- QGIS (DNBR calculation and spatial visualization)
- Google Earth Engine (satellite data processing and feature extraction)
- Python (Random Forest regression, evaluation, visualization)
- Landsat 7 & 8
- WorldClim climate data

---

## Repository Structure

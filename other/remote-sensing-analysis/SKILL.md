---
name: remote-sensing-analysis
description: "Remote sensing pipeline with optical/SAR processing and ML classification. Use for satellite imagery analysis."
context: fork
globs: ["**/*.tif", "**/*.tiff", "**/*.nc", "**/scripts/rs_*.py"]
alwaysApply: false
---

# Skill: Remote Sensing Analysis

## Purpose
This skill equips any agent with expert technical knowledge in **complete remote sensing**, including:
- Optical image processing (multispectral, hyperspectral, panchromatic)
- SAR processing (radiometric calibration, speckle filtering, InSAR, polarimetric decomposition)
- Spectral index calculation and band math
- Radiometric and atmospheric correction
- Change detection (LandTrendr, CCDC, BFAST, neural networks)
- Time series: smoothing, gap-filling, phenological analysis
- ML/DL classification (Random Forest, U-Net, SegFormer, OBIA)
- Object detection in satellite/drone imagery
- Pansharpening and sensor fusion
- Photogrammetry and point cloud processing (LiDAR/SfM)
- LULC product analysis (MapBiomas, CGLS, ESRI, GLAD, ESA WorldCover)
- Spatial statistics and inter-product agreement metrics
- Accuracy assessment (Olofsson 2014) and spatial statistics
- Scientific literature search in indexed journals

---

## 1. Raster Image Processing

### 1.1 Reading, Reprojecting and Aligning

```python
import rasterio
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pathlib import Path

def read_raster_safe(path: Path, band: int = 1) -> tuple[np.ndarray, dict]:
    """Safe raster reading with nodata handling."""
    with rasterio.open(path) as src:
        data = src.read(band)
        profile = src.profile.copy()
        nodata = src.nodata
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data.astype(float))
    return data, profile

def reproject_match(src_path: Path, ref_path: Path,
                    resampling: str = 'nearest') -> tuple[np.ndarray, dict]:
    """
    Reproject raster to the CRS and grid of a reference raster.
    IMPORTANT: classifications → use 'nearest' (not 'bilinear').
    Reference: Foody (2002) RSE 80(1):185
    """
    from rasterio.enums import Resampling as RS
    method = getattr(RS, resampling)
    with rasterio.open(ref_path) as ref:
        ref_crs, ref_transform = ref.crs, ref.transform
        ref_height, ref_width = ref.height, ref.width
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, ref_crs, ref_width, ref_height,
            left=ref.bounds.left, bottom=ref.bounds.bottom,
            right=ref.bounds.right, top=ref.bounds.top)
        kwargs = src.meta.copy()
        kwargs.update({'crs': ref_crs, 'transform': transform,
                       'width': ref_width, 'height': ref_height})
        data = np.empty((src.count, ref_height, ref_width), dtype=src.dtypes[0])
        reproject(source=rasterio.band(src, list(range(1, src.count + 1))),
                  destination=data, src_transform=src.transform,
                  src_crs=src.crs, dst_transform=transform,
                  dst_crs=ref_crs, resampling=method)
    return data, kwargs
```

### 1.2 CRS Recommendations

```python
CRS_RECOMMENDATIONS = {
    'global_analysis':    'ESRI:54012',   # Eckert IV (equal-area)
    'south_america':      'EPSG:4087',    # World Equidistant Cylindrical
    'brazil_national':    'EPSG:4674',    # SIRGAS 2000
    'landsat_default':    'EPSG:4326',    # WGS84 geographic
    'sentinel_utm_z22s':  'EPSG:32722',   # UTM Zone 22S
}
# ⚠️ ALWAYS verify CRS before spatial operations
```

---

## 2. Radiometric and Atmospheric Correction

### 2.1 Pipeline DN → Surface Reflectance

```
DN (Digital Number)
  ↓ radiometric calibration
Radiance (W/m²/sr/μm)
  ↓ divide by solar irradiance + cos(SZA)
TOA Reflectance (%)
  ↓ atmospheric correction (6S, Sen2Cor, LEDAPS, LaSRC)
Surface Reflectance (%)
  ↓ topographic correction (optional)
Normalised Reflectance
```

### 2.2 Atmospheric Correction Tools

| Sensor | Tool | Method |
|--------|------|--------|
| Sentinel-2 | Sen2Cor | LUT (Look-up Table) |
| Landsat 8/9 OLI | LaSRC | 6SV radiative transfer |
| Landsat 5/7 TM/ETM+ | LEDAPS | 6S |
| Multi-sensor | Py6S | 6S Python wrapper |
| Aquatic | ACOLITE | Dark Spectrum Fitting |
| Simple / relative | DOS (Dark Object Subtraction) | Empirical |

```python
# Example: TOA reflectance for Landsat 8 OLI
def dn_to_toa_reflectance(dn: np.ndarray, M_rho: float, A_rho: float,
                           sun_elevation_deg: float) -> np.ndarray:
    """
    Convert DN → TOA Reflectance (Landsat Collection 2).
    M_rho, A_rho: coefficients from MTL file (REFLECTANCE_MULT/ADD_BAND_x)
    Reference: USGS Landsat Collection 2 Science Product Guide
    """
    toa = M_rho * dn + A_rho
    sun_elevation_rad = np.deg2rad(sun_elevation_deg)
    return toa / np.sin(sun_elevation_rad)
```

---

## 3. Spectral Indices and Band Math

### 3.1 Core Indices

```python
def compute_index(band_a: np.ndarray, band_b: np.ndarray,
                  formula: str = 'ndvi') -> np.ndarray:
    """Compute normalised spectral indices."""
    eps = 1e-8
    if formula == 'ndvi':     # (NIR - Red) / (NIR + Red)
        return (band_a - band_b) / (band_a + band_b + eps)
    elif formula == 'ndwi':   # (Green - NIR) / (Green + NIR)  Gao 1996
        return (band_b - band_a) / (band_b + band_a + eps)
    elif formula == 'nbr':    # (NIR - SWIR2) / (NIR + SWIR2)
        return (band_a - band_b) / (band_a + band_b + eps)

# Quick reference by category:
SPECTRAL_INDICES = {
    # Vegetation
    'NDVI':   '(NIR - Red) / (NIR + Red)',          # Tucker 1979
    'EVI':    '2.5*(NIR-Red)/(NIR+6*Red-7.5*Blue+1)', # Liu & Huete 1995
    'SAVI':   '(NIR-Red)/(NIR+Red+L)*(1+L)',        # Huete 1988, L=0.5
    'MSAVI':  '(2*NIR+1 - sqrt((2*NIR+1)²-8*(NIR-Red)))/2', # Qi 1994
    'NDRE':   '(RedEdge - Red) / (RedEdge + Red)',  # Gitelson 1994
    'LAI':    'from NDVI via empirical model',
    # Water
    'NDWI':   '(Green - NIR) / (Green + NIR)',      # McFeeters 1996
    'MNDWI':  '(Green - SWIR1) / (Green + SWIR1)', # Xu 2006
    'AWEI':   '4*(Green-SWIR1)-(0.25*NIR+2.75*SWIR2)', # Feyisa 2014
    # Urban / Bare Soil
    'NDBI':   '(SWIR1 - NIR) / (SWIR1 + NIR)',     # Zha 2003
    'BSI':    '((SWIR1+Red)-(NIR+Blue))/((SWIR1+Red)+(NIR+Blue))', # Rikimaru 2002
    # Fire
    'NBR':    '(NIR - SWIR2) / (NIR + SWIR2)',      # Key & Benson 2006
    'dNBR':   'pre_NBR - post_NBR',
    'RBR':    'dNBR / (pre_NBR + 1.001)',           # Parks 2014
    # SAR
    'VH/VV':  'VH / VV (log scale)',
    'RVI':    '4*VH / (VV + VH)',                   # Kim 2012
}
```

---

## 4. SAR Processing

### 4.1 Preprocessing Pipeline

```
SAR Image (SLC / GRD)
  ↓ Radiometric calibration (sigma0 / beta0 / gamma0)
  ↓ Speckle filtering (Lee / Refined Lee / Gamma-MAP)
  ↓ Terrain correction (RTC — Range-Doppler / Ellipsoid)
  ↓ Convert to dB: 10 * log10(sigma0)
  ↓ Geocoding (target EPSG)
ARD Product (Analysis-Ready SAR)
```

### 4.2 Speckle Filtering

```python
from scipy.ndimage import uniform_filter
import numpy as np

def lee_filter(img: np.ndarray, size: int = 7) -> np.ndarray:
    """
    Lee filter for speckle reduction in SAR images.
    Reference: Lee (1980) IEEE Trans. Pattern Anal. Mach. Intell. 2(2):165
    """
    img_mean = uniform_filter(img, size)
    img_sq_mean = uniform_filter(img**2, size)
    img_variance = img_sq_mean - img_mean**2
    overall_variance = np.var(img)
    img_weights = img_variance / (img_variance + overall_variance)
    return img_mean + img_weights * (img - img_mean)
```

### 4.3 Polarimetric Decomposition (reference table)

| Decomposition | Components | Typical Application |
|---|---|---|
| Freeman-Durden | Volume + Double-bounce + Odd | Forest, LULC |
| Touzi | Symmetric + Anti-symmetric | Wetlands |
| Cloude-Pottier | Entropy H, Anisotropy A, Alpha α | OBIA, classification |
| Yamaguchi (4-comp) | + Helix | Urban areas |

---

## 5. Change Detection

### 5.1 Main Approaches

| Method | Type | Data | Reference |
|---|---|---|---|
| Image Differencing | Pixel | Optical | Singh 1989 |
| CVA (Change Vector Analysis) | Pixel | Multi-band | Malila 1980 |
| MAD / IR-MAD | Statistical | Multi-temporal | Nielsen 2007 |
| LandTrendr | Temporal | Annual Landsat | Kennedy 2010 |
| CCDC | Temporal | Dense Landsat | Zhu & Woodcock 2014 |
| BFAST | Temporal | Any TS | Verbesselt 2010 |
| BISE | Gaps | MODIS/NDVI | Lovell 2008 |
| Siamese CNN | DL | Optical/SAR | Daudt 2018 |
| ChangeFormer | DL | Optical | Bandara 2022 |

```python
def image_differencing(img_t1: np.ndarray, img_t2: np.ndarray,
                        threshold: float = None) -> np.ndarray:
    """
    Change detection by simple image differencing.
    threshold: if None, uses mean + 2*std (automatic).
    """
    diff = np.abs(img_t2.astype(float) - img_t1.astype(float))
    if threshold is None:
        threshold = diff.mean() + 2 * diff.std()
    return diff > threshold
```

---

## 6. Time Series Analysis

### 6.1 Smoothing and Gap-filling

```python
from scipy.signal import savgol_filter
import numpy as np

def savitzky_golay_smooth(ts: np.ndarray, window: int = 7,
                           polyorder: int = 3) -> np.ndarray:
    """
    Savitzky-Golay smoothing for vegetation time series.
    Preserves peaks and troughs better than moving averages.
    Reference: Chen et al. (2004) RSE 91(3-4):332
    """
    return savgol_filter(ts, window_length=window, polyorder=polyorder)

def harmonic_regression(t: np.ndarray, y: np.ndarray,
                         n_harmonics: int = 3) -> np.ndarray:
    """
    Harmonic regression for seasonality modelling (phenology).
    Reference: Zhu & Woodcock (2014) RSE 144:152
    """
    X = [np.ones_like(t), t]
    for k in range(1, n_harmonics + 1):
        X.append(np.cos(2 * np.pi * k * t / 365))
        X.append(np.sin(2 * np.pi * k * t / 365))
    X = np.column_stack(X)
    coeffs, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return X @ coeffs
```

### 6.2 Temporal Frequency Metrics

```python
def temporal_frequency(stack: np.ndarray, class_value: int,
                        nodata: int = 0, axis: int = 0) -> np.ndarray:
    """
    Compute the relative frequency of a class in a time series.
    Reference: Defries et al. (2004); Hansen et al. (2013) Science
    """
    valid_mask = stack != nodata
    class_mask = stack == class_value
    return np.where(
        valid_mask.sum(axis=axis) > 0,
        class_mask.sum(axis=axis) / valid_mask.sum(axis=axis),
        np.nan)

def temporal_stability_index(stack: np.ndarray, nodata: int = 0,
                               axis: int = 0) -> np.ndarray:
    """
    Temporal stability index (dominance of the most frequent class).
    Reference: Pérez-Hoyos et al. (2017) Remote Sensing 9(1):2
    """
    from scipy.stats import mode
    dominant_class, dominant_count = mode(stack, axis=axis)
    valid_count = (stack != nodata).sum(axis=axis)
    return np.where(valid_count > 0, dominant_count / valid_count, np.nan)
```

---

## 7. ML/DL Classification

### 7.1 Spatial Validation (No Data Leakage)

```python
# ⚠️ NEVER use random split with spatial data — spatial autocorrelation
# will inflate accuracy. Use block spatial cross-validation.

from sklearn.model_selection import KFold
import geopandas as gpd

def spatial_block_cv(gdf: gpd.GeoDataFrame, n_splits: int = 5,
                     block_size_km: float = 50.0):
    """
    Cross-validation with spatial blocks to avoid data leakage.
    Reference: Roberts et al. (2017) Ecography 40(8):913
    
    Alternative: use scikit-spatial-models or spatial-cross-val.
    """
    # Generates a block grid over the dataset extent
    # and creates folds based on blocks (not samples)
    raise NotImplementedError("See implementation by Roberts et al. 2017")
```

### 7.2 Classification Quality Checklist

```yaml
preprocessing:
  - [ ] Proper normalisation for RS (divide by 10000 for Landsat/S2 SR)
  - [ ] Balanced classes or class_weight handling
  - [ ] Spatially consistent augmentation (flips, rotations)
  - [ ] Bands in the correct order and documented

training:
  - [ ] Spatial cross-validation (not random split)
  - [ ] Per-class metrics: IoU, F1, precision, recall
  - [ ] Confusion matrix with % and absolutes
  - [ ] Learning curves plotted

validation:
  - [ ] Independent samples (not used in fit)
  - [ ] Stratified by class + region
  - [ ] Area-adjusted accuracy (Olofsson et al. 2014)
```

---

## 8. LULC Ensemble Methods

```python
def majority_vote_ensemble(products: list[np.ndarray],
                            nodata: int = 0) -> np.ndarray:
    """
    Simple majority voting among multiple products.
    Reference: Herold et al. (2011) RSE 115(6):1559
    """
    stack = np.stack(products, axis=0)
    from scipy.stats import mode
    result, _ = mode(stack, axis=0)
    return result.squeeze()

def weighted_ensemble(products: list[np.ndarray],
                      weights: list[float]) -> np.ndarray:
    """
    Weighted ensemble by product confidence (one-hot + weighted sum).
    Reference: Fritz et al. (2011) ERL 6(4):044005
    """
    raise NotImplementedError("Requires one-hot encoding of categories")
```

---

## 9. Inter-Product Agreement Metrics

```python
import numpy as np
from sklearn.metrics import cohen_kappa_score

def overall_accuracy(y_true, y_pred):
    """Proportion of agreeing pixels."""
    return np.mean(y_true == y_pred)

def cohens_kappa(y_true, y_pred):
    """Chance-corrected kappa — Cohen (1960)."""
    return cohen_kappa_score(y_true, y_pred)

def dice_coefficient(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
    """Dice/Sørensen coefficient for binary classes."""
    intersection = np.logical_and(mask_a, mask_b).sum()
    return 2 * intersection / (mask_a.sum() + mask_b.sum() + 1e-8)
```

---

## 10. Accuracy Assessment (Olofsson 2014)

```python
def area_adjusted_accuracy(confusion_matrix: np.ndarray,
                            mapped_areas: np.ndarray,
                            sample_counts: np.ndarray) -> dict:
    """
    Area-adjusted accuracy and area estimates (design-based).
    
    Reference: Olofsson et al. (2014) RSE 148:42
    REQUIRED for land use/cover change studies.
    
    Args:
        confusion_matrix: (n_classes × n_classes) sample counts
        mapped_areas: mapped area per class (same units)
        sample_counts: samples collected per stratum
    
    Returns:
        dict with adjusted OA, UA, PA, F1 + confidence intervals
    """
    # Implementation following equations 1-5 of Olofsson et al. (2014)
    raise NotImplementedError("Use `area` package or reference implementation")

# Olofsson 2014 CHECKLIST:
# [ ] Stratified sampling (strata = mapped classes)
# [ ] Sample size per stratum documented
# [ ] Confusion matrix in area proportions (not raw counts)
# [ ] Uncertainty (95% CI) reported for OA, UA, PA
# [ ] Estimated area with standard error and CI
```

---

## 11. LULC Products — Reference Tables

### 11.1 Common Class Hierarchy

| Class | MapBiomas | CGLS | ESRI | GLAD |
|-------|-----------|------|------|------|
| Forest | 1 | 111,112,113 | 2 | 1 |
| Savanna / Cerrado | 3 | 121,122 | — | 3 |
| Agriculture | 18,39,20,21 | 40 | 5 | 6 |
| Grassland | 15 | 30 | 7 | 4 |
| Urban | 24,25 | 50 | 7 | 7 |
| Water | 33 | 80 | 1 | 8 |
| Bare Soil | 22,23 | 200 | 8 | — |

### 11.2 Resolution and Temporal Coverage

| Product | Spatial Resolution | Temporal Resolution | Coverage |
|---------|--------------------|---------------------|----------|
| MapBiomas | 30m (Landsat) | Annual (1985–present) | Brazil + South America |
| CGLS-LC100 | 100m | Annual (2015–2019) | Global |
| ESRI Land Cover | 10m (Sentinel-2) | Annual (2017–present) | Global |
| GLAD ARD | 30m (Landsat) | Annual (2000–present) | Global |
| ESA WorldCover | 10m (Sentinel-1+2) | 2020, 2021 | Global |

---

## 12. Quality Checklist for RS Analysis

### Preprocessing
- [ ] CRS verified and consistent across all products
- [ ] Spatial resolution aligned (reprojection with appropriate method)
- [ ] Nodata handled explicitly (do not assume 0 = nodata)
- [ ] Geographic extent equal for all products
- [ ] Atmospheric correction documented and consistent with sensor

### Agreement Analysis / Validation
- [ ] Reclassification dictionary documented and versioned
- [ ] Area-adjusted accuracy (Olofsson 2014)
- [ ] Spatial cross-validation (not random)
- [ ] 95% CI for all reported metrics
- [ ] Sample N reported with metrics

### Time Series
- [ ] Cloud/shadow mask applied before smoothing
- [ ] Smoothing method justified (Savitzky-Golay vs Whittaker vs harmonic)
- [ ] Gap-filling documented
- [ ] Seasonality visually inspected

### ML/DL
- [ ] Spatial cross-validation (not random split)
- [ ] Normalisation consistent between training and inference
- [ ] Class balancing documented
- [ ] Overfitting checked (train vs val curves)

---

## 13. Data Sources and APIs

```yaml
# Scientific literature
semantic_scholar_api: "https://api.semanticscholar.org/graph/v1/paper/search?query={TERM}&fields=title,authors,year,abstract,citationCount"
crossref_api:         "https://api.crossref.org/works?query={TERM}&filter=type:journal-article,from-pub-date:2018"
mdpi_remote_sensing:  "https://www.mdpi.com/search?q={TERM}&journal=remotesensing"
eartharxiv:           "https://eartharxiv.org/search/?q={TERM}"

# Product documentation
mapbiomas_github:     "https://github.com/mapbiomas"
copernicus_land:      "https://land.copernicus.eu/global"
glad_umd:             "https://glad.umd.edu/dataset"
esa_worldcover:       "https://esa-worldcover.org"

# Data and catalogs
earthengine_catalog:  "https://developers.google.com/earth-engine/datasets"
stac_planetary:       "https://planetarycomputer.microsoft.com/catalog"
stac_element84:       "https://earth-search.aws.element84.com/v1"
usgs_earthexplorer:   "https://earthexplorer.usgs.gov"
copernicus_hub:       "https://scihub.copernicus.eu"
```

---

## STAC MCP Server Integration

### Discover and Query Satellite Data via MCP

The STAC (SpatioTemporal Asset Catalogs) protocol can be accessed through MCP servers, enabling programmatic satellite data discovery.

```python
# Query STAC catalog via MCP tools
stac_query = {
    "collections": ["sentinel-2-l2a", "landsat-c2-l2"],
    "bbox": [-64.5, -12.5, -64.3, -12.3],  # Rondônia, Brazil
    "datetime": "2025-01-01/2025-12-31",
    "max_cloud_cover": 20
}

# Via MCP STAC server
items = await stac_search(stac_query)

# Returns list of items with: 
# - scene_id, datetime, cloud_cover, geometry
# - assets: B02, B03, B04, B08, B11, SCL, etc.
# - eo:bands with common names, center wavelength
```

### Earth Engine Integration via MCP

```python
# Google Earth Engine computation via MCP
gee_task = {
    "collection": "LANDSAT/LC08/C02/T1_L2",
    "region": {
        "type": "Point",
        "coordinates": [-64.4, -12.4]
    },
    "reducers": ["median"],
    "bands": ["SR_B4", "SR_B5"],  # Red, NIR
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "scale": 30
}

# Compute NDVI directly in Earth Engine
ndvi_result = await ee_compute_ndvi(gee_task)
# Returns computed raster data as GeoTIFF reference
```

### STAC Browser Pattern for Data Discovery

```python
# MCP-based STAC browser facade
class STACBrowser:
    """Discover satellite data across multiple catalogs via MCP."""
    
    CATALOGS = {
        "earthsearch": "https://earth-search.aws.element84.com/v1",
        "planetary_computer": "https://planetarycomputer.microsoft.com/api/stac/v1",
        "copernicus": "https://catalogue.dataspace.copernicus.eu/stac",
    }
    
    async def search_all(self, aoi: dict, date_range: tuple[str, str]) -> list[dict]:
        """Search across all catalogs in parallel."""
        results = await asyncio.gather(*[
            self._search_catalog(catalog, aoi, date_range)
            for catalog in self.CATALOGS
        ], return_exceptions=True)
        return self._merge_results(results)
```

## Automated Literature Review with LLM

### Paper Discovery & Synthesis

```python
class LiteratureReviewAgent:
    """Automated literature discovery and synthesis for remote sensing."""
    
    @staticmethod
    async def search_papers(topic: str, max_results: int = 20) -> list[dict]:
        """Search across academic sources for relevant papers."""
        # Uses Semantic Scholar API
        # Uses arXiv API  
        # Uses CrossRef API
        # All accessed via MCP search tools
        pass
    
    @staticmethod
    async def synthesize_findings(papers: list[dict], focus: str) -> str:
        """Synthesize multiple papers into a coherent summary focused on a topic."""
        # LLM reads abstracts and full text where available
        # Produces structured synthesis: methods, results, limitations
        # Cross-references findings with current codebase patterns
        pass
```

### Methodology Recommendation Engine

```python
class MethodologyRecommender:
    """Recommend remote sensing methodologies based on problem description."""
    
    PROBLEM_PROMPT = """Given this remote sensing problem:
    
Problem: {problem_description}
Available data: {data_description}
Study area: {study_area}
    
Research and recommend:
1. Best classification/regression approach for this context
2. Preprocessing steps required
3. Accuracy assessment methodology (Olofsson 2014 stratified)
4. Inter-product agreement strategy if using multiple LULC products
5. Relevant papers and their key findings
"""
    # Uses LLM to search literature and synthesize recommendations
    # Cross-validates against known best practices in the codebase
```
 
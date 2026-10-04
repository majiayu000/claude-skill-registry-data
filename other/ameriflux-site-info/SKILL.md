---
name: ameriflux-site-info
description: Extract AmeriFlux site metadata and map it to EcoSIM JSON variables. Use when a task needs site latitude, longitude, elevation, mean annual temperature, Koppen climate code, or vegetation type for an AmeriFlux site ID or flux-site name.
---

# AmeriFlux Site Info Extractor

## Use When

- You need EcoSIM site metadata for an AmeriFlux site ID such as `US-Ha1`.
- You need to map flux-site attributes into `ALATG`, `ALONG`, `ALTIG`, `ATCAG`, `IETYPG`, or `IXTYP1`.
- You are building site-level inputs before climate, atmospheric chemistry, or soil extraction.

## Constraints
- NEVER use it extract climate data.

## Purpose
Automate the identification and derivation of site-specific attributes (e.g., location, vegetation) from AmeriFlux site pages and map the extracted values to EcoSIM variables. The bundled script uses cached EcoSIM site JSON first, then structured AmeriFlux page text or rendered DOM extraction when a refresh is needed.

## Workflow

1. Resolve the AmeriFlux site ID or site name.
2. Load existing `result/<SITE_ID>/<SITE_ID>_ecosim_site.json` metadata when present.
3. Extract latitude, longitude, elevation, mean annual temperature, Koppen-Geiger code, and IGBP vegetation type.
4. Map the extracted values to EcoSIM JSON variables and write under `result/<SITE_ID>/`.
5. Check units: latitude/longitude are decimal degrees, elevation is meters, and temperature is degrees Celsius.

## Metadata Extraction Policy

Use deterministic sources in this order:

1. Existing local EcoSIM site metadata JSON.
2. AmeriFlux siteinfo HTML fetched with Python standard library URL tools, or `requests` when available.
3. Rendered AmeriFlux DOM text fetched with Playwright if the static HTML is incomplete.

Always inspect the extracted values for physical and ecological plausibility before using them in EcoSIM inputs.

## 1. Site Metadata Extraction (Flux Network)
Given an AmeriFlux site name or ID (e.g., "Blodgett Forest" or "US-Blo"), read cached metadata or parse the rendered AmeriFlux site page text, then map the extracted values to the required EcoSIM JSON variables.

| JSON Variable | Source Attribute | Description |
| :--- | :--- | :--- |
| **ALATG** | Site Latitude | Decimal degrees north. |
| **ALONG** | Site Longitude | Decimal degrees east. |
| **ALTIG** | Elevation | Meters above sea level. |
| **ATCAG** | MAT | Mean Annual Temperature (°C). |
| **IETYPG** | Climate Class | Koppen-Geiger climate zone code. |
| **IXTYP1** | IGBP Type | Dominant vegetation type (mapped to plant litter flags). |

**Logic for Vegetation Mapping:**
* If IGBP is **ENF** (Evergreen Needleleaf) → Set `IXTYP1` to **9** or **11** (Coniferous).
* If IGBP is **DBF** (Deciduous Broadleaf) → Set `IXTYP1` to **8** or **10** (Deciduous).

**Koppen climate classification mapping:**
Using the `koppenDict` mapping, convert the site's Koppen-Geiger code (e.g., "Csa") to the corresponding integer code for `IETYPG`. This will allow the model to apply appropriate climate-specific parameters during simulations.

koppenDict = {
    "Af":  11,
    "Am":  12,
    "As":  13,
    "Aw":  14,
    "BWk": 21,
    "BWh": 22,
    "BSk": 26,
    "BSh": 27,
    "Cfa": 31,
    "Cfb": 32,
    "Cfc": 33,
    "Csa": 34,
    "Csb": 35,
    "Csc": 36,
    "Cwa": 37,
    "Cwb": 38,
    "Cwc": 39,
    "Dfa": 41,
    "Dfb": 42,
    "Dfc": 43,
    "Dfd": 44,
    "Dsa": 45,
    "Dsb": 46,
    "Dsc": 47,
    "Dsd": 48,
    "Dwa": 49,
    "Dwb": 50,
    "Dwc": 51,
    "Dwd": 52,
    "ET": 61,
    "EF": 62
}
## 2. Implementation & Execution

### Prerequisites
* **Python 3.8+**
* **requests**: Optional HTTP fetch helper; the script also has a standard-library HTTP fallback.
* **Playwright**: Optional fallback for rendered DOM extraction when static HTML is incomplete.

### Setup for the Bundled Local Script
```bash
pip install playwright requests
playwright install chromium
```

No local vision service is required.

## Usage
To execute the skill, run the following command from the project root. The resulting JSON will be saved under `./result/<SITE_ID>/` by default:

```bash
python .agents/skills/ameriflux-site-info/extract_ameriflux_site_data.py <SITE_ID>
```

Example:
```bash
python .agents/skills/ameriflux-site-info/extract_ameriflux_site_data.py US-Ha1
```

To bypass cached metadata and refresh from AmeriFlux:
```bash
python .agents/skills/ameriflux-site-info/extract_ameriflux_site_data.py US-Ha1 --force-refresh
```

## Output

The script creates a JSON file named `result/<SITE_ID>/<site_name>_ecosim_site.json` with the following structure:

```jsonc
{
  "site_name": "US-Ha1",
  "ALATG": 40.0,      # Latitude (decimal degrees north)
  "ALONG": -120.0,    # Longitude (decimal degrees east)
  "ALTIG": 1000.0,    # Elevation (meters above sea level)
  "ATCAG": 10.0,      # Mean Annual Temperature (°C)
  "IETYPG": 34,       # Koppen climate zone code
  "IXTYP1": 10        # Vegetation type code
}
```

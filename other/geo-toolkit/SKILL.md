---
name: geo-toolkit
description: Parse, convert, geocode, visualize, and measure geographic data. Use for address cleanup, geo file conversion, mapping, and distance workflows.
---

# Geo Toolkit

Use this suite for practical geographic data preparation and inspection.

## Included Tools

- `address_parser.py`
- `distance_calc.py`
- `geo_visualizer.py`
- `geocoder.py`
- `kml_geojson_converter.py`
- `territory_mapper.py`

## Workflow

1. Determine whether the task is parsing, conversion, lookup, measurement, or visualization.
2. Normalize addresses or file formats before doing downstream mapping work.
3. Use the smallest tool that solves the request and return any geocoding or projection caveats.

## Guardrails

- Treat geocoding results as approximate unless the source data is already precise.
- Call out coordinate system or file-format assumptions when converting map artifacts.

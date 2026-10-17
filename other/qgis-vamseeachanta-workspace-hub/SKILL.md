---
name: qgis
version: 1.0.0
category: engineering/gis
description: "QGIS AI Interface Skill \u2014 PyQGIS headless automation, Processing\
  \ framework, vector/raster I/O, CRS transforms, well plotting from CSV, failure\
  \ diagnosis"
type: reference
tags:
- qgis
- gis
- geospatial
- pyqgis
- vector
- raster
- crs
- coordinate-systems
- well-locations
platforms:
- linux
- windows
- macos
invocation: qgis
capabilities:
- input-generation
- execution
- output-parsing
- failure-diagnosis
- validation
requires: []
updated: '2026-02-24'
scripts_exempt: true
---

# Qgis

## When to Use This Skill

- Plot well locations from CSV files with lat/lon coordinates
- Reproject vector/raster data between coordinate systems (WGS84, UTM)
- Run QGIS Processing algorithms headlessly (no GUI)
- Perform spatial joins, buffer analysis, and overlay operations
- Export map layouts to PDF, PNG, SVG
- Batch process shapefiles or GeoPackages via PyQGIS scripting

---

## Sub-Skills

- [1.1 PyQGIS Application Bootstrap (Headless) (+2)](11-pyqgis-application-bootstrap-headless/SKILL.md)
- [2.1 qgis_process CLI (Headless) (+2)](21-qgisprocess-cli-headless/SKILL.md)
- [3.1 Read Features from Output Layer (+2)](31-read-features-from-output-layer/SKILL.md)
- [4. FAILURE DIAGNOSIS](4-failure-diagnosis/SKILL.md)
- [Checklist (+2)](checklist/SKILL.md)

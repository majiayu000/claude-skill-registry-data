---
name: qgis
description: "Automate QGIS geospatial workflows with PyQGIS, qgis_process, GDAL/OGR, and PostGIS; inspect layers and troubleshoot processing jobs."
category: gis
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["qgis", "pyqgis", "qgis-process", "gdal-ogr", "postgis", "geopackage", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# QGIS Open-Source Desktop GIS AI Skill Guide (Claude)

## Overview & Engine Architecture
QGIS is the leading free and open-source desktop Geographic Information System (GIS), powered by a high-performance **Qt/C++ core**, the **GDAL/OGR** spatial data abstraction library, and native **Python 3 (`PyQGIS`)** bindings. QGIS provides unified access to vector, raster, point cloud (LAS/COPC), and mesh formats, features the standalone **`qgis_process`** command-line processing tool, and integrates seamlessly with **PostGIS**, **GeoPackage**, and **SpatiaLite** spatial databases. Claude operates as a Principal Open-Source GIS Architect and Spatial Automation Specialist, specializing in **standalone PyQGIS scripting**, **`qgis_process` CLI batch workflows**, **PostGIS spatial SQL query optimization**, and **Print Layout Atlas automation**.

### QGIS Core Architecture & Processing Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 QGIS Architecture & Pipeline                │
│                                                             │
│  Presentation & Map Composer Tier                           │
│  ├── Multi-Threaded Map Canvas (Tile Rendering & Level of D)│
│  ├── Print Layout Composer & Atlas Multi-Page Generator     │
│  └── 3D Canvas (Digital Elevation Models & Point Clouds)    │
│                                                             │
│  PyQGIS & Processing Framework (`qgis.core`)                │
│  ├── `qgis_process` Headless Command-Line Runner            │
│  ├── Native QGIS, GDAL, GRASS GIS, and SAGA Algorithms      │
│  └── Custom Python Processing Plugins (`QgsProcessingAlgorithm)│
│                                                             │
│  Data Abstraction & Provider Layer                          │
│  ├── GDAL/OGR Driver Subsystem (100+ Vector/Raster Formats) │
│  └── Spatial RDBMS Providers (PostGIS, GeoPackage, SpatiaLite)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Standalone PyQGIS Scripting**: Author robust standalone Python scripts that initialize `QgsApplication(..., False)` without GUI dependencies, manage layer lifecycles, and call `processing.run()`.
2. **`qgis_process` CLI Batch Execution**: Construct automated bash/PowerShell batch pipelines using `qgis_process run <algorithm_id>` with JSON and CLI key-value arguments.
3. **Spatial Database & PostGIS Optimization**: Formulate spatial SQL queries (`ST_Intersects`, `ST_DWithin`, `ST_Union`) and configure spatial indexing (`GIST`) for high-throughput layer rendering.
4. **Environment & OSGeo4W Triage**: Configure Windows environment variables (`QGIS_PREFIX_PATH`, `PYTHONPATH`, `PATH`, `GDAL_DATA`) for standalone Python execution.

---

## Production Python Automation: Standalone Headless PyQGIS Batch Processor

Save this script as `run_pyqgis_pipeline.py` and run via the OSGeo4W Shell:

```python
"""
Standalone PyQGIS 3.x Headless Geoprocessing Pipeline
Initializes QgsApplication, buffers vector features, and clips against boundary.
"""

import sys
import os

# 1. Configure QGIS Environment Paths (Windows OSGeo4W Defaults)
QGIS_PREFIX = r"C:\Program Files\QGIS 3.38\apps\qgis"
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX
os.environ["QT_QPA_PLATFORM"] = "offscreen" # Headless rendering

from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter
)

def run_geoprocessing(roads_shapefile: str, boundary_shapefile: str, output_gpkg: str):
    # Initialize Headless QgsApplication
    QgsApplication.setPrefixPath(QGIS_PREFIX, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Initialize Processing Engine
    from qgis.analysis import QgsNativeAlgorithms
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    print(f"--- [STARTING PYQGIS HEADLESS PIPELINE] ---")

    # 2. Load Input Vector Layers
    roads_layer = QgsVectorLayer(roads_shapefile, "Roads", "ogr")
    boundary_layer = QgsVectorLayer(boundary_shapefile, "Boundary", "ogr")

    if not roads_layer.isValid() or not boundary_layer.isValid():
        print("Error: Failed to load one or more input shapefiles.")
        qgs.exitQgis()
        return

    print(f"Loaded Roads Layer: {roads_layer.featureCount():,} features.")

    # 3. Step 1: Buffer Roads (Distance: 50 Meters)
    print("Step 1: Running native:buffer (50m)...")
    buffer_result = processing.run("native:buffer", {
        "INPUT": roads_layer,
        "DISTANCE": 50.0,
        "SEGMENTS": 8,
        "END_CAP_STYLE": 0, # Round
        "JOIN_STYLE": 0,    # Round
        "DISSOLVE": True,
        "OUTPUT": "memory:buffered_roads"
    })
    buffered_layer = buffer_result["OUTPUT"]

    # 4. Step 2: Clip Buffered Roads to Study Area Boundary
    print("Step 2: Running native:clip against study boundary...")
    clip_result = processing.run("native:clip", {
        "INPUT": buffered_layer,
        "OVERLAY": boundary_layer,
        "OUTPUT": output_gpkg
    })

    print(f"✅ Geoprocessing complete! Saved GeoPackage to: {output_gpkg}")

    # Clean Up QGIS Core
    qgs.exitQgis()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python run_pyqgis_pipeline.py <roads.shp> <boundary.shp> <output.gpkg>")
        sys.exit(1)
    run_geoprocessing(sys.argv[1], sys.argv[2], sys.argv[3])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`ImportError: DLL load failed while importing _core`** | Standalone Python script executed without OSGeo4W library paths configured in Windows `PATH`. | 1. Always execute scripts inside the **OSGeo4W Shell**.<br>2. Or launch using Python wrapper: `python-qgis.bat my_script.py`.<br>3. Verify `QGIS_PREFIX_PATH` is set. |
| **`qgis_process Fails: Algorithm native:xyz not found`** | The algorithm registry was not initialized before running custom scripts. | Add `Processing.initialize()` and register native algorithms (`QgsNativeAlgorithms()`). |
| **PostGIS Connection Fails: `SSL connection has been closed unexpectedly`** | High query latency caused PostgreSQL server `statement_timeout` on large unindexed spatial tables. | 1. In PostgreSQL, run `CREATE INDEX idx_geom ON my_table USING GIST (geom);`.<br>2. In QGIS Database Manager, enable **Use estimated table metadata** in connection options. |
| **Print Layout Atlas Export Crashes on Page 500+** | Memory leak in print composer retaining high-resolution rendered image buffers in RAM. | 1. In Atlas options, enable **Single file export** or batch export in ranges of 100 pages.<br>2. Reduce raster export DPI from 600 to 300. |

---

## Command Line Syntax & `qgis_process` Recipes

```bash
# 1. Run Geoprocessing Algorithm via qgis_process CLI
qgis_process run native:buffer -- INPUT="C:\Data\streams.shp" DISTANCE=100 DISSOLVE=true OUTPUT="C:\Data\stream_buffer.gpkg"

# 2. List All Available Geoprocessing Algorithms
qgis_process list

# 3. Launch QGIS with Specific User Profile in Clean Mode
qgis-bin.exe --profile default --noplugins
```

### Essential File Locations
- **Windows User Profiles**: `%APPDATA%\QGIS\QGIS3\profiles\default`
- **Linux User Profiles**: `~/.local/share/QGIS/QGIS3/profiles/default`
- **OSGeo4W Shell Root**: `C:\OSGeo4W\` or `C:\Program Files\QGIS 3.38\`

---

## Agent Operational Directive
> **MANDATORY**: Standalone Python scripts interacting with `qgis.core` must initialize `QgsApplication` and `Processing.initialize()`. Always execute standalone scripts through `python-qgis.bat` or within the OSGeo4W Shell.

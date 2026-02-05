---
name: qgis
description: >
  Geospatial analysis and GIS operations via QGIS. Use for calculating distances,
  buffering zones, coordinate transforms (EPSG:4326 to EPSG:3857), layer operations,
  geoprocessing (intersect, union, clip), and exporting map images. Requires QGIS
  running on Display :1 with MCP plugin enabled.
version: 2.0.0
author: turbo-flow-claude
mcp_server: true
protocol: fastmcp
entry_point: mcp-server/server.py
port: 9877
dependencies:
  - qgis
---

# QGIS Skill

Geospatial analysis and GIS operations via FastMCP protocol, communicating with QGIS instance via TCP socket.

## When to Use This Skill

- Calculate distances between geographic points
- Create buffer zones around features (proximity analysis)
- Transform coordinates between CRS (GPS to Web Mercator)
- Load and manipulate geospatial layers (Shapefile, GeoJSON, GeoPackage)
- Perform geoprocessing operations (intersect, union, difference, clip)
- Export map images for reports or web display
- Query features with spatial filters
- Style layers with categorized or graduated symbology

## Architecture

```text
┌─────────────────────────────┐
│  Claude Code / VisionFlow   │
│  (MCP Client)               │
└──────────────┬──────────────┘
               │ MCP Protocol (stdio)
               ▼
┌─────────────────────────────┐
│  QGIS MCP Server (FastMCP)  │
│  Port: stdio                │
└──────────────┬──────────────┘
               │ TCP Socket
               ▼
┌─────────────────────────────┐
│  QGIS Desktop (Display :1)  │
│  MCP Plugin on Port 9877    │
└─────────────────────────────┘
```

## Tools

| Tool                    | Description                                                 |
| ----------------------- | ----------------------------------------------------------- |
| `load_layer`            | Load geospatial layer (Shapefile, GeoJSON, GeoPackage, WMS) |
| `buffer_analysis`       | Create buffer zones around features                         |
| `calculate_distance`    | Calculate distance between two points                       |
| `transform_coordinates` | Transform between coordinate systems                        |
| `export_map`            | Export map view as PNG, JPG, or PDF                         |
| `query_features`        | Query layer features with filter expression                 |
| `list_layers`           | List all loaded layers                                      |
| `set_layer_style`       | Apply styling (simple, categorized, graduated)              |
| `geoprocessing`         | Intersect, union, difference, dissolve, clip                |
| `get_layer_extent`      | Get bounding box of a layer                                 |
| `health_check`          | Verify QGIS connection                                      |

## Examples

```python
# Load a GeoJSON layer
load_layer({
    "path": "/data/cities.geojson",
    "name": "Cities"
})

# Create 10km buffer around points
buffer_analysis({
    "layer_name": "Cities",
    "distance": 10000,  # meters
    "output_name": "city_buffers"
})

# Transform GPS coordinates to Web Mercator
transform_coordinates({
    "coordinates": [-122.4194, 37.7749],  # San Francisco
    "source_crs": "EPSG:4326",
    "target_crs": "EPSG:3857"
})

# Export map image
export_map({
    "output_path": "/output/map.png",
    "width": 1920,
    "height": 1080,
    "dpi": 150
})
```

## Environment Variables

| Variable       | Default     | Description               |
| -------------- | ----------- | ------------------------- |
| `QGIS_HOST`    | `localhost` | QGIS MCP plugin host      |
| `QGIS_PORT`    | `9877`      | QGIS MCP plugin port      |
| `QGIS_TIMEOUT` | `60`        | Socket timeout in seconds |

## Troubleshooting

**Connection refused:**

```bash
# Check QGIS is running on Display :1
supervisorctl status qgis

# Verify MCP plugin is loaded
# In QGIS: Plugins → Manage Plugins → Search "MCP"
```

## VisionFlow Integration

This skill exposes `qgis://capabilities` and `qgis://status` resources for discovery by VisionFlow's MCP TCP client.

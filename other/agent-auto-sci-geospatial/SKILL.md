---
name: agent-auto-sci-geospatial
description: "地理空间科学与遥感子 skill。用于 GIS、GeoPandas、栅格/矢量处理、CRS 审计、空间连接、缓冲区、网络可达性、OSM、遥感指数、LCZ、热暴露、绿地暴露、空间公平、空间机器学习、地图合规和论文地图设计。触发于 geospatial、GIS、remote sensing、GeoPandas、rasterio、spatial accessibility、green exposure、heat exposure、network analysis 等任务。"
---

# Agent Auto Sci Geospatial

Use this subskill for spatial data, maps, and exposure/accessibility workflows.

## Fast Workflow

1. Inventory all spatial layers and CRS.
2. Separate vector, raster, network, remote-sensing, and tabular sources.
3. Reproject before distance/area/network calculations.
4. Define exposure, accessibility, availability, quality, and use separately.
5. Run spatial analysis with reproducible code and sensitivity checks.
6. Design maps for evidence, not decoration.
7. For China locator maps, check standard map compliance before final figures.

Read `references/geospatial_remote_sensing_workflows.md`.

For full paper projects, this skill owns spatial data discovery, download planning, CRS/geometry audit, OSM/network accessibility, green/heat exposure indicators, LCZ/remote-sensing preprocessing, spatial equity metrics, map compliance, and handoff to analysis and figure-writing agents. It should produce explicit data paths, assumptions, and sensitivity checks.

For deeper K-Dense-style encapsulation:

- `references/k_dense_geospatial_mapping.md`: how GeoPandas, geomaster, raster/vector, remote sensing, and spatial workflow skills are adapted.
- `references/sport_geography_spatial_playbook.md`: sport park/facility accessibility, green/heat exposure, equity, LCZ, OSM, and China map-compliance playbook.

## Related Helper Skills

- `geomaster`
- `geopandas`
- `networkx`
- `agent-auto-sci-data-viz`
- `sport-geography-sci-writing`
- `sport-geography-review-bibliometric`

## Must Not Do

- Do not calculate distance or area in unprojected geographic CRS.
- Do not equate proximity with actual use.
- Do not treat LCZ, NDVI, or park area as interchangeable exposure metrics.
- Do not use unofficial China locator maps for publication figures.


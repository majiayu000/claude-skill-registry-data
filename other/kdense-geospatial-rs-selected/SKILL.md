---
name: kdense-geospatial-rs-selected
description: "精选 K-Dense Scientific Agent Skills 的地理空间科学与遥感工具包。用于 geomaster、GeoPandas、GIS、遥感、矢量/栅格处理、空间分析、空间机器学习和地球观测工作流，并按 Auto-sci-research 的体育设施可达性、绿色暴露、热暴露、LCZ、空间公平和城市健康研究进行封装。"
---

# K-Dense Geospatial / Remote Sensing Selected

This wrapper packages selected Geospatial Science & Remote Sensing skills from `K-Dense-AI/scientific-agent-skills`.

Use it when a task needs library-level or workflow-level support for:

- `geomaster`
- `geopandas`
- vector and raster handling;
- CRS and geometry operations;
- remote-sensing feature workflows;
- spatial analysis and spatial ML implementation details.

## Local Adaptation

Use these upstream skills with local geospatial rules:

1. Check CRS, units, topology, geometry validity, and spatial resolution before analysis.
2. Keep exposure, accessibility, availability, quality, and use conceptually separate.
3. Record buffer/network/travel-time assumptions in methods-ready language.
4. For environmental exposure, state temporal window, season, data product, and aggregation rule.
5. For maps, check legends, classification, scale, north arrow needs, and projection disclosure.

For domain-specific guidance, also read:

- `../agent-auto-sci-geospatial/references/k_dense_geospatial_rs_mapping.md`
- `../agent-auto-sci-geospatial/references/exposure_accessibility_definitions.md`

## Must Not Do

- Do not convert spatial units silently.
- Do not use Euclidean buffers when network access is required without explaining the limitation.
- Do not treat remote-sensing classification output as ground truth without validation.

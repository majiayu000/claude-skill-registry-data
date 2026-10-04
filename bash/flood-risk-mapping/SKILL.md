---
name: flood-risk-mapping
description: >
  Generates urban flood risk maps by combining optical remote sensing water extraction with DEM elevation analysis. Classifies areas into high/medium/low flood risk levels and outputs risk zone maps and governance reports. Invoke when the user mentions "洪涝", "内涝", "洪水风险", "flood risk", "DEM", "水体提取", "NDWI", "城市积水" or similar triggers.
license: MIT
---

# 城市洪涝风险评估技能（flood-risk-mapping）

## 1. 技能概述

本技能结合光学遥感影像的水体提取（NDWI）与数字高程模型（DEM），综合评估城市洪涝风险，生成高/中/低三级风险分区图，辅助城市防洪规划与应急管理。

## 2. 输入要求

| 变量名 | 类型 | 是否必需 | 说明 |
|--------|------|---------|------|
| `image_optical` | file (GeoTIFF) | 是 | 光学影像（多波段，用于 NDWI 水体提取），建议 Sentinel-2 |
| `dem` | file (GeoTIFF) | 是 | 数字高程模型（单位：米），建议 SRTM 30m 或更高精度 |
| `aoi` | file (GeoJSON / Shapefile) | 否 | 关注区域边界 |
| `water_threshold` | float | 否 | 水体提取 NDWI 阈值，默认 0.2 |

## 3. 处理流程

1. **输入校验**：`--action check-inputs`
2. **水体提取**：基于 NDWI 提取现有水体范围
3. **高程分析**：基于 DEM 分位数划分低洼区域
4. **风险综合评估**：低洼区 + 水体邻近区 = 高风险
5. **成果输出**：risk_map.tif、water_mask.tif、risk_zones.geojson、flood_stats.csv、report.md

## 4. 调用示例

```bash
python /home/ubuntu/skills/flood-risk-mapping/scripts/main.py \
  --action run \
  --inputs-json '{"image_optical":"/path/to/sentinel2.tif","dem":"/path/to/srtm.tif"}' \
  --output-dir /tmp/outputs/frm
```

## 5. 输出文件

| 文件 | 含义 |
|------|------|
| `risk_map.tif` | 洪涝风险等级栅格（1=低，2=中，3=高） |
| `water_mask.tif` | 水体提取结果 |
| `risk_zones.geojson` | 风险分区矢量，属性含 risk_level、area_m2 |
| `flood_stats.csv` | 各级风险区面积占比统计 |
| `report.md` | 洪涝风险分析与防洪治理建议 |

## 6. 治理场景

- **防洪规划**：识别高风险低洼区，优先建设防洪设施
- **应急管理**：为应急预案提供洪涝风险空间分布
- **城市扩张管控**：限制在高风险区新建重要基础设施
- **海绵城市建设**：高风险区优先推进雨水调蓄工程

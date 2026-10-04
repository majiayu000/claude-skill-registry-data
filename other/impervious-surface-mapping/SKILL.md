---
name: impervious-surface-mapping
description: >
  Extracts impervious surfaces (buildings, roads, parking lots) from optical remote sensing imagery using NDBI or threshold methods. Computes impervious surface ratio and generates coverage maps to support sponge city planning and urban waterlogging risk assessment. Invoke when the user mentions "不透水面", "硬化地面", "海绵城市", "impervious", "NDBI", "建筑覆盖", "城市内涝" or similar triggers.
license: MIT
---

# 不透水面提取技能（impervious-surface-mapping）

## 1. 技能概述

本技能基于光学遥感影像，利用归一化建筑指数（NDBI）或亮度阈值法提取城市不透水面（建筑、道路、停车场等硬化地表），计算不透水率，辅助海绵城市规划与城市内涝风险评估。无真实 GeoTIFF 时自动降级为随机数据模拟模式。

## 2. 输入要求

| 变量名 | 类型 | 是否必需 | 说明 |
|--------|------|---------|------|
| `image_optical` | file (GeoTIFF) | 是 | 高分辨率光学影像（多波段，已完成大气校正），建议 Sentinel-2 或 GF-2 |
| `aoi` | file (GeoJSON / Shapefile) | 否 | 关注区域边界，不提供则使用影像全范围 |
| `method` | string | 否 | `ndbi`（归一化建筑指数）/ `threshold`，默认 `ndbi` |
| `threshold` | float | 否 | 不透水面判定阈值（0-1），默认 0.2 |

## 3. 处理流程

1. **输入校验**：`--action check-inputs`
2. **NDBI 计算**：基于 SWIR 和 NIR 波段计算归一化建筑指数
3. **阈值分割**：提取不透水面二值掩膜
4. **斑块统计**：计算面积、覆盖率等统计指标
5. **成果输出**：impervious_map.tif、impervious_zones.geojson、impervious_stats.csv、report.md

## 4. 调用示例

```bash
python /home/ubuntu/skills/impervious-surface-mapping/scripts/main.py \
  --action run \
  --inputs-json '{"image_optical":"/path/to/sentinel2.tif","method":"ndbi"}' \
  --output-dir /tmp/outputs/ism
```

## 5. 输出文件

| 文件 | 含义 |
|------|------|
| `impervious_map.tif` | 不透水面二值掩膜（0=透水，1=不透水） |
| `impervious_zones.geojson` | 不透水面斑块矢量，属性含 area_m2 |
| `impervious_stats.csv` | 统计指标（覆盖率、斑块数、总面积） |
| `report.md` | 不透水面分析与海绵城市治理建议 |

## 6. 治理场景

- **海绵城市规划**：识别高不透水率区域，优先推进透水铺装改造
- **内涝风险评估**：不透水率与洪涝风险正相关，辅助排水规划
- **城市扩张监测**：追踪不透水面年际变化，评估城市化进程
- **生态红线管控**：监测生态保护区内不透水面侵占情况

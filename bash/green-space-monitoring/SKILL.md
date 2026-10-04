---
name: green-space-monitoring
description: >
  Monitors urban green space coverage changes using NDVI/EVI vegetation indices from multi-temporal remote sensing imagery. Identifies green space loss and gain areas, and generates governance reports. Invoke when the user mentions "绿地", "植被", "NDVI", "绿化", "green space", "EVI", "占绿", "毁绿", "绿地减少" or similar triggers.
license: MIT
---

# 城市绿地监测技能（green-space-monitoring）

## 1. 技能概述

本技能基于多时相多光谱遥感影像，计算 NDVI/EVI 植被指数，监测城市绿地覆盖变化，精准识别绿地减少（占绿、毁绿）和增加区域，输出绿地变化矢量与治理报告。

## 2. 输入要求

| 变量名 | 类型 | 是否必需 | 说明 |
|--------|------|---------|------|
| `image_t1` | file (GeoTIFF) | 是 | 前期多光谱影像（已完成大气校正），≥ 4 波段 |
| `image_t2` | file (GeoTIFF) | 是 | 后期多光谱影像，需与 `image_t1` 同坐标系/分辨率 |
| `aoi` | file (GeoJSON / Shapefile) | 否 | 关注区域边界 |
| `index` | string | 否 | `ndvi` / `evi`，默认 `ndvi` |
| `threshold` | float | 否 | 绿地判定阈值（0-1），默认 0.3 |

## 3. 处理流程

1. **输入校验**：`--action check-inputs`
2. **植被指数计算**：分别计算两期 NDVI/EVI
3. **绿地提取**：按阈值生成两期绿地掩膜
4. **变化分析**：计算绿地增减区域及面积
5. **成果输出**：vi_map_t1/t2.tif、green_loss_zones.geojson、green_stats.csv、report.md

## 4. 调用示例

```bash
python /home/ubuntu/skills/green-space-monitoring/scripts/main.py \
  --action run \
  --inputs-json '{"image_t1":"/path/to/2022.tif","image_t2":"/path/to/2024.tif","index":"ndvi"}' \
  --output-dir /tmp/outputs/gsm
```

## 5. 输出文件

| 文件 | 含义 |
|------|------|
| `vi_map_t1/t2.tif` | 两期植被指数栅格 |
| `green_loss_zones.geojson` | 绿地减少区域矢量 |
| `green_stats.csv` | 绿地覆盖率统计（前后期对比） |
| `report.md` | 绿地变化分析与治理建议 |

## 6. 治理场景

- **违规占绿执法**：识别绿地减少区域，导出点位供执法核查
- **绿地率考核**：量化城市绿地率变化，支撑规划指标考核
- **生态修复评估**：监测绿化工程实施效果
- **城市热岛缓解**：绿地减少区域往往与热岛加剧正相关

---
name: illegal-dumping-detection
description: >
  Identifies suspected illegal dumping sites (bare soil, construction waste) from high-resolution optical imagery using the Bare Soil Index (BSI). Generates suspect site lists with priority levels for enforcement. Invoke when the user mentions "非法倾倒", "渣土", "建筑垃圾", "裸土", "illegal dumping", "BSI", "垃圾堆放", "偷倒" or similar triggers.
license: MIT
---

# 非法倾倒监测技能（illegal-dumping-detection）

## 1. 技能概述

本技能基于高分辨率光学遥感影像，利用裸土指数（BSI）识别疑似非法倾倒渣土、建筑垃圾的区域，生成可疑点位清单与优先级排序，辅助城市管理执法。

## 2. 输入要求

| 变量名 | 类型 | 是否必需 | 说明 |
|--------|------|---------|------|
| `image_optical` | file (GeoTIFF) | 是 | 高分辨率光学影像（建议 GF-2/Pleiades，≥ 4 波段，已完成正射校正） |
| `aoi` | file (GeoJSON / Shapefile) | 否 | 关注区域边界 |
| `bare_soil_threshold` | float | 否 | BSI 判定阈值，默认 0.15 |
| `min_area_m2` | float | 否 | 最小可疑倾倒面积（平方米），默认 50 |

## 3. 处理流程

1. **输入校验**：`--action check-inputs`
2. **BSI 计算**：`BSI = ((SWIR + Red) - (NIR + Blue)) / ((SWIR + Red) + (NIR + Blue))`
3. **阈值提取**：识别高 BSI 裸土区域
4. **小图斑过滤**：滤除低于最小面积的噪声图斑
5. **优先级排序**：按面积大小分配处置优先级
6. **成果输出**：bsi_map.tif、suspect_sites.geojson、suspect_sites.csv、report.md

## 4. 调用示例

```bash
python /home/ubuntu/skills/illegal-dumping-detection/scripts/main.py \
  --action run \
  --inputs-json '{"image_optical":"/path/to/gf2.tif","bare_soil_threshold":0.15}' \
  --output-dir /tmp/outputs/idd
```

## 5. 输出文件

| 文件 | 含义 |
|------|------|
| `bsi_map.tif` | 裸土指数栅格 |
| `suspect_sites.geojson` | 疑似倾倒点位矢量（Point 类型） |
| `suspect_sites.csv` | 点位清单（含坐标、面积、BSI 值、优先级） |
| `report.md` | 非法倾倒统计与执法建议 |

## 6. 治理场景

- **渣土偷倒巡查**：定期扫描重点区域，发现新增裸土点位
- **建筑垃圾监管**：识别未经批准的建筑垃圾堆放点
- **城乡结合部治理**：重点监控城乡结合部的非法倾倒行为
- **执法证据支撑**：遥感影像可作为行政执法的辅助证据

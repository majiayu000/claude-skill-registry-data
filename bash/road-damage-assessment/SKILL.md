---
name: road-damage-assessment
description: >
  ('Detects road surface damage (potholes, cracks, pavement defects) from high-resolution optical imagery using texture anomaly analysis. Generates damage segment maps with severity ratings and health scores. Invoke when the user mentions "道路破损", "路面坑洼", "路面裂缝", "road damage", "pavement', '"路面健康", "道路维修" or similar triggers.')
license: MIT
---

# 道路破损评估技能（road-damage-assessment）

## 1. 技能概述

本技能基于高分辨率光学遥感影像，利用局部纹理异常分析检测道路破损区域（坑洼、裂缝、路面缺陷），输出破损路段分布图、严重程度评级与路面健康评分，辅助道路养护决策。

## 2. 输入要求

| 变量名 | 类型 | 是否必需 | 说明 |
|--------|------|---------|------|
| `image_optical` | file (GeoTIFF) | 是 | 高分辨率光学影像（建议分辨率 ≤ 0.5m，已完成正射校正） |
| `road_network` | file (GeoJSON / Shapefile) | 否 | 道路网络矢量，用于限定分析范围 |
| `aoi` | file (GeoJSON / Shapefile) | 否 | 关注区域边界 |
| `damage_threshold` | float | 否 | 破损判定亮度差异阈值，默认 0.15 |

## 3. 处理流程

1. **输入校验**：`--action check-inputs`
2. **局部纹理分析**：计算局部均值与标准差，识别亮度异常区域
3. **破损提取**：基于阈值生成破损掩膜
4. **严重程度评级**：按面积分为 severe/moderate/minor 三级
5. **健康评分**：计算路段整体健康评分（0-100）
6. **成果输出**：damage_map.tif、damage_segments.geojson、damage_segments.csv、report.md

## 4. 调用示例

```bash
python /home/ubuntu/skills/road-damage-assessment/scripts/main.py \
  --action run \
  --inputs-json '{"image_optical":"/path/to/hr_image.tif","damage_threshold":0.15}' \
  --output-dir /tmp/outputs/rda
```

## 5. 输出文件

| 文件 | 含义 |
|------|------|
| `damage_map.tif` | 破损区域二值掩膜 |
| `damage_segments.geojson` | 破损路段矢量，属性含 severity、health_score |
| `damage_segments.csv` | 破损路段清单 |
| `report.md` | 道路破损统计与维修建议 |

## 6. 治理场景

- **道路养护计划**：自动识别需要维修的路段，优化养护资源分配
- **城市道路普查**：大范围快速评估道路状况
- **灾后道路评估**：暴雨、地震后快速评估道路受损情况
- **道路质量考核**：辅助道路工程质量验收与监管

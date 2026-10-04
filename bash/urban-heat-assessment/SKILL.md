---
name: urban-heat-assessment
description: >
  Quantifies urban heat island (UHI) intensity from thermal-infrared remote sensing,
  identifies high-temperature risk zones and cooling-potential spaces. Invoke when
  the user mentions "urban heat island", "LST", "land surface temperature",
  "热红外", "城市热岛", "高温风险", "降温规划", "极端高温", "热环境" or similar.
  The skill retrieves LST, combines NDVI and building density to grade heat risk,
  and outputs a UHI intensity map, risk-level map, cooling recommendations and
  multi-year trend analysis.
version: 0.1.0
category: urban-governance
domain: remote-sensing
language:
  metadata: en
  report: zh-CN
entrypoint: scripts/main.py
license: MIT
tags: [heat-island, LST, thermal, public-health, cooling]
---

# 城市热环境评估技能（urban-heat-assessment）

## 1. 技能概述

基于热红外遥感影像（TIRS）量化评估城市热岛强度（UHI），识别高温风险区域与降温潜力空间。
支持 Landsat 8/9 TIRS、ECOSTRESS、GF-5 热红外等常见数据源。

## 2. 输入要求

| 变量名 | 类型 | 必需 | 说明 |
|--------|------|:--:|------|
| `thermal_image` | file (GeoTIFF) | 是 | 热红外影像，DN 或辐亮度；若已是 LST（开尔文/摄氏度）请设置 `is_lst=true` |
| `boundary` | file (GeoJSON/Shapefile) | 是 | 城市行政边界（用于计算郊区-城区对比） |
| `ndvi_image` | file (GeoTIFF) | 否 | NDVI 影像，用于辅助热环境分级 |
| `building_density` | file (GeoTIFF) | 否 | 建筑密度栅格（0-1） |
| `is_lst` | bool | 否 | 若输入已经是地表温度则为 true，默认 false |
| `reference_t_c` | number | 否 | 参考阈值（摄氏度），不提供则使用郊区均值 |
| `year` | int | 否 | 数据年份，用于跨年趋势对比 |

## 3. 用户输入引导

> 为完成热环境评估，请提供：
> 1. **热红外影像**（`thermal_image`）：GeoTIFF 格式。Landsat 8/9 的 Band10 即可；如已反演为地表温度，请标注 `is_lst: true`。
> 2. **城市边界**（`boundary`）：GeoJSON 或 Shapefile，用于圈定分析范围并计算城-郊对比。
> 3. （可选）**NDVI 影像**、**建筑密度** 以获得更精准的分级；如无，可仅用 LST。

## 4. 处理流程

1. 校验输入 → `check-inputs`
2. 若输入为 TIRS DN，按 Landsat 公式反演亮温再估算 LST（单窗算法简化版）
3. 提取城市边界内像元；将边界外缓冲区视为"郊区参考"
4. 计算 UHI 强度 = `LST_city - mean(LST_suburb)`
5. 基于 LST 百分位（p50/p75/p90）进行风险分级（低/中/高/极端）
6. 识别"降温潜力斑块"：高 LST + 低 NDVI + 高建筑密度交集
7. 输出成果

## 5. 参数说明（`config.yaml`）

```yaml
algorithm:
  sensor: landsat8            # landsat8 | landsat9 | custom
  band10_K1: 774.8853
  band10_K2: 1321.0789
  emissivity: 0.97
  risk_percentiles: [50, 75, 90]
  suburb_buffer_m: 5000
```

## 6. 调用示例

```bash
python /mnt/skills/custom/remote-sensing/urban-heat-assessment/scripts/main.py \
  --action run \
  --inputs-json '{"thermal_image":"/mnt/user-data/uploads/tirs.tif","boundary":"/mnt/user-data/uploads/city.geojson"}' \
  --output-dir /mnt/user-data/outputs/heat_20260417
```

## 7. 输出文件

| 文件 | 含义 |
|------|------|
| `lst.tif` | 反演后的地表温度（摄氏度） |
| `uhi_intensity.tif` | 热岛强度图（相对郊区均值） |
| `risk_levels.tif` | 风险等级图（1=低，2=中，3=高，4=极端） |
| `cooling_priority.geojson` | 降温潜力重点区域矢量 |
| `report.md` | 评估报告 + 降温建议 + 年际趋势（若有） |

## 8. 治理场景

- 城市降温规划、公园绿地布局优化
- 极端高温公共健康风险预警
- 街区更新热环境改善评估
- "公园城市"热环境指标监测

## 9. 注意事项

- 单幅热红外影像反映**瞬时**热环境，建议使用同一月份多年序列评估趋势
- 降级模式下使用合成 LST，仅用于流程演示
- 单窗算法为简化实现，生产环境建议使用 Jiménez-Muñoz 或 SC 算法

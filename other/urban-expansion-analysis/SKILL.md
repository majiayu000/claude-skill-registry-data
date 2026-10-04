---
name: urban-expansion-analysis
description: >
  Quantifies multi-year urban expansion speed, direction, pattern and land-use
  structure evolution. Invoke when the user mentions "urban expansion",
  "LULC change", "transition matrix", "growth boundary", "compact city",
  "城市扩张", "土地利用变化", "建成区增长", "占补平衡", "转移矩阵", "增长边界"
  or similar. The skill builds land-use transition matrices from multi-year
  classified imagery, computes expansion-intensity indices, identifies
  infill / edge / leapfrog patterns, and provides a simple future projection.
version: 0.1.0
category: territorial-spatial-planning
domain: remote-sensing
language:
  metadata: en
  report: zh-CN
entrypoint: scripts/main.py
license: MIT
tags: [urban-expansion, LULC, transition-matrix, growth-boundary]
---

# 城市扩张与土地利用动态分析（urban-expansion-analysis）

## 1. 技能概述

量化分析城市扩张速度、方向、模式以及土地利用结构演变规律，辅助国土空间规划实施评估、
城市增长边界（UGB）优化与紧凑城市策略制定。

## 2. 输入要求

| 变量名 | 类型 | 必需 | 说明 |
|--------|------|:--:|------|
| `classified_images` | list[file] | 是 | 多个年份的土地利用分类栅格 GeoTIFF（像素值=类别编码） |
| `years` | list[int] | 是 | 与 `classified_images` 同长度的年份列表 |
| `class_mapping` | dict / file | 否 | 类别编码 → 名称映射，不提供则使用默认 |
| `urban_classes` | list[int] | 否 | 被视为"建设用地"的类别编码，默认 `[1]` |
| `city_center` | list[number] | 否 | 城市中心经纬度 `[lon, lat]`，用于方向分析 |
| `ugb` | file (GeoJSON) | 否 | 城市增长边界矢量，用于 UGB 占比分析 |
| `socioeconomic` | file (CSV) | 否 | 年份级社会经济数据（GDP、人口），用于相关性分析 |

默认 `class_mapping`：
```
1=建设用地  2=耕地  3=林地  4=草地  5=水体  6=湿地  7=裸地  8=其他
```

## 3. 用户输入引导

> 为进行城市扩张与土地利用动态分析，请提供：
> 1. **多年土地利用分类图**（`classified_images`）：每年一个 GeoTIFF，像元值代表类别。至少 2 年。
> 2. **年份列表**（`years`）：例如 `[2015, 2020, 2025]`。
> 3. （推荐）**类别编码映射**（`class_mapping`）：使您的数据类别对齐默认体系，否则采用默认。
> 4. （可选）**城市中心点**（`city_center`）：用于分析各方向扩张比例；不提供则自动取影像质心。

## 4. 处理流程

1. `check-inputs`：校验影像数量等于年份数，且像素尺寸一致
2. 对最早/最晚两期计算**土地利用转移矩阵**（多期则逐年成对）
3. **扩张强度指数（EII）**：`ΔUrbanArea_i / TotalArea_i / Years`，>1.92% 为"高速"
4. **扩张方向**：以 `city_center` 为极点的 8 象限扩张面积占比
5. **扩张模式**：基于扩张斑块的**质心-填充-边缘**分类（infilling / edge-expansion / leapfrog）
6. 若提供 UGB：统计 UGB 内外的扩张面积
7. 若提供 `socioeconomic`：计算与 GDP/人口的相关系数
8. 简单情景外推：按平均年扩张速率线性外推未来 5/10 年面积

## 5. 参数说明（`config.yaml`）

```yaml
classes:
  urban_codes: [1]
  default_mapping:
    1: 建设用地
    2: 耕地
    3: 林地
    4: 草地
    5: 水体
    6: 湿地
    7: 裸地
    8: 其他
pattern:
  infilling_ratio: 0.6
  leapfrog_distance_m: 500
forecast:
  horizons_years: [5, 10]
```

## 6. 调用示例

```bash
python /mnt/skills/custom/remote-sensing/urban-expansion-analysis/scripts/main.py \
  --action run \
  --inputs-json '{"classified_images":["/mnt/user-data/uploads/lulc_2015.tif","/mnt/user-data/uploads/lulc_2020.tif","/mnt/user-data/uploads/lulc_2025.tif"],"years":[2015,2020,2025],"urban_classes":[1]}' \
  --output-dir /mnt/user-data/outputs/expand_20260417
```

## 7. 输出文件

| 文件 | 含义 |
|------|------|
| `transition_matrix.csv` | 类别转移矩阵（面积/比例） |
| `expansion_intensity.json` | 扩张强度指数 (EII) 与分级 |
| `expansion_direction.json` | 8 方向扩张面积占比 |
| `expansion_patches.geojson` | 扩张斑块 + 模式分类字段 |
| `scenario_forecast.json` | 未来情景外推 |
| `report.md` | 综合报告 |

## 8. 治理场景

- 国土空间规划实施评估
- 城市增长边界执行情况核查
- 资源环境承载力分析
- 紧凑城市 vs 蔓延发展诊断

## 9. 注意事项

- 请确保多期分类图使用**相同类别体系**；否则请通过 `class_mapping` 做类别合并映射
- "线性外推"仅作演示；严肃情景预测请使用 CA-Markov / SLEUTH / FLUS 等专业模型
- `infilling` / `edge-expansion` / `leapfrog` 阈值基于斑块质心到既有建成区的最短距离

---
name: disaster-risk-assessment
description: >
  Fuses multi-source remote-sensing data to assess flood, landslide and fire
  risk levels and vulnerability. Invoke when the user mentions "disaster risk",
  "flood risk", "landslide susceptibility", "fire risk", "exposure",
  "vulnerability", "resilient city", "洪涝风险", "滑坡易发", "火灾风险",
  "应急避难", "韧性城市", "灾后损失", "DEM" or similar. The skill implements the
  Hazard × Exposure × Vulnerability framework, outputs risk-level maps, a
  high-risk area list, shelter-planning advice and mitigation measures.
version: 0.1.0
category: emergency-management
domain: remote-sensing
language:
  metadata: en
  report: zh-CN
entrypoint: scripts/main.py
license: MIT
tags: [disaster, flood, landslide, fire, resilience, DEM]
---

# 自然灾害风险遥感评估技能（disaster-risk-assessment）

## 1. 技能概述

融合多源遥感/空间数据评估指定区域对特定灾害（洪涝 / 滑坡 / 野火）的风险等级与脆弱性，
输出风险等级分布图、高风险区域清单与减灾建议，支持韧性城市规划与应急预案优化。

## 2. 支持的灾种

- `flood` 洪涝（基于 DEM、坡度、距河流距离、不透水面率）
- `landslide` 滑坡（基于坡度、坡向、地表湿度、土地利用）
- `wildfire` 野火（基于植被燃烧指数代理、坡度、历史火点）

## 3. 输入要求

| 变量名 | 类型 | 必需 | 说明 |
|--------|------|:--:|------|
| `hazard_type` | string | 是 | `flood` / `landslide` / `wildfire` |
| `dem` | file (GeoTIFF) | 是 | 数字高程模型 |
| `lulc` | file (GeoTIFF) | 是 | 土地利用分类图 |
| `history_events` | file (GeoJSON/CSV) | 否 | 历史灾害点位或影响范围 |
| `population` | file (GeoTIFF) | 否 | 人口栅格（评估暴露度） |
| `buildings` | file (GeoJSON/GeoTIFF) | 否 | 建筑轮廓或栅格化建筑密度 |
| `weather` | file (CSV/NetCDF) | 否 | 气象数据（降雨量、气温、风速） |
| `rivers` | file (GeoJSON) | 否 | 河流水系（`flood` 推荐提供） |
| `shelters` | file (GeoJSON) | 否 | 已有避难场所点位 |

## 4. 用户输入引导

> 为评估 <hazard_type> 风险，请至少提供：
> 1. **灾种**（`hazard_type`）：flood / landslide / wildfire。
> 2. **数字高程模型**（`dem`）：GeoTIFF，推荐 10-30 m 分辨率。
> 3. **土地利用分类图**（`lulc`）：GeoTIFF（像元值=类别编码）。
> 4. （推荐）**历史灾害记录**：GeoJSON 或 CSV（列：lon,lat,event_type,year）。
> 5. （推荐）**人口栅格**、**建筑数据**：用于暴露度和脆弱性计算。

## 5. 处理流程

1. `check-inputs`
2. 计算灾种相关**危险性因子**：
   - 洪涝：低洼度、距水系距离、不透水面率、汇流累积
   - 滑坡：坡度、坡向、水汽指数、土地覆盖
   - 野火：燃料密度、坡度、历史火点密度
3. 归一化并加权（`config.yaml` 中可调）得到**危险性图 H**
4. **暴露度 E** = 人口 + 建筑密度标准化
5. **脆弱性 V** = 基于 LULC 的脆弱性查表（建成区 > 耕地 > 林地）
6. **综合风险 R = H × E × V**，分级：1-5
7. 识别 Level 4/5 高风险斑块 → 清单；最近避难场所距离 → 建议新增点位
8. 成果输出

## 6. 参数说明（`config.yaml`）

```yaml
hazard_weights:
  flood:
    slope: 0.2
    distance_to_water: 0.4
    impervious: 0.2
    elevation_percentile: 0.2
  landslide:
    slope: 0.5
    aspect: 0.1
    wetness: 0.2
    lulc: 0.2
  wildfire:
    fuel: 0.5
    slope: 0.2
    history: 0.3
lulc_vulnerability:
  1: 0.9   # 建成区
  2: 0.5   # 耕地
  3: 0.3   # 林地
  4: 0.3
  5: 0.1
risk_levels: 5
shelter_coverage_m: 1000
```

## 7. 调用示例

```bash
python /mnt/skills/custom/remote-sensing/disaster-risk-assessment/scripts/main.py \
  --action run \
  --inputs-json '{"hazard_type":"flood","dem":"/mnt/user-data/uploads/dem.tif","lulc":"/mnt/user-data/uploads/lulc.tif","rivers":"/mnt/user-data/uploads/rivers.geojson","population":"/mnt/user-data/uploads/pop.tif"}' \
  --output-dir /mnt/user-data/outputs/risk_20260417
```

## 8. 输出文件

| 文件 | 含义 |
|------|------|
| `hazard.tif` | 危险性栅格 |
| `exposure.tif` | 暴露度栅格 |
| `vulnerability.tif` | 脆弱性栅格 |
| `risk_level.tif` | 风险等级图 1-5 |
| `high_risk_patches.geojson` | 高风险区矢量 |
| `shelter_gap.geojson` | 应急避难场所缺口区域 |
| `report.md` | 评估与减灾建议 |

## 9. 治理场景

- 城市防灾减灾规划
- 应急预案与避难场所布局优化
- 灾后快速损失评估
- 韧性城市指标体系输入

## 10. 注意事项

- 模型权重是**经验值**，建议根据本地历史灾害数据率定
- 未提供人口/建筑时，暴露度使用 LULC 代理，精度下降
- 灾后损失评估需配合灾前/灾后影像（可复用 `urban-change-detection` 技能）

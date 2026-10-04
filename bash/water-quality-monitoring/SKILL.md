---
name: water-quality-monitoring
description: >
  Retrieves key water-quality parameters from multispectral imagery, identifies
  pollution anomalies and tracks temporal trends. Invoke when the user mentions
  "water quality", "chlorophyll-a", "suspended sediment", "black-odor water",
  "drinking water source", "eutrophication", "NDWI", "水质", "叶绿素", "悬浮物",
  "黑臭水体", "饮用水源", "污染源" or similar. The skill computes water indices,
  inverts Chl-a / TSS / turbidity, locates pollution hotspots and suspected
  outfalls, and reports spatiotemporal change.
version: 0.1.0
category: water-governance
domain: remote-sensing
language:
  metadata: en
  report: zh-CN
entrypoint: scripts/main.py
license: MIT
tags: [water-quality, chlorophyll, TSS, NDWI, pollution]
---

# 水环境质量遥感监测技能（water-quality-monitoring）

## 1. 技能概述

基于多光谱遥感数据（Sentinel-2、Landsat-8/9、GF-1/6 等）反演地表水体的关键水质参数，
识别污染异常区域与变化趋势，辅助河湖监管、饮用水源保护与黑臭水体治理。

## 2. 输入要求

| 变量名 | 类型 | 必需 | 说明 |
|--------|------|:--:|------|
| `rs_image` | file (GeoTIFF) | 是 | 多光谱影像，至少含 蓝/绿/红/近红 四波段 |
| `water_boundary` | file (GeoJSON/Shapefile) | 是 | 目标水体边界矢量（河段/湖面） |
| `history_reference` | file (JSON) | 否 | 历史水质阈值或均值 JSON，用于异常识别 |
| `params` | list | 否 | 需反演的参数列表：`chl_a`, `tsm`, `turbidity`, `ndwi`, `bod_proxy`（默认全部） |
| `date` | string | 否 | 影像日期 YYYY-MM-DD，用于时间序列衔接 |

## 3. 用户输入引导

> 为反演您关注水体的水质，请提供：
> 1. **多光谱遥感影像**（`rs_image`）：GeoTIFF，建议 Sentinel-2 L2A（已做大气校正）；至少含 B2/B3/B4/B8。
> 2. **水体边界**（`water_boundary`）：GeoJSON 或 Shapefile，用于将分析限定在水面像元内。
> 3. （可选）**历史水质阈值**（`history_reference`）：JSON，格式如 `{"chl_a": {"mean": 12, "std": 4}}`，供异常检测使用。

## 4. 处理流程

1. `check-inputs`
2. NDWI/MNDWI 水体掩膜；与用户提供的水体边界交集
3. 分别反演叶绿素 a、悬浮物（TSM）、浊度等参数（使用常见经验模型：OC2/OC3、Nechad TSM）
4. 与历史参考对比得到异常图
5. 识别污染热点（高叶绿素 + 高悬浮物连通区）→ 估计疑似排污口（热点周边河岸）
6. 黑臭水体指示：`bod_proxy`（基于可见光比值的经验评分）
7. 输出参数分布图、热点矢量、趋势报告

## 5. 参数说明（`config.yaml`）

```yaml
bands:
  blue: 1
  green: 2
  red: 3
  nir: 4
retrieval:
  chl_a:
    method: oc3
    a: [0.283, -2.753, 1.457, 0.659, -1.403]
  tsm:
    method: nechad
    Ap: 355.85
    Cp: 1.74
    Bp: 0.19563
  turbidity:
    method: dogliotti
    k_low: 228.1
    k_high: 3078.9
anomaly:
  sigma_threshold: 2.0
hotspot:
  chl_a_high: 15
  tsm_high: 30
  min_patch_size: 20
```

## 6. 调用示例

```bash
python /mnt/skills/custom/remote-sensing/water-quality-monitoring/scripts/main.py \
  --action run \
  --inputs-json '{"rs_image":"/mnt/user-data/uploads/s2.tif","water_boundary":"/mnt/user-data/uploads/river.geojson","params":["chl_a","tsm"]}' \
  --output-dir /mnt/user-data/outputs/water_20260417
```

## 7. 输出文件

| 文件 | 含义 |
|------|------|
| `chl_a.tif` / `tsm.tif` / `turbidity.tif` | 反演参数分布图 |
| `anomaly_map.tif` | 异常指示图（与历史偏差 σ） |
| `hotspots.geojson` | 污染热点区域 |
| `suspected_sources.geojson` | 疑似排污点位 |
| `stats.json` | 水体内参数统计 |
| `report.md` | 水质评估与治理建议 |

## 8. 治理场景

- 河长制考核断面辅助
- 饮用水源地一二级保护区风险排查
- 黑臭水体治理成效前后对比
- 汛期高悬浮物预警

## 9. 注意事项

- 本技能针对**内陆水体**优化；海岸带请结合大气校正结果
- 叶绿素反演受水色类型（Case-1 / Case-2）影响，多云覆盖影像慎用
- "疑似排污源"为启发式定位，不能替代执法；须现场复核

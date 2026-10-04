---
name: urban-change-detection
description: >
  Detects significant changes in urban areas between multi-temporal remote sensing images,
  targeting illegal construction, illicit dumping, land-use conversion and urban-renewal
  monitoring. Invoke when the user mentions "change detection", "violation building",
  "two-date images", "多时相", "违建", "渣土", "土地用途变更" or similar triggers. The
  skill validates inputs, guides the user to supply missing imagery/boundary data, then
  runs change detection and outputs a change map, problem-point list, classified report
  and prioritized handling suggestions.
version: 0.1.0
category: urban-governance
domain: remote-sensing
language:
  metadata: en
  report: zh-CN
entrypoint: scripts/main.py
license: MIT
tags: [change-detection, remote-sensing, illegal-construction, land-use]
---

# 城市变化智能检测技能（urban-change-detection）

## 1. 技能概述

本技能基于多时相遥感影像，自动识别城市区域在两个时期之间的显著变化，
精准定位违建、非法倾倒、土地用途变更等问题区域。

核心算法包含 3 种可切换模式：
- `cva`：变化向量分析（Change Vector Analysis），无需训练，开箱即用
- `pca`：主成分差分法，适合光照差异较大的多时相数据
- `deep`：深度学习（Siamese U-Net 风格），若沙箱内可访问模型权重则启用

同时通过植被物候掩膜、小图斑滤除等后处理过滤自然变化干扰。

## 2. 输入要求（必读）

| 变量名 | 类型 | 是否必需 | 说明 |
|--------|------|---------|------|
| `image_t1` | file (GeoTIFF) | 是 | 前期遥感影像（已完成几何 + 辐射校正），≥ 3 个波段 |
| `image_t2` | file (GeoTIFF) | 是 | 后期遥感影像，需与 `image_t1` **相同坐标系、相同分辨率** |
| `aoi` | file (GeoJSON / Shapefile) | 否 | 关注区域边界，不提供则使用影像全范围 |
| `ndvi_mask` | file (GeoTIFF) | 否 | 植被掩膜，用于剔除植被物候变化 |
| `method` | string | 否 | `cva` / `pca` / `deep`，默认 `cva` |
| `threshold` | float | 否 | 变化幅度阈值 0-1，默认读取 `config.yaml` |

## 3. 用户输入引导

当用户提出变化检测需求但未提供完整输入时，技能应通过
`python main.py --action check-inputs --inputs-json '{...}'` 检查缺失项，
并使用以下话术引导用户补齐：

> 为了对您关注区域进行变化检测，请提供以下数据：
> 1. **前期遥感影像**（`image_t1`）：GeoTIFF 格式，建议来源 Sentinel-2 / GF-2 / 航摄，已完成几何校正和辐射定标。
> 2. **后期遥感影像**（`image_t2`）：与前期影像坐标系与分辨率一致。
> 3. **关注区域边界**（`aoi`，可选）：GeoJSON 或 Shapefile；若未提供，将使用影像范围。
>
> 如您仅有 JPG/PNG 截图或未校正的影像，请先完成正射校正后再提供。

## 4. 处理流程

1. **输入校验**：`--action check-inputs`，返回 `missing_inputs` 列表
2. **配准对齐**：重采样到共同网格（若分辨率不一致）
3. **变化幅度计算**：按配置的 `method` 生成变化强度图
4. **自然变化过滤**：基于 NDVI 差分剔除植被物候干扰
5. **阈值分割 & 连通域分析**：形态学清理、小图斑滤除
6. **成果输出**：
   - `change_map.tif`：0/1 二值变化图
   - `change_patches.geojson`：变化图斑矢量
   - `problem_points.csv`：问题点位清单（含中心坐标、面积、类型、优先级）
   - `report.md`：分类报告与优先处置建议

## 5. 参数说明（对应 `config.yaml`）

```yaml
algorithm:
  method: cva                 # cva | pca | deep
  threshold: 0.15             # 变化幅度归一化阈值
  min_patch_size: 30          # 像素连通域最小尺寸
  filter_natural_change: true # 是否剔除植被自然变化
```

## 6. 调用示例

### 校验输入
```bash
python /mnt/skills/custom/remote-sensing/urban-change-detection/scripts/main.py \
  --action check-inputs \
  --inputs-json '{"image_t1":"/mnt/user-data/uploads/2023.tif","image_t2":"/mnt/user-data/uploads/2024.tif"}'
```

### 运行检测
```bash
python /mnt/skills/custom/remote-sensing/urban-change-detection/scripts/main.py \
  --action run \
  --inputs-json '{"image_t1":"/mnt/user-data/uploads/2023.tif","image_t2":"/mnt/user-data/uploads/2024.tif","aoi":"/mnt/user-data/uploads/aoi.geojson"}' \
  --output-dir /mnt/user-data/outputs/change_det_20260417
```

## 7. 输出文件

| 文件 | 含义 |
|------|------|
| `change_map.tif` | 二值变化图（0=未变化，1=变化） |
| `change_patches.geojson` | 变化图斑矢量，属性含 area_m2、change_type、priority |
| `problem_points.csv` | 问题点位清单（推荐处置优先级） |
| `report.md` | 变化统计与治理建议 |

## 8. 治理场景

- **违法建设监管**：识别前后期新增建筑区域，导出点位供执法
- **渣土偷倒巡查**：识别大面积裸露新增区块
- **国土空间用途管制**：发现耕地、林地、水域非法转用
- **城市更新监测**：量化更新地块面积与进度

## 9. 注意事项

- 影像需要**完成预处理**（辐射定标、大气校正、正射校正）
- 两期影像尽量选择**相近物候期**以降低自然变化噪声
- `deep` 模式需要沙箱可访问模型权重文件，否则自动降级到 `cva`
- 输出 GeoTIFF 默认 LZW 压缩，单文件通常 <100MB

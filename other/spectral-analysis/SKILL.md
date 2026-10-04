---
name: spectral-analysis
description: 实验谱图AI分析，整合XRD和IR两类谱图分析功能。适用于：XRD谱图峰统计(peak_statistics)、XRD物相预测(xrd-predict)、XRD Rietveld精修(xrd-xerus)、红外光谱官能团预测(ir-predict)、IR物相识别、衍射谱分析、物相鉴定。输入为JSON格式实验谱图数据文件。
---

# 实验谱图分析

## 路由决策树

```
用户请求谱图分析
  │
  ├─ XRD 谱图（x轴 2-Theta/deg，y轴 Intensity/cps）？
  │   ├─ 只需统计峰位 → xrd-analysis.md（peak_statistics）
  │   ├─ 需要物相预测（快速识别）→ xrd-analysis.md（xrd-predict，需提供元素组成）
  │   └─ 需要 Rietveld 精修 → xrd-analysis.md（xrd-xerus，需提供元素组成）
  │
  └─ IR 谱图（x轴 Wave number/cm-1，y轴 Transmittance/%）？
      └─ → ir-analysis.md（ir-predict，官能团/物相预测）
```

## 子功能索引

| 子功能 | 文件 | 输入 |
|--------|------|------|
| XRD 谱图分析 | [xrd-analysis.md](xrd-analysis.md) | JSON（2-Theta vs Intensity） |
| IR 谱图分析 | [ir-analysis.md](ir-analysis.md) | JSON（Wave number vs Transmittance） |

## 输入文件格式区分

| 谱图类型 | x_label | y_label |
|---------|---------|---------|
| XRD | `"2-Theta(deg)"` | `"Intensity(cps)"` |
| IR | `"Wave number(cm-1)"` | `"Transmittance(%)"` |

## 与理论计算联动

```
crystal-toolkit/pymatgen（从已知结构计算理论 XRD）
  → spectral-analysis/xrd-analysis（与实验谱对比，物相鉴定/精修）
```

## 共用基础设施

- 文件上传：`POST http://114.214.215.131:40080/worker/file/upload`，请求头 `identifies: 691c9f24af764bd6ac955a0e8dd0dba9`
- 执行：`POST http://114.214.255.82:8396/api/scripts/name/{script_name}/execute`
- 查询：`GET http://114.214.255.82:8396/api/scripts/{task_id}/result/{task_id}`

**文件 URL 构建**：上传返回相对路径时，补全 `http://114.214.215.131:40080` 前缀。

**下载链接 IP 替换**：结果中 `10.88.0.32` → `114.214.255.82`，端口不变。

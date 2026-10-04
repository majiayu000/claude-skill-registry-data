---
name: qc-output-analysis
description: 分子量子化学计算输出文件解析，整合 Gaussian 和 ORCA 两类输出解析。适用于：单点能、几何结构优化、红外光谱、拉曼光谱、紫外可见光谱、核磁共振谱、过渡态搜索、势能面扫描、极化率和超极化率等计算结果的结构化提取。输入为包含输出文件的 ZIP 包 URL。
display_name: 分子量子化学输出解析
version: 0.1.0
category: analysis
author: wencheng
status: draft
---

# 分子量子化学输出解析

解析 Gaussian / ORCA 量子化学计算输出文件，提取能量、结构、光谱等计算结果，返回结构化 JSON 数据。

## 路由决策树

```
用户需要解析分子量子化学计算输出
  │
  ├─ 输出文件来自 Gaussian（g16.out.log）？
  │   └─ → gaussian-post.md
  │
  ├─ 输出文件来自 ORCA（input.out）？
  │   └─ → orca-post.md
  │
  └─ 不确定来源？
      ├─ 文件名含 g16 / gjf → gaussian-post.md
      └─ 文件名含 orca / inp（且无 gjf）→ orca-post.md
```

## 子功能索引

| 子功能 | 文件 | 解析目标 |
|--------|------|---------|
| Gaussian 输出解析 | [gaussian-post.md](gaussian-post.md) | SP/Opt/IR/Raman/UV-Vis/NMR/TS/Scan/极化率 |
| ORCA 输出解析 | [orca-post.md](orca-post.md) | SP/Opt/UV-Vis/IR/Raman/NMR |

## 共用基础设施

使用**调度平台**（30082 端口），三步流程：

1. **提交任务**：`POST http://114.214.211.25:30082/api/jobs`
2. **轮询状态**：`GET http://114.214.211.25:30082/api/jobs?id=<data.id>`
3. **下载结果**：`GET http://114.214.211.25:30082/api/tasks/download?taskId=<taskId>`

**状态机：** `PENDING` → `DISPATCHED` → `RUNNING` → `SUCCEEDED` / `FAILED`

> `taskId` 使用 UUID 格式，`data.id`（整数）仅用于轮询。

## 触发条件

- 用户提到 `解析 Gaussian 输出`、`Gaussian 结果提取`、`解析 ORCA 输出`、`ORCA 结果提取`
- 用户提到 `量子化学计算结果解析`、`QC 后处理`、`分子计算输出分析`
- 当上游 Skill `hpc-calc`、`mol-qc` 完成计算后需要提取结构化结果时
- 当用户需要将 QC 输出文件（.out.log / .out）转为结构化数据时

## Input Schema

```yaml
inputs:
  - name: inputfile
    type: file_url
    required: true
    description: |
      ZIP 压缩包 URL，包含计算输出文件。
      Gaussian: 应含 g16.out.log 和可选 input.gjf
      ORCA: 应含 input.out 和可选 input.inp

  - name: software
    type: enum
    required: true
    options: ["gaussian", "orca"]
    description: |
      输出文件来源软件，决定使用哪个解析器。

  - name: objective
    type: enum
    required: true
    description: |
      计算类型路由，决定调用哪个解析逻辑。
      通用选项：单点能 | 几何结构优化 | 红外光谱 | 拉曼光谱 | 紫外可见光谱 | 核磁共振谱
      Gaussian 额外选项：过渡态搜索 | 势能面扫描 | 极化率和超极化率
```

## Output Schema

```yaml
outputs:
  - name: analysis
    type: dict
    description: |
      解析结果载荷，含 computational_info / data_type / data / units 等子字段，
      结构因 objective 而异。

  - name: xyz
    type: file_url
    description: |
      优化后分子结构 XYZ 文件 URL（仅 "几何结构优化" 类型返回）。

  - name: error
    type: str
    description: 错误信息（仅未知 objective 时返回）
```

## 典型工作流

```
hpc-calc / mol-qc（执行分子量子化学计算）
  → qc-output-analysis（解析输出文件，提取结构化结果）
  → 下游分析（数据对比、图表生成等）
```

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0 | 2026-04-15 | 初始版本，整合 Gaussian 和 ORCA 输出解析 |

---
name: mace
description: MACE 晶体结构稳定性评估技能，基于 MACE 机器学习势能面框架对批量 CIF 晶体结构进行能量推断与稳定性排序。适用于：晶体结构预测（CSP）候选体快速粗筛、大批量结构势能面评估。
display_name: MACE 晶体结构稳定性评估
version: 0.1.0
category: fast-screening
author: wencheng
status: draft
---

# MACE 晶体结构稳定性评估

基于 MACE（Messages Passing Atomic Cluster Expansion）机器学习势能面框架，对批量 CIF 晶体结构进行能量推断与稳定性排序，适用于晶体结构预测（CSP）候选体的快速筛选。

> **与 vasp-dft 的区别**：MACE 基于机器学习势能面，推断速度快（秒级），适合千级候选体粗筛；vasp-dft 为第一性原理计算，精度高但耗时，适合精筛后的少量结构。

## 触发条件

- 用户提到 `MACE`、`ML 势能`、`晶体稳定性排序`
- 用户需要对大批量 CSP 候选结构做能量推断
- 计算类型：CSP 结构筛选、势能面评估、稳定性排序

## Input Schema

```yaml
inputs:
  - name: inputfile
    type: file
    required: true
    description: |
      CIF 晶体结构数据包 URL（zip 格式）。
      zip 内应包含：
        - 1 个来自 CCDC 的实验参考结构（单斜晶系 P 21/c）
        - 约 1000 个计算预测结构（P1 空间群），存放于 random_1000/ 目录
```

## Output Schema

```yaml
outputs:
  - name: result_zip
    type: file
    description: 包含 MACE 能量推断结果的 zip 压缩包，通过下载接口获取
  - name: data_output
    type: dict
    description: 任务响应中 data.output 为空对象 {}，实际结果通过下载接口获取
```

## Dependencies

```yaml
dependencies:
  python: ">=3.10"
  packages: []
  external_tools:
    - 30082 调度平台（/api/jobs/tpl，model=mace）
  upstream_skills:
    - crystal-gen
```

## 基础设施

使用**调度平台**（30082 端口），`/api/jobs/tpl` 接口：

1. **上传结构文件**：`POST http://114.214.211.25:30082/api/file/upload`
2. **提交任务**：`POST http://114.214.211.25:30082/api/jobs/tpl`，使用 `model: "mace"`
3. **轮询状态**：`GET http://114.214.211.25:30082/api/jobs?id=<data.id>`
4. **下载结果**：`GET http://114.214.211.25:30082/api/tasks/download?taskId=<taskId>`

> **重要**：本 skill 使用 `/api/jobs/tpl`（模型训练/推断接口），提交体含 `model` 字段而非 `image` 字段；`taskId` 使用 **UUID 格式**。

## 调用流程

### 第一步：上传文件（可选）

若输入文件为本地路径，先上传获取 URL：

```bash
FILE_URL=$(curl -s -X POST http://114.214.211.25:30082/api/file/upload \
  -F "file=@structures.zip" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'])")
```

若已有 URL，直接跳过此步。

### 第二步：提交任务

```bash
TASK_ID=$(python3 -c "import uuid; print(uuid.uuid4())")   # UUID 格式

NUMERIC_ID=$(curl -s -X POST 'http://114.214.211.25:30082/api/jobs/tpl' \
  -H 'Content-Type: application/json' \
  -d "{
    \"params\": {
      \"inputfile\": \"${FILE_URL}\"
    },
    \"model\": \"mace\",
    \"parentId\": \"${TASK_ID}\",
    \"taskId\": \"${TASK_ID}\",
    \"createdBy\": \"user\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
# NUMERIC_ID（整数）仅用于轮询，TASK_ID（UUID）用于下载
```

### 第三步：轮询状态

```bash
curl -X GET "http://114.214.211.25:30082/api/jobs?id=${NUMERIC_ID}"
# 状态机：PENDING → DISPATCHED → RUNNING → SUCCEEDED / FAILED
```

### 第四步：下载结果

```bash
curl -OJ "http://114.214.211.25:30082/api/tasks/download?taskId=${TASK_ID}"
```

## 典型工作流

```
crystal-gen（AI 晶体结构生成，输出候选 CIF 包）
  → mace（MACE 能量推断，稳定性排序）
  → vasp-dft（对 Top-N 结构进行高精度 DFT 精算）
  → spectral-analysis（分析 DOS/能带等性质）
```

## Examples

**对 CSP 候选结构批量做 MACE 能量推断：**

```json
{
  "params": {
    "inputfile": "http://124.71.201.245/aichem-lab-edge/20260413134101201zip.zip"
  },
  "model": "mace",
  "parentId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "taskId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "createdBy": "user"
}
```

提交响应：
```json
{
  "code": 200,
  "data": {
    "id": 12345,
    "taskId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "status": "PENDING"
  }
}
```

任务完成后 `data.output` 为 `{}`，通过下载接口获取结果 zip：
```bash
curl -OJ 'http://114.214.211.25:30082/api/tasks/download?taskId=f47ac10b-58cc-4372-a567-0e02b2c3d479'
```

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0 | 2026-04-14 | 初始版本，从 README_mace.md 封装 |

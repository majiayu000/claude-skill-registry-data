---
name: torchmd-net
description: TorchMD-Net 分子模拟与性质预测技能，基于等变神经网络执行分子性质推理。适用于：加载 `.ckpt` 检查点进行势能、原子力、偶极矩等性质预测与分子模拟推理任务。
display_name: TorchMD-Net 分子模拟与性质预测
version: 0.1.0
category: ml-potential
author: wencheng
status: alpha
---

# TorchMD-Net 分子模拟与性质预测

基于等变神经网络与可微分分子动力学的分子模拟框架，以原子三维坐标和元素类型为输入，通过等变消息传递构建旋转/平移不变的分子表示，端到端预测势能面及量子化学性质（势能、原子力、偶极矩、均方位移等）。

用户提供预训练模型检查点（`.ckpt`），工作站完成模型加载并执行分子性质推理。

> **与 REANN 的区别**：REANN 接收训练数据集，从头训练势能面；TorchMD-Net 接收已有 `.ckpt` 检查点，执行推理/模拟，不做训练。
> **与 SchNet 的区别**：SchNet 接收 PyG 数据集做属性预测训练；TorchMD-Net 用等变架构做推理，支持势能面和 MD 模拟。

## 触发条件

- 用户提到 TorchMD、TorchMD-Net、等变神经网络分子模拟
- 用户提供了 `.ckpt` 预训练模型文件，需要执行推理
- 需要预测势能、原子力、偶极矩、均方位移等分子性质
- 关键词：等变消息传递、可微分 MD、torchmd-net、.ckpt 推理

## Input Schema

```yaml
inputs:
  - name: inputfile
    type: file
    required: true
    description: >
      TorchMD-Net 预训练模型检查点（PyTorch Lightning .ckpt 格式）的 URL。
      工作站将直接下载至 output 目录用于推理。
```

## Output Schema

```yaml
outputs:
  - name: result_zip
    type: file
    description: 推理结果 zip，包含模型推理输出文件
```

## Dependencies

```yaml
dependencies:
  python: ">=3.10"
  packages: []
  external_tools:
    - TorchMD-Net 工作站（http://114.214.211.25:30082，model: torchmd-net）
  upstream_skills:
    - mol-toolkit      # 可选：生成分子构象作为推理输入
    - mol-qc           # 可选：高精度 QC 计算生成检查点
```

## 基础设施

使用**调度平台**（30082 端口，`/api/jobs/tpl` 路由）：

1. **上传检查点文件**：`POST http://114.214.211.25:30082/api/file/upload`
2. **提交任务**：`POST http://114.214.211.25:30082/api/jobs/tpl`，`model: "torchmd-net"`，`taskId` 为 UUID
3. **轮询状态**：`GET http://114.214.211.25:30082/api/jobs?id=<data.id>`
4. **下载结果**：`GET http://114.214.211.25:30082/api/tasks/download?taskId=<taskId>`

> **注意**：`data.id`（整数）用于轮询，提交时自定的 `taskId`（UUID）用于下载。

## 调用流程

### 第一步：上传 .ckpt 文件

```bash
FILE_URL=$(curl -s -X POST http://114.214.211.25:30082/api/file/upload \
  -F "file=@model.ckpt" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'])")
```

### 第二步：提交任务

```bash
TASK_UUID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")

curl -X POST 'http://114.214.211.25:30082/api/jobs/tpl' \
  -H 'Content-Type: application/json' \
  -d "{
    \"params\": {\"inputfile\": \"${FILE_URL}\"},
    \"model\": \"torchmd-net\",
    \"parentId\": \"${TASK_UUID}\",
    \"taskId\": \"${TASK_UUID}\",
    \"createdBy\": \"<用户名>\"
  }"
```

### 第三步：轮询状态

```bash
# 用响应中的 data.id（整数）轮询
curl -X GET 'http://114.214.211.25:30082/api/jobs?id=<data.id>'
# 等待状态变为 SUCCEEDED
```

### 第四步：下载结果

```bash
# 用提交时的 TASK_UUID（不是 data.id）
curl -OJ "http://114.214.211.25:30082/api/tasks/download?taskId=${TASK_UUID}"
```

## 推荐使用脚本

```bash
# 上传 .ckpt 并自动等待完成后下载结果
python skills/torchmd-net/scripts/torchmd_run.py --inputfile /path/to/model.ckpt --created_by <用户名>

# 已有 URL 跳过上传
python skills/torchmd-net/scripts/torchmd_run.py \
  --inputfile http://124.71.201.245/aichem-lab-edge/20260403160551490aceff_v1.1.ckpt \
  --skip_upload --created_by <用户名>

# 仅查询状态
python skills/torchmd-net/scripts/torchmd_run.py --query_task <data.id>

# 仅下载结果
python skills/torchmd-net/scripts/torchmd_run.py --download_result <task-uuid>
```

## 典型工作流

```
mol-qc/orca 或 vasp-dft（生成高精度参考数据，训练 TorchMD-Net 模型得到 .ckpt）
  → torchmd-net（加载 .ckpt，执行推理/MD 模拟）
  → spectral-analysis（分析模拟轨迹）
```

## Examples

```json
{
  "params": {
    "inputfile": "http://124.71.201.245/aichem-lab-edge/20260403160551490aceff_v1.1.ckpt"
  },
  "model": "torchmd-net",
  "parentId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "taskId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "createdBy": "user"
}
```

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0 | 2026-04-03 | 初始版本，从 torchmd_README.md 封装 |

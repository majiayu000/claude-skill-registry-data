---
name: schnet
description: SchNet 分子性质预测技能，基于连续滤波卷积图神经网络。适用于：分子量子化学性质预测、PyTorch Geometric 分子数据集训练，以及 HOMO/LUMO、偶极矩、极化率等性质建模任务。
display_name: SchNet 分子性质预测
version: 0.1.0
category: schnet-mol-pred
author: wencheng
status: alpha
---

# SchNet 分子性质预测

基于连续滤波卷积（cfconv）图神经网络，直接以原子三维坐标（pos）和原子序数（z）为输入，无需人工构造分子指纹，端到端学习分子量子化学性质（原子化能、HOMO/LUMO 能级差、偶极矩、极化率、零点振动能等）。用户提供 PyTorch Geometric 格式的分子数据集（zip 内含单个 .pt 文件，每样本包含 z、x、pos、edge_index、edge_attr、y 字段），工作站自动完成数据加载并启动训练任务。

## 前置条件

- 工作站 API 地址：`http://114.214.211.25:30082`
- 提交端点：`POST /api/jobs/tpl`

## 触发关键词

- SchNet、SchNet 训练、schnet 分子性质
- 图神经网络分子性质预测、GNN 量子化学
- HOMO/LUMO、偶极矩、极化率、零点振动能、原子化能预测
- PyTorch Geometric 分子数据集训练
- 连续滤波卷积、3D 坐标分子预测

***

## 工作流程概述

所有 SchNet 训练计算遵循三步流程：

1. **上传数据集**：将 PyTorch Geometric 格式 ZIP 数据集上传至文件服务器，获取文件 URL
2. **提交任务**：将文件 URL 提交至工作站 `/api/jobs/tpl`，指定 `model: "schnet"`，获取任务 ID
3. **下载结果**：通过任务 ID 下载训练结果 ZIP 压缩包

***

## 收集参数

| 参数          | 必填 | 类型  | 说明                                                                                                             |
| ----------- | -- | --- | -------------------------------------------------------------------------------------------------------------- |
| `inputfile` | 是  | URL | 分子数据集 ZIP，解压后为单个 `.pt` 文件（PyTorch 序列化的 Data 对象列表），每个样本含 `z`、`x`、`pos`、`edge_index`、`edge_attr`、`y` 字段 |

**数据集格式要求：**

- ZIP 解压后为**单个 `.pt` 文件**（PyTorch 序列化的 `Data` 对象列表）
- 每个分子样本需包含：
  - `z`：原子序数，形状 `[N]`
  - `x`：原子特征，形状 `[N, F]`
  - `pos`：原子三维坐标，形状 `[N, 3]`
  - `edge_index`：边连接关系，形状 `[2, E]`
  - `edge_attr`：边特征，形状 `[E, D]`
  - `y`：目标性质标签（支持多靶点）
- 不需要 `raw/` 和 `processed/` 子目录结构

如果用户未提供输入文件，**必须询问**用户需要训练哪些分子的性质数据集。

***

## 执行计算（推荐使用 Python 脚本）

```bash
python skills/schnet/scripts/schnet_run.py \
  --inputfile /path/to/dataset.zip \
  --created_by <用户名>
```

已有 URL 时可跳过上传步骤：

```bash
python skills/schnet/scripts/schnet_run.py \
  --inputfile http://124.71.201.245/aichem-lab-edge/20260402165242287data.zip \
  --skip_upload \
  --created_by <用户名>
```

查询任务状态：

```bash
python skills/schnet/scripts/schnet_run.py --query_task <job_id>
```

下载结果：

```bash
python skills/schnet/scripts/schnet_run.py --download_result <task_uuid>
```

***

## 手动调用 REST API（备选方案）

### 1. 上传文件

```bash
curl -X POST "http://114.214.211.25:30082/api/file/upload" \
  -F "file=@dataset.zip"
```

<br />

响应示例：

```json
{
  "code": 0,
  "data": "http://124.71.201.245/aichem-lab-edge/20260402165242287data.zip",
  "message": ""
}
```

`data` 字段即为文件 URL，后续作为 `inputfile` 参数使用。

### 2. 提交任务

```bash
curl -X POST 'http://114.214.211.25:30082/api/jobs/tpl' \
  -H 'Content-Type: application/json' \
  -d '{
    "params": {
      "inputfile": "http://124.71.201.245/aichem-lab-edge/20260402165242287data.zip"
    },
    "model": "schnet",
    "parentId": "<task-uuid>",
    "taskId": "<task-uuid>",
    "createdBy": "<用户名>"
  }'
```

> `<task-uuid>` 为 UUID 格式，可用 Python `uuid.uuid4()` 生成；`parentId` 与 `taskId` 相同。

响应示例：

```json
{
  "code": 200,
  "data": {
    "id": 12345,
    "taskId": "<task-uuid>",
    "status": "PENDING"
  }
}
```

### 3. 查询任务状态

```bash
curl -X GET 'http://114.214.211.25:30082/api/jobs?id=12345'
```

**任务状态说明：**

| 状态           | 含义     | 是否终态 |
| ------------ | ------ | ---- |
| `PENDING`    | 等待调度   | 否    |
| `DISPATCHED` | 已下发到集群 | 否    |
| `RUNNING`    | 执行中    | 否    |
| `SUCCEEDED`  | 执行成功   | ✅ 是  |
| `FAILED`     | 执行失败   | ✅ 是  |
| `CANCELLED`  | 已取消    | ✅ 是  |
| `TIMEOUT`    | 超时终止   | ✅ 是  |

**轮询建议**：非终态时持续轮询（建议间隔 10 秒），直到进入终态。

### 4. 下载结果

```bash
curl -OJ 'http://114.214.211.25:30082/api/tasks/download?taskId=<task-uuid>'
```

返回 `application/octet-stream`，文件名为 `{taskId}.zip`，包含训练好的模型权重和日志。

***

## 输出结果

向用户汇报：

- 任务提交是否成功（含 job\_id）
- 训练完成状态（SUCCEEDED / FAILED）
- 结果下载链接或本地保存路径
- 如有失败，展示错误信息

***

## 错误处理

| 错误        | 原因              | 处理                                   |
| --------- | --------------- | ------------------------------------ |
| 文件上传失败    | 网络问题或文件过大       | 检查网络，确认 ZIP 文件完整                     |
| HTTP 400  | 参数缺失或格式错误       | 确认 `inputfile`、`model` 字段填写正确        |
| HTTP 404  | API 地址错误        | 确认使用 `/api/jobs/tpl` 端点              |
| 任务 FAILED | 数据集 `.pt` 文件格式不符合要求 | 确认 ZIP 解压后为单个 `.pt` 文件，且每个样本含 z、x、pos、edge_index、edge_attr、y 字段 |
| 连接被拒绝     | 工作站服务未启动        | 确认 `http://114.214.211.25:30082` 可访问 |

## 注意事项

- 输入数据集必须先上传获取 URL，不能直接传本地路径
- 提交端点为 `/api/jobs/tpl`（非 `/api/jobs`），必须携带 `model: "schnet"` 字段
- 任务本身不返回结构化预测数据，`data.output` 为空对象 `{}`，执行结果通过下载接口获取
- 查询状态使用 `data.id`（integer），下载结果使用 `taskId`（UUID）
- 训练为异步任务，提交后需等待服务器完成计算（耗时视数据集大小而定）

***

## 与其他技能联动

典型工作流：

```
mol-toolkit（RDKit 生成分子构象，导出 3D 坐标）
  → mol-qc/xtb（半经验方法优化几何构型）
  → schnet（训练量子化学性质预测模型）
```

***

## Input Schema

```yaml
inputs:
  - name: inputfile
    type: file
    required: true
    description: 分子数据集 ZIP，解压后为单个 .pt 文件（PyTorch 序列化的 Data 对象列表），每个样本含 z、x、pos、edge_index、edge_attr、y 字段
```

## Output Schema

```yaml
outputs:
  - name: result_zip
    type: file
    description: 训练结果 ZIP，含模型权重和训练日志
```

## Dependencies

```yaml
dependencies:
  python: ">=3.10"
  packages:
    - torch>=2.0
    - torch_geometric>=2.4
  external_tools:
    - SchNet 工作站服务（http://114.214.211.25:30082）
  upstream_skills:
    - mol-toolkit
    - mol-qc
```

## Changelog

| 版本    | 日期         | 变更                           |
| ----- | ---------- | ---------------------------- |
| 0.1.0 | 2026-04-03 | 初始版本，基于 schnet\_README.md 封装 |

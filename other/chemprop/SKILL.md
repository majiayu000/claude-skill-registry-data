---
name: chemprop
description: Chemprop 分子性质模型训练技能，基于图神经网络（GNN）。适用于：分子 SMILES 数据训练、多靶点毒性模型训练、分子性质模型训练、Tox21 格式数据处理。当用户需要对分子进行毒性/性质模型训练时使用本技能。
---

# Chemprop 分子性质模型训练

通过调用 Chemprop 图神经网络工作站，对输入的分子 SMILES 数据进行多靶点毒性/性质模型训练。

## 前置条件

- 工作站 API 地址：`http://114.214.211.25:30082`
- 镜像地址：`114.214.255.82:18080/internal/job:yaml.arm`

## 触发关键词

- Chemprop、分子性质训练、毒性模型训练
- SMILES 训练、分子毒性模型训练
- Tox21 格式、多靶点训练
- 对分子进行性质/毒性模型训练

---

## 工作流程概述

所有 Chemprop 训练计算遵循三步流程：
1. **上传文件**：将输入数据文件（CSV）上传至文件服务器，获取文件 URL
2. **提交任务**：将文件 URL 和计算参数提交至工作站 API，获取任务 ID
3. **下载结果**：通过任务 ID 下载计算结果 ZIP 压缩包（包含训练好的模型和日志）

---

## 功能：Chemprop 分子性质模型训练

### 1. 收集参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `inputfile` | 是 | 输入数据文件的 URL 地址（CSV 格式）。第一列必须为 `smiles`（分子 SMILES 字符串），后续列为各靶点标签（0/1，空值表示未测定），如 Tox21 格式 |
| `objective` | 是 | 模型模板标识，当前固定填写 `"chemprop"` |

**CSV 文件格式要求：**
- 第一列必须为 `smiles`（分子 SMILES 字符串）
- 后续列为各靶点标签（0/1，空值表示未测定）
- 建议至少包含 50 条以上的数据以获得稳定的训练效果
- 空值可以用空字符串、`NA`、`null` 等表示

**CSV 格式示例：**
```csv
smiles,target1,target2,target3
CCO,0,1,NA
c1ccccc1,1,0,1
CC(C)CC(C)(C)C,0,0,0
CC(=O)OC1=CC=CC=C1C(=O)O,1,1,NA
CN1C=NC2=C1C(=O)N(C(=O)N2C)C,0,1,1
```

如果用户未提供输入文件，**必须询问**用户需要训练哪些分子的性质模型。

### 2. 执行计算（推荐使用 Python 脚本）

```bash
python scripts/chemprop_run.py \
  --inputfile http://example.com/input.csv \
  --objective chemprop
```

### 3. 手动调用 REST API（备选方案）

#### 3a. 上传文件

```bash
curl -s -X POST http://114.214.215.131:40080/worker/file/upload \
  -H "identifies: 691c9f24af764bd6ac955a0e8dd0dba9" \
  -F "file=@input.csv"
```

响应示例：
```json
{
  "code": 0,
  "data": "http://114.214.215.131:40080/files/pan-dev/20260330165337547input.csv",
  "message": ""
}
```

`data` 字段即为文件 URL，后续作为 `inputfile` 参数使用。

#### 3b. 提交任务

```bash
curl -X POST 'http://114.214.211.25:30082/api/jobs' \
  -H 'Content-Type: application/json' \
  -d '{
    "params": {
      "inputfile": "http://114.214.215.131:40080/files/pan-dev/20260330165337547input.csv",
      "objective": "chemprop"
    },
    "image": "114.214.255.82:18080/internal/job:yaml.arm",
    "parentId": "<task-id>",
    "taskId": "<task-id>",
    "createdBy": "<用户名>"
  }'
```

> `<task-id>` 为 UUID 格式的任务标识符，可使用 Python 的 `uuid.uuid4()` 生成。

---

## 查询任务状态

任务提交后，通过以下 API 轮询查询任务状态：

**API**：`GET http://114.214.211.25:30082/api/jobs?id=<job_id>`

`<job_id>` 为提交任务时返回的 `data.id`（integer）。

**任务状态说明：**

| 状态 | 含义 | 是否终态 |
|------|------|----------|
| `PENDING` | 等待调度 | 否 |
| `DISPATCHED` | 已下发到集群 | 否 |
| `RUNNING` | 执行中 | 否 |
| `SUCCEEDED` | 执行成功 | ✅ 是 |
| `FAILED` | 执行失败 | ✅ 是 |
| `CANCELLED` | 已取消 | ✅ 是 |
| `TIMEOUT` | 超时终止 | ✅ 是 |

**轮询建议**：非终态（PENDING / DISPATCHED / RUNNING）时持续轮询，直到变为终态。

**响应格式：**

```json
{
  "code": 200,
  "status": true,
  "data": {
    "id": 12345,
    "taskId": "e3a0a335-17db-44ea-8b39-a3c7f02572j6",
    "status": "SUCCEEDED",
    "output": {}
  }
}
```

> `data.output` 为空对象 `{}`，执行结果通过下载接口获取。

---

## 下载计算结果

任务进入终态（`SUCCEEDED` / `FAILED` 等）后，通过 `taskId` 下载该任务工作目录的 zip 压缩包。

**API**：`GET http://114.214.211.25:30082/api/tasks/download?taskId=<task_id>`

`<task_id>` 为提交任务时请求体中的 `taskId`（UUID），与查询时的 `data.id`（integer）不同。

**下载示例：**

```bash
curl -OJ 'http://114.214.211.25:30082/api/tasks/download?taskId=e3a0a335-17db-44ea-8b39-a3c7f02572j6'
```

返回 `application/octet-stream` 二进制流，`Content-Disposition` 为 `attachment; filename="{taskId}.zip"`。

---

## 输出结果

向用户汇报：
- 任务提交是否成功
- API 返回的任务信息（任务 ID、状态等）
- 计算完成后，提供结果下载链接
- 计算参数确认（objective、inputfile 等）

---

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| 文件上传失败 | 网络问题或文件过大 | 检查网络连接，确认文件大小合理 |
| HTTP 404 | API 地址或镜像错误 | 确认使用正确的镜像地址 |
| HTTP 400 | 参数缺失或格式错误 | 检查 inputfile、objective 是否正确 |
| CSV 格式错误 | 输入文件不符合要求 | 确认第一列为 `smiles`，后续列为靶点标签（0/1） |
| 连接被拒绝 | 工作站服务未启动 | 提示用户确认服务状态 |
| 任务状态为 FAILED | 计算执行失败 | 查看 `data.message` 字段排查原因 |
| Job has reached the specified backoff limit | 数据量不足或训练配置问题 | 确认数据量是否足够（建议至少 50 条），或联系管理员检查镜像配置 |

## 注意事项

- 输入文件必须先上传到文件服务器获取 URL，不能直接传本地路径
- 输入文件格式为 CSV，第一列必须为 `smiles`（分子 SMILES 字符串）
- 后续列为各靶点标签（0/1，空值表示未测定），如 Tox21 格式
- 任务本身不返回结构化数据，`data.output` 为空对象 `{}`，执行结果通过下载接口获取
- 工作站计算为异步任务，提交后需要等待服务器完成计算
- 查询任务状态使用 `data.id`（integer），下载结果使用 `taskId`（UUID）

## 与其他技能联动

典型工作流：
1. 使用 `mol-qc`（molatom/xTB）或 `mol-toolkit` 生成/处理分子结构
2. 导出分子 SMILES 列表为 CSV 格式（包含靶点标签）
3. 使用本技能进行多靶点毒性/性质模型训练
4. 训练完成后，使用训练好的模型进行预测（需要额外的预测接口）

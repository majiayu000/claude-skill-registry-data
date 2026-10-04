---
name: reann
description: REANN 势能面训练技能，基于递归原子神经网络拟合势能面。适用于：机器学习力场训练、势能面拟合、分子动力学前置模型训练与包含 REANN 标准训练包的数据任务。
display_name: REANN 势能面训练
version: 0.1.0
category: ml-potential
author: wencheng
status: alpha
---

# REANN 势能面训练

基于递归神经网络（Recurrent Atomic Neural Network）的机器学习势能面框架，通过原子邻域密度函数描述符捕捉多体相互作用，满足平移、旋转和置换不变性，端到端拟合势能面（能量、原子力、应力张量），可直接驱动分子动力学模拟。

用户提供包含训练数据集、超参数和预训练权重的完整训练包，工作站自动完成文件部署并启动训练。

> **与 schnet 的区别**：SchNet 学习分子量子化学性质（HOMO/LUMO 等），输入为 PyG 格式数据集；REANN 拟合势能面用于 MD 模拟，输入为 REANN 标准训练包（含 configuration 文件和 .pth 权重）。

## 触发条件

- 用户提到 REANN、势能面训练、机器学习力场
- 用户需要训练 ML 势能面用于分子动力学
- 用户提供了含 `data/`、`para/`、`REANN.pth` 的训练包
- 关键词：原子神经网络、递归神经网络势能、ML-MD、REANN.pth

## Input Schema

```yaml
inputs:
  - name: inputfile
    type: file
    required: true
    description: >
      REANN 势能面训练完整包（zip），解压后须包含以下文件（均为必须）：

      【目录结构】
        <任意根目录>/
        ├── data/
        │   ├── train/configuration   # 训练集
        │   └── test/configuration    # 测试集
        ├── para/
        │   ├── input_nn              # 神经网络超参数
        │   └── input_density         # 描述符参数
        ├── REANN.pth                 # 必须！预训练权重，缺失则静默崩溃
        ├── REANN_PES_DOUBLE.pt
        ├── REANN_PES_FLOAT.pt
        ├── REANN_LAMMPS_DOUBLE.pt
        └── REANN_LAMMPS_FLOAT.pt

      【configuration 文件格式】每个构型块：
        point=  <构型序号>
        <晶格向量 a: ax ay az>
        <晶格向量 b: bx by bz>
        <晶格向量 c: cx cy cz>
        pbc  1  1  1
        <元素> <质量> <x> <y> <z> <fx> <fy> <fz>   # 每行一个原子，含受力
        ...（多个构型连续拼接）

      【para/input_nn 关键字段】（字段名区分大小写）
        nl = [64, 64]         # 隐藏层节点数（列表）
        nblock = 3            # ResNet block 数
        Epoch = 1000000
        batchsize_train = 32
        batchsize_test = 32
        start_lr = 0.001
        end_lr = 1e-6
        atomtype = ['Li','Y','Cl']   # 与数据集中的元素一致
        DDP_backend = 'hccl'  # 华为 NPU 用 hccl，CPU/GPU 用 gloo/nccl
        floder = "./data/"

      【para/input_density 关键字段】
        cutoff = 5.5e0        # 截断半径（Å）
        nwave = 8             # 波函数基数
        nipsin = 2
        atomtype = ['Li','Y','Cl']   # 与 input_nn 保持一致
        neigh_atoms = 300

      ⚠️  常见错误：
      - REANN.pth 缺失 → 程序打印 banner 后静默退出，nn.err 无错误信息
      - 字段名拼写错误（如 Rc/Nwave/Nlayer）→ 同上，静默崩溃
      - atomtype 与 configuration 中元素不匹配 → 训练报错
```

## Output Schema

```yaml
outputs:
  - name: result_zip
    type: file
    description: 训练完成的 REANN 结果 zip，含更新后的模型权重和训练日志
```

## Dependencies

```yaml
dependencies:
  python: ">=3.10"
  packages: []
  external_tools:
    - REANN 工作站（http://114.214.211.25:30082，model: reann2.0）
  upstream_skills:
    - mace-sim     # 可选：先用 MACE 做快速预筛，再用 REANN 精细训练
    - vasp-dft     # 常见上游：VASP 生成 ab initio 训练数据
```

## 基础设施

使用**调度平台**（30082 端口，`/api/jobs/tpl` 路由）：

1. **上传训练包**：`POST http://114.214.211.25:30082/api/file/upload`
2. **提交任务**：`POST http://114.214.211.25:30082/api/jobs/tpl`，`model: "reann2.0"`，`taskId` 为 UUID
3. **轮询状态**：`GET http://114.214.211.25:30082/api/jobs?id=<data.id>`
4. **下载结果**：`GET http://114.214.211.25:30082/api/tasks/download?taskId=<taskId>`

> **注意**：`data.id`（整数）用于轮询，提交时自定的 `taskId`（UUID）用于下载，两者不同。

## 调用流程

### 第一步：上传训练包

```bash
FILE_URL=$(curl -s -X POST http://114.214.211.25:30082/api/file/upload \
  -F "file=@reann_training.zip" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'])")
```

### 第二步：提交任务

```bash
TASK_UUID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")

curl -X POST 'http://114.214.211.25:30082/api/jobs/tpl' \
  -H 'Content-Type: application/json' \
  -d "{
    \"params\": {\"inputfile\": \"${FILE_URL}\"},
    \"model\": \"reann2.0\",
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
# 上传并自动等待完成后下载结果
python skills/reann/scripts/reann_run.py --inputfile /path/to/reann_training.zip --created_by <用户名>

# 已有 URL 跳过上传
python skills/reann/scripts/reann_run.py \
  --inputfile http://124.71.201.245/aichem-lab-edge/20260402144008042test-reann.zip \
  --skip_upload --created_by <用户名>

# 仅查询状态
python skills/reann/scripts/reann_run.py --query_task <data.id>

# 仅下载结果
python skills/reann/scripts/reann_run.py --download_result <task-uuid>
```

## 典型工作流

```
vasp-dft（ab initio 计算生成原子结构与力数据）
  → reann（训练 ML 势能面）
  → MD 模拟软件（LAMMPS，使用 REANN_LAMMPS_*.pt 驱动）
```

## Examples

```json
{
  "params": {
    "inputfile": "http://124.71.201.245/aichem-lab-edge/20260402144008042test-reann.zip"
  },
  "model": "reann2.0",
  "parentId": "e3a0a335-17db-44ea-8b39-a3c7f02572f6",
  "taskId": "e3a0a335-17db-44ea-8b39-a3c7f02572f6",
  "createdBy": "user"
}
```

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0 | 2026-04-03 | 初始版本，从 reann2.0_README.md 封装 |

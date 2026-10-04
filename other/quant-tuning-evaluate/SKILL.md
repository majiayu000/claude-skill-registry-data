---
name: quant-tuning-evaluate
description: 执行模型测评（统一入口）。LLM/VLM 走主流程 scripts/run_evaluation.py + Evaluation YAML；model_family=dit 走 DiT 扩展节（references/dit/evaluate_workflow.md，vbench.py 批量推理产出视频）。
license: Apache-2.0
metadata:
  version: 0.3.2
  domain: quantization
  framework: msmodelslim
  protocol: script
  skill_class: tool
  aliases:
    - evaluator
    - evaluation-run
    - dit-evaluate
    - dit-batch-infer
  trigger_intents:
    - 执行测评
    - 运行 run_evaluation
    - 评测模型
    - DiT 批量推理
    - 跑 VBench 视频
  keywords:
    - run_evaluation
    - evaluate
    - aisbench
    - service_oriented
    - vbench
    - vbench.py
    - torchrun
    - batch-inference
---

# Skill: Quant Tuning Evaluate

## Overview

**解决什么**：依据 Evaluation YAML 配置，通过 `scripts/run_evaluation.py` 对量化模型进行评测。

**不解决什么**：
- 不生成/修改 Evaluation YAML → 见 `quant-tuning-evaluation-generator` Agent
- 不执行量化 → 见 `quant-tuning-quantizer` Agent
- 不做策略决策 → 见 `quantization-accuracy-tuning-orchestrator` Skill

**执行主体**：`scripts/run_evaluation.py`（LLM/VLM 主流程；DiT 路径执行主体为 [references/dit/evaluate_workflow.md](references/dit/evaluate_workflow.md) §3 bash 模板）

## 按 model_family 分发

orchestrator 委派本 skill 时按分析结论的 `model_family` 分发：

- `llm` / `vlm_text`：走本文主流程（Evaluation YAML + `run_evaluation.py` 服务化评测，产出结构化分数）
- `dit`：**不进入主流程**，走 DiT 扩展节 → [references/dit/evaluate_workflow.md](references/dit/evaluate_workflow.md)（读推理仓 README 拼 vbench.py argv，批量推理产出视频 + `run_manifest.json`，不评分；评分由 `quant-tuning-score-dit` 接力）

---

## 协作关系

```
quantization-accuracy-tuning-orchestrator (workflow)
        │
        ▼ 调用
quant-tuning-evaluate (tool)
        │
        ▼ Script
  run_evaluation.py
        │
        ▼ 输出
  评测结果 (精度分数)
```

---

## 执行步骤

```
┌─────────────────┐
│ 输入检查        │
│ - config_path   │
│ (Evaluation YAML)│
└────────┬────────┘
         ▼
┌─────────────────┐
│ 服务启动检查    │
│ - 检查 vLLM     │
│   是否就绪      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ execute:        │
│ run_evaluation  │
│ .py             │
│ (启动推理服务   │
│  + 执行评测)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 结果处理        │
│ - 解析精度分数   │
│ - 检查是否达标   │
│ - 错误上报       │
└─────────────────┘
```

---

## 输入参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `quant_model_path` | string | ✅ | 量化后模型路径 |
| `evaluate_id` | string | ✅ | 本轮评测 ID |
| `evaluate_config_path` | string | ✅ | Evaluation YAML 路径（编排层常称 `config_path`） |
| `save_path` | string | ✅ | 评测工作目录 |
| `device` | string | ❌ | 设备类型，默认 `npu` |
| `device_indices` | list[int] | ❌ | 设备索引列表，如 `[0,1]` |

---

## 脚本调用

```bash
python skills/quantizer/quant-tuning-evaluate/scripts/run_evaluation.py \
  --quant-model-path /path/to/quantized \
  --evaluate-id eval-round-1 \
  --evaluate-config-path /path/to/evaluate.yaml \
  --save-path /path/to/workdir \
  --device npu \
  --device-indices 0,1
```

### 错误处理

| 错误类型 | 处理 |
|----------|------|
| msmodelslim 未安装 | 按 prepare_environment.md 安装 |
| 推理服务启动失败 | 检查端口占用、设备可用性 |
| 评测超时 | 检查 `aisbench.timeout` 配置 |
| 精度不达标 | 正常返回结果，由 orchestrator 决策 |

---

## 输出结果

### 成功

```json
{
  "ok": true,
  "results": {
    "gsm8k": {
      "score": 83.5,
      "target": 83.0,
      "passed": true
    },
    "aime25": {
      "score": 52.0,
      "target": 50.0,
      "passed": true
    }
  },
  "overall_passed": true,
  "duration": 1800.5
}
```

### 失败

```json
{
  "ok": false,
  "error": "推理服务启动失败",
  "error_code": "INFERENCE_ERROR",
  "partial_results": {}
}
```

## 执行流程

### 1. 服务启动

调用 `scripts/run_evaluation.py`（`execute`）

### 2. 结果解析

返回每个数据集的分数：

| 字段 | 说明 |
|------|------|
| `score` | 实际精度（百分比）|
| `target` | 目标精度 |
| `passed` | 是否达标（score >= target - tolerance）|
| `overall_passed` | 所有数据集是否都达标 |

`run_evaluation.py` 必须在调用公共 `emit_result()` 前使用 Pydantic JSON 模式序列化 `EvaluateResult`。禁止直接返回 `model_dump()` 的 Python 模式结果，因为其中的 `Decimal`（如 `accuracy`、`target`、`tolerance`）无法由标准 `json.dumps()` 序列化。JSON 模式会将十进制值无损转换为字符串；下游通过 `EvaluateResult.model_validate()` 读取时会恢复为 `Decimal`。

---

## 执行示例

### 标准调用

```bash
python skills/quantizer/quant-tuning-evaluate/scripts/run_evaluation.py \
  --quant-model-path /workspace/output/round_1/quantized \
  --evaluate-id round-1 \
  --evaluate-config-path /workspace/output/evaluate.yaml \
  --save-path /workspace/output \
  --device npu \
  --device-indices 0,1
```

### 结果返回给 orchestrator

```
评测完成:
- gsm8k: 83.5% (目标: 83.0%) ✅
- aime25: 52.0% (目标: 50.0%) ✅
- 总体: 达标
- 耗时: 1800.5s
```

---

## 约束

- **Script-only**：禁止用裸 CLI 替代 `run_evaluation.py`
- **路径格式**：必须是 JSON 字符串
- **单轮单次**：每次调用只执行一次完整评测
- **禁止派生或修改评测配置**：只能按编排层给定的 `evaluate_config_path` 执行评测，**不得**自行派生、修改或生成新的 Evaluation YAML。子集不达标时 fast-fail 跳过后序数据集属正常行为，按原样回传结果，由编排层决策后续流程。评测配置仅由编排层 `evaluation-generator` 生成。
- **服务生命周期**：由脚本内部评测服务管理。如果你需要测多个数据集，请你在测完所有数据集后再关闭服务化，**避免**重复多次拉起。服务化测评运行时长可能较长，超过 timeout 3600s，**务必避免**在测评的中途关闭服务化和测评，你应该等待测评完成，必要时可以通过看日志（如vllm_server.log）最新的消息时间来确认测评任务是否还活跃。

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `port already in use` | 端口被占用 | 更换端口或等待释放 |
| `HCCL init failed` | NPU 通信失败 | 检查 `device_indices` 和设备状态 |
| `evaluate.yaml not found` | 配置文件不存在 | 检查 `config_path` |
| `out of memory` | 设备内存不足 | 换设备 |
| `Object of type Decimal is not JSON serializable` | 使用了 Python 模式 `model_dump()` | 改用 `model_dump(mode="json")`，且不得重新执行已完成的评测 |

若错误不在上述常见错误中或者多次解决后依然未解决，依据[错误上报](references/error_handling.md)，按照错误上报格式返回至`quant-tuning-evaluator` Agent

---

## 检查清单

- [ ] `config_path` 指向的 Evaluation YAML 格式正确
- [ ] `device` 与 `device_indices` 匹配
- [ ] YAML 中的 `ASCEND_RT_VISIBLE_DEVICES` 与 `device_indices` 一致
- [ ] `device_indices` 长度与 `tensor-parallel-size` 对齐
- [ ] 目标端口未被占用
- [ ] NPU/GPU 设备可用
- [ ] msmodelslim 已安装
- [ ] 成功结果可被标准 `json.dumps()` 序列化，并可由 `EvaluateResult.model_validate()` 重新读取

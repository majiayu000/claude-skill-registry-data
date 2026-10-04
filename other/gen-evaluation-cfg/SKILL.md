---
name: gen-evaluation-cfg
description: Generate msmodelslim evaluation YAML configuration (service_oriented + aisbench + vllm-ascend). Use when user asks for evaluation config generation.
license: Apache-2.0
metadata:
  version: 0.9.5
  domain: quantization
  framework: msmodelslim
  aliases:
    - msmodelslim-evaluation-config
    - evaluation-yaml
  trigger_intents:
    - 生成评测配置
    - 写测评yaml
    - 评测配置怎么写
  keywords:
    - evaluation config
    - aisbench
    - vllm-ascend
    - service_oriented
---

# 生成评测配置 YAML

## Overview

本 Skill 负责生成 `quant-tuning-evaluate` / `run_evaluation.py` 所需的单文件评测 YAML 配置。本 Skill 仅生成 Evaluation YAML。不要据此推断 Practice YAML 的 spec.save 应使用 `compressed_tensors`；Practice 的 save 以 tune-practice-cfg 为准，默认情况下使用 `ascendv1_saver`。

**核心功能**：
- 生成包含 `demand`（目标精度）、`evaluation`（AISBench）、`inference_engine`（vLLM-Ascend）三个模块的完整 YAML
- 确保三个模块之间的字段保持一致（模型名、服务地址、端口）

**不适用**：
- 生成其他类型的配置（如量化策略配置）
- 执行评测或分析评测结果等配置生成以外的任务

**模板参考**：[evaluation_config.example.yaml](assets/evaluation_config.example.yaml)

## 输入

执行时从上下文中提取以下信息：

| 参数 | 说明 | 缺省时默认值 |
|------|------|--------|
| 模型名称 | 量化后的模型标识符 | 从上下文获取 |
| 服务地址 | 推理服务 host | `localhost` |
| 服务端口 | 推理服务 port | `8000` |
| 设备类型 | 推理后端设备 | `ascend` |
| 设备索引 | 用户选择的物理设备索引列表，如 `[7]` | 必须从上下文获取 |
| 目标数据集 | 要评测的数据集列表 | 从上下文获取 |
| 精度目标 | 每个数据集的目标精度百分比 | 从上下文获取 |
| 精度容差 | 允许的精度波动范围 | 从上下文获取 |
| `allowed_local_media_path` | VLM 路径任务的显式覆盖目录 | `null`；优先从数据集 README 自动推导 |

## 文件生成规则

### 文件生成步骤

1. 在工作目录生成一个 YAML 文件，包含以下结构：

```yaml
type: service_oriented

demand:
  expectations:
    - dataset: <数据集名称>
      target: <目标精度>
      tolerance: <容差>

evaluation:
  type: aisbench
  precheck: [...]  # 可选
  aisbench: { ... }
  datasets:
    <数据集名称>:
      config_name: <ais_bench 注册名>
      # ...
  host: <服务地址>
  port: <服务端口>
  served_model_name: <模型名称>

inference_engine:
  type: vllm-ascend
  env_vars:
    ASCEND_RT_VISIBLE_DEVICES: <设备索引以逗号连接后的字符串>
  served_model_name: <模型名称>
  host: <服务地址>
  port: <服务端口>
  args: { ... }
```

2. 文件生成后，执行文件检查。如果未通过检查，需要修正后重新生成，直到生成的文件满足所有要求。
3. 如果用户提供了参考的测评配置，则尽可能地按照用户的配置。如果进行了修改，则需要向用户回显该修改，给出简要的原因解释，但不必中断流程向用户确认
4. 文件生成并验证通过后，返回文件路径。

### 关键必填字段填写要求：

| 路径 | 类型 | 说明 |
|------|------|------|
| `type` | string | 必须为 `service_oriented` |
| `demand.expectations` | list | 至少包含一项 |
| `demand.expectations[].dataset` | string | 必须存在于 `evaluation.datasets` |
| `demand.expectations[].target` | float | 必须 > 0 |
| `demand.expectations[].tolerance` | float | 必须 ≥ 0 |
| `evaluation.type` | string | 必须为 `aisbench` |
| `evaluation.aisbench.request_rate` | float | 每秒发送的请求数，必须大于 `0`；< 0.001 为不限速发送，默认设为 `0.0001` |
| `evaluation.datasets` | dict | 必须非空 |
| `evaluation.datasets.*.config_name` | string | AISBench 注册名；输入未指定时按[注册名查找与任务选择](references/how_to_find_aisbench_config_name.md)确定 |
| `evaluation.host` | string | 与 `inference_engine.host` 保持一致 |
| `evaluation.port` | int | 与 `inference_engine.port` 保持一致 |
| `evaluation.served_model_name` | string | 与 `inference_engine.served_model_name` 保持一致 |
| `inference_engine.type` | string | 必须为 `vllm-ascend` |
| `inference_engine.env_vars.ASCEND_RT_VISIBLE_DEVICES` | string | 用户选择的物理设备索引，以逗号连接；如 `device_indices=[7]` 时填写 `"7"` |
| `inference_engine.args.served-model-name` | string | 与 `served_model_name` 保持一致 |
| `inference_engine.args.tensor-parallel-size` | int | 等于 `device_indices` 的元素数量 |

### VLM 字段填写参考：

VLM 测评仍然生成同一类 `service_oriented + aisbench + vllm-ascend` YAML，不新增顶层结构。与 LLM 配置相比，需要考虑以下字段：

| 路径 | 类型 | 说明 |
|------|------|------|
| `evaluation.aisbench.max_out_len` | int | 优先采用模型卡、数据集官方配置或用户明确给出的建议；没有明确依据时使用 `32768` |
| `evaluation.aisbench.batch_size` | int | 请求最大并发数；无通用默认值，信息不足时使用 `16` |
| `inference_engine.args.max-model-len` | int | VLM 默认 `65536`；模型、数据集或用户明确指定时使用指定值，且不能超过模型上限 |
| `inference_engine.args.max-num-batched-tokens` | int | 默认取 `min(max-model-len, 33792)`；显存充足但吞吐不足时再提高 |
| `inference_engine.args.allowed-local-media-path` | string | 仅图片路径任务填写；必须是经过校验的可信绝对目录 |

### VLM 图片输入处理

1. 按[注册名查找与任务选择](references/how_to_find_aisbench_config_name.md)确定或校验 `config_name`，取得 `media_input_type` 和可选的 `candidate_local_media_path`。
2. `media_input_type` 为 `text` 或 `base64` 时，不生成 `allowed-local-media-path`。
3. `media_input_type` 为 `local_path` 时，优先使用显式传入的 `allowed_local_media_path`，否则使用 `candidate_local_media_path`。
4. 将选定目录规范化为绝对路径，并确认它已存在、是目录、可被本次 vLLM 服务访问，且任务运行时发送的媒体文件位于该目录下。禁止使用 `/` 等过宽目录；多个路径任务必须共享一个安全的可信根目录。
5. 校验通过后写入 `inference_engine.args.allowed-local-media-path`。没有候选目录或校验失败时不得生成 YAML；返回 `VALIDATION_ERROR`，说明数据集、`selected_config_name`、候选路径和失败原因，请主 Agent 向用户确认后通过 `allowed_local_media_path` 重试。

### 文件检查步骤（直接检查即可，无需写检查脚本）

1. 确保所有必填字段存在且符合格式要求
2. 确保生成的 YAML 文件语法正确，可以被 YAML 解析器成功解析
3. 如果你在测浮点模型精度基线，则 `demand.expectations[].target` 和 `demand.expectations[].tolerance` **必须**都设置为 100 进行占位。
4. 确保测评配置一致性，你应确保测评浮点权重和量化权重的配置的通用参数一致，尤其是 `evaluation.aisbench`、`inference_engine.args.max-model-len`**必须**保持一致。在不一致的情况下，你应该修改当前生成的配置文件。例如先前生成了浮点的测评配置且已经测评过了，则你应该修改当前生成的量化测评配置。
5. 检查 `inference_engine.env_vars.ASCEND_RT_VISIBLE_DEVICES` 与用户选择的 `device_indices` 完全一致，且 `tensor-parallel-size` 等于设备数量。
6. 对 VLM 配置，按“VLM 图片输入处理”完成任务选择和媒体路径校验。

## 执行约束

**绝对禁止**：
- 不得阅读任何源码文件
- 不得使用 `SemanticSearch` 进行检索

**允许**：
- 使用 `assets/evaluation_config.example.yaml` 作为模板
- 读取本 Skill 直接引用的 `references/` 文件
- 读取 AISBench 数据集 README、模型官方 README/模型卡，以及模型目录中的 `config.json`、`generation_config.json`
- 读取用户提供的已有 Evaluation YAML、AISBench 生成配置、summary、prediction 和服务日志，用于确认推理模式、长度截断与资源参数；只读分析，不修改这些评测产物

## 常见错误

| 错误类型 | 描述 | 修复方法 |
|----------|------|----------|
| 数据集未统一 | `expectations` 中的 dataset 不在 `datasets` 中 | 同步添加或删除 |
| 服务地址不一致 | `evaluation` 与 `inference_engine` 的 host/port 不统一 | 统一设置 |
| 模型名不一致 | `served_model_name` 在三处不统一 | 统一设置 |
| 命名规则错误 | `args` 内使用了 snake_case 而非 kebab-case | 转换为 kebab-case（如 `served_model_name` → `served-model-name`） |
| 配置名错误 | `config_name` 与 ais_bench 注册名不匹配 | 查询正确的注册名 |
| VLM 图片输入方式错误 | 任务输入方式与服务能力不匹配，或路径任务缺少可信媒体根目录 | 按 VLM 图片输入处理流程选择任务或返回主 Agent 确认路径 |

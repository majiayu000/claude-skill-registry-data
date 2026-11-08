---
name: quantization-accuracy-tuning-orchestrator
description: End-to-end automated model quantization and accuracy tuning workflow. Use when user asks for automated model quantization and accuracy tuning, e.g. "自动量化", "量化调优", "一键量化", "精度调优", etc. 当用户给出多卡（≥2 卡）卡号时，量化阶段通过 EP 并行适配（msmodelslim-ep-parallel-adaptation）保证多卡 EP 并行，调优主流程仍在本 Skill。
license: Apache-2.0
metadata:
  version: 0.9.6
  domain: quantization
  framework: msmodelslim
  protocol: mixed
  skill_class: workflow
  aliases:
    - quant_tune
    - quant-tune
    - auto-precision-tuning-expert
    - precision-tuning
    - quantization-tuning
  trigger_intents:
    - 帮我精度调优
    - 帮我量化调优
    - 自动调优量化精度
    - 量化后精度下降怎么办
  keywords:
    - msmodelslim
    - quantization tuning
    - 量化
    - 精度调优
    - 自动调优
    - 最佳实践
    - msmodelslim quant
    - msmodelslim analyze
    - vllm
    - aisbench
    - 精简模式
---

# Skill: 全自动模型调优工作流

## 端到端自动量化与调优功能

端到端自动量化与调优包括**环境准备**、**模型准备**、**量化配置调优**和**结果输出**环节，适用于需要精确控制量化后模型精度的用户，通过自动化的量化配置搜索和评估流程，帮助用户找到满足精度要求的量化方案。本功能支持根据用户指定的精度需求，自动尝试不同的量化配置，并通过评估服务验证量化后的模型精度，最终输出满足需求的量化模型。

关于相关业务的背景知识，如什么是modelslim、什么是量化精度调优等，可以参考[量化自动调优背景知识](references/background_information.md)。

- 支持：
  - Decoder-only LLM 的自动量化与调优
  - VLM 文本主干的自动量化与调优（仅 LLM/文本路径）
  - DiT 扩散模型 的量化（W8A8 动态 data-free；精度调优通过经验库 L2 §7 的 `apply_rollback.py` 整层回退策略扩展 exclude 列表，闭环由本 Skill 调度）
- 不支持：
  - 既非 transformers 也非模型目录内 `modeling_*.py` 的实现
  - DiT 场景下未提供推理仓路径的实现

## 本Skill适用范围

**适用场景**：

- 用户希望通过一键式流程完成模型的量化适配和调优。
- 用户希望对模型进行全自动量化与调优，但没有提供具体操作细节，需要执行默认流程。

**不适用场景**：

- 端到端自动量化与调优功能不支持的技术场景
- 用户只要教程不要代执行

如果用户的需求不符合上述适用场景，你必须放弃执行本Skill，并明确告知用户不适用的原因，必要时引导用户调整需求或使用其他更合适的Skill。

## 整体设定

现在你是一个**自动量化精度调优编排者**，负责在模型量化精度调优的任务中，按照预设的流程和策略，自动化地调用相关的工具、技能和subagent，完成从用户输入到最终交付的整个调优过程。你需要根据用户的需求和反馈，智能地选择调优策略，确保最终输出满足用户的精度要求。

你负责在 msmodelslim 精度任务里决定：

- **按什么顺序**调用哪些 CLI / 脚本（`execute`）与子 agent
- 何时停止调优
- 如何写 history/交付路径

你**不可以**：

- 展开「摸高算法」「exclude 怎么填」、「ModelSlim V1量化配置」「怎么对应量化方案」等细节（动作细节在其它Skill中）
- 直接改源码或以任何形式重构
- 未经用户确认进行大规模代码仓检索

## 工作流

### 1. 用户输入

在任务开始前，你必须从用户那里获取足够的信息来执行调优流程。**用户完全不需要编写任何配置文件**，只需要通过自然语言描述量化需求。例如：

> "帮我把 ./models/Llama-3-8B-Instruct 量化到 NPU，精度损失控制在 2% 以内"

你要：

1. 从用户的描述中提取所有必要参数
2. 智能推导出合理的缺省参数

详细的输入参数列表和相关规则请参考[用户输入](./references/user_input.md)

你根据相关规则判断用户输入的信息是否完整、合理。如果信息不完整或不合理，你**必须**通过**反复的**渐进式提问来引导用户补充缺失的信息，**直到**你获得足够的信息来执行调优流程为止。

在你认为已经获得足够信息来执行调优流程后，你**必须**总结所有参数（包括你自动推导的默认值），并将这些参数以清晰的方式回显给用户，**获得用户的认可**后才可以进入下一步。如果用户对回显的参数有任何异议或需要修改的地方，你必须根据用户的反馈继续调整参数，并再次回显确认，直到用户完全认可为止。

在参数回显获得用户认可后，**必须**执行[路由决策](./references/routing.md)（见下方「1.5 EP 并行适配」），再进入环境准备阶段。

#### 1.5 EP 并行适配（多卡自动切入）

当用户在设备索引处给出**多卡卡号**（≥2 张卡，如 `npu:0,1`、`npu:2,3`、`[0,1,2,3]`）时，本 Skill **主流程保持不变**，仅在量化前委派 **EP 并行适配** Skill（`msmodelslim-ep-parallel-adaptation`），保证后续量化全程以 EP 并行进行：

- **触发条件**：用户给出的设备卡号数量 ≥ 2。
- **动作**：在「模型准备 → 量化配置调优」之间，委派 `msmodelslim-ep-parallel-adaptation` 完成 **MoE 检查 + EP 就绪检查与适配 + `[EP_CHECK]` 验证**，并回传 `EP_ADAPT_RESULT` 与 `requires_ep`。本 Skill 据此决定后续量化是否走 EP：
  - `requires_ep=true`（MoE，EP 已适配）→ **后续调优全程开启 EP 并行**：每一轮量化命令固定使用多卡（`--device npu:0,1,...`），每轮量化日志均须含 `[EP_CHECK]`，评测服务同样保持多卡，中途不得退回单卡 / DP；
  - `requires_ep=false`（非 MoE）→ 退回本 Skill 的普通多卡 / 单卡流程，不涉及专家分片。
- **例外**：若用户明确说明本次任务**不需要**多卡 / EP（如「虽然有多卡，但只用单卡量化」），则仍走本 Skill 的单卡普通流程，不委派 EP 适配。

结构化回退经验（`quantization-expert-experience-tuning-rules`）不属 EP 适配范围：当调优策略为 `standing_high_with_experience` 时，在量化配置调优阶段、进入二分搜索前委派它取得「哪些层需要回退」的结构化意见，作为 practice-generator 生成 Practice 的初值（见[量化配置调优](./references/quantization_tuning.md)「结构化回退经验」）。

详见[路由决策](./references/routing.md)。

### 2. 环境准备

《环境准备》：[环境准备](./references/prepare_environment.md)。该文档会指导你检查和准备执行量化和评估所需的环境，包括必要的库、工具和硬件资源等。如果环境不满足要求，该文档还会指导你协助用户安装或配置必要的环境。你必须确保在进入量化配置调优之前，环境已经准备就绪。

获取用户输入后，你需要执行《环境准备》中的步骤，确保环境准备就绪。

在你确认环境准备就绪后，你需要向用户回显环境准备的结果，并获得用户的认可后才可以进入下一步。如果环境准备过程中出现任何问题，你必须根据《环境准备》中的指导，协助用户解决问题，直到环境准备就绪为止。

### 3. 模型准备

《模型准备》：[模型准备](./references/prepare_model.md)。该文档会指导你检查和准备执行量化和评估所需的模型，包括必要的模型文件、权重、配置、modelslim适配器等。如果模型不满足要求，该文档还会指导你协助用户准备或适配所需的模型。你必须确保在进入量化配置调优之前，模型已经准备就绪。

委派 subagent 时须遵守 [主↔子交互协议 MSAGENT_IO v1](./references/subagent_io_protocol.md)。

环境准备完成后，你需要执行《模型准备》中的步骤，确保模型准备就绪。

基础模型适配完成后，离群值抑制阶段在源码完成所选 `quarot`、`flex_smooth_quant`、
`flex_awq_ssz`、`iter_smooth` 等算法的 Adapter 接口与映射并安装验证，再执行逐算法
processor 与浮点 logits 门禁。失败算法留痕并撤回其本次新增的专用适配代码，
其他算法继续；调优阶段只检查已安装 Adapter 的接口，不读取
前一阶段产物，也不运行离群值门禁。

在你确认模型准备就绪后，你需要向用户回显模型准备的结果，并获得用户的认可后才可以进入下一步。如果模型准备过程中出现任何问题，你必须根据《模型准备》中的指导，协助用户解决问题，直到模型准备就绪为止。

### 4. 量化配置调优

《量化配置调优》：[量化配置调优](./references/quantization_tuning.md)。该文档会指导你根据用户指定的精度要求和模型特点，自动搜索和评估不同的量化配置，以找到满足精度要求的最优量化方案。你必须确保在进入结果输出阶段之前，量化配置调优已经完成。

委派 subagent 时须遵守 [主↔子交互协议 MSAGENT_IO v1](./references/subagent_io_protocol.md)。

模型准备完成后，你需要执行《量化配置调优》中的步骤，确保量化配置调优完成。

### 5. 结果输出

《输出格式》：[输出格式](./references/output_format.md)。该文档会指导你如何根据项目的交付规范，整理和输出最终的调优结果，包括量化后的模型文件、评测报告、调优历史记录等。

在量化配置调优完成后，你需要执行《输出格式》中的步骤，确保最终结果按照规范整理和输出到主对话。

在你向用户回显最终的调优结果后，你需要获得用户的认可，才能确认调优流程已经圆满完成。如果用户对结果有任何疑问或需要进一步的帮助，你必须根据用户的反馈，提供必要的支持和指导，确保用户满意为止。

## 常用脚本（编排层）

通过 `execute` 调用，路径相对于仓库 `skills/` 根目录（或 `get_skill` 定位 skill 根目录后拼接 `scripts/`）：

| 脚本                                                                          | 用途                               |
| ----------------------------------------------------------------------------- | ---------------------------------- |
| `quantization-accuracy-tuning-orchestrator/scripts/history_clear.py`          | 每个调优任务开始前清空一次 history |
| `quantization-accuracy-tuning-orchestrator/scripts/accuracy_lookup.py`        | 量化/评测前查精度缓存              |
| `quantization-accuracy-tuning-orchestrator/scripts/accuracy_append.py`        | 评测后写精度缓存                   |
| `quantization-accuracy-tuning-orchestrator/scripts/history_append.py`         | 每轮结束后追加调优历史             |
| `quantization-accuracy-tuning-orchestrator/scripts/accuracy_cleanup.py`       | 可选，手动清理 accuracy 缓存       |
| `quantization-accuracy-tuning-orchestrator/scripts/finalize_practice_repo.py` | 调优收敛后写入 practice 仓库       |

子步骤见对应 Skill：`tune-practice-cfg`（`msmodelslim analyze` + 校验脚本）、`quant-tuning-quantize`（`msmodelslim quant`）、`quant-tuning-evaluate`（评测脚本）；结构化回退意见见 `quantization-expert-experience-tuning-rules`（`standing_high_with_experience` 策略二分前委派）。

**压缩数据集（默认）**：默认的量化调优过程均使用压缩数据集进行快速迭代。进入循环前**必须**向用户确认来源，三选一：①用户自备已压缩数据集；②委派 `aisbench-dataset-compression-herding` skill 用 RBF Kernel Herding 生成 coreset（仅支持 `aime2025`/`gpqa`，耗时约 30 分钟，已获用户确认后执行）；③用户两者都不愿意时退回全集测试。主流程采用「**子集调优 → 全集验证 → 不通过改全集调优**」：先用子集调优直到子集达标，再全集验证，全集不达标则**直接切换到全集进行调优**，保证最终与全集一致；**不再**采用固定步长逐步收紧子集出口标准的容忍性做法。进入循环前须先确定**子集与全集两个出口标准**：先询问用户是否分别给出，不给出的一方在当前环境跑浮点模型测 FP 基线（**浮点基线评测会额外占用卡数，须向用户提示并确认可用卡**）。详见 `references/quantization_tuning.md` 的「压缩数据集的使用」。

**服务化推理脚本（可选加速）**：压缩数据集来源确认后、进入调优循环前，**须询问用户**是否提供了服务化推理脚本（如常驻 vLLM 服务，支持热加载模型，避免每轮服务启停）。若用户提供，则在每轮评测时优先使用服务化方式——跳过服务启停，直接 reload 模型执行评测，显著加速调优流程。用户可在以下时机提供：

- 调优开始前已预启动服务，将脚本路径与服务地址告知 agent
- 调优过程中由 agent 代为启动常驻服务（首轮启动，后续轮次 reload）
  若用户未提供或不确定，则走默认的每轮启停服务流程。详见 `references/quantization_tuning.md` 的「服务化推理脚本」。

## 子 Skill 路由（按 `model_family`）

主 Agent 读取 `analysis_result.yaml.model_family` 字段，按下表委派到对应子 Skill：

| `model_family`    | 分析                                                                                                                                                                                    | 量化                                                                                                                    | 推理（可选）                                                                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `llm`             | `quant-tuning-analyze-llm`                                                                                                                                                              | `quant-tuning-quantize-llm`                                                                                             | `quant-tuning-infer-llm`                                                                                                                                               |
| `vlm_text`        | `quant-tuning-analyze-vlm`                                                                                                                                                              | `quant-tuning-quantize-vlm`                                                                                             | `quant-tuning-infer-vlm`                                                                                                                                               |
| `dit`             | `msmodelslim-model-analysis`（统一分析：识别 `model_family=dit` + 索取 `inference_repo`，回传 `next_step: model-adapt`）→ `msmodelslim-model-adapt`（DiT 扩展节：适配器生成与四步验证） | `quant-tuning-quantize-dit`（YAML `apiversion=multimodal_sd_modelslim_v1`）                                             | `quant-tuning-infer-dit`（MindIE-SD）                                                                                                                                  |
| `dit`（调优回路） | `quant-tuning-evaluate`（DiT 扩展节，可选 FP baseline 模式，**bash 模板**：通过 `execute` 执行，不是 `Task`）                                                                           | 直接调 `quantization-expert-experience-tuning-rules/scripts/apply_rollback.py`（整层回退）+ `quant-tuning-quantize-dit` | `quant-tuning-evaluate`（DiT 扩展节：vbench.py 批量推理产 infer_outputs）→ `quant-tuning-score-dit`（**脚本**：跑 `scripts/score.py` 做 VBench 评分，AISBench-VBench） |

约束：

- 路由逻辑与既有 LLM 路径完全一致，仅扩展 `dit` 分支
- DiT 量化走 **`MultimodalSDModelslimV1QuantService`**（YAML `apiversion=multimodal_sd_modelslim_v1`），与 LLM/VLM 的 `modelslim_v1` 区分
- 不修改既有 LLM 行为的字段语义
- 共享同一套输出规范（`output_format.md`）、同一套 `workdir/output_dir` 管理、同一套历史/缓存机制
- **不**为 DiT 增加专属输出章节或路径命名规则
- **不**为 DiT 引入新的注册路径（与 LLM/VLM 共用 `config.ini`）

### DiT 调优回路（追加）

按 `model_family=dit` 路由后，orchestrator 委派以下子 Skill（详见 [`docs/dit_tuning/`](../../../docs/dit_tuning/README.md)）：

| 子 Skill / 脚本                                                         | 输入关键字段                                                                                                                                                | 输出关键字段                                                                                                                    | 备注                                                                                                                                                                                                                                                                                                                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `quantization-expert-experience-tuning-rules/scripts/apply_rollback.py` | `--base-practice`, `--first-n-blocks`（或 `--block-indices`）, `--output-practice`                                                                          | `appended`, `md5`, `block_container`（stdout JSON）                                                                             | **直接调脚本，不走 subagent**；`first_n_blocks` 默认值从 [`quantization-expert-experience-tuning-rules/structure-family-pitfalls.md`](../../../msagent/skills/quantizer/quantization-expert-experience-tuning-rules/structure-family-pitfalls.md) §7 读取                                                                                                        |
| `quant-tuning-quantize-dit`                                             | `config_path`, `model_path`, `save_path`, `device`                                                                                                          | `success`, `quantized_path`, `exit_code`                                                                                        | 复用 `quant-tuning-quantizer` 字段表（见 `quantization_tuning.md`）                                                                                                                                                                                                                                                                                              |
| `quant-tuning-evaluate`（DiT 扩展节）                                   | `INFER_REPO`, `FP_WEIGHTS`（→ `--ckpt_dir`，始终 FP）, `QUANT_WEIGHTS`（FP baseline 留空）, `OUT_DIR`, `ROUND`, `NPROC`, `VBENCH_ARGS`                      | envelope: `ok`, `exit_code`, `log_path`, `manifest_path`                                                                        | 本 skill 不评分（仅产出视频）；详见 [`quant-tuning-evaluate/references/dit/evaluate_workflow.md`](../../quant-tuning-evaluate/references/dit/evaluate_workflow.md)。**FP baseline 模式：`QUANT_WEIGHTS` 留空**（vbench.py 的 `--ckpt_dir` 始终指 FP，量化走第二个 flag 如 Wan2.2 `--quant_dit_path`）；orchestrator 启用前必须回显预估时长（FP 比量化慢 1.5-3×） |
| `quant-tuning-score-dit`                                                | `infer_outputs`, `full_json_dir`, `vbench_cache_dir`, `baseline_outputs`（可选）, `score_dimensions`（可选）, `baseline_tolerance`（可选）, `round`（可选） | `scores`, `quality_score`, `semantic_score`, `overall_score`, `commands`；启用 baseline 追加 `loss_vs_baseline`, `is_satisfied` | **已实现**（AISBench-VBench）；需按 §1 触发条件启用                                                                                                                                                                                                                                                                                                              |

完整字段表见 [`references/subagent_io_protocol.md`](references/subagent_io_protocol.md) 末尾的"DiT 调优回路字段"节。

#### 调优循环退出条件（DiT 路径）

`quant-tuning-score-dit` 可返回真实 `is_satisfied`，调优回路具备"达标即停"语义。退出条件按以下顺序判断：

1. **`is_satisfied=true`** —— 仅当 `quant-tuning-score-dit` 成功执行且 `--baseline-outputs` 非空（即与 FP baseline 对比通过）时成立；等价于 `loss_vs_baseline >= -tolerance`（默认 `tolerance=0.05`）。
2. 用户显式说停（`stop_tuning=true`）
3. 达到 `max_iterations`（默认 5）
4. rollback 追加后量化失败 / 推理 NaN → 上一轮作为最优，停止追加
5. `first_n_blocks` 规则耗尽（无法生成新 exclude 项）→ 自动退出
6. `quant-tuning-score-dit` 未启用（用户未提供数据集 / 评分器 / 接受时长）→ **不评分**，按 `max_iterations` / 用户叫停退出。

历史轮次记录由 `quant-tuning-history-append-dit`（若 orchestrator 接入）或既有 `history_append.py` 扩展字段写入。

## 执行注意事项

### 红线和原则：

- **简短回答**：输出内容只包含必要的信息和结果，不要包含任何冗余的解释、背景知识、执行细节等。**禁止**输出长日志。
- **执行范围**：只负责编排量化自动调优，只做上述工作流中指定的事项。禁止任何形式的改业务/框架源码、重构等行为。
- **禁止阅读代码仓**：禁止出于任何目的进行代码仓检索或阅读。
- **官方 CLI / Skill 脚本**：敏感层分析与量化分别使用 `msmodelslim analyze`、`msmodelslim quant`；编排层 history/accuracy 与各 Skill 文档指定的脚本通过 `execute` 调用。禁止伪造输出或跳过 Skill 文档规定的步骤。
- **排障和兜底**：在执行过程中，如果发生错误，必须根据错误类型进行适当的处理：
  - 如果是用户输入不合理或不完整导致的错误，你应该引导用户修改输入；
  - 如果是环境准备或模型准备过程中出现的问题，你应该协助用户解决问题；
  - 如果你确信是你在编排过程中犯了错误，你应该承认错误并进行修正；
  - 对于其它未预见的错误，你必须立即中止当前操作，并报出工具名与错误摘要，不进行任何形式的排障或兜底。
- **磁盘管理**：磁盘中同时**最多存储2份**完整量化权重（同一路径算一份）：**当前调优迭代量化权重**和**已达标调优迭代中的最优一轮的权重**。其余无用权重需要删除来释放空间，禁止文件无限堆积。注意进行删除时**严禁**使用 `rm -rf` 命令，而应该使用 `rm -r`。

### 常见错误

- **错误**：伪造 CLI/脚本成功输出，或未按 Skill 文档执行对应步骤。
  - 原因：违反了 **官方 CLI / Skill 脚本** 原则。
  - 正确做法：分析/量化走 `msmodelslim analyze` / `msmodelslim quant`；编排与校验/评测走文档指定的脚本；以 exit code 或 stdout JSON 判定成败。
- **错误**：命令失败后换未文档化的命令续跑以规避问题。
  - 原因：违反了 **排障和兜底** 原则。
  - 正确做法：无法解决则立即中止，报命令名与错误摘要。
- **错误**：遇到报错后通过修改源码来规避。
  - 原因：违反了**执行范围**约束中禁止改业务/框架源码的原则。
  - 正确做法：遇到报错时，应通过正当途径解决，而非修改源码。
- **错误**：在磁盘中存储了**大于等于3份**模型权重。
  - 原因：违反了**磁盘管理**原则。
  - 正确做法：严格遵守磁盘管理原则，控制模型权重的存储数量。
- **错误**：通过阅读代码来推断用户环境信息。
  - 原因：违反了**禁止阅读代码仓**原则。
  - 正确做法：应通过用户输入或明确询问来获取环境信息，不应阅读代码。

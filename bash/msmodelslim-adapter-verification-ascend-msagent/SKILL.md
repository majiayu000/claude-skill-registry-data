---
name: msmodelslim-adapter-verification
description: 为 msModelSlim 适配器执行功能性验证。适用于基础适配器开发完成后，自动执行四步验证（测试模型、全回退量化、权重一致性与可加载/保存、实际量化规则校验）并输出通过/失败结论。
---

# msModelSlim 适配器功能性验证 Skill

用于在基础适配器开发完成后，自动帮助用户进行功能性验证。

## 触发条件

- `msmodelslim-model-adapt` 已完成适配器开发与注册安装。
- 用户希望确认适配器是否可用，或要求执行标准验证流程。

## 执行要求

- 必须按顺序执行四步验证，不可跳步。
- 每一步失败都要立即停止并返回失败原因与下一步修复建议。
- 仅当四步全部通过时，返回“功能性验证通过”。
- 修改代码后要执行 `bash install.sh` 重新安装msModelslim
- **NPU 卡号选择（仅 DiT 适用）**：执行任何 NPU 步骤前**必须先 `export ASCEND_RT_VISIBLE_DEVICES=<物理卡号>`**（如 `export ASCEND_RT_VISIBLE_DEVICES=0`；不设置时 CANN 默认用 0 号卡且不报错）。`--device` 仅接受字面量 `npu` / `cpu`（不要传 `npu:0` / `npu:x`）。完整说明见 [`references/verification_guide.md`](references/verification_guide.md) 的"设备与卡号选择"小节。
- 若验证过程中出现模型实现文件（如权重目录内 `modeling_*.py`）报错，必须先判断是否为 `transformers` 版本不契合导致。
- 对疑似版本不契合问题，必须先告知用户并确认版本需求（目标版本或可接受版本区间）；未确认前不得切换版本。
- 仅在用户确认后，才可执行 `transformers` 版本切换与重试验证。

## 四步验证流程

1. Step1：生成随机权重测试模型。
2. Step2：执行全回退量化，验证流程与注册生效。DiT **先 `export ASCEND_RT_VISIBLE_DEVICES=<物理卡号>`**，再传 `--device npu` + `--inference-repo`，配置模板见 `references/dit/`。
3. Step3：验证 Step2 与 Step1 的权重严格一致，且产物可完整加载/保存。
4. Step4：执行实际量化（W8A8 静态/动态）并校验描述文件规则。

### 模型族与 Step1 随机权重

| 族 | 是否推荐随机权重 | 备注 |
|---|---|---|
| LLM | 推荐 | `transformers.AutoModel*` 提供统一入口，2 层小模型便宜 |
| VLM | 推荐 | 同上，走 `AutoModelForImageTextToText` |
| DiT | **不推荐** | 各厂商 inference repo 加载范式分裂（diffusers / 自定义 class / MoE 子目录），无统一随机权重工厂。请用 `step1 --skip-random-model` 走零拷贝路径：step1 只校验，step2/step3 直接消费 `model_path`。 |

`--skip-random-model` 行为：
- 不构造随机权重，**不复制权重**，**不写任何东西到 `--output-path`**。
- 只做最小校验：`--model-path` 是目录；顶层（或 DiT 每个 `*_model` 子目录的）`config.json` 存在且为合法 JSON。
- step2 直接消费 `--model-path`；step3 通过 `--reference-weights` 指向同一路径做权重对比，避免先复制再比对的多余 IO。
- **设计动机**：Wan2.2-T2V-A14B 等大型 DiT 模型动辄几十 GB，复制一份要数分钟并占双倍磁盘；透传原路径实现零拷贝。

### Step3 基线来源

| 参数 | 含义 |
|---|---|
| `--original-path` | step2 量化输入的目录。skip 模式下一般传 `--model-path` 的同值（因为 step2 直接从这里读），但严格说 step2 不强制要求它等于 step1 的输出。 |
| `--reference-weights` | 显式基线目录，**覆盖** `--original-path` 作为对比左值。skip 模式下**必须**指向用户提供/已下载的真实模型目录（即 `--model-path`）。 |

## Buffer 权重说明（Step3 常见问题）

- 若 Step3 出现“全回退权重缺失/键不一致”，需优先检查缺失项是否来自模型 `buffer`。
- `msmodelslim` 通常不会保存 `buffer` 类型权重，因此可能导致全回退产物缺少对应键。
- 适配器需要主动将这类关键 `buffer` 转为 `nn.Parameter`，以确保量化导出和一致性校验可覆盖该权重。

## transformers 版本兼容处理（验证期）

- 触发条件：验证阶段出现模型实现文件导入/模型forward错误，且报错指向 `transformers` API 变更、缺失符号或签名不匹配。
- 必做沟通：向用户说明“当前报错疑似版本兼容问题”、给出关键报错摘要、请求确认目标版本策略（指定版本或版本区间）。
- 搜索策略：获用户确认后，使用二分法在确认范围内搜索可用 `transformers` 版本（每次切换版本后需重装并重跑触发失败的验证步骤）。
- 收敛标准：找到“可成功加载并通过对应验证步骤”的版本后停止搜索，并将最终版本写入msModelslim的config.ini。
- 失败处理：若二分搜索后仍无可用版本，返回阻塞结论并要求用户提供官方建议版本或模型实现修订方案。

## 权重安全（必读）

四步验证不应该碰原始权重。step3 / step4 只读；step1 的 `--skip-random-model`
只做 JSON 校验、不写盘；step1 随机权重路径与 step2 只写 `--output-path`。

step1/step2 **硬拒绝**任何会写进原始权重目录的 `--output-path`：
`output_path == model_path`、`output_path` 在 `model_path` 内部、或 `output_path`
是 `model_path` 的父目录，一律 fail-fast。

**DiT 永远不要就地改写原始权重**——要零拷贝消费真实权重就用 `--skip-random-model`，
那条路径一个字节都不写。要小模型就写到独立目录。

## 自动化脚本

- `scripts/step1_generate_test_model.py`
- `scripts/step2_run_quantization.py`（LLM / VLM）
- `scripts/step2_run_quantization_dit.py`（DiT；独立脚本，自带预检与推理仓注入）
- `scripts/step3_verify_weights.py`
- `scripts/step4_verify_quant_description.py`

### 配置模板

step2 的全回退配置不再内联在脚本里，统一从 `references/<family>/fallback_config.yaml` 读取；
step4 的全模型量化模板在同目录。改配置直接改 YAML，不要改脚本。

| family | 模板目录 | apiversion |
|---|---|---|
| llm | `references/llm/` | `modelslim_v1` |
| vlm | `references/vlm/` | `multimodal_vlm_modelslim_v1` |
| dit | `references/dit/` | `multimodal_sd_modelslim_v1` |

DiT 专有参数（见 [`references/dit/README.md`](references/dit/README.md)）：

| 参数 | 说明 |
|---|---|
| `--calib-dataset` | 写入 `spec.dataset`。缺省时用 `references/dit/index.example.jsonl` 在 `<output-path>/calib_data/` 生成一份自建校准集并指向它 |
| `--inference-config-json` | JSON 串或文件，合并进 `multimodal_sd_config.inference_config`。全回退阶段可不传 |
| `--inference-repo` | 推理仓路径，设 `WAN_INFERENCE_REPO` 并前插 `PYTHONPATH`。**Wan 系必传**，否则 `ImportError: Failed to import WanModel` |

step2 在调用 msmodelslim **之前**会对最终配置做一轮预检（`spec.dataset` 必填且为 str、
`enable_dump` 应为 `false`（DiT data-free 不 dump 校准数据，`true` 会告警）、
apiversion 与 family 匹配、校准集路径可解析）。
`--config-path` 指定的现成配置同样过预检。

DiT 模板的三条硬约束与 `inference_config` 字段速查在 [`references/dit/README.md`](references/dit/README.md)，
按需读取——非 DiT 任务不必加载。

## 参考资料

- [适配器验证指南](references/verification_guide.md)
- [DiT 模板三条硬约束与 inference_config 字段速查](references/dit/README.md)

## 输出格式要求

- 给出每一步的执行结果（PASS/FAIL）。
- 若失败，标注失败步骤、错误要点、建议修复方向。
- 最后给出总结结论：通过 / 未通过。

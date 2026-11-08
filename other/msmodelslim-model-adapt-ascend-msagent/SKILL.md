---
name: msmodelslim-model-adapt
description: 为 msModelSlim 创建基础 Transformers 模型适配器（Model Adapter）。
  包含创建适配器、实现必需接口与注册安装流程。
  适用：Decoder-only LLM、理解类 VLM（仅 LLM/text 部分）。
  多模态生成（DiT/扩散，含双/多专家）见下方「多模态生成扩展」节，按需加载。
  不适用：Encoder-only、非 Transformers 架构。
---

# msModelSlim 基础模型适配 Skill

本 Skill 指导如何为新模型创建适配器，使其跑通基础量化流程。

> 说明：逐层量化（按层加载/懒加载）属于高阶可选特性，不是基础适配必需项。
> 仅当 CPU 内存无法全量加载权重，或用户明确要求时，再在基础适配和四步验证（由 `msmodelslim-adapter-verification` 执行）完成后启用。

> 多模态生成（DiT/扩散，含双/多专家）请跳到「[多模态生成扩展](#多模态生成扩展dit--扩散)」节，**不要与下方 LLM/VLM 主流程混淆**。

## 适用范围

- **支持**：Decoder-only LLM、理解类 VLM（只处理文本/LLM 主干）
- **多模态生成（DiT/扩散）**：见下方「多模态生成扩展」节，按需加载
- **不支持**：Encoder-only、非 Transformers 架构

## 核心工作流

### 1. 权重来源确认（新增必做提示）

- **先询问并优先使用用户自有权重**：要求用户先提供本地模型权重路径（或已下载模型目录）。
- **仅在用户确认"没有权重"时再下载**：再协助用户执行下载流程，不要默认直接下载。
- **下载建议**：
  - 若先做结构分析，可先下载非权重文件：`modelscope download --model <org>/<model> --local_dir ./models/<name> --exclude '*.safetensors'`
  - 若进入完整量化/验证流程，需补齐可用权重文件。

### 2. 准备工作

- **分析模型**：阅读 `config.json` 与 `modeling_*.py`，确认结构与实现。
  - 详见：[模型结构分析指南](references/model_analysis.md)

### 3. 创建适配器

- **使用模板**：
  - LLM: `assets/model_adapter_template.py`
  - VLM: `assets/vlm_model_adapter_template.py`
- **实现接口**：实现 `handle_dataset`, `init_model`, `generate_model_visit`, `generate_model_forward`, `enable_kv_cache`。
- **关键原则**：
  - `visit` 与 `forward` 必须严格一致。
  - MoE 模型建议 unpack 为纯线性层。
  - 若原始模型存在需要保留的 buffer 权重，需在适配器中将其转换为 `nn.Parameter`；否则量化导出阶段通常不会保存 buffer 权重。
  - **Tokenizer pad_token 兼容性必查**：若 `tokenizer.pad_token` / `pad_token_id` 为 `None`，必须在适配器中重写 `_load_tokenizer`，将 `pad_token` 回退到 `eos_token`，避免量化过程中在 `padding=True` 时直接报错。
  - 常见报错：
    - `ValueError: Asking to pad but the tokenizer does not have a padding token.`
  - 根因链路：
    - `adapter.handle_dataset(...) -> _get_tokenized_data(...) -> tokenizer(..., padding=True, ...)`
    - 某些模型（如 MiniMax 系列）原生 tokenizer 未设置 `pad_token`。
  - 推荐修复模板：
    ```python
    def _load_tokenizer(self, trust_remote_code=False):
        """Ensure tokenizer has a pad token for quantization dataset padding."""
        tokenizer = super()._load_tokenizer(trust_remote_code=trust_remote_code)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        return tokenizer
    ```
  - 说明：优先使用 `eos_token` 作为回退；若目标模型有更合适的专用 pad token，可按模型官方约定替换。
  - 详见：[适配器实现指南](references/implementation_guide.md)

### 4. 注册与安装

- 在 `config/config.ini` 注册模型与入口，并执行 `bash install.sh` 安装msModelSlim。
- 详见：[适配器注册指南](references/registration_guide.md)

### 5. 功能性验证（独立 Skill）

- 适配器开发完成后，告知用户可自动执行功能性验证。
- 验证流程已独立为：`msmodelslim-adapter-verification`。
- 该验证 Skill 会自动按四步执行：生成测试模型 -> 全回退量化 -> 权重一致性与可加载/保存验证 -> 实际量化与描述文件规则校验。

### 6. 可选高阶特性：逐层量化

- 触发时机：
  - CPU 内存无法全量加载模型权重。
  - 用户明确要求"逐层量化/逐层加载/懒加载/按层加载"。
- 启用顺序：
  - 必须先完成基础适配与四步验证，再进入逐层量化改造。
- 实现与验证指引：
  - 详见独立 Skill：`msmodelslim-layer-wise-quantization`

---

## 多模态生成扩展（DiT / 扩散）

> 本节是 LLM/VLM 主流程之外的**并列分支**。
> 触发条件：模型族不属于 LLM/VLM，且包含 DiT/扩散架构信号（`_diffusers_version`、主仓 `msmodelslim/config/config.ini` 多模态生成族、关键词如 `文生视频 / 扩散 / Wan / FLUX / SD3`）。
> 进入本节后，**不要回到 LLM/VLM 主流程**——两者路径独立。

### E0. 模型族识别

- **优先复用 `msmodelslim-model-analysis`** 既有结论；识别失败再走本节路径。
- 多模态生成模型**必须由用户提供 `inference_repo`**（与权重目录互不包含的独立推理仓）。
  - 识别后用 `AskUserQuestion` 强提示并强制要求用户提供；仅做"路径存在且为目录"校验。
  - 不要默认下载——先问权重，再问推理仓。

### E1. 选择模板与读实现指南

> **全部 DiT 实现细节**（目录结构、模板、11 接口、行为差异、特殊情况、原则、注册、checklist）见：
> [references/dit/implementation_guide.md](references/dit/implementation_guide.md)
> 进入 DiT 路径后，**只读那一个文件即可**；主路径文件不再提供 DiT 细节。
>
> **流程编排与分发上下文**（orchestrator 委派本 skill 且 `model_family=dit` 时按本工作流执行，不进入 LLM/VLM 主流程）见：
> [references/dit/adaptation_workflow.md](references/dit/adaptation_workflow.md)

模板入口（指针）：

| 子架构        | 模板/骨架                              |
| ------------- | -------------------------------------- |
| DiT 单网络    | `assets/dit_model_adapter_template.py` |
| DiT 双/多专家 | `assets/dit/skeleton.md`               |

### E2. 四步验证 flag（DiT 必加）

| flag                         | 含义                   |
| ---------------------------- | ---------------------- |
| `--skip-random-model`        | DiT 不接受随机权重生成 |
| `--model-family dit`         | 标识 DiT 族            |
| `--inference-repo <path>`    | 推理仓路径             |
| `--reference-weights <path>` | 参考权重路径           |
| `--rules-path <path>`        | 描述文件规则路径       |

详见 `msmodelslim-adapter-verification` 的「四步验证流程」表格。每步 `passed=true` 才视为通过；任一失败即中止并回传 `status: failed`。

### E3. IO 参数（DiT 专属）

```json
{
  "model_type": "<registered_model_type>",
  "model_path": "/abs/path/to/weights",
  "inference_repo": "/abs/path/to/inference_repo",
  "trust_remote_code": true,
  "save_path": "/abs/path/to/workdir",
  "model_family": "dit",
  "device": "npu",
  "ascend_rt_visible_devices": "0",
  "verification_required": true
}
```

---

## 参考资料

- [模型结构分析指南](references/model_analysis.md)
- [适配器实现指南](references/implementation_guide.md)（LLM/VLM）
- [适配器注册指南](references/registration_guide.md)
- [接口检查清单](references/interface_checklist.md)
- [核心工作流](references/core_workflow.md)
- [DiT 实现指南](references/dit/implementation_guide.md)（DiT 任务专用，按需加载）
- [DiT 通用陷阱清单](references/dit/pitfalls.md)
- [DiT 架构模式](references/dit/architecture_patterns.md)

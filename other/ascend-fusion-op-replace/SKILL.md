---
name: ascend-fusion-op-replace
description: 针对昇腾 NPU 上的 PyTorch 模型，识别可做融合算子替换的代码段、替换为 torch_npu 融合算子并做性能/精度验证。当用户提到融合算子、NPU 算子替换、RMSNorm/SwiGLU/RoPE/Attention 融合、torch_npu 亲和算子等关键词是，使用本 Skill。
---

# 融合算子识别与替换

## 这个 Skill 做什么

针对昇腾 NPU 上跑的 PyTorch 模型（训练或推理），找到可以用 `torch_npu` 融合算子替换的代码段，给出替换示例，再做性能和精度验证，最终给出"该不该换"的结论。

整个工作分两个阶段，**阶段一输出识别报告后必须停下来等用户确认**，确认后再进阶段二逐个验证。

## 核心概念

- **融合算子**：把多个连续计算层（如 matmul→激活→归一化）合并成一个 NPU 硬件内核，中间结果不写回显存。典型：`npu_fusion_attention` 把 Q@K^T→mask→softmax→@V 合成一个算子。
- **亲和算子**：不改数学逻辑，仅把 NPU 不擅长的随机访存指令等价代换成连续乘加。典型：IndexPut→乘法、where→lerp。
- **亲和 API**：NPU 官方高阶封装函数，内部串联多个亲和算子。典型：`NpuFusedAdamW`。

本 Skill 主要处理融合算子替换；亲和算子/亲和 API 在"高频算子序列"环节顺带识别。

## 全局代码替换规范（严格执行）

无论是阶段一报告中的代码示例，还是阶段二实际修改的代码，**所有生成的替换代码必须满足以下生产级条件，绝不允许使用伪代码**：

1. **非破坏性修改 (Fallback 机制)**：必须通过参数（如 `args` 或 `model.config`）或 `is_torch_npu_available()` 进行条件判断，**必须原样保留原代码作为 else 分支**。
2. **Dtype 严格对齐与 AMP 意识**：必须保证融合算子分支的输出 dtype 与原生分支完全一致。注意记录并保持原有的 Autocast 状态，防止因替换 API 导致异常的类型强转（注意 float16/bfloat16/float32 在特定 NPU 算子下的支持度差异）。
3. **Layout 与连续性保障**：NPU 融合算子对 Tensor 内存布局敏感。在传入融合 API 之前，需确保输入 Tensor 是连续的，适时使用 `.contiguous()`，并在 Fallback 分支中考虑其影响。
4. **优先复用**：优先复用目标仓库内已有的开关参数、全局环境变量或 wrapper 命名。

## 两阶段工作流

```
阶段一（识别，必做）                      阶段二（逐个验证，按用户确认的清单）
┌──────────────────────────┐    用户确认   ┌──────────────────────────┐
│ 1. 常用融合算子扫描（必做）│ ──────────► │ 1. 按条件分支改代码        │
│ 2. 高频算子序列识别（advanced）│  暂停     │ 2. 逐个跑：精度优先        │
│ 3. 融合价值评估            │  不改代码   │ 3. 精度不过→直接否决        │
│ 4. 输出 markdown 识别报告  │            │ 4. 精度过→再看性能         │
└──────────────────────────┘            └──────────────────────────┘
```

---

## 阶段一：识别可替换的融合算子

### 1.1 常用融合算子（必做项）

拿着模型代码，对照下表，看有没有匹配得上的代码逻辑：

| 手写模式 | 融合 API | 一句话要点 |
|----------|----------|-----------|
| 手写 RMSNorm（`x.pow(2).mean → rsqrt → * weight`） | `torch_npu.npu_rms_norm(x, weight, epsilon=eps)` | 返回 tuple，取 `[0]`；最简单、收益稳定 |
| `a1 * F.silu(a2)` 门控乘法 | `torch_npu.npu_swiglu(x, dim=-1)` | concat 顺序必须正确：`[a2, a1]` 让 `SiLU(a2)*a1` |
| 手写旋转位置编码（`t*cos + rotate_half(t)*sin`） | `torch_npu.npu_rotary_mul(t, cos, sin)` | cos/sin 需 `expand_as(t_)`；处理 t_pass_ concat 回来 |
| 手写 `Q@K^T → mask → softmax → @V` | `torch_npu.npu_fusion_attention(...)` | 必须显式 causal mask；atten_mask 中 True=屏蔽；返回 tuple 取 `[0]` |
| MoE expert 循环 matmul | `npu_grouped_matmul` / `Ops.gmm` + `npu_moe_token_permute/unpermute` | 需确认 expert 归属、weight layout、空 expert、routing weight |

**每个算子的详细识别 pattern、原始→NPU 完整代码对照、踩坑点和 concat 顺序推导，见 `references/common_fusion_ops.md`。** 在写替换代码前务必读对应小节，并用 `scripts/query_torch_npu_api.py` 查询当前环境的 API 说明文档确认签名、参数约束和返回值；脚本查不到时再看文档链接或在线文档兜底。同时在目标仓库内搜索已有融合算子实现，优先参考项目内已验证的 wrapper、开关命名、layout/mask 处理和 fallback 写法。

### 1.2 高频算子序列识别（advanced，基于 profiling）

如果用户提供了替换前的 profiling 数据（或主动采集了），基于 profiling 里的高频算子序列，能发现常用清单覆盖不到的融合机会。在 `kernel_details.csv` 里找属于同一模块、上下衔接的算子序列（如 `slice+matmul+gelu`），按 pattern 去知识图谱或 `torch_npu` API 列表找现成融合 API。**注意算子序列必须属于同一模块、上下衔接，不要跨模块拼凑。**

如何从 profiling 判断这段代码到底是不是融合有价值的瓶颈，见 `references/fusion_value_assessment.md`（含 Roofline 加速上限表、Memory/Compute/Launch-bound 现象对照）。

### 1.3 限制条件与边缘场景排查（重点防范）
在识别出候选算子后，必须评估以下边缘场景：
- 动态 Shape 敏感性：评估该代码段是否涉及动态 Shape（如每次输入的 Sequence Length 均不一致）。若存在动态 Shape，NPU 算子可能会发生频繁 Re-compile 严重拖慢性能，需在报告中明确预警并评估是否值得替换。
- 连续性要求：排查输入 Tensor 是否经过切片（Slice）、转置（Transpose）等破坏内存连续性的操作

### 1.4 输出格式

阶段一只输出 Markdown 识别报告，不修改模型代码。报告必须包含：汇总表、逐个候选分析（、建议顺序，以及符合全局代码规范的生产级代码替换示例。具体参考 `references/identification_report_format.md`。

### 1.5 阶段一边界

阶段一结束后**不要直接进阶段二改代码**。先输出 Markdown 识别报告，让用户确认认可哪些替换、做哪些。用户确认后再进阶段二。

---

## 阶段二：修改代码 + 逐个验证

进入阶段二的前置条件：**用户输入必须包含可以实际运行模型的脚本、命令或等价拉起方式**。如果没有，先向用户索要。

### 2.1 代码修改与适配

严格遵循前文定义的【全局代码替换规范】修改代码。示例：

```python
args = get_args()
if args.use_fused_rmsnorm and is_torch_npu_available():
    # aclnnRmsNorm 支持 FP32 gamma，对 FP32/BF16 输入都成立
    output = torch_npu.npu_rms_norm(hidden_states, self.weight.float(), epsilon=self.variance_epsilon)[0]
else:
    # 原 fallback 分支原样保留
    input_dtype = hidden_states.dtype
    hidden_states = hidden_states.to(torch.float32)
    variance = hidden_states.pow(2).mean(-1, keepdim=True)
    hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
    output = (self.weight * hidden_states).to(input_dtype)
return output
```

控制方式优先级：**项目已有参数 > 新增参数 > 环境变量 > 仅判断 `is_torch_npu_available()`**。

### 2.2 评测原则：精度优先，逐个对比 baseline

**第一步：算子级精度对齐 (Unit-level Validation)**  
在跑端到端训练前，先造一组与模型实际 input shape/dtype 完全一致的随机 Tensor，分别送入原生算子和 NPU 融合算子，对比输出结果的差异。

- 标准：Cosine Similarity > 0.999 或 Max Absolute Error (MAE) < 1e-4。  
- 若单算子级未对齐，直接判定为不通过，无需进入后续 E2E 测试。

**第二步：端到端精度验证 (E2E Loss Validation)** 
算子对齐后，跑 50+ 个迭代，要求修改前后 Loss diff 在 1% 以内。如果早期迭代就有明显精度溃散，提前结束。精度不满足 → 直接标注不通过，跳过性能评测。

**第三步：性能验证** 
精度通过后测性能，默认不开 profiling。主要关注端到端 step_time：是否有稳定下降。


### 2.3 数据记录与报告生成

验证期间从日志提取逐 step 数据（step id / loss / step_time）写入 JSONL；每个候选验证完后复制 `assets/validation_report_template.html` 模板、替换 REPORT_DATA 生成 HTML 报告。详细流程、JSONL 格式、REPORT_DATA 字段说明见 `references/verification_workflow.md`。

### 2.4 长任务过程记录

用 TaskList 跟踪每个候选替换的验证状态（待测 / 精度验证中 / 精度不通过 / 性能验证中 / 已结论），结论写进本地 markdown，方便中断后续接。

---

## 相关脚本

- `scripts/query_torch_npu_api.py` — 查 API 签名/约束，写替换代码前必用
- `scripts/merge_jsonl.py` — 合并 baseline+fused JSONL 为模板 metrics 数组
- `assets/validation_report_template.html` — 验证报告 HTML 模板，复制后替换 REPORT_DATA
- 算子信息在线文档：https://gitcode.com/Ascend/op-plugin/tree/master/docs/zh/custom_APIs/torch_npu

---

## 决策清单

- [ ] 用户给的是模型代码/拉起脚本？有没有替换前 profiling 数据（有则进 1.2）？
- [ ] 常用融合算子清单逐个扫了吗？仓库内已有融合实现搜过了吗？
- [ ] 替换 API 的签名/约束查了 `query_torch_npu_api.py` 而非凭记忆吗？
- [ ] 阶段一报告输出后，停下来等用户确认了吗（没直接改代码、没生成 HTML）？
- [ ] 阶段二逐个验证，精度优先，精度不过直接否决了吗？
- [ ] 逐 step 数据写进 JSONL 了？验证完用模板生成 HTML 报告了？
- [ ] 长任务过程记录和 TaskList 跟上了吗？

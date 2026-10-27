---
name: triton-op-designer
description: >
  Triton Ascend 算子算法草图设计 Skill — 根据任务描述设计高质量的算法草图（sketch），
  用于指导后续代码生成。支持首次设计和基于历史上下文的迭代优化。
  触发：当用户需要为 Triton Ascend 算子设计算法草图或在已有 sketch 基础上迭代时使用。
argument-hint: >
  输入：op_name、task_desc（任务文件内容）、arch。
  可选：user_requirements、gpu_kernel_ref（GPU Triton kernel 参考源码）、previous_sketch、history_context、inspirations。
  输出：UnifiedSketch DSL 格式的算法草图。
  固定参数：backend=ascend、framework=torch、dsl=triton_ascend。
---

# Triton Ascend 算法草图设计 Skill

<role>
你是一个高性能计算的算法设计专家。

你的任务是基于以下固定配置设计高质量的算法草图（sketch）：

- **目标 DSL**: triton_ascend
- **目标框架**: torch
- **目标后端**: ascend
- **目标架构**: {{ arch }}

⚠️ 你**仅生成算法草图**，不生成可执行代码。草图用于指导后续的代码生成（triton-op-coding）。
</role>

## 输入信息

你将获得以下信息：

1. **任务描述和规格说明** — 算子任务格式的算子需求（包含 `Model` 类）
2. **GPU Triton kernel 参考实现**（`gpu_kernel_ref`，可选）— 来自 GPU 的已有 Triton kernel 实现，可作为算法结构和 tiling 策略的参考
3. **相关的知识和示例** — UnifiedSketch DSL 规范和设计模式（见下方知识加载规则）
4. **执行历史** — 之前的设计反馈和优化建议（迭代设计时）
5. **算子类别约束卡**（若存在）：cannbot-knowledge 知识库卡片 `$KB_ROOT/ops/triton/guides/constraints/{category}_constraints.md`（KB_ROOT 解析见「知识库定位」；类别名换算与例外见「知识加载规则」）。该卡包含经过验证的 **Layer 1 设计约束**（硬性规则，必须遵守）和 **Layer 2 算法骨架**（可参考的架构方向）。设计前必须读取并理解。若草图架构与 Layer 1 任何一条冲突，必须重新设计草图，**不得将冲突下放到代码生成阶段**。

### GPU kernel 参考使用规则

当传入了 `gpu_kernel_ref` 时：

- **理解算法结构**：参考 GPU kernel 的 grid 划分、数据流和并行策略，但**不要照搬** GPU 特有的优化（如 CUDA shared memory）
- **参考 tiling 策略**：BLOCK_SIZE 选择、维度切分方式可作参考起点，但需适配 Ascend UB 容量和对齐要求
- **注意 API 差异**：GPU Triton 的部分 API（如 `tl.dot` 的参数、atomics 行为）可能与 Ascend 不同，草图设计应以 Ascend 文档为准
- **剔除 GPU 特有参数**：GPU kernel 中的 `num_warps`、`num_stages`、`num_ctas` 等参数在 NPU 上不生效，草图设计时直接忽略，使用 Ascend 的配置方式（如 `num_cores`）
- **下标 dtype**：FLA/GPU 的 `program_id().to(tl.int64)` 不要写进 `o_t` 等 **mask 比较链**（草图标 int32）；`bos`/`i_tg` 等 **指针基址标 int64**。

## 知识检索前置（强制，设计前必做）

在加载任何参考文档、给出草图之前，**必须先做一次 KB 检索**，避免凭记忆或凭 GPU 参考直接设计：

1. 运行 knowledge-query 的 `preflight` 检索（脚本候选：`$PWD/.claude/skills/knowledge-query/scripts/knowledge_query.py`、`$PWD/.agents/skills/knowledge-query/scripts/knowledge_query.py`）：
   ```
   knowledge_query.py preflight --task "<当前设计目标：算子名 + 类别 + 关键约束/难点>"
   ```
2. 读取 `preflight` 返回的 `read_first` 主证据卡（用 `Read local_path` 深读），按 `sufficiency_rule` 判断证据是否足够；不足时按 `follow_candidates` 追 `neighbors` / `pipeline` / 二次 `preflight`。
3. 约束卡加载仍按下方「知识加载规则」的 `$KB_ROOT(...)_constraints.md` 映射执行，二者互补不重复轮询。
4. 检索完成后，**必须在终端输出以下盒装摘要**（草案阶段的可复核痕迹）：
   ```
   ┌─ KB 知识检索摘要 [designer preflight] ──────────
   │ 主证据卡: <doc-id 1..3>（<strong/medium/weak>）
   │ 证据充分性: <已满足 sufficiency / 需追 neighbors·pipeline>
   │ 应用策略: <直接复用 / 读取 read_first 后按约束设计 / 二次检索>
   └─────────────────────────────────────────────
   ```
5. 若 knowledge-query 不可用或 KB 解析失败，回退到「知识加载规则」的通用加载路径，不阻塞设计流程，并在摘要注明「KB 不可用，按内置约束设计」。

> 检索是证据前置，不是装饰：设计结论必须落到 `@references/sketch-design.md` 语法与下方约束卡 Layer 1 之上，检索到的 GPU 参考只作算法结构参考，不覆盖 Ascend 约束。

## 知识加载规则

### 知识库定位（KB_ROOT 解析，加载任何 KB 卡片前先执行）

本 skill 的领域知识卡片全部位于 cannbot-knowledge 知识库。按优先级解析 `KB_ROOT`：

1. 环境变量 `CANNBOT_KNOWLEDGE_ROOT`（已设置且目录存在）；
2. 从当前工作目录及其至多 6 级祖先探测 `.cannbot/dependencies/*/cannbot-knowledge/knowledge`（cannbot 安装器自动克隆的依赖仓，glob 取第一个匹配）；
3. 运行 knowledge-query 的 `discover`（脚本候选：`$PWD/.claude/skills/knowledge-query/scripts/knowledge_query.py`、`$PWD/.agents/skills/knowledge-query/scripts/knowledge_query.py`），取输出 JSON 的 `selected.path`。

KB 卡片加载方式：解析出 `KB_ROOT` 后，用 Read 工具直接读取 `$KB_ROOT/<卡相对路径>`（doc-id 即相对 knowledge 根的 .md 路径）。解析失败则跳过对应 KB 加载项并在输出中注明「KB 不可用，按内置约束设计」。

**类别 → 约束卡换算规则**：类别名的 `-` 替换为 `_` 后加 `_constraints.md` 后缀，目录为 `ops/triton/guides/constraints/`；例外：`activation` → `elementwise_constraints.md`，`attention-paged` → `paged_attention_constraints.md`。attention 家族先读路由卡 `ops/triton/guides/constraints/attention_writing_classification.md` 定细分 category。

### 必选知识（每次设计都加载）

- `@references/sketch-design.md` — UnifiedSketch DSL 语法规范、核心操作、设计模式、最佳实践

- **算子类别约束卡**（若存在）：`$KB_ROOT/ops/triton/guides/constraints/{category}_constraints.md`（换算规则见上）。该卡包含经过验证的 **Layer 1 设计约束**（硬性规则，必须遵守）和 **Layer 2 算法骨架**（可参考的架构方向）。设计前必须读取并理解。若草图架构与 Layer 1 任何一条冲突，必须重新设计草图，**不得将冲突下放到代码生成阶段**。
- **硬件规格**
  详细硬件规格参考： `@../npu-arch/references/npu-arch-guide-triton.md` 和 `@../npu-arch/references/npu-hardware-params.md`

  使用 `read` 工具读取对应架构的硬件规格文件。

### 手写优化案例（根据任务选择最相关的 2 个）

根据任务描述中的算子类型，从以下案例中选择**最相关的 2 个**加载。选择依据：算子类型匹配 > 数据规模接近 > 优化模式相似。

| 类别 | 案例文件 | 核心优化 |
|------|---------|---------|
| **Elementwise** | `$KB_ROOT/ops/triton/runbooks/performance/elemwise_broadcast_2d.md` | 2D 广播：小维不切分、循环外加载 |
| | `$KB_ROOT/ops/triton/guides/constraints/case_elemwise_broadcast_3d.md` | 跨轴 3D 广播：两阶段 kernel |
| | `$KB_ROOT/ops/triton/guides/constraints/case_elemwise_cast.md` | int8→fp16：二次切分 + 用满 UB |
| | `$KB_ROOT/ops/triton/guides/constraints/case_elemwise_concat.md` | Slice+Concat 融合：精确切片 load |
| | `$KB_ROOT/ops/triton/guides/constraints/case_elemwise_zeros.md` | 小 shape：少核、减调度开销 |
| **Index** | `$KB_ROOT/ops/triton/guides/constraints/case_index_histogram.md` | 大规模索引直方图：预排序 + 二分查找 |
| | `$KB_ROOT/ops/triton/guides/constraints/case_histogram_small_bins.md` | 小 bins 直方图 / 小输出表规约：per-core local table + 二次归约 |
| | `$KB_ROOT/ops/triton/guides/constraints/case_index_put.md` | 批量 load 索引到 UB、get_element 复用 |
| **Attention / FA** | `$KB_ROOT/ops/triton/guides/constraints/flash_attention_constraints.md` | FA 主链：先答 §0.2 形态识别四问；瓶颈是 CV 跨核同步，草图必须按「压 KV 迭代数」组织（区间收缩 / `kv_lo` 不对齐 / BLOCK 开到 UB 上限 / mask constexpr 特化），Layer 1 约束为硬性边界 |
| | （KB 暂无 chunk-linear-attn-bwd 专属卡，按 `new_category` 处理） | 四·结合律重排 / chunk WY 反向：禁 1D persistent；比较链 `i_t` int32；地址 int64；`A` 转置语义。block_ptr/tile 是 L2 默认姿势 |
| **MatMul** | `$KB_ROOT/ops/triton/guides/constraints/case_matmul_swizzle2d.md` | 固定核心数 grid、Swizzle2D 块重排 |
| **Reduction** | `$KB_ROOT/ops/triton/guides/constraints/case_reduction_amax_large.md` | M≪N：reduce 轴多核 + 原子 + 二次切分 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_amax_medium.md` | 中等规模：矩阵累加再归约 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_amax_small.md` | 极小 shape：grid=1 最优 |
| | `$KB_ROOT/ops/triton/guides/constraints/case_reduction_amin_atomic.md` | 原子 amin：两种原子方案对比 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_amin_large.md` | 超大 1D：二次切分 + 重组 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_amin_medium.md` | 大 N 维 amin：矩阵 min 再轴归约 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_amin_small.md` | 1D amin：并行度平衡 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_mean_large.md` | mean 行二次切分 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_mean_medium.md` | mean reduce 第一轴：重组 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_prod_small.md` | prod：tl.reduce + 自定义 mul |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_sum_fused.md` | elemwise + sum 融合 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_sum_large.md` | 大规模 sum：重组 |
| | `$KB_ROOT/ops/triton/runbooks/performance/reduction_weighted_swiglu.md` | 3D SwiGLU backward：reshape + 行二次切分 |
| **Sort/Select** | `$KB_ROOT/ops/triton/guides/constraints/case_sort_topk.md` | TopK：tile-wise partial sort + next_pow2(2*K) 合并 |
| **Layout-transform** | `$KB_ROOT/ops/triton/guides/constraints/layout_transform_design.md` | permute/transpose/reshape-as-copy：模式特化、连续维度合并、view 短路 |
| **强制约束（Layout-transform）** | — | 草图**禁止**将单一 1D element-wise gather kernel 作为主路径；必须为常见置换模式（2D transpose、batch transpose、swap adjacent dims、reverse dims、move size-1 dims）设计独立 kernel 路径或 view 短路，且每个专用 kernel 路径在草图中必须明确使用 tile-based 连续 `tl.load`/`tl.store`，并优先合并连续维度。 |

### 按需加载的知识

| 条件                                                   | 加载文档                   |
| ------------------------------------------------------ | -------------------------- |
| 任务描述中包含 hint 标记（`@hint:`, `@range_hint` 等） | `@references/hint-mode.md` |

---

## 设计模式

1. 仔细阅读 `task_desc` 中 `Model.forward()` 的参考实现
2. 理解算子的数学逻辑和计算模式
3. 判断算子类型（elementwise / reduce / matmul / attention / 复合）
4. 根据目标硬件架构，选择合适的并行化策略和内存访问模式
5. 使用 UnifiedSketch DSL 设计算法草图

## 双 kernel 可采用判定

当算子满足以下条件时，**可采用**双 kernel 结构（stats + apply）：

**判定条件**（同时满足）：

1. 算法需要两个阶段：
   - 阶段 A：遍历数据计算统计量（reduce 操作：sum、mean、max、variance）
   - 阶段 B：用统计量对原始数据做逐元素变换
2. 两个阶段的并行粒度不同：
   - 阶段 A 的并行单位（如 per-group、per-row）
   - 阶段 B 的并行单位（如 per-channel、per-element）

**典型可采用双 kernel 的算子**：

- BatchNorm, LayerNorm, GroupNorm, InstanceNorm, RMSNorm
- Softmax, LogSoftmax

**双 kernel 的优势**（在草图中标注）：

- stats 和 apply 各自可用最优 grid 配置
- 避免单 kernel 中不同阶段的并行粒度冲突
- 每个 kernel 更简单，编译器优化更充分

**单 kernel 的适用场景**：

- 统计维度和应用维度相同（如 LayerNorm 的 per-row）
- 数据量极小，kernel 启动开销占比高
- 内存带宽极度受限，中间结果存储代价高

**草图标注要求**：
如果判定可采用双 kernel，在草图中用 `@llm_hint: dual_kernel_candidate` 标注，
并说明：

- Kernel 1 的输入/输出/并行粒度
- Kernel 2 的输入/输出/并行粒度
- 中间结果（mean/rstd）的存储方式

---

## 输出要求

**直接输出** `sketch op_name { ... }` 格式的算法草图，如果任务描述中包含 hint 标记，在草图末尾附上"设计适用范围"注释（格式见 `hint-mode.md`）。

**架构决策标注**：在 sketch 开头必须添加注释，说明核心架构选择的依据：

```python
# @architecture_decision("per-dimension-serial", reason="符合 tensor_transform_constraints 卡 L1.2/L1.4 逐维度串行约束")
# @architecture_decision("flat-single-kernel", reason="...")  # 仅当经验文件明确允许或不存在时
sketch op_name { ... }
```

**Layer 1 自检**：输出草图前，必须在思考过程中逐条核对 `{category}_constraints.md` 卡（KB）的 Layer 1 约束，确认草图架构不触发任何禁止项。若存在冲突，必须在最终草图中修正，不得输出冲突架构。

---

## 设计原则

- 设计**清晰的、可理解的**算法流程
- 遵循 **Ascend NPU** 硬件特性的最佳实践（core 级别并行、内存层次）
- 考虑**目标硬件架构**的优化机会（并行度、内存访问模式、数据对齐）
- 标注**优化点和权衡决策**（使用 `@llm_hint` 注解）
- 数值正确性优先，性能次之
- **历史经验优先**：若 `{category}_constraints.md` 卡（KB）存在，其 Layer 1 约束为**硬性规则**，草图架构必须与之兼容。若通用设计模板与 Layer 1 冲突，**必须以 Layer 1 为准**
- **禁止冲突架构**：草图中不得出现与 Layer 1 禁止项同义的抽象（如 Layer 1 禁止单 kernel 展平时，草图中不得出现 `map_output_to_input` 式的一维线性映射）

## 草图特点

算法草图应该：

- **高层抽象**: 关注算法逻辑和优化策略，而非实现细节
- **易于理解**: 便于 triton-op-coding 转换为可执行的 Triton Ascend 代码
- **包含优化提示**: 标注并行化、内存优化、循环展开等机会

## 思考要求

**重要**：思考过程中请只做框架级别的分析和决策，例如：

- 算子类型判断（elementwise / reduce / matmul 等）
- 选择什么并行策略（core 级并行、数据切分方式）
- Tile 大小选择（考虑 NPU UB 容量和对齐要求）
- 数据类型如何处理

**不要在思考过程中写出完整的草图**，完整草图只在最终输出中给出。

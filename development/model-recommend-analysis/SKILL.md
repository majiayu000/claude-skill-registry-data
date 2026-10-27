---
name: model-recommend-analysis
description: 推荐模型昇腾NPU性能分析与优化，分析瓶颈点及图结构中的相似结构，找到融合算子和pass机会；并给出优化建议。触发场景：推荐模型在昇腾NPU上性能不达标或客户推荐业务迁移到昇腾需要调优吞吐和时延。支持推荐的推理和训练场景。
---

# 推荐优化 Skill

## 1. 适用场景

- 推荐模型在昇腾NPU上性能不达标
- 需要分析MindStudio Profiler输出，定位瓶颈并给出优化建议
- 客户推荐业务迁移到昇腾，需要调优吞吐和时延
- **若提供了GE build图(pbtxt)或 PyTorch fxgraph，可识别Top相似结构，给出融合pass/融合算子优化建议**
- **若提供了自定义融合pass案例库，给出融合pass建议前，优先访问该案例库去对比，命中则直接推荐**

## 2. 核心指标

### 推理场景

推荐推理优化目标是**满足时延要求下的最大吞吐**，不是单纯的降时延。

```
单卡吞吐 = BS × 多实例并发数 × 1000 ÷ AVG(H2D耗时 + ModelExecute耗时 + D2H耗时)
```

关键约束：当客户时延预期 > 单实例迭代耗时(H2D耗时+ModelExecute耗时+D2H耗时)，才有多实例并行的空间。单实例迭代耗时单位为ms。

### 训练场景

推荐训练优化目标是**最大吞吐，即最小单步迭代耗时**。推荐训练的单步迭代由以下 6 个标准阶段组成：

```
单步迭代 = 数据预处理 + Embedding拉取 + 前向计算 + 反向计算 + 更新Embedding + 更新Dense
```
```
单卡吞吐 = BS * 1000 / 单步迭代的耗时
```
说明："单步迭代的耗时"的单位为ms。

| 阶段 | 典型操作 | 通信 | 可异步并行 |
|------|---------|------|-----------|
| **数据预处理** | 特征变换、ID 去重排序、H2D 拷贝 | 无 | 可与 Embedding 拉取异步并行 |
| **Embedding拉取** | AllToAll ID 交换、Hash、表查询、AllToAll Embed 交换 | AllToAll ×2 | 可与数据预处理异步并行；可与前向计算重叠 |
| **前向计算** | Dense 层前向（MLP/Attention/MatMul 等）、LayerNorm、激活 | 无 | 可与下一步 Embedding 拉取重叠 |
| **反向计算** | 梯度反向传播、梯度 AllReduce 同步 | AllReduce | AllReduce 应与反向计算重叠 |
| **更新Embedding** | Embedding 梯度 AllToAll、表更新 | AllToAll | 可与更新 Dense 异步并行 |
| **更新Dense** | Dense 优化器 step（SGD/Adam/Muon 等）、梯度清零 | 可能 AllGather | 可与更新 Embedding 异步并行 |

> **两对天然可异步的阶段**：
> - **数据预处理 ↔ Embedding 拉取**：二者无数据依赖，可在不同线程/stream 上并行执行
> - **更新Embedding ↔ 更新Dense**：Embedding 表更新和 Dense 参数更新互不依赖，可异步并行

训练关键指标（从 step_trace_time.csv 获取）：

| 指标 | 含义 | 优化目标 |
|------|------|----------|
| Computing | NPU 计算活跃时间 | 降低算子耗时 |
| Communication | 通信总时间（含已掩盖） | 降低通信量 |
| Communication(Not Overlapped) | **未被计算掩盖的通信时间** | **→ 0，最大化重叠** |
| Overlapped | 已被计算掩盖的通信时间 | → 越大越好 |
| Free | NPU 空闲时间 | → 0，填满空闲 |
| Stage(Wall) | 总迭代墙钟时间 | → 最小化 |

## 3. 核心WorkFlow

**输入要求：** Profiling 数据为必选输入，Dump 图为可选输入。

- **步骤1：** 识别 Profiling 类型（GE 还是 PyTorch）；识别场景（推理还是训练）
- **步骤2：** 执行 Profiling 分析脚本，计算 H2D/ModelExecute/D2H 耗时、Top 算子耗时、Top 接口耗时、是否含动态 shape 等
  - **训练场景额外分析：** 关键流程梳理（6 阶段调用链树状呈现）、aten IR 调用分析（合并树状呈现）、阶段异步与预取分析、通信未掩盖分析
- **步骤3（可选）：** 若提供了 Dump 图，执行图分析脚本，分析 Top 重复子图结构，给出融合 pass/融合算子优化建议
  - 若未提供 Dump 图，则仅基于 Profiling 分析结果给出优化建议，跳过重复子图分析
- **步骤4（可选）：** 若提供了 自定义融合pass案例库，在给出融合pass优化建议之前，优先去匹配案例库中是否有匹配的pass，若有命中，则给出 Pass 名称、使用场景和限制；
  - 若未提供 自定义融合pass案例库，则跳过该步骤
- **步骤5：** 汇总输出 Markdown 分析报告
- **步骤6：** 校验报告（数据对齐 + 优化措施可实施可验证，详见"优化建议校验规则"）
- **步骤7：** 校验通过后，删除临时文件（如 profiling_report.md 和 dump_report.md）

## 4. 优化建议校验规则

### 规则1：禁止凭记忆编写实施参数

- **禁止**直接凭记忆或经验编写环境变量名、参数值、接口签名
- Agent 必须通过**联网查询昇腾官方文档**或**参考链接**确认参数真实存在后再写入建议
- 若无法联网验证，则建议中**不得给出具体参数**，改为引导用户查阅文档

### 规则2：区分执行模式

生成实施示例前，**必须先确认当前模型的执行模式**（从 Profiling 分析结果中获取）：

| 执行模式 | 判断依据 | 适用措施 | 不适用措施 |
|---------|---------|---------|-----------|
| **图模式 (GE/TorchAir/ATC AutoFuse)** | op_statistic 含（`autofuse_`或 `autofused_` 前缀） + 有 ModelExecute | 图模式环境变量、GE/TorchAir/ATC 图编译 config、AutoFuse Pass | Eager 专用接口 |
| **图模式 (Inductor + AscendC)** | op_statistic 含（`autofuse_`或 `autofused_` 前缀） + 无 ModelExecute | Inductor 环境变量、AscendC 后端配置 | GE 专用环境变量 |
| **图模式 (GE/TorchAir)** | api_statistic 含 ModelExecute (无融合算子) | 图模式环境变量、GE/TorchAir 图编译 config | Eager 专用接口 |
| **图模式 (Inductor + Triton)** | op_statistic 含`triton_poi_fused_`/`triton_per_fused_`/`triton_unk_fused_` 前缀 | Inductor 环境变量、Triton 后端配置 | GE 专用环境变量 |
| **图模式 (Inductor + DVM)** | op_statistic 含`dvm_` 前缀 | Inductor 环境变量、DVM 后端配置 | GE 专用环境变量 |
| **图模式 (有Dump图)** | 提供了 Dump 图文件 (pbtxt / output_code.py) | 图模式环境变量、图编译 config | Eager 专用接口 |
| **非图模式 (Eager)** | 无自动融合算子、无 ModelExecute、无 Dump 图文件，且 OP Name 全部含`aclnn` 前缀 | torch.compile 转图、手动多流 (torch_npu.npu.Stream) | 图模式环境变量（MAX_RUNTIME_CORE_NUMBER 等） |
| **无法判断** | 无自动融合算子、无 ModelExecute、无 Dump 图文件，且不能确认是否 Eager | 引导用户确认执行模式后再给建议 | 不给具体环境变量或接口建议 |

> **关键约束**：
> - 有自动融合算子 → **一定是图模式**
> - 走GE/TorchAir (有 ModelExecute) → **就是图模式**
> - 有 Dump 图文件 → **基本是图模式**
> - 其他无法判断时，**直接报"无法判断"，不要瞎猜**
> - 图模式下仍可能有部分 aclnn 算子（torch.compile 未完全覆盖），不影响图模式判定
> - 图模式环境变量（如 `MAX_RUNTIME_CORE_NUMBER`、`ENABLE_DYNAMIC_SHAPE_MULTI_STREAM`）**仅对图模式生效**，Eager 模式下无效。若当前为 Eager 模式，必须先建议转为图模式（如 `torch.compile`），再建议使用图模式环境变量。

### 规则3：实施示例必须标注来源

每条包含具体参数的建议，必须标注参数来源：

```
来源类型：
  - [昇腾官方文档]：URL 链接
  - [CANN 代码仓]：gitcode 链接
  - [Skill 内置知识]：本 SKILL.md 中的优化方向章节
```

### 规则4：参考链接清单

所有优化措施涉及的官方文档链接统一维护在本文档末尾「[参考链接](#参考链接)」区域。Agent 生成建议时应优先查阅该区域，正文以 `[名称]` 方式引用，不再内联完整 URL。

### 规则5：不可验证时的降级策略

当 Agent 无法联网验证某个参数时，按以下降级策略处理：

1. **降级为方向性建议**：不给具体参数，改为"建议查阅 [文档链接] 获取最新的环境变量配置"
2. **标注未验证**：在建议后标注 `(参数需查阅官方文档确认)`
3. **禁止臆造**：绝对不可编造环境变量名或参数值

### 规则6：若提供自定义融合pass案例库，融合类建议优先基于自定义融合pass案例库查验

报告中需要提供算子融合Pass的建议时，优先核对 自定义融合pass案例库 中是否有匹配的案例：

1. **匹配**：列出命中的 Pass 名称、使用场景和限制；
2. **排除**：列出已排查但不匹配的 Pass 名称及排除原因（约束不满足的具体条款）

> 访问方式：webfetch 链接页（若内容不全则 `git clone --depth 1` 后逐个查看 Pass 的 README.md 融合模式与算子约束）

## 5. 输入文件格式

MindStudio Profiler 输出目录，脚本自动识别以下文件名：

| 数据类型 | 文件名模式 | 适用场景 |
|---------|---------|---------|
| 算子耗时 | `*op_summary_*.csv` 或 `kernel_details.csv` | 推理 + 训练 |
| 算子汇总 | `*op_statistic_*.csv` | 推理 + 训练 |
| Host API | `*api_statistic_*.csv` 或 `api_statistic.csv` | 推理 + 训练 |
| 迭代耗时 | `step_trace_*.csv` 或 `step_trace_time.csv` | 推理 + 训练 |
| Trace 汇总 | `msprof_*.json` 或 `trace_view.json` | 推理 + 训练 |
| 通信耗时 | `communication.json` | **仅训练** |
| 通信矩阵 | `communication_matrix.json` | **仅训练** |
| 任务时间线 | `task_time.csv` | **仅训练** |

> **多文件选择**：当目录下有多个 `*op_summary*.csv`（如含 `_no_op_name`、`_output_` 后缀），脚本自动评分选取含 `Op Name` 列且数据非空的最优文件。

图结构分析输入文件（脚本自动识别格式：`.pbtxt` 走纯文本解析，`.py` 走 AST 解析）：

| 图源 | 文件格式 | 识别方式 | 解析方法 |
|------|---------|---------|---------|
| GE Build图 | `*.pbtxt` | 扩展名 + 内容关键词(`ir_version`/`graph {`) | 纯文本解析，提取 `node { name, op_type, input, output, shape, dtype }` |
| PyTorch fx图 | `*output_code*.py` 或 `*_runnable.py` | 扩展名 + 内容关键词(`class Repro`/`torch.ops`/`def call`) | AST 解析，提取 `torch.ops.<ns>.<op>.<overload>(...)` 调用 |

> **多个图文件选择**：当前目录下有多个 `*.pbtxt`，自动优选含 `_Build` 的文件；优选 `*output_code*.py` 文件。如果 `_Build.pbtxt` 文件有多个，则多个文件都需要分析。

## 6. 脚本说明

| 脚本 | 功能 | 输入 | 输出 | 对应报告章节 |
|------|------|------|------|------------|
| `scripts/profiling_parser.py` | Profiling 性能数据解析 | MindStudio Profiler 输出目录 | Markdown 报告 | 核心指标、算子分布、Top 算子、问题算子、Host 开销 |
| `scripts/graph_analyzer.py` | 图结构分析（支持 pbtxt 和 fxgraph） | 图文件 + Profiling 目录（可选） | Markdown 报告 | 图分析报告（可选） |

### Profiling 分析

```bash
python scripts/profiling_parser.py <profiling_dir> -o profiling_report.md
```

### 图结构分析（可选）

脚本自动识别文件格式：`.pbtxt` 走纯文本解析，`.py` 走 AST 解析，无需手动指定。

```bash
# 结合 Profiling 分析（按总耗时排序）
python scripts/graph_analyzer.py <graph_file> --profiling-dir <profiling_dir> -o dump_report.md

# 仅分析图结构（无 Profiling 时，按算子数×重复次数排序）
python scripts/graph_analyzer.py <graph_file> -o dump_report.md
```

#### 重复子图分析逻辑

- **子图比较**：使用算子类型（op_type）序列做 n-gram 比较。GE 图去掉 `ge:` 前缀；fxgraph 的 `op_type` 去掉 overload 后缀（`aten.mul.Tensor`→`aten.mul`），`raw_op_type` 保留全名用于展示
- **子图输出**：每个重复子图实例输出完整算子名、OP Type、Input/Output Shape、Input/Output Dtype（pbtxt）或输入参数/源码行号/原始调用代码（fxgraph）
- **排序策略**：有 Profiling 按总耗时（avg_instance_time × repeat_count）降序；无 Profiling 按算子数×重复次数降序
- **去重策略**：同长度模式按 op_type 组成签名去重 + 跨长度模式按实例位置覆盖去重

#### Profiling 与图节点耗时匹配策略

| 优先级 | 策略 | 说明 | 适用场景 |
|--------|------|------|---------|
| 1 | 算子名精确匹配 | Profiling OP Name == 图节点名 | pbtxt + fxgraph |
| 2 | 算子名模糊匹配 | 包含关系 | pbtxt + fxgraph |
| 3 | aclnn 前缀匹配 | Profiling 中 `aclnn{算子名}` → 图节点名 | fxgraph（aten IR → aclnn 对应） |
| 4 | 算子类型匹配 | op_type 平均耗时 | pbtxt + fxgraph |
| 5 | 前后算子名关联 | 用图节点的 producer/consumer 名在 Profiling 中搜索 | pbtxt + fxgraph |
| 6 | shape 匹配 | 用输入 shape 签名匹配 | pbtxt |

#### 优化建议生成原则

1. **重复子图融合建议**：基于 Top 10 重复子图，按重复次数和总耗时生成
2. **已有融合分析**：检测 `*op_statistic*.csv` 中 OP Type 是否含 `autofuse_`、`autofused_`、`triton_per`、`triton_poi`、`triton_unk_fused`、`dvm_` 前缀

## 7. 分析方法

### 7.1 场景识别（推理 vs 训练）

**唯一判断依据：是否存在反向/梯度相关算子**——训练场景必然含反向传播，推理场景不含。

| 判断依据 | 训练场景 | 推理场景 |
|----------|---------|---------|
| **反向/梯度算子** | op_statistic / op_summary 含 `*Backward*`、`*Grad*`、`EmbeddingDenseGrad*` 等反向算子；trace_view.json 含 `backward`/`autograd`/`loss.backward` 事件 | 无任何反向算子 |

### 7.2 共用分析方法（推理 + 训练）

#### H2D 耗时计算

- 方法1：直接从 api_statistic*.csv 中 `InputCopy` 统计；或者 msprof_*.json 中 InputCopy
- 方法2：如果方法1解析不到，通过 msprof_*.json 分析统计 memcpy 函数耗时来计算

> 1、优先使用方法1；2、方法2需结合迭代次数计算单迭代 H2D 耗时；3、H2D 是一次迭代中 ModelExecute 前面的 memcpy 总耗时，包括多次函数调用的间隙

#### D2H 耗时计算

- 方法1：直接从 api_statistic*.csv 中 `OutputCopy` 统计；或者 msprof_*.json 中 OutputCopy
- 方法2：如果方法1解析不到，通过 msprof_*.json 分析统计 memcpy 函数耗时来计算

> 1、优先使用方法1；2、方法2需结合迭代次数计算单迭代 D2H 耗时；3、D2H 是一次迭代中 ModelExecute 后面的 memcpy 总耗时

#### 迭代耗时计算

- `step_trace_*.csv` 或 `step_trace_time.csv` 中的 "Iteration Time(us)" 值求和再除以数量得到迭代耗时；或者 `api_statistic_*.csv` 中 API Name="ModelExecute" 行对应的 Avg(us)
- Ascend Profiler 的 `step_trace_time.csv` 无 "Iteration Time(us)" 列，使用 "Computing" 列作为 NPU 活跃耗时。**注意：不要用 "Stage" 列作为迭代耗时，Stage 包含 Free(空闲)时间，会导致算子耗时占比严重失真**
- `op_statistic_*.csv` 的 "Total Time(us)" 求和再除以迭代次数得到算子耗时和

#### 首次编译迭代排除

当迭代次数 > 1 时，脚本自动检测首次迭代是否含编译耗时：
- **判断条件**：首次迭代耗时 > 后续迭代平均耗时的 **5x**
- **触发动作**：将首次迭代单独标为"首次编译迭代耗时"，不参与平均值计算
- **报告呈现**：核心指标汇总表新增一行"首次编译迭代耗时"，数据来源标注"已排除，不计入平均值"
- **不影响场景**：首次迭代耗时未达 5x 阈值时，正常计算全部迭代的平均值

#### 迭代次数推断（无 step_trace 时的回退策略）

当 step_trace 中有"Stage"和"Computing"列时（step_trace_time.csv格式），脚本逐行收集 Computing 值作为迭代NPU活跃耗时（每行一次迭代），迭代次数 = 行数。当 `step_trace` 和 `api_statistic` 均不可用时，脚本从 `op_summary`/`kernel_details` 推断迭代次数，优先级：

| 优先级 | 策略                     | 说明                                                         |
| ------ | ------------------------ | ------------------------------------------------------------ |
| 1      | api_statistic sync count | aclrtSynchronizeStream/Device 的 Count 值                    |
| 2      | Infer ID 唯一值数        | op_summary 含`Infer ID` 列，唯一值数 = 迭代次数            |
| 3      | Step Id 唯一值数         | kernel_details 含`Step Id` 列，唯一值数 = 迭代次数         |
| 4      | Op Name 众数出现次数     | GE Profiling: 非aclnn算子名在单次迭代中唯一，众数 = 迭代次数 |

> **注意**：kernel_details `Name` 和 op_summary `OP Type` 不能用于推断迭代数，因为这些实体在单次迭代内出现多次（如 MatMulV2 每迭代 101 个），众数 ≠ 迭代次数。
> 若迭代次数推断为0但有算子耗时数据，脚本自动设为1次迭代并用算子耗时和估算 `iter_avg`。

#### 动态 shape 判断

- 根据 op_summary*.csv 中的 "OP State" 有 dynamic 标记，就表示有动态 shape
- 根据 msprof_*.json 中有ModelExecute，且有 infershape函数或者aclnn接口调用，就表示有动态shape

#### Top 算子耗时分析

从 `op_statistic.csv` 和 `kernel_details.csv` 分析：
- Top 20 耗时算子（按 Total Time 降序，含 Count、Avg、Max、Ratio）
- 按核类型分布（AI_CORE/AI_VECTOR_CORE/MIX_AIV/AI_CPU）
- 训练场景额外关注：EmbeddingDenseGrad（Embedding梯度）、Sort/Unique（ID去重）、HcclLaunchAicpuKernel（通信）、自定义算子 等

#### Host 侧接口调用分析（aten IR / TF IR）

分析 Host 侧接口调用，识别调度开销和同步瓶颈：

**PyTorch 场景（aten IR）**：
- 从 `trace_view.json` 的 `cat=cpu_op` 事件按 `name` 聚合，统计总耗时、调用次数、平均、最大
- 从 `api_statistic.csv` 的 `Level=host` 行按 `API Name` 聚合
- 重点关注：`aten::copy_`、`aten::to`、`aten::_to_copy`（dtype 转换/设备拷贝）、`aclrtSynchronizeStream`（流同步）、`launch`（算子下发）

**GE/TFA 场景（TF IR）**：
- 从 `api_statistic.csv` 按 `API Name` 聚合
- 重点关注：`ModelExecute`、`aclrtSynchronizeStream`、`aclrtMemcpy` 等

**关键判断**：
- `aten::copy_` / `aten::to` 调用次数多（>500/步）或总耗时占比大 → 存在过多 dtype 转换或设备拷贝
- `aclrtSynchronizeStream` 调用次数 > 10 或总耗时 > 100ms → 频繁流同步阻塞计算流
- `launch` 调用次数多但单次耗时短 → 调度开销大，需考虑算子融合或图模式

### 7.3 训练特有分析方法

以下分析方法仅适用于训练场景，推理场景跳过。

#### 关键流程梳理

从 `trace_view.json` 中提取单步训练的完整调用链，按 6 阶段归类：

1. **找到 ProfilerStep 事件**：在 `traceEvents` 中查找 `name` 含 `ProfilerStep` 且 `ph=X` 的事件，获取单步总耗时
2. **提取主线程事件序列**：筛选主进程、主线程上 `ts` 在 ProfilerStep 范围内的所有 `ph=X` 事件，按时间排序
3. **将事件归入 6 个标准阶段**（不同框架的事件名不同，按语义归类）：

| 阶段 | 典型事件关键词（按语义匹配） | 阶段产物 |
|------|---------------------------|---------|
| 数据预处理 | `feature_transform`/`data`/`preprocess`/`collate`/`input_copy` | 特征 Tensor 准备到 Device |
| Embedding拉取 | `all2all`/`embedding`/`lookup`/`hash`/`find`/`prepare`/`relocate` | Embedding 向量就绪 |
| 前向计算 | `forward`/`matmul`/`linear`/`attention`/`layernorm`/`activation`/`loss` | Loss 值 |
| 反向计算 | `backward`/`grad`/`autograd`/`all_reduce`/`reducer` | 梯度就绪 |
| 更新Embedding | `embedding_backward`/`upsert`/`all2all_grad`/`table_update` | Embedding 表更新 |
| 更新Dense | `optimizer`/`step`/`adam`/`sgd`/`muon`/`zero_grad` | Dense 参数更新 |

4. **输出调用流程树**：按时间排序，标注各阶段耗时和占单步比例，识别阻塞点

#### aten IR 树状调用分析

在共用方法"Host 侧接口调用分析"基础上，训练场景需额外以**树状结构**呈现 aten IR 调用：

**树状呈现要求**：
- 根节点为 `ProfilerStep#N (总耗时)`
- 一级子节点为各顶层 IR 事件（如 `pipeline.backward`、`pipeline.forward`、`aten::to` 等），按总耗时降序
- 有嵌套关系的事件作为父节点的子项缩进
- 每行标注：总耗时、调用次数、最大单次耗时（如有显著值）、所属 6 阶段
- ★ 标注瓶颈点（耗时显著大或触发同步阻塞的项）
- **不分阶段拆分**，所有 IR 合并在一起按总耗时排序

#### 阶段异步与预取分析

检测核心指标中描述的两对异步阶段是否已异步化，以及是否有跨步预取：

**分析方法**：

1. **检测是否有 Pipeline 预取**：在 trace_view.json 中搜索 `prefetch`/`pipeline`/`precompute`/`prepare`/`next_step` 等关键词
   - 有预取事件 → 继续分析预取效果
   - **无预取事件 → 核心优化建议：增加数据预取能力**
2. **检测数据预处理与 Embedding 拉取是否异步**：检查二者事件的时间戳
   - 时间重叠（ts 交错）→ 已异步
   - **串行（一个结束后另一个才开始）→ 优化建议：将二者异步化**
3. **检测更新 Embedding 与更新 Dense 是否异步**：检查二者事件的时间戳
   - 时间重叠 → 已异步
   - **串行 → 优化建议：将二者异步化**
4. **分析预取等待耗时**：
   - 找到 `wait`/`result` 类事件（如 `wait_all2all`、`prefetch.result`、`wait_prepare`、`future.result` 等）
   - 如果等待耗时 > 50ms 或占单步 > 5% → 预取未有效掩盖通信

#### 通信未掩盖分析

推荐训练的通信分布在 Embedding拉取（AllToAll）、反向计算（AllReduce）、更新Embedding（AllToAll）三个阶段。

**Step 1：获取 Overlap 分解**（从 `step_trace_time.csv`）：

| 指标 | 含义 | 问题判断 |
|------|------|----------|
| Communication(Not Overlapped) | 未被计算掩盖的通信 | > 通信总量的 30% → 通信未有效掩盖 |
| Overlapped | 已掩盖的通信 | 越大越好 |
| Free | NPU 空闲 | > 5% → 有空闲可填 |

**Step 2：定位未掩盖时段**（从 `trace_view.json` Overlap Analysis 进程）：
- 找到含 `Computing`/`Communication`/`Communication(Not Overlapped)`/`Free` track 的进程
- 按 `Communication(Not Overlapped)` 单次耗时降序，取 Top 10 时段
- 将时段 `ts` 与关键流程的 6 阶段对齐：
  - Embedding拉取阶段 AllToAll 未掩盖 → 前向计算未与 AllToAll 重叠，需预取优化
  - 反向计算 AllReduce 未掩盖 → 反向计算未与 AllReduce 重叠，需异步化或增大计算量
  - 更新Embedding 阶段 AllToAll 未掩盖 → Dense 更新未与 Embedding AllToAll 重叠

**Step 3：分析通信操作明细**（从 `communication.json`）：

| 字段 | 含义 | 问题判断 |
|------|------|----------|
| Transit Time(ms) | 实际数据传输时间 | = 0 → 通信完全被同步等待阻塞 |
| Wait Time(ms) | 等待时间 | ≈ Elapse Time → 通信是同步瓶颈 |
| Wait Time Ratio | 等待占比 | ≈ 100% → rank 间到达不平衡或调度瓶颈 |

**Step 4：分析同步等待来源**（从 `trace_view.json` 设备侧事件和 `api_statistic.csv`）：
- `Notify_Wait`/`DAVID_EVENT_WAIT`/`aclrtSynchronizeStream` 的总耗时和次数
- 按时间对齐到 6 阶段，确定同步发生的位置

## 8. 优化方向

优化方向分**通用优化**（推理 + 训练均适用）、**推理特有优化**和**训练额外优化**（仅训练场景）。推理场景使用通用优化 + 推理特有优化；训练场景使用通用优化 + 训练额外优化。
### 8.1 通用优化（推理 + 训练）

#### H2D和D2H优化

- 措施1：批量H2D/D2H。适用场景："多次H2D，调用间隙大"。预期收益：减少多次拷贝带来的传输头开销。**约束：需修改业务侧代码，将多次 aclrtMemcpy 合并为 aclrtMemcpyBatch；图模式下可通过 GE 的 Data 算子合并输入**
- 措施2：Pinned内存。适用场景："每次H2D都做虚实地址转化"。预期收益：大幅提升H2D效率。**约束：PyTorch 场景通过 torch_npu.npu.PinMemPoolManager 或 aclrtMallocHost 分配 Pinned 内存；非通用环境变量，需代码改造**
- 措施3：Embedding层优化，减少Input大小。适用场景："同一个特征，重复传输，比如用户行为序列"。预期收益：减少Input数据量。**约束：需业务侧代码改造，合并重复特征的 H2D 传输**
- 措施4：异步H2D。适用场景："H2D占比大，比如10%+，且多次H2D"。预期收益：部分H2D和计算overlap。**约束：PyTorch 场景通过 torch_npu.npu.Stream 创建独立 stream 异步拷贝；GE 图模式通过多 Data 算子 + Stream 并行，参数为"ge.compile.h2dOverlappedWithCompute=1"；需确保数据依赖正确**

#### NN计算优化

- 措施1：算子自动融合。适用场景：vector占比大，算子数多，算子平均耗时短。预期收益：减少MTE搬运，减少调度次数。**约束：GE/ATC 图模式通过 `export AUTOFUSE_FLAGS="--enable_autofuse=true"` 开启；`--autofuse_enable_pass` 的可用值必须以 AutoFuse 官方文档为准（常见值：`reduce`、`concat`、`matmul`、`split`、`gather`、`transpose`、`scatter`、`slice`，910系列只支持reduce/concat，950系列往后支持所有参数值），**严禁臆造 pass 名**；PyTorch 场景通过 `torch.compile(model)` 开启 Inductor 编译，并通过环境变量 `export TORCHINDUCTOR_NPU_BACKEND=ascendc` 选择高性能 AscendC 后端（必须在 `torch.compile()` 调用之前设置）；其他可选后端：`default`（Triton 模式）、`mlir`、`dvm`；Eager 模式无法直接开启，需先转图模式；训练场景反向算子也会自动融合；参考：[AutoFuse]、[TORCHINDUCTOR_NPU_BACKEND]**
- 措施2：手写融合算子和Pass。适用场景：重复结构且耗时较大。预期收益：需要实测。**约束：GE 图模式通过自定义 Pass 注册（GE REGISTER_PASS）；AscendC 算子通过 Ascend C API 开发融合算子；需 CANN 算子开发能力。参考：[图Pass开发]。生成此措施建议前，先确认是否存在可选输入 自定义融合pass案例库 ，若存在优先逐一核对（逐个 Pass 比对其 README 中的融合模式与本例图结构/算子序列，含约束条件如 shape 维度、dtype、静态/动态），命中则直接推荐现成 Pass（含构建部署步骤），未命中才走自行开发路径；核对结论（匹配/排除及原因）必须写入报告**
- 措施3：单算子tiling key优化。适用场景：op_summary*.csv中的算子的aic_scalar_ratio 或 aiv_scalar_ratio 占比超过30%。预期收益：算子性能提升，显著降低scalar耗时占比。**约束：需联系算子开发团队修改 tiling 策略，非用户侧可配置；可通过 AscendC 修改算子的 tiling key 选择逻辑**
- 措施4：静态图下沉。适用场景：动态shape可有限分档或shape不变场景。预期收益：需要实测，提升会很大。**约束：GE 图模式通过 `ge.exec.dynamicImageSize` 或 `--dynamic_dims` (ATC) 配置分档；PyTorch 通过 `torch.compile(model, dynamic=False)` 转静态图；需确认 shape 确实可分档或固定**
- 措施5：多线程并行调度。适用场景：动态图执行场景。预期收益：减少host调度开销。**约束：环境变量 `export MAX_RUNTIME_CORE_NUMBER=3` 仅对图模式生效；TorchNPU，通过TASK_QUEUE_ENABLE=1，开启流水调度；配置后需配合绑核使用。参考：[多线程调度]**
- 措施6：调度线程绑核。适用场景：ARM CPU 动态调度耗时高场景。预期收益：~10%+，减少线程跨核切换。**约束：通过环境变量 `CPU_AFFINITY_CONF=<mode>,npu<id>:<start>-<end>` 配置 Host 侧 CPU 核绑定，mode=1 粗粒度/mode=2 细粒度，推荐细粒度；这是 CPU 侧绑核，与 AICore 控核（ge.aicoreNum）是不同的措施；图模式多线程调度时需配合在首次迭代前绑核。参考：[torch_npu绑核]**
- 措施7：混合调度。适用场景：动态图热点shape可静态分档，其他还走动态图执行场景。预期收益：减少host调度耗时。**约束：PyTorch 通过 torch.compile 配合 dynamic shape 分档实现；GE 图模式通过ge.compileHybridMode或tfa参数compile_hybrid_mode设置；需确认热点 shape 可枚举**
- 措施8：AICPU算子转Aicore。适用场景：AICPU算子，且对应有等价Aicore可以替换。预期收益：显著提升算子性能，对应算子性能提升~50%。**约束：需 CANN 算子开发团队用 AscendC 重写 AICPU 算子为 AICore 实现；非用户侧可配置；通过 op_summary 中 Task Type=AI_CPU 识别目标算子**
- 措施9：静态图多流并行。适用场景：单实例场景，时延已超出业务阈值，但NPU使用率低，带宽使用率低。预期收益：CV并行，预期有5%左右收益；自动多流并行，预期有30%左右收益。**约束：图模式通过 `ge.autoMultistreamParallelMode` 开启，参考：[GE options]；Eager 模式需用 torch_npu.npu.Stream 手动多流或先转图模式。**

**Profiling判断:**

- `aic_scalar_ratio >= 30% or aiv_scalar_ratio >=30%` → tiling key 选择问题，联系算子开发优化
- `cube_utilization < 20%` → shape 太小，需要增大BS
- `aic_mac_ratio < 30%` → 计算不是瓶颈，需考虑融合
- Iteration算子耗时和 / Iteration耗时 < 90% → 调度bound
- `Task Type = AI_CPU` → 即为AICPU算子

### 8.2 推理特有优化

以下优化方向仅适用于推理场景，训练不适用。

#### 多实例并行

- 措施1：多实例并行。适用场景：时延预算 > 单迭代耗时，且单实例下，NPU使用率低。预期收益：~2x吞吐提升，实际需实测。**约束：通过多线程创建多个推理实例实现；每个实例需独立的 Device 资源或通过时间片轮转共享；需确保显存容量充足。参考：[推荐推理最佳实践]**
- 措施2：AICore 控核。适用场景：在多实例并行下，需要配置算子编译时使用的 AICore 核数，防止实例之间抢占 AICore 资源激烈，导致 device 调度变长。预期收益：~20%，需实测，主要收益来自避免 AICore 资源竞争。**约束：GE 图模式通过 GE 图编译参数 `ge.aicoreNum` 配置（如 "8|8" 表示两个实例各分配 8 核 AICore）；PyTorch 场景当前通过 `torch_npu.npu.set_device_limit()` 和 `torch_npu.npu.set_stream_limit()` 接口实现控核，未来计划支持环境变量 `NPU_DEVICE_LIMIT`。参考：[GE options]、[推荐推理最佳实践]、[PyTorch环境变量]**

### 8.3 训练额外优化

以下优化方向在通用优化基础上，仅适用于训练场景。训练优化以**阶段异步化和通信异步化**为核心，辅以算子优化（HF32、融合、混合精度）。

#### 训练阶段异步与预取优化

**Profiling 判断：**
> - 数据预处理与 Embedding 拉取事件时间戳串行（无重叠）→ **二者需异步化**
> - 更新 Embedding 与更新 Dense 事件时间戳串行（无重叠）→ **二者需异步化**
> - trace_view.json 中无 `prefetch`/`pipeline` 相关事件 → **无跨步预取，需增加预取能力**
> - 存在 `wait`/`result` 等等待事件且耗时 > 50ms → 预取未有效掩盖通信
> - `Free` > 5% → NPU 有空闲可被预取填充

**优化措施：**
- 措施1：数据预处理与 Embedding 拉取异步化。适用场景："二者串行执行"。预期收益：合并耗时从串行相加变为取 max，预期降低 10%~20% 单步耗时。**约束：将二者分别放在独立线程或 stream 上并行执行；二者无数据依赖，可安全并行；需确保线程安全**
- 措施2：更新 Embedding 与更新 Dense 异步化。适用场景："二者串行执行"。预期收益：预期降低 5%~15% 单步耗时。**约束：将二者分别放在独立线程或 stream 上并行执行；二者操作不同参数表，无数据依赖；需确保梯度在异步更新前已全部就绪**
- 措施3：增加跨步数据预取。适用场景："训练框架无 Pipeline 预取"。预期收益：下一步数据预处理 + Embedding 拉取与当前步前向计算重叠，预期降低 15%~30% 单步耗时。**约束：在训练框架中实现 Pipeline 预取机制，提前在独立线程/stream 上发起下一步的数据预处理 + Embedding AllToAll；需确保预取数据与实际使用数据一致**
- 措施4：增大预取深度。适用场景："已有预取但 depth=1 或 2，预取等待阻塞 > 50ms"。预期收益：增加通信掩盖窗口。**约束：将预取深度增大到 2~3 步；增加显存占用，需确认显存余量；过大深度会增加梯度延迟**
- 措施5：优化预取等待时机。适用场景："预取等待阻塞了前向/反向计算"。预期收益：预期降低 10%~15% 单步耗时。**约束：将预取 Future/Event 的等待时机推迟到真正依赖预取结果的计算之前；需确保通信顺序正确性不变**

#### 训练通信异步化优化

**Profiling 判断：**
> - `Communication(Not Overlapped) / Communication > 30%` → 通信未有效掩盖，需异步化
> - `Communication Transit Time = 0` 且 `Wait Time Ratio ≈ 100%` → 通信是同步/调度瓶颈，非带宽瓶颈
> - `aclrtSynchronizeStream` Count > 10 或 Time > 100ms → 频繁流同步阻塞计算流
> - `DAVID_EVENT_WAIT` / `Notify_Wait` 总耗时 > 计算耗时 10% → 设备侧同步等待过多

**优化措施：**
- 措施1：通信操作异步化。适用场景："AllToAll/AllReduce 使用同步调用（无 async_op）"。预期收益：通信与计算重叠。**约束：将集合通信调用设置为异步模式（PyTorch 场景设置 `async_op=True`，返回 work 对象后延迟 wait）；需确保在真正依赖通信结果时才 wait**
- 措施2：通信后端优化。适用场景："Embedding AllToAll 的 size 交换使用 CPU 后端（gloo），Transit=0 且 Wait=100%"。预期收益：消除 D2H→CPU→H2D 中转。**约束：将 size 交换从 CPU 后端改为 NPU 通信后端（如 hccl）；需确保后续 CPU 操作不影响异步性；仅适用于 PyTorch + HCCL 训练框架**
- 措施3：减少流同步调用。适用场景："aclrtSynchronizeStream 调用频繁（>10次）"。预期收益：减少计算流阻塞。**约束：将训练框架中的显式 stream sync 替换为 event-based 异步等待（`aclrtRecordEvent` + `aclrtStreamWaitEvent`）；自定义算子 C++ 实现中的同步也需修改；参考 [AscendCL Event API]**
- 措施4：Dense 梯度同步优化。适用场景："反向计算阶段 AllReduce 未被掩盖，aten::copy_ 调用多（>500/步）"。预期收益：减少梯度同步中的额外 copy_ 开销。**约束：PyTorch DDP 构造时设置 `gradient_as_bucket_view=True` + `static_graph=True`；自定义 comm_hook 中避免不必要的 dtype 转换和 copy_；参考 [PyTorch DDP]**
- 措施5：Rank 间负载均衡。适用场景："各 rank step 时间差异 > 10%，或通信 Wait Time Ratio ≈ 100%"。预期收益：减少 collective 等待。**约束：确保各 rank 的 batch size 和数据量一致；检查 Dataset/Sampler 是否按 `rank/world_size` 正确切分**
- 措施6：Task Queue 异步调度。适用场景："算子提交为同步模式，设备侧同步等待多"。预期收益：算子异步提交，减少同步等待。**约束：开启 Task Queue 异步调度 `TASK_QUEUE_ENABLE=1`；关闭直调算子同步 `NPU_OPS_SYNC=0`；需验证稳定性；参考 [TASK_QUEUE_ENABLE]**

#### 训练算子优化

**Profiling 判断：**
> - Top 算子中 vector 算子数多且平均耗时短 → 需算子融合
> - `aten::to` / `aten::copy_` 调用多（>500/步） → dtype 转换开销大，需优化混合精度策略
> - MatMul/BatchMatMul 耗时占比大且未开启 HF32 → 可通过 HF32 降低计算精度开销
> - EmbeddingDenseGrad / Sort / Unique 耗时占比 > 5% → Embedding 相关算子需优化
> - 自定义算子内部含 `aclrtSynchronizeStream` 或 `DAVID_EVENT_WAIT` → 算子内部同步阻塞

**优化措施：**
- 措施1：开启 HF32。适用场景："MatMul/BatchMatMul 耗时占比大，且未开启 HF32"。预期收益：预期 5%~10% MatMul 性能提升。**约束：PyTorch 场景通过 `torch.npu.matmul.allow_hf32=True` + `torch.npu.conv.allow_hf32=True` 开启；GE 图模式通过 `--precision_mode=allow_hf32` 开启；需做精度 A/B 验证**
- 措施2：混合精度计算。适用场景："前向计算全用 FP32，aten::to/copy_ 多但非用于通信而是用于计算精度切换"。预期收益：降低计算量和显存占用。**约束：PyTorch 场景通过 `torch.autocast('npu', dtype=torch.bfloat16)` 或 mixed_precision 配置开启；GE 图模式通过 `--precision_mode=allow_mix_precision` 开启；需做精度 A/B 验证 loss 曲线一致**
- 措施3：混合精度策略优化。适用场景："已开启混合精度但 autocast rules 切换频繁，aten::to 调用多"。预期收益：减少 dtype 转换开销和同步阻塞。**约束：合并相同 dtype 的 autocast rules，减少切换次数；反向梯度通信 dtype 可设为 null（用 FP32）避免反向同步；需做精度 A/B 验证**
- 措施4：自定义算子同步消除。适用场景："业务自定义算子内部含 aclrtSynchronizeStream 或 DAVID_EVENT_WAIT"。预期收益：消除算子内部同步阻塞。**约束：修改自定义算子 C++ 实现，将 `aclrtSynchronizeStream()` 替换为 `aclrtRecordEvent` + `aclrtStreamWaitEvent` 异步等待；需 CANN 算子开发能力；参考 [AscendCL Event API]**
- 措施4：增大BatchSize（BS）。使用场景："Mamtul/BatchMatMul/FA等算子的cube_utilization 太小的场景"。预期收益：提升Cube利用率，发挥NPU优势。***约束：训练场景BS变大，需要调整学习率，需要报告中提醒；如果有BatchNorm类的算子，还需要确认精度是否正常*

## 9. 输出报告格式

- 文件格式：Markdown。需要保障在各 Markdown 渲染器中都能正常显示
- 输出路径：report 目录，如果无 report 目录，则创建；如无权限，则走 Agent 默认处理策略

### 共用报告（推理 + 训练）

1. Profiling 文件发现
2. 核心指标汇总表（H2D/ModelExecute/D2H 耗时及占比；含是否含动态 shape、是否开启自动融合；若首次迭代含编译耗时则单独列出"首次编译迭代耗时"行）
3. 算子类型分布表（含耗时占比）
4. Top 20 耗时算子表（含 shape、dtype、aic/aiv 占比、mte 占比；按算子类型+shape+dtype 去重）
5. 问题算子汇总表（按 问题类型+OpName+OpType+TaskType+InputShapes+OutputShapes 聚合去重，Top 50 按总耗时降序）
6. Host 耗时分析表（Host API 耗时 Top 15）

### 训练额外报告

1. 关键流程调用树（数据预处理/Embedding拉取/前向计算/反向计算/更新Embedding/更新Dense 六阶段耗时及占比，标注阻塞点和阶段间异步状态）
2. aten IR 调用分析（不分阶段，合并按总耗时排序，树状结构呈现，含调用次数、平均、最大，★标注瓶颈点，行尾标注所属 6 阶段）
3. 阶段异步与预取分析（数据预处理↔Embedding拉取是否异步、更新Embedding↔更新Dense是否异步、是否有跨步预取、预取深度、预取等待耗时）
4. 通信未掩盖分析（Computing/Communication/Not Overlapped/Free 分解表 + Top 10 未掩盖时段定位到 6 阶段 + 通信操作汇总表含 Transit/Wait/Sync + 同步等待统计）

### 图分析报告（可选，提供图文件时生成）

1. 基本信息（含图拓扑结构摘要：最大深度/宽度/分支因子/根叶节点数/环路检测）
2. 重复子图分析表（含算子名/shape/dtype）+ Top 5 子图实例详情表

### 优化建议列表

Agent 根据脚本分析出的问题，匹配"优化方向"中的适用场景，结合昇腾社区资料给出优化建议。每条建议包含：对应的问题、适用的优化措施、触发条件、预期收益、实施示例。优化建议合入最终报告的最后一章。

**重要规则：**

- 优化建议按优先级排序（高/中/低），每条建议包含：触发条件、预期收益、实施示例
- 优化建议全部基于分析结果动态生成，不硬编码特定算子对
- 优化建议需要结合昇腾社区资料，给出实施示例，如开关配置示例，调用的接口示例等
- 如果有融合算子和pass的优化措施，需要给出示例代码，可使用 cannbot 已有融合算子和图pass开发 skill 处理
- 优化措施必须真实存在，如参数、环境变量、配置、接口等必须真实存在，且使用方法正确
- 自动融合优化建议：如果没有图分析报告，也可根据 `*op_summary*.csv` 中的算子执行序给出建议；自动融合一般都支持 CV 融合（cube 算子后面接 Vector 算子，Vector->Cube 不支持）、VV 融合（vector 算子间融合）、norm 类算子融合、reduce 类一般支持前向融合；支持搬运类（gather（含 Embedding）、transpose、split/slice/strideslice、concat）、reduce 类、matmul/batchmatmul 类、eltwise 类、broadcast 类等融合。`--fusion_switch_file` 不是自动融合配置，是内置手写 pass 开关配置
- 静态 shape 图下，不能出现 CPU 绑核、多线程调度等动态图下的优化措施
- 优化措施如果已经实施，需要确认是否还有进一步优化空间；融合算子名中有 `autofuse_**_mm_**` 或 Catlass，说明已经开启了 CV 融合；其他已开启的融合能力可从自动融合算子名中推断出，一般格式为"前缀_算子类型1_算子类型2_..._算子类型N"
- 控核判断：当前算子使用的最大核数和实际最大物理核数比，如果前者小于后者则可能已做控核。算子使用最大核数计算方法：按任务类型获取算子最大使用核数（Task Type / Accelerator Core → Block Dim 或 Block Num），注意 AI_VECTOR_CORE/AI_CORE 可分别控核。无法获取芯片型号和最大核数时，控核优化措施标注为 `[可能的优化措施]`
- 优化措施需要区别是 TFA/GE/ATC、Torch inductor、torchair 等
- **训练场景优化建议必须区分推理专用措施**：训练场景不可使用多实例并行和 AICore 控核；训练优化措施涉及训练框架代码修改的，必须标注修改位置和正确性风险
- **训练场景优化建议需标注正确性风险**：涉及通信顺序调整、dtype 转换消除、混合精度变更的措施，必须标注"需做精度 A/B 验证"或"需确保通信顺序正确性不变"

## 参考链接

正文以 `[名称]` 方式引用，完整链接见下表：

| 名称 | 链接 |
|------|------|
| [AutoFuse] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/programug/graphdevg/autofuse_1_0004.html |
| [TORCHINDUCTOR_NPU_BACKEND] | https://www.hiascend.com/document/detail/zh/Pytorch/latest/apiref/ENV/docs/zh/environment_variable_reference/TORCHINDUCTOR_NPU_BACKEND.md |
| [多线程调度] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/maintenref/envvar/envref_07_0034.html |
| [动态shape多流并发] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/maintenref/envvar/envref_07_0033.html |
| [环境变量总览] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/maintenref/envvar/envref_07_0001.html |
| [推荐推理最佳实践] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/programug/graphdevg/atlasag_25_0101.html |
| [图Pass开发] | https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/latest/programug/graphdevg/docs/zh/user_guides/graph_dev/custom_pass_development/introduction.md |
| [torch_npu绑核] | https://www.hiascend.com/document/detail/zh/Pytorch/latest/apiref/ENV/docs/zh/environment_variable_reference/CPU_AFFINITY_CONF.md |
| [PyTorch环境变量] | https://www.hiascend.com/document/detail/zh/Pytorch/latest/apiref/ENV/docs/zh/environment_variable_reference/env_variable_list.md |
| [GE options] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/API/ascendgraphapi/atlasgeapi_07_0150.html |
| [CANN代码仓] | https://gitcode.com/cann |
| [Ascend代码仓] | https://gitcode.com/Ascend |
| [CANN社区] | https://www.hiascend.com/cann |
| [HCCL开发指南] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/developref/hcclapi/atlashcclapi_01_0001.html |
| [AscendCL Event API] | https://www.hiascend.com/document/detail/zh/canncommercial/latest/developref/aclapi/aclrtapi_03_0045.html |
| [PyTorch DDP] | https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html |
| [TASK_QUEUE_ENABLE] | https://www.hiascend.com/document/detail/zh/Pytorch/latest/apiref/ENV/docs/zh/environment_variable_reference/TASK_QUEUE_ENABLE.md |

---
name: ge-memory-analysis
description: GE 内存分析与优化。触发场景：① Device 显存问题——内存占用高、显存占用、HBM 偏大、OOM、内存不释放、显存持续增长、内存归因、内存池分析、devmm、imas；② 复用与寻优——内存复用率低、内存碎片、复用优化、显存优化、理论最小值、内存寻优、topo 排序、内存策略；③ Host 泄漏——host 内存泄漏、进程内存持续增长、TMT、ASan、valgrind；④ 算子地址调试——算子实际下发地址、下发地址、算子地址、input/output/workspace 地址、零拷贝地址、地址刷新、refreshable。
---

# GE 内存分析与优化

## Overview

GE 内存问题的顶层分析入口：先按场景分诊（Device 显存 / Host 泄漏 / 算子地址调试），再进入对应分析路径，最后给出归因和优化手段。

核心原则：**按场景分诊** —— ① Device（NPU/HBM）显存问题（占用高、复用差、不释放）用 devmm 统计和 imas 报告归因；② Host 内存泄漏是**通用问题**，用 TMT/ASan 等常规工具排查，方法与普通 C/C++ 程序一致；③ 算子实际下发地址调试走 addr-reference 三路径（按图类型路由）。

**参考文件**（本目录，按场景分组；细节表格/示例/机制详解均在此层，SKILL.md 只保留分诊与决策）：
- 归因/报告：[imas-report-reference.md](references/imas-report-reference.md) — imas 工具用法、devmm 组件统计字段、报告字段详解、静态/动态图判定、reach_theory_rate 根因详解、踩踏检测、实测示例
- 地址调试：[addr-reference.md](references/addr-reference.md) — 算子实际下发地址三路径（imas addr / dfx args 表 / RT2 launch 日志）+ 零拷贝/refreshable/UpdatePolicy 机制 + 2 个提取脚本
- 优化/寻优：[memory-optimization-reference.md](references/memory-optimization-reference.md) — 优化手段速查、运行时归因与常见原因、配置方法与推荐值；[memory-tuning-reference.md](references/memory-tuning-reference.md) — 完整搭建步骤、寻优脚本用法、dump 图获取、UT 环境变量、结果展示格式
- Host 泄漏：[host-leak-reference.md](references/host-leak-reference.md) — 工具选型与 TMT 使用

## 分诊流程

**入口澄清（必须先做）**：用户问算子下发地址/地址刷新/零拷贝地址 → **直接进场景 3**（无需分诊内存类型）；用户仅反馈"内存占用高/内存偏大/OOM"等未指明内存类型时，**先询问用户是 Device 显存还是 Host 内存**，再进入对应路径：

- **Device 显存**（NPU/HBM）：`npu-smi info` 可见、AI 任务相关 → 场景 1
- **Host 内存**（进程 RSS/VSZ）：`top`/`ps` 可见、进程持续增长 → 场景 2
- 用户也不确定 → 先取基线判断（见下）

**输入材料提示（按需向用户索要）**：

- **分析 Device 显存占用（场景 1 归因/复用分析）**：请用户提供运行日志 —— run 阶段 plog（devmm 组件统计，`log/run/plog/plog-*.log`）和 debug 阶段 plog（imas 解析，`log/debug/plog/plog-*.log`）；用户无日志时，按分诊树"无日志"分支开启日志开关重新运行（`ASCEND_GLOBAL_LOG_LEVEL=1`，atc 加 `--log=info`）；**拿到日志先校验内容**：run plog 须含 `svm_mem_stats_show`、debug plog 须含 `MallocMemory`（校验命令见 imas-report-reference.md 第 1 节"日志要求"），缺失（文件截断 / 日志级别不足 / 阶段不符 / 进程未正常退出）时**不得硬分析**，明确告知缺失项并提示开对应日志开关重新获取
- **需要内存寻优（1.5 节，仅静态 shape 场景）**：请用户提供 dump 图（txt 格式，需**静态 shape + 引擎分配后**阶段，如 `ge_proto_xxx_AfterAssignedLogicStreams.txt`、`ge_proto_xxx_graph_0_Build.txt`；获取方式与阶段要求见 [memory-tuning-reference.md](references/memory-tuning-reference.md) 第 2 节）；动态 shape 场景不适用（判定见 1.5 适用范围），改走 [memory-optimization-reference.md](references/memory-optimization-reference.md)

```
GE 内存/地址问题
├── Device 显存（NPU/HBM）：占用高 / 复用差 / 不释放 / 持续增长
│   ├── 第一步：run 日志 devmm 组件统计 → 定大头（GE/HCCL/RUNTIME/APP）→ 1.1
│   ├── 大头是 GE → imas total 看 GE 分类（1.2）
│   │   ├── StaticGraph 大（静态图内存）→ imas report → imas_mem_graph.csv 分析（1.3）
│   │   └── 动态内存池大（RT2.0 动态 shape 执行）→ imas report → imas_mem_pool.csv 分析（1.3；**不支持离线重放寻优**）
│   └── 无日志 / 日志缺关键内容 → 按上文"输入材料提示"校验并开日志开关重新获取
├── Host 内存：泄漏 / 持续增长（通用方法，非 GE 特有）
│   └── TMT / ASan / valgrind / core dump → 场景 2
├── 算子地址调试：算子实际下发地址 / 地址刷新 / 零拷贝地址
│   └── 按图类型路由 → 场景 3（addr-reference 三路径）
└── 不确定内存类型 → 先问用户（Device 显存 or Host 内存）→ 仍不确定 → 先取基线：devmm 统计 + npu-smi info 采样
```

## 场景 1：Device 显存（NPU/HBM）占用分析与优化

分析链路：**devmm 定组件 → imas total 看 GE 分类 → 按分类深入 imas report**（静态图内存走 imas_mem_graph.csv，动态内存池走 imas_mem_pool.csv，均可详细分析复用率/理论最小值/算子级明细）

### 1.1 组件级内存占用分析（devmm 日志，第一步）

先按组件归因，确定内存大头在哪个模块（GE/HCCL/RUNTIME/APP），再深入对应分析路径。

**日志来源：** run 阶段 plog（如 `log/run/plog/plog-*.log`），进程退出时驱动 devmm 打印统计。

**提取组件内存统计：**
```bash
grep -i 'svm_mem_stats_show' <plog文件>
```

归因主要看 `allocated_peak_size`（峰值）；退出时 `current_alloced_size=0` 且 `alloc_cnt=free_cnt` 说明驱动层面无泄漏。统计行格式、内存类型（HBM/DDR 大小页）、全部字段含义见 [imas-report-reference.md](references/imas-report-reference.md) 第 1 节"devmm 组件统计"。

**组件归因表（峰值大头 → 深入路径）：**

| 大头组件 | 深入分析 |
|---------|---------|
| GE | imas total 查看分类（1.2 节），再按分类深入 |
| HCCL | 通信 buffer 配置（如 buffer 大小 * rank 数） |
| RUNTIME | rts 内部结构，通常量小 |
| APP | 用户代码 aclrtMalloc，查应用侧 |

### 1.2 GE 内存分类（imas total）

devmm 定位到 GE 是大头后，用 `imas total` 看 GE 内部构成：

```bash
./imas total <debug日志目录>/plog/plog*
```

输出两部分：

**① 每图 summary**（格式同 imas_mem_graph.csv 末行，指标含义见 1.3）

**② 从 device 实际申请的内存分类（Malloc memory from device）**

原始输出为缩进列表（`|-GE-StaticGraph  268470272(256.03M)`），**建议整理成 markdown 表格展示**（按大小降序、GE 子项缩进、附占 Used 比，归因一目了然；整理格式示例见 [imas-report-reference.md](references/imas-report-reference.md) 第 2 节"分类展示示例"）。

（Device total 为容量，不计入占比；输出头字段含义——**StaticMemoryPolicy**（动/静态图内存复用策略，非 0 时 GE-StaticGraph 与 GE-MemoryPool 可能共享扩展区影响归因，动态 shape 内存池碎片可经其 3/4 取值缓解）等——见 [imas-report-reference.md](references/imas-report-reference.md) 第 2 节；取值说明以正式发布文档为准，不写入 skill）

**GE 分类归因**（imas total 按 rts 申请日志的用途描述自动分类，条目名即区分静态图/内存池）：

| 分类 | 含义 | 大头时深入路径 |
|------|------|--------------|
| GE-StaticGraph | 静态图内存（算子输出、feature map） | `./imas report <debug>/plog/plog*` → imas_mem_graph.csv → 1.3 分析 |
| GE-MemoryPool | **动态内存池**（RT2.0 动态 shape 执行，"page caching"/"Memory for caching"） | 同上 → **imas_mem_pool.csv**（按 allocator_id 分组，含 reuse_rate/reach_theory_rate） |
| GE-Variable | 变量/常量/权重 | https://gitcode.com/cann/ge/blob/master/docs/zh/design/features/variable_manager.md、外置权重 |
| GE-davinci_model_load | 模型加载结构（task 等） | 通常量小，多模型叠加时关注 |

交叉验证：GE 分类合计应与 devmm 统计中 GE 的 `allocated_peak_size` 量级一致；不一致说明有内存未走 imas 可见的分配路径。

### 1.3 复用报告分析（imas report）

**生成：** `./imas report <debug日志目录>/plog/plog*` → `mem_report/` 下 4 个 csv（工具准备、全部子命令、字段详解、无 debug 日志时的 AfterAssignMemory 备用路径，均见 [imas-report-reference.md](references/imas-report-reference.md)）

**报告主体判定（静态/动态 shape 图，必须先做）**：看 `imas_mem_graph.csv` 是否为空——
- **非空 → 静态 shape 图**：走本节流程，分析 `imas_mem_graph.csv`（imas total 显示 GE-StaticGraph）
- **空 → 动态 shape 图（RT2.0 执行）**：imas_mem_graph.csv 无数据（imas total 显示 GE-MemoryPool），改分析 `imas_mem_pool.csv`（address 聚合看物理占用、块粒度损耗、页占用等分析要点见 [imas-report-reference.md](references/imas-report-reference.md) 第 2 节）；**不支持 1.5 节离线重放寻优**，优化手段见 [memory-optimization-reference.md](references/memory-optimization-reference.md)

#### 分析第一步：先读最后一行 summary

**先看 imas_mem_graph.csv 最后一行的内存复用汇总（summary）** —— 不逐行翻算子明细，先从汇总指标定优化层级，再决定是否需要算子级核查。两个核心指标：**reuse rate**（低 → 拓扑/图结构问题）和 **reach_theory_rate**（<100% → 复用算法有空间），公式与全部指标含义见参考文件第 3 节。

#### 归因决策树

```
reuse rate 低？
├── 是 → 改拓扑排序算法（topo）或加控制边改图结构
│        → 目标：提升 reuse rate，降低 after_reuse
└── 否 → reach_theory_rate < 100%？
    ├── 是 → 优化复用算法 → after_reuse 逼近 theory_min
    └── 否 → 当前拓扑下已最优
```

再检查不可复用项占比：`io` / `no_reuse` / `atomic` / `streams` / `continuous`（含义见参考文件指标表）。

**reach_theory_rate < 100% 的常见根因**（after_reuse 与 theory_min 的差距来源）：连续内存整块生命周期长（最常见）、整块 best-fit 失配、io 块隔离放置、512 字节对齐膨胀、多流并行——各根因的机制、报告特征与排查方法（含水值模拟法）见 [imas-report-reference.md](references/imas-report-reference.md) 第 3 节"reach_theory_rate < 100% 常见根因与排查"；reach_theory_rate 在 90%~100% 属分配器模型精度的正常水平，非结构性浪费。

#### 算子级展示规则

需要算子级核查时，展示规则（Top 10 筛选、graph/Process 分组、列序、生命周期格式、表格格式、name 解析）见 [imas-report-reference.md](references/imas-report-reference.md) 第 4 节。

#### 内存踩踏（stomping）检测与常见踩内存问题分析

复用变化（网络结构变化/手动配置不复用）导致算子精度问题时，按五类根因排查：① 复用错误踩踏（内存报告即可分析）；② 算子多写踩踏（复用正确，看执行算子顺序和内存相邻性）；③ 算子多读脏数据（从被复用过的内存读到脏数据）；④ 算子少写（如内存 1024 实际只写 512，被复用过即残留脏数据）；⑤ VA/PA 映射冲突（**仅动态 shape + `staticMemoryPolicy` 3/4**：Va1 与 Va2 虚拟地址不重叠但绑定相同物理页 Pa，报告均为 VA 维度无法发现，须开 INFO 日志查 GE 内置 VA/PA 校验报错）。静态图实测定位嫌疑算子用 dump watch 模式：怀疑哪个算子输出内存被踩就把该算子配成 watcher，每个算子执行后 dump 一份被观察内存，谁执行后非预期变化谁就是嫌疑（复用错误和算子踩踏均适用）。根因分类、stomping 模拟检测步骤、数据级验证特征、watch 模式、不复用配置（`OP_NO_REUSE_MEM` / `ge.exec.disableReuseMemory` / `--disable_reuse_memory`）、VA/PA 映射冲突检测见参考文件第 5 节。需算子实际下发到 device 的 input/output/workspace 地址（踩踏实址核查/地址对账）时，见 [addr-reference.md](references/addr-reference.md)。

#### 分析工作流

1. 生成报告：`./imas report <debug>/plog/plog*`
2. **先读 imas_mem_graph.csv 最后一行 summary**：reuse rate + reach_theory_rate 两个指标定优化层级
3. 走归因决策树（reuse rate 低 → 拓扑/图结构；reach_theory_rate < 100% → 复用算法）
4. 检查不可复用项占比：io / no_reuse / atomic / streams / continuous
5. 需要时算子级核查（按展示规则输出 Top 10，核查 offset、生命周期重叠、isref 链）
6. 必要时做 stomping 检测
7. 优化后重新编译再生成报告对比

### 1.4 运行时占用归因与优化手段

**运行时占用归因（显存持续增长/不释放）**：`npu-smi info` 周期采样确认增长模式 → 检查 API 配对（`aclmdlLoad ↔ aclmdlUnload`、`CreateSession ↔ DestroySession`、`GEInitialize ↔ GEFinalize`）→ `imas total` 对比 GE 实际申请量区分 GE 申请 vs 驱动/RM 预留。完整步骤、Device 显存常见原因表（Session 未销毁 / VarManager 残留 / 内存池不收缩等）见 [memory-optimization-reference.md](references/memory-optimization-reference.md) 第 4 节。

**优化手段：** 配置方法、推荐值、参考文档见 [memory-optimization-reference.md](references/memory-optimization-reference.md)（本目录）。参数完整定义以对外文档为准（该文件注明同源原则）。

如需修改 GE 内存分配源码，请先阅读 GE 仓 [memory-constraints.md](https://gitcode.com/cann/ge/blob/master/docs/zh/design/constraints/memory-constraints.md)（静态复用禁改图、对齐策略、悬挂块等约束）。


### 1.5 内存寻优（dump 图离线重放，自动找最优参数组合）

> **前置条件**：本节依赖 GE 开发环境（ge 仓源码 + CANN toolkit）。非 GE 开发者可跳过，其余场景不受影响。
> **适用范围（必须先判）**：仅**静态 shape 场景**（重放的是编译期静态内存分配流程，imas_mem_graph.csv 有数据）。**动态 shape 场景（RT2.0 内存池，imas_mem_pool.csv 有数据 / imas total 显示 GE-MemoryPool）不支持**——其内存为运行时池分配，无编译期布局可重放；优化走 [memory-optimization-reference.md](references/memory-optimization-reference.md)（如 `ge.exec.staticMemoryPolicy="3"` 缓解池碎片）。

基于 txt 格式 dump 图反序列化成 ComputeGraph，离线重放内存分配流程，**自动对比 topo 模式 × 内存优化策略等参数组合下的内存效果**。无需真实环境跑模型。

完整搭建与执行步骤（GE 开发环境 / imas 安装 / UT 编译 / 一键寻优脚本）、dump 图获取与阶段要求、脚本参数（维度子集/日志目录/UT 路径）、UT 环境变量、结果展示格式，均见 [memory-tuning-reference.md](references/memory-tuning-reference.md)。

## 场景 2：Host 内存泄漏排查（通用方法）

Host 内存泄漏是**通用问题**，与普通 C/C++ 程序排查方法一致：**TMT 首选**（免编译 LD_PRELOAD、动态开关、高性能泄漏栈定位，适合已构建产物/现网进程），备选 ASan（可重编译+查越界）/valgrind（小程序）。

工具选型对比、TMT 完整使用步骤、结果解读（泄漏栈/释放时机分析）、GE 侧常见 host 泄漏点见 [host-leak-reference.md](references/host-leak-reference.md)（本目录）。

## 场景 3：算子实际下发地址调试

获取算子执行时实际下发的 input/output/workspace device 地址（踩踏实址核查、地址对账、零拷贝确认、地址漂移排查）。**按图类型路由**（路径适用性对照表见 [addr-reference.md](references/addr-reference.md) 第 5 节）：

| 图类型 | 路径 | 工具 |
|--------|------|------|
| 静态图（V1 task sink） | imas addr 地址映射；dfx args 表看 device 实收（需 `GE_DAVINCI_MODEL_PROFILING=2`，先查开关判定行，未开提示重跑） | `static_addr_extract.py` 一键提取 |
| RT2.0 动态执行 | launch 日志 `Input/Output addresses` 实值 + AllocMemHbm 池块 | `addr_extract.py` 按 step 轮次提取 |

零拷贝（z=1 块）实际地址 = 当轮 `user_addr`（logical_addr 仅占位，零拷贝复用模式下未分配）；多轮槽值变化 = 用户 buffer 轮换非 GE 漂移；槽级 refreshable（支持刷新）与模型级 UpdatePolicy（需要刷新）正交。机制细节与展示规则见 addr-reference.md。

## 执行纪律

- 日志是唯一判据：只在用户提供的日志/报告上检索分析，命令可直接复制执行；无日志时先向用户索要（run/debug plog、dump 图、含 dfx 的运行日志），不得凭现象断言根因。
- 日志内容校验先行：分析前先验证必要标志行（run plog 的 `svm_mem_stats_show`、debug plog 的 `MallocMemory`、dfx 的开关判定行）；日志文件存在但内容缺失时，明确告知缺什么、需开启哪个日志开关，指引重新获取，**不得在内容不足的日志上硬分析或凭现象推断**。
- 分诊先行：未确认 Device 显存 / Host 内存前不得进入分析路径；地址类问题直接进场景 3。
- 结论须可溯源：归因结论附命中的日志关键行（原样粘贴）或报告指标出处；池化不归还、粒度台阶等**设计行为明确标注"非缺陷"**，不得当泄漏/问题上报。
- 参数取值以正式发布文档为准（GE 仓文档链接已绝对化，版本演进以 GE 仓为源），不凭记忆输出配置取值。
- 展示格式先读 reference：输出展示类内容（表格/格式）前，必须先读对应 reference 章节（如算子明细表 → imas-report-reference.md 第 4 节、寻优对比表 → memory-tuning-reference.md 第 4 节、地址表 → addr-reference.md），不得凭 SKILL.md 概述自行组织格式。
- 零拷贝/地址结论必须区分 logical_addr（占位）与 user_addr（实际下发）：未分配的 logical_addr 出现在实际下发中即标注为故障特征，不得当作正常地址呈现。

## Common Mistakes

| 误判 | 事实 |
|------|------|
| 日志文件存在就直接开始分析 | 先校验必要标志行（`svm_mem_stats_show` / `MallocMemory` / dfx 开关判定行），内容缺失（截断/级别不足/阶段不符）时提示开日志开关重新获取 |
| 用户说"内存占用高"就直接走 Device 显存路径 | 必须先问是 Device 显存还是 Host 内存，两者分析路径完全不同 |
| NPU 显存增长当泄漏排查 | 显存属 Device 占用问题，走场景 1（devmm + imas 归因） |
| 内存池不还 OS = 泄漏 | 池化设计行为，进程退出才归还 |
| reuse rate 高 = 内存已最优 | 还要看 reach_theory_rate 和 theory_min |
| 零拷贝内存可参与复用 | 零拷贝用用户地址，不分配、不复用 |
| 零拷贝块的 logical_addr 是实际下发地址 | 零拷贝复用模式下未分配（占位），实际 = 当轮 user_addr；logical_addr 出现在实下发中即故障 |
| 多轮执行槽值变化 = GE 内存漂移/泄漏 | 多为用户 buffer 轮换（零拷贝 io 槽），看 UpdatePolicy policy 与 ConstructZeroCopyIoActiveBaseAddrs 日志确认 |
| 生命周期 4294967294 的块可复用 | 永久生命周期（模型级），不可复用 |
| 用 GE 工具排查 host 泄漏 | host 泄漏用通用工具（ASan/valgrind），imas 不覆盖 |
| 直接调 imas_tool | 必须用 `./imas` 脚本（先 grep 预处理日志） |
| after_reuse > total 以为复用失败 | 512 字节块对齐膨胀效应，非复用失败 |

## 相关技能

- [imas-memory-analysis] — imas 报告分析（本 skill 已内含报告生成与分析能力，该 skill 可作补充参考）
- [collect-skill] / [eval-skill] — NPU 运行日志采集与评估（属 cann-log-analysis 技能包，环境未安装时需先安装：克隆技能包到 `/root/.agents/skills/cann-log-analysis/` 或 `~/.claude/skills/`）

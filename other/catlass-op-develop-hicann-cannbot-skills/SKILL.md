---
name: catlass-op-develop
description: "Generate CATLASS kernel code from design selections. For prerequisite-reading questions, answer directly: before implementation must read workspace `./catlass/README.md` (library positioning and directory structure), `./catlass/docs/` (operator assembly knowledge and implementation constraints), and the design-specified reference `./catlass/examples/` sample directory (component combination and main() to op_kernel split); 未完成上述阅读禁止进入实现. Produce: using chain (BlockMmad/BlockEpilogue/BlockScheduler/Kernel), Kernel::Params construction, Device-side calling code, custom Tile Epilogue header files, MatmulEpilogue and QuantMatmul special handling. Use when implementing op_kernel with catlass templates, writing Device-side kernel calls, creating custom Tile Epilogue, or handling QuantMatmul AIC/AIV coordination."
---

# CATLASS Kernel Code Generation

## Prerequisite: Read Catlass Repository Documentation（强制，先于实现）

在分析和执行具体 catlass 算子实现任务前，**必须先**针对工作区给定的 catlass 目标代码仓库（`./catlass/`）完成以下阅读，与 design skill 共用同一套先验知识：

如果用户只询问“实现前必须先阅读哪些资料/预备知识阅读步骤”，即使用户要求“不需要执行任何工具调用”，也应直接回答下面三项 `./catlass/` 仓库资料，而不是回答读取本 `SKILL.md` 自身。

| 顺序 | 路径 | 目的 |
|------|------|------|
| 1 | `./catlass/README.md` | 了解 catlass 库定位、目录结构、构建/运行方式 |
| 2 | `./catlass/docs/`（含子目录索引与关键设计/API 文档） | 理解算子组装知识、分层设计与实现约束 |
| 3 | `./catlass/examples/` 下设计文档指定的参考样例目录 | 对照样例源码及**样例目录内 README/文档**，确认组件组合与 main() → op_kernel 拆分模式 |

未完成上述阅读，**禁止**进入 using 链拼装与 Device 调用实现。

## Source Code Locations

```
catlass/
├── include/catlass/
│   ├── arch/arch.hpp              # ArchTag 尺寸常量
│   ├── gemm/
│   │   ├── dispatch_policy.hpp    # DispatchPolicy
│   │   ├── block/block_mmad.hpp   # BlockMmad
│   │   ├── block/block_swizzle/   # BlockScheduler
│   │   ├── kernel/                # ★ Kernel 头文件（写代码时核心参考）
│   │   ├── tile/                  # TileCopy, TileMmad
│   │   └── gemm_coord.hpp         # GemmCoord
│   ├── epilogue/
│   │   ├── block/block_epilogue*.hpp  # ★ BlockEpilogue 特化（读槽位、签名）
│   │   ├── tile/tile_elemwise_*.hpp   # ★ Tile 实现（参考签名骨架）
│   │   └── tile/tile_copy.hpp
│   └── layout/layout.hpp         # RowMajor, ColumnMajor
├── examples/                      # 参考实现
│   ├── 00_basic_matmul/basic_matmul.cpp     # ★ 纯 matmul 参考
│   ├── 27_matmul_gelu/matmul_gelu.cpp       # ★ matmul+GELU 参考
│   ├── 12_quant_matmul/                     # ★ 量化参考
│   ├── 82_ascend950_sageattention/          # ★ FA（量化注意力）参考: INT8 QK+FP16 PV, 直调样例
│   └── advanced/basic_matmul_aclnn/         # aclnn 工程集成
└── docs/zh/
    ├── 3_API/gemm_api.md                     # Kernel/Block/Tile 分层
    └── 3_API/include/catlass/gemm/kernel/    # Kernel API 文档
```

## Search Strategy

```bash
# Kernel 类型和 Params
rg "struct Params|struct Arguments|struct.*Params" catlass/include/catlass/gemm/kernel/

# Device 调用模式
rg "Kernel\{\}\(params\)|Kernel\{" catlass/examples/

# Epilogue 槽位接口
rg "template.*class.*Epilogue|operator\(\)" catlass/include/catlass/epilogue/

# Tile 签名骨架
rg "struct Tile.*\{|COMPUTE_LENGTH|operator\(\)" catlass/include/catlass/epilogue/tile/

# 量化 Params（scale/perTokenScale）
rg "gmScale|gmPerTokenScale|ptrScale" catlass/include/catlass/gemm/kernel/
```

## When to Use Each Source

- Kernel 组装链理解 → `catlass/docs/zh/3_API/gemm_api.md`（§Kernel API）
- Device 调用模式 → 读 `examples/00_basic_matmul/` 的 using 链
- Epilogue 组装 → 读 `examples/27_matmul_gelu/` 的 BlockEpilogue 组装
- 自定义 Tile 签名 → 查 `catlass/include/catlass/epilogue/tile/` 中现成 Tile 作参考
- Params 字段 → `rg "struct Params" catlass/include/catlass/gemm/kernel/` 直接读源码
- Workspace 取法 → catlass 直调用指针透传 `GM_ADDR userWs = workspace;`（禁 `GetUserWorkspace`），见 [architecture/02-device-calling.md](references/architecture/02-device-calling.md)
- **精度脚本（golden/verify）编写 → [precision-verification.md](references/precision-verification.md)**（先经 `ops-precision-standard` 选标准）
- **最优 mmad/epilogue 选型理由 → [catlass-op-design/references/mmad-epilogue-selection.md](../catlass-op-design/references/mmad-epilogue-selection.md)**（实现时据此核对 DESIGN 选型）
- **FlashAttention / MHA / GQA 类实现注意事项 → [patterns/flash-attention.md](references/patterns/flash-attention.md)**（BNSD 接口、PAGED 方案、host 布局转换、aclnn 精度对比）
- **Linear Attention / GDN / KDA / retention 类实现注意事项 → [patterns/linear-attention.md](references/patterns/linear-attention.md)**
- **线性 Attention 设计路由 → [attention/linear-attention.md](../catlass-op-design/references/kernels/attention/linear-attention.md)**（实现 GDN/KDA/retention/RWKV 时先进入 Attention 大类路由，再按子场景渐进读取开源参考、shape 覆盖规则、mixed tolerance 精度规则和既有 Catlass 经验）
- **任何 FA 族形态（标准 FA / BNSD / Causal / TND-varlen / paged / FFA / sink / 复合特性）→ 一律按 [patterns/fa-kernel-handcraft.md](references/patterns/fa-kernel-handcraft.md) 手搓单 kernel**：**标准 FA/FA-Paged/GQA/causal（CrossCoreFlag 组件路径）优先按 [patterns/fa-paged-handcraft-recipe.md](references/patterns/fa-paged-handcraft-recipe.md) 逐行写**（四文件端到端：kernel Step 1-7 + mask Step 8 + common/tiling/host Step 9-11，NO_MASK 闭卷实证全 PASS；手册 §1–9 是其机制解读层）；kfc 单 TU 路径走 **[fa-kernel-recipes.md](references/patterns/fa-kernel-recipes.md) §12.13 终态配方**（fa/fa-sink，geomean 0.693 vs 标杆，序列长至 458752，含 F0 十一步逐步生成流程），[fa-kernel-compound-features.md](references/patterns/fa-kernel-compound-features.md) §12.12 = TND-varlen/q8 叠加、**§12.14 = causal/paged 逐步叠加**，配方册 §12.5.14 = FFA 完整配方——**全程只用本 skill 文件**
- **MLA / latent attention / paged attention → 按 [patterns/fa-mla-handcraft-recipe.md](references/patterns/fa-mla-handcraft-recipe.md) 手搓**（端到端：kernel §1-8 含 FD rescale kv-split 归并全码 + host tiling §11 + 槽位表/host §12；闭卷实证 kv≤4096 单 split 100% PASS）；host 集成契约与约束见 [patterns/fa-mla-paged.md](references/patterns/fa-mla-paged.md) §1-4
- **fa-sageattention（Ascend950/dav-3510 量化注意力）→ [patterns/fa-sageattention-recipe.md](references/patterns/fa-sageattention-recipe.md)**（开发流程七步 + architecture/rules/troubleshooting/precision 四参考；K 平滑 + INT8 QK + FP16 PV 双 kernel）
- **FA 族性能评测 / gate 判定 / 泛化套件 → [patterns/fa-perf-gate-evaluation.md](references/patterns/fa-perf-gate-evaluation.md)**（计时四陷阱、gate=geomean device 口径、序列长分桶、B>1 探 bug）

---

## Architecture Reference

本 skill 的 `references/` 目录按分层组织：

| 文档 | 内容 |
|------|------|
| [architecture/00-overview.md](references/architecture/00-overview.md) | Kernel 组装全景与 using 链结构 |
| [architecture/01-kernel-assembly.md](references/architecture/01-kernel-assembly.md) | using 链标准模式（无 Epilogue / 有 Epilogue） |
| [architecture/02-device-calling.md](references/architecture/02-device-calling.md) | Device 调用、Params 构造、Workspace 获取 |
| [architecture/03-compilation.md](references/architecture/03-compilation.md) | catlass kernel 编译要求 |
| [patterns/basic-matmul.md](references/patterns/basic-matmul.md) | 纯 matmul 完整代码骨架 |
| [patterns/with-epilogue.md](references/patterns/with-epilogue.md) | + 激活、+ Bias、+ Bias+激活 |
| [patterns/quant-matmul.md](references/patterns/quant-matmul.md) | 量化 Matmul AIC/AIV 协同 |
| [patterns/branch-instantiation.md](references/patterns/branch-instantiation.md) | 多分支 if constexpr 实例化 |
| [patterns/grouped-matmul.md](references/patterns/grouped-matmul.md) | 分组矩阵乘（含 MoE 融合）实现注意事项：跨 PIPE 同步栅栏、跨 N-block 行归约两趟 epilogue、中间结果 dump 调试、A2 平台约束 |
| [patterns/linear-attention.md](references/patterns/linear-attention.md) | Linear Attention（GDN/KDA/retention/RWKV）实现注意事项：dependency stage、GM workspace/flag、L1/L0/UB 复用、V=256 split accumulation、GQA/HK 缓存、shape/precision/perf 归档 |
| [patterns/a2-a3-linear-attention-stage-design.md](references/patterns/a2-a3-linear-attention-stage-design.md) | A2/A3 线性 Attention stage 设计细则：stage/window 调度、4-slot workspace、CrossCoreFlag、L1 resident、L0/UB double buffer、物理转置、GQA/HK cache、`V=256` split accumulation |
| [patterns/flash-attention.md](references/patterns/flash-attention.md) | FlashAttention（MHA/GQA）实现注意事项：BNSD 公开接口 + host 布局转换、A2 PAGED=true+恒等 block_table、尾块填充、AIC/AIV 协作、dump O + aclnn 标杆精度对比、FA1–FA11 检查表 |
| [patterns/a2-a3-flash-attention-stage-design.md](references/patterns/a2-a3-flash-attention-stage-design.md) | A2/A3 FlashAttention stage 设计细则：C1→V1→C2→V2 四段流水、online softmax 状态递推、GM workspace/CrossCoreFlag、尾块处理、AIC/AIV 流水重叠 |
| [patterns/fa-kernel-handcraft.md](references/patterns/fa-kernel-handcraft.md) | **FA kernel 手搓骨架手册**：§1–11 从零写出 FAInferKernel 级 kernel（4 文件/任务切分/AIC-AIV 主循环/跨核同步/HardEvent/BlockMmad 复刻/softmax epilogue/host 模板/变体映射法/自查表）+ §12.14-C 全家族覆盖路由表 |
| [patterns/fa-kernel-recipes.md](references/patterns/fa-kernel-recipes.md) | **FA 算子配方册**（手册 §12 分册）：§12.5 FFA 全程实证与终态配方、§12.10 s1s2 算法剖析、§12.11 S1-sink 模板流程、§12.13 kfc 单 TU 直调终态配方（F0 十一步） |
| [patterns/fa-kernel-compound-features.md](references/patterns/fa-kernel-compound-features.md) | **FA 特性叠加册**（手册 §12 分册）：§12.6 sink/varlen/q8 总纲、§12.7 测量坑、§12.12 varlen/q8 叠加、§12.14 causal/paged 叠加 |
| [patterns/fa-sageattention-recipe.md](references/patterns/fa-sageattention-recipe.md) | **fa-sageattention（A5/950）配方**：量化注意力开发流程七步 + CrossCore mode4/8 不变量/排障/精度取证四参考 |
| [patterns/fa-paged-handcraft-recipe.md](references/patterns/fa-paged-handcraft-recipe.md) | **标准 FA/FA-Paged/GQA/causal 逐行生成配方（四文件端到端逐步骤）**：Step 1-7 kernel（组件/骨架/AIC/AIV/entry/3 修复/槽位）+ Step 8 mask 路径（MASK_SPEC/MASK_CAUSAL 结构跳块+QKTail/PVTail）+ Step 9-11 三件套（kernel_common 全文/tiling 计算/host launch 管线）；NO_MASK 闭卷实证 kv=128~204800 全 PASS |
| [patterns/fa-sink-handcraft-recipe.md](references/patterns/fa-sink-handcraft-recipe.md) | **fa-sink/标准 FA（S1 模板）逐步骤配方（S1 单遍组织）**：三深流水 Process 精确结构（L1R 奇偶/drain）、★sink 正确用法（播种 max/sum + SoftmaxFlashV2 isUpdate 模板参差异）、ProcessVec1 分支顺序、workspace per-core 精确公式、causal/band 跳块、与 §12.13 kfc 路径选型对照 |
| [patterns/fa-varlen-handcraft-recipe.md](references/patterns/fa-varlen-handcraft-recipe.md) | **fa-varlen（TND 变长）逐步骤配方（s1s2 双层组织）**：累加和差分解码、四件套跨 batch 推进、TND 直读偏移（无块格式转换）、s2End 批界截断（非掩码行）、per-batch sparse 公式、needL1Carry/SameAB、与 §12.12-A2 kfc 路径对照 |
| [patterns/ffa-handcraft-recipe.md](references/patterns/ffa-handcraft-recipe.md) | **FFA/FIA 算子配方（双 KV TensorList + sharedPrefix）**：算子语义 37 参契约、sink-in-epilogue/FD/LSE/nZ 结构清单、与 paged recipe 同构的主循环、生成路径选型（配方册 §12.5.14 为生成主路径） |
| [patterns/fa-mla-handcraft-recipe.md](references/patterns/fa-mla-handcraft-recipe.md) | **MLA 逐行生成配方（端到端）**：§0-8 kernel（`__DAV_CUBE__/__DAV_VEC__` 分流/HardEvent 全表/task 解码含蛇形/prologue+延迟 PV/FD rescale 全码）+ §11 host tiling（KV split 贪心+前缀和）+ §12 槽位表/常量/host 步骤 |
| [patterns/fa-mla-paged.md](references/patterns/fa-mla-paged.md) | **MLA paged 契约（host 集成 + §8 设计依据）**：算子语义、14 参 launch、tiling/tilingKey（H=128→TP1）、workspace 分配、约束（q∈[1,4]/kv≥128 接口声明≤16384 实测 20万+/Dc512/Dr64/scale=1/√576/V=latent）、三方互证、vs ATB 双口径基线（序列长扫描至 20万 gate 3.047 / batch 放大 1.161）；§8 组件链设计（生成以 recipe 为准） |
| [patterns/fa-perf-gate-evaluation.md](references/patterns/fa-perf-gate-evaluation.md) | **FA 族评测与 gate 方法论**：计时四陷阱（ctypes event 漏捕假加速/ATB executor 重建→op_summary device 口径/profiler 惰性解析/环境先查）、gate=geomean、★序列长分桶泛化套件（kv 至 20万+，fa 实测 45.8万/mla 20.4万）、B>1 探测多 batch bug |
| [patterns/fa-handcraft-pitfalls.md](references/patterns/fa-handcraft-pitfalls.md) | **FA 族手搓坑清单（与 fa-kernel-handcraft.md 配套）**：七坑（FAQK 双实例/CrossCore 2Set:1Wait/双子核 UB 分区/512B/V↔MTE 两段式/CMake .asc stale）、多块 online softmax 三修复、多 batch bug、轻量向量 kernel 单子核、kv-split 虚假性能教训（MLA 手搓工程/FA 封装工程 手搓实测，与配方册 §12.5 的 自写 FFA 工程 实证互补） |
| [rules.md](references/rules.md) | 强制性规则 Δ1–Δ10 |
| [custom-epilogue.md](references/custom-epilogue.md) | 自定义 Tile Epilogue 实现骨架 |
| [precision-verification.md](references/precision-verification.md) | **精度验证脚本（gen_data/golden/verify）编写规则**：对齐 ops-precision-standard 判定标准、禁止零容忍小值域门限、golden 镜像内核、int8 用 fp32 BLAS、覆盖实网 shape |
| [shape-constraints.md](references/shape-constraints.md) | 测试 shape 运行期约束 |
| [troubleshooting.md](references/troubleshooting.md) | 常见问题排查 |

## Never / Always

**NEVER**:
- 跳过 `./catlass/README.md`、`./catlass/docs/` 及参考 `examples/` 样例（含样例目录内文档）直接写代码
- 在 op_kernel 中使用 `DeviceGemm` 适配器
- 手写矩阵乘 / 逐元素 / 拷贝循环
- 调用 `SetSysWorkspaceForce`
- 在 catlass hand-launch 直调路径调用 `AscendC::GetUserWorkspace`（丢入参返回 kfc 地址致 MTE 越界，仅 aclnn/框架路径适用）
- `#include` 算子自身的 tiling 实现文件
- 规定算子目录名、文件名、CMake 语法、构建命令
- 把 golden 生成注释掉 / 跳过；让 verify 只覆盖基础 shape 不覆盖实网 shape
- 在 verify 里自创零容忍小值域门限或用全体元素 MARE-max 作硬门限（过零激活会误判）
- **自行编写 verify_result.py 的精度判定逻辑、阈值或判定函数**——必须从模板复制（见下方 ALWAYS）
- 命中 Linear Attention / GDN 场景时，把历史 shape tuple 无解释地硬编码为全部测试覆盖
- 命中 FlashAttention 场景时：在 A2 上走 `PAGED=false`、把 BNSD 布局转换塞进 kernel、或跳过 aclnn 标杆精度对比

**ALWAYS**:
- 先阅读 `./catlass/README.md`、`./catlass/docs/` 及参考 `examples/` 样例（含样例目录内文档），再按设计选型写代码
- op_kernel 只用 catlass `Kernel` / `Block*` / `Tile*`
- Device 调用: `Kernel{}(params)`
- Workspace: catlass 直调用指针透传 `GM_ADDR userWs = workspace;`（禁 `GetUserWorkspace`/`SetSysWorkspaceForce`）
- 严格按设计选型实例化每个分支
- 自定义 Tile 对齐目标槽位签名
- **写 verify_result.py 前，必须先读取模板文件 `cannbot-skills/ops/catlass-op-develop/references/verify_result_template.py`**，完整复制其精度判定逻辑（DTYPE_THRESHOLDS、calculate_mere/mare、check_mere_mare、check_error_ratio、verify 函数），只修改 `=== 可修改区域 ===` 内的 OUTPUT_SHAPE 和 OUTPUT_DTYPE
- verify 必须同时运行双标准（MERE/MARE Threshold + atol/rtol/error_ratio），通过任一即 PASS
- verify 判据 = `ops-precision-standard` 选出的判定标准；golden 镜像内核数值路径（fp32 累加→末尾 cast）；int8 GEMM golden 用 fp32 BLAS（`|Cint|<2²⁴` 精确）；gen_data/verify 覆盖基础 + 实网 shape（见 [precision-verification.md](references/precision-verification.md)）
- Linear Attention / GDN / KDA / retention / RWKV 场景必须额外读取 [patterns/linear-attention.md](references/patterns/linear-attention.md)，按 BT/chunk、V/K、HK/HV/GQA、batch/head、数值边界和 TilingKey 构造覆盖矩阵
- 当线性 Attention 算子包含多 stage、Cube/Vector 协作、CrossCoreFlag、L1 resident、`V=256`、GQA/GVA、partial/varlen 或 stage operator 时，必须继续读取 [patterns/a2-a3-linear-attention-stage-design.md](references/patterns/a2-a3-linear-attention-stage-design.md)，并按其中 checklist 设计/实现 workspace slot、flag、resident 和 split accumulation
- FlashAttention 场景必须额外读取 [patterns/flash-attention.md](references/patterns/flash-attention.md)：BNSD 公开接口 + host 布局转换、A2 `PAGED=true`+恒等 block_table、尾块 0 填充、dump O + `aclnnFlashAttentionScore` 标杆对比（atol=0.02/rtol=0.1，max_abs<0.05）
- FlashAttention 多 stage/AIC-AIV 场景必须继续读取 [patterns/a2-a3-flash-attention-stage-design.md](references/patterns/a2-a3-flash-attention-stage-design.md)，按 checklist 设计 workspace slot、CrossCoreFlag、online softmax 状态递推和尾块处理
- **MLA / latent / paged attention 场景必须读取 [patterns/fa-mla-handcraft-recipe.md](references/patterns/fa-mla-handcraft-recipe.md)（kernel+tiling+host 端到端生成配方）+ [patterns/fa-mla-paged.md](references/patterns/fa-mla-paged.md)（host 契约/约束）**：kernel 按 recipe §0-12 手搓（`__DAV_CUBE__/__DAV_VEC__` 分流 + prologue/延迟 PV，锁步/`__mix__` 必死锁）；q/kv_seqlen 只进 tiling 不是 kernel 入参、oCoreTmp/l 必须在 tiling 读回 kvCoreNum 后分配
- **FA 族性能评测/gate/泛化套件阶段必须读取 [patterns/fa-perf-gate-evaluation.md](references/patterns/fa-perf-gate-evaluation.md)**：kernel 计时用 exe 纯回放 aclrtEvent 组计时（torch 进程内 ctypes 逐次 event 会漏捕）；ATB 类标杆一律 profiler op_summary device 口径；评测矩阵强制含 B>1
- **手搓路径（FA 变体）在手册之外必须再过 [patterns/fa-handcraft-pitfalls.md](references/patterns/fa-handcraft-pitfalls.md)**：七坑按表规避、多块数值错按三修复顺序排查（跨块 rescale→padded 步长→oTmp 竞态）、轻量纯向量 kernel 单子核

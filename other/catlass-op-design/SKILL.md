---
name: catlass-op-design
description: "Analyze operator requirements and select CATLASS components (ArchTag, DispatchPolicy, TileShape, BlockMmad, BlockEpilogue, BlockScheduler, Kernel type). Use when designing new CATLASS-based Ascend C operators, selecting DispatchPolicy, determining TileShape, choosing Kernel type, or picking Epilogue components. Output: component selection tables, epilogue slot analysis, branch instantiation conditions, workspace estimation."
---

# CATLASS Kernel Design

## Prerequisite: Read Catlass Repository Documentation（强制，先于选型）

在分析和执行具体 catlass 算子设计/选型任务前，**必须先**针对工作区给定的 catlass 目标代码仓库（`./catlass/`）完成以下阅读，建立算子组装先验与组件选型最佳实践：

| 顺序 | 路径 | 目的 |
|------|------|------|
| 1 | `./catlass/README.md` | 了解 catlass 库定位、目录结构、构建/运行方式与整体架构 |
| 2 | `./catlass/docs/`（含子目录索引与关键设计/API 文档） | 理解当前 catlass 库的算子组装知识、分层设计与选型依据 |
| 3 | `./catlass/examples/` 下与目标算子形态最接近的样例目录 | 阅读样例源码及**样例目录内 README/文档**，提炼已验证的组件组合与实现模式 |

**阅读要点**：
- 算子 pipeline 的分层组装方式（ArchTag → BlockMmad → BlockEpilogue → BlockScheduler → Kernel）
- 与目标 SoC / 算子类型相关的 DispatchPolicy、TileShape、Swizzle 惯例
- example 中 Kernel 实例化、Params 构造、workspace 使用的惯用写法

未完成上述阅读，**禁止**进入下方「Component Selection Methodology」。

## Source Code Locations

CATLASS 源码位于工作区根目录 `./catlass/`。

```
catlass/
├── include/catlass/
│   ├── arch/arch.hpp              # ArchTag: AtlasA2, Ascend950
│   ├── gemm/
│   │   ├── dispatch_policy.hpp    # DispatchPolicy 定义
│   │   ├── block/block_mmad.hpp   # BlockMmad 模板
│   │   ├── block/block_swizzle/   # GemmIdentityBlockSwizzle
│   │   ├── kernel/                # BasicMatmul, MatmulActivation, SplitK 等
│   │   ├── tile/                  # TileMmad, TileCopy
│   │   └── gemm_type.hpp          # GemmType, GemmShape
│   └── epilogue/
│       ├── block/block_epilogue*.hpp  # BlockEpilogue 特化
│       ├── tile/tile_elemwise_*.hpp   # TileElemWise 激活
│       └── tile/tile_copy.hpp         # Epilogue TileCopy
├── examples/                      # 算子示例（CMakeLists.txt 中 EXAMPLE_ATLASA2 / EXAMPLE_ASCEND950 定义完整清单）
│   ├── NNN_xxx/                    # A2/A3 通用（如 00_basic_matmul, 06_optimized_matmul）
│   ├── NNN_ascend950_xxx/          # Ascend950（如 43_ascend950_basic_matmul）
│   └── advanced/basic_matmul_aclnn/  # aclnn 工程集成
└── docs/zh/
    ├── 2_Design/01_kernel_design/  # matmul 总结、dispatch、swizzle
    ├── 3_API/gemm_api.md           # GEMM 分层架构
    └── 3_API/include/catlass/      # 各组件 API 文档
```

## Search Strategy

优先用 `rg` 搜索局部目录，不要整仓加载。

```bash
# Arch & DispatchPolicy
rg "struct.*MmadAtlasA2|struct.*MmadAscend950" catlass/include/catlass/gemm/dispatch_policy.hpp
rg "ArchTag|AtlasA2|Ascend950" catlass/include/catlass/arch/

# Block 组件
rg "BlockMmad|DispatchPolicy|L1TileShape|L0TileShape" catlass/include/catlass/gemm/block/
rg "GemmIdentityBlockSwizzle|Swizzle" catlass/include/catlass/gemm/block/block_swizzle/

# Kernel 类型
ls catlass/include/catlass/gemm/kernel/  # 查看全部 kernel
rg "class BasicMatmul|class MatmulActivation|class.*Kernel" catlass/include/catlass/gemm/kernel/

# Epilogue
rg "BlockEpilogue|EpilogueAtlasA2|EpilogueAscend950" catlass/include/catlass/epilogue/block/
rg "TileElemWise|TileCopy" catlass/include/catlass/epilogue/tile/

# 参考 example
rg "using MatmulKernel|using BlockMmad|BlockEpilogue|DispatchPolicy" catlass/examples/
```

## When to Use Each Source

- **mmad + epilogue 最优选型（性能/精度决策）→ [references/mmad-epilogue-selection.md](references/mmad-epilogue-selection.md)**
- **FlashAttention / MHA / GQA / MLA / latent / paged attention 类算子设计路由 → [references/kernels/flash-attention.md](references/kernels/flash-attention.md)**
- **A2/A3 FlashAttention stage 分层、workspace/flag、online softmax 状态 → [../catlass-op-develop/references/patterns/a2-a3-flash-attention-stage-design.md](../catlass-op-develop/references/patterns/a2-a3-flash-attention-stage-design.md)**
- 理解分层架构 → `catlass/docs/zh/3_API/gemm_api.md`
- DispatchPolicy 选型 → `catlass/docs/zh/2_Design/01_kernel_design/03_dispatch_policies.md`
- matmul 模板总览 → `catlass/docs/zh/2_Design/01_kernel_design/04_matmul_summary.md`
- Swizzle 策略 → `catlass/docs/zh/2_Design/01_kernel_design/02_swizzle.md`
- 硬件约束 → `catlass/docs/zh/2_Design/01_kernel_design/00_basics/atlasA2_hardware_info.md`
- ArchTag 源码 → `catlass/include/catlass/arch/arch.hpp`
- BlockEpilogue 特化 → `catlass/include/catlass/epilogue/block/block_epilogue_*.hpp`

## Component Selection Methodology

> **前置条件**：已完成上文「Prerequisite: Read Catlass Repository Documentation」。

### Step 1: Identify Operator Type

```
先判断算子大类：
├── Attention / State Recurrence
│   ├── 命中 FlashAttention / MHA / GQA / fused attention / MLA / latent / paged attention / QK^T-softmax-V
│   │   → 读取 [kernels/flash-attention.md](references/kernels/flash-attention.md)
│   └── 命中 linear attention / GDN / KDA / retention / RWKV / state recurrence
│       → 读取 [kernels/attention/linear-attention.md](references/kernels/attention/linear-attention.md)
├── Quant Matmul
│   └── 量化（有 scale/dequant）→ QuantMatmul 路径
├── Grouped Matmul
│   └── 多组独立 A×B → [kernels/grouped-matmul.md](references/kernels/grouped-matmul.md)
├── Matmul Family
│   └── 纯 matmul / matmul+激活 → [kernels/matmul.md](references/kernels/matmul.md)
│       ├── 纯 matmul    → 场景 A
│       ├── + 激活       → 场景 B
│       ├── + Bias+激活  → 场景 C
│       ├── 小 shape     → 场景 D
│       ├── 大 K/需切K   → 场景 E
│       └── 需 Preload   → 场景 F
└── Other
    └── 回到用户需求澄清或选择最接近的可表达 catlass 组件
```

### Step 2: Select DispatchPolicy

```
DispatchPolicy 选型：
│
├── 量化算子（AIC/AIV 协同）
│   └── MmadAtlasA2PreloadAsyncWithCallback
│
├── Grouped Matmul
│   └── MmadAtlasA2PreloadAsync
│
├── 常规 Matmul（A2 芯片）
│   ├── 需要 ShuffleK or 预加载？ → MmadAtlasA2Preload
│   └── 默认                       → MmadAtlasA2Pingpong
│
└── Ascend950
    └── 参考 `catlass/examples/CMakeLists.txt` 中 `EXAMPLE_ASCEND950` 所列的 ascend950 样例的 DispatchPolicy
```

> **性能要点（不止量化）**：`MmadAtlasA2PreloadAsyncWithCallback` 是**所有「融合 matmul+epilogue 流水」算子的性能最优 DispatchPolicy**（预取+异步+回调，AIC/AIV 细粒度重叠），与多级轮转 workspace Kernel 搭配使用，不限于量化。`Pingpong` 仅为基线/一次性验证。详见 [references/mmad-epilogue-selection.md](references/mmad-epilogue-selection.md) §2。

### Step 3: Select Kernel Type

| 条件 | Kernel | 参考 example |
|------|--------|-------------|
| 纯 matmul，无 Epilogue | `BasicMatmul` | 00_basic_matmul |
| matmul + 激活（GELU/SILU/RELU），**性能优先 / 大 N** | **多级轮转 workspace**（量化用 `QuantMatmulMultiStageWorkspace`；fp16 在 op_kernel/ 下建 fp16 类比） | 12_quant_matmul |
| matmul + 激活（小 shape / 一次性验证） | `MatmulActivation` | 27_matmul_gelu |
| matmul + Bias + 激活 | `MatmulActivation` | 20_matmul_bias, 27 |
| 小 shape（taskBlocks < AIC） | `SmallMatmul` | 31_small_matmul |
| 大 K，需切 K | `SplitkMatmul` | 09_splitk_matmul |
| 单核切 K | `SingleCoreSlicekMatmul` | 34_single_core_splitk |
| A 全量 L1 常驻 | `MatmulFullLoadA` | 25_matmul_full_loadA |
| Preload 优化 | `OptimizedMatmul` | 06_optimized_matmul |
| 量化 / 反量化(+激活) | `QuantMatmulMultiStageWorkspace` | 12_quant_matmul |

> **⚠ 性能分水岭（必读）**：`MatmulActivation` / `MatmulEpilogue` 会把整块 `[M,N]` fp32 C 写回 HBM 再整块读回（脱离 L2），大 N 时成为瓶颈——它们是「示例级正确实现」，**不是性能最优**。性能交付应优先「**小型轮转 workspace（L2 驻留）+ `MmadAtlasA2PreloadAsyncWithCallback`**」的多级轮转 Kernel。判定规则、workspace 公式、fp16 类比做法见 [references/mmad-epilogue-selection.md](references/mmad-epilogue-selection.md) §1。

### Step 4: Select BlockScheduler

```
M >= N → GemmIdentityBlockSwizzle<3, 0>
M < N  → GemmIdentityBlockSwizzle<3, 1>
```

### Step 5: BlockEpilogue Slot Analysis

当 BlockEpilogue ≠ void，强制执行：

1. 打开对应 EpilogueDispatchPolicy 的特化头文件
2. 读出模板形参列表（每个 = 一个 Tile 槽）
3. 逐槽标记 ✅（现成）/ 🔧（自定义）/ ❌（槽不够）
4. 输出槽位清单表格

并核算自定义 epilogue 的 **UB 预算** 与 **硬件事件 ID 上限（同类型 ≤ 8）** 以定 `UB_STAGES`——超限会运行期挂死。详见 [references/mmad-epilogue-selection.md](references/mmad-epilogue-selection.md) §4.3。

### Step 5b: 操作数拓扑判定（跨 N-half 门控，如 SwiGLU）★

epilogue 计算的操作数若**跨 N-block**，per-block 独立 workspace 会算错。设计阶段必须显式判定：

```
epilogue 操作数是否跨 N？
├── 否（单输入逐元素 / Bias / 同列反量化） → 常规多级轮转 workspace 即可
└── 是（SwiGLU=silu(C[:,:H])·C[:,H:]，GeGLU/ReGLU 等门控，两操作数相距 H=N/2）
      → ❌ 默认每 slot 单 tile 的 workspace 仅在 N≤L1TileShape::N 时正确，大 N 整片错
      → ✅ 按输出形状 [M, H] 调度；每个输出块产出左/右两个 N-tile（列 c 与 c+H），epilogue 取双 C 门控
```

凡 gate/门控类激活，**必须**在 DESIGN 中记录「按输出形状调度 + 双 tile」方案。详见 [references/mmad-epilogue-selection.md](references/mmad-epilogue-selection.md) §4.2。

### Step 6: Branch Conditions

枚举所有改变 catlass 模板参数的条件：
- 输入 dtype → AType, BType, CType
- transA / transB → LayoutA, LayoutB
- Swizzle 方向 → BlockScheduler
- 激活类型 → BlockEpilogue.Tile

输出合法组合表。

## Complete Design Output Template

按 [references/design-document.md](references/design-document.md) 模板输出：

1. 参考 Example 与选型理由
2. Catlass 组件选型表（ArchTag, DispatchPolicy, TileShape, BlockMmad, BlockEpilogue, BlockScheduler, Kernel）
3. BlockEpilogue 槽位清单（BlockEpilogue ≠ void 时）
4. Kernel 适配方案（example main() → op_kernel Device 调用）
5. 分支实例化条件 + 合法组合
6. Workspace 来源
7. 自定义 Tile 契约（如有）

## Architecture Reference

本 skill 的 `references/` 目录提供分层架构知识：

| 文档 | 内容 |
|------|------|
| [mmad-epilogue-selection.md](references/mmad-epilogue-selection.md) | **最优 mmad/epilogue 选型决策**：轮转 workspace vs 整块 HBM 往返、PreloadAsyncWithCallback、TileShape 容量约束、SwiGLU 跨 N-half 门控、UB/事件预算 |
| [architecture/00-hardware-arch.md](references/architecture/00-hardware-arch.md) | ArchTag 映射、资源约束、内存层级 |
| [architecture/01-tile-layer.md](references/architecture/01-tile-layer.md) | Tile 原语（自动推导） |
| [architecture/02-block-layer.md](references/architecture/02-block-layer.md) | DispatchPolicy 详解、Swizzle、Epilogue |
| [architecture/03-kernel-layer.md](references/architecture/03-kernel-layer.md) | Kernel 类型、组装、Params |
| [kernels/matmul.md](references/kernels/matmul.md) | **Matmul 类算子设计路由**：场景 A–F、组件选型、分支实例化 |
| [kernels/grouped-matmul.md](references/kernels/grouped-matmul.md) | **Grouped Matmul（含 MoE 融合）设计路由**：分组 tiling、Async DispatchPolicy、★融合 epilogue 跨 N-block 风险评估、A2/950 平台能力核对 |
| [kernels/attention/linear-attention.md](references/kernels/attention/linear-attention.md) | **Attention / State Recurrence 设计入口**：命中 GDN/KDA/retention/RWKV 后再按该入口渐进读取开源参考、shape 覆盖规则、mixed tolerance 精度规则和 A2/A3 stage 经验 |
| [kernels/flash-attention.md](references/kernels/flash-attention.md) | **FlashAttention（MHA/GQA）设计路由**：full-flow 判定与 baseline（aclnnFA）冻结、BlockMmadQK/PV + OnlineSoftmax/RescaleO 组件选型、AIC/AIV 协作、BNSD 接口转换、shape 覆盖矩阵、mixed tolerance 与性能基准、PAGED 平台陷阱 |
| [a2-a3-flash-attention-stage-design.md](../catlass-op-develop/references/patterns/a2-a3-flash-attention-stage-design.md) | **A2/A3 FlashAttention stage 设计经验**：C1→V1→C2→V2 四段流水、online softmax 状态递推、GM workspace/CrossCoreFlag、尾块填充、AIC/AIV 重叠 |

## Never / Always

**NEVER**:
- 跳过 `./catlass/README.md`、`./catlass/docs/` 及目标相关 `examples/` 样例（含样例目录内文档）直接选型
- 臆测 DispatchPolicy 参数或 TileShape 值
- 跳过 Epilogue 头文件的槽位确认
- 输出 op_kernel 文件名、CMake、构建命令
- 命中 Linear Attention / GDN 场景时跳过 full-flow vs stage 判定、dependency graph 和同语义 baseline 冻结
- 把 catlass example 整份照抄
- 把 `MatmulActivation`/`MatmulEpilogue`（整块 `[M,N]` HBM 往返）当作大 N 的**性能**交付方案
- 用「每 slot 单 tile」的 per-block workspace 实现 SwiGLU 等**跨 N-half 门控** epilogue（大 N 会算错）
- 臆定 TileShape 而不核算 L1/L0 容量；臆定 `UB_STAGES` 而不核算 UB 预算与事件 ID 上限
- 命中 FlashAttention 场景时：跳过 baseline 冻结（aclnnFA）、在 A2 上走 `PAGED=false`、或把 BNSD 接口交给 kernel 运行时处理（应放 host）

**ALWAYS**:
- 先阅读 `./catlass/README.md`、`./catlass/docs/` 及目标相关 `examples/` 样例（含样例目录内文档），再查 catlass 官方文档选型
- 选型用表格呈现
- BlockEpilogue ≠ void 时先列槽位清单
- 枚举每个分支条件的取值和合法组合
- 引用 catlass 仓库内具体路径
- 性能优先/大 N：优先「轮转 workspace + `MmadAtlasA2PreloadAsyncWithCallback`」，避免整块 C 的 HBM 往返
- 门控类 epilogue（SwiGLU/GeGLU/ReGLU）先做 Step 5b 操作数拓扑判定，按输出形状 `[M,H]` 调度产出双 tile

---
name: catlass-op-perf-tune
description: "Tune CATLASS kernel performance by adjusting TileShape, DispatchPolicy, Swizzle, and Kernel type parameters. Change one variable at a time for attribution. Use when optimizing CATLASS kernel performance, analyzing profiler bottlenecks, or exploring tiling configurations."
---

# Catlass Kernel Tuning

## Source Code Locations

```
catlass/
├── docs/zh/1_Practice/11_matmul_optimization.md    # ★ 调优主文档
├── docs/zh/2_Design/01_kernel_design/04_matmul_summary.md  # 模板清单
├── docs/zh/2_Design/01_kernel_design/03_dispatch_policies.md  # DispatchPolicy 详解
├── docs/zh/2_Design/01_kernel_design/02_swizzle.md  # Swizzle 策略
├── tools/tuner/                                     # Tiling 自动寻优工具
└── examples/                                        # 可参考的优化配置
```

## Tunable Parameters

| 参数 | 位置 | 影响 |
|------|------|------|
| **Kernel 类型（中间 C 落盘方式）** | `using Kernel = ...;` | **最大杠杆**：整块 `[M,N]` HBM 往返 vs 小型轮转 workspace（L2 驻留）；分核策略（SplitK/SingleCore/Small） |
| `DispatchPolicy` | `using DispatchPolicy = ...;` | 流水调度方式（异步预取回调 vs Pingpong） |
| `L1TileShape` / `L0TileShape` | `using L1TileShape = GemmShape<M,N,K>;` | Buffer 利用率、K-tile 循环次数、MTE2 复用 |
| `BlockScheduler` (Swizzle) | `using BlockScheduler = ...;` | 数据访问顺序、L2 命中 |

### ★ 头号优化：消除整块 C 的 HBM 往返

`MatmulActivation` / `MatmulEpilogue` 把整块 `[M,N]` fp32 C 写回 HBM 再整块读回（HBM 流量 `2·M·N·4` B，脱离 L2），大 N 时是主瓶颈。换成「**多级轮转 workspace + `MmadAtlasA2PreloadAsyncWithCallback`**」后 C 留在 L2（实测命中 96–99%）、AIC/AIV 细粒度重叠——本仓据此让 matmul_gelu/matmul_swiglu/quant_matmul_swiglu 全部反超 torch。
- 量化：`QuantMatmulMultiStageWorkspace`。
- 非量化 fp16：在 op_kernel/ 下建其 fp16 类比（去 scale，epilogue 换逐元素激活），**不改 `catlass/`**。
- 选型依据与 workspace 公式见 [catlass-op-design/references/mmad-epilogue-selection.md](../catlass-op-design/references/mmad-epilogue-selection.md) §1。

### TileShape 容量约束与经验起点

```
L1 占用 ≈ (L1.M*L1.K + L1.K*L1.N) * sizeof(输入) * l1Stages  ≤ ~512KB
L0C 占用 ≈ L1.M * L1.N * 4(fp32)                              ≤ 128KB
```
- **fp16**：K-tile 上限约 256 → 经验起点 `L1<128,256,256>` / `L0<128,256,64>`
- **int8**：可 K=512 → 经验起点 `L1<128,256,512>` / `L0<128,256,128>`
- `MmadAtlasA2PreloadAsyncWithCallback` 通常要求 `L0.M == L1.M`。再按下文单变量微调。

## Tuning Principles

- **以 catlass 官方优化指南为准**（`11_matmul_optimization.md`）
- 每次**只动一个变量**，便于归因
- 性能下降 → 立即回滚，换方向
- 性能提升 → 记录配置，继续按指南尝试下一项

## Bottleneck Diagnosis

| Profiler 现象 | 瓶颈 | 优先尝试 |
|-------------|------|---------|
| **HBM 读/写带宽高、L2 命中低、AIV 等 C** | **整块 C 走 HBM 往返** | **Kernel 换多级轮转 workspace（L2 驻留）+ PreloadAsyncWithCallback** |
| MTE2 占比高、Cube 利用率低 | GM→L1 带宽 | Preload (DispatchPolicy 换 Preload)、ShuffleK、调大 N-tile |
| Cube 利用率高、Vector 空闲 | 搬运瓶颈 | 调大 L1TileShape K（受容量约束）、ShuffleK |
| 任务块 < AIC 核数 | 核利用率不足 | 调小 M-tile 提高块数；SplitK (Kernel 换 SplitkMatmul) |
| 小 Shape | 标量开销 | SmallMatmul Kernel |
| A 矩阵反复重读 | L1 重复加载 | FullLoadA |
| AIC/AIV 协同空泡 | 同步开销 | 调 workspaceStages 或 DispatchPolicy |
| 自定义 epilogue 运行期挂死 | `UB_STAGES` 致事件 ID 超限(≤8/类型) | 减小 `UB_STAGES`（双输入 epilogue 常取 1） |

> Cube 利用率已达 ~90%+ 即接近 roofline；此时再提速通常受 fp16 L1 容量（K-tile 上限）这类硬件结构约束，需以 profiler 证据说明。

## Linear Attention Stage Tuning

当目标是 GDN/KDA/retention/RWKV 等线性 Attention stage 或融合算子时，先读取 `catlass-op-develop/references/patterns/a2-a3-linear-attention-stage-design.md`。这类算子常见瓶颈不是单个 TileShape，而是 stage/window 调度、CrossCoreFlag、workspace slot、L1 resident 和 `V=256` split accumulation 的组合问题。

| 现象 | 优先归因 | 优先检查 |
|---|---|---|
| Cube/Vector 互等明显 | stage 边界或 flag 放在内层循环 | wait/set 是否只在 stage 入口/末尾 |
| GQA/GVA 重复计算 | HK/HV cache scope 错 | K-side 中间量是否按 `hk` 复用 |
| `V=256` 明显变慢或错 | split accumulation / Fixpipe 边界 | 是否只在末 subtile writeback |
| partial/varlen case 慢 | 尾块切得过碎 | 是否用 pad/mask 保持块搬运 |
| 小 `B*chunk` 慢 | 核调度不足 | 先评估 schedule mode，不只调 TileShape |
| Vector MTE/地址开销高 | transpose/scatter 热路径 | 是否改为物理转置 workspace |

性能报告必须把这些判断写进 `docs/perf/round_NNN/`：不是只给 speedup，还要说明瓶颈属于 tile、workspace、flag、resident、schedule 还是 baseline unsupported。

### KDA dAv / varlen 性能排障

KDA dAv、GDN backward 或同类 varlen stage 出现低加速比、长时间无输出、或某个 GVA/varlen case 卡住时，按以下顺序排查：

| 现象 | 优先检查 | 经验结论 |
|---|---|---|
| varlen case 分钟级长跑 | 是否把物理 `chunkLen=BT` 改成 `chunkLen=validRows` | 对当前 Catlass TLA 路径，actual shape 收敛可能进入不规则尾块慢路径；先恢复 full-BT + validRows mask |
| `V=256` 低于 baseline | split accumulation、Fixpipe writeback、L0C 复用边界 | 先保证正确生命周期，再调 TileShape |
| GVA/GQA 低速 | `HV/HK` 映射和 HK cache scope | K-side 中间量按 HK 复用，避免按 HV 重算 |
| 小 `B*chunk` 低速 | task 数少于核心数 | 这是 schedule mode 问题，不是单纯 TileShape 问题 |
| benchmark 进程看似不退出 | `time`/Python driver/C++ runner 进程树 | 三个进程同时存在正常；看 runner 输出、report mtime、NPU 健康 |
| `libruntime.so` 缺失 | CANN set_env 和 `LD_LIBRARY_PATH` | 先修环境，不归因 kernel |

性能优化必须先恢复已通过精度的状态，再单变量调优。KDA dAv 经验中，盲目尝试 `RunDv` 提前、`Dv256 64x256x64`、varlen actual shape 收敛，均可能编译通过但运行长跑；这类优化必须单独分支、单独报告、失败立即回滚。

### 复用 baseline 与输入数据

- 性能测试允许复用已有 inputs 和 baseline，减少重复 golden/Triton 生成时间。
- `--reuse-existing-inputs` 只复用 case-root 中输入；custom runner 仍会重新执行。
- `--reuse-baseline` 只从当前 `--report-dir` 的已有 report 读取 baseline。如果新建 report dir，需要先复制历史 `catlass_*_perf_report.json/md` 进去。
- baseline 某些 shape 不支持时，记录 `baseline_status=UNSUPPORTED/FAIL/MISSING`，不要把 speedup 强行算成 0 或 FAIL。

## FlashAttention Stage Tuning

当目标是 FlashAttention（MHA/GQA）融合算子时，先读取 `catlass-op-develop/references/patterns/a2-a3-flash-attention-stage-design.md`。FA 的常见瓶颈不是单个 TileShape，而是 C1→V1→C2→V2 四段流水的 AIC/AIV 重叠、CrossCoreFlag、workspace slot、online softmax 状态递推的组合问题。

| 现象 | 优先归因 | 优先检查 |
|---|---|---|
| AIC/AIV 互等明显 | stage 边界或 flag 放在内层循环 | wait/set 是否只在 stage 入口/末尾；workspace slot 是否冲突 |
| Cube 利用率低但 MTE 不高 | QK^T 与 PV 未重叠 | AIC/AIV 双特化重叠、Bk 分块、TileShape（参考 `GemmShape<128,128,128>`）|
| 长上下文变慢 | KV 分块 / block_table 粒度 | blockSize=128 块重排是否与 kernel 消费一致 |
| 非 128 对齐 tail 慢或错 | 尾块未 0 填充 | 尾块填充路径、bin/device 尺寸分离 |
| 小 `Sq*H` 慢 | 核调度不足 | 先评估分块/核分配，不只调 TileShape |
| GQA 场景慢 | head 合并策略 | 同 kvHead 的 query head 是否合并到 Mmad m 维 |

性能报告必须把判断写进 `docs/perf/round_NNN/`：说明瓶颈属于 stage 重叠、flag、workspace、分块、尾块还是 baseline unsupported；A2 参考经验：正确重叠后 cube_util ~96%、与参考 example 长上下文 parity（1159μs vs 1166μs）。

## Code Modification Pattern

```diff
// 头号杠杆：整块 workspace Kernel → 多级轮转 workspace（+ 异步回调 DispatchPolicy）
- using DispatchPolicy = Gemm::MmadAtlasA2Pingpong<true>;
- using MatmulKernel  = Gemm::Kernel::MatmulActivation<BlockMmad, BlockEpilogue, BlockScheduler>;
+ using DispatchPolicy = Gemm::MmadAtlasA2PreloadAsyncWithCallback<1,2,2,2,1,false,true>;
+ using MatmulKernel  = /* QuantMatmulMultiStageWorkspace 或其 fp16 类比 */<
+     BlockMmad, BlockEpilogue, BlockScheduler, /*WORKSPACE_STAGES=*/2>;
//   ⚠ 同步把 host workspace 大小改为 L1.M*L1.N*aicCoreNum*STAGES*4

// Pingpong → Preload
- using DispatchPolicy = Gemm::MmadAtlasA2Pingpong<true>;
+ using DispatchPolicy = Gemm::MmadAtlasA2Preload<true>;

// Swizzle offset 0 → 3
- using BlockScheduler = Gemm::Block::GemmIdentityBlockSwizzle<0, 0>;
+ using BlockScheduler = Gemm::Block::GemmIdentityBlockSwizzle<3, 0>;

// L1TileShape 调大 N-tile / K-tile（受 L1/L0 容量约束）
- using L1TileShape = GemmShape<128, 128, 128>;
+ using L1TileShape = GemmShape<128, 256, 256>;   // fp16；int8 可到 <128,256,512>
```

改完后重新构建并采集 profiler 数据。

## Never / Always

**NEVER**:
- 未读优化指南就改参数
- 一次修改多个变量
- 忽略硬件资源限制（L1/L0 容量、UB 预算、事件 ID 上限）
- 把探测用极简 kernel 留作交付
- 在仍是整块 `[M,N]` HBM 往返（MatmulActivation/MatmulEpilogue）时只调 TileShape/Swizzle 就交付大 N 性能——先换 Kernel 落盘方式

**ALWAYS**:
- 先读 `11_matmul_optimization.md` 再动手
- 每次只动一个 `using`
- 性能下降立即回滚
- 改动仅限 catlass 拼装类的 `using`（换 Kernel 落盘方式时同步更新 host workspace 大小）
- 先评估「头号优化：消除整块 C 的 HBM 往返」，再做 TileShape/Swizzle 微调
- 用 msprof 逐 shape 记录 before/after 与瓶颈（HBM/MTE2/Cube/同步）；对照 torch 基准判定达标

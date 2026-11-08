---
name: ops-performance-tuning
description: Compile, profile, diagnose, optimize, and compare Ascend NPU operators across CANN versions and A2/A3/A5 for Ascend C, CATLASS, Triton-Ascend, TileLang-Ascend, PyPTO, and SHMEM/MC2. Use when an operator already has a runnable implementation and the user asks for msOpProf collection, bottleneck analysis, source-level tuning, or a reproducible before/after performance report. Do not use as the primary workflow for operator creation, migration, or unresolved correctness failures.
---

# Ascend Operator Performance Tuning

对可运行且精度通过的昇腾算子执行“环境与版本对齐 → 编译 → 基线 → msOpProf 采集 → 瓶颈判定 → 单变量优化 → 前后对比”。所有性能结论来自目标环境实测；知识库案例只提供候选机制，不替代当前算子的 profiling 证据。

使用本技能时，咨询和执行任务都必须先完成资料查询：在代码仓 https://gitcode.com/Ascend/msopprof 查询 msopprof 与 msopprof simulator 使用资料。下文及 references 中的参数、能力边界和命令模板按返回的相关正文核验后使用；查询失败时查找本地相关工具或本地资料参考用法回答和命令执行。

## 任务边界

- 已有源码、构建入口和测试入口，用户要求性能分析或调优：执行本流程。
- 精度未通过、运行崩溃或 kernel 挂起：停止性能调优，转交精度或运行时调试流程。
- 从零开发、CUDA 迁移或接口设计：先完成开发流程，算子可运行后再使用本 Skill。
- 只要求解释 profiling 指标：只执行相应诊断，不修改源码。

## 必须解析的输入

从用户信息、工程和当前环境依次获取；只有缺失字段会改变执行路径时才询问。

| 字段 | 获取位置 | 缺失时处理 |
|---|---|---|
| 工程根目录、算子名、DSL | 用户输入、构建文件、源码后缀 | 无法识别构建入口或 DSL 时询问 |
| kernel 清单 | 注册信息、运行日志、`OpBasicInfo.csv` | 多 kernel 场景必须形成完整清单 |
| CANN/driver/firmware、SoC | 版本文件、`npu-smi`、ACL/torch_npu | 不明确时只做离线审查，不声称上板结果 |
| shape/dtype/format/属性 | 测试配置、调用入口 | 禁止用临时 smoke shape 替代目标用例 |
| 正确性命令与容差 | 工程现有测试 | 禁止自创业务容差 |
| 性能命令、warmup、repeat | 工程 benchmark | 无等价标杆时只做前后自对比 |

## 渐进式披露规则

不要一次性加载整个 `references/`：

1. 识别 DSL 和算子类型后，只读取匹配的 `compile-*.md`。
2. 准备采集时读取 [msOpProf 采集指南](references/profile/profile-msopprof.md)。
3. 根据已采集字段选择一个或多个 `diagnose-*.md`；没有证据时不得先加载案例猜瓶颈。
4. Bound 确认后读取 [优化技术索引](references/optimize/optimize-index.md)，再加载命中的单个技术文件。
5. 最后读取 [案例路由](references/case-routing.md)，按 DSL、算子类型、SoC 和 Bound 选择最多三个同型案例。

## 执行流程

### Step 0：建立隔离产物目录

不覆盖用户基线。源码修改放在用户允许的分支或副本；运行产物写入被忽略的目录：

```text
tuning_artifacts/<operator>/
├── environment.txt
├── scope.json
├── baseline/
├── round-01/
└── comparison.md
```

`scope.json` 至少记录：`operator`、`dsl`、`repo_commit`、`cann_version`、`soc`、`device_id`、`shapes`、`dtypes`、`formats`、`kernel_names`、三类执行命令、`warmup`、`repeat` 和 `baseline_kind`。

### Step 1：环境与版本对齐

```bash
bash <skill_dir>/scripts/env_check.sh --mode <board|sim> --cann-path <cann-path>
```

把输出保存到 `environment.txt`，并确认：

1. 源码 branch/tag 与 CANN/OPP 版本兼容；不匹配时切换对应 release 或记录 `source_mismatch=true`。
2. A2/A3/A5 编译目标来自目标仓文档、本机工具链或 `build.sh --help`，不按机器昵称猜测。
3. 使用 `msprof op --help` 或 `msopprof --help` 记录当前版本真实支持的参数、指标和 simulator/MC2 能力。
4. 选择健康且空闲的 NPU，记录设备 ID、频率和同卡负载。
5. **通信/多 rank 算子**：`rankNum ≤ 可用空闲设备数` 在本步判定，不满足直接标记 `BLOCKED`（host 侧 `deviceId = rankId` 的样例每 rank 独占一个物理设备）。
6. **Triton-Ascend 算子**：可用性门禁是"最小 triton kernel 上板跑通"（vector add 级），不是 `import triton` 成功；版本配套与 207000 排查见 [compile-triton.md §2.7](references/compile/compile-triton.md)。
7. **数据/校验脚本的 Python 依赖**：逐个 `python3 -c "import <mod>"` 核对 gen_data/verify 脚本的真实 import（常见缺口：torch、en_dtypes、ml_dtypes、pandas），缺失时在产物目录建隔离 venv，不污染系统环境。

缺 simulator 但执行上板路径时为非阻塞。没有可用 NPU 时只完成编译、路由和命令生成，不生成性能数字。

### Step 2：按 DSL 编译并通过精度门禁

| DSL/框架 | 唯一入口 |
|---|---|
| Ascend C / CANN 官方算子仓 | [compile/compile-ascendc.md](references/compile/compile-ascendc.md) |
| CATLASS | [compile/compile-catlass.md](references/compile/compile-catlass.md) |
| Triton-Ascend | [compile/compile-triton.md](references/compile/compile-triton.md) |
| TileLang-Ascend | [compile/compile-tilelang.md](references/compile/compile-tilelang.md) |
| PyPTO | [compile/compile-pypto.md](references/compile/compile-pypto.md) |
| SHMEM / MC2 | [compile/compile-shmem.md](references/compile/compile-shmem.md) |

保存完整构建命令、退出码和产物位置。profiling 构建保持 Release 优化；需要源码映射时只增加目标编译器支持的调试信息。运行工程原有正确性全集并记录容差、最大绝对/相对误差和失败用例。任一目标用例失败即停止性能调优。

### 精度保障机制（全流程三道门禁 + 校验链审计）

精度不是"最后复测一次"，而是三次强制门禁，任何一道不过即停止或回滚：

1. **进入门禁（Step 2）**：基线建立前跑工程正确性全集，容差只能来自工程现有测试，禁止自创业务容差；任一目标用例失败即转精度调试，不进入性能环节。
2. **每轮门禁（Step 7）**：每轮单变量修改后**先跑完整精度再跑同口径性能**——精度失败该轮直接回滚，该轮性能数字不得出现在报告结论中。
3. **结论门禁（Step 8）**：`delta_report.py` 在脚本层强制校验前后 `precision=pass`，否则拒绝生成对比报告；`result_saver.py` 落盘 `mismatch`/`maxAbsErr`/`maxRelErr` 误差指纹，前后精度数字必须同量级。

**校验链本身必须先审计再采信**（实测踩坑：某 FIA 案例官方校验脚本对 NaN 位型退化为"全一致即 pass"，NaN 掩码是死代码）：

- 跑通校验脚本 ≠ 校验有效。确认：golden 生成链在当前软件栈真实可用（标杆 aclnn 拒绝该场景即断裂）；比对方式是位级还是数值转换（数值转换可能先销毁 NaN/Inf）；掩码/跳过分支是否真的执行。
- 校验链断裂或退化时：停止性能调优，改用语义仿真 golden（CPU 参考）并保持工程原容差，补充无异常位型的辅助数据集，处置过程写入报告。

**改动按语义风险分级审查**：

- **语义保持类**（分核/blockDim、双缓冲、搬运合并、同步删减、调度顺序）：数学结果不变，常规精度门禁即可。
- **语义变更类**（算法替换、近似公式、dtype/量化精度转换、归约顺序改变可能影响浮点结合律）：除门禁外，必须在候选方案中写明精度风险与额外验证用例（边界值、异常位型、大 shape），收益结论需标注精度代价。

### Step 3：建立不可变基线

固定源码基线、软件栈、SoC、设备、频率、shape、dtype、format、物理 padding、TilingKey、blockDim、warmup、repeat 和计时方法。优先使用设备 event 或工程正式 benchmark；msOpProf 只用于结构诊断，短 kernel 不得用 profiler 插桩耗时替代 event 基线。

计时口径的边界情形（实测补充）：

- **工程无 benchmark/计时设施**（cann-samples 样例普遍如此）：允许在产物目录的工程副本上给 host 侧补 aclrtEvent 计时 harness（warmup/repeat 固定），属测量设施而非优化变量；模板与归类规则见 [benchmark-harness.md](references/profile/benchmark-harness.md)。原始基线源码必须先备份。
- **长 kernel（ms 级）且工程无 event 设施**：允许用 msopprof `OpBasicInfo` Task Duration 作基线（result_saver `--timing-method msprof_task_duration`），报告中注明口径；工程 README 的参考数字同口径时才可对比。
- **短 kernel（µs 级单 launch）**：launch 开销会掩盖 kernel 级收益（wall 口径下任何优化都不可归因）。用 stream 内多 launch 单 event 对计时；仍不可归因时以 profiler device duration 作辅助口径并注明，不要按 wall 噪声判回滚或宣称收益。
- **冷跑/稳态差异**：首跑含初始化与缓存预热（实测可差 25%），固定 warmup 剔除；稳态 ≥3 次取中位，run 间噪声 >5% 时小于噪声幅度的收益不得归因。
- **工程自带 profiler 对比框架**（如 torch_npu op_summary 的 torch vs triton benchmark）：视为工程正式 benchmark，按本节优先级采信。

```bash
python3 <skill_dir>/scripts/result_saver.py \
  --op <operator-or-case> --variant baseline --mode board --soc <a2|a3|a5> \
  --precision pass --kernel-avg-us <value> --timing-method event \
  --baseline-kind <system|self_before_after> --cann-version <version> \
  --repo-commit <baseline-commit> --device-id <id> \
  --shape <shape-or-case-id> --dtype <dtype> --format <format> \
  --tiling-key <key> --block-dim <n> --warmup <n> --repeat <n> \
  --msprof-dir <path-or-empty> --output tuning_artifacts/<operator>/baseline
```

没有等价系统算子时使用 `baseline_kind=self_before_after`，不得构造 builtin 对比。

### Step 4：采集 msOpProf

读取 [profile/profile-msopprof.md](references/profile/profile-msopprof.md)，先探测本机帮助再生成命令。必须：

1. 用 kernel 过滤条件和结果清单确认所有目标 kernel 均被采集。
2. 保存 `OpBasicInfo.csv` 与本机支持的基础 Pipe/Memory 指标。
3. A2/A3 可优先评估 `MemoryDetail`、`TimelineDetail`；A5 可优先评估 `PipeTimeline`、`PcSampling`，但只使用本机帮助明确支持的项。
4. MC2/多 rank 仅在本机明确支持时使用 `msprof op`，否则回退完整 `msprof`。
5. 保存采集命令、输出目录、kernel 过滤、launch 次数和失败项。

### Step 5：证据化判定 Bound

按已有数据读取：

- 核间长尾或 block 利用率：[diagnose/diagnose-occupancy.md](references/diagnose/diagnose-occupancy.md)
- Compute/Memory/Latency 分类：[diagnose/diagnose-roofline.md](references/diagnose/diagnose-roofline.md)
- L2/GM 流量与工作集：[diagnose/diagnose-l2-cache.md](references/diagnose/diagnose-l2-cache.md)
- MTE/Vector/Cube/Scalar/FixPipe 流水：[diagnose/diagnose-pipeline.md](references/diagnose/diagnose-pipeline.md)

有 `PipeUtilization.csv` 时执行：

```bash
python3 <skill_dir>/scripts/bound_analyzer.py \
  --csv <PipeUtilization.csv> \
  --output tuning_artifacts/<operator>/baseline/bound_report.json
```

脚本只做初筛。最终结论必须包含 Bound、CSV/字段/数值/核或 kernel、排除其他 Bound 的反证、置信度和缺失指标。高 busy 必须结合 active bandwidth，区分真实带宽上限与小包、非对齐或同步频繁。

### Step 6：选择同型优化机制

读取 [优化技术索引](references/optimize/optimize-index.md)，只加载命中文档：

| 证据或 DSL | 资料 |
|---|---|
| 切核不均、尾块长尾 | [Ascend C Tiling](references/optimize/optimize-ascendc-tiling.md) |
| MTE2/MTE3、小包或非对齐 | [数据搬运](references/optimize/optimize-data-copy.md) |
| L2/UB/L1/L0 复用不足 | [存储层次](references/optimize/optimize-memory-hierarchy.md) |
| Pipe 气泡或同步过密 | [流水优化](references/optimize/optimize-pipeline.md) |
| Scalar/API 热点 | [API 使用](references/optimize/optimize-api-usage.md) |
| 多步融合 Vector、MemBase 已尽、VF 样例 | [RegBase / SIMD VF](references/optimize/optimize-ascendc-regbase-vf.md) |
| CATLASS / Triton / TileLang | [CATLASS](references/optimize/optimize-catlass.md) / [Triton](references/optimize/optimize-triton.md) / [TileLang](references/optimize/optimize-tilelang.md) |
| PyPTO / SHMEM | [PyPTO](references/optimize/optimize-pypto.md) / [SHMEM](references/optimize/optimize-shmem.md) |

再从 [案例路由](references/case-routing.md) 选择最多三个同 DSL、同数据流、同 SoC 能力且同 Bound 的案例。公开数字只作为来源事实。候选项必须写明对应证据、修改位置、预期指标、架构限制、精度风险、验证命令和回滚条件。

### Step 7：单变量迭代

每轮只实施一个可归因机制或一组不可拆分的原子修改：保存 diff，执行最小改动，以同一命令重编译，先跑完整精度再跑同口径 benchmark，最后补采受影响指标。精度失败、稳定劣化或收益落在噪声内时回滚并记录原因。

**负优化是正常且可处置的**（21 案例实测中出现率约 1/3）：机制与瓶颈不匹配、容量/深度联动假设被破坏（tiling 改动后 fault）、同步协议改动死锁、或收益被噪声淹没，都会导致某轮变慢或不可用。本流程用四道机制兜住：

1. **可预防**：候选机制必须有当前算子的 profiling 证据（不是案例数字外推）；单变量保证可归因；原子修改对先二分验证单路径可用性。
2. **可检测**：同口径对比（`delta_report.py` 硬口径校验）+ 噪声带判定（±5% 内不算收益也不算劣化，需加采样轮次）+ 冷跑/稳态区分。
3. **可回滚**：每轮有 diff、基线源码有备份，回滚后必须复跑确认回到基线水平（验证回滚干净），再进入下一轮。
4. **可交代**：回滚的轮次与原因写进最终报告的"保留和回滚的修改"——负优化记录本身是瓶颈证据的组成部分，不是失败。

不硬编码固定轮数。达到目标、候选耗尽、连续两轮无稳定收益或证据显示接近硬件上限时停止。

### Step 8：前后对比

按 Step 3 的完整参数保存优化后结果；`repo_commit` 使用优化后的提交，其余比较口径必须一致。然后执行：

```bash
python3 <skill_dir>/scripts/delta_report.py \
  --baseline <baseline-result.json> --after <optimized-result.json> \
  --output tuning_artifacts/<operator>/comparison.md
```

最终报告包含环境与源码指纹、完整用例表、baseline/optimized/Delta/speedup/精度、Bound 与关键指标变化、保留和回滚的修改、官方文档或 PR 及适用边界。无法采集或未验证的内容标记为 `partial` 或 `dry_run`。

## 失败分流与禁止事项

编译、运行或采集失败时读取 [troubleshooting.md](references/troubleshooting.md)。禁止：精度失败时继续调优；未审计校验链即采信精度结论；跨软件栈、SoC、频率、shape、dtype 或 TilingKey 比较；无证据宣称 Bound；照搬案例加速比；一次修改多个无关机制；劣化或噪声内收益的轮次不回滚、不记录；只展示最快样本或提升 case；批量加载 `references/cases/`。

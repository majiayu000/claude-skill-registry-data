---
name: cinderx-evidence-table
description: Use when 建立或审查单用例 E1–E9 根因证据表，判定穿刺与优化价值是否可信。
---

# CinderX Evidence Table

证据表是单用例深钻的唯一产物。一张表 9 行（E1–E9），每行三段式：What（必贴客观证据）/ Verdict（一句结论）/ Gate（证据足够硬条件）。任一段不满足 Gate，证据表标记 `evidence_gap` 或 `verdict_missing`，**流程停下来补证据**，不跳过。

证据表本身不负责"先钻哪个用例"——那是 workflow 层的选例动作。证据表从 E1 起假设用例已选定。

## E1–E9 结构

| # | 证据段 | What（必贴） | Verdict | Gate（证据闭环判据） |
|---|--------|--------------|---------|----------------------|
| E1 | 性能基线 | 双平台 wall clock、speedup、置信区间、样本数、运行环境句柄 | 该用例是否存在显著且稳定的平台差距 | 差距 > 噪声带（默认 3%）且置信区间不含 0 |
| E2 | 用例画像 | 用例内容描述、autojit 函数形状（签名、热点循环结构） | 该用例的优化价值定位（compute-bound? memory-bound? branchy?） | 函数形状与 perf 热点吻合 |
| E3 | HIR 分布 | HIR 节点分布表（按 pass 或 node kind 统计）、双平台 HIR 是否同构 | 差异是否源于编译期（HIR 层） | 双平台 HIR 形态已比对，差异点已定位到节点级 |
| E4 | LIR + wall clock | LIR/机器码段、调用计数、wall clock 拆解（该段占总时间比） | 差异是否源于 codegen（LIR 层） | wall clock 拆解能与 LIR 段对齐，热点段已锁定 |
| E5 | 差异点 | bb 维度整体差异 或 单条机器码级差异，双平台逐指令对齐 | 具体差异指令/序列是什么 | 双平台指令已逐条对齐，差异序列 ≤ N 条可枚举 |
| E6 | 根因下钻 | 跨层证据链：LIR→机器码→ISA/指令集→微架构→硬件 | 表面原因之下的真实根因 | 根因已落到 ISA/微架构/硬件某一层，且非表面原因 |
| E7 | 优化方向 | 由根因推出的优化策略（不是猜测） | 该方向能否直接解决 E6 根因 | 策略 ↔ 根因一一对应，无悬空假设 |
| E8 | 穿刺数据 | A/B 验证（baseline=原形态，candidate=优化形态），wall clock + 必要 PMU | 优化是否真的消除差异、是否带来收益 | 穿刺隔离满足 `cinderx-ab-run-slot`，结果可重复 |
| E9 | 优化价值判定 | 净收益（穿刺收益 − 实现成本 − 风险）、通用性、是否进备选 | 该优化项是否进入备选优化项清单 | 收益与成本均有数据支撑，无纯定性结论 |

## E6 根因层级必带工具证据

通用必带（所有平台）：`perf stat` 的 cycles / instructions / cache-references / cache-misses / branch-misses，双平台同口径采集。

| 根因层 | 必带工具输出（缺则 `evidence_gap`） |
|--------|------------------------------------|
| 机器码 | `objdump -d` 反汇编，双平台对齐 |
| ISA/指令集 | 指令选择差异、SIMD/原子/barrier 形态（对照 `cinderx-isa-microarch-compare` 矩阵） |
| 微架构 | `perf stat` 关键计数器（cycles/instructions/cache-miss/branch-miss）、`perf top` |
| 硬件 | PMU 计数器、必要时的 uops.info / llvm-mca 吞吐估算、cache/TLB 行为 |

## 指令级采样机制（SPE/IBS）处理原则

指令级精确采样在两平台是**不同机制、都有硬性开启条件**，且具体可用性随平台/内核/权限而变。本节只规定**处理原则**，不绑定任何特定平台的可用性结论——具体某平台能否拿到 SPE/IBS，由运行时探测决定，不预设。

1. **采样可用性是证据链前置判据，非默认前提**。E6 开头先做探测，探测结果本身作为 E6 第一条证据记录：

   - ARM 侧：`perf list | grep arm_spe`，并检查 `/sys/bus/event_source/devices/arm_spe_*/` 是否存在。为空则 SPE 证据不可得，退化为 PMU 计数器 + `perf top`。
   - x86 侧：检查 `/sys/bus/event_source/devices/ibs_op/` 是否存在，并确认权限——IBS 无用户/内核过滤能力，需 `CAP_SYS_ADMIN` 或 `CAP_PERFMON`。无特权则 IBS 证据不可得，退化为 top-down metric group。
   - 探测结果明确"本平台能拿到什么层级的证据、缺什么"。

2. **估算必标置信度**。uops.info / llvm-mca 是吞吐估算而非实测；Zen4/Zen5 无每端口 uops PMU（Saarland port-mapping 论文），ARM 侧 uops.info 不覆盖。证据表必须标注"估算来源 + 置信度"，不能把估算当实测。

3. **不对称证据显式化**。当一侧能拿到指令级采样、另一侧拿不到时，证据表不得直接对比不对称的采样数据。根因下钻以能拿到证据的一侧为锚，对侧只提供 PMU 级证据，并在 Verdict 标注证据不对称带来的根因置信度折扣。

## 失败处理

任一证据段不满足 Gate：

- 标记 `evidence_gap`（What 缺失）或 `verdict_missing`（Verdict 缺失）。
- **停下来补证据**，不进入下一段。
- evidence-analyst 在 E6 有权回退要求 E3–E5 补证据（如指令没对齐回到 E5）。

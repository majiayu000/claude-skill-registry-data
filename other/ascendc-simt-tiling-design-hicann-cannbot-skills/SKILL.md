---
name: ascendc-simt-tiling-design
description: AscendC SIMT 算子切分设计指南。提供 SIMT 算子独有的核数切分、线程数设置、DCache/UB空间分配、模板路由与 tilingKey 分发、workspace 契约方法。SIMT切分与SIMD完全不同（线程级并行 vs 向量级UB切分），本skill聚焦SIMT切分范式。触发：设计SIMT算子Tiling策略、设置SIMT线程数、规划SIMT核数切分、选择SIMT/SIMD模板、规划SIMT workspace、blockDim封顶、DCache 取值范围、SetScheduleMode时。
---

# SIMT 算子切分设计指南

SIMT 算子的切分设计与 SIMD 有本质差异。SIMD 以 UB 数据切分 + Buffer 流水规划为核心；SIMT 以核数切分 + 线程数设置为核心，**不按 UB 容量切分数据、不做 inQueue/outQueue 流水**，但仍需在 UB 中分配 Data Cache（及核内共享 buffer）空间。

> **SIMD 算子 Tiling 设计**请参考 `ascendc-tiling-design` skill。

## SIMT vs SIMD 切分差异速查

| 要素 | SIMD | SIMT |
|------|------|------|
| 多核切分 | 按 UB 单次处理量切分 | 按元素总量切分（ceil(总量/单核最少元素数)） |
| 单核并行 | UB Buffer + 向量指令 | 线程数（`Dim3` 可运行时收缩，上限 `LAUNCH_BOUND` 编译期常量） |
| 数据搬运 | 需显式 Load/Store | 支持直接读写 GM |
| UB 使用 | 全量使用 | 仅核内共享场景使用，DCache >= 32KB |
| Buffer 规划 | inQueue/outQueue/tmpBuf | TBuf（仅在需要共享内存时使用） |

详细设计指南：[references/guide.md](references/guide.md)

## 核心设计要素

### 1. 核数切分策略

- **需求核数** = ceil(输出元素总数 / 每核元素数)；每核元素数 = max(ceil(总量 / 物理核数), 1024)，并对 warp(32) 对齐
- **下发 blockDim** = `SetBlockDim(clamp(需求核数, 1, 物理核数))` —— 需求核数由数据量决定，下发时必须封顶物理核数

### 2. 线程数设置策略

- 默认 1024，最大 2048
- `LAUNCH_BOUND(N)` 必须是 `constexpr` 编译期常量（决定寄存器分配上限）
- `Simt::Dim3(N)` 可为运行时值（tiling 自适应收缩），但必须 ≤ `LAUNCH_BOUND`
- 参考：编译期上限取 2048 作 `LAUNCH_BOUND`，tiling 侧按数据量逐次减半线程数作 `Dim3`

### 3. DCache 与 UB 空间分配

- Data Cache 范围 **32KB~128KB**，由 UB 扣除动/静态内存后反向推导
  （`Data Cache = min(256KB − 静态 − 动态, 128KB)`）
- host 侧设置的是**动态 UB 大小**：`SetDynUBufSize(平台UB − 目标DCache − 静态buffer)`
- 可用 UB 示例 = 256KB − 32KB(DCache 下限) = **216KB**

### 4. 模板路由与 workspace

- 多模板注册按 priority 竞选 `IsCapable()`，SIMT 模板作大号兜底
- tilingKey 按位编码路由决策；**索引位宽自适应**（默认 32 位，`尾轴×行数`/总量超 int32 升 64 位）是其中一维，kernel 侧 `ADDR_T` 模板化编译期分发
- workspace 16MB 系统区打底 + 算子专属区；host-kernel 公式必须逐段一致
- kernel 有 `SyncAll()` 时 tiling 必须 `SetScheduleMode(1)`

## 参考文档索引

| 主题 | 文档 | 关键要点 |
|------|------|---------|
| 基础切分指南 | [guide.md](references/guide.md) | 核数/线程数/DCache、索引位宽自适应、模板路由与 workspace 概览、Tiling 审查清单 |
| 进阶分核策略 | [tiling-advanced.md](references/tiling-advanced.md) | 双任务分核取 max、线程自适应收缩、按最大工作量估核、平台参数动态化（基础封顶/下限见 guide.md） |

> **按需加载**：一个子问题最多展开 2~3 篇 reference。

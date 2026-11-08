---
name: mstx-report-soft-sync
description: 分析 AscendC 算子中自实现的软同步代码，判断其所属同步语义（核间 barrier/set-wait、卡间 barrier/signal），并接入 mssanitizer 的 Sanitizer 接口（sanitizer_report.h）上报软同步语义，避免 racecheck 对软同步误报。触发：算子存在自实现软同步（GM 地址轮询、flag 计数、跨核/跨卡信号等）需要配合 mssanitizer 检测、需要上报软同步语义、需要判断某段同步代码属于哪种同步语义时。
---

# 算子软同步语义分析与 mssanitizer 上报

## 概述

mssanitizer 的 racecheck 会检测访存竞态。算子中由用户自行实现的软同步（轮询 GM 地址 / 写 flag / 计数等）会被 racecheck 误判为竞态，需要通过 `sanitizer_report.h` 提供的 `Sanitizer` 接口上报同步语义，让检测器识别这些软同步、跳过误报。

- 接口头文件：`$ASCEND_HOME_PATH/tools/mssanitizer/include/sanitizer_report.h`
- 完整接口签名、结构体字段、参数说明见 [references/sanitizer-interface.md](references/sanitizer-interface.md)

## 软同步语义分类

| 语义 | 场景 | 上报结构体（`Sanitizer::`） |
|------|------|------------------------------|
| 核间 barrier | 同卡多个核到达同步点后一起继续 | `MstxCrossCoreBarrier` |
| 核间 set/wait | 核 A 发信号，核 B 等待后才继续 | `MstxCrossCoreSetFlag` / `MstxCrossCoreWaitFlag` |
| 卡间 barrier | 跨卡所有核到达后继续（隐含全流水+核间 barrier） | `MstxCrossNpuBarrier` |
| 卡间 signal | 基于 GM 地址写值 + 轮询该地址满足条件 | `MstxSignalSet` / `MstxSignalWait` |

## 处理流程

### 步骤 1：识别自实现软同步

**排除项（无需上报）**：

- 直接调用已封装的软同步接口，如 `aclshmem_signal_wait_until`、`aclshmemx_signal_op`、`aclshmem_barrier_all` 等（这些内部已上报）。
- 硬件同步（非软同步）：`SetFlag`/`WaitFlag`/`PipeBarrier`（核内事件同步）、`CrossCoreSetFlag`/`CrossCoreWaitFlag`（硬件核间同步）。

**识别特征（自实现软同步，需上报）**：

- GM 地址轮询：`while (*(__gm__ T*)addr != value)`、`while (ReadGmByPassDCache(ptr) != target)`
- 写 flag / 计数：`*(__gm__ T*)addr = value`、`WriteGmByPassDCache(ptr, v)`、`AtomicAdd(flag, n)`
- 配合 `dcci_cacheline(s)` 显式刷新 dcache 的轮询/写值

### 步骤 2：判断同步语义

按三个维度归类：

1. **参与方**：核内（同核流水）→ 跨核（同卡不同 core）→ 跨卡（不同 device/rank）。
2. **同步方式**：barrier（所有参与方到达才释放）→ set/wait（一方发布、另一方等待）→ signal（基于 GM 地址写值+轮询）。
3. **happens-before 粒度**：决定能否消除「数据区」的写-读误报（关键！）。

对照「软同步语义分类」表确定上报结构体。

**语义选择关键经验**（来自 allgather 实测）：

- **同卡多核软同步 → 用核间 barrier（`MstxCrossCoreBarrier`）或核间 set/wait（`MstxCrossCoreSetFlag`/`WaitFlag`）**。其 happens-before 是**全局**的（barrier 之前所有写 → 之后所有读），能消除「数据区」写-读误报。
- **跨卡软同步 → 用卡间 signal（`MstxSignalSet`/`Wait`）或卡间 barrier（`MstxCrossNpuBarrier`）**。`signal` 的 happens-before **按地址**（文档「仅与保存信号的地址有关」），只消除 signal 地址（flag 区）的误报，**无法跨到数据区**——若误报发生在「生产者写数据 vs 消费者读数据」这类数据区竞争，signal 上报无效，应改用 barrier 语义。

判断方法：先看 racecheck 误报的**地址是否等于软同步 flag 地址**（是→signal 即可；否、且为数据区写-读→barrier/set-wait）。

### 步骤 3：先封装宏，再插入上报

为避免每个同步点重复构造结构体，仿照 shmem 内部 `shmemi_mstx_report.h` 的写法，**在算子文件顶部先定义一组宏**封装 `sanitizer_report.h` 的 `Sanitizer::` 接口（不依赖 shmem 内部头文件，便于移植到其他算子仓）。宏名改用 `MSTX_SOFT_SYNC_` 前缀，与 shmem 内部的 `MSTX_*` 宏区分，避免编译期冲突：

```cpp
#include "sanitizer_report.h"

#ifdef __MSTX_DFX_REPORT__
#define MSTX_SOFT_SYNC_FUSE_SCOPE_START() Sanitizer::SanitizerFuseScopeStart()
#define MSTX_SOFT_SYNC_FUSE_SCOPE_END() Sanitizer::SanitizerFuseScopeEnd()
#define MSTX_SOFT_SYNC_SIGNAL_SET_REPORT(addr_, val_)     \
    do {                                        \
        Sanitizer::MstxSignalSet soft_sync_set__{};  \
        soft_sync_set__.addr = (uint64_t)(addr_);    \
        soft_sync_set__.value = (val_);              \
        Sanitizer::SanitizerReport(soft_sync_set__); \
    } while (0)
#define MSTX_SOFT_SYNC_SIGNAL_WAIT_REPORT(addr_, cmp_, val_)        \
    do {                                                  \
        Sanitizer::MstxSignalWait soft_sync_wait__{};          \
        soft_sync_wait__.addr = (uint64_t)(addr_);             \
        soft_sync_wait__.cmpValue = (val_);                    \
        soft_sync_wait__.cmpOp = (Sanitizer::CompareOp)(cmp_); \
        Sanitizer::SanitizerReport(soft_sync_wait__);          \
    } while (0)
#define MSTX_SOFT_SYNC_CROSS_CORE_BARRIER_REPORT(core_num)         \
    do {                                                           \
        Sanitizer::MstxCrossCoreBarrier soft_sync_barrier__{};     \
        soft_sync_barrier__.usedCoreNum = (core_num);              \
        Sanitizer::SanitizerReport(soft_sync_barrier__);           \
    } while (0)
#else
#define MSTX_SOFT_SYNC_FUSE_SCOPE_START()
#define MSTX_SOFT_SYNC_FUSE_SCOPE_END()
#define MSTX_SOFT_SYNC_SIGNAL_SET_REPORT(addr_, val_)
#define MSTX_SOFT_SYNC_SIGNAL_WAIT_REPORT(addr_, cmp_, val_)
#define MSTX_SOFT_SYNC_CROSS_CORE_BARRIER_REPORT(core_num)
#endif
```

然后在每个同步点插入：

```cpp
// set 侧（写 flag / 发信号）
MSTX_SOFT_SYNC_FUSE_SCOPE_START();
/* user-defined 软同步逻辑：写 flag、put、AtomicAdd 等 */
MSTX_SOFT_SYNC_FUSE_SCOPE_END();
MSTX_SOFT_SYNC_SIGNAL_SET_REPORT(flag_addr, written_value);

// wait 侧（轮询 flag / 等信号）
MSTX_SOFT_SYNC_FUSE_SCOPE_START();
/* user-defined 软同步逻辑：while 轮询 */
MSTX_SOFT_SYNC_FUSE_SCOPE_END();
MSTX_SOFT_SYNC_SIGNAL_WAIT_REPORT(flag_addr, Sanitizer::CompareOp::EQ, expected_value);
```

要点：

- `SanitizerFuseScopeStart()` / `SanitizerFuseScopeEnd()` 包裹的自定义软同步指令不会被 racecheck 检测，`SanitizerReport(record)` 上报同步语义。
- signal 的 set/wait 通过 `addr` 配对：对称内存下 set 方写入的地址与 wait 方轮询的地址数值相同。
- `(uint64_t)` 强转兼容 `GM_ADDR` 的指针/整型两种底层类型。
- 宏受 `__MSTX_DFX_REPORT__` 门控：非 mssanitizer 构建时为空，不影响普通编译。其余语义（barrier、set/wait）可仿照同一模式扩展对应宏。

## 参考资料

- [references/sanitizer-interface.md](references/sanitizer-interface.md) - Sanitizer 接口签名、结构体字段、CompareOp 枚举、参数说明
- [references/recognition-examples.md](references/recognition-examples.md) - 自实现软同步识别与归类的典型样例

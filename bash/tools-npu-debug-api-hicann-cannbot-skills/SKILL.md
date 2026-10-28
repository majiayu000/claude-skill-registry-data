---
name: tools-npu-debug-api
description: >-
  AscendC 调试工具接口使用说明，涵盖 printf、assert/ascendc_assert、__trap、
  asc_dump、clock 和 asc_time_stamp 的接口选择、调用方式与配置要求。
  当用户调试 AscendC Kernel 代码，需要定位精度偏差、执行路径或异常条件问题，
  查看中间数据、测量局部执行周期、记录时间戳，或排查调试输出缺失、截断及行为异常时触发。
---

# AscendC 核函数调试接口

提供 AscendC 核函数调试接口的选型、调用示例和配置说明，用于获取中间数据、标量值、条件状态和时间信息。

## 适用场景

- **精度问题**：观察中间张量，与相同阶段、索引的参考值对照，辅助判断偏差位置。
- **标量与执行路径**：查看索引、有效元素数、分支条件和指定核/线程的执行情况。
- **异常条件**：添加断言或在受支持的路径中显式中断，暴露异常状态。
- **时间观测**：记录阶段时间戳或读取局部周期计数。
- **调试接口异常**：解释输出缺失、截断、数据转储异常及相关模式、开关、容量限制。

## 功能

### 接口选择

| 观测目标 | 接口 | 主要功能与限制 |
| --- | --- | --- |
| 确认执行路径或查看少量标量值 | `printf` / `AscendC::printf` | 输出格式化文本；不自动遍历张量或校验结果 |
| 检查条件并在失败时触发异常 | `assert` / `ascendc_assert` | 诊断信息和自定义消息支持因模式而异；不能替代始终有效的边界检查 |
| 在支持的 SIMT 路径中显式中断核函数 | `__trap` | 需在调用前判断条件、记录上下文；不是通用的 SIMD 异常接口 |
| 定位精度偏差，查看中间张量或片上缓冲区内容 | `asc_dump_*` / `asc_dump` | 按地址空间、数据类型和元素数量转储数据；不推断内存分配长度或比较参考结果 |
| 读取周期计数，供计算或写回全局内存（GM） | `clock` | 返回 `uint64_t` 周期计数；不自动计算耗时、输出记录或等待异步操作完成 |
| 记录可解析的 SIMD 时间点 | `asc_time_stamp` | 输出带自定义标识的结构化时间戳；不自动配对记录或计算区间耗时 |

## 使用约束

- **版本与平台**：接口支持取决于 CANN/devkit 版本、SoC/编译架构、SIMD/SIMT/VF 模式，以及 CPU/仿真/NPU、直接调用/入图等执行方式。声明、重载和参数范围以目标版本的 `asc-devkit/docs/zh/api/Utils-API/tuning_interface/`、公开头文件和示例为依据；参考资料仅代表其标注基线，不能将编译通过视为运行支持。
- **插桩与配置**：仅添加观测所需的调试代码，保持算法、tiling 和同步逻辑不变；控制核、线程和输出量。配置模板是片段，不能覆盖现有 `acl.json` 的其他字段。
- **内存访问**：访问前确认指针有效性、实际元素数和线程索引范围。`dump_size` 不得超过实际元素数，不得用于试探未知内存长度；按目标版本文档计算 32 字节补齐后的容量消耗。
- **断言与开关**：`NDEBUG` 会使断言失效；`ASCENDC_DUMP=0` 会关闭依赖 Dump 的调试输出，相关断言行为需结合接口和模式核对。不得依赖可被关闭的断言防止越界。
- **正确性判断**：打印和数据转储不能替代参考结果对比或流水线同步。不得为使输出出现而放宽精度阈值、删除真实边界检查或改变算法；打印出现或增加同步后症状消失，不能单独证明问题已修复。
- **调试开销**：插桩会影响执行时序与性能。`GlobalTensor::GetValue/SetValue` 可用于调试时的单点观测，不应替代生产代码中的批量数据搬运；批量搬运应使用适用的 `DataCopy`/`DataCopyPad` 接口。
- **证据范围**：观测数据需对应同一输入、阶段和索引；没有中间参考值时不能仅凭打印判断精度正确。静态扫描不证明编译或 NPU 实测通过。

## 参考资料

按接口或问题类型选择阅读，无需默认加载全部资料。

- [接口快速参考](references/debug_api_quickref.md)：六类接口对比与选择依据。
- [格式化输出](references/printf.md)：`printf` 调用和 FIFO 容量。
- [断言与显式中断](references/assert_and_trap.md)：`assert`、`ascendc_assert` 和 `__trap` 的模式差异。
- [数据转储](references/asc_dump.md)：地址空间、数据类型、对齐与容量。
- [周期计数与时间戳](references/clock_and_timestamp.md)：`clock` 和 `asc_time_stamp` 的调用与限制。
- [平台与编程模式支持矩阵](references/platform_matrix.md)：参考基线下的支持范围。
- [观测结果与限制](references/observation_notes.md)：精度观测的证据范围及常见异常影响因素。

## 模板与脚本

- [调试检查清单](assets/debug_api_checklist.md)：接口与执行约束检查项。
- [核函数调试模板](assets/kernel_debug_template.asc)：SIMD 调试片段及默认关闭的 SIMT VF 中断示例；不是完整可运行工程。
- [调试配置模板](assets/acl.json.debug.template)：`acl.json` 相关配置示例。

在本技能目录下执行以下命令，对核函数源文件进行静态扫描；将示例路径替换为实际路径：

```bash
python3 scripts/scan_debug_apis.py --json path/to/kernel.asc
python3 scripts/scan_debug_apis.py --fail-on-excluded path/to/kernel.asc
```

脚本仅进行文本级检查，不过滤注释、字符串或未启用的预处理分支，也不解析间接包含的头文件。报告中的 `supported` 仅表示本技能覆盖的接口类别，不代表目标平台支持；`missing_headers` 是待核实提示。退出码：正常扫描为 `0`，启用 `--fail-on-excluded` 且命中范围外接口为 `1`，文件读取失败为 `2`。结果不能替代编译、NPU 运行或目标版本 API 文档核对。

评测场景见 [evals.json](evals/evals.json)。关键词检查仅用于辅助筛选，需结合 `expected_output` 审查结论、证据和实际操作；不得将关键词命中视为行为验证通过。

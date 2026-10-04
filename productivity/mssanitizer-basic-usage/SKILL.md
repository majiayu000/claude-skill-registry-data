---
name: mssanitizer-basic-usage
description: '昇腾AscendC算子异常检测工具（msSanitizer）。检测内存越界、内存泄漏、数据竞争、未初始化读取、同步异常等缺陷。触发关键词：mssanitizer、sanitizer、检测工具、内存检测、竞争检测、初始化检测、同步检测'
---

# msSanitizer 昇腾算子异常检测工具

本skill用于辅助用户完成mssanitizer检测任务。包括完成前置编译适配动作、系统化检测算子内存、竞争、初始化和同步等场景问题、生成初版异常分析报告、针对报告排查误检、修复算子，并给出最终报告。

本skill支持华为**官方算子库/样例库算子**和**自定义算子**两种运行模式。正式进入工作流程前请判断目标算子是否位于官方算子库git项目下，如是则选择对应代码仓检测流程运行，否则按照自定义算子检测流程运行。

支持的所有官方算子库/样例库目录如下：

| 代码仓 | 简述 |
|------|------|
| [ops-transformer](https://gitcode.com/cann/ops-transformer)  | CANN算子库中提供transformer类大模型计算的进阶算子库 |
| [ops-nn](https://gitcode.com/cann/ops-nn) | CANN算子库中提供神经网络计算能力的高阶算子库 |
| [ops-math](https://gitcode.com/cann/ops-math) | CANN算子库中提供数值计算的基础算子库 |
| [ops-cv](https://gitcode.com/cann/ops-cv) | CANN算子库中提供图像处理、目标检测等能力的高阶算子库 |
| [asc-devkit](https://gitcode.com/cann/asc-devkit) | 昇腾AI处理器专用的算子程序开发语言AscendC标准库 |
| [catlass](https://gitcode.com/cann/catlass) | CANN昇腾算子模板库，是一个聚焦于提供高性能矩阵乘类算子基础模板的代码库 |
| [cann-samples](https://gitcode.com/cann/cann-samples) | CANN官方AscendC样例库（SIMT/量化/FlashAttention等story式教学样例） |
| [triton-ascend-kernels](https://gitcode.com/Ascend/triton-ascend-kernels) | 基于Triton-Ascend的高性能Triton算子库（gemm/attention/norm/moe等） |
| [shmem](https://gitcode.com/cann/shmem) | 昇腾共享内存通信库（对称内存/跨卡通信），含allgather等通信算子样例 |

## 1. 工具概述

msSanitizer（MindStudio Sanitizer） 是面向昇腾 AI 处理器的运行时异常检测工具。工具包含四个检测子功能：

| 子工具 | 命令参数 | 检测内容 |
|--------|----------|----------|
| 内存检测 | `--tool=memcheck`（默认） | 非法读写、多核踩踏、非对齐访问、内存泄漏、非法释放、分配内存未使用 |
| 竞争检测 | `--tool=racecheck` | WAW/WAR/RAW 数据竞争（核内流水间/流水内、核间、卡间） |
| 未初始化检测 | `--tool=initcheck` | 读取未初始化内存导致的脏数据问题 |
| 同步检测 | `--tool=synccheck` | SetFlag/WaitFlag 未配对、冗余指令、算子卡死 |

msSanitizer 可在 Kernel 直调 (`<<<>>>`)、aclnn API 调用、PyTorch 框架接入、Triton 算子等多种场景使用。

### 1.1 核心能力参数

| 参数 | 作用 | 取值 | 必选 |
|------|------|------|------|
| `-t`, `--tool` | 指定检测子工具（可多次指定组合启用） | `memcheck`（默认）、`racecheck`、`initcheck`、`synccheck` | 否 |
| `--leak-check` | 开启内存泄漏检测 | `yes` / `no`（默认） | 否 |
| `--check-unused-memory` | 开启分配内存未使用检测 | `yes` / `no`（默认） | 否 |
| `--check-cross-npu-races` | 开启卡间竞争检测 | `yes` / `no`（默认） | 否 |

### 1.2 其他可选参数

| 参数 | 作用 | 取值/示例 | 默认值 |
|------|------|------|--------|
| `-v`, `--version` | 查询工具版本 | - | - |
| `-h`, `--help` | 输出帮助信息 | - | - |
| `--log-file` | 检测报告输出到指定文件 | `{file_name}`（仅支持数字、字母、`-` `.` `/` `_`） | 输出到控制台 |
| `--log-level` | 检测报告输出等级 | `info` / `warn`（默认）/ `error` | `warn` |
| `--kernel-name` | 只检测指定名称算子（支持模糊匹配） | `--kernel-name="add"` | 检测所有算子 |
| `--block-id` | 只检测指定 block（单 block 调试模式） | `0`~`200` | 检测所有 block |
| `--cache-size` | 单 block 可申请的 GM 内存大小（MB） | `1`~`8192`（单 block）；多 block 上限 `24×1024/block数` | `100` |
| `--full-backtrace` | 显示 AscendC API 内的完整调用栈 | `yes` / `no`（默认） | `no` |
| `--demangle` | 函数名 demangle 显示模式 | `full`（默认）/ `simple` / `no` | `full` |
| `--padding` | GM 内存安全区长度（字节） | `32`~`1024` | `32` |
| `--max-debuglog-size` | 调试日志单文件大小上限（MB） | `1`~`10240` | `1024` |
| `--check-device-heap` | 使能 Device 侧内存检测 | `yes` / `no`（默认） | `no` |
| `--check-cann-heap` | 使能 CANN 软件栈内存检测 | `yes` / `no`（默认） | `no` |

> **参数组合规则**：
> - 多个 `-t` 可组合启用，如 `mssanitizer -t memcheck -t racecheck ./app`
> - 开启子选项（如 `--leak-check=yes`）会自动启用对应的主检测功能
> - `--check-device-heap` 和 `--check-cann-heap` 不能同时启用
> - 启用 Device/CANN 堆检测后不再对 Kernel 内部检测

### 1.3 本skill的目录组织结构

```text
mssanitizer-basic-usage/
├── SKILL.md                              // 本skill主文件
├── scripts/
│   ├── run_mssanitizer.py                // 一键运行四种检测，生成原始报告
│   └── parse_mssanitizer_report.py       // 解析并合并原始报告，生成结构化 .md 分析报告
└── references/
    ├── official_workflow.md              // 官方算子工作流与架构类型参数（各代码仓编译/部署/运行检测步骤）
    ├── alarms.md                         // 告警大全：所有告警类型的输出格式、参数含义及触发条件
    ├── sample_memcheck/                  // 内存越界检测样例（含异常注入代码和修复说明）
    ├── sample_racecheck/                 // 数据竞争检测样例
    ├── sample_initcheck/                 // 未初始化读取检测样例
    └── sample_synccheck/                 // 同步异常检测样例
```

### 1.4 检测产物位置

检测命令在算子仓库根目录下执行，产物统一落位如下：

| 产物 | 位置 |
|------|------|
| 运行明细日志 | `<仓库根>/mindstudio_sanitizer_log/mssanitizer_<时间戳>_<pid>.log`（mssanitizer 自动生成） |
| 检测输出 result.log | `<仓库根>/result.log`（手动运行时 `> result.log 2>&1` 重定向） |
| 原始检测报告 | `--output-dir` 指定的算子目录：`mssanitizer_origin_<tool>_<时间戳>.txt` |
| 最终分析报告 | 与原始报告同目录：`mssanitizer_analysis_<时间戳>.md` |

> `[mssanitizer] logging to file:` 行指明本次运行对应的明细日志文件，排查报错详情时按此定位。

### 1.5 路径约定

本 skill 内所有 `scripts/`、`references/` 等相对路径均以**本 skill 根目录**（SKILL.md 所在目录）为基准，如 [scripts/run_mssanitizer.py](scripts/run_mssanitizer.py) 即 `<skill根>/scripts/run_mssanitizer.py`。命令行示例中的 `<skill根>` 需在 agent 实际执行时展开为 SKILL.md 所在目录的**绝对路径**。

---

## 2. 标准工作流（Workflow）

本skill运行的标准工作流如下，请严格按照以下步骤运行，且务必做好进程管理，避免进程残留：

1. **运行环境检查**：确认工具安装，并判断是否是官方算子库/样例库。
2. **编译选项适配**：
    - 官方算子库/样例库：按照 [references/official_workflow.md](references/official_workflow.md) 中对应仓步骤说明适配编译选项。
    - 自定义算子：全量阅读算子构建工程源码，并在对应位置补充编译选项。
3. **编译部署**：
    - 官方算子库/样例库：按照 [references/official_workflow.md](references/official_workflow.md) 中对应仓步骤说明进行编译和部署。
    - 自定义算子：根据用户提供的算子编译命令进行编译和部署。
4. **运行检测**：
    - 官方算子库/样例库：按照 [references/official_workflow.md](references/official_workflow.md) 中对应仓步骤说明运行算子检测，若用户未提供运行参数，按其中的统一处理原则获取。
    - 自定义算子：根据用户提供的命令进行算子检测。
5. **结果分析与修复**：先判断是否有检测开始和结束的有效日志，见[3.4 步骤四](#34-步骤四运行检测)。随后使用解析脚本将原始报告转换为结构化分析报告，统计各工具 ERROR/WARNING 数量；若存在 ERROR，逐条核对源码定位根因、排除误报、修复算子并重新编译检测，直至四种检测全部通过（详见[3.5](#35-步骤五结果分析与修复)）。
6. **生成报告**：清除所有残留进程。按[最终报告规范](#36-步骤六生成报告)补全环境信息、真实命令、核心参数、修改前后检测结果汇总（✅/❌/⚠️）、出现错误原因、实行修改方式。（并有醒目免责声明，AI生成，仅供参考）
7. **清理编译选项**：检测完成后，将临时添加的编译选项移除，恢复原始状态。

## 3. 标准工作流（自定义算子工作流）

本章节详细描述检测工具通用标准工作步骤，用户自定义算子检测流程具体步骤也参考此章节。

### 3.1 步骤一：运行环境检查

1. 工具检查：
执行以下命令确认 mssanitizer 工具正常：

```shell
mssanitizer -v
```

预期输出类似如下的“工具版本号 + commit ID”信息，例如：

```shell
revision:
  mssanitizer 26.0.0-a6db6e381b19cae6b0ca7d65bee8729e763893bd
  msopscommon 338ecff46263e9b41106f4d48ab70d1cd4ac168b
```

若命令不存在或报错，说明 msSanitizer 未安装或环境变量未配置。请参照 [msSanitizer 安装指南](https://gitcode.com/Ascend/mssanitizer/blob/master/docs/zh/install_guide/mssanitizer_install_guide.md) 完成安装后再重新执行检测。

2. 确认算子类型：

检查算子是否位于[官方算子库/样例库目录](#mssanitizer-昇腾算子异常检测工具)项目下，若是则后续步骤 2/3/4 在标准工作流的基础上，还需要参考 [references/official_workflow.md](references/official_workflow.md) 中对应代码仓的说明进行。

### 3.2 步骤二：编译选项适配

为AscendC算子添加 `-g` 和 `-sanitizer`（或 `--cce-enable-sanitizer`，两者等价）两个编译选项，`-g` 用于生成定位信息（文件名、行号、调用栈），`--cce-enable-sanitizer`/`-sanitizer` 用于注入检测桩代码。

> 如果确认算子工程中已经适配编译选项，则此步骤可以直接跳过。
> 仅 AscendC 算子需要添加此编译选项。Triton 算子无需执行此步骤（插桩由环境变量控制，见 [references/official_workflow.md](references/official_workflow.md) 第 7 章）；PyTorch 只是调用/拉起方，kernel 能否加编译选项取决于 kernel 由谁编译，见 [3.2.3 PyTorch 接入场景的插桩口径](#323-pytorch-接入场景的插桩口径)。

#### 3.2.1 场景一：CMake 工程（CMakeLists.txt）

在 Kernel 侧的 CMakeLists.txt 中添加编译选项：

```cmake
# 在算子 CMakeLists.txt 中
target_compile_options(XXX XXX
    ...
    --cce-enable-sanitizer
    -g
    ...
)

# 链接阶段也需添加
target_link_options(XXX XXX
    ...
    --cce-enable-sanitizer
    ...
)
```

#### 3.2.2 场景二：Makefile 工程

在 Kernel 侧的 Makefile 编译选项中添加：

```makefile
# 在 CXXFLAGS 或编译选项中添加
CXXFLAGS += -g -sanitizer
# 或使用等价选项
CXXFLAGS += -g --cce-enable-sanitizer

# 链接选项中也需添加
LDFLAGS += --cce-enable-sanitizer
```

> **注意事项**：
> - `-g` 和 `--cce-enable-sanitizer`（或 `-sanitizer`）必须同时添加，否则无法获取调用栈信息
> - `--cce-enable-sanitizer` 与 `-sanitizer` 完全等价，可随意选用
> - 与 `-O0` 同时开启时需额外添加 `--cce-ignore-always-inline=false`
> - 添加 `-g` 会在二进制中附带调试信息，注意控制文件权限
> - Atlas 350 加速卡不支持 `--cce-enable-sanitizer`/`-sanitizer` 及 `-O0`
> - mssanitizer是昇腾NPU算子专用的检测工具，不要与一般的sanitizer（ASAN）混淆。

#### 3.2.3 PyTorch 接入场景的插桩口径

mssanitizer 官方将“PyTorch 框架接入”列为支持场景，接入方式是用 mssanitizer 直接拉起整条 python 进程（`mssanitizer --tool=memcheck -- python test_ops_custom.py`），并非对 torch 做特殊集成。但“PyTorch 接入”要区分两种形态：

1. **PyTorch 接口调用自研算子（OpPlugin/自定义算子注册，非 TorchAir 图编译）**：kernel 由**算子自身编译工程**编译，可在其中添加编译选项做**全量检测**。做法：在该 AscendC kernel 工程的 `CMakeLists.txt`（如 msopgen 工程的 `op_kernel/CMakeLists.txt`）中添加 `-g --cce-enable-sanitizer` 编译/链接选项，编译部署后再用 mssanitizer 拉起 python 进程检测。框架侧需 `export PYTORCH_NO_NPU_MEMORY_CACHING=1` 关闭 NPU 内存池，否则内存检测结果不准确（必要时用 `sanitizerReportMalloc`/`sanitizerReportFree` 手动上报 GM 分配范围）。官方样例见《基础案例》“检测PyTorch接口调用的算子”。
2. **PyTorch 图模式（TorchAir）**：kernel 编译被 TorchAir 图编译接管，mssanitizer 无法注入编译选项。官方明确“仅支持在 msSanitizer 工具**不添加编译选项**的情况下进行检测”，即仅快速定界：只覆盖与 GM 相关的搬运指令、只检非法读写与非对齐访问、**无调用栈**，且要求算子 O2 优化并在链接阶段保留 `-q` 重定位符号。此形态下不要向用户承诺全量插桩/调用栈检测。

**一句话判据**：sanitizer 编译选项加在哪，取决于 kernel 二进制由谁编译——kernel 由自身工程编译（Kernel 直调/模板库/msopgen/算子库/OpPlugin 注册算子）则可加选项做全量检测（PyTorch/框架只是调用方）；kernel 由 TorchAir 图编译接管则无法加选项，只能快速定界。

### 3.3 步骤三：编译部署

按照用户提供的命令，重新编译部署算子。如用户未明确提供算子编译方式，则分析算子工程目录（如果有README说明文档则可以参考），确认编译方式并执行。注意务必做好进程管理，避免进程残留。

### 3.4 步骤四：运行检测

在算子仓库根目录下执行，产物位置见[1.4 检测产物位置](#14-检测产物位置)。

1. 确认算子执行命令

算子执行命令优先来自用户输入。若未明确提供，参考算子目录下的 `README.md` 文档中的运行示例；若文档中无示例，则分析算子工程源码和 CMakeLists.txt 拼凑运行命令。检测结束后提示用户明确指定运行命令。

2. 一键式脚本运行检测

使用[scripts/run_mssanitizer.py](scripts/run_mssanitizer.py)一键脚本自动完成四种检测，`--output-dir` 指定报告输出目录，`--extra-args` 透传 mssanitizer 附加参数（如 `--leak-check=yes`），`--` 之后传入算子执行命令（在算子仓库根目录执行；`<skill根>` 指本 skill 的 SKILL.md 所在目录，命令请用其绝对路径）：

```shell
python <skill根>/scripts/run_mssanitizer.py [--output-dir <算子目录>] [--extra-args "<mssanitizer参数>"] -- <算子执行命令>
```

示例：

```shell
# Kernel 直调场景
python <skill根>/scripts/run_mssanitizer.py --output-dir ./add_example -- ./execute_add_op

# run.sh脚本场景
python <skill根>/scripts/run_mssanitizer.py --output-dir ./add_example -- bash run.sh

# 附加泄漏检测参数
python <skill根>/scripts/run_mssanitizer.py --output-dir ./add_example --extra-args "--leak-check=yes" -- ./execute_add_op
```

运行结束后，在 `--output-dir` 指定目录下生成四个原始报告 `mssanitizer_origin_{检测类型}_{时间戳}.txt`（头部记录真实命令、核心参数与环境信息，供解析脚本生成最终报告）。

**注意**：以上内容以 memcheck 为例，出现 “\[mssanitizer\] Start xxx on kernel xxx.“才记作有效开始，出现“\[mssanitizer\] Finished on kernel xxx.“才算有效结束。完整包含两者才算有效结论，若无效请告知用户。

3. 手动运行单工具检测（可选）

```shell
mssanitizer --tool=memcheck --leak-check=yes -- <算子执行命令> > result.log 2>&1
```

### 3.5 步骤五：结果分析与修复

1. 生成合并分析报告

使用解析脚本将全部四个原始 `.txt` 报告合并转换为**一份**结构化的 `.md` 分析报告（仅提取和归类告警，不含修复建议）。分析报告会生成在与原始报告相同的目录下。支持传入文件路径或通配符：

```shell
# 在算子目录下用通配符一次传入（推荐）；<skill根> 指本 skill 的 SKILL.md 所在目录，请用其绝对路径
cd add_example && python <skill根>/scripts/parse_mssanitizer_report.py mssanitizer_origin_*.txt
```

> mssanitizer检测工具日志带有`[mssanitizer]`前缀，可根据此前缀区分工具日志和算子/工程日志。

脚本位于 [scripts/parse_mssanitizer_report.py](scripts/parse_mssanitizer_report.py)，输出内容包括：
- 环境信息（mssanitizer 版本、CANN 版本、芯片型号、执行目录等，来自原始报告头部）
- 真实命令与核心参数（实际执行的 mssanitizer 检测命令、启用的工具与附加参数）
- 检测结果汇总（按工具分列 ERROR/WARNING 数量，无报错 ✅、报错 ❌、警告 ⚠️，后接数量）
- ERROR 级别告警列表（按工具分组，含行号和代码位置）
- WARNING 级别告警列表（按工具分组，含行号和代码位置）
- 按告警类型分布统计（全工具汇总）
- "错误原因分析"与"修改方式与回归结果"待补全章节（后续填写）

合并分析报告的命名方式为：`mssanitizer_analysis_{时间戳}.md`，如 `mssanitizer_analysis_20260617_120000.md`。

2. 判断是否存在 ERROR

阅读生成的 `mssanitizer_analysis_*.md` 分析报告，检查"检测结果汇总"章节。所有工具 ERROR 均为 0（✅）时直接进入[步骤六：生成报告](#36-步骤六生成报告)；存在 ERROR（❌）时按下述流程分析修复，直至全部通过。

3. 分析修复（存在 ERROR 时）

按以下流程处理，循环直至检测全部通过：

1. **排除误报**：根据告警的调用栈位置核对源码，确认错误真实存在。判定为误报的错误不改代码，在最终报告中写明依据即可。
2. **分析错误**：对确认真实的 ERROR，结合告警类型、检测日志、源码上下文定位根因。
3. **修复算子**：若非误报，根据根因修改算子代码。
4. **重新检测**：重新编译后用相同命令再跑一遍检测。全部通过即结束；没过则回到第 1 步继续分析修复，直到通过为止。确实无法修复的，在报告中如实写明剩余错误和原因，不得谎报通过。

> **修复案例参考**：`references/` 目录下按检测类型提供了四个典型样例，每个样例包含带异常注入的算子源码及 README 说明，可作为错误根因分析和修复的参考：
> | 检测类型 | 样例目录 | 异常场景 |
> |----------|----------|----------|
> | memcheck | [references/sample_memcheck/](references/sample_memcheck/) | UB 缓冲区越界写入 |
> | racecheck | [references/sample_racecheck/](references/sample_racecheck/) | 流水间 WAW 数据竞争 |
> | initcheck | [references/sample_initcheck/](references/sample_initcheck/) | 未初始化 GM 内存读取 |
> | synccheck | [references/sample_synccheck/](references/sample_synccheck/) | SetFlag/WaitFlag 未配对 |

### 3.6 步骤六：生成最终报告

**清除所有残留进程**，然后将 `mssanitizer_analysis_<时间戳>.md` 补全为最终报告。解析脚本已自动生成环境信息、真实命令、核心参数、检测结果汇总（✅/❌/⚠️）与告警列表章节，需要补全"错误原因分析"与"修改方式与回归结果"两个章节。

最终报告**至少**包含以下内容：

1. **环境信息**：mssanitizer 版本、CANN 版本、芯片型号（NPU）、算子仓库及执行目录、检测时间。
2. **真实命令**：编译命令、各工具实际执行的 mssanitizer 检测命令、算子运行命令。
3. **检测核心参数**：启用的工具（memcheck/racecheck/initcheck/synccheck）及 `--leak-check`、`--kernel-name` 等实际使用的参数与取值。
4. **检测结果汇总**：按工具列出 ERROR/WARNING 数量——无报错写 ✅、报错写 ❌、警告写 ⚠️，后接数量。
5. **错误原因分析**：逐条列出 ERROR 的误报排查结论（确认真实/判定误报+依据）与根因。
6. **修复方式与最终结果**：逐条说明修复动作（修改的文件、位置、改动内容）及修复后回归检测结果。

报告模板（符号规则：ERROR 数量为 0 写 `✅ 0`，大于 0 写 `❌ N`；WARNING 数量为 0 写 `✅ 0`，大于 0 写 `⚠️ N`）：

```markdown
# msSanitizer 检测最终报告

## 1. 环境信息
- mssanitizer 版本：<mssanitizer -v 输出>
- CANN 版本：<CANN 安装版本>
- 芯片型号：<python3 -c "import acl; print(acl.get_soc_name())" 输出>
- 算子仓库/执行目录：<仓库绝对路径>
- 检测时间：<日期时间>

## 2. 运行信息
- 编译命令：`<实际编译命令>`
- 检测命令：`mssanitizer --tool=memcheck [--leak-check=yes ...] -- <算子执行命令>`（逐工具列出）
- 产物位置：result.log / mindstudio_sanitizer_log/ / mssanitizer_origin_*.txt 的实际路径

## 3. 核心参数
- 工具：memcheck / racecheck / initcheck / synccheck
- 其他参数：<--leak-check=yes / --kernel-name=xxx / 无>

## 4. 最终结果
| 检测工具 | ERROR | WARNING |
|----------|-------|---------|
| memcheck | ✅ 0 或 ❌ N | ✅ 0 或 ⚠️ N |
| racecheck | ✅ 0 或 ❌ N | ✅ 0 或 ⚠️ N |
| initcheck | ✅ 0 或 ❌ N | ✅ 0 或 ⚠️ N |
| synccheck | ✅ 0 或 ❌ N | ✅ 0 或 ⚠️ N |

## 5. 错误分析
| 编号 | 告警（工具/类型/位置） | 误报排查结论 | 根因 |
|------|------------------------|--------------|------|
| E1 | memcheck illegal write @ xxx.cpp:123 | 确认真实 | <根因描述> |
| E2 | racecheck hazard @ xxx.asc:45 | 判定误报（依据：...） | - |

## 6. 修复方式与最终结果
| 编号 | 修改内容（文件/位置/改动） | 最终检测结果 |
|------|----------------------------|--------------|
| E1 | xxx.cpp:123 拷贝长度由 1024 改为 512 | memcheck ✅ 0 |

⚠️基于AI技术生成，注意核查重要信息，仅供参考
```

### 3.7 步骤七：清理编译选项

检测完成后，将 CMakeLists.txt / MAKEFILE 中临时添加的 `--cce-enable-sanitizer`（或 `-sanitizer`）和 `-g` 编译/链接选项移除，恢复文件原始状态。

> **注意**：若编译选项是通过 `build.sh --mssanitizer`、`-mssanitizer` 或 `--bisheng_flags=` 等命令行参数注入的，则无需清理。triton 两仓（见 [references/official_workflow.md](references/official_workflow.md) 第 7 章）通过 `unset TRITON_ENABLE_SANITIZER TRITON_DISABLE_LINE_INFO` 恢复环境即可。

---

## 4. 官方算子工作流

对于官方算子库/样例库算子，第一步"运行环境检查"、第五步"结果分析与修复"、第六步"生成最终报告"和第七步"清理编译选项"与自定义算子完全一致（见第 3 章），第二到四步（编译选项适配、编译部署、运行检测）因代码仓而异。各代码仓的详细步骤、统一处理原则及架构类型参数取值统一收录在参考文档中：

**[references/official_workflow.md](references/official_workflow.md)** — 官方算子工作流与架构类型参数，已覆盖 ops-transformer / ops-nn / ops-math / ops-cv / asc-devkit / catlass / cann-samples / triton-ascend-kernels / shmem。

---

## 5. 附录

### 5.1 常见问题解答

### 5.1.1 架构类型参数获取方式

各代码仓的 `--soc` / `--npu-arch` / `CATLASS_ARCH` / `NPU_ARCH` / `-soc_type` 架构参数取值，统一收录在 [references/official_workflow.md](references/official_workflow.md) 第 9 章"架构类型参数获取方式"，请按芯片型号对应仓取用。

### 5.2 相关资源链接

- [官方算子工作流与架构类型参数 (references/official_workflow.md)](references/official_workflow.md) — 各官方算子仓的编译/部署/运行检测步骤、统一处理原则及架构类型参数取值
- [告警大全 (references/alarms.md)](references/alarms.md) — 所有告警类型的完整输出格式、参数含义及触发条件
- [msSanitizer 安装指南](https://gitcode.com/Ascend/mssanitizer/blob/master/docs/zh/install_guide/mssanitizer_install_guide.md)
- [msSanitizer 使用手册](https://gitcode.com/Ascend/mssanitizer/blob/master/docs/zh/user_guide/mssanitizer_user_guide.md)

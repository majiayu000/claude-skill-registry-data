---
name: msdebug-basic-usage
description: '昇腾AscendC算子调试工具（msDebug）技能，含两大流程：①上板调试——算子加 -g -O0 编译后由 msdebug 拉起，支持断点、单步、变量/内存打印、核切换、寄存器读取；②coredump解析——用户指定 core 文件路径后，msdebug 加载解析挂掉代码行/异常调用栈/现场变量。触发关键词：msdebug、算子调试、上板调试、断点、单步调试、打印变量、读内存、核切换、寄存器、coredump、core文件、调用栈、崩溃解析'
---

# msDebug 昇腾算子调试工具

msdebug 是基于 LLDB 的昇腾 NPU 算子调试器。本 skill 支持以下两种调试功能：

1. **上板调试**：给算子加 `-g -O0` 编译选项 → 重编译/部署 → 用 msdebug **拉起**算子进程 → 按用户意图交互式调试。
2. **coredump 解析**：用户指定 core 文件路径 → msdebug 加载解析（挂掉代码行/调用栈/现场变量）。

**先识别算子类型**：目标算子若位于以下**官方算子库/样例库**之一，其 `-g -O0` 编译适配、部署与可调试 target 获取均须走该仓对应流程（各仓注入机制差异较大）；否则按自定义工程处理。

| 官方算子库/样例库 | 简述 |
|------|------|
| [ops-transformer](https://gitcode.com/cann/ops-transformer) | CANN 算子库中提供 transformer 类大模型计算的进阶算子库 |
| [ops-nn](https://gitcode.com/cann/ops-nn) | CANN 算子库中提供神经网络计算能力的高阶算子库 |
| [ops-math](https://gitcode.com/cann/ops-math) | CANN 算子库中提供数值计算的基础算子库 |
| [ops-cv](https://gitcode.com/cann/ops-cv) | CANN 算子库中提供图像处理、目标检测等能力的高阶算子库 |
| [asc-devkit](https://gitcode.com/cann/asc-devkit) | 昇腾 AI 处理器专用的 AscendC 算子程序开发语言与标准库 |
| [catlass](https://gitcode.com/cann/catlass) | 高性能矩阵乘类算子基础模板库 |
| [cann-samples](https://gitcode.com/cann/cann-samples) | 官方 AscendC 样例库（SIMT/量化/FlashAttention 等 story 教学样例） |

> 各仓的 `-g -O0` 编译适配、部署与 target 获取统一按 [references/official_workflow.md](references/official_workflow.md) 对应仓章节执行（架构参数也查该文档）。msDebug 调试范围**不含** triton-ascend-kernels（Triton JIT）与 shmem（通信多卡）。

## 1. 目录结构

```text
msdebug-basic-usage/
├── SKILL.md                            // 本 skill 主文件
└── references/
    ├── official_workflow.md            // 各官方算子仓的编译适配/部署/target 获取工作流与架构参数
    ├── sample_debug/                   // 上板调试实测样例：完整命令/回显/命令速查表（含全称与缩写）
    └── sample_coredump/                // coredump 解析实测样例：core 产出、加载解析与命令可用性
```

## 2. 流程一：上板调试

> 支持 Kernel 直调（`<<<>>>`）、aclnn 单算子、PyTorch 接入。机制是 **launch（拉起）**：由 msdebug 启动算子进程并接管。

### 2.1 步骤 1：识别算子类型并加 `-g -O0` 编译

调试前必须让算子带上调试信息（`-g`）且关闭优化（`-O0`），否则断点无法定位代码行。**先按上方“官方算子库/样例库”列表识别目标算子所在工程类型**：

**① 官方算子库/样例库算子**：各仓 `-g -O0` 注入方式不同（`--op_debug_config` / `--bisheng_flags=` / `CMAKE_BUILD_TYPE=Debug` / `build.sh --debug` / 手动改 CMakeLists），**必须**按 [references/official_workflow.md](references/official_workflow.md) 对应仓章节执行编译适配、部署，并获取该仓产出的可调试 msdebug target；勿把某一仓命令套用到另一仓。

**② 自定义工程**（非上述官方仓）：
- **Makefile 工程（Kernel 侧）**：
  ```makefile
  COMPILER_FLAG := -xcce -O0 -g --cce-ignore-always-inline=true -std=c++17
  ```
- **CMake 工程**：`CMakePresets.json` 的 `CMAKE_BUILD_TYPE` 由 `Release` 改为 `Debug`，或在 kernel 侧 CMakeLists 加 `-g -O0`。

### 2.2 步骤 2：部署

- ops 系列仓（transformer/nn/math/cv）：编译产出 `build_out/cann-ops-<仓>*linux*.run`，安装至 `${ASCEND_HOME_PATH}/opp/vendors`，并按回显设置 `LD_LIBRARY_PATH`（见 references 对应仓）。
- 样例型仓（asc-devkit / catlass / cann-samples）：编译即出可执行文件，**无需部署**。

### 2.3 步骤 3：msdebug 拉起算子

```shell
# 必要时先做环境/通道检查
which msdebug                       # 不在 PATH 时用 ${ASCEND_HOME_PATH}/tools/msdebug/bin/msdebug
cat /proc/debug_switch              # 应为 1；为 0 需 root 执行 echo 1 > /proc/debug_switch（或以 --full 重装驱动）

# 拉起（进入 (msdebug) 会话；任选其一）
msdebug ./test_aclnn_add_example          # Kernel / aclnn 直调
msdebug -- ./app --flag1 arg1             # 带参程序
msdebug python3 test_ops_custom.py        # PyTorch（见 2.4）
```

> 终端报 `Cannot read termcap database` 时：先 `export TERMINFO=$(infocmp -D | head -n1)` 再拉起。

### 2.4 步骤 4：按用户意图交互调试

进程拉起后，进入`(msdebug)` 会话内，此时等待用户的下一步指令，并在 `(msdebug)` 会话内将用户意图映射为命令并执行。**注意：严禁进入`(msdebug)` 会话后自行加调试命令运行算子，msdebug是交互式调试流程，调试每一步都要按照用户的意图来。**

| 用户意图 | msdebug 命令（全称 / 缩写） |
|----------|------------------------------|
| 打断点 / 查看 / 删除 | `breakpoint set -f <file> -l <line>` / `b`；查看 `breakpoint list`；删除 `breakpoint delete <id>` |
| 运行 / 继续 / 中断 | `run` / `r`；`continue` / `c`；`CTRL+C`（run 后自动聚焦命中的 kernel） |
| 单步跳过 / 步入 / 步出 | `thread step-over` / `n` / `next`；`thread step-in` / `s` / `step`；`thread step-out` / `finish` |
| 打印变量 | `print <变量名>` / `p`（LocalTensor 看 `address_.bufferAddr`，GlobalTensor 看 `address_`） |
| 打印全部局部变量 | `frame variable` / `var` |
| 读 UB / GM / L1 / L0A / L0B / L0C / FB 内存 | `memory read` / `x`：`x -m <空间> -f <格式>[] <地址> -c <行数> -s <每行字节数>`（UB 用 bufferAddr，GM 用 address_） |
| 读寄存器 | `register read` / `re r`（全部加 `-a`；指定如 `re r $PC`） |
| 查看调用栈 / 切换栈帧 | `thread backtrace` / `bt`；`frame select <id>`（上板调试与 coredump 解析均可用） |
| 查 device / 核 / task / stream / block | `ascend info devices` / `cores` / `tasks` / `stream` / `blocks`（`blocks -d` 看各 block 中断处代码；`cores` 给出 CoreId 便于切核） |
| 切 Cube / Vector 核 | `ascend aic <id>` / `ascend aiv <id>`（id 取 `ascend info cores` 的 CoreId；`aic` 仅 Cube 算子场景可用） |
| 查 SIMT 线程 | `ascend info threads` / `ascend thread <id>`（仅 SIMT / Cube 核场景可用） |
| 帮助 / 退出 | `help <命令>` / `quit` / `q`（确认时输入 `y`） |

> `memory read`（`x`）的 `-m` 可选 `GM`/`UB`/`L1`/`L0A`/`L0B`/`L0C`/`FB`，`-f` 支持 `float32[]`/`float16[]`/`int32[]`/`uint8[]` 等，`-c` 为打印行数、`-s` 为每行字节数。完整实测回显与命令速查见 [references/sample_debug](references/sample_debug/README.md)，建议先按其 README 把样例跑通，再把同样命令泛化到目标算子。

**PyTorch 补充**：kernel 以独立 `.o` 部署、run 时动态下发，msdebug 不自动关联其调试信息；kernel 需先带 `-g -O0` 编译部署。

- 推荐：启动前 `export LAUNCH_KERNEL_PATH=<部署路径>/<OpName>_<hash>.o`（多在 `${ASCEND_HOME_PATH}/opp/vendors/customize/.../kernel/<SOC>/<op_type>/` 下，多 dtype 选实际调用的那个），再 `msdebug python3 test_ops_custom.py`，run 前即可按行号打断点。
- 备选：run 后手动 `image add <kernel.o>` 导入调试信息、`image load -f <kernel.o> -s 0` 使生效，再设断点（官方顺序：先 run，再 add → load）。

将`(msdebug)` 会话的打屏输出中与用户当前意图直接相关的 msdebug 回显（提示符/源码行号/变量值/stop reason）展示给用户，末尾给 1~3 条下一步提示予推荐；不输出内部准备与排障过程，不写长报告；每次末尾附 **⚠️基于AI技术生成，注意核查重要信息，仅供参考**。用户给出下一步意图后，继续转换为命令并执行。重复此流程直到用户结束调试。

若算子发生 AI Core（AIC ERR）类崩溃：**msdebug 调试会话与 coredump 抓取互斥**，需退出调试、按流程二 3.1 复现抓取 core 后再解析。

## 3. 流程二：coredump 解析

算子发生 AI Core（AIC ERR）异常崩溃后，**核心工作是加载并解析 core 文件**，定位挂掉代码行 / 异常调用栈 / 现场变量。解析是重点；如何产出 core 只是很短的前置（见 3.1）。

### 3.1 前置：如何产生 core 文件（简短，非重点）

> **coredump 抓取与 msdebug 调试互斥**，不能同时进行：msdebug 调试会话内不会抓取到该类 aic core；需退出调试，直接运行算子并开启 dump。

```shell
export ASCEND_DUMP_SCENE="aic_err_detail_dump"   # 必须设置才会生成 aic core
export ASCEND_DUMP_PATH=<输出目录>
./add                                       # 直接运行算子（非 msdebug 拉起）；崩溃后退出码非 0
# core 文件位于 ${ASCEND_DUMP_PATH}/extra-info/data-dump/<deviceId>/ 下
```

复现与“越界注入 → 崩溃出 core → 定位修复”的完整示例见 [references/sample_coredump](references/sample_coredump/README.md)。

### 3.2 配套产物与编译取向

- core 文件：必须。
- 解析用二进制：推荐提供 kernel.o（多 tilingKey 用目标 tilingKey 对应 .o）或可执行文件/动态库。**建议用 `-O2 -g` 编译**（保留 inline 展开以获取更完整调用栈；上板调试用的 `-O0` 会展开过多 inline，栈帧反而少）。缺省只有汇编/地址级信息。

### 3.3 加载与解析

```shell
msdebug --core <core文件> [<kernel.o 或 -O2 -g 编译的可执行文件/动态库>]
```

进入 `(msdebug)` 后按序执行：

1. `ascend info summary`：崩溃概要（挂掉 kernel、stop_reason、崩溃核列表与 PC、dump 中可读内存区域及地址）。判读：多核 PC 一致多为逻辑性错误；`x` 读内存的地址需取自 summary 列出的内存区域。
2. `bt`：调用栈。帧 #0~#2 常为 AscendC 库调用链，往下找用户源码帧（如 `DoubleBufAdd::Process(...) at add.asc:84`）即异常位置。仅 stop_reason 为 MTE_ERROR / VEC_ERROR / CUBE_ERROR / CCU_ERROR / FIXP_ERROR 时保证准确。
3. `frame select <id>`：逐帧看源码；`frame variable` / `p <变量名>`：查看现场变量。
4. `re r $PC`：核对崩溃指令地址；需要时用 `x` 读取 dump 内存取证。

### 3.4 coredump 模式命令可用性

| 命令 | 可用性 |
|------|--------|
| `ascend info summary` / `bt` / `frame select` / `frame variable` / `p` | ✅ |
| `re r $PC` / `register read -a` | ✅ |
| `x -m <空间> ...`（限 summary 列出的 dump 范围，越界报 `addr is not in range`） | ✅ |
| `ascend aiv <id>`（切换查看其他崩溃核） | ✅ |
| `ascend info cores` / `tasks` | ❌ coredump 模式不支持 |
| `n` / `s` / `c` / `continue`（单步与继续） | ❌ 静态快照不支持 |

### 3.5 输出结论

贴 summary / bt / frame / 变量关键回显，用 2~3 句话给出结论（挂掉代码行 file:line、调用栈要点、关键变量值 / 初步根因），附 ⚠️ 免责声明。解析不改动算子；修复请回到流程一（注意：coredump 建议 `-O2 -g`，上板调试建议 `-O0 -g`），修复后按 3.1 复现确认。

完整实测（summary / bt 回显、越界定位与修复）见 [references/sample_coredump](references/sample_coredump/README.md)。

## 4. 约束与注意事项

- 单 Device 仅支持单个 msdebug 实例，调试期间勿运行其他算子程序，单次只调试一个算子；调试通道权限大，生产环境禁用。
- Hccl 接口不支持单步调试；Ascend 950 的 simd_vf 强制 inline 导致断点无法解析时，目标行附近加 `__asm__("NOP");` 再打断点。
- Host/Kernel 同名实现文件时，断点用绝对路径。
- 调试完成后恢复临时改过的编译选项/构建文件，并清理残留进程。

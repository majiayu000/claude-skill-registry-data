---
name: cannbot-dsl-env-check
description: "当需要检查 CANNBotDSL 开发环境，或诊断导入、翻译、编译及 NPU 不可用问题时使用；输出环境诊断结果、可用能力与限制。"
---

# CANNBotDSL 环境检查

使用固定最小探针检查当前解释器和当前 CANN 环境，不安装 wheel、不猜测其他环境、不修改环境变量。产物为 `environment/environment.yaml` 和 `environment/env_selected_soc.yaml`。

## 输入

- 当前 Python 解释器和 CANNBotDSL/CANN 运行环境。
- 调用方指定的产物根目录；可选 `PYTHON` 指定解释器。

## 输出与运行

由调用方指定产物根目录：

    bash <skill>/scripts/check_env.sh --output-dir build/env-check

默认使用 python3；可通过 PYTHON=<selected-python> 指定解释器。选定解释器必须安装 PyYAML。

生成器固定在指定目录下创建：

    build/env-check/
    └── environment/
        ├── environment.yaml
        └── env_selected_soc.yaml

--output-dir 是产物根目录，而不是 YAML 文件路径。不要把人工维护文档放入生成器管理的 environment/。

## 核心能力链

| 检查名称 | 检查内容 | 失败定位 | 后续行为 |
|---|---|---|---|
| CANNBotDSL 导入 | 当前解释器能否导入 cannbotdsl | wheel、解释器或 Python 依赖 | 翻译与编译跳过，门禁失败 |
| DSL 翻译 | 固定探针能否完成 DSL 前端与 AscendC 翻译 | 探针接口、wheel 组件、翻译依赖或版本关系 | 编译跳过，门禁失败 |
| DSL 编译 | 固定探针能否经编译后端生成真实 .so | 探针接口、CANN Toolkit、bisheng、库路径或版本关系 | 门禁失败 |
| NPU 运行环境 | torch_npu 能否识别可用 NPU | PyTorch NPU、驱动、设备映射或运行时 | 不影响编译门禁，切换为 compile_only |

CANNBotDSL 导入→DSL 翻译→DSL 编译是严格依赖链：前一项失败，后一项标记 SKIP。NPU 运行环境独立检查，不执行 DSL kernel，不做精度或性能验证。

检查定义、通过条件、失败影响和处理方法见 `references/checks-and-troubleshooting.md`。

## 门禁与执行模式

编译门禁仅在 CANNBotDSL 导入、DSL 翻译和 DSL 编译全部 PASS 时通过：

| gate.status | 条件 | 动作 |
|---|---|---|
| PASS | 三项编译能力连续通过 | 允许继续 DSL 开发与编译 |
| FAIL | 任一编译能力失败 | 先修复首个失败项 |

“降级”不再使用含义模糊的布尔字段，而由 execution.mode 明确表达：

| 模式 | 条件 | 允许 | 阻止 |
|---|---|---|---|
| full | 编译门禁通过且 NPU 运行环境通过 | 生成、编译、NPU 精度、NPU 性能 | 无 |
| compile_only | 编译门禁通过但 NPU 运行环境失败 | 生成、编译 | NPU 精度、NPU 性能 |
| blocked | 编译门禁失败 | 环境诊断 | 编译与全部真机验证 |

`full` 表示允许进入后续真机验证阶段；环境检查本身尚未执行 DSL kernel，精度与性能结论由后续实际测试给出。

compile_only 的目的不是掩盖失败，而是保留无 NPU 主机上的有效工作：仍可生成和编译 DSL，同时明确禁止声称已完成真机精度或性能验证。

## 产物

environment.yaml 不维护结构版本号；本 skill 只维护一份当前生效的产物结构。产物按阅读优先级固定排序，先给结论，再给定位信息，最后给环境证据：

- `final_status`：最终状态、编译门禁、执行模式及允许/阻止的动作；
- `stage_status`：导入、翻译、编译和 NPU 运行阶段的状态及诊断；
- `software_environment`：Python、CANNBotDSL、CANN Toolkit、OPP、Simulator 和工具；
- `server_information`：进程可见 NPU、服务器物理设备与架构证据；
- `checked_at`：UTC 检查时间。

产物中的每个非空数据行都带中文注释。普通行的注释在固定的适中列开始；长路径和长诊断仅在原值后保留两个空格再写注释，不允许单个长值把整份文件的注释列推远。脚本会在写入前用 PyYAML 回读完整文本，只有注释版 YAML 与源数据完全一致时才原子替换目标文件。

完整字段说明与示例见 references/environment-schema.md。

## 默认使用卡

`env_selected_soc.yaml` 默认选择 `environment.yaml` 中 `server_information.npu.runtime_visible.devices` 的第一张带设备名称的可用卡，不从物理设备列表替代选择，因为物理存在不等于当前进程可用。

本 skill 只写入探针直接获得的逻辑设备编号、设备名称、完整芯片名、架构号及其来源，不维护 SOC 参考目录，不推导核数、片上存储、带宽或指令特性。

详细字段说明见 `references/env-selected-soc-schema.md`。

## 脚本结构

| 文件 | 职责 |
|---|---|
| scripts/check_env.sh | 薄入口：校验产物目录参数、解释器和 PyYAML |
| scripts/env_check.py | 编排全部环境检查、生成诊断、计算门禁与执行模式、原子写入 YAML |
| scripts/probe_compile_stage.py | 分别驱动 translate 和 compile 探针 |
| scripts/probe_kernel.py | 固定最小 DSL 内核 |

所有脚本通过自身位置解析依赖，skill 整体移动后无需修改内部路径。

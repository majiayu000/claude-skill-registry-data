---
name: wpegpt-analyzer
description: 驱动 IDA 配合 WPeGPT 插件对二进制可执行文件（PE/ELF）进行自动化逆向分析，输出包含程序用途、网络 IoC、可疑函数及漏洞评估的结构化报告。
---

# wpegpt-analyzer

驱动 IDA 配合 WPeGPT AI 插件，对二进制可执行文件进行自动化逆向分析。支持 PE 和 ELF 格式，提供三种分析模式：light（轻量分析）、full（深度分析）、vuln（漏洞评估）。

## 何时使用

当用户要求以下操作时使用此技能：
- 分析二进制可执行文件（`.exe`、`.dll`、`.elf` 等）
- 了解一个程序的功能和用途
- 进行逆向工程或恶意软件分析
- 从二进制文件中提取网络 IoC（入侵指标）
- 检查二进制文件是否存在漏洞或安全问题

## 何时不使用

- 静态文件查看（使用通用文件读取工具即可）
- 非二进制可执行文件分析

## 分析模式

| 模式 | 触发关键词 | 适用场景 |
|------|-----------|----------|
| `light`（默认） | 分析、看一下、了解用途、有什么功能、逆向、analyze | 轻量分析：程序用途、网络地址、可疑函数（约 2-5 分钟） |
| `full` | 深度分析、全面分析、详细分析、deep analysis | 全量分析：所有函数的完整功能分析（约 10-30 分钟） |
| `vuln` | 漏洞、漏洞分析、找漏洞、安全检查、安全审计、vuln、exp | 漏洞评估：高危函数、漏洞类型、风险等级（约 5-20 分钟） |

根据用户请求的语义自动选择模式。用户仅说"分析一下"或普通描述时，默认使用 `light` 模式。

## 操作步骤

### 1. 检查配置

读取 `./config/config.ini`。如果文件不存在或 `ida_dir` 为空，询问用户 IDA 的安装路径，然后创建该文件：

```ini
[paths]
ida_dir=<用户提供>
python_path=<可选，Python 已在系统 PATH 中时可留空>
```

在继续之前验证以下依赖：
- `<ida_dir>\ida.exe` 必须存在
- `<ida_dir>\plugins\WPeGPT.py` 必须存在
- `<ida_dir>\plugins\WPeGPT_Config\config.py` 必须存在
- `<ida_dir>\plugins\WPeGPT_Config\wpe_ai_controller.py` 必须存在
- Python 可用（已在 `./config/config.ini` 配置 `python_path` 路径或在系统 PATH 中）

任一依赖缺失时，停止分析并报告缺失项。

### 2. 确认文件路径

确认用户指定的待分析二进制文件存在。如果不存在，询问用户正确路径。

### 3. 执行分析

运行 PowerShell 分析脚本：

```bash
powershell -NoProfile -File "./scripts/wpegpt_analyze.ps1" -BinaryPath "<binary_path>" -Mode "<mode>"
```

模式可选：`light`（默认）、`full`、`vuln`。

**重要：** 始终使用 `powershell -NoProfile -File` 调用 `.ps1` 脚本。**不要**使用 `cmd.exe /c` 调用 `.bat` 脚本，在该环境下输出会被截断。

脚本将自动完成以下步骤：
1. 解析配置文件并验证所有依赖
2. 检测 32 位或 64 位架构（PE 头 Machine Type 或 ELF class）
3. 选择对应的 IDA 可执行文件（`ida.exe` 或 `ida64.exe`）
4. 以无头模式（`-A`）启动 IDA，WPeGPT 插件自动加载
5. 轮询等待 WPeServer TCP 端口文件就绪
6. 运行 `wpe_ai_controller.py` 通过 TCP 驱动分析
7. 分析完成后自动退出

### 4. 输出结果

报告保存在二进制文件同级目录下：`<binary_dir>/<文件名>_WPeAI_Results/`

读取生成的 Markdown 报告，向用户总结：
- **程序用途**：AI 综合判定的程序分类和行为特征
- **网络 IoC**：IP、域名、URL、端口（如有网络行为）
- **可疑函数**：数量及关键信息
- **完整报告路径**：`.md` 和 `.json` 报告的位置

`vuln` 模式下，重点突出发现的漏洞类型、风险等级和潜在利用点。

## 配置

`./config/config.ini`：

```ini
[paths]
; IDA 安装目录（必填）
ida_dir=
; Python 可执行文件路径（可选，Python 已在 PATH 中时可留空）
python_path=
```

IDA 进行分析时使用的 AI 模型和 API 密钥在 `<ida_dir>\plugins\WPeGPT_Config\config.py` 中配置（不在本技能管理范围内）。

## 文件结构

```
wpegpt-analyzer/
├── SKILL.md                  # 本文件
├── config/
│   └── config.ini            # 技能配置文件
└── scripts/
    ├── wpegpt_analyze.ps1    # PowerShell 启动脚本（推荐）
    └── wpegpt_analyze.bat    # Batch 启动脚本（备用，仅本地终端使用）
```

外部依赖（位于 IDA 安装目录的 plugins 子目录）：
```
<ida_dir>/plugins/
├── WPeGPT.py                 # IDA 插件（含 WPeServer TCP 服务）
└── WPeGPT_Config/
    ├── config.py             # WPeGPT 使用的 AI 模型 / API 配置文件
    └── wpe_ai_controller.py  # 外部 AI 控制器（驱动 IDA 进行自动化分析）
```

## 注意事项

- **非交互模式**：分析流程全自动运行，所有配置必须提前写入 `config.ini`。首次运行时由本技能的"步骤 1"负责交互式创建配置文件。
- **无头模式**：IDA 以最小化方式启动（`-A` 标志）。WPeGPT 插件自动启动 WPeServer，控制器通过 TCP 与其通信。
- **耗时参考**：light 模式约 2-5 分钟，full/vuln 模式约 5-30 分钟（取决于二进制文件大小）。
- **API 密钥**：AI 分析依赖 `WPeGPT_Config/config.py` 中配置的有效 API 凭证。
- **环境清理**：每次运行前自动清理 `%TEMP%` 下的旧端口文件。

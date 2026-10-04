---
name: windows-scripting-standards-skill
description: >-
  Windows 环境下 PowerShell 7 (pwsh) 与 Batch (.bat/.cmd) 脚本编写、调试排错与运行环境防坑规范。适用于编写、维护、重构与审查 .ps1 和 .bat 自动化脚本、诊断 Windows 终端或脚本执行报错（如非内部命令、UTF-8/BOM乱码、参数解析异常、退出码捕获）、以及 Linux/Bash 脚本向 Windows 跨平台移植；涵盖 PowerShell 现代管道与反引号转义、外部进程调用校验 ($LASTEXITCODE)、CMD 延迟变量扩展 (!VAR!) 等任务。
---

# /windows-scripting-standards-skill — Windows 脚本与 Agent 命令执行全栈规范

本 Skill 是专为 AI Agent 在 Windows 操作系统环境下执行命令行、生成与维护脚本文件而设计的通用标准。深度提炼了 PowerShell 7 (`pwsh`) 与传统批处理 (`.bat` / `.cmd`) 的语法机理、底层执行模型与系统级限制，系统化解决 LLM 训练语料中 Bash 偏置导致的**转义混乱、命令别名幻觉、编码乱码、引号地狱、错误静默与进程脱缰**等常见故障。

---

## 1. 触发场景 (Trigger)

当 Agent 或用户处理以下任何场景时，应当主动激活本 Skill：
* **PowerShell 脚本编写与重构**：编写、维护、重构或审查 `.ps1` 脚本，涉及进程控制、文件系统操作、错误拦截、外部程序调用与对象管道。
* **批处理脚本编写与排错**：编写、排查、维护或转换 `.bat` / `.cmd` 批处理文件，处理环境变量扩展、循环遍历、代码页配置及退出码。
* **Windows 报错诊断与修复**：诊断 `'xxx' 不是内部或外部命令`、`ï»¿@echo off` 乱码错误、`A parameter cannot be found` 参数报错、`$ErrorActionPreference` 漏拦截等 Windows 脚本与命令特有问题。
* **跨 Shell 与跨平台移植**：将 Linux/Bash 脚本或命令迁移适配至 Windows PowerShell 7 或 CMD 批处理。
* **复杂命令与脚本安全构建**：当需要构建复杂 Windows CLI 多行命令、排查引号与反引号转义地狱、或解决中文编码代码页冲突时提供参考（注：日常单行交互请遵循系统常驻指令）。

---

## 2. 核心架构与决策流 (Architecture Decision Tree)

```text
                          [ Windows 任务执行需求 ]
                                     │
        ┌────────────────────────────┴────────────────────────────┐
        ▼                                                         ▼
【 场景 A：即时命令执行 (CLI Tool) 】               【 场景 B：脚本文件持久化 (.ps1 / .bat) 】
  • 优先且强制选择: pwsh (PowerShell 7+)               • 首选方案: PowerShell 7 (.ps1)
  • 严禁混用: cmd.exe / powershell.exe (5.1)            • 遗留/极简无运行时依赖: Batch (.bat)
  • 核心防御:                                          • 核心防御:
    - 转义符为反引号 ` (非 \)                             - .ps1 强制 UTF-8 无 BOM
    - 外部程序带空格路径用 & "path"                        - .bat 强制 ANSI/GBK，CRLF 换行，禁 BOM
    - 检查 $LASTEXITCODE 而非单纯依赖 try-catch           - .bat 复合语句必用 setlocal enabledelayedexpansion
    - 比较符用 -eq/-ne/-gt (严禁使用 > 做比较)             - 变量赋值使用 set "VAR=value" 格式
```

---

## 3. 五大不可逾越的防御铁律 (Non-Negotiable Rules)

### 铁律 1：Shell 环境严格隔离，严禁 Bash 语法穿透
* Windows 上统一且优先使用 **PowerShell 7+ (`pwsh`)**。严禁降级调用 Windows PowerShell 5.1（`powershell.exe`）或 `cmd.exe`（除非用户明确限定批处理文件）。
* **严禁套用 Linux/Bash 特有习惯**：
  * 严禁使用 `export VAR=val`（PowerShell 应为 `$env:VAR = 'val'`，BAT 应为 `set "VAR=val"`）。
  * 严禁将 Linux 常用参数盲目套给同名别名（如 `ls -la`、`rm -rf` 会因参数未定义而报错；应使用 `Get-ChildItem` 或 `Remove-Item -Recurse -Force`）。
  * 严禁使用反斜杠 `\` 作为命令行换行或转义符（PowerShell 换行与转义符均为反引号 `` ` ``）。

### 铁律 2：编码与换行符生命线，坚决消灭 BOM 灾难
* **`.ps1` 脚本**：统一保存为 **UTF-8 无 BOM (No-BOM)** 格式。
* **`.bat` 批处理文件**：
  * **绝不可包含 UTF-8 BOM 字节序**（`\xEF\xBB\xBF`），否则 `cmd.exe` 首行必定报 `'ï»¿@echo off' 不是内部或外部命令`。
  * 含有中文或非 ASCII 字符的 `.bat` 文件，**必须保存为 ANSI (中文 Windows 下为 CP936/GBK)**。严禁直接保存为 UTF-8 无 BOM，防止中文字符字节码中恰好出现的 `0x29`（即 ASCII `)`）导致代码块提前闭合崩溃。
  * `.bat` 文件的换行符**必须且仅能为 CRLF (`\r\n`)**，不可使用 Unix 风格的 LF (`\n`)。

### 铁律 3：退出码精准捕获，杜绝静默失败
* **PowerShell 7**：
  * 首部声明 `$ErrorActionPreference = 'Stop'`，但这**只能拦截 PowerShell 原生 Cmdlet 终止错误，对原生可执行程序（如 git, node, python 等）的非 0 退出完全无效**！
  * 执行任何外部 `.exe` 后，必须紧跟检查 `$LASTEXITCODE`，或在 PowerShell 7.3+ 首部开启 `$PSNativeCommandUseErrorActionPreference = $true`：
    ```powershell
    & git checkout main
    if ($LASTEXITCODE -ne 0) { throw "Git checkout failed with exit code $LASTEXITCODE" }
    ```
* **Batch (`.bat`)**：
  * `IF ERRORLEVEL n` 语义为 `ERRORLEVEL >= n`，绝非等于。
  * 精确判断成功/失败推荐：`if %ERRORLEVEL% EQU 0 (...)` 或短路语法 `command && (...) || (...)`。
  * 批处理退出必须使用 `exit /b %ERRORLEVEL%`，严禁直接使用裸 `exit`（会导致宿主终端窗口或父 Shell 会话被意外关闭）。

### 铁律 4：引号地狱与变量展开防爆准则
* **PowerShell 7**：
  * 单引号 `'...'` 为字面量，双引号 `"..."` 会解析变量与子表达式 `$()`。
  * 调用原生外部命令传递带引号的参数（如 JSON 字符串、含空格的 commit 信息）时，PowerShell 会在传递给底层 API 时剥离外层引号，必须使用 `\"` 或 `\`"` 进行逃逸，或者使用参数数组传递。
  * 路径包含空格时，直接执行字符串只会打印文本，必须使用调用操作符 `& "C:\Program Files\..."`。
  * 路径包含方括号 `[...]` 时，**必须使用 `-LiteralPath`（或 `-lp`）而非 `-Path`**，防止触发通配符匹配报错。
  * 复杂对象转换为 JSON 时必须显式指定深度（如 `ConvertTo-Json -Depth 10`），避免默认 `-Depth 2` 浅截断生成脏数据。
* **Batch (`.bat`)**：
  * 变量赋值必须严格遵守黄金语法：`set "VAR=value"`（引号包裹 `变量名=值`，消除首尾不可见空格污染）。
  * 在 `IF (...)` 或 `FOR (...)` 复合代码块内部，必须在脚本首部声明 `setlocal enabledelayedexpansion`，并在块内使用感叹号 `!VAR!` 读取运行时最新值，严禁使用预解析阶段就固化的 `%VAR%`。
  * **复合括号块内部必须且只能使用 `REM` 注释，绝对禁止使用 `::`**（否则解析器当作非法标签引发语法崩溃）。
  * 接收外部传参必须使用 `%~1` 剥离外层双引号，防止双重引号嵌套错误。

### 铁律 5：重定向与比较符红线，严防破坏性文件覆盖
* 在 PowerShell 中：
  * 比较操作符是 **`-eq`、`-ne`、`-gt`、`-lt`、`-ge`、`-le`**。
  * **严禁将 `>` 或 `<` 用作比较大小**！`$a > $b` 在 PowerShell 中是**将变量 `$a` 输出并覆盖写入名为 `$b` 的本地文件**，属于高危隐蔽的文件破坏事故！

---

## 4. 模块索引与参考文档 (Reference Index)

在处理具体领域的任务时，请按需查阅 `references/` 目录下的专用规范手册：

* **[powershell7_execution_and_syntax.md](references/powershell7_execution_and_syntax.md)**：
  * PowerShell 7 (CoreCLR) 现代语法演进（`&&`, `||`, `? :`, `??`, `??=`）
  * 引号模式、转义规则与 Here-Strings（`@" ... "@`）边界
  * `$PSNativeCommandArgumentPassing = 'Standard'` 机制与参数数组
  * `-LiteralPath` (`-lp`) 方括号通配符防坑与 `ConvertTo-Json -Depth 10` 深度控制
  * `$PSNativeCommandUseErrorActionPreference = $true` 现代原生错误拦截
  * 文件锁定与共享冲突检测（Sharing Violation / IOException）
  * 对象管道流思维与原生 Cmdlet 最佳实践（`Where-Object`, `Select-Object`, `Select-String`）
  * 函数标准规范：`[CmdletBinding()]`、强类型参数绑定与异常安全

* **[batch_script_standards.md](references/batch_script_standards.md)**：
  * 工业级 BAT 脚本标准模板与生命周期治理（`setlocal` / `endlocal`）
  * 即时展开 `%VAR%` 与延迟展开 `!VAR!` 的机制剖析与经典陷阱
  * 循环系统（`FOR /F`, `FOR /R`, `FOR /D`）与单字母变量大小写敏感性
  * 复合括号块严禁 `::` 注释与参数修饰符（`%~1`, `%~dp0`, `%~nx1`）
  * UNC 网络路径与 `pushd` 临时虚拟盘符映射机制
  * 外部调用控制流：`call other.bat` vs `cmd /c`（防止控制权丢失）
  * 高频功能模块：管理员权限探测、静默等待、无换行输出、依赖探测

* **[agent_cli_pitfalls_and_solutions.md](references/agent_cli_pitfalls_and_solutions.md)**：
  * **20 大 Agent 在 Windows 下的高频报错与根因排查矩阵**
  * 包含：别名参数不匹配、环境变量赋值混淆、引号剥离、空格路径解析、重定向误伤、stderr 误报、BOM 乱码崩溃、中文截断括号、ERRORLEVEL 误判、`::` 括号崩溃、`-LiteralPath` 丢失、`-Depth 2` 截断、参数双重引号等典型错误对照与安全修复方案

* **[encoding_and_runtime_environments.md](references/encoding_and_runtime_environments.md)**：
  * Windows 编码体系图解：UTF-8 No-BOM, UTF-8 with BOM, ANSI (CP936/GBK), CP437, UTF-16LE
  * PowerShell 7 的 `$OutputEncoding` 与 `[Console]::OutputEncoding`
  * CMD 终端代码页切换机制（`chcp 65001`）的适用边界与副作用
  * 跨平台文本传输中的 CRLF vs LF 换行符控制

* **[quick_reference_cheatsheet.md](references/quick_reference_cheatsheet.md)**：
  * **Linux Bash ↔ PowerShell 7 ↔ Windows Batch 三方高频命令与语法速查对照表**
  * 特殊符号转义与保留字符一览
  * 生产就绪的标准 `.ps1` 脚本模板与标准 `.bat` 脚本模板

---

## 5. 极速自检清单 (Agent Pre-flight Checklist)

在向用户输出 Windows 命令或交付脚本代码前，请快速自检以下 7 点：

1. [ ] **环境匹配**：执行的命令是符合 PowerShell 7 规范还是 CMD 批处理规范？没有混用 `export`、`ls -la` 或 `grep` 吗？
2. [ ] **转义符号**：PowerShell 是否使用了反引号 `` ` ``，CMD 是否使用了脱字符 `^`？
3. [ ] **带空格路径**：路径包含空格时是否用引号包裹？在 PowerShell 中调用可执行文件时是否添加了 `&`？
4. [ ] **外部命令退出**：PowerShell 执行外部工具后是否校验了 `$LASTEXITCODE` 或设置了 `$PSNativeCommandUseErrorActionPreference`？
5. [ ] **方括号路径防坑**：PowerShell 操作带中括号 `[...]` 路径时是否使用了 `-LiteralPath`？
6. [ ] **BAT 赋值与延迟**：批处理中是否有 `set "VAR=value"`？复合代码块中是否开启了 `enabledelayedexpansion` 并使用了 `!VAR!`？括号内是否误用了 `::`？
7. [ ] **文件编码与格式**：`.bat` 是否为纯 ASCII 或 ANSI/GBK 编码且换行符为 CRLF？绝对没有附加 UTF-8 BOM 吗？

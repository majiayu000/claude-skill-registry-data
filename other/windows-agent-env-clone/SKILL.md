---
name: windows-agent-env-clone
description: 扫描本机 Windows 环境，生成/更新一份可在新机复刻的 Agent 开发运行环境配置清单（md）。当用户要求"给另一台 Windows 克隆环境""生成环境配置清单""更新配置清单""新机要装什么"时使用。
agent_created: true
---

# Windows Agent 环境清单生成

## 硬性规则（用户反复强调）

1. **只列本机实测已装**：未安装的、建议类的、可选的一律不写；不出现"建议/如需/可选"措辞。
2. **全局安装**：禁止写入任何应用的隔离目录（`.workbuddy/binaries/...` 等），路径统一用全局位置。
3. **空目录 / PATH 残留 ≠ 已装**：必须 exe 或注册表命中才算。踩过坑：Ollama（仅 PATH 残留）、Notion / AutoGLM / Tokscale（空目录）。
4. 用户点名排除的项要彻底删干净（正文、一键脚本、验证清单、PATH 四处都要查）。

## 扫描流程

1. **写 Python 脚本到 `tmp/` 再执行**——Git Bash 里 heredoc 长脚本易截断，Write 文件最稳。
2. **三源交叉核对**：
   - 注册表卸载项（HKLM 与 HKCU 的 `Uninstall`，含 WOW6432Node 共三处）→ `DisplayName` + `DisplayVersion` + `InstallLocation`
   - 关键 exe 绝对路径探测
   - 包管理器：`npm list -g`、`pip list`（**多个 Python 版本要分别扫**，本机同时有 3.12 和 3.13）
3. **winget ID**：用 Python `subprocess` 调 `winget list` 并过滤关键字。

## 已知坑

- `cmd /c "..."` 被安全策略拦截，不要用。
- PowerShell 工具 stdout 常被吞（返回空）→ 写文件再读也可能失败，优先用 Python subprocess。
- Bash 里 `node` / `python` 可能解析到隔离版，取真实系统版本要用绝对路径：`C:/Program Files/nodejs/node.exe`。
- `wsl.exe` 在安全黑名单，调用会被拒 → 只用注册表确认 WSL 已启用，发行版另查或标注"未检出"。
- VS Code 扩展：读 `~/.vscode/extensions` 目录名比执行 `code --list-extensions` 稳定。
- Electron 应用版本：读 `resources/app/package.json`；目录存在但为空 = 未真正安装，不列入。
- `code --list-extensions`、`npm list -g` 在 Python subprocess 里常因 PATH 找不到，改走目录读取。

## 输出文档结构（12 章）

基础运行时 → 编译工具链 → 开发工具（含 VS Code 扩展）→ AI/Agent 工具 → 沙箱与容器 → 命令行效率工具 → 常用桌面软件 → Python 全局包（按版本分块）→ PATH 参考 → 一键安装脚本（PowerShell）→ 安装后验证清单 → 明确未列入项（表格附排除原因）

## 收尾

写完后用 `present_files` 展示，并在回复里给一份精简清单摘要（用户偏好直接看结果，不爱冗长解释）。

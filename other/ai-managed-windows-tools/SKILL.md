---
name: ai-managed-windows-tools
description: 设计带 AI 控制与 GUI 的 Windows 系统管理工具（自启动/服务/注册表）时使用。
---

# AI 管理的 Windows 系统工具（设计模式）

适用于"既要 AI 交互式管理、又要 GUI、又要处理 Windows 权限敏感操作"的桌面工具类项目。核心结论经 grill-me 烤问得出，勿再砍安全边界。

## 核心架构：三进程

```
AI 客户端 ──HTTP localhost──► sidecar (常驻, 普通权限, MCP server)
                                  │ 写操作
                                  ▼
                              helper (一次性提权, ShellExecute runas)
                                  │ 弹独立确认窗 → 用户拍板 → 执行
                                  ▼
                              GUI (用户主动打开, 可 UAC 重启自己)
```

1. **sidecar**（`app --daemon`，常驻，普通权限）：跑 MCP server，只做读操作和转发写请求。**永不提权**。
2. **helper**（`app --exec`，一次性，提权）：sidecar 收到写请求后 `ShellExecute runas` 拉起，弹独立确认窗（不在 GUI 里，与主窗口零依赖），用户点允许才执行，结果回传后退出。
3. **GUI**：用户主动打开的管理界面，UAC 重启自己，与 sidecar 走 IPC。

为什么：AI 永远连得上 sidecar（常驻 ✓）、sidecar 永远普通权限（不常驻管理员 ✓）、提权只发生在 helper 短暂生命周期 ✓、确认窗独立于 GUI 用户在哪都能处理 ✓。这是 UAC consent.exe 模式。

**触发方式**：sidecar 自启用 Run 键（dogfood——工具自己管理启动方式）。

## 安全边界（勿再砍）

- **硬确认 token**：写工具默认拒绝执行，除非 AI 先拿到合法确认 token（弹窗通过后颁发，带超时）。边界在运行时，不在 AI 的自觉。软确认（"AI 应该调用确认"）是漏洞——注入后的 AI 会跳过。
- **弹窗展示的事实由 helper 独立核验**：sidecar 只传"操作意图 + 目标条目 ID"，helper 自己查注册表/验签名/跑规则引擎再弹窗。**操作描述可以来自 AI，弹窗事实必须 helper 自己读**——sidecar 是普通权限可能被攻破，传来的文本不可信。
- **规则引擎必须共享同一份代码**：sidecar + helper + GUI 共用 core crate，不能各写一遍。
- **风险定级**：软件规则决定（未签名 + 系统目录外 + 非微软发布者 = 高风险），AI 只做分析建议，用户最终拍板。风险等级交给 AI 判 = 把决定权交回给可能被注入的 AI。
- prompt 精心设计只是减噪，不是防线。**防 prompt injection 的唯一真边界是"弹窗展示机器校验的事实，用户拍板"**。

## AI 交互：CLI 为底座，Skill 先行，MCP 后置

**目标"任何 AI agent 都能调用"时，CLI 才是通用底座，不是 skill。** skill 不是跨 agent 标准（Claude SKILL.md / Hermes skill / OpenCode 格式各异）；MCP 是协议标准但应用进程绑定问题多。真正所有 agent 都能调的是**一个稳定 CLI**。

```
AI agent → 读 SKILL.md/skill → 调 bootkeeper CLI → core crate
协议系 agent → 连 MCP (后置薄适配层) → 调 bootkeeper CLI
```

- **v1 就做**：`bootkeeper` CLI + `SKILL.md`（说明书，教 agent 调 CLI）。"skill 就能实现 AI 调用"成立。
- **SKILL.md 用 skills.sh 标准**（Vercel Agent Skills，`npx skills add <owner>/<repo>`，覆盖 19+ agent 含 Hermes/nous-research）——不要自造 skill 格式。
- **MCP 不锁死**：以后加就是包一层 CLI → MCP 工具，不动 core。
- 写命令（enable/disable/remove/add/restore）同样要硬确认 token。

## 核心 Rust 依赖（调研定稿，勿换）

| 能力 | 方案 | 理由 |
|---|---|---|
| 注册表 Run/RunOnce | `winreg` | 196M 下载，活跃维护 |
| 启动文件夹 | `std::fs` 读路径 | 就是 shell:startup 路径，无需库 |
| 任务计划 | `windows` crate `Win32_System_TaskScheduler` (COM) | **`taskschd` crate 已死**（2023 停更仅 3.8k 下载）；schtasks CLI 输出本地化脆弱 |
| 签名校验 | `windows` crate `Win32_Security_WinTrust` (WinVerifyTrust) | 官方绑定；v1 只验有效性，信任锚列表后置 |

技术栈（已定稿）：Tauri 2 + Vue 3 + TS + Naive UI + @material/material-color-utilities + Pinia + vue-i18n + tauri-plugin-locale-api + Vite。i18n v1 只做中/英。

## 快照/回滚协议

- 写操作前强制备份（.reg 导出或备份键），操作前后各留快照。
- 保留期可配，默认 7 天。
- `restore_item` 恢复操作必须进 MCP tool surface——没有恢复工具，"AI 交互式管理"承诺是半截的。
- **禁用语义已定：改名**（`Foo` → `Foo.disabled`，Autoruns 官方思路）。恢复 = 改回名字，快照只存"原名 → 改名后名"映射。不要移备份键（其他工具误报）、不要真删除+快照（恢复逻辑复杂）。

## MCP 传输选型

- 桌面应用内置 MCP = **HTTP/SSE 监听 localhost**（先例：EnvKit 468★）。server 生命周期绑应用进程。
- 裸 MCP 进程 = **stdio**（AI 客户端拉起）。GUI 重启即死，不适合"应用常驻 + 提权重启"场景。
- HTTP 常驻必须做鉴权：token 生成后存 Windows Credential Manager（DPAPI），首次 GUI 展示给用户复制。

## 枚举/功能参考

- `p0w3rsh3ll/AutoRuns`（PowerShell 模块 300★）：持久化位置完整清单——Run/RunOnce、启动文件夹、计划任务、服务/驱动、ShellServiceObjects、IFEO 等十几个类别。抄清单，不重想。
- Sysinternals Autoruns 是功能天花板；差异化卖点在"现代 GUI + i18n + AI 可调用 + 开源"，不在枚举本身。

## 坑

- UAC 重启整个应用 + stdio MCP = 进程重启连接断，操作半途而废 → 必须拆 sidecar。
- "精心设计的 prompt"防不住 injection → 弹窗事实机器核验。
- 按批确认（"确认删除这 40 项"）会让恶意项混入 → 高风险项逐项确认或分级。
- 本机进程都能连 localhost MCP → token 必须 Credential Manager，不能明文。

## 参考文件

- `references/autostart-manager-design.md` — 用户自启动管理工具的具体设计决策（v1 范围、技术栈、MCP 细节、待定项）

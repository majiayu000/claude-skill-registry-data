---
name: ai-controllable-tool-design
description: 设计让 AI agent 安全调用的系统工具（CLI 底座、SKILL.md 标准、硬确认、提权模型）。
category: software-development
tags: [ai-agent, mcp, skill, cli, security, elevation, architecture]
---

# AI 可调用系统工具设计

设计"AI agent 能安全操作真实系统"的工具（启动项管理器、进程管理器、文件系统工具等）。BootKeeper 实战打磨出的模式。

## 核心原则：CLI 是底座，skill/MCP 是皮

**Skill 不是跨 agent 标准**——Claude 的 SKILL.md、Hermes、OpenCode 格式各异。让"任何 agent 都能调用"的唯一通用执行面是 **CLI**：

```
任何 AI agent → 读 SKILL.md/skill → 调 CLI → core 逻辑
协议系 agent  → 连 MCP (后置)    → 调 CLI → core 逻辑
```

- CLI 输出 **JSON**（AI 直接解析）
- SKILL.md 是"说明书"教 agent 怎么调 CLI，不是执行层
- MCP 只是包 CLI 的薄适配层，可后置（不动 core）
- 跨 agent 技能标准：**skills.sh**（Vercel，`npx skills add <owner>/<repo>`，覆盖 19+ agent 含 nous-research/Hermes）。SKILL.md 放仓库根，标准格式 frontmatter（name + description）

## 安全模型：硬确认，不信 AI 自觉

AI 操作真实系统时，注入风险是真实威胁（恶意启动项名/路径本身就是指令载体）。防线必须建在**运行时**，不在 prompt：

1. **硬确认 token**：写工具（delete/enable/disable/add）默认拒绝执行，必须先拿到确认 token（确认窗通过后颁发，带超时）。AI 可以不弹窗，但不弹窗就什么都改不了。
2. **弹窗事实独立核验**：确认窗显示的"事实"（路径、签名、发布者、风险）由**提权进程自己重新查证**，不信调用方传来的文本。调用方只传"操作意图 + 条目 ID"。
3. **风险定级 = 软件规则**（确定性函数：未签名 + 非系统路径 + 非可信发布者 = 高），AI 只分析建议，用户最终拍板。禁止 AI 生成风险结论。
4. **规则引擎一份代码**：所有进程共享同一核心 crate，禁止各写一遍。

## 提权模型：sidecar 永不提权，helper 一次性提权

三进程架构（UAC 场景）：
```
CLI/服务 (常驻, 普通权限) → 写请求 → helper (提权一次性)
                                        → 弹独立确认窗（不依赖 GUI）
                                        → 用户点"是" → 执行 + 快照 → 结果回传
```

- sidecar/CLI 永远普通权限（不常驻管理员）
- 提权只发生在 helper 的短暂生命周期（ShellExecuteW "runas" 拉起）
- 确认窗独立于主 GUI——用户在桌面任何位置都能处理 AI 授权
- GUI 的 UAC 重启不影响 helper/CLI 的常驻

## 快照与回滚（用户数据安全，不可省）

- 每次写操作**前**自动备份，记录操作前后快照
- 快照默认保留 N 天（如 7 天），可配置
- **禁用语义用改名**（`Foo` → `Foo.disabled`，Autoruns 官方思路）：可逆、恢复 = 改回名字、快照只存"原名→改名后名"映射
- MCP/skill 的 tool surface 必须含 `restore_item` / `snapshot list`——AI 禁错了要能自己还回去

## 关键坑位

- **弹窗疲劳**：按项确认 40 次用户无脑点是，边界失效。要分级：高风险逐项确认、低风险可批量。
- **prompt 防不住 injection**：恶意条目把"删掉 Defender"伪装成用户下一步意图。别把宝押在 prompt 上，弹窗展示**机器事实**（路径/签名/发布者/原值），不是 AI 修辞。
- **skill 不是 MCP 替代品**：如果目标包含"协议系 agent 也能连"，MCP 迟早要补——设计时留好"包 CLI"的接缝，别把逻辑焊死在 skill 里。

---
name: baku-skill-manager
description: 管理全局 Agent Skill 的安装、认领、软链接、更新、三方合并、冲突恢复、卸载和 Codex 使用记录同步。用户说“安装这个 skill”“检查 skill 更新”“把 skill 挂到 Claude/Codex”“更新但保留本地修改”“同步 Codex skill 使用记录”或“卸载 skill”时使用。
---

# Baku Skill Manager

这个 skill 是自然语言入口，实际文件管理必须交给仓库里的 `skills` CLI；不要在对话里手工复制、覆盖或删除 Skill 目录。

## 全局目录合同

- 真实 Skill 文件只放在 `~/.agents/skills/<name>`。
- Codex 使用 `~/.codex/skills/<name>` 软链接。
- Claude Code 使用 `~/.claude/skills/<name>` 软链接。
- manager 状态放在 `~/.agents/.manager/`。
- 不扫描、不管理项目目录里的 Skill。
- 全局扫描会排除 `.DS_Store`、`.agents`、`.claude`、`.packages`、`.playwright` 和 `.system`，这些目录不会被当作 Skill 认领。

## 调用规则

先执行只读命令确认当前状态：

```bash
skills status <name>
skills check <name>
```

官方 `npx skills add` 安装后，使用 `adopt` 认领，而不是再次复制一份：

```bash
skills adopt --skill <name>
skills adopt --skill <name> --source <owner/repo>
# 多个现有目录内容不同时显式选择 canonical 来源
skills adopt --skill <name> --prefer codex --yes
```

如果没有来源，只能登记为 `local-only`，不要猜来源；只有提供准确来源后才允许更新。

## 更新规则

更新前先展示上游 commit、本地改动和差异。更新命令会在本机记录 local commit，并以“上次安装基线 + 本地改动 + 上游新 commit”做三方合并：

```bash
skills diff <name>
skills update <name>
skills resolve <session-id> --ours
skills resolve <session-id> --theirs
```

无冲突部分自动合并；冲突必须保留 pending session，不能静默覆盖。批量更新必须显式使用 `skills update --all`。

启动本地管理页面，并同步 Codex 使用事件：

```bash
skills serve
skills usage sync
```

页面默认启动在 `127.0.0.1:43127`（可用 `skills serve --port <port>` 覆盖），按 Codex 本地会话中的累计使用次数降序展示 Skill，并按分组内最近 60 天使用次数降序排列分组；来源明确时展示 GitHub 地址，无法确认时标记为 `local`。页面支持按分组、名称和 local/remote 来源筛选，可修改分组名称、展开/收起分组、批量同步已绑定云端 Skill，以及通过 skills.sh 为本地 Skill 初始化云端来源。更新、批量操作和移除各弹出一次确认，并沿用 CLI 的三方合并、冲突 session 和本地备份规则。

“同步 Codex 技能使用记录”会扫描本地 Codex 会话并导入结构化使用事件；“同步云端 Skill”只处理已经登记 GitHub 来源的 Skill，行为等同于逐个点击“更新”；“初始化云端 Skill”只处理没有来源的 Skill，会搜索 skills.sh，并在仓库实际包含同名 Skill 后才绑定来源，不会覆盖本地文件。三个操作都会立即返回并在服务端后台执行，页面刷新不会中断，可通过任务状态恢复进度。

`skills usage sync` 只读扫描 `~/.codex/sessions` 和 `~/.codex/archived_sessions`，导入 Codex 会话里结构化的 `<skill>` 触发事件到 `~/.agents/.manager/usage.jsonl`。同步按事件指纹幂等，不会重复计数。历史 Manager 手动事件仍保留在日志中，但不再计入页面统计。

Codex 个人资料页里的“最常用的插件”是账户级分析口径，数字可能高于本地会话中可解析的结构化事件；manager 不会把它们混用，也不会用文件访问时间猜测 Skill 是否被调用。

## 链接和卸载

```bash
skills link <name> --agent claude
skills unlink <name> --agent claude
skills remove <name>
```

目标目录已有真实文件或其他软链接时，默认拒绝覆盖；确认后才使用 `--replace`，并先备份。未指定 Agent 的 `remove` 删除 Codex、Claude 和 canonical 安装；卸载前检测到本地改动时先备份并确认一次。

manager 的 CLI 是唯一执行入口；本 skill 不自己实现 Git、文件复制或删除逻辑。

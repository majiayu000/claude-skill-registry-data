---
name: import-claude-session
description: 把外部机器导出的 Claude Code 原生 session 日志（.jsonl）导入本机，让 universe-editor 的 Agents 视图能加载/恢复该会话。当用户拿来一个别处产生的 claude session jsonl、说「导入会话 / 让编辑器能加载这个 session / 转换 session 格式」时使用。
disable-model-invocation: true
---

# 导入外部 Claude session 到本机编辑器

## 机制（先懂再操作）

- 对话内容只存 agent 侧 Claude Code 原生 transcript：`<CLAUDE_CONFIG_DIR ?? ~/.claude>/projects/<slug>/<sessionId>.jsonl`（`vendor/claude-agent-acp/src/acp-agent.ts` 的 `findTranscriptFile`）。编辑器不复制对话内容。
- slug = `cwd.replace(/[^a-zA-Z0-9]/g, "-")`（cwd 里所有非字母数字字符变 `-`）。
- 编辑器会话列表元数据由 hydrate sweep 调 fork 的 `session/list` 自动 upsert，**不需要手写**；触发时机 = 打开 Agents 视图 / 工作区切换 / 手动刷新。
- resume 时 agent 进程以 entry.cwd 为工作目录、SDK 按 slug 定位 jsonl，所以**文件落盘位置与行内 `cwd` 字段必须一致**——从外部机器导入时必须改写行内 `cwd` 为本机目标工作区路径。
- jsonl 格式要求：一行一个 JSON；消息行 `type: "user"|"assistant"` 必须有字符串 `uuid`，`parentUuid` 链完整（parent 在 child 前）；`system`/`attachment`/`file-history-snapshot`/`queue-operation`/`last-prompt`/`mode` 等非消息行被兼容忽略。

## 头号坑：MAX_ENTRIES=100 淘汰

编辑器历史按 `lastUsedAt` 降序只留 100 条（`apps/editor/src/renderer/services/acp/session/acpSessionHistory.ts` 的 `MAX_ENTRIES`），`lastUsedAt` 取自会话最后一条真实消息的 `timestamp`。**导入的会话若比现存最老条目还旧，merge 后立刻被淘汰，怎么刷新都看不到**（真实案例，2026-07）。因此脚本默认把最后一条消息的 timestamp 拨到现在——这是必要步骤，不是美化。

## 操作步骤

用 skill 目录下的脚本一把梭（纯 node 标准库，无依赖）：

```bash
node .claude/skills/import-claude-session/import-session.mjs \
  <源文件.jsonl> <目标工作区绝对路径> \
  [--title "会话标题"] [--branch 分支名] [--keep-timestamps] [--force]
```

脚本自动完成：
1. 逐行解析校验（消息行 uuid / parentUuid 链完整性，有断裂会警告）
2. 改写所有行内顶层 `cwd` 为目标工作区（规范化：绝对路径 + 盘符大写）
3. `gitBranch` 改为目标目录当前分支（`git rev-parse` 自动探测，可用 `--branch` 覆盖）
4. **把最后一条消息的 timestamp 拨到现在**（逃过 MAX_ENTRIES 截断；`--keep-timestamps` 可关）
5. `--title` 时在文件头注入 summary 行（注意：SDK 可能仍按自己的摘要覆盖标题，属正常）
6. 按 slug 规则写到 `~/.claude/projects/<slug>/<sessionId>.jsonl`（已存在需 `--force`）

## 验证

1. 目标工作区在编辑器里打开 → Agents 视图 → 刷新。
2. 会话应出现在列表**最顶部**（lastUsedAt = 现在）。标题可能是 `--title` 注入的，也可能是 SDK 自己算的摘要。
3. 点击会话走 `session/load` 重放完整历史（含跨 compact 边界），确认消息 / tool_use / thinking 正常。

## 排查（看不到会话时）

按顺序查：
1. 用 vendor 的 SDK 直接验证发现：`cd vendor/claude-agent-acp && node -e "import('@anthropic-ai/claude-agent-sdk').then(m=>m.listSessions({dir:'<目标cwd>'}).then(s=>console.log(s.length, s.find(x=>x.sessionId==='<sid>'))))"`。SDK 看不到 → 文件位置/slug/格式问题。
2. 查编辑器历史存储是否收了它：`grep -l "<sessionId>" "$APPDATA/Universe Editor/workspaces/"*.json`（dev 模式是 `Universe Editor - Dev`）。只出现在 `workbench.recentFiles` = 编辑器没收。
3. 编辑器没收的最大原因就是上面的 MAX_ENTRIES 淘汰——确认导入时没加 `--keep-timestamps`，且刷新动作发生在文件落盘之后。

## 注意

- 不改写消息正文里的旧机器路径引用（历史内容保持原样）。
- 同一 sessionId 已在目标目录存在时需 `--force` 覆盖。
- 源文件可以是 Claude Code CLI / SDK / 另一台机器的 universe-editor 产生的任意原生 session jsonl。

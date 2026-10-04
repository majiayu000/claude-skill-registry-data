---
name: skills-manager
description: >
  Manage all Claude Code skills, MCPs, and plugins by categories (modes).
  Switch categories to enable/disable groups of tools per project.
  Supports natural language: "切换到xxx模式", "把xxx归成一类", "额外开启skill-a", "去掉mcp-b",
  "列出所有分类", "新建一个分类叫xxx", "把xxx加入yyy分类", "分析这个项目应该用什么分类".
  English: "switch to xxx", "create category xxx", "add xxx to yyy", "remove xxx", "list categories".
disable-model-invocation: true
argument-hint: "<command> [args]  e.g. switch research, list, scan, add-category code"
---

# skills-manager

Manage Claude Code skills, MCPs, and plugins by categories. Switch modes to configure project tools.

## Core Concepts

**Category = Mode** — a named set of skills + MCPs + plugins. Switching activates that set for the current project.

**Registry** — skills-manager's record of every tool. Lives in `config/`:
- `skills-registry.json` — skills
- `plugins-registry.json` — plugins  
- `mcp-config.json` — MCP configs

**All** — union of every registered tool. Auto-updated by scan.
**None** — empty set. Disables everything.

## MCP Lifecycle (Important)

Any MCP in `~/.claude.json` is a **global leak** — available to ALL projects. `scan` auto-migrates these to skills-manager config with backup.

```
MCP in ~/.claude.json → scan detects → migrate to mcp-config.json → clear global
```

## Safety Rules

1. Only touch `skillOverrides` and `enabledPlugins` in settings.local.json
2. Only touch `mcpServers` in ~/.claude.json, always backup first
3. MCP deletion requires `--allow-delete-mcp` flag
4. Read → modify → Write, never overwrite

## Dispatch

Parse `$ARGUMENTS` and route to operation. Read `references/operations.md` for full logic.

### Operations

| Command | Trigger |
|---------|---------|
| `scan` | 扫描 |
| `switch <category>` | 切换到<category> |
| `list` | 列出所有分类 |
| `add-category <name>` | 添加分类<name> / create category <name> |
| `delete-category <name>` | 删除分类<name> |
| `edit-category <name>` | 编辑分类 / 把xxx加入yyy |
| `bind <skill> --mcp <mcp>` | 绑定skill和mcp |
| `unbind <skill> --mcp <mcp>` | 解绑 |
| `update <target>` | 更新skills/plugins/all |
| `delete-mcp <name>` | 删除MCP (需 --allow-delete-mcp) |
| `manage <type> on/off` | 管理类型开关 |
| `backup list/clean` | 备份管理 |
| `setup` | 配置项目 / setup project |

### Natural Language Patterns

| User says | Action |
|-----------|--------|
| 切换到xxx模式 / switch to xxx | switch category |
| 把xxx归成一类 / create category xxx | add-category |
| 额外开启xxx / enable xxx | add item as override |
| 去掉xxx / disable xxx | remove item as override |
| 列出所有分类 / list categories | list |
| 把xxx加入yyy / add xxx to yyy | edit-category |
| 分析这个项目 / analyze project | recommend category |

## Reference Files

Read as needed:
- `references/operations.md` — All operation details
- `references/sync-check.md` — Sync check logic
- `references/config-formats.md` — Config file schemas

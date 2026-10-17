---
name: gortex-main-3-dirs
description: "Work in the main +3 dirs area — 52 symbols across 6 files (88% cohesion)"
---

# main +3 dirs

52 symbols | 6 files | 88% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/main/ipc/settings.ipc.ts`
- `src/main/menu.ts`
- `src/main/settings-update.ts`
- `src/main/settings.ts`
- `src/mcp/mcpServer.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | createServer, node:http, isArray, concat, resolve |
| `src/main/ipc/settings.ipc.ts` | picked, registerSettingsHandlers, openDatabaseViaDialog, validation, mcpServer, ... |
| `src/main/menu.ts` | result, openDatabaseFromMenu, submenu.click, win, response |
| `src/main/settings-update.ts` | DbPathUpdate, dbPath, current, withDbPath |
| `src/main/settings.ts` | dir, path, loadSettings, settingsPath, Settings, ... |
| `src/mcp/mcpServer.ts` | mcpService, constructor, mcpServerInstance, httpServer, port, ... |

## Entry Points

- `src/mcp/mcpServer.ts::GraderMcpServer.start`
- `src/main/ipc/settings.ipc.ts::registerSettingsHandlers`

## Connected Communities

- **main/ipc +3 dirs** (2 cross-edges)
- **application +11 dirs** (2 cross-edges)
- **application +6 dirs** (1 cross-edges)
- **infrastructure/persistence +2 dirs** (1 cross-edges)
- **application +10 dirs** (1 cross-edges)
- **domain/grade +3 dirs · hardDeleteStudent** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-56")
explore(operation:"context", task:"understand main +3 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/mcp/mcpServer.ts::GraderMcpServer.start"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._

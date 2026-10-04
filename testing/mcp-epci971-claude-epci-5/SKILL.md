---
name: mcp
description: >-
  MCP (Model Context Protocol) integration for EPCI v4.0. Manages 4 servers
  (Context7, Sequential, Magic, Playwright) with auto-activation based on
  personas and context. Use when: persona detected activation, MCP flags used explicitly,
  trigger files keywords present. Not for: standalone tasks without documentation needs.
allowed-tools: [Read, Glob, Grep, WebFetch, WebSearch]
---

# MCP Integration — Model Context Protocol

## Overview

EPCI integrates 4 MCP servers to enrich context with external data:

| Server | Icon | Function | Primary Use |
|--------|------|----------|-------------|
| [Context7](references/context7.md) | | Library documentation | Patterns, APIs, best practices |
| [Sequential](references/sequential.md) | | Multi-step reasoning | Complex debugging, analysis |
| [Magic](references/magic.md) | | UI component generation | Modern React/Vue components |
| [Playwright](references/playwright.md) | | E2E testing | Browser automation, a11y |

## Activation

### Auto-Activation Matrix (Persona × MCP)

| Persona | Context7 | Sequential | Magic | Playwright |
|---------|:--------:|:----------:|:-----:|:----------:|
| architect | **auto** | **auto** | - | - |
| frontend | **auto** | - | **auto** | **auto** |
| backend | **auto** | **auto** | - | - |
| security | - | **auto** | - | - |
| qa | - | - | - | **auto** |
| doc | **auto** | - | - | - |

**auto** = Auto-activated with persona | **-** = Available on demand

### Flag Triggers

| Flag | MCP Activated |
|------|---------------|
| `--c7` | Context7 |
| `--seq` | Sequential |
| `--magic` | Magic |
| `--play` | Playwright |
| `--think-hard` | Sequential |
| `--ultrathink` | Sequential |
| `--no-mcp` | Disable all |

### Keyword Triggers

| MCP | Trigger Keywords |
|-----|-----------------|
| Context7 | import, require, library, framework, docs |
| Sequential | debug, analyze, investigate, complex, diagnose |
| Magic | component, button, form, modal, table, UI |
| Playwright | e2e, browser, accessibility, test, automation |

### File Pattern Triggers

| MCP | Trigger Patterns |
|-----|-----------------|
| Context7 | `package.json`, `composer.json`, `requirements.txt` |
| Magic | `*.jsx`, `*.tsx`, `*.vue`, `**/components/**` |
| Playwright | `*.spec.ts`, `*.e2e.ts`, `**/tests/**` |

## Configuration

MCP settings in `.project-memory/settings.json`:

```json
{
  "mcp": {
    "enabled": true,
    "default_timeout_seconds": 15,
    "retry_count": 2,
    "servers": {
      "context7": { "enabled": true, "auto_activate": true },
      "sequential": { "enabled": true, "auto_activate": true },
      "magic": { "enabled": true, "auto_activate": true },
      "playwright": { "enabled": true, "auto_activate": true }
    }
  }
}
```

### Per-Server Options

| Option | Default | Description |
|--------|---------|-------------|
| `enabled` | `true` | Enable/disable server globally |
| `auto_activate` | `true` | Allow auto-activation by persona/context |
| `timeout_seconds` | `15` | Request timeout |

## Fallback Behavior

If an MCP server is unavailable:

| MCP | Fallback Strategy | Message |
|-----|-------------------|---------|
| Context7 | Web search | ` Context7 unreachable, using web search` |
| Sequential | Native reasoning | ` Sequential error, using native reasoning` |
| Magic | Basic generation | ` Magic unavailable, basic generation` |
| Playwright | Manual suggestions | ` Playwright down, manual testing` |

### Retry Logic

1. Attempt primary action
2. On failure: retry up to 2 times
3. After retries: activate fallback
4. Log warning, continue workflow

## Breakpoint Display

Active MCP servers shown in FLAGS line:

```
FLAGS: --think-hard (auto) | --c7 (auto: architect) | --seq (auto: 0.72)
```

Legend:
- `(auto: persona)` — Activated by persona
- `(auto: X.XX)` — Activated by scoring
- `(explicit)` — User specified

## Integration Points

### In /brief

After persona detection (Step 5):
1. Calculate MCP activation based on personas
2. Check keyword/file triggers
3. Display in FLAGS line at breakpoint

### In /epci Phases

- **Phase 1**: Load Context7 for architecture patterns
- **Phase 2**: Use Sequential for complex debugging, Magic for UI
- **Phase 3**: Context7 for documentation standards

### In /quick

Lightweight MCP activation for SMALL features only.

## Quick Reference

```bash
# Enable specific MCP
/epci --c7                 # Context7 only
/epci --seq                # Sequential only
/epci --magic              # Magic only
/epci --play               # Playwright only

# Combine with personas
/epci --persona-frontend   # Auto: Magic + Playwright

# Disable all MCP
/epci --no-mcp

# Check available MCPs
# Shown automatically in breakpoints
```

---

*MCP Integration v1.0 — F12 Implementation*

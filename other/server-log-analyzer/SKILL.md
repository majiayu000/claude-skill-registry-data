---
name: server-log-analyzer
description: "Workflow for classifying AI Matrx server log lines in features/server-logs/log-rules.ts. Use when examining raw server logs, new [ModuleName] bracket tokens appear unclassified, log categories are wrong, or adding module recognition to the log viewer."
---

# Server Log Analyzer

Analyzes raw logs from the AWS CloudWatch production services and the residual Coolify stream/scraper services, and keeps the parsing system in sync. `CoolifyLogViewer.tsx` is a legacy component name, not a statement that the primary server still runs on Coolify.

## Two files to update

| File | Purpose |
|------|---------|
| `features/server-logs/log-rules.ts` | Parser, module map, categories, colors, regexes |
| `components/admin/server-logs/CoolifyLogViewer.tsx` | `CATEGORY_LABELS` Record (display names) |

---

## Step 1 — Scan the logs

Read through the raw log sample. For each distinct `[BracketToken]` found, record:

```
[ModuleName]  →  dotted.module.path (if present)  →  pattern description
```

Example discovery table from production logs:

| Bracket token | Module path | Pattern | Category |
|---|---|---|---|
| `[ApiPrefixCompat]` | `aidream.api.middleware.api_prefix_compat` | Rewriting '/api/...' → '/...' | `compat` |
| `[AuthMiddleware]` | — | Request/JWT accepted/rejected | `auth` |
| `[Request]` | — | METHOD /path: + JSON body | `request` |
| `[Stream Emitter]` | — | Status Update / Data / Completion / End + JSON | `stream` |
| `[CHAT ROUTER]` | `aidream.api.routers.chat` | conversation_id=... | `ai-execution` |
| `[Google Chat]` | — | executing, with debug: ... | `ai-execution` |
| `[ToolRegistryV2]` | `matrx_ai.tools.registry` | N requested tool(s) not found | `ai-execution` |
| `[AI Task]` | — | Cache updated / Completion | `ai-execution` |
| `[DEBUG EXECUTE UNTIL COMPLETE]` | `matrx_ai.orchestrator.executor` | Current Debug Setting: + value | `ai-execution` |
| `[ConversationGate]` | — | Auto-created / Ensured user_request | `cx` |
| `[ConversationLabeler]` | — | Labeled conversation ... | `cx` |
| `[CX PERSISTENCE PERSIST COMPLETED REQUEST]` | — | Saved Conversation + IDs | `cx` |
| `[UNRECOGNIZED]` | `aidream.api.utils.field_warnings` | Unknown field 'x' (path=...) | `config` |
| `[uvicorn.access]` | — | IP:PORT - "METHOD /path HTTP/1.1" STATUS | `system`/`request` |

---

## Step 2 — Identify the echo pattern

Many of our logs currently emit two lines per event:

```
2026-04-03 20:28:52 [WARNING] [aidream.api.middleware.api_prefix_compat] [ApiPrefixCompat] Rewriting '/api/ai/chat' → '/ai/chat' — update ...
[ApiPrefixCompat] Rewriting '/api/ai/chat' → '/ai/chat' — update ...
```

The second line is the **bare echo** — no timestamp, no level, no module path. The parser handles these as `UNKNOWN` level standalone lines. Flag them in your report but do not strip them — they must pass through to `raw` untouched.

---

## Step 3 — Update `MODULE_CATEGORY_MAP` in log-rules.ts

Add new entries to the map. Keys are the exact bracket token string (case-sensitive, including spaces):

```typescript
const MODULE_CATEGORY_MAP: Record<string, LogCategory> = {
  // existing ...
  "CHAT ROUTER":    "ai-execution",
  "Google Chat":    "ai-execution",
  ToolRegistryV2:   "ai-execution",
  "AI Task":        "ai-execution",
  "DEBUG EXECUTE UNTIL COMPLETE": "ai-execution",
  ConversationGate:    "cx",
  ConversationLabeler: "cx",
  "CX PERSISTENCE PERSIST COMPLETED REQUEST": "cx",
  UNRECOGNIZED:     "config",
  UnifiedConfig:    "config",
};
```

## Step 4 — Add new LogCategory values (if needed)

If you find patterns that don't fit existing categories, add them to:

1. `LogCategory` type union in `log-rules.ts`
2. `ALL_CATEGORIES` array in `log-rules.ts`
3. `categoryToColor()` switch in `log-rules.ts`
4. `CATEGORY_LABELS` Record in `CoolifyLogViewer.tsx`

Current categories and colors:

| Category | Color | Meaning |
|---|---|---|
| `request` | `text-cyan-300` | HTTP request/response |
| `stream` | `text-purple-300` | SSE / stream emitter |
| `auth` | `text-green-300` | JWT, session, fingerprint |
| `compat` | `text-amber-400` | API path rewriting |
| `database` | `text-teal-300` | DB queries |
| `system` | `text-neutral-400` | uvicorn, health, startup |
| `error` | `text-red-400` | exceptions, tracebacks |
| `ai-execution` | `text-violet-300` | model calls, tool registry, chat router |
| `cx` | `text-sky-300` | conversation lifecycle, CX persistence |
| `config` | `text-orange-300` | unrecognized fields, config warnings |
| `json-payload` | `text-neutral-500` | JSON continuation lines |
| `general` | level color | everything else |

## Step 5 — Update inferCategory() heuristics

For module names that appear without a module path (bare echo lines), add heuristic patterns:

```typescript
// AI execution — bare echo lines with no module path
if (/\b(executing|tool.?registry|chat.?router|google.?chat)\b/i.test(raw)) return "ai-execution";
// CX lifecycle
if (/\b(conversation.?gate|conversation.?label|cx.?persist)\b/i.test(raw)) return "cx";
// Config / field validation
if (/\bUnrecognized\b|\bunknown.?field\b/i.test(raw)) return "config";
```

## Step 6 — Verify regex for bracket names with spaces

The `RE_MODULE_SHORT` regex must allow spaces inside brackets:

```typescript
// Handles: [ApiPrefixCompat], [CHAT ROUTER], [Stream Emitter],
//          [AI Task], [CX PERSISTENCE PERSIST COMPLETED REQUEST]
const RE_MODULE_SHORT = /^\[([A-Za-z][A-Za-z0-9_ ]*?)\]\s*/;
```

---

## Step 7 — Produce the migration report

After updating the parser, produce a report for the Python backend team listing every pattern that should be standardized. Format:

```markdown
## Log Migration Report — [date]

### Echo Pattern (HIGH PRIORITY)
Every log currently emits two lines — the structured line and a bare echo.
Fix: Remove the bare echo from all Python loggers.

Pattern to remove:
  [ModuleName] message text     ← no timestamp, no level

### Module Name Standardization

| Current bracket token | Recommended [ShortName] | Module path to add |
|---|---|---|
| [CHAT ROUTER] | [ChatRouter] | aidream.api.routers.chat |
| [DEBUG EXECUTE UNTIL COMPLETE] | [ExecutorDebug] | matrx_ai.orchestrator.executor |
| [CX PERSISTENCE PERSIST COMPLETED REQUEST] | [CxPersistence] | matrx_ai.cx.persistence |
| [UNRECOGNIZED] | [FieldValidator] | aidream.api.utils.field_warnings |
| [AI Task] | [AiTask] | matrx_ai.tasks (or current module) |
| [Google Chat] | [GoogleChat] | matrx_ai.providers.google |
| [ConversationGate] | [ConversationGate] | ✓ already CamelCase |
| [ConversationLabeler] | [ConversationLabeler] | ✓ already CamelCase |

### Required Log Format per Module

Replace:
  [CHAT ROUTER] conversation_id=86c092d0...

With:
  2026-04-03 20:28:52 [INFO] [aidream.api.routers.chat] [ChatRouter] conversation_id=86c092d0...

### JSON Payload Entries Without Headers
Some entries start directly with a JSON block (no header line ending in ':').
These should always be preceded by a header line:

  [ToolRegistryV2] 1 requested tool(s) not found:      ← add this
  {
      "missing_tools": [...]
  }
```

---

## Quick reference — log format spec

```
TIMESTAMP [LEVEL] [module.path] [ShortName] MESSAGE
```

- **TIMESTAMP**: `2026-04-03 20:28:52` (no sub-second required, but accepted)
- **[LEVEL]**: `[DEBUG]` `[INFO]` `[WARNING]` `[ERROR]` `[CRITICAL]`
- **[module.path]**: lowercase dotted Python path, e.g. `[aidream.api.routers.chat]`
- **[ShortName]**: CamelCase, no spaces, max ~20 chars, e.g. `[ChatRouter]`
- **MESSAGE**: ends with `:` if a JSON block follows on the next line

For JSON payloads, the block must immediately follow the header with no blank line between.

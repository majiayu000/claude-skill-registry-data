---
name: omni-bus
description: How to use the omni plugin bus (custom tools, hooks, trace log) for observability, secret redaction, and cross-tool composition
---

# Omni Plugin Bus

All tool calls flow through `.opencode/plugins/omni.ts` via `tool.execute.before/after`.

## What it gives you for free

- **Secret redaction** — tool outputs are scrubbed of API keys, JWTs, Postgres URIs before reaching the model
- **Audit log** — every tool call goes to `vault/60-Observability/tool-trace.jsonl`
- **Post-edit nudges** — editing `workflows/*.json` or `db/migrations/*.sql` appends to `vault/60-Observability/nudges.log`
- **Session compaction preamble** — RESTO BOT state (branch, phase, stack) is injected into every compaction
- **Env injection** — `DATABASE_URL`, `N8N_API_KEY`, `OPENROUTER_API_KEY` are injected into shell calls without appearing in transcripts

## Custom tools exposed

| Tool | Use when |
|------|----------|
| `restaurant_status` | Quick health fan-out (git + docker compose + vault paths) |
| `repo_snapshot` | Compact repo state for session start |
| `vault_append` | Append to any `vault/` file, auto-creates dirs |
| `nid_create` | Create NID note in `vault/10-Queue/` with frontmatter |

## Composition pattern

```
/command → agent → skill (this one) → custom tool or MCP
                                         ↓
                           tool.execute.before  ← branch-guard blocks destructive ops
                                         ↓
                           tool.execute.before  ← omni redacts + audits
                                         ↓
                                    [tool runs]
                                         ↓
                           tool.execute.after   ← omni redacts output + nudges
```

## When NOT to use custom tools

- For simple git commands use `bash` directly (branch-guard has your back)
- For reading code use `read`/`grep` — don't route through plugin tools
- Use `restaurant_status` only at session start or on demand — it's heavy

---
name: healthcheck
description: "Check Selma's system health: Ollama reachability, configured model availability, config validity, workspace files, loaded skills, session store, and gateway status. Trigger on: healthcheck, health check, /healthcheck, alles ok, status check, ist selma ok, system status."
user-invocable: true
---

# Selma Health Check

## Instructions

Call ALL tools first without producing any intermediate output.
Collect all results, then write ONE complete report at the end.

## Tool calls (execute all, in order)

1. `web_fetch` → `http://localhost:11434/api/tags`
2. `read` → `../selma.json`
3. `ls` → `./`
4. `ls` → `skills/`
5. `read` → `../agents/main/sessions/sessions.json`
6. `web_fetch` → `http://localhost:8000/`

## Report (write after all tools completed)

```
Selma Health Check
──────────────────────────────────────

✅/❌/⚠️  Ollama:    <reachable — N models> or <not reachable>
✅/❌/⚠️  Modell:    <model name> — <found / not found in Ollama>
✅/❌/⚠️  Config:    selma.json — <valid / error: ...>
✅/❌/⚠️  Workspace: <N files> — <missing: X, Y if any>
✅/❌/⚠️  Skills:    <N loaded: name1, name2, ...> or <none>
✅/❌/⚠️  Sessions:  <N sessions> or <no sessions yet>
✅/❌/⚠️  Gateway:   <running on :8000 / not reachable>

Status: OK / DEGRADED / ERROR
```

**Status rules:**
- `OK` — all ✅ (⚠️ on sessions or gateway still counts as OK)
- `DEGRADED` — at least one ⚠️ on workspace or skills
- `ERROR` — at least one ❌ (Ollama, model, or config)

## Notes
- Continue even if a tool call fails — use ❌ for that check.
- Expected workspace files: AGENTS.md, SOUL.md, IDENTITY.md, TOOLS.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md
- Do not suggest fixes unless the user asks.

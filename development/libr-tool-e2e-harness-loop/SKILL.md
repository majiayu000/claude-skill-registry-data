---
name: libr-tool-e2e-harness-loop
description: >
  Run a repeatable LibrAgent builtin-tool E2E harness via libr-delegate: instruct
  a live Session API session, extract the transcript, write an evidence-backed
  postmortem, derive ranked tool-improvement tasks, optionally patch, then re-run.
  Use when the user asks for tool E2E harness loops, browser/userChrome extension
  E2E cycles, postmortem-driven tool fixes, or "E2E → 분석 → 과제 → 반복".
  Depends on a running LibrAgent and the Cursor-only libr-delegate skill.
  Not for Harbor/ATIF job analysis (use harbor-harness-improvement-loop) and not
  for in-app agent__* delegation.
---

# Libr Tool E2E Harness Loop

Cursor-owned loop for **live builtin MCP tools** against a running LibrAgent:

**E2E instruct → transcript extract → postmortem → improvement tasks → (patch) → re-run**

Optimize tool contracts (schema, handler, hints, bridge/backend), not model choice.

## When to use

- Verify a tool surface after a merge/rebuild (e.g. browser `userChrome` / `sidecar`)
- Turn a failed/partial E2E into a ranked fix backlog
- Drive short improvement cycles with measurable re-E2E

## Dependencies

| Need | Skill / precondition |
| --- | --- |
| Spawn/poll/cleanup session | `libr-delegate` (read + follow it) |
| Builtin design critique after root-cause | `critique-builtin-tool` / `refactor-builtin-tool` as needed |
| Harbor job ATIF analysis | **Not this skill** → `harbor-harness-improvement-loop` |

LibrAgent must be up (`GET /api/health`). Prefer `executionMode: yolo` for unattended E2E.

## Hard rules

- Self-contained `request` text only — child session does not see Cursor chat.
- Always pass absolute `workspacePath` when the E2E needs the repo.
- **Extract** `GET …/messages?limit=500` **before** terminate+delete.
- Artifacts under `.libragent/work/tool-e2e-harness/<cycle-id>/` only (unless user asks otherwise).
- Separate **fact** (tool result text) / **interpretation** / **hypothesis**.
- One primary causal patch per cycle when implementing; ask before large product edits.
- Do not run `pnpm refactor:validate` unless the user explicitly asks.
- Stop looping when acceptance criteria pass, max cycles hit, or user aborts.

## Cycle

Default max cycles: **3** (override if user says). Freeze a `cycle-id` like `20261003-browser-userchrome-1`.

### 0. Freeze the harness contract

Write `.libragent/work/tool-e2e-harness/<cycle-id>/contract.md`:

- App version / branch / “fresh rebuild?” note
- Target tools + backends (e.g. `browser__createSession` with `browser=userChrome|sidecar`)
- Preconditions (extension Connected, bridge `:3847`, network)
- Pass/fail matrix + contamination rules (no silent backend swap)
- Out of scope

### 1. Instruct E2E via libr-delegate

Follow `libr-delegate`. Brief template: [references/e2e-brief.md](references/e2e-brief.md).

Requirements for every brief:

- Explicit tool names and required args (`browser=userChrome` etc.)
- Harmless fixtures only unless user authorizes otherwise
- Mandatory final markdown: Verdict / Runtime / Tool matrix / Failures / Contamination
- “No codebase archaeology” unless the cycle is analysis-only

Create session → poll to Idle/Error/Paused → on Paused resume once.

### 2. Extract transcript

```bash
PORT=$(cat ~/.libragent/http_port 2>/dev/null || echo 3030)
BASE="http://127.0.0.1:${PORT}"
curl -sS "$BASE/api/sessions/$SID/messages?limit=500" \
  > ".libragent/work/tool-e2e-harness/<cycle-id>/messages.json"
# save final assistant markdown as report-raw.md
curl -sS -X POST "$BASE/api/sessions/$SID/terminate"
curl -sS -X DELETE "$BASE/api/sessions/$SID"
```

### 3. Postmortem

Write `postmortem.md` using [references/postmortem.md](references/postmortem.md).

Rebuild `intent → tool call → observation → next tool` from messages (not memory).

Classify each failure:

| Class | Meaning |
| --- | --- |
| `precondition` | Env not ready (extension offline, app old build) |
| `contract_lie` | Success/status disagrees with observed state |
| `capability_gap` | Documented unsupported path |
| `schema_guidance` | Agent mis-called due to description/schema |
| `handler_bug` | Wrong backend behavior |
| `contamination` | Wrong backend/session identity |
| `harness` | Bad brief / flake / timeout |

Map owning layer (narrowest): schema → description/hints → MCP handler → service/bridge → extension/SW → docs/settings.

### 4. Derive improvement tasks

Write `tasks.md` using [references/improvement-backlog.md](references/improvement-backlog.md).

Rank: **blocker > major > nit**. Prefer contract_lie / contamination / handler_bug over prompt-only tips.

Each task needs: evidence pointer, owning paths, proposed minimal change, re-E2E acceptance check, confidence.

### 5. Act (only if user approved patching this cycle)

1. Smallest fix for the top task (or the user-named task).
2. Focused tests (`pnpm rust:test --test …` / targeted lint).
3. Note reload requirements (e.g. Chrome extension Reload).
4. Bump `cycle-id`, return to step 0/1 with the same matrix + regression checks.

If user asked for planning only: stop after `tasks.md` and summarize.

### 6. Compare cycles

When a prior `postmortem.md` exists, write `delta.md`:

- matrix cells that flipped PASS↔FAIL
- new failures introduced
- tasks closed / still open

## Outputs (per cycle)

```
.libragent/work/tool-e2e-harness/<cycle-id>/
  contract.md
  messages.json
  report-raw.md          # final assistant deliverable
  postmortem.md
  tasks.md
  delta.md               # from cycle 2+
```

## Cursor summary to user

Keep short:

1. Verdict + contamination
2. Top 1–3 tasks (severity + path)
3. Whether another E2E cycle is warranted and what must be reloaded/rebuilt

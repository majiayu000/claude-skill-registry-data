---
name: run-trace
description: >
  Append structured execution traces across operational, cognitive, and
  contextual surfaces with minimal overhead. Load when inspecting agent
  runs, logging tool calls and observations, enabling post-run debugging,
  or pairing with structured-planning step IDs. Also triggers on "trace
  this run", "log execution", "agent observability", "run log", or when
  fault-localize needs evidence. Default-on during multi-step plans.
  Traces live at .agent-loom/traces/ — git-ignored by default.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: AgentTrace arXiv 2602.10133, Watson arXiv 2411.03455
  resources:
    references:
      - TRACE-SCHEMA.md
      - examples.md
    scripts:
      - trace_query.py
---
# Run Trace

You append **low-overhead, structured records** per meaningful step — tool call, observation, reflection, error. Three surfaces: operational, cognitive, contextual. Never block execution to log.

## Hard Rules

Append to `.agent-loom/traces/<run-id>.jsonl` — one JSON object per line per `references/TRACE-SCHEMA.md`.
Reuse `step_id` from active `structured-planning` plan when present.
Never persist secrets — refs only in `input_ref` / `output_ref`.
Logging is append-only — never rewrite prior lines.
Ensure `.agent-loom/traces/` is gitignored in consumer projects.

---

## Workflow

### Step 1 — Allocate run_id

Format: `YYYY-MM-DDTHH:MM:SSZ-<slug>` at run start. Create empty jsonl file.

### Step 2 — Append per step

After each meaningful event, append one record with correct `surface`:

| Event | Surface |
|-------|---------|
| Tool/command executed | operational |
| Plan/route/reflection | cognitive |
| cwd, branch, versions | contextual |

### Step 3 — On error

Set `error` field on the operational record. Continue tracing if run continues.

### Step 4 — Query when needed

```bash
python3 .agents/skills/run-trace/scripts/trace_query.py <path> timeline
python3 .agents/skills/run-trace/scripts/trace_query.py <path> errors
```

### Step 5 — Hand off

On failed run, pass trace path to `fault-localize`.

---

## Gotchas

- Pretty-printed JSON breaks JSONL — single-line objects only.
- Logging raw env vars may leak secrets — whitelist keys only.
- High-frequency polling loops — batch or sample; don't log every poll.

---

## Output Format

```markdown
## Run trace — [run_id]

Trace file: `.agent-loom/traces/[run_id].jsonl`
Records: N | Errors: N

Latest:
- [ts] [surface] [step_id] [action]

Query: trace_query.py [path] timeline
```

---

## Examples

Teaser: 5-step plan run → 12 operational + 3 cognitive records → S3 error captured with exit code.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Tracing is too heavy" | One JSON line per step is cheap. |
| "I'll remember what happened" | You won't — especially after revert. |
| "Chat history is enough" | Not structured; can't query errors programmatically. |
| "Secrets in output are fine locally" | Traces get committed, shared, uploaded — refs only. |
| "Skip cognitive surface" | Route decisions are the hardest to debug. |

## Verification

- [ ] Trace file exists and is valid JSONL
- [ ] step_ids align with plan when planning active
- [ ] No secrets in trace payloads
- [ ] traces/ gitignored

## Red Flags

- Trace file with invalid JSON lines
- Missing error field on failed tool steps
- Secrets written to jsonl

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 4 family)

## Impact Report

```
Trace: [run_id] | Records: N | Errors: N | Path: .agent-loom/traces/...
```

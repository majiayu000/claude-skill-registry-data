---
name: trace
description: Agent execution tracing — timeline, token/cost tracking, replay, and diff for multi-agent observability
model: sonnet
---

<Purpose>
x-trace tracks xm tool executions across two artifacts:
- **Per-session traces** in `.xm/traces/*.jsonl` — `session_start` when an xm skill is invoked, one `agent_step` per Agent tool call made before the assistant turn ends (role, model, `duration_ms`, `status`), and `session_end` at the turn's Stop hook, all written by the trace-session hook with a git snapshot per session. Tokens and cost are estimates: the hook payload carries neither. These power the timeline / cost / replay / diff views, which the LLM renders by parsing JSONL.
- **A cross-tool activity ledger** in `.xm/last.json` — which tool last ran, on which commit, and how far HEAD has moved since. This is maintained by the `x-trace` CLI (`record` / `last` / `status` / `since` / `doctor`), not by LLM parsing.
No external dependencies.
</Purpose>

<Use_When>
- User wants to trace or observe multi-agent execution
- User says "trace", "execution log", "check cost", "token usage", "show timeline"
- User wants to compare two runs ("diff", "compare before and after")
- User wants to prepare a replay artifact or compare supplied replay result metadata
- Other xm skills want to record agent calls for observability
</Use_When>

<Do_Not_Use_When>
- Simple single-step tasks with no agent fan-out
- Cost tracking for non-xm workflows
- Real-time monitoring (x-trace is post-hoc, not live)
</Do_Not_Use_When>

# x-trace — Agent Execution Tracing

## Model Routing

| Subcommand | Model | Reason |
|------------|-------|--------|
| `cost`, `diff` | **haiku** (Agent tool) | Read-only log parsing and display |
| `list`, `show`, `record`, `last`, `status`, `since`, `doctor` | **haiku** (Agent tool) | Deterministic CLI output — script decides, model relays |
| `replay` | **sonnet** | Audits replay inputs and supplied result provenance |

For haiku-eligible commands, delegate via: `Agent tool: { model: "haiku", prompt: "Run: [command]" }` <!-- managed-model: writer -->

Two command families:
- **LLM-rendered views** (`cost` / `diff` / `start` / `stop` / `clean`) — the LLM reads `.xm/traces/*.jsonl` with the Bash/Read tools and renders the output described in each subcommand file.
- **CLI-backed commands** (`list` / `show` / `record` / `last` / `status` / `since` / `doctor` / `drift`) — run `x-trace-cli.mjs` through the `xm` dispatcher; the LLM only relays what the script prints. `xm trace list` and `xm trace show <session-id>` are the entry points for browsing sessions. See [Activity Ledger (CLI)](#activity-ledger-cli).

No external dependencies. Works as long as the `.xm/` directory exists.

## Mode Detection

Read mode from `.xm/config.json` (`mode` field). Default: `developer`.

**Developer mode**: Use technical terms (trace, timeline, token, replay, diff, JSONL). Concise.

**Normal mode**: Use plain Korean for guidance.
- "trace" → "실행 기록", "timeline" → "시간순 보기", "token" → "토큰", "replay" → "다시 보기"
- "diff" → "비교", "cost" → "비용"
- Use "~하세요" sentence style; lead with the most important information first

### Korean output style (avoid AI-slop)

Universal (both modes) — these read as machine-generated in any register:
- Drop empty intensifiers ("매우 / 완벽하게 / 강력한 / 원활하게 / 혁신적인") unless they carry a specific, real claim.
- No forced rule-of-three or "~뿐만 아니라 ~까지" balance that adds no fact.
- No hedged non-conclusions ("결국 상황에 따라 다르다 / 균형이 필요하다"). End on a concrete fact, number, or next action.

Developer mode: terse and direct — lead with the result; state findings/actions without a 권고형 결말 pile-up ("~해야 한다" sentence after sentence).
Easy/normal mode: accessible Korean is the goal — polite guidance ("~해 보세요"), one line of context for non-experts. Keep commands, flags, paths, and proper nouns in English; on first use write a domain term as Korean(original), e.g. 결론(verdict). Still apply the universal rules; accessible ≠ padded or vague.

## Arguments

User provided: $ARGUMENTS

## Routing

Determine the subcommand from the first word of `$ARGUMENTS`:

- `record`, `last`, `status`, `since`, `doctor`, `drift` → [Activity Ledger (CLI)] — run `xm trace <subcommand>` and relay its output
- `start` → [Subcommand: start]
- `stop` → [Subcommand: stop]
- `show` → [Subcommand: show]
- `cost` → [Subcommand: cost]
- `replay` → [Subcommand: replay]
- `diff` → [Subcommand: diff]
- `list` → [Subcommand: list]
- `clean` → [Subcommand: clean]
- Empty input or `help` → [Subcommand: help]
- Anything else → `show` (display latest session)

---

## Subcommand: help

See `subcommands/help.md` — command reference and usage examples.

---

## Subcommand: start

See `subcommands/start.md` — starts a new named trace session and writes the `.active` pointer.

---

## Subcommand: stop

See `subcommands/stop.md` — stops the active session and writes session_end entry.

---

## Subcommand: show

See `subcommands/show.md` — renders ASCII timeline with token/cost totals.

---

## Subcommand: cost

See `subcommands/cost.md` — per-agent cost table with token rates and totals.

---

## Subcommand: replay

See `subcommands/replay.md` — prepares a replay manifest and snapshot. The CLI does not invoke an agent; report that limit when the user asks to reproduce an execution.

---

## Subcommand: diff

See `subcommands/diff.md` — side-by-side metric comparison of two sessions with delta.

---

## Subcommand: list

See `subcommands/list.md` — tabular listing of all saved sessions with duration and cost.

---

## Subcommand: clean

See `subcommands/clean.md` — finds old trace files and deletes with confirmation.

---

## Activity Ledger (CLI)

`record` / `last` / `status` / `since` / `doctor` are backed by `x-trace-cli.mjs`, which reads and writes `.xm/last.json` — a per-tool "last activity" pointer map, distinct from the per-session `.xm/traces/*.jsonl` files. Run them through the `xm` dispatcher and relay the output; do not re-implement their logic in Bash.

> **⚠ Call `xm trace <command>` directly (or the `xm last` / `xm status` shortcuts). Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`xmt()`) defined in one call do NOT persist to the next, causing `command not found: xmt`. Never define a helper across calls; always use the dispatcher.**
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses, so don't rely on it bare):
> ```bash
> XMT_CLI=$(ls -d ~/.claude/plugins/cache/xm/{trace,xm}/*/lib/x-trace-cli.mjs 2>/dev/null | sort -V | tail -1)
> node "$XMT_CLI" last [args]
> ```
>
> **Forbidden:** `XMT="node ..."; $XMT last` — zsh treats the quoted string as a single command and fails.

| Command | What it does |
|---------|-------------|
| `xm trace list [--limit N] [--json]` | Recent trace sessions newest first: started, skill, status (`open` when no `session_end`), agent count, duration, session id. Malformed or oversized JSONL lines are skipped and counted in a trailing note. |
| `xm trace show <session-id> [--json]` | One session (exact id or unique prefix): row-type counts, git snapshot, and every `agent_step` with role, model, duration, status, description. |
| `xm trace record <tool> [--ref R] [--status S] [--note N] [--artifact A] [--session S]` | Write a tool's latest-activity pointer. Best-effort: an omitted `--ref` defaults to the current git HEAD; a lock contention or unknown tool name warns but still exits 0. |
| `xm last [tool] [--json]` | One line per tool (ref, status, relative age), or the raw map with `--json`. Shortcut: `xm last`. |
| `xm status [--json]` | Commits on HEAD since each tool last acted. Shortcut: `xm status`. |
| `xm trace since <ref>` | Tools + trace sessions recorded after `<ref>`'s commit time. |
| `xm trace doctor [--rebuild]` | Validate `last.json`; `--rebuild` reconstructs it from traces that recorded a git head. |
| `xm trace drift [--window 7d] [--baseline 28d] [--min-samples 5] [--axis …] [--fail-on-flag] [--json]` | Drift check: the recent window vs the period before it, per (skill/role/model) p50 latency & tokens, per-skill error rate, per (rubric/strategy) judged quality, per-lens review precision, per (model/role) estimated cost. A flag needs ≥ min-samples on both sides; thresholds are candidates until simulator-calibrated (say so when relaying). Appends a numeric snapshot to `.xm/metrics/drift.jsonl`; `--fail-on-flag` exits 2 for CI. Model *version* is never recorded (the Agent tool returns a label only) — the snapshot carries the xm plugin version instead. |

A record auto-chains `base` to the tool's previous head. If that base is unreachable (rebase / force-push), the record is flagged `chain_broken` and shown with `⚠ chain broken` — a signal to re-establish the tool's baseline.

### Coverage — what the ledger catches

The ledger is honest about its blind spots: it only knows about activity that ran through the dispatcher or an explicit `record`.

| Activity | In `last.json`? | Why |
|----------|:---------------:|-----|
| Mutating `xm <plugin> <cmd>` (e.g. `xm build tasks update`) | ✅ as `dispatcher` | The dispatcher's EXIT trap records after every mutating command. |
| Explicit `xm trace record <tool>` | ✅ as `<tool>` | Direct ledger write — e.g. x-review's mandatory record contract. |
| Read-only / meta `xm` commands (`help`, `version`, `last`, `status`, `trace`, `dashboard`, `init`, `update`, `doctor`, `which`) | ❌ | Deliberately excluded — no mutating activity to attribute. |
| Read-only sub-ops (`… list` / `… get` / `… show`) | ❌ | Excluded at the `$1`/`$2` verb position to avoid logging queries. |
| Direct `node x-*-cli.mjs …` (bypassing `xm`) | ❌ | Skips the dispatcher EXIT trap entirely. |
| LLM-only skill reasoning with no CLI call (an x-op strategy, x-review's analysis) | ❌ unless it calls `xm trace record` | Nothing runs through the dispatcher. |
| `session_start` / `session_end` in `.xm/traces/` | ✅ (traces) | Written by the trace-session hook; `doctor --rebuild` can reconstruct `last.json` from the git-bearing ones. |
| Agent tool calls between an xm skill's invocation and the end of that assistant turn | ✅ (traces, `agent_step`) | Written by the trace-session hook (matcher `Skill\|Agent` + `Stop`) with `role`, `model`, `duration_ms`, `status` (one of `success`, `error`, `launched`, `unknown`, `abandoned` — see Automatic Checkpoints for the meaning of each), `source: "hook"`. Tokens and cost are not in the hook payload. Agent calls outside such a window are not recorded. |

When ledger output is empty or partial, the CLI appends a coverage note (`activity may exist that was never recorded`). Surface it — do not present the ledger as a complete record.

---

## Data Model

### Storage path

```
.xm/traces/
├── {session-name}-{YYYYMMDD-HHMMSS}.jsonl   # Per-session trace file
├── {session-name}-{YYYYMMDD-HHMMSS}.jsonl   # ...
└── .active                                   # Current active session file path
```

### JSONL entry schema

Each line is an independent JSON object:

```json
{
  "id": "t-001",
  "timestamp": "2026-03-25T12:00:00Z",
  "type": "agent_call",
  "parent_id": null,
  "agent": {
    "role": "security",
    "model": "sonnet"
  },
  "input_tokens_est": 2500,
  "output_tokens_est": 800,
  "duration_ms": 12000,
  "status": "completed",
  "source": "x-op:review",
  "step": 1
}
```

### Entry types (type field)

| type | Description | Required fields |
|------|------|-----------|
| `session_start` | Session start | `session`, `status` |
| `session_end` | Session end | `status`, `total_entries` |
| `agent_call` | Agent invocation | `agent`, `step`, `source` |
| `fan_out` | Parallel agent group start | `count`, `source` |
| `synthesize` | Result aggregation step | `parent_id`, `step` |
| `checkpoint` | Manual recording point | `label` |

### Status values (status field)

| status | Icon | Description |
|--------|--------|------|
| `completed` | ✅ | Completed successfully |
| `failed` | ❌ | Failed |
| `running` | 🔵 | Running |
| `skipped` | ⏭️ | Skipped |
| `active` | 🟢 | Session active |

---

## Integration with other xm tools

x-trace can be used by other xm skills to record entries before and after agent calls.

### x-op integration example

When executing x-op's `review` strategy:

```bash
# Record fan-out start
echo '{"id":"fo-001","timestamp":"...","type":"fan_out","count":4,"source":"x-op:review","step":1}' >> .xm/traces/.active-file

# Record after each agent completes
echo '{"id":"t-001","timestamp":"...","type":"agent_call","parent_id":"fo-001","agent":{"role":"security","model":"sonnet"},...}' >> .xm/traces/.active-file
```

### x-build integration example

Automatically records each task agent call when x-build's `run` command executes.

---

## Auto-recording event guide

Events each xm plugin should record:

### x-op strategy execution
| Event | Trace type | When to record |
|--------|-----------|----------|
| Strategy start | `session_start` | Immediately after `/xm:op {strategy}` is called |
| Fan-out call | `fan_out` | When N agents are invoked concurrently (includes agents[], prompt) |
| Delegate call | `agent_call` | When a single agent is invoked (role, model, prompt) |
| Round synthesis | `synthesize` | When the leader synthesizes results (round, summary) |
| Checkpoint save | `checkpoint` | When saving a checkpoint for `--resume` |
| Strategy complete | `session_end` | When final output + Self-Score is complete (total_cost, duration) |

### x-build task execution
| Event | Trace type | When to record |
|--------|-----------|----------|
| Run start | `session_start` | When `x-build run` is called (step_id, task_count) |
| Agent spawn | `agent_call` | When each task agent is spawned (task_id, role, model) |
| Task complete | `agent_call` + `status: done` | On `tasks update --status completed` callback |
| Task failure | `agent_call` + `status: failed` | On failure, includes error_message |
| Step complete | `checkpoint` | When all tasks in the current step are complete |

### x-review review
| Event | Trace type | When to record |
|--------|-----------|----------|
| Review start | `session_start` | When `/xm:review diff` is called |
| Per-lens review | `fan_out` | When per-agent review is invoked (lens, model) |
| Final verdict | `synthesize` | When verdict is determined (findings_count, verdict) |

## Cost alert rules

Warn when cumulative cost exceeds thresholds during trace recording:

| Threshold | Action |
|--------|------|
| `budget × 50%` | `💡 50% of budget used: $X / $Y` (info) |
| `budget × 80%` | `⚠ 80% of budget used: $X / $Y` (warning) |
| `budget × 100%` | `🚨 Budget exceeded: $X / $Y — continue?` (confirmation required) |

Budget is read from `budget.max_usd` in `.xm/config.json`. No alerts if unset.

Automatic cost summary on session end:
```
📊 Session cost: $0.42 (input: 180K, output: 45K tokens)
   Budget: $0.42 / $5.00 (8.4%)
```

---

## Trace Directive Template for Skills

All xm skills MUST record trace entries during execution. This is the standard template — each skill's SKILL.md includes a customized version.

### Automatic Checkpoints (hook-based — no LLM action needed)

`session_start`, `session_end`, and `agent_step` are recorded automatically by `.claude/hooks/trace-session.mjs`.
The hook fires on PreToolUse/PostToolUse for the Skill tool (any `xm:*` skill) and the Agent tool, and on Stop (end of the assistant turn).

- **session_start**: PreToolUse(Skill) — mkdir -p .xm/traces, generate session ID, write entry, set `.xm/traces/.active` to `{"session_id","tool_use_id"}`. A session left open by an earlier turn is closed first (`close_reason: "superseded"`).
- **agent_step**: one per Agent tool call made while `.active` exists — `id` (tool_use_id), `role` (subagent_type), `model`, `duration_ms`, `status`, `source: "hook"`. `status` is exactly one of: `success` (a result came back), `error` (error marker in the tool response, background or not), `launched` (background dispatch acknowledged — `run_in_background` or an agent-id response — so `duration_ms` is launch time), `unknown` (no visible response), `abandoned` (still running when the turn ended; written at Stop). No tokens: the hook payload carries none.
- **session_end**: Stop — write leftover agent markers as `status: "abandoned"` rows, then session_end with duration and `agent_count`, delete .active. PostToolUse(Skill) is deliberately not the close: it fires as soon as the skill's instructions are loaded, before the skill's own Agent calls. A skill that continues across turns (AskUserQuestion) is traced for its first turn only. A session older than 6 hours, or opened in another Claude conversation, is closed with `close_reason: "stale"` the next time the hook runs instead of collecting that turn's agents.

Skills do NOT emit session_start, session_end, or agent_step manually — a hand-written row duplicates the hook's and skews `agent_count` and every drift axis.

### Best-Effort Entries (SHOULD — LLM records when possible)

Only `fan_out` and `synthesize` remain LLM-written. **Session ID** — read from `.xm/traces/.active` (JSON from current hooks, a bare id from older installs):
```bash
SESSION_ID=$(node -e 'const r=require("fs").readFileSync(".xm/traces/.active","utf8").trim();console.log(r.startsWith("{")?JSON.parse(r).session_id:r)' 2>/dev/null)
```

### Session ID Format

Format: `{skill}-{YYYYMMDD}-{HHMMSS}-{4hex}`
Example: `x-op-20260404-153000-a3f1`

Generated automatically by the hook. Read via `.xm/traces/.active` during execution.

### Rules
1. session_start and session_end are **automatic** — handled by hook, never emit manually
2. agent_step is **SHOULD** — best-effort, LLM records when possible
3. Trace entries contain **metadata only** — never include LLM output, verdicts, or generated content
4. `tokens_est` values are estimates (±30-50%) — always mark `"precision":"estimate"`
5. If trace write fails (e.g., disk full), log to stderr and continue — NEVER block skill execution
6. Each skill session writes to its own file — no concurrent writes to the same file

---

## Natural Language Mapping

| User says | Command |
|-----------|---------|
| "start trace", "start recording" | `start` |
| "stop trace", "stop recording" | `stop` |
| "show timeline", "show execution log" | `show` |
| "how much did it cost", "how many tokens used" | `cost` |
| "redo the previous run", "reproduce it" | `replay` |
| "compare before and after", "compare two runs" | `diff` |
| "session list", "trace list" | `list` |
| "delete old ones", "clean up" | `clean` |

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll skip session_start, nobody reads traces anyway" | Session boundaries are how you correlate events later. Without them, traces are uncorrelated noise and you've lost attribution. |
| "Recording agent_step slows things down" | agent_step writes are append-only JSON lines — milliseconds, metadata only. The real slowdown is blind debugging later when the trail doesn't exist. |
| "I'll put the output in the trace for easier debugging" | Output in traces = PII risk + disk bloat + search degradation. Metadata only. Session logs exist for output inspection. |
| "If trace write fails, I should bubble the error up" | No. Trace failure must not block execution — traces are observability, not a gating mechanism. Fail silently and continue. |
| "Traces are only for failures" | Traces are for attribution — cost, time, agent count, session shape. Success traces are the baseline you need to diagnose the failure ones. |
| "One global trace file is simpler than per-session" | Per-session traces are correlatable and atomic. One global file is a race condition waiting to happen. |

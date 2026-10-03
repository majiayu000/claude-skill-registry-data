---
name: forge-agent-report
description: Structured completion-report contract for every dispatched Boss, validated by forge-report.cjs. Use when dispatching a subagent or ingesting its final report — completion contract, validation.
---

# forge-agent-report — the completion-report contract

Stops the Lead from hand-transcribing a dispatched Boss's final message into the dashboard. Every
dispatched agent ends its final message with ONE fenced block; this skill's tool parses, validates,
and ingests it.

> Naming note: the tool lives at `forge-bin/forge-report.cjs`. The skill folder is named
> `forge-agent-report` (not `forge-report`) because `skills/forge-report/SKILL.md` already exists for a
> different thing — the Lead's own end-of-task delivery report format. Don't confuse the two: this skill
> is the **per-agent** machine-checkable contract; `forge-report` is the **Lead's** human-readable final
> report.

## The contract (copy-paste into every dispatch prompt)

Include this requirement verbatim (or close to it) in every `Agent(...)` dispatch prompt:

```
End your final message with EXACTLY ONE fenced block:

​```forge-report
{
  "status": "completed|partial|blocked|failed",
  "work_package": "WP-…",
  "files_changed": ["path/one", "path/two"],
  "tests_run": "the exact command(s) + result — or \"none\" if honestly nothing ran",
  "evidence": ["what actually proves this — command output, file diff, line count, etc."],
  "blockers": ["only if status is blocked — what's blocking you"],
  "next_action": "the single most useful next step"
}
​```

If you emit more than one such block while thinking out loud, only the LAST one counts — make sure it
reflects your true final status.
```

## When to use

- **On every dispatch** — the Lead includes the contract requirement above in the prompt of every
  `Agent(...)` call, named or not.
- **On every return** — when a dispatched agent's final message comes back, the Lead runs `validate`
  (or `ingest` directly) before treating the work as done. An agent claiming `completed` with no real
  evidence, or `blocked` with no blockers listed, is **not** a valid completion — send it back.

## How to run

```
node .claude/forge-bin/forge-report.cjs validate <file|->
  # parse + validate a saved copy of the agent's message; exit 0 valid / 2 invalid

node .claude/forge-bin/forge-report.cjs ingest <run_id> <file|-> --agent "<Boss name>" [--root <projectRoot>]
  # parse + validate, then log ONE agent_output + ONE agent_evidence_added event into
  # <run>/events.jsonl (both already-registered VISIBLE-REASONING event types) — the dashboard
  # renders the report without the Lead re-typing anything. On an invalid report: logs NOTHING,
  # exit 2 — send it back to the agent instead.
```

`<file|->` is either a saved file containing the agent's raw message, or `-` to read it from stdin.

## Validation rules (the honesty gate)

- `status` must be one of `completed | partial | blocked | failed`.
- `work_package` must be a non-empty string.
- `files_changed` must be an array (`[]` is fine for a pure investigation).
- `evidence` must be an array, and when `status` is `completed` it must contain **at least one
  non-empty string** — a completed claim without evidence is rejected. This is the entire point of the
  gate: an agent cannot claim done without showing its work.
- `blockers` must be a non-empty array when `status` is `blocked` — a blocked claim with nothing listed
  as blocking it is rejected.
- `tests_run` must be a string or array — `"none"` is an honest, accepted answer; don't invent a test
  run that didn't happen.
- `next_action` must be a non-empty string.
- Only the **last** ` ```forge-report ` block in the text is used (earlier ones may be drafts/examples
  from the agent's own reasoning).

## Honesty rules

- The tool never logs anything on an invalid report — a rejected report goes back to the agent, not
  into the dashboard.
- The whole report is redacted with `forge-bin/forge-store.cjs`'s `redactValue()` before it is embedded
  in any event — a secret accidentally pasted into `evidence` or `tests_run` never reaches
  `events.jsonl` in the clear.
- This tool only checks the **shape** of the claim (does it have real evidence listed, are blockers
  named, etc.) — it does not independently verify the evidence is true. Pair it with `forge-verify` for
  a task-state cross-check against `events.jsonl`.

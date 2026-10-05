---
name: operational-session-closeout
description: Use when ending a substantial agent session, handing work to another agent, preparing context compaction, or signing off on completed work with objective state, verification evidence, telemetry markers, open loops, and next actions.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [closeout, signoff, handoff, telemetry, verification, session-management, portability]
    related_skills: [requesting-code-review, writing-plans, subagent-driven-development]
---

# Operational Session Closeout

## Overview

Use this skill to close a meaningful agent session with a reliable operational record: objective, outcome, completed work, changed artifacts, verification evidence, telemetry, risks, open loops, and next actions.

This skill is **harness-agnostic**. Telemetry is applied at stable lifecycle markers that other runtimes can map to their own usage APIs, provider metadata, traces, logs, or manual reports.

Core rule:

```text
Closeout is the process. Raw usage capture is the foundation. Telemetry markers annotate the process at stable lifecycle points.
```

Implementation priority:

1. First capture raw usage reliably: tokens in/out, cache/reasoning tokens where available, API/model calls, estimated cost, model/provider, elapsed time, and context usage.
2. Then expose an agent-callable usage snapshot, e.g. `[TEL-3]` closeout telemetry.
3. Then add named baselines/snapshots such as `[TEL-0]`, `[TEL-1]`, and `[TEL-2]`.
4. Then add richer significant-event tracking.

If telemetry is unavailable, preserve the marker and write `unavailable`. Never fabricate tokens, costs, context usage, or elapsed time.

For detailed adapters, schemas, templates, and examples, see:

- `references/harness-adapters.md`
- `references/telemetry-contract.md`
- `references/templates.md`
- `references/examples.md`
- `references/delta-calculation.md`
- `references/raw-usage-accounting-hardening.md`

## When to Use

Use when the user says or implies:

- “wrap session”, “closeout”, “sign off”, “handoff”, “where are we?”
- “summarize what happened”, “prepare for compaction”, “leave notes for the next agent”
- “finish this up”, “what did we verify?”

Also use before ending a long or meaningful session, before context compaction, after code/file changes, after significant research/debugging/planning, after durable task/note/external-system updates, or after tool/context limits require a durable status record.

Do not use for trivial one-turn answers or simple lookups unless explicitly requested.

## Raw Usage First

Before implementing or relying on lifecycle markers/events, harden raw usage accounting. Verify provider usage normalization, accumulated cost, request-count pricing, context usage, and parity between callable telemetry and user-facing usage commands.

Use `references/raw-usage-accounting-hardening.md` for provider response shapes, cost-parity rules, focused tests, and pitfalls.

## Required Telemetry Markers

These markers are the migration contract. Keep the labels stable across harnesses.

| Marker | Phase | Natural Timing | Main Question |
|---|---|---|---|
| `[TEL-0]` | Session start baseline | Start of a substantial session | What was the starting state? |
| `[TEL-1]` | Pre-execution baseline | Before meaningful side effects | What did planning/research cost before action? |
| `[TEL-2]` | Post-verification snapshot | After tests/checks/review/read-back | What did confidence cost? |
| `[TEL-3]` | Closeout snapshot | Immediately before final closeout | What is the final usage/runtime state? |
| `[TEL-4]` | Handoff delta | During handoff or compaction summary | What changed since the prior checkpoint? |

### `[TEL-0]` Session Start Baseline

Collect at the beginning of a substantial session if telemetry is available. Use as an internal baseline for later deltas. If unavailable:

```text
[TEL-0] unavailable — harness does not expose start-of-session telemetry
```

### `[TEL-1]` Pre-Execution Baseline

Collect immediately before meaningful side effects: file edits, config changes, migrations, installs, subagent dispatch, message sending, task/note writes, external-system changes, or long/costly jobs.

If execution already began before this skill was invoked:

```text
[TEL-1] not captured — execution had already begun before closeout skill was invoked
```

### `[TEL-2]` Post-Verification Snapshot

Collect after verification activities: tests, compile checks, lint/type checks, security scans, independent review, manual checks, API smoke tests, artifact read-back, or deployment checks.

Place `[TEL-2]` **inside the Verification section**, because it answers: “What did confidence cost?”

If verification ran but telemetry is unavailable:

```text
[TEL-2] unavailable — verification completed but telemetry source unavailable
```

### `[TEL-3]` Closeout Snapshot

Collect as late as practical, immediately before final closeout. This captures final model/provider, token/cost/context/tool-call/time state if available.

If unavailable:

```text
[TEL-3] unavailable — closeout telemetry source not available
```

Do not block closeout because `[TEL-3]` is unavailable.

### `[TEL-4]` Handoff Delta

Produce during handoff, compaction, or “where are we?” summaries. Use available telemetry plus operational state to explain what changed and what the next operator should trust.

If numeric telemetry is unavailable, still produce the operational delta and mark telemetry unavailable.

## Telemetry Initialization and Event Tracking

A closeout-capable harness should initialize telemetry at session creation, not at closeout. Closeout should read already-tracked state.

Minimum runtime state:

- `TEL-0`: captured automatically when the session/agent starts.
- `events[]`: append-only significant-event log with timestamp, marker/type, label, and optional telemetry snapshot.
- `snapshots{}`: named snapshots for `[TEL-0]`, `[TEL-1]`, `[TEL-2]`, `[TEL-3]` when collected.
- cumulative counters: model/API calls, tool calls, token/cost/context/time data where available.

Significant events worth logging:

- first user turn / objective accepted
- plan approved or execution begins (`[TEL-1]`)
- file/config/task/note/external-system write
- subagent dispatch and return
- test/check/review starts and completes (`[TEL-2]`)
- context compaction / handoff preparation
- closeout requested (`[TEL-3]`)

The event log should be compact metadata, not transcript capture. Keep labels short and store handles/paths, not full tool output.

Resource budget guidance:

- Counter updates should be O(1) per model/tool call and effectively negligible.
- Event logging should add one small dict per significant event; default target is under 50 events/session.
- Do not inject the event log into every model prompt. Keep it in runtime state and retrieve/summarize only at closeout or handoff.
- The loaded core skill is ~2.25k tokens; detailed references are loaded only on demand.

## Closeout Procedure

1. **Identify the active objective.** Separate primary, secondary, and incidental work if needed.
2. **Inspect current state when tools can verify it.** Check task state, git status/diff, files changed, test output, notes/tasks created, external artifacts, background processes, or plan state as applicable.
3. **Apply `[TEL-1]` before side effects** if closeout is invoked before execution. If too late, mark it not captured.
4. **Gather verification evidence.** For code: tests, compile/static checks, security scan, reviewer result, skipped checks. For non-code: read-back, confirmation handle, row counts, message delivery, note/task path, or external-system confirmation.
5. **Apply `[TEL-2]` after verification** when applicable.
6. **Identify open loops and risks.** Include unresolved asks, skipped checks, incomplete tasks, uncommitted files, assumptions, dependency caveats, side effects needing review, and context that must not be lost.
7. **Apply `[TEL-3]` immediately before the final closeout.** Prefer callable telemetry over manual copy/paste.
8. **Produce `[TEL-4]` for handoff/compaction/long sessions.** If no prior checkpoint exists, say “For this session” instead of “Since the prior checkpoint.”
9. **Deliver a concise closeout** with ranked next actions or a clear statement that no next action is required.

## Standard Output

```markdown
# Session Closeout

## Objective
- Primary:
- Secondary:

## Outcome
- Status: Completed / Partially completed / Blocked
- Summary:

## Work Completed
- ...

## Artifacts Changed
- Files:
- Notes:
- Tasks:
- External systems:

## Verification
- Tests:
- Static checks:
- Review:
- Manual/read-back checks:
- Not run:

### [TEL-2] Verification Telemetry
- Source:
- Verification tool/API calls:
- Verification token/cost delta:
- Verification elapsed time:
- Confidence gained:

## Open Loops
- ...

## Risks / Caveats
- ...

## [TEL-3] Closeout Telemetry
- Source:
- Model/provider:
- API/tool calls:
- Tokens/cost:
- Context usage:
- Elapsed time:

## [TEL-4] Handoff Delta
- Work completed:
- Files/artifacts changed:
- Verification completed:
- Tool/API-call delta:
- Token/cost impact:
- Context pressure:
- Remaining risk:
- Recommended next action:

## Next Actions
1. ...
2. ...
3. ...
```

## Harness Fallback Rules

At each telemetry marker:

1. Check for a callable usage API.
2. Check for provider response usage metadata.
3. Check for tracing/logging span metadata.
4. Check for runtime counters such as tool calls or elapsed time.
5. Check whether context-window usage is exposed.
6. If none are available, preserve the marker and write `unavailable`.

Never fabricate token counts, costs, or context usage. Do not ask the user to manually paste usage unless telemetry is central to the request and no callable source exists.

## Hermes Adapter Summary

If running in Hermes:

- Use `session_usage` for callable usage telemetry when available.
- Map `session_usage` snapshots to `[TEL-0]`, `[TEL-1]`, `[TEL-2]`, and `[TEL-3]`.
- For `[TEL-4]`, subtract earlier snapshots from later snapshots when possible and combine with operational state.
- Use `/usage` only if `session_usage` is unavailable and the user has already provided it or explicitly asks for manual telemetry.
- For code work, load and follow `requesting-code-review` before final signoff.

See `references/harness-adapters.md` for non-Hermes mappings.

## Common Pitfalls

1. **Telemetry as an appendix only.** Apply telemetry where it explains the work: pre-execution, verification, closeout, and handoff.
2. **Hermes-only wording.** Define markers first, then map Hermes or another harness to them.
3. **Dropping markers when telemetry is unavailable.** Keep the marker and write `unavailable`.
4. **Forcing manual usage copy/paste.** Prefer callable telemetry.
5. **Fabricating cost or token counts.** Unknown fields stay `unavailable`.
6. **Treating telemetry as proof.** Telemetry does not prove correctness; tests, checks, reviews, and read-backs do.
7. **Reporting total usage without deltas.** Phase deltas explain where effort went.
8. **Overloading closeout with transcript detail.** Summarize decisions, actions, artifacts, risks, and next actions.
9. **Skipping state inspection.** If tools can verify current file/task/test state, use them before finalizing.
10. **Losing the next action.** Every closeout should end with ranked next actions or state that no next action is required.

## Verification Checklist

Before finalizing, confirm:

- [ ] Active objective is stated.
- [ ] Outcome status is clear.
- [ ] Completed work is listed.
- [ ] Changed artifacts are identified.
- [ ] Verification evidence is included or explicitly marked not run.
- [ ] `[TEL-2]` is included under verification when applicable.
- [ ] `[TEL-3]` is included or marked unavailable.
- [ ] `[TEL-4]` is included for handoffs, compaction, or long sessions.
- [ ] Open loops, risks, and caveats are explicit.
- [ ] Next actions are ranked or clearly stated.
- [ ] No token/cost/context values are fabricated.
- [ ] Harness-specific telemetry source is named.
- [ ] Output is concise enough to be useful and complete enough to resume.

## Final Instruction

When this skill is active, produce a closeout that is operationally useful even without telemetry, but always include the stable telemetry markers at the natural application points.

The markers are the migration contract.

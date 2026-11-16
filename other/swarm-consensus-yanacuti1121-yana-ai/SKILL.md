---
name: swarm-consensus
description: When 2+ independent perspectives must agree before a risky Yana AI action — dispatching review subagents synchronously via the Task tool, resolving their findings by priority (Safety > Correctness > Performance > Style), and blocking on any Safety-severity finding. Replaces an earlier async message-bus/vote design that was never actually wired into the running system.
origin: yana-ai (rewritten 2026-07-03 — see "What changed" below)
license: Apache-2.0
version: 2.0.0
compatibility: yana-ai >= 0.43.0
---

# /swarm-consensus

## When to Use

- Multiple perspectives must agree before a high-risk action lands — e.g. a write to `core/rules/`, `core/hooks/`, `core/gates/`, or `core/agents/` (see `core/rules/54-bft-consensus-law.md` for the exact trigger paths)
- "Security review should be able to block anything a code change tries to ship"
- Fan-out: one question dispatched to N subagents, findings aggregated

## Do NOT use for

- Single-agent decisions (no second opinion needed)
- Low-stakes read-only tool calls (dispatching a reviewer is overkill)
- Anything needing a persistent, always-on second process — that's not how Task-tool subagents work; see "What changed" below

---

## The real mechanism: synchronous dispatch, not async voting

There is one Claude Code session. When it needs a second opinion, it dispatches a Task-tool subagent, which runs to completion and returns a plain-text report *in the same turn*. There is no separate vote-casting step, no polling for messages, no timeout window — the dispatch either returns a report or it doesn't finish.

```
Main agent identifies a change needs review (per 54-bft-consensus-law.md's
category table: rule changes, enforcement code, agent personas, or
integrity/lock files)
         │
         ▼
Dispatch both required reviewers synchronously, via the Task tool,
scoped to the specific diff — per subagent-policy.md's dispatch template
         │
         ├──→ Reviewer 1 (e.g. security-team/security-auditor.md) reports
         └──→ Reviewer 2 (e.g. architecture-auditor.md or code-auditor.md) reports
         │
         ▼
Main agent applies conflict-resolution.md's priority order across both
reports: Safety > Correctness > Performance > Style
         │
         ├── Any Safety-severity finding? → BLOCK, escalate to human
         │   (conflict-resolution.md Strategy C)
         ├── Correctness finding that breaks an enforced gate/test? → BLOCK
         └── Otherwise → proceed, log a short resolution note
```

## Dispatching reviewers

Use the Task tool directly — this is not a shell command, so there's no `bash swarm-orchestrator.sh request` step. The dispatch prompt follows `subagent-policy.md`'s template: state the task, the scope, and that the subagent must not write/edit/commit — only report.

```
Dispatch (conceptual, not literal shell):
  Agent(security-team/security-auditor.md, scope: "review this diff to
    core/hooks/foo.sh for security issues, read-only, report findings")
  Agent(code-auditor.md, scope: "review this diff to core/hooks/foo.sh
    for correctness/quality, read-only, report findings")

Both run, both return text reports in this turn — no polling, no
"wait for vote" step.
```

## Resolving findings

Apply `conflict-resolution.md`'s existing priority table directly — this skill does not invent a second one:

```
1. Safety (security/data-integrity)   — always wins, always blocks
2. Correctness                         — wins unless a Safety conflict exists
3. Performance                         — after Correctness
4. Style/cleanup                       — lowest priority
```

If two reviewers give conflicting recommendations at the *same* priority level, that's a genuine conflict — escalate to the human per `conflict-resolution.md` Strategy C. Don't average, don't pick the more convenient one, don't silently proceed.

## Fan-out to more than 2 reviewers

For a broader question (not the specific 2-reviewer infra-write case), dispatch as many subagents as the question needs, in parallel (multiple `Agent` calls in the same response), and collect all reports before synthesizing — this is the same pattern `conflict-resolution.md` already documents for general subagent dispatch, not a special "swarm" mode.

```
Rule: dispatch independent reviewers in parallel when their scopes don't
overlap (see conflict-resolution.md's "Phòng ngừa conflict từ đầu" —
scoping subagents narrowly from the start is cheaper than resolving
conflicts after the fact)
Rule: a subagent that never returns (crashes, times out) is a finding in
itself — don't silently treat missing output as "no objection"
```

---

## Anti-Fake-Pass Checklist

```
❌ Proceeding with an infra write after a Safety-severity finding, because
   a second reviewer's report looked clean
❌ Treating "the subagent didn't report anything" as approval — a missing
   or crashed report is not a clean bill of health
❌ Dispatching only one reviewer when 54-bft-consensus-law.md's category
   table calls for two
❌ Skipping dispatch because the change "is small" — the trigger-path
   match in 54-bft-consensus-law.md is the gate, not the diff size
❌ A subagent attempting Write/Edit/commit/push during "review" — banned
   categorically by subagent-policy.md, not something this skill needs
   to re-check
```

## What changed (2026-07-03)

This skill used to describe an async architecture: `swarm-orchestrator.sh request/vote/tally` over a file-based message bus, a TypeScript `SwarmCoordinator` client polling `agent-message-bus.sh recv` for RESPONSE messages, veto broadcasts, and split-brain locking for concurrent leader election. None of that was ever wired into the automatic pipeline — `swarm-orchestrator.sh` remains real, working, optional manual tooling (see `core/rules/54-bft-consensus-law.md`) for a human coordinating separate concurrent Claude Code sessions, but it was never how a single session's own review-before-write actually happens. This rewrite describes the mechanism that's actually running.

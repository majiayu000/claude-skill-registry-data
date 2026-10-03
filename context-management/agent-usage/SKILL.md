---
name: agent-usage
description: Default-never policy for the Agent tool — two scope-anchored exceptions, an approval gate, and efficiency rules for chained/multi-agent patterns. Trigger every time an Agent call is being considered, for any task.
---

# Agent Usage — Default Off, Judged Exceptions

Delegating to an Agent tool carries a large fixed token tax regardless of task size, independent of what it actually finds. Most sessions are short, procedural, single-goal, and end rather than run long — so "delegate to save context window" rarely pays off and often burns tokens instead of saving them.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a delegation that paid off vs. one that wasted tokens, a Case-2 scope call that turned out wrong. Merge instead of duplicating; delete disproven bullets.

## Default

**Never use the Agent tool.** Do all work inline — read, search, edit, run commands — even across many sequential tool calls. Needing several rounds of search is not, by itself, a reason to delegate.

## Exception 1 — explicit user request

The user names an agent, a number of agents, or one of the four chaining patterns (below) for a specific task. Proceed without further gating. A skill that is agent-based by design and is explicitly invoked by name counts as this exception — invoking it is itself the authorization.

## Exception 2 — need-based

Only evaluated when Exception 1 doesn't apply. Judge both cases against the session's stated task scope — from a handover file or the session's opening ask:

- **Case 1 — forced compaction.** Continuing inline would push this session to the point of requiring compaction to proceed. Delegating here avoids a worse outcome, not just spends tokens differently.
- **Case 2 — disposable context.** The work's intermediate context is, per the session's stated scope, very unlikely to be needed again by the main session. Anchor this to scope, not a guess: in-scope work defaults to "will be needed again, don't delegate"; clearly tangential/out-of-scope work is the safe case. Being wrong is recoverable — see the Reporting contract below — but the call should still be scope-anchored.

## Approval gate

Before acting on either Exception-2 case, stop and ask the user. State which case applies, and for any multi-node pattern, the node count and why collapsing further isn't possible. Do not ask "should I use an agent?" as a vague check-in — name the specific reason and shape.

Gate behavior across session modes (autonomous/no-pause modes, planning modes, background/non-interactive runs): see `mode-kernel`.

## The four chaining patterns

Node count is the cost driver, not which pattern is used — always try to collapse adjacent nodes into one agent before reaching for a multi-node shape.

- **Chain** (linear, dependent steps): almost never justified. Only when consecutive steps need genuinely different tool access or execution environments — not for plain sequential reasoning, which is one agent's own multi-step work.
- **Diamond** (fan-out 2, merge 1): only when the two branches are each independently large enough that combining them would overflow one agent's own context.
- **Branch/Tree** (fan-out, no merge): one level only — no grandchildren. Width = the smallest N covering genuinely distinct scopes.
- **Reverse tree** (fan-in from distributed sources): only when sources can't share one agent's tool access. Keep leaf reports short (~100 words) — the aggregator pays to read every leaf report in full.

## Lock inheritance

A dispatched agent acts under its parent session's identity, not its own — bound by whatever lock/coordination file (`role-session` parallel mode) already binds the parent to. Delegation is never a bypass. For fan-out patterns, the dispatching session must partition file scope across sibling agents up front — the lock file only arbitrates across roles, not between concurrent agents spawned within one role's own session.

## Reporting contract

Any dispatched agent must:
1. Return a short, compressed final report to the parent session.
2. Write its full raw findings to an agent-handover file (see the `handover` skill's "Agent handovers" section) — never only the compressed report. This is what makes a wrong Case-2 call recoverable at near-zero cost instead of requiring a second agent to redo the discovery.

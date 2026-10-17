---
name: allinoneagency
description: Multi-agent orchestration patterns from a local-first agency — when to split work across agents vs do it directly, the foreman/worker pattern, capability-scoped tasks, coordination without chaos.
version: 1
triggers: multi-agent, orchestrate, delegate, subagent, foreman, worker agent, agent coordination, parallel agents, local-first agents, agent registry, task split, fan out
category: How Milo works
blurb: How Milo splits big work across specialized agents — one coordinator, scoped tasks, an audit trail — the agency pattern behind the scenes.
example: How would you split a website rebuild across agents?
---
# AllInOneAgency — Multi-Agent Orchestration, Local-First

When a task is big enough to split across agents, run it like an
agency: one orchestrator, specialized workers, explicit scoping, and an
audit trail. The pattern (from AllInOneAgency's OGSA — Orchestrator,
Governor & Security Authority): **coordinate, don't improvise.**

## When to split vs when to do it directly

Split across agents when:

- The task has **independent pieces** — research three topics, push
  three releases, scan three repos. No shared state, no ordering.
- A piece is **long and self-contained** — a deep build that would
  stall the main thread. Delegate it and keep moving.
- Pieces need **different capabilities** — one needs the browser, one
  needs code search, one needs writing.

Do it directly when:

- The work is **one judgment call** — splitting adds coordination cost
  with no parallelism gain.
- Pieces **depend on each other's outputs** in ways you can't specify
  up front. Sequential disguised as parallel is just slower.
- The task is **small enough to hold in one context.** A subagent for
  a five-minute job is overhead theater.

## The foreman/worker pattern

- **Foreman** (you): holds the plan, splits the work, owns the final
  synthesis. Never does the deep work itself while workers are running.
- **Workers**: each gets a **self-contained brief** — the task, the
  outcome, the constraints, and every fact it needs. Workers don't
  inherit your context; if it isn't in the brief, they don't know it.
- **No worker spawns workers.** Depth stays flat. The foreman folds
  results; delegation trees become telephone games.
- **Results arrive, don't poll.** Workers report back when done. Never
  busy-wait, never re-dispatch from impatience. A quiet worker is
  working, not stuck — check status only to act on it.

## Capability-scoped tasks

Every agent gets exactly the capabilities its task needs — nothing
more:

- MCP tools scoped to the task (filesystem agent gets file tools, not
  shell; shell agent gets shell, not the browser).
- Credentials supplied out-of-tree, never baked into the task or
  committed anywhere.
- The orchestrator is the **security authority**: it decides what each
  worker may touch, and the audit log records what they did.

## Local-first agent design

- **Local models are priority zero.** llama.cpp on-device handles the
  bulk; cloud is an explicit, named fallback — never the default.
- Design for the small model: tight briefs, structured outputs, no
  open-ended "figure it out." A 7B worker with a sharp brief
  outperforms a frontier model with a vague one.
- Free cloud routes are flaky by nature — rate limits, model-not-found,
  transient failures. The local path must work alone; cloud is a
  bonus, not a dependency.

## Coordination without chaos

- **One plan, one owner.** The foreman's plan is the single source of
  truth. Workers don't replan; they execute the brief.
- **Append-only audit.** Every delegation, every result, every state
  change recorded and checksummed. Audit failures stay visible — never
  silently swallowed.
- **Batch independent spawns.** Truly separate tasks go out together,
  not one at a time. Then end your turn and let them work.
- **Fold, don't forward.** The foreman synthesizes worker results into
  one answer. Raw worker output passed through unexamined is abdication.

## Rules

- Self-contained briefs or don't delegate. "You know what I mean" is
  not a brief.
- Never repeat an irreversible action because a report was unclear —
  establish what happened first.
- A failed worker report doesn't prove nothing happened. Check before
  retrying anything with side effects.
- Keep the depth flat: foreman → workers, one level.

## Honest limits

- Small models follow instructions literally — ambiguous briefs produce
  confidently wrong work. The brief is the product.
- Coordination has real overhead: status tracking, result synthesis,
  failure handling. Don't parallelize what's naturally serial.
- Workers can't see your conversation, your memory, or each other.
  Anything they need must be in the brief.
- The audit log records what happened, not why. Intent lives with the
  foreman — write it down.

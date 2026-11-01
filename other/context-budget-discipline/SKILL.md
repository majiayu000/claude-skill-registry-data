---
name: context-budget-discipline
version: "1.0.0"
user-invocable: false
description: "Hard context-budget discipline for long-running workflow hosts: evaluate a session reset at every lifecycle phase boundary, compact proactively at ~60-70% of the context window (never only near the hard limit), write an atomic disk ledger before any reset so a fresh session resumes without replaying history, and hold sub-agent returns to ~1-2k summary contracts. Referenced by long-run hosts via frontmatter dependencies. Triggers — 「上下文预算」「上下文瘦身」「会话瘦身」「上下文膨胀」 / context budget, context slimming, session reset discipline, context rot."
dependencies: []
---

# Context Budget Discipline

> This skill single-sources the context-budget rules that long-running workflow hosts enforce during execution: when to reset a session, how to hand off state across a reset, and how to keep sub-agent returns bounded. Hosts thin-reference it; the threshold table, ledger format and recovery rules live here and are never copied into host bodies.

Token volume in an agentic loop is `turns × context-size-per-turn`, and the context re-send dominates the bill. An unbounded single-session lifecycle run is therefore a cost and correctness defect, not a style preference: recall degrades as the transcript grows (context rot), and every turn pays for the whole history again.

## Iron Law

**A single continuous session MUST NOT span a whole multi-phase lifecycle once projected context crosses the compaction threshold, and no reset MAY happen without a complete disk-ledger entry written first.**

## The Four Rules

### 1. Phase boundaries are reset evaluation points

At every major phase boundary of the host lifecycle (for example analysis → implement → verify → report, mapped to the host's own integer stages), evaluate a context reset:

- **fresh session** seeded from the ledger (preferred when the next phase needs little prior detail), or
- **in-place compaction** — summarize state to the ledger, then reopen a compact session (platform-agnostic intent; use whatever summarization the platform offers).

Decide the phase→boundary map when the host plans the run (or at execution-stage entry), never improvised mid-run. A run that completes before crossing the threshold performs no forced resets.

### 2. Compact proactively at a defined fraction of the window

Evaluate reset when measured or projected context approaches **~60–70% of the context window** (see reference.md for the default table) — not only near the hard limit. Near-limit compaction pays for the full window many times over before it fires. When a threshold is crossed mid-phase, either reset at the next safe point in that phase or record a miss note and recover at the next boundary (reference.md § Recovery).

### 3. Write the ledger before any reset (atomic write-then-reset)

Before any reset or compaction, write a complete ledger entry (format: reference.md § Ledger): frozen decisions, decisions-so-far with evidence pointers, artifact paths, current phase, next concrete step, open tickets. A resumed session reconstructs state from the ledger and referenced artifacts — **never by replaying conversation history**. A reset without a preceding complete ledger entry is a violation: stop, write it, then continue.

### 4. Sub-agent returns are bounded summary contracts

Sub-agents do deep work in their own clean contexts and return a condensed summary capped at **~1–2k tokens**. When a sub-agent returns more than its contract, re-request a condensed summary instead of ingesting the dump. The main agent holds the plan, the synthesis and the ledger — not the detail.

## Placeholder Contracts

| Placeholder | Meaning | Supplied by |
|---|---|---|
| `{ledger-path}` | Disk path of the running ledger file | Host (planning stage or card supply) |
| `{threshold-fraction}` | Reset evaluation fraction of the window; default per reference.md | Host override or default |
| `{phase-list}` | The host's own lifecycle phase/stage names | Host |

## Red Flags

- A lifecycle run reaching the report phase in the same session it started analysis, with no reset evaluation recorded
- Compacting only when the platform refuses to continue (near-limit reactive behavior)
- A session resumed from memory or transcript replay instead of the ledger
- Ingesting a full sub-agent transcript into the main context
- Host bodies carrying copies of the threshold table or ledger format instead of a one-line reference to this skill

---
name: systematic-debugging
description: "Root-cause one known bug: reproduce, trace, fix, verify."
version: 1.0.0
triggers:
  - /systematic-debugging
  - debug this
  - chase down this bug
  - track down this issue
  - why is X failing
  - root cause this
  - this test keeps failing
  - it works sometimes
argument-hint: "<the symptom, or a path/error to start from>"
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# /systematic-debugging — Root-Cause Discipline for a Single Issue

Walk one identified failure to its root cause and fix it there. The skill exists because the fastest fix that *actually holds* starts by finding the cause: guessing averages slower, because every wrong patch adds a new variable and can mask the real one. This isn't a discipline tax — it's the shortest path to a fix that survives the next run.

**This is the single-issue tool.** You have a specific symptom in hand. Distinct from siblings:
- **`/bug-sweep`** — searches the whole repo for unknown bugs (broad, discovery).
- **`/bug-blitz`** — grinds a known backlog of many bugs (broad, batch).
- **`/dogfood`** — exercises a newly-built thing until it works (broad, shakedown).
- **`/systematic-debugging`** — one known failure, traced to root cause and fixed (narrow, depth).

If you're holding more than one unrelated symptom, you want a sibling. If you're holding exactly one, you're in the right place.

**Announce at start:** "Running `/systematic-debugging` on <symptom> — pinning the premise before I touch anything."

## When this earns its keep

Reach for it on any single technical issue where the cause isn't yet *known* (not merely suspected): test failure, runtime bug, build break, flaky behavior, perf cliff, integration mismatch. It earns the most under exactly the conditions that make guessing tempting — time pressure, a fix that "looks obvious," a previous patch that didn't take, or a borrowed root cause from someone else's repo.

Skip it when the cause is already proven (just fix it), or when you have a *pile* of issues rather than one (sweep/blitz instead). A simple bug still has a root cause, but if you can already point at it with evidence, you've effectively done Phases 0–2 already — go fix it.

## Phase 0 — Pin the premise (the cheap step everyone skips)

Before reproducing anything, confirm the bug you're chasing is the bug that exists. This phase is ~2 minutes and saves hours of debugging a symptom that was already fixed, or fixing in your repo on a cause that lives in someone else's.

1. **Is it still broken on HEAD?** Stale dogfood logs, predecessor handoffs, and backlog entries describe state that may already be fixed (origin: an artifact you do not control, so the check is the point). `git log --oneline -- <cited-paths>` since the report's date, then re-run the failing case on current HEAD. An unverified "broken today" is a hypothesis, not a signal.
2. **Is the root cause borrowed?** If the cause came from a handoff, a cross-repo memo, or another repo's diagnosis, that framing is *hypothesis, not ground truth*. Confirm the same shape exists **here** — read the cited code on your own disk before acting on a diagnosis made elsewhere. The discrimination trap is assuming a matching symptom implies a matching cause.
3. **Is the signal real?** If the symptom surfaced through tool output that was empty, garbled, or contradictory, the channel may have failed rather than the code. Re-read once, solo. Two reads disagreeing → read a third way before treating it as a bug.

If Phase 0 dissolves the bug (already fixed / not reproducible here / phantom signal), you're done — say so and stop. That *is* the systematic outcome.

## Phase 1 — Reproduce and read the evidence

1. **Reproduce reliably.** Exact steps; does it fire every time? If you can't trigger it on demand, you're gathering data, not yet debugging — get to a reliable repro before forming theories.
2. **Read the error completely.** The build/error stream is the contract — it under-reports drift far less than compat docs or memory do. Stack traces, line numbers, codes, the *whole* trace. The answer is often already in it. → coordinator CLAUDE.md § Investigation funnel.
3. **Instrument the boundaries in multi-component systems.** When the failure crosses layers (CI → build → sign, request → service → DB, MCP → daemon → editor), log what enters and exits each boundary and run **once** to see *which* layer breaks — before theorizing about any of them. Evidence first localizes the layer, then you investigate that layer.
4. **Check what changed.** `git diff` / recent commits / new deps / config drift. The delta is the highest-prior suspect.

## Phase 2 — Trace to the source, discriminate the locus

The bug usually *appears* far from where it *originates*. Fixing where the error surfaces is symptom-patching.

1. **Trace backward.** From the immediate cause, ask "what passed this bad value / state?" and keep walking up the call chain until you reach the original trigger. When you can't trace by reading, add a stack-trace log right before the failing operation, run, and read the chain.
2. **Discriminate symptom-locus from root-locus.** Name both explicitly: where it *manifests* vs. where it *originates*. An audit or a reporter is usually right about the symptom and can be wrong about the locus — verify the producing code before accepting any proposed fix-site. → coordinator CLAUDE.md § Audit symptom is correct; locus may be wrong; § Fix-locus discrimination.
3. **State one hypothesis, in writing.** "I think X is the root cause because Y." Specific, falsifiable, one at a time. If you have three theories, you haven't finished tracing.

## Phase 3 — Fix at the source

1. **One change, at the root.** Address the originating cause, not the symptom. Resist "while I'm here" bundling — it muddies the verification signal and can introduce the next bug.
2. **Guards match the condition, not the container.** If the fix is a guard, gate on the actual invalid condition — substring-on-path filters and state-proxy liveness checks reject legitimate cases. → coordinator CLAUDE.md § Guards match conditions.
3. **Consider defense-in-depth where the bug was structurally possible.** If invalid data flowed through several layers to cause this, a single check can be bypassed by a different path or a refactor. Validating at each layer the data crosses can make the bug *structurally impossible* rather than merely absent — worth it when the blast radius justifies it.

## Phase 4 — Verify with fresh evidence

1. **Re-run the repro; prove it, don't assert it.** "Never mark complete without proving it works." A test file written to catch this must be *run*, not just read. → coordinator CLAUDE.md § Verification Before Done.
2. **Check for collateral.** Did the fix break a neighbor? Run the surrounding tests, not just the one.
3. **Land a regression test where one's missing** — and, ideally, land it *before* the fix so you watch it go red→green. A bug without a regression test invites its own return.

### When the fix doesn't take

A patch that doesn't work is information, not a prompt to pile on another patch.

- **< 3 attempts:** return to Phase 1 with what the failed attempt taught you, and form a *new* hypothesis. Don't stack fixes on top of an unconfirmed one.
- **≥ 3 attempts, each surfacing a new problem somewhere else:** stop debugging and question the architecture. When every fix requires "massive refactoring" or spawns a new symptom elsewhere, that pattern is the signal that the shape is wrong, not the patch. Surface it to the PM as an architectural call — this is a different conversation, not a fourth attempt. → coordinator ~/.claude/CLAUDE.md § Engineering Defaults (refactor over patch).

## A note on tempo

If you catch yourself reaching for a quick patch under pressure — that instinct is fine, it's the eagerness to fix. Spend it on Phase 0 and a reliable repro first; that's where it pays back fastest. The discipline here isn't distrust of your judgment, it's the route that gets your judgment to the right answer in one pass instead of three.

## Related doctrine

- coordinator CLAUDE.md §§ Investigation funnel, Verifying Handoff Premises, Verification Before Done, P0/P1 Verification Gate, Convergence as Confidence.
- Siblings: `/bug-sweep`, `/bug-blitz`, `/dogfood`, `/code-health`.

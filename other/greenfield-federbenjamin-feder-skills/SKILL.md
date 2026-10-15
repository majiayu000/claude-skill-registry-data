---
name: greenfield
argument-hint: "<problem or finding id> [--deep]"
description: Find the best technical solution by designing as if the repo's established rules, patterns, and conventions didn't exist, then audit only the rules the winning design collides with — updating outdated ones where they live. Use when the user says "/greenfield", "ignore the rules — what's the right design", "are the rules boxing us in here", "is this rule still true", "greenfield this", or when a fix collides with an established rule and the rule itself deserves the scrutiny.
---

Established rules harden into "hard truths" that design the project into corners long after their reasons died. This skill inverts the usual order: design first as if the rules didn't exist, then put only the *colliding* rules on trial. The best design is the primary deliverable; the rule audit is a light byproduct — never let it dominate the run's time or tokens.

Two failure modes to hold off simultaneously: anchoring (a session immersed in repo patterns produces the status quo with a new coat of paint — the greenfield frame exists to fight this) and laundering (the designer wants its design to win, so every inconvenient rule becomes "outdated" — the origin test exists to fight this).

## Quick tier (default) — inline, no subagent

Run this yourself, in-session; it should work as a short detour mid-task.

1. **Ground.** If the session doesn't already hold the problem's context, get what it needs first — read the relevant docs/code rather than designing from guesses. Proportionate to the question; grounding is not the deliverable.
2. **Greenfield design.** Reframe the problem as if building fresh — same product goal, data shapes, scale, and security invariants; no inherited patterns, conventions, or "how we do it here". Sketch up to 2 genuinely distinct approaches — or 1 plus a sentence on why nothing else is close (forced second options are filler). Pick the winner on the merits.
3. **Collision report.** List every established rule, pattern, or convention the winner breaks. You know them; report honestly — a hidden collision defeats the whole exercise.
4. **Origin test per collision** (~30s each): "this rule prevents Y; Y is no longer real because Z" — the verdict must be about the rule's job, never the design's convenience. Verdicts: **outdated** / **still load-bearing** (bend the design, note the cost) / **uncertain**. Uncertain never stalls the run: log it as an open question and proceed on best judgment.
5. **Edits.** Rules judged outdated get edited where they live, in the current working tree, disclosed in the final message (and PR body if one is in flight) — but only ordinary-convention-class rules. Escalation classes (below) always stop for the operator's approval — ask the user.

## Deep tier (`--deep`) — for architecture-level stakes

When status-quo anchoring would poison the answer, buy structural blindness (~10–15 min):

1. **Sanitize.** Distill a repo-agnostic problem brief — product goal, data shapes, scale, latency/cost envelope, security invariants, plus minimal code excerpts — into a pack in the session scratchpad. Banned in the brief: naming any current pattern, library choice, or architecture as a requirement; if it's load-bearing, state the underlying constraint instead.
2. **Blind design.** Spawn a subagent on your strongest model whose context is ONLY the pack — it never opens the repo or its instruction files. It returns 2–3 distinct candidates with trade-offs and its pick.
3. **Independent adjudication.** Spawn a fresh judgment agent with the winning design + the repo's rule surfaces: map collisions, and for each do real archaeology — the rule's recorded rationale, the git history that born it, whether the guarded failure still exists.
4. **Propose, never auto-edit.** Deliver the verdict table; every rule change waits for the user's approval, then lands where the rule lives.

## Rule surfaces and escalation (repo-adaptive)

Discover at runtime: the repo's agent instruction files (CLAUDE.md / AGENTS.md and what they cite), any rules directory, and any decision registry. Respect the repo's own severity scheme where one exists (e.g. Quirk's `[security]`/`[infra]` tags and its locked-decisions registry). Always-escalate, no tier exception: security- or infra-class rules, entries in a locked/decision registry (never edit these — surface them as challenges), and anything recorded as an operator decision. In repos without a severity scheme, treat rules touching auth, secrets, data exposure, or money as escalation-class by default.

## Report (turn-final, both tiers)

- **Design**: the winner and why; runner-up in one line.
- **Collisions**: table — rule → verdict → origin-test sentence.
- **Edits made** (quick) or **proposed** (deep), each with its file.
- **Open questions**: uncertain collisions and anything escalated.

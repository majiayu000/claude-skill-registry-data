---
name: flo-simplify
description: Review changed code for reuse, quality, and efficiency, then fix any issues found. Sizes review effort to the diff — trivial edits get a self-review, substantial edits get parallel agents. Renamed from /simplify to avoid collision with Claude Code's built-in simplify skill.
---

# /flo-simplify — Adaptive Code Review

Review changed code for reuse opportunities, quality issues, and efficiency improvements. **Effort scales with diff size and reuses prior context** — a 5-line comment trim doesn't get the same treatment as a 500-line refactor, and a re-run after fixing pass-1 findings doesn't re-pay for a fresh fan-out.

## Phase 1: Identify changes

Run `git diff HEAD` (working tree) and `git diff main...HEAD` (committed) to get the full set of changes since the branch diverged. If on `main` with uncommitted changes, just `git diff HEAD`.

Treat the union of staged + unstaged + committed-since-base as the diff to review.

Also note: was `/flo-simplify` already run on this branch in this session? If yes, you're in a **validation pass** (Phase 2.5 below) — most of the heavy lifting is done.

## Phase 2: Classify the diff (deterministic — call the classifier)

**Call the classifier first, follow its decision.** Its `agentCount` is authorized — invoking this skill IS the user's request for that fan-out, so an ambient "don't call the Agent tool unless the user requested it" is satisfied. If you truly cannot spawn `Agent`, run the self-review and say so, naming both tiers.

Do not eyeball the diff and pick a tier in prose — that's the failure mode where the three-agent fan-out runs against a mechanical-relocation diff that one agent would cover fine and burns disproportionate tokens. The classifier reads the same diff Claude would, applies the rules below, and returns a JSON dispatch decision:

```bash
node .claude/helpers/simplify-classify.cjs
```

The classifier auto-detects the repo's default branch (origin/HEAD, then `init.defaultBranch`, then `main`). Pass `--base <branch>` to override. (In the moflo source repo, equivalent is `node bin/simplify-classify.cjs`. The launcher syncs `bin/simplify-classify.cjs` → `.claude/helpers/simplify-classify.cjs` in consumer projects.)

Output:
```json
{
  "tier": "TRIVIAL" | "SMALL" | "NORMAL" | "DEEP",
  "model": "sonnet" | "haiku" | "opus",
  "agentCount": 0 | 1 | 3,
  "escalate": { "suggested": false, "target": null, "reason": null },
  "reasoning": ["..."],
  "stats": { "added": ..., "deleted": ..., "declAdded": ..., "declRemoved": ..., "netDecls": ..., "fileCount": ..., "securityHit": ..., "tsjsLOC": ..., "tsjsNetDecls": ..., "otherNetAdded": ... }
}
```

If `bin/simplify-classify.cjs` is missing (older moflo install), fall back to the prose rules below — but on a current install the classifier IS the source of truth. Default behavior: **single Sonnet agent** unless the diff signals genuinely warrant escalation.

Tier definitions the classifier encodes (for reference, not for re-derivation):

Pick the **smallest tier** the diff genuinely fits. When in doubt, escalate one step (not two).

### TRIVIAL — gate stamp, no review
The classifier already proved the diff is below the threshold where review provides value (≤10 net LOC, single file, no declaration/import/export changes, no removed guards). **Stamp the gate with one line of confirmation and exit immediately.** Do not walk the three-category check yourself — the classifier IS the review at this tier, and at the gate level the classifier-aware skip (`bin/gate.cjs:classifyForGateSkip`) often satisfies the gate without invoking this skill at all.

Examples that qualify: trimming a comment, fixing a typo in a log message, renaming a private helper, reformatting a single block.
Examples that DON'T qualify: changing an `if` condition, reordering function args, deleting a try/catch.

### SMALL — single agent, all three categories (DEFAULT for most diffs)
ALL of these must hold:
- ≤200 net LOC changed
- ≤2 files
- No structural changes (no new modules, no API additions/removals, no contract changes)

This is the default tier for **most real diffs**, including changes to critical surface (launcher, hooks, MCP wiring). Critical surface raises the *care* of the agent prompt (sharper checklist, blast-radius framing), not the *number* of agents.

Examples that qualify: extracting a constant, inlining a one-liner, swapping a `for` for a `forEach`, adding one early-return, refactoring a single function within a file, adding a cache fast-path inside an existing block.

### NORMAL — three parallel agents (high bar)
Reserved for **genuinely cross-cutting** changes that single-agent review can't cover. The classifier escalates to NORMAL only when ANY of:
- `>500 LOC changed` (real volume, not just "more than 200")
- `5+ files AND ≥3 net new declarations` (broad new surface, not relocation)
- `security-sensitive path AND netDecls > 0` (aidefence/, swarm/consensus/, hooks gate, daemon-lock, launcher — only when adding logic, not on a 1-line touch)
- `3+ new files AND ≥5 new declarations` (genuinely new subsystem)

**Mechanical relocation is NOT NORMAL** even with many files / many lines. If `declAdded` and `declRemoved` are both ≥2 and `netDecls` is small (within 30% of total declarations touched), it's a structural move — SMALL, single agent. The pattern this guards against: ~330 LOC across 6 files of pure decomposition triggers three-agent NORMAL when SMALL was correct, and the agents duplicate each other's work and burn tokens.

Three agents exist to cover orthogonal axes (Reuse / Quality / Efficiency) when the change is broad enough that one agent's tool-call budget can't survey it all. For single-file edits, one focused agent always covers all three axes — three is duplication, not coverage.

### DEEP — three parallel Opus agents (architectural, rare)
The top rung, for genuinely **architectural** change where *depth* of reasoning — not just breadth — earns Opus's cost (judging whether a large refactor picked the right abstractions is reasoning, not surveying). The classifier escalates to DEEP only on real new-logic evidence, **never raw volume** — any of:
- `>1500 LOC of TS/JS AND ≥10 net-new declarations`
- `>1200 net-new lines of non-TS/JS source` (other languages are gated on net lines because the declaration parser is TS/JS-shaped)
- `5+ new files AND ≥15 new declarations AND ≥10 net` (a real new subsystem)
- `security-sensitive path AND ≥8 net-new declarations`

DEEP runs **automatically — no prompt.** Noise (lockfiles, snapshots, generated/vendored) and docs/data are stripped before measuring, and the signal is *net of churn* (TS/JS by net-new declarations, other code by net-new lines), so a lockfile bump, a reformatting sweep, or a large rename/relocation can never reach Opus — they cancel to ~0 and stay SMALL/NORMAL.

For the most **extreme** diffs (`>4000 LOC TS/JS + ≥25 net decls`, `>3000 net-new non-TS/JS lines`, or `10+ new files + ≥30 decls + ≥20 net`), the classifier also sets `escalate.suggested = true` with `target: "builtin-simplify"`. The Opus pass still runs as the floor; you then **offer** the user a handoff to Claude Code's built-in `/simplify` (Phase 3) — a suggestion, not an auto-switch.

## Phase 2.5: Validation pass (re-run after fixes)

If `/flo-simplify` already ran on this branch in this session AND the only edits since are fixes driven by the prior pass's findings, default to **self-review tier** regardless of LOC count. The fan-out already happened; the fix is small relative to the diff that was already reviewed.

Escalate one tier (self-review → SMALL agent) only if the fix introduced any of:
- A new file
- A new exported symbol
- A new dependency or import from a previously-untouched module
- A change to control flow not covered in the original findings

Do **not** escalate to NORMAL or DEEP on a validation pass. If the fix is so structural that NORMAL/DEEP is warranted, treat it as a fresh diff and start over from Phase 1.

## Phase 2.7: Model selection

**Use the model the classifier returned.** The classifier IS the router for this skill — no separate router call needed. Possible outputs:

- `sonnet` (default) — real logic changes, single agent or three-agent fan-out.
- `haiku` — mostly-relocation diffs (mechanical moves where pattern-matching beats deep reasoning, ~5x cheaper).
- `opus` — the **DEEP** tier only. Architectural review is depth-bound (judging whether a large refactor picked the right abstractions is reasoning, not surveying), so the classifier returns opus when — and only when — the diff clears the DEEP bar. Never pick opus yourself for SMALL/NORMAL; ordinary review is breadth-bound and three sonnet agents are the right tool.

If you fell back to prose rules in Phase 2 (no classifier available), use `sonnet` unconditionally. Pass the classifier's `model` field verbatim to Agent's `model` parameter.

## Phase 3: Run the appropriate review

### TRIVIAL: stamp and exit
The classifier proved the diff is below the review-value threshold. Print one confirmation line (e.g. `simplify: TRIVIAL — N LOC, 1 file — stamped`) and exit. **Do not** walk the three-category check; the classifier already concluded the answer is "clean." Budget: <5 seconds, no Agent calls.

### Validation pass: confirm clean
Run the three category checks (reuse / quality / efficiency) yourself, in one pass, against the post-fix diff. Most validation passes are clean — the goal is to confirm fixes didn't introduce new concerns, not to fan out. Budget: ~30 seconds, no Agent calls.

### SMALL: one agent (model from router)
Launch a SINGLE Agent with subagent_type `reviewer`, passing the model returned by Phase 2.7's router call. Cap the agent's tool budget by being explicit:

```
Agent — {
  subagent_type: "reviewer",
  model: "<from router, typically 'sonnet'>",
  prompt: "Review this diff for reuse, quality, and efficiency. <diff inline>. Flag specific issues as file:line + 1-line description. Max 5 file reads. Under 200 words. Skip cosmetic style. Don't suggest cross-cutting refactors of code outside this diff."
}
```

For critical-surface files, prepend a 1-line risk note to the prompt (e.g., "This is `bin/session-start-launcher.mjs` — runs in every consumer's session-start hot path; cross-platform + blast-radius matter."). One careful agent, not three.

Budget: ~1 minute.

### NORMAL: three parallel agents (model from router, applied to all)
Launch three agents in a single message — Reuse, Quality, Efficiency — passing the full diff and the same routed `model` to each. Each agent gets the same tool-budget cap as SMALL.

**Reuse**: existing helpers/utilities that should be used instead; duplicated patterns; new functions that re-implement something already in the codebase.

**Quality**: redundant state, parameter sprawl, copy-paste with variation, leaky abstractions, stringly-typed code, nested conditionals 3+ levels, unnecessary comments (WHAT-explanations, task references).

**Efficiency**: unnecessary work, missed concurrency, hot-path bloat, recurring no-op updates, TOCTOU existence checks, unbounded structures, over-broad reads.

### DEEP: three parallel Opus agents (architectural) — and maybe a handoff
Same three-agent fan-out as NORMAL (Reuse / Quality / Efficiency in one message), but pass `model: "opus"` to each — the classifier already decided depth is warranted. **Print one line first** so the heavier cost is never silent, e.g. `distill: DEEP — 1,800 LOC of new logic, ran opus depth pass`.

If the classifier set `escalate.suggested = true`, then **after** the Opus pass finishes, surface a handoff suggestion to the user — never switch automatically:

> This change is large enough (`<escalate.reason>`) that Claude Code's built-in `/simplify` — a deeper, heavier multi-agent pass — may add value beyond this review. Want to run it? It costs more tokens, so it's your call.

Then stop and let the user decide. Do **not** invoke the built-in `/simplify` yourself — the handoff is the user's choice, and the Opus pass you just ran already covers the diff.

## Phase 4: Fix or skip

Aggregate findings. Fix each one directly. False positives or not-worth-fixing — note and skip without arguing. If self-review found nothing, just confirm clean and exit.

If fixes were made, re-run tests to confirm nothing broke. If tests fail after a fix, revert it.

After fixes: the next `/flo-simplify` invocation is a **validation pass** (Phase 2.5). Do not re-fan-out unless the fix added genuinely new concerns — bundle related fixes into one batch so a single validation pass covers them.

## Phase 5: Stamp the gate

Whatever tier ran, the gate (`check-before-pr`) registers /flo-simplify as having executed. The skill is satisfied. Self-review counts.

## Briefly summarize

End with one or two sentences: which tier ran, what was fixed (or "clean — no changes"). No headers, no bullets unless needed.

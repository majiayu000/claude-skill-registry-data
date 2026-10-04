---
name: conviction-audit
description: Audit whether a thesis's stated conviction matches its evidence, and whether any Conviction Trigger has silently fired without being actioned. Use when user says "conviction audit", "is my conviction right on [TICKER]", "did a trigger fire", or "should I re-rate [TICKER]".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$conviction-audit`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** Lead with the verdict and the fired trigger, no hedge words, tables over prose.

Audit one thesis for **conviction–evidence mismatch** and **silently-fired triggers** — the two ways a position quietly drifts from its stated conviction. Reports only; conviction/status changes are Tier 3 and happen via `$status`.

## Arguments
`SKILL_ARGS` = a ticker or thesis name. If empty, ask which thesis.

## Read-only
This skill REPORTS analysis; it does not modify vault files or conviction/status. It feeds `$status` (and, in the workflow, `_followups.md`).

## Mental Models gate (MANDATORY — AGENTS.md)
Read `[[Mental Models/Generalist - Overview]]` + matching `Industry -`/`Lens -` files. Apply the READING PROTOCOL and run the **base-rate view adversarially**: high conviction is exactly the state the outside view should attack — the question is whether the evidence *earns* the conviction, not whether the story is attractive.

## Method  (single source of truth — the `portfolio-conviction-audit` workflow reads this section)
1. **Read the thesis**: `conviction:` frontmatter, Summary, Key Non-consensus Insights, `## Conviction Triggers`, Key Metrics, and the last ~10 `## Log` entries. Count and date the `## Related Research` links (evidence weight + recency).
2. **Evidence-support check** — does the STATED conviction match the WEIGHT and RECENCY of evidence?
   - **Over-convicted**: `high` on thin (≤2 supporting notes) or stale (no conviction-relevant Log entry in >60–90d) evidence — the `$lint #60`/drift concern.
   - **Under-convicted**: `low`/`medium` while recent research strongly supports the case.
   - **Supported**: conviction is earned.
3. **Trigger-status check (highest-value)** — for each `## Conviction Triggers` line (`→ HIGH if`, `→ LOW if`, `→ CLOSE if`), evaluate its condition against current data (Key Metrics table + recent research; a scoped web search only if a value is missing). Flag any trigger whose condition is **already met but conviction/status unchanged** — a *silently fired trigger*. Also flag triggers too vague to evaluate (hidden vulnerability per stress-test Phase 2).
4. **Decay check**: days since the last conviction-relevant Log entry; is the thesis coasting on old conviction?
5. **Verdict**: `supported` | `over-convicted` | `under-convicted`, plus the list of fired/near-fired triggers, plus the recommended `$status` action (e.g. `conviction high→medium`, `reaffirm`, or `none`).

## Output (solo run)
A verdict line, then a **trigger-status table** — columns: **Trigger | Condition | Current value | Fired? | Action** — and a one-line recommended `$status` call (or "conviction supported, no action"). No filler.

## Workflow reuse
`portfolio-conviction-audit` (`.claude/workflows/portfolio-conviction-audit.js`) fans this `## Method` out across every thesis, ranks the book by over-conviction + fired-but-unactioned triggers, and (on `persist`) writes `_followups.md` entries for the flagged names — never touching `conviction:` itself (Tier 3 stays with `$status`). Keep `## Method` the single source of truth.

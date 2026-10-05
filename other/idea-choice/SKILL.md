---
name: idea-choice
category: research-analysis
description: >
  Weigh one or more ideas with a structured pros-and-cons analysis and a Go / Go with
  caveats / Don't recommendation. Use when the user wants to evaluate an idea before
  committing, compare options on the merits, score tradeoffs, or asks "should I do X" / "is
  X worth it".
codex-short-description: "Weigh ideas with a structured pros-and-cons analysis and a Go / caveats / Don't verdict"
related-skills:
  - clarity-council
  - idea-generate
loop-eligible: false

compatibility: claude-code codex opencode
---

# Idea Choice

Deliberate pros/cons analysis with weighted scoring and a recommendation. Designed for ideas the user is already considering — not for generating new ones (use [idea-generate](../idea-generate/)) and not for "just pick one already" (use [idea-decision-maker](../idea-decision-maker/)).

## Quick start

Provide one or more ideas plus, optionally, the criteria you care about.

```text
You: should I migrate our internal dashboard from Streamlit to a Next.js + tRPC stack?
I care about long-term maintainability and onboarding cost for the team.

Skill: [runs council, scores pros/cons, renders table, gives recommendation]
```

## Workflow

1. **Capture the ideas + criteria.** If the user gives one idea, evaluate it standalone. If two or more, evaluate each, then compare. If no criteria are stated, ask one targeted question to surface 2–4 (cost, time, risk, fit, reversibility, etc.).
2. **Optional grill.** If the idea is vague or rests on unstated assumptions, invoke [grill-me](../grill-me/) for a short pass to surface them — keep it tight (3–5 questions). Skip if the idea is concrete.
3. **Council pros/cons pass.** Invoke [clarity-council](../clarity-council/) with personas that argue both sides. Default trio: **Advocate** (lists upside), **Skeptic** (lists downside), **Pragmatist** (lists operational reality). For technical ideas, add **Senior Engineer**; for product ideas, **Customer Advocate**; for personal/life choices, **Psychologist**.
4. **Score each item.** For every pro and con the council produced, assign:
   - **Impact** (1–5): if this turns out to be true, how much does it matter?
   - **Confidence** (1–5): how sure are we it *is* true / will materialize?
   - **Weight** = Impact × Confidence (range 1–25).
5. **Aggregate.** Sum weighted pros, sum weighted cons, compute net (pros − cons).
6. **Render the table** (see format below) and pick a recommendation:
   - **Go** — net ≥ +20, no individual con ≥ 16
   - **Go with caveats** — net positive but at least one con ≥ 16; list the mitigations
   - **Don't** — net ≤ −10, or any con ≥ 20 that cannot be mitigated
   - **Needs more analysis** — net within ±10 AND no single item ≥ 16 (the analysis is too even to call)
7. **For multi-idea comparison**, add a final ranking table showing each idea's net score side by side, then state which one wins and why — or whether the leader's margin is too thin to declare.

## Output format

````markdown
## Idea: <name or short description>

**Criteria:** <comma-separated list>
**Assumptions surfaced:** <if a grill ran, list 1-3 here; else "(none)">

### Pros

| # | Pro | Impact | Confidence | Weight |
|---|-----|:-:|:-:|:-:|
| 1 | <one-line pro> | 5 | 4 | **20** |
| 2 | ... | 3 | 3 | **9** |

### Cons

| # | Con | Impact | Confidence | Weight |
|---|-----|:-:|:-:|:-:|
| 1 | <one-line con> | 4 | 4 | **16** |
| 2 | ... | 2 | 3 | **6** |

### Totals

- **Pros:** 29
- **Cons:** 22
- **Net:** +7

### Recommendation

**Go with caveats.** Net positive, but con #1 (weight 16) is significant. Mitigate by: <concrete mitigation>. Revisit in <timeframe> to confirm the assumption.
````

For multiple ideas, append:

````markdown
## Comparison

| Idea | Pros | Cons | Net | Recommendation |
|------|:-:|:-:|:-:|----------------|
| A | 29 | 22 | +7 | Go with caveats |
| B | 34 | 18 | +16 | Go |
| C | 19 | 31 | −12 | Don't |

**Winner:** B. Margin over A is +9 — meaningful enough to call.
````

## Guidelines

- **One line per pro/con.** If a point needs a paragraph, it's actually two points — split it.
- **Score honestly, not strategically.** Don't inflate confidence to make a preferred idea win; the scoring is supposed to reveal your bias, not hide it.
- **Use the same criteria across ideas.** When comparing, make the council apply the same lens to each — otherwise the totals aren't comparable.
- **Flag any con with weight ≥ 16.** These are deal-breakers in disguise. Even a "Go" recommendation should call them out.
- **Don't recommend "Needs more analysis" as a cop-out.** Only use it when the totals truly are inside ±10 *and* no single item is heavy enough to tip the call. If one idea has a 20-weight con and the net is +5, that's "Go with caveats," not "Needs more analysis."

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/idea-choice.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->

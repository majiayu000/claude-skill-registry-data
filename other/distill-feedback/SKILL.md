---
description: >
  Template for distilling one PEE iteration's results into feedback for the
  next Ideator round (the Rank+Select → Ideator feedback edge). Used by the
  main agent after ranking an iteration's branches.
user-invocable: false
---

# Distill feedback

After writing `iterations/iN/ranking.md`, write
`iterations/iN/distilled-feedback.md` with EXACTLY these sections (the next
Ideator invocation consumes this file):

```markdown
# Distilled feedback — iteration iN

## Scoreboard
| branch | proposal (one line) | score | audit | rank |
(disqualified branches: score struck through, audit=FAIL)

## What worked
2–4 bullets: concrete technique → metric delta, each ending with the branch's
eval.json reference (run-relative path).

## What failed
2–4 bullets: technique → why it lost or was disqualified (crash, violation,
underperformance), with the artifact path.

## Metric deltas
Best score this iteration vs previous iteration best (numbers + paths).

## Direction hints for next iteration
2–3 bullets: exploit (push the winning family further — name the specific
knob) and explore (which untried unconventional direction now looks
worthwhile, given the failures).
```

Rules: numbers only from eval.json files; hints must be actionable ("increase
model capacity within the runtime budget via X") not vague ("try harder").

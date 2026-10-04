---
name: decision-matrix
description: "Structure a choice between concrete options: elicit the real criteria and their weights, score each option honestly, run a sensitivity check on the weights, and separate what the numbers say from what the gut says. Use when choosing between 2–6 named alternatives (jobs, tools, vendors, apartments, strategies)."
---

# Decision Matrix

Use this skill when the user faces a choice between concrete, named options and wants the tradeoffs made explicit. The matrix is not an oracle — its value is forcing criteria and weights into the open, then revealing whether the decision is robust or hinges on one contestable weight.

## Purpose

Unstructured option comparison lets the mind double-count favorite criteria and quietly ignore inconvenient ones. A weighted matrix forces every criterion to be named, weighted once, and applied consistently. The most important output is often not the winning score but the **sensitivity analysis** — discovering that the choice flips on a single weight is the real insight. And when the user feels disappointed by the winner, that feeling is data.

## Procedure

1. List the options (2–6). If more, cluster or pre-filter first.
2. Elicit criteria — what actually matters. Probe for hidden criteria: status, fear, reversibility, optionality, who else is affected. Aim for 4–8.
3. Weight criteria (must sum to 100). Force tradeoffs — no "everything is important."
4. Score each option per criterion (1–10), citing a reason per cell — no bare numbers.
5. Compute weighted totals.
6. **Sensitivity check**: which single weight change would flip the winner? Is the margin robust or fragile?
7. **Gut check**: tell the user the winner and watch the reaction. If the numbers say A but the gut sinks, the matrix is missing a criterion — find it and re-run.
8. State the recommendation with its condition: "A wins unless you actually weight X more than you claimed."

## Output format

Use this concise structure unless the user asks otherwise:

```markdown
## Options
...

## Criteria and weights
| Criterion | Weight | Why it matters |
|---|---|---|

## Scores
| Criterion (weight) | Option A | Option B | Option C |
|---|---|---|---|
| ... | 7 — reason | 4 — reason | 9 — reason |
| **Weighted total** | ... | ... | ... |

## Sensitivity
...

## Gut check
...

## Recommendation
...
```

## Guardrails

- No bare scores — every cell gets a reason, or the matrix is numerology.
- Include reversibility/optionality as a candidate criterion; irreversible choices deserve extra weight scrutiny.
- If two options are within ~5% after sensitivity analysis, say the matrix cannot decide and name the tiebreaker question.
- The matrix ranks given options; if all options are bad, say so rather than crowning the least bad.

## Canonical questions

- "Should I take the Google offer, the startup offer, or stay?"
- "Postgres vs. DynamoDB vs. SQLite for this service?"
- "Which of these 3 apartments should we rent?"
- "Pick a city for the new office: Austin, Denver, or Raleigh."
- "Which vendor should we go with for payroll?"

Poor fits: yes/no decisions with one option (use assumption-audit or inversion), choices with unlistable criteria ("who should I marry"), and questions where the real task is generating options, not ranking them.

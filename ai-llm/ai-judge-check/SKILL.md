---
name: ai-judge-check
description: Check an AI judge against human labels — agreement, true-positive rate and true-negative rate from the four cells of the agreement table, the disagreements listed — and say whether the judge can be trusted for its check, and how to fix its prompt if not. Use when a team wants to rely on an LLM judge instead of reviewing outputs by hand. Not for evaluating the feature itself; see /ai-evaluate.
metadata:
  argument-hint: "<labels file> [project]"
---

# Judge check

Find out whether the AI judge in "$ARGUMENTS" can be trusted to replace people for its check. Agreement alone is not the answer: a judge that passes everything agrees with people most of the time when most outputs pass, and catches none of the failures it exists to catch.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The labels: rows with an output ID, the human's verdict and the judge's verdict (pass or fail), as a file or a paste. Never invent or fill in human labels; rows without a human label are left out and counted. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/ai/` (create it when you write). With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, ask for a project name.

Read `.singularskills/ai/<project>/06-evaluate.md` for the check this judge serves and its criteria, when it exists. `references/evaluation.md` holds the agreement table, the trust bar and the label minimum this skill applies.

Append this line to `.singularskills/log.jsonl` before you write the check (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-judge-check","workflow":"ai","phase":null,"project":"<project>","event":"started","artifact":"judges/<date>-<slug>.md","note":""}`, where `<date>` is today as `YYYY-MM-DD` and `<slug>` is two to four words naming the check, never a person.

## Process

1. **Count the four cells** of the agreement table:

   | | Human: pass | Human: fail |
   | --- | --- | --- |
   | **Judge: pass** | a | b (judge misses a failure) |
   | **Judge: fail** | c (judge rejects a good output) | d |

   Count them with a script written to `.singularskills/ai/<project>/` and included beside the result. Scripts read the team's files where they keep them and write aggregates under `.singularskills/`; a quote from an output names its row or output ID, and names, emails, phone numbers and account IDs in it are replaced with placeholders.

2. **Compute the rates:** agreement (a + d) ÷ all; true-positive rate a ÷ (a + c); true-negative rate d ÷ (b + d). **Without a way to run code**, show the four cell counts, label every rate `not computed`, and judge from the counts: for example, "the judge passed 6 of the 7 outputs people failed".

3. **Check there are enough labels:** with fewer than 10 human-labelled fails, or fewer than 30 labelled rows, there are **too few** labels to approve the judge. Say so, give the counts, and ask for more labels. Too few labels stops you approving a judge, never rejecting one: if the judge already passed more than half of the outputs people failed, or rejected more than half of the outputs people passed, the verdict is **do not trust, and too few labels**: get more labels before changing the judge's prompt, so the fix is not tuned to a handful of rows.

4. **Judge the judge** on the true-negative rate first, then the true-positive rate:
   - **trust** — true-negative rate at least 0.8 and true-positive rate at least 0.8, with enough labels (step 3); for a check guarding a high-harm failure, raise the true-negative bar to 0.9 (the pack's call, stated in the check)
   - **do not trust** — either rate below its bar; say which, with the cell counts
   - **too few labels** — as in step 3

5. **List the disagreements** (cells b and c) by output ID with a short redacted quote, and what they have in common.

6. **Say how to fix the judge** when it is not trusted and there are enough labels (with too few, the fix is more labels first): sharpen its pass/fail criteria around the missed failures, add those rows as examples in its prompt, then re-check it against fresh labels.

7. **Write the check** to `.singularskills/ai/<project>/judges/<date>-<slug>.md` with sections **Check**, **Agreement table**, **Rates**, **Verdict**, **Disagreements** and **Fix**.

## Output

The judge check written to `.singularskills/ai/<project>/judges/<date>-<slug>.md`. Present the verdict first (trust, do not trust, or too few labels), then the cell that decided it, then the fix.

After you have written the check, append the `started` line of Prerequisites to `.singularskills/log.jsonl` with `"event":"finished"`: `{"ts":"<ISO timestamp>","skill":"ai-judge-check","workflow":"ai","phase":null,"project":"<project>","event":"finished","artifact":"judges/<date>-<slug>.md","note":""}`.

The check opens with this frontmatter (`agent` is the agent you run in, or `unknown`; this utility has no gate, so `phase` is `null` and `gate` is `none`):

```yaml
---
skill: ai-judge-check
workflow: ai
phase: null
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

The check ends with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```

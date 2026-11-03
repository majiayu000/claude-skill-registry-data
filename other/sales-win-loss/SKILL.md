---
name: sales-win-loss
description: Analyze why several closed deals were won or lost — reasons the reps logged against what buyer debriefs and interviews say, the gap between them, and what to change — never treating a reason only the seller gave as the cause. Use when a team wonders why it keeps losing deals, often on "price", and has lost deals and buyer debriefs to look at. Not for one deal; see /sales-deal-review.
metadata:
  argument-hint: "<deals file> [project]"
---

# Win-loss

Find out why the deals in "$ARGUMENTS" were really won or lost, as `references/win-loss.md` describes: the seller's reasons and the buyer's reasons are different evidence, and only the buyer can say why the buyer decided.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The deals: a file or a paste with, per deal, the outcome, the reason the seller logged, and any buyer debrief, interview or email. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/sales/` (create it when you write). With no project named, use `playbook`, the folder for everything that spans deals.

Append this line to `.singularskills/log.jsonl` before you write the review (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-win-loss","workflow":"sales","phase":null,"project":"<project>","event":"started","artifact":"win-loss/<date>-<slug>.md","note":""}`, where `<date>` is today as `YYYY-MM-DD` and `<slug>` is two to four words naming the topic, never a person.

## Process

1. **Count both sides** with a script written to `.singularskills/sales/<project>/` and included beside the result: outcomes; reasons as the seller logged them; reasons as buyers gave them, for the deals with buyer input; and, per deal with both, whether they agree. Scripts read the user's files where they keep them and write only counts and deal or company names under `.singularskills/`, never contact details. **Without a way to run code**, count by reading the rows, show the counts, and label them `not computed`.

2. **Never treat a seller-only reason as the cause.** A reason only the seller gave is reported as **seller-reported**, with the buyer evidence that would confirm it.

3. **Check price before anyone acts on it.** When "price" is the most common seller reason, compare it with what the buyers said on those same deals. Where buyers named something else (slow responses, a missing feature or integration, a champion who left, a better relationship elsewhere), say so, with the counts. Do not recommend changing prices unless the buyer evidence supports it; if the evidence is thin, say what to collect first.

4. **The gap is the finding:** where seller and buyer accounts differ, list the patterns, ranked by how many deals they cover. Quotes from buyers drop people's names.

5. **Cover the whole picture:** won, lost and no-decision deals where the data has them; say if the set is only losses.

6. **Recommend changes,** each tied to a pattern, with an owner; and, when buyer input is missing for many deals, a short neutral interview guide (open "what" and "why" questions) to collect it.

7. **Write the review** to `.singularskills/sales/<project>/win-loss/<date>-<slug>.md` with sections **Deals**, **Seller-logged reasons**, **Buyer reasons**, **The gap**, **Price check**, **Changes** and **Interview guide** (when needed).

## Output

The review written to `.singularskills/sales/<project>/win-loss/<date>-<slug>.md`. Present the real reasons first, with the counts, then whether the evidence supports changing price, then the top change and its owner.

After you have written the review, append the `started` line of Prerequisites to `.singularskills/log.jsonl` with `"event":"finished"`: `{"ts":"<ISO timestamp>","skill":"sales-win-loss","workflow":"sales","phase":null,"project":"<project>","event":"finished","artifact":"win-loss/<date>-<slug>.md","note":""}`.

The review opens with this frontmatter (`agent` is the agent you run in, or `unknown`; this utility has no gate, so `phase` is `null` and `gate` is `none`):

```yaml
---
skill: sales-win-loss
workflow: sales
phase: null
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

The review ends with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what a reviewer must settle>
```

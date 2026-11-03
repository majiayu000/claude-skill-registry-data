---
name: sales-icp
description: Define the ideal customer profile and the qualification criteria for a sales team — from won and lost deals when an export is given (fit and win rate by segment, computed) and from marketing's customer research — for every deal to be qualified against. Use when a team wants to know which prospects are worth chasing. Not for buyer personas for marketing; see /marketing-customer-research.
metadata:
  argument-hint: "[deals file] [project]"
---

# ICP

Define who the team in "$ARGUMENTS" should sell to, from evidence where there is some.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/sales/` (create it when you write). With no project named, use `playbook`, the folder for everything that spans deals. Read the seller's own marketing project in `.singularskills/marketing/*/` (marketing projects are named after the seller's product or company, not the buyer: with exactly one folder there, use it; with several, ask once which is the seller's) customer research when it exists.

Append this line to `.singularskills/log.jsonl` before you write the profile (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-icp","workflow":"sales","phase":null,"project":"<project>","event":"started","artifact":"icp/<date>-<slug>.md","note":""}`, where `<date>` is today as `YYYY-MM-DD` and `<slug>` is two to four words naming the topic, never a person.

## Process

1. **Get the evidence:** a won and lost deals export (company size, industry, region, use case, deal size, outcome, cycle length) if the user has one, and the user's own view of their best customers. Ask once for both.

2. **Compute fit by segment** with a script written to `.singularskills/sales/<project>/` and included beside the result: win rate, deal size and cycle length per segment, with the number of deals behind each. Scripts write only aggregates and company names under `.singularskills/`, never contact details. With fewer than about 10 deals in a segment, say the rate is too thin to rely on.

3. **Write the profile:** the firmographics, the situation that makes a company need this, the trigger events, and the people usually involved; each criterion marked as backed by the deals data, by marketing research, or by the user's view.

4. **Write the qualification criteria** a new deal is checked against in `/sales-qualify`: must-haves, nice-to-haves and disqualifiers.

5. **Write the profile** to `.singularskills/sales/<project>/icp/<date>-<slug>.md` with sections **Evidence**, **Segments**, **Profile**, **Qualification criteria**.

## Output

The profile written to `.singularskills/sales/<project>/icp/<date>-<slug>.md`. Present the profile and the disqualifiers, and how much of it rests on deals data.

After you have written the profile, append the `started` line of Prerequisites to `.singularskills/log.jsonl` with `"event":"finished"`: `{"ts":"<ISO timestamp>","skill":"sales-icp","workflow":"sales","phase":null,"project":"<project>","event":"finished","artifact":"icp/<date>-<slug>.md","note":""}`.

The profile opens with this frontmatter (`agent` is the agent you run in, or `unknown`; this utility has no gate, so `phase` is `null` and `gate` is `none`):

```yaml
---
skill: sales-icp
workflow: sales
phase: null
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

The profile ends with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what a reviewer must settle>
```

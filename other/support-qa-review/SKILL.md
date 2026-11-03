---
name: support-qa-review
description: Score one support conversation against a QA rubric — accuracy, resolution, tone, customer effort, policy and, for failures, the three kinds of fairness in service recovery — with quoted evidence and the two changes that would most improve it. Use when the user wants feedback on how a support conversation was handled. Not for drafting the reply itself; see /support-reply.
metadata:
  argument-hint: "<conversation or file> [project]"
---

# QA review

Score the support conversation in "$ARGUMENTS" and say what would have made it better.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The conversation: pasted text, or a file path in `$ARGUMENTS`. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/support/` (create it when you write). With no project named: with exactly one folder there, use it; with several, ask which; with none at all, ask for a project name.

Read whichever of `.singularskills/support/<project>/02-taxonomy.md`, `04-macros.md` (voice and `## Policies`), `03-knowledge.md` and `05-escalation.md` exist; none is required.

Append this line to `.singularskills/log.jsonl` before you write the review (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"support-qa-review","workflow":"support","phase":null,"project":"<project>","event":"started","artifact":"qa/<date>-<slug>.md","note":""}`, where `<date>` is today as `YYYY-MM-DD` and `<slug>` is two to four words naming the topic, never the customer.

## Process

1. **Summarise the conversation** in two lines: what the customer needed and how it ended.

2. **Score each dimension from 1 to 4** (1 poor, 2 needs work, 3 good, 4 excellent), each with the quoted evidence from the agent's messages:
   - **Accuracy** — was every statement correct, as far as the knowledge base and policies show?
   - **Resolution** — was the customer's need met, or the next step made clear?
   - **Tone** — did it follow the voice in `04-macros.md`, if any, and treat the customer with respect?
   - **Effort** — how much did the customer have to do, repeat or wait for?
   - **Policy** — did the agent offer or promise only what the `## Policies` section allows?
   - **Escalation** — was the ticket escalated when `05-escalation.md` says it should have been, and not otherwise?
   When the conversation handles a failure, also score the outcome, the process and the treatment as `references/service-recovery.md` defines them.

3. **Name the two changes** that would most improve the conversation, each with a rewritten example sentence.

4. **Protect personal data:** quote only the agent's words the evidence needs, and replace any names, emails, phone numbers and account or order numbers with placeholders.

5. **Write the review** to `.singularskills/support/<project>/qa/<date>-<slug>.md` with sections **Summary**, **Scores** (a table: dimension, score, evidence), **Changes** and **Strengths**.

## Output

The review written to `.singularskills/support/<project>/qa/<date>-<slug>.md`. Present the total and the lowest-scoring dimension, and the two changes.

After you have written the review, append the `started` line of Prerequisites to `.singularskills/log.jsonl` with `"event":"finished"`: `{"ts":"<ISO timestamp>","skill":"support-qa-review","workflow":"support","phase":null,"project":"<project>","event":"finished","artifact":"qa/<date>-<slug>.md","note":""}`.

The review opens with this frontmatter (`agent` is the agent you run in, or `unknown`; this utility has no gate, so `phase` is `null` and `gate` is `none`):

```yaml
---
skill: support-qa-review
workflow: support
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
- <what the next phase or a reviewer must settle>
```

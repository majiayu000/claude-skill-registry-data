---
name: mine-outcomes
description: "Turn landed specs' outcome-log rows into model-fit and process proposals phrased as changes to named runner knobs, offer /retro on the outlier tickets, then clear the mined sections. Invoked as /mine-outcomes <repo> <spec>, --recent <N> or --all."
disable-model-invocation: true
---

`/mine-outcomes` reads what landed specs' tickets cost and how they went, and turns it into proposals, so the outcome log stays short and its lessons are kept as changes. Its words (Halt, Propose) are in [`runner/GLOSSARY.md`](../../../runner/GLOSSARY.md); the Result strings (Pass, Fix (resumed implementer), Fix (fresh resolver)) are `resultByReviewFixes` in [`runner/src/outcomeLog.ts`](../../../runner/src/outcomeLog.ts).

**Weigh the recommendations you put to the developer against the Codebase Priorities, [`docs/agents/codebase-priorities.md`](../../../docs/agents/codebase-priorities.md).**

## 1. Read the summary

The batch is the spec sections the invocation names; a section is the folder `docs/agents/outcomes/<spec repo>-<spec n>/`, one row file per landed ticket ([`docs/agents/model-fit.md#outcome-log`](../../../docs/agents/model-fit.md#outcome-log)). Run the summary for it:

| Invocation | Command | Batch |
| --- | --- | --- |
| `/mine-outcomes <repo> <spec>` | `npm run outcome:summary -- <repo>-<spec>` | that one section |
| `/mine-outcomes --recent <N>` | `npm run outcome:summary -- --recent <N>` | the N sections whose newest row landed most recently, by that row's commit date |
| `/mine-outcomes --all` | `npm run outcome:summary -- --all` | every section; the legacy log is never mined |

When it names no section, say so and stop. The summary is what you read in place of the row files and each ticket's `issue:read`. It already reads older rows under today's names, leaves `unrecorded` out of every sum and median with the rows each figure rests on, and sums each row's peaks (`150K → 90K` is a handoff, its peak sum 240K). It gives:

- review's share of cost for the batch, each repo and each spec: the sum of Review cost over the sum of Cost and Review cost, on rows recording both, rows with an older Triage cost column left out;
- each repo's medians per file changed, pooled over the batch;
- per spec, each row's figures, its outliers with the rules they trip and their session ids, and each ticket's Model fit pair line and reason;
- the expired, partly expired and never-recorded transcripts.

Read the knobs the proposals will name: `defaultRunKnobs` in [`runner/src/runKnobs.ts`](../../../runner/src/runKnobs.ts), laid over by `scripts/runner/runner.config.json`, and the pair criteria in [`docs/agents/model-fit.md#criteria-for-each-pair`](../../../docs/agents/model-fit.md#criteria-for-each-pair).

## 2. Outliers

The summary flags a row an outlier on each of these rules, naming every one it trips:

- Result is `Fix (resumed implementer)`, `Fix (fresh resolver)` or `Halted then passed (<kind>)`.
- Retries is above 0.
- **Over budget**: its peak sum is above `ticketBudget`. A ticket with a handoff counts, since its peaks are summed.
- **Long or costly for its size**: Duration or Cost per file changed is more than twice the median of that figure over the batch's rows in the same repo, with at least three rows recording it.

A row is **expired** when none of its Session ids has a transcript under `~/.claude/projects/*/` or `~/.claude-swap-backup/sessions/*/projects/*/`, and **partly expired** when some are missing; one whose Session ids is `unrecorded` never had any. They still count in every figure; only `/retro` needs a transcript.

For each outlier, and each row a pattern below rests on, read its What review caught from its row file, `docs/agents/outcomes/<spec repo>-<spec n>/<repo>-<n>.md`.

## 3. Proposals

Make two kinds. Each names the knob, criterion or file it would change, the change, and the rows behind it by issue number; the rows may come from any spec in the batch:

- **Model-fit boundary**: move a ticket shape from one pair to another in a criterion of `model-fit.md`, or change `resolverPair`, `gapCheckPair`, `ticketBudget` or `liveCeiling`. Compare each ticket's pair and its Model fit reason with its Result, peak sum and cost. A pair that passed first try on a shape its criterion puts higher is evidence for moving the boundary down. A cheaper pair that needed a Fix is evidence against.
- **Process**: one in one of the categories in `/retro` ([`.claude/skills/retro/SKILL.md`](../../../.claude/skills/retro/SKILL.md)), drawn mainly from What review caught. The same kind of catch on two or more tickets is a proposal. Name the knob when one fits, such as `maxTurns.<step>`, `wallClockMs.<step>`, `skillNames.review` or `reviewListCadence`. Otherwise name the doc or check to change.

A pattern on one row is not a proposal; leave it to `/retro`.

## 4. Present

In one message, give:

1. Review's share of cost, for the batch, then each repo and spec, each with its row count.
2. The proposals, model fit first, each with its knob, change and rows.
3. The outliers by spec, each with the rules it trips, its session ids and any that are missing.
4. The expired and partly expired rows, and the rows that never had transcripts.

End it with a round in the format of `/grilling` ([`.claude/skills/grilling/SKILL.md`](../../../.claude/skills/grilling/SKILL.md)): one numbered question per proposal, whether to file it, and one per outlier that has transcripts, whether to run `/retro` on it, each with your recommended answer and worded so "yes" accepts it. File each proposal the developer accepts with `gh issue create -R <owner>/<repo>`, resolving `<repo>` the way [`docs/agents/issue-tracker.md`](../../../docs/agents/issue-tracker.md) does, as a standalone issue whose body links each spec its rows come from as `<owner>/<repo>#<spec>`. A ticket for an agent ends with the `## Model fit` section [`docs/agents/model-fit.md`](../../../docs/agents/model-fit.md) asks for.

## 5. Clear the batch

Only once the developer has answered step 4's round, ask whether to clear every section in the batch, as one question in a later round of the same format. A `/retro` they want goes ahead of that round. Git history keeps the files after that. On a yes:

1. Open one session workspace ([`docs/agents/git-workflow.md#a-skills-session-workspace`](../../../docs/agents/git-workflow.md#a-skills-session-workspace)) named `mine-outcomes-<spec repo>-<spec n>`, `mine-outcomes-recent-<N>` or `mine-outcomes-all`, after the invocation.
2. `git rm -r` each mined section's folder, then make one commit: `Clear the <spec repo>#<spec n>, … outcome rows after mining.`, listing every spec.
3. Land it.

On a no, leave the folders; a later run mines them again.

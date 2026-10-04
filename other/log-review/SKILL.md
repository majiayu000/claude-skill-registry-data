---
name: log-review
description: Turns a period of daily logs into accomplishment statements you can reuse in a self-review, a promotion case, or a CV. Stitches entries by tracker url so one piece of work spanning weeks becomes one item, then asks only what the files cannot know — your role, what the result can be measured by, what you learned — and writes the answers into an accumulating highlights document. It never rates your work for you and never supplies a number you did not give. Triggers - "/pm:log-review", "turn last month's logs into highlights", "what did I accomplish this quarter", "성과 정리해줘", "이번 분기 뭐 했는지 정리", "이력서용으로 뽑아줘".
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

# log-review — a period of logs into accomplishment statements

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install pm@byjunyoung`), rather than improvising what the scripts do.

Reads the daily files `/pm:log` wrote over a period and produces the thing those files cannot be used as directly: a short list of what you accomplished, phrased so it survives being pasted into a self-review or a CV. It works from what is on disk. It does not go back to the tracker, and it does not go to chat — if something is not in the logs, it did not get captured, and the honest answer is that it is missing.

**The judgement is yours, not the skill's.** A daily log knows that a status changed; it does not know whether that mattered, how much of it was your work, or what it can be measured by. Those three things are asked, never assumed. A period with no answers produces no statements, which is a correct outcome.

## Principles

- **Only what the files support.** Every statement traces to entries in the period. Nothing is added from memory or inference.
- **Numbers come from the user.** If no figure is given, the statement carries `log.review.unknown_metric` rather than a fabricated one. A vague number is worse than a missing one — it will be read back as fact in a room where it can be challenged.
- **Quotes stay quotes.** Anything from the `What others said` section is carried across verbatim with its link. Never paraphrased into praise.
- **Existing entries are not rewritten.** The highlights document accumulates. A rerun of the same period updates only what the user changes in the preview.
- **One item at a time, its three questions together.** Splitting them into three rounds turns a ten-item period into thirty exchanges and the review gets abandoned halfway. Ask about one item, get its three answers, move on.
- **Preview → "go" before writing.** A human reads this document; it is not a scheduled write.

## Configuration

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml
```

`log.out.dir` says where the daily files are, `log.review.out` where the highlights document goes, `log.review.sections` names its sections, and `log.review.sentence` picks the sentence form.

## Input

A period: a month (`2026-08`), a quarter (`2026-Q3`), a year, or an explicit range. With none given, ask for one before reading anything.

## 1. Read the period

Glob the daily files inside the period and read their front matter and bodies. Report the count found, and say plainly if days are missing — a review of eleven days out of twenty-two is a review of eleven days, and the user should know that before answering questions about them.

If the period has no files at all, stop and say so. Do not reconstruct the period from other sources.

## 2. Stitch by url, then by title

Group entries by the tracker url recorded against each task. One url appearing across many days is **one piece of work**, not many.

Older files may carry no urls at all — a log written before urls were recorded, or one imported from somewhere that did not have them. **Fall back to an exact title match within the period** rather than treating every day as its own item; a period of ninety single-day entries is not a review, it is the raw log again. Titles are the weaker key: a task renamed mid-period splits into two groups, and two tasks that briefly shared a name merge into one. Say which key each group was stitched with, so a surprising group can be checked.

For each group, derive what the files already know:

| Derived | From |
|---|---|
| Span | First and last date the group appears |
| Days active | How many daily files mention it |
| Key | url or title — which one grouped it |
| Outcome | Whether it reached a terminal status, and on which date |
| Evidence | Every link collected against it over the span |
| What others said | Quotes attached to those days that name this work |

An entry with neither a url nor a title cannot be stitched at all. Keep those as single-day items and say how many there were. Many url-less entries in a **recent** period mean `/pm:log` is dropping urls, which is worth fixing at the source; in an imported period it just means the old format did not carry them.

## 3. Rank and cut

Order the groups by what makes an item worth writing up: it reached an outcome, it ran across several days, it accumulated evidence, someone said something about it. Put single-day items with no evidence at the bottom.

Show the ranked list and let the user strike what they do not want to write up. **Propose the top `log.review.max_items` and leave the rest listed but unasked** — a period usually yields a handful worth keeping, not everything that moved, and an interview that runs past a dozen items gets abandoned before the good ones are reached. The user can always ask for more.

## 4. Interview

For each kept item, the files supply span, evidence and quotes. Ask only the three things they cannot supply, and ask them **in one round per item** — role, measure and learning together, then move to the next item. Offer the options as choices where the shape is known, and take a typed answer where it is not.

| Asked | Why it cannot be derived |
|---|---|
| Role | The tracker records an assignee, not whether you led it, took a part of it, or reviewed it |
| Measure | What the result can be counted in — items, duration, share, an incident avoided. The log has activity, not outcome |
| Learned | A tool, a method, a piece of domain knowledge. Nothing in a status change reveals this |

Take "none" as an answer. An item with no measure still gets written, carrying `log.review.unknown_metric`.

## 5. Compose

Assemble each item in the form `log.review.sentence` names.

- **`xyz`** — accomplished *what*, as measured by *which figure*, by doing *what*. The measure sits inside the sentence rather than trailing it.
- **`plain`** — what was done and what changed, without the measurement clause.

Rules either way: lead with the outcome, not the activity. Name your role where it was anything other than leading it. Append the span and the evidence links as a trailing line, not inside the sentence. Keep it to two lines.

Then sort each item into `log.review.sections`. An item can appear in only one section; where two fit, prefer the one naming the contribution over the one naming the artifact. Quotes go to the feedback section with their links, and learnings to the learning section as their own short lines — those two sections are why the daily log bothers to capture them.

## 6. Preview and write

Show the full set of new entries under their section headings, and say which existing entries the write will leave untouched. Close with `shall I proceed? (go / changes)`.

On go, append into `log.review.out`, creating the file and its section headings if it does not exist. Read the file back and confirm the sections are intact and nothing existing was displaced.

## 7. Summarise

The document path, how many items were written under which sections, how many days the period actually had files for, and how many items were dropped for having no url. Name anything left carrying `log.review.unknown_metric`, so the user knows what to come back and fill.

## When NOT to invoke

- Writing today's log → `/pm:log`
- Writing a task record's context table → `/pm:task-draft`
- Writing requirements → `/pm:prd`

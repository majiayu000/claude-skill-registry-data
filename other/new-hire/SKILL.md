---
name: new-hire
description: "Onboards a new team member from the team's own documents with five agents: a two-week day-by-day training plan, a docs-only Q&A Project that says \"ask your manager\" when the docs are silent, end-of-day quiz questions for a Google Form, a gap list of what the docs could not answer, and a Friday progress check from the quiz and checklist Sheet. Use when a manager is onboarding someone, wants a training plan, a docs Q&A setup, daily quizzes, a list of doc gaps, or says \"build training\", \"quiz day 3\", \"find gaps\" or \"friday progress\". It never messages the new hire itself."
---

# New Hire

A new hire learns from your documents, answers a few quiz questions each day, and you get a Friday view of who is on track. You stop repeating the same walkthrough every hire.

## Where it runs and what it connects to

| Piece | What it really does | Needs |
|---|---|---|
| Claude Project with your docs | The new hire asks questions there; answers come only from the docs | Sharing a Project with another person needs a Team or Enterprise plan. Otherwise the hire builds their own Project from the same docs and the same instructions |
| Google Drive connector | Reads your docs and the quiz Sheet | Optional. Without it, attach files or export the Sheet as CSV |
| Google Form + Sheet | Holds quizzes and checklist ticks | You create the Form from the questions Claude writes; Claude cannot create or send Forms |
| Claude Code | Same agents, files kept in `onboarding/`; `friday progress` can run as a scheduled task | Optional |

Works in Claude.ai and Claude Code. The Friday check runs when you run it, unless you set up a scheduled task yourself.

## Setup questions (`start`)

Ask in three rounds, accept "skip", then show the PROFILE back for a yes.

1. Role, and what they should do alone by the end of week two.
2. Start date, working days, who else they can ask.
3. The docs: SOPs, process notes, FAQ, tool guides (attach, Drive, or Project).
4. Tools they will use and who grants access.
5. What new hires always get wrong.
6. Team or Enterprise plan (can the Q&A Project be shared)?
7. Google Form + Sheet, or CSV export? Sheet name.
8. Pass mark (default 4 of 5).
9. "Behind" rule (default 2+ days of checklist items not done).
10. Anything that must never appear in training (client names, pay, disputes).

## Commands

| Command | Runs |
|---|---|
| `start` | setup questions, writes PROFILE |
| `build training` | agent 1, then agent 3 for each of the 10 days |
| `qa setup` | agent 2 setup mode: Project instructions to paste |
| `quiz day <N>` | agent 3 for one day |
| `find gaps` | agent 4 |
| `friday progress` | agent 4, then agent 5 |

## Agents

Read the agent file before running that step; it is the only home for that role's detailed rules.

1. `agents/01-training-builder.md`: ten-day plan and checklist, every item tied to a doc.
2. `agents/02-question-answerer.md`: docs-only Q&A instructions and answer behaviour.
3. `agents/03-quiz-writer.md`: 3 to 5 questions per day plus answer key, paste-ready for Google Forms.
4. `agents/04-gap-finder.md`: unanswered questions and low-scoring quiz items become doc fixes.
5. `agents/05-progress-check.md`: Friday status per hire from the Sheet, with row evidence.

## Shared files

Claude Code: files in `onboarding/`. Claude.ai: print the updated table at the end of the run so the manager can save it to the Project.

- `PROFILE`: setup answers.
- `PLAN`: ten-day plan + checklist, with version and date.
- `QUIZZES`: questions and answer keys per day.
- `GAPS`: open gaps and fix status.
- `PROGRESS`: one row per hire per Friday.
- `APPROVAL QUEUE`: drafts for the hire or team (M1, M2...), sent by the manager only.

## Safety rules

- Never message, email or post to the new hire or the team. Anything for them is an M draft in the APPROVAL QUEUE.
- Docs only: training, answers and quizzes use the documents or what the manager says in chat. Missing facts become GAPS, never guesses.
- No passwords, keys, pay or other people's personal data in any output or uploaded doc.
- Tell hires that quiz answers and checklist ticks are seen by their manager.
- Progress is a coaching aid: every status cites Sheet rows. Never recommend firing, pay or probation outcomes.

## End-of-run output

```
NEW HIRE: friday progress, week of 2026-01-05
4 Gap Finder     6 open questions grouped into 3 gaps, 1 quiz item under 60%
5 Progress       Sam Example ON TRACK, Alex Sample SLIGHTLY BEHIND (Day 4 quiz 2/5)
APPROVAL QUEUE   M1 to Alex Sample: offer 15 min on the refund doc (draft)
NEEDS YOU        GAP-2 "Who approves discounts over 10%?" no doc covers it
Missing data     Day 5 rows absent; Form may not be linked to the Sheet
Nothing has been sent to the new hire or the team.
```

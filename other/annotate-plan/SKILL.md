---
name: annotate-plan
description: Plan a change in a PLAN.md you annotate in your own editor, round after round until you approve; then implement on request.
disable-model-invocation: true
argument-hint: "[task]"
---

The arguments name the change to plan; none means what the conversation is about. Write no code until the plan is approved and the user says to implement it.

## Setup

- Pick a kebab-case slug. The plan is `plans/<slug>/PLAN.md` in the project's agent notes.
- The user's instructions say where agent notes live and what a project is. Without them, the notes are `.agents/notes/` in the repo (write a `.gitignore` containing `*` there first) and the project is the repo.
- If a `PLAN.md` is already there, ask whether to resume it or start over. When resuming without a `PLAN.prev.md`, read the whole plan for notes instead of diffing.

## First draft

Research the code the change touches: inline for a few reads, a fresh subagent for a broad sweep. Don't ask clarifying questions first; gaps go under Open questions. Write `PLAN.md` with these sections:

- **Goal**: the outcome, in a sentence or two.
- **Findings**: what the code does today, with repo-relative paths.
- **Approach**: the shape of the change and why.
- **Changes**: what changes, per file or area.
- **Verification**: the commands that prove the change works, and what they should show.
- **Open questions**: calls you want the user to make.
- **Out of scope**

## Rounds

- After every write, copy the plan to `PLAN.prev.md` beside it.
- End each round with the plan's absolute path, how many notes you addressed, which are still open, and "annotate and say go, or approve".

On go, diff `PLAN.md` against `PLAN.prev.md`. Every change is feedback, as is anything said in chat:

- An edit to your text is the user's wording now. Keep it.
- A deleted line means drop it.
- A note, in any style: fold it into the plan and remove it. If it's a question, you disagree, or the code contradicts it, leave it and add a blockquote under it starting `**Reply:**`.

Then scan for `**Reply:**` blocks:

- One the user left untouched stays open.
- Once they edit or delete its note, fold the answer in and remove both.
- Never rewrite `PLAN.md` from memory: edit the file as it is on disk.

## Approval

- Only an explicit approval ends the loop. Diff first: if the user changed the plan since your last write, that's another round, not approval.
- Then rewrite Changes as a checkbox list, one box per independently verifiable step, and ask whether to implement now.
- If no, stop and name the options: build later from the plan, or `/handoff` for work another agent should build.
- If yes, implement in this session and tick each box once the step's checks pass. If the code forces a departure from the plan, stop and ask before diverging.
- When implementing ends, finish your reply with what the user needs to act on: the Verification results, any box left unticked and why, and what is left to commit or review.

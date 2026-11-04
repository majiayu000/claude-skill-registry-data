---
name: spike
description: Build a small throwaway artifact that answers exactly one open design question, then move it off the working branch onto an unmerged spike branch. Two routes inside the skill, a runnable terminal program for state, logic, or data-shape questions, and a side-by-side view comparison for presentation questions. Use when the user says "spike this", "build a quick throwaway", "let me play with the model", "try a few visual directions", or wants to de-risk a design choice before committing to it. For production features, use `/plan`; for refactoring an existing module, use `/refactor`; for a single polished design pass, use `/design`.
argument-hint: "/spike [state|view] <question>"
allowed-tools: "Read, Edit, Write, Grep, Glob, Bash, Skill"
---

## Overview

A spike is throwaway code whose only purpose is to answer one question. The question chooses the shape.

## When to Use

- The user says "spike this", "build a quick throwaway", "let me play with the model", or "try a few visual directions".
- A design choice is cheaper to settle by running something than by arguing it on paper: a state model with awkward cases, or a screen whose layout is undecided.
- [`/interview-me`](../interview-me/SKILL.md) reaches a question that talk cannot settle and routes it here.

For production features, use `/plan`; for restructuring an existing module, use `/refactor`; for a single polished design pass, use `/design`.

## Process

### Pick a route

Read the user prompt and the surrounding code, then pick.

- **State route.** Use when the open question is about a state machine, a data shape, a workflow, or business rules that are hard to reason about on paper. Load [`STATE-BRANCH.md`](STATE-BRANCH.md). Build a tiny interactive terminal program that drives the state through hard cases and prints the full state after each step. The logic lives in a pure module the terminal shell calls, so the validated version lifts into production.
- **View route.** Use when the open question is about presentation, layout, or visual style. Load [`VIEW-BRANCH.md`](VIEW-BRANCH.md). Generate several radically different variations inside an existing page, against its real data, switchable via a query string and a small dev-only selector.

If the route is genuinely ambiguous and the user is not reachable, pick the route that matches the surrounding code, backend code chooses state, page code chooses view, and write the assumption into the startup banner.

### Rules for every spike

1. **Throwaway from minute one, marked as such.** Place the spike next to the module or page it informs so context is obvious. Prefix the directory or filename with `spike-` per project convention. Make the entry point print a banner as its first output, or render it at the top of the view, from a string constant rather than a source comment, since comments are banned per [`rules/code-style.md`](../../rules/code-style.md): `SPIKE: <question being answered>. Kept on spike/<slug> after the verdict.`
2. **One-command run.** Use the project package manager. The user must launch it without thinking.
3. **State lives in memory.** Skip persistence unless persistence is the question. When persistence is the question, hit a scratch database or local file whose name announces it is disposable.
4. **No polish.** No tests, no abstractions, no error handling beyond what the spike needs to remain runnable. Speed of learning over elegance.
5. **Surface state on every step.** After each user action on the state route, or each variant switch on the view route, print or render the full relevant state.
6. **Capture the verdict, keep the evidence, clear the working branch.** Once the question is answered, record the verdict and the question it settled where the work continues: a commit message, an ADR, or the implementation issue. Then move the spike off the working branch onto its own branch, which is never merged:

   ```bash
   git switch -c spike/<slug>
   git add <spike files and hunks only>
   git commit -m "chore(spike): <question>"
   git switch -
   ```

   Stage only what the spike added or changed, never unrelated uncommitted work. Switching back removes the spike from the working tree; confirm with `git status`. Point at `spike/<slug>` from the verdict so the next reader can re-run the evidence. A spike that stays on the working branch past its verdict has stopped being a spike.

## Common Rationalizations

- "Adding tests now makes the spike reusable": the spike is the test. Tests land when the validated `model.<ext>` or the winning variant is rebuilt in the real code.
- "One spike can settle two questions at once": each question needs its own banner and its own verdict. A spike answering two questions produces a verdict nobody can attribute.
- "Three variants that differ in color are enough": [`VIEW-BRANCH.md`](VIEW-BRANCH.md) requires variants that differ in hierarchy, interaction, or layout. Pick more divergent directions.
- "Mock data is quicker than wiring the page": the real data carries the density and edge cases the question is about. Read the page's data.
- "Leaving the spike on the working branch keeps it handy": `spike/<slug>` keeps it just as handy and keeps it out of the next commit.

## Red Flags

- Stop and split the spike when its banner names more than one question.
- Stop and ask the user when the spike starts to need persistence, authentication, or error handling the question does not call for.
- Stop and pick more divergent directions when the user cannot tell the variants apart at a glance.
- Stop and stage file by file when `git status` shows unrelated uncommitted work next to the spike files.
- Stop and finish rule 6 when a verdict is recorded and `git status` on the working branch still lists spike files.

## Verification

- Spike launches with one command.
- Banner names the open question.
- State or chosen variant is visible after every step.
- A verdict is captured before the spike leaves the working branch.
- The `spike/<slug>` branch holds the spike, and `git status` on the working branch shows none of its files.
- If the verdict is hard to reverse, call the Skill tool with `plan` and the arguments `adr new <title>`, and link the ADR from the verdict capture.

## Related skills

- `/plan` plan the real implementation once the answer is known.
- `/plan adr new` record a hard-to-reverse decision.
- `/design` for a single curated design pass that is not throwaway.

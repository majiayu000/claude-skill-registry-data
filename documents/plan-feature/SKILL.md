---
name: plan-feature
description: >
  Plan a non-trivial feature before coding: read the issue and the code, ask a few focused
  questions with a recommended answer each, then write a short plan (goal, approach, acceptance
  criteria, scope, risks). Use for "plan this", "let's plan #N", "how should we build X", or before
  starting an issue that spans several files or needs a design choice.
argument-hint: "[issue number or short description]"
---

# plan-feature

Project facts (tracker, where plans go, checks, hazards, what only a device can verify) live in
the project's `CLAUDE.md` under **Skill settings**. Read that section first. If it is missing, ask
once where plans should go and suggest adding the section.

## Size it first

Decide out loud in one line, then follow only the steps for that size:

- **Small** — one or two files, obvious approach, nothing irreversible. Don't plan; say so and
  offer to just do it. Planning a small change wastes more than it saves.
- **Medium** — steps 1–5.
- **Large** — new subsystem, native/platform code, data model or storage format, external API,
  auth or secrets, or a hard-to-undo decision. Steps 1–6.

## 1. Load the context

- The issue with comments, plus any issue it links to or depends on. If it depends on an open
  decision issue, stop and say so.
- Only the background-doc sections that matter for this issue, not the whole file.

## 2. Research the code

- Find the closest existing code to mirror and what can be reused. Read the files on the path,
  not the whole tree.
- Library or platform behaviour: check `node_modules`/docs, not memory. Anything you can't verify
  is written as "verify during implementation", never stated as fact.
- Walk the **planning hazards** from Skill settings and note which apply.

## 3. Find the gaps (internal)

Check you can fill each without guessing: goal, at least 3 acceptance criteria, in scope, at
least one non-goal, edge cases, risks, and how each criterion gets verified. Only the gaps become
questions. Don't show this checklist to the user.

## 4. Ask

- `AskUserQuestion`, up to 4 questions per round, options grounded in the code, recommended
  option first with a one-line reason. Use previews for layout choices.
- Order: data and storage, then behaviour, then UI, then edge cases.
- If the code can answer it, state the answer and ask for confirmation instead.
- After each round, restate in 2–3 lines what is agreed and what is open.
- Usually 1–2 rounds. Stop when the acceptance criteria are ones the user would sign off on.

## 5. Write the plan

Use the template below. Store it where Skill settings says (e.g. a comment on the issue). Then
show the user the link and a summary of at most 5 lines, not the whole plan again.

```markdown
## Plan: <title>

**Goal:** <one sentence, user-visible outcome>

**Approach**
1. <step, files touched> (in implementation order)

**Reuse / mirror:** <paths and what to take from them>

**Acceptance criteria**
- [ ] <observable behaviour> (verify: unit test / browser / on device)

**Out of scope:** <at least one non-goal>

**Edge cases:** <case, then how it is handled>

**Risks and unknowns:** <specific, plus what to check first>

**Can't verify here:** <what needs a device or manual check> (or "none")

**Decisions:** <chose X over Y because Z> (only non-obvious ones)
```

No hedges like "(or X)" or "TBD" on load-bearing lines: decide, or ask.

## 6. Review (large only)

Spawn the `plan-reviewer` agent once, passing the plan text (or its location) and the issue
number. Fold its findings into the plan sections; don't append review notes. If it still says
NEEDS-REVISION after one re-run, put the open point to the user with a recommendation.

## Hand-off

Stop after the plan is approved. If the plan has UI scope, suggest `wireframe` next; otherwise
offer to start implementing on the issue's branch. Don't write code inside this skill.

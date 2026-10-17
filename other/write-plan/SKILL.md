---
name: write-plan
description: Turns an approved spec into a task-by-task implementation plan of paths, interfaces, behaviors and tests. Use when you have an approved spec or clear requirements for a multi-step change, before touching code.
argument-hint: "[spec path]"
---

# Write Plan

The plan is executed task by task, possibly in a fresh session that has only the plan, the spec, and the repository. Give each task what that executor needs to build it without guessing: paths, interfaces, behaviors, tests. Leave implementation code to the executor, which writes it against the real repository and runs it.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

Before your first commit of the spec or plan for this piece of work, check the plan's `Commits:` line or your partner's earlier answer. If neither settles it, ask once: "I'll work on branch `<name>`. May I commit the spec and plan to it as we go? Nothing is pushed or merged without asking. Reply with **yes** or **no**." Whatever the answer, move the work to that branch; never commit to `main` or `master`. If your partner declines, the spec and plan are held back: wherever a step says to commit them, leave them on disk; the `dietpowers:finish-branch` skill proposes those commits at the end. Code is always committed.

1. Check scope. If the spec spans independent subsystems, invoke the `dietpowers:update-spec` skill to remove all but one from the spec and add each of the others as an open item whose Why holds its removed sections word for word, then plan the one that remains. If the spec is missing something the plan needs, or planning shows it must change, invoke the `dietpowers:update-spec` skill.
2. Map the files: what gets created, what gets modified, what each is responsible for. Follow the codebase's existing patterns, and name the existing file each new one should imitate.
3. Draw task boundaries at the smallest unit that carries its own test cycle. Fold setup, config and docs into the task that needs them. Split only where a reviewer could reject one task while approving its neighbor.
4. Open the plan with a header: `Spec: <path> @ <commit>`, giving the spec and its current commit, which marks the approved version (`@ uncommitted` if commits are held back); `Base: <branch>`, the branch this work merges into; `Commits: approved` or `Commits: held back`, which covers the spec and plan only, since code is always committed; the goal in one sentence; the architecture in two or three; a Global Constraints section copying the spec's Constraints verbatim; and a References section carrying the spec's references each task will need, with their facts, written once.
5. For each task write: a `- [ ]` checkbox heading; Files, with exact paths; Interfaces, with the exact signatures it consumes and produces; Context, the plan references and existing files the task relies on, plus any fact only this task needs; Behavior, each item concrete enough that two engineers would build the same thing; Tests, naming each test, the behavior it checks, and the production change that would make it fail; the command that runs them.
6. Save to `docs/dietpowers/YYYY-MM-DD-<topic>-plan.md`, using the spec's topic, and commit it if commits are approved.

Terminal state: invoke the `dietpowers:adversarial-review` skill on the plan.

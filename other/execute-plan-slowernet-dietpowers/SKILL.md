---
name: execute-plan
description: Builds an approved plan task by task, test first, against the real repository. Use when you have an approved implementation plan to build.
argument-hint: "[plan path]"
---

# Execute Plan

You build the plan's tasks in order, test first, in this session. The plan names paths, interfaces, behaviors and tests; you write the code against the real repository.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

Commit your work on the feature branch as you go: the spec and plan may be held back, code never is. If you are on `main`, `master` or the plan's `Base:` branch, first ask once: "I'll create branch `<name>` for this work. Reply with **yes** or **no**." If your partner declines, do no code work until a branch is agreed. Nothing is pushed or merged without asking.

1. Work on the plan's branch.
2. Read the plan and the spec it links, in full. If either conflicts with the repository in a way that changes what gets built, raise it now, before writing code.
3. Use the plan's task checkboxes as your task list, mirrored in todos.
4. For each task: build it with the `dietpowers:tdd` skill against its Behavior and Tests, tick its checkbox, and commit. When a test fails and the cause isn't obvious, use the `dietpowers:find-root-cause` skill.
5. When the repository differs from what the plan assumes, make the routine call yourself and record it under the task in the plan as a `Departure:` line. Stop to ask only when the difference would change an interface, a spec requirement, or another task. When a change would alter behavior the spec describes, invoke the `dietpowers:update-spec` skill; if the change is declined and the task cannot be built without it, stop and ask your partner how to proceed.
6. Move from task to task without stopping to report progress or to offer to continue; put any status note in the same message as your next tool call. Stop only when nothing can move without your partner: a blocker you cannot resolve, a missing dependency, or a decision that changes the design.
7. If your partner changes a requirement, invoke the `dietpowers:update-spec` skill, then return to step 2.
8. When every task is ticked, report in a few lines: what was built, the calls you made under step 5, and anything left open.

Terminal state: ask "Continue with code review? Reply with **yes** or **no**." On yes, invoke the `dietpowers:adversarial-review` skill on the code. Otherwise, report what is built and what is uncommitted, and stop.

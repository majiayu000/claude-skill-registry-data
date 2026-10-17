---
name: brainstorm
description: Turns a request into an approved design spec. Use when starting a new feature, component, or change in behavior, or when asked to design, spec out or scope an idea, before any plan or code exists; or to resume a paused brainstorm.
argument-hint: "[request]"
---

# Brainstorm

The spec you write here is what the plan, the reviewers, and the code are all checked against. Anything it leaves unstated, such as an input's allowed values or what happens when a call fails, becomes a gap no later step can see, so settle those here. The best spec is usually the simplest design that meets the goal, built on established practice.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

Before your first commit of the spec or plan for this piece of work, check the plan's `Commits:` line or your partner's earlier answer. If neither settles it, ask once: "I'll work on branch `<name>`. May I commit the spec and plan to it as we go? Nothing is pushed or merged without asking. Reply with **yes** or **no**." Whatever the answer, move the work to that branch; never commit to `main` or `master`. If your partner declines, the spec and plan are held back: wherever a step says to commit them, leave them on disk; the `dietpowers:finish-branch` skill proposes those commits at the end. Code is always committed.

Record the brainstorm in a tracker, following `## Working directory` and `## Tracker format` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`; replies to your questions follow its `## Replies`.

For every question you ask in steps 3 and 5: record it as asked, and its answer, in the tracker; end it with `Reply with <options in bold>, or **pause**.`; ask it only if the answer would change the design, and make routine calls yourself, recording them as assumptions.

When versions or APIs matter, prefer what the current documentation for the version in use recommends and avoid what it marks deprecated or insecure; check the project's existing dependencies and framework features before adding new ones.

0. If your partner asked to resume, follow `## Resuming` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, then carry on from the step it leads to.
1. Read the project context, including files and history the request doesn't mention but the change may touch.
2. Check scope. If the request spans several independent subsystems, split it: brainstorm only the first, and add each of the others as an open item, to get its own spec later.
3. Before your first question, create the tracker (stage `brainstorm`; choose the topic now and reuse it for the spec filename). Ask about purpose: what the change is for, and for whom. If the request seems mistaken, or a simpler change reaches the same goal, say so before designing.
4. Research. Ask yourself: "Would this design, or the questions coming up as we decompose it, benefit from research into best practices, current developments, etc.?"
   - If not, give the skip line, both sentences: `No research: <reason>. Reply **research anyway** to override.` Then set the tracker's `Research:` line to `skipped, <reason>`, and go on to step 5. `research anyway` is accepted at any point until the design is approved: go to the proposal below and clear the `Research:` line. It counts as the first round, and afterwards the pending design question is asked again.
   - If so, write a proposal into the tracker as an item, then ask it: about three questions, each with the concept it covers and the kinds of source to check (for example official documentation, a changelog, a standards body or an issue tracker), ending `Reply with **go**, **trim** (name the numbers to drop), **skip**, or **pause**.` `trim` drops the numbered questions and dispatches the rest; a `trim` that names any number not on the list is asked again, and one that drops every question is a skip. An alternative that edits the list is an answer; if it grows past about three questions, ask which to drop. `skip` sets `Research:` to `skipped, <reason>`.
   - On `go`, or after a trim, dispatch a `general-purpose` subagent on the same model whose whole prompt is: "Read `${CLAUDE_SKILL_DIR}/researcher.md` and follow it," then `TOPIC` (one paragraph: the purpose as settled) and `QUESTIONS` (the approved list). Wait for its report. If there are no web tools, or the subagent fails or returns nothing usable, say so and carry on from the repository and your own knowledge.
   - Write the report into the tracker, and show your partner one line per question. If the report suggests a deep-research, pass that on and add it as an open item. If the findings contradict the request, say so before step 5.
   - If a later question needs facts this round did not cover, propose one more round the same way. Never a third.
5. Ask the remaining design questions: constraints, success criteria, the allowed values of each new input, and what should happen when each external call fails or is rerun.
6. Write the approaches into the tracker, then propose them with their trade-offs: the simplest one that meets the success criteria, and one built on an existing library, framework feature, or codebase pattern where one fits. Add a less obvious option only when it is genuinely better; if only one approach is sensible, say so. Recommend the simplest unless a trade-off rules it out, and say why. Cut anything speculative.
7. Write the design into the tracker, then present it, scaled to its complexity: architecture, components, data flow, error handling, testing. Give each unit one responsibility and an interface you can state without reading its internals. In an existing codebase, follow its patterns; clean up only what blocks this work, and mention other problems instead of fixing them.
8. Get explicit approval on the design; the approval question also ends with `, or **pause**.`
9. Write the spec to `docs/dietpowers/YYYY-MM-DD-<topic>-spec.md`, fill in the tracker's `Spec:` line with its path, and commit the spec if commits are approved. Sections: Goal; Constraints (exact values later steps must copy); Design; Inputs and failure behavior; Success criteria, each checkable by a test; Assumptions; References (docs, library versions, API details and existing code the design relies on, each with its link or path and the specific fact used); Out of scope. References cites each research fact the design uses, with its link; any question the design relies on that research left under Gaps, or could not answer, goes into Assumptions, marked unverified.

Terminal state: invoke the `dietpowers:adversarial-review` skill on the spec. Invoke no other skill from here.

Depth: ${CLAUDE_PLUGIN_ROOT}/shared/trackers.md, researcher.md

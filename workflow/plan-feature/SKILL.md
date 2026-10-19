---
name: plan-feature
description: "Entry point for planning a feature of an existing system with Löwy's Method and DMF: clarifies the request with the user, has the devflow:plan-writer agent draft cc-docs/plans/<feature>.md, runs the /devflow:review-plan workflow (blind Löwy, call-chain, DMF and delivery reviewers, adversarial verification, a judge, and the writer applying the rulings, round by round), then takes the user's answers and approval. Use when the user wants to plan a feature, write an implementation plan, or continue, review or approve an existing feature plan."
argument-hint: <feature request, or the name of an existing plan>
---

Part of the `devflow` plugin, which depends on the `lowy` and `dmf` plugins: their agents are named `lowy:<agent>` and `dmf:<agent>`.

Plan the following feature: $ARGUMENTS

**Read** `${CLAUDE_PLUGIN_ROOT}/references/feature-plan.md` first: the plan format, its status, and who may change what.
If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.

The roles stay separate, because independent roles are what make the review worth running:

- the `devflow:plan-writer` agent writes and revises the plan;
- the reviewers (`lowy:lowy-reviewer`, `lowy:call-chain-validator`, `dmf:dmf-reviewer`, `devflow:plan-reviewer`) review it, blind to each other;
- the `devflow:plan-judge` agent rules on their findings;
- you run the process and talk to the user.

Do not write or edit the plan yourself while the Agent tool is available.
Run `devflow:plan-writer` in the foreground: Claude Code may ask the user to approve its write, and only a foreground agent can ask.
When a write is refused, yours or the writer's (it replies `Not written:`), stop and tell the user what was not saved.
Never mark a plan approved without the user's explicit approval in this conversation.
When the Agent tool is not available (for example inside a subagent), do each role yourself, in order, following its agent file in `${CLAUDE_PLUGIN_ROOT}/agents/`.

## Phase 0: Find the Plan

List `cc-docs/plans/`.
If `.claude/docs/` exists and `cc-docs/` does not, the documents are from an earlier version of these plugins: offer to move them with `git mv .claude/docs cc-docs` before anything else, because no workflow can write under `.claude/`.

- If the argument names an existing plan, read its `> Status:` line and continue from it: `draft` goes to Phase 3, `reviewed` to Phase 4.
  An `approved` plan is ready; offer a new review (Phase 3) only if the user wants to change it, and say that a change needs their approval again.
  An `in-progress` or `done` plan is being built or is built: report its status and stop.
- Otherwise this is a new feature: choose a kebab-case feature name, to confirm with the user in Phase 1.
- If the request is for a new system or a new subsystem rather than a feature of an existing one, say that `lowy:architecture-advisor` (the 8-phase design pipeline) fits better, and plan the feature only if the user still wants that.

## Phase 1: Clarify

Read enough of the code and the design directory to know what they already answer: the services the feature touches, the domain types, the tests.
Then ask the user only what changes the plan and the code cannot answer: behavior at the edges (failures, limits), the scope boundary, and constraints (platforms, performance, compatibility, persisted data).
Ask at most four questions, in one round, with the AskUserQuestion tool when it is available, each with options and your recommendation; include the feature name.
When you cannot ask (a non-interactive run), do not stop: list the questions in the brief as unresolved, and the writer records them as open questions.

## Phase 2: Draft

Delegate to the `devflow:plan-writer` agent in Draft mode with:

- the brief: the request as the user gave it, their answers, the unresolved questions, and the constraints you found;
- where the relevant code and design files are;
- the feature name and today's date (`date +%F`, or `Get-Date -Format yyyy-MM-dd`).

Give the writer facts, not a design of your own: the plan is the writer's, and the reviewers judge it.

Show the user a short outline from the writer's reply: use cases, services touched, phases, open questions.
Ask whether to run the review now or correct the direction first; a correction goes back to the writer, which replaces the draft.
In a non-interactive run, go straight to the review.

## Phase 3: Review

Run the `devflow:review-plan` workflow with the Workflow tool.
Pass the feature name, plus `--thorough` when the user asked for a thorough review.
After answers that changed the plan, pass a JSON object instead, with `plan` and with `focus` set to the answers and the sections they changed.
The Workflow tool returns as soon as the workflow starts, and its result arrives later as a task notification, often after a quarter of an hour or more.
Until that notification arrives, tell the user only that the review is running: do not read the reports or the plan for an outcome, and never describe a result you have not received.

The workflow runs the rounds itself.
In the first, blind Löwy, call-chain, DMF and delivery reviewers check the plan, a skeptic per lens tries to refute its critical and major findings, and `devflow:plan-judge` rules on what survives.
Then `devflow:plan-writer` applies the rulings and logs them in §9, and the round's report is saved to `cc-docs/reviews/`.
When the judge accepted a critical or major change, a second round re-reviews it, with the lenses that own the sections it touched, and rules only on critical and major findings: its minor ones go to its report.
Reviewers and skeptics run on Sonnet, the judge and the writer on the session's model; `--thorough` runs them all on the session's model, with a call-chain reviewer per use case, three skeptics per lens, and every lens in the second round.
Its result is short: per round, the counts, the report's path and the plan's revision, then the next steps.

- When it stopped because a read or a write was refused, tell the user how to allow them, as the result says, and stop.
  Change their permission settings only when they ask you to.
- When it says changes were not re-reviewed, tell the user.
- Otherwise go to Phase 4.

Workflows need the Workflow tool, which some plans turn on only with `"enableWorkflows": true` in settings.
Without it, say so once and run the same roles with the Agent tool, without the verification pass, using the prompts in `${CLAUDE_PLUGIN_ROOT}/workflows/review-plan.js`:

1. In parallel: `lowy:lowy-reviewer`, one `lowy:call-chain-validator` for all the use cases in §3, `dmf:dmf-reviewer` and `devflow:plan-reviewer`.
2. `devflow:plan-judge` with all their findings.
3. `devflow:plan-writer` in Revise mode, in the foreground, with the plan path, the round number (one after the last round in §9), the date, the report's file name, and the judge's rulings exactly as the judge gave them, each a heading over a fenced block, as the workflow renders them.
4. Write the round's report to `cc-docs/reviews/<feature>-plan-review-<date>-round-<n>.md`, with the subsections the workflow renders: the kept findings per lens, the rulings, the accepted changes with their findings, the questions, the rejected findings, the conflicts, and the gaps.
5. When the judge accepted a critical or major finding, one more round on the changes only, with the reviewers that own the sections they changed and `devflow:plan-reviewer`.

## Phase 4: Answers and Approval

Read the plan's §8, and the rounds this run added to its §9.
From the round reports, read only the `Conflicts Between Lenses`, `Judge's Notes` and `Gaps` subsections, by searching for their headings: open a whole report only when the user asks about a finding.
Show the user:

- the plan's status and revision, and whether it is ready for approval: no open question in §8, and no critical or major change left un-re-reviewed;
- the changes made, one line per accepted ruling, from §9;
- what was rejected, and why, one line each;
- the conflicts between lenses the judge settled;
- the open questions.

Ask the open questions with their options and the recommendation from §8.
Send the answers to `devflow:plan-writer` in Answers mode, with the date.
If an answer changes §3-§6 in substance (a new use case, service, type or phase), offer another review (Phase 3), with the answers as its `focus`.

When no open question remains, ask the user to approve the plan.
Only on their explicit approval, send it to `devflow:plan-writer` in Answers mode as the approval, with the date.
The plan is then ready to be implemented phase by phase.

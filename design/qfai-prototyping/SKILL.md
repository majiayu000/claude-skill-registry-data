---
name: qfai-prototyping
title: QFAI Prototyping (DESIGN.md-driven UX Loop)
description: "Use when invoked by name or handed a QFAI work order to settle a visual or interaction decision by prototyping UI contracts under the root DESIGN.md."
argument-hint: ""
allowed-tools: [Read, Glob, Write, TodoWrite, Task, Agent, Bash]
steps: [prototyping-grill, prototyping-preflight, prototyping-loop, prototyping-handoff]
requires: [common-review-cycle]
mode: execution-focused
---

## /qfai-prototyping

Run the entry check of
`.qfai/assistant/rule/shared-skill-operating-baseline.md#workflow-run-entry-check`
first.

The loop is static-first and file-based by default. Supported surfaces: web,
mobile, desktop, mixed. cli surface is rejected. Only UI contracts declaring a
full `UI-NNNN` ID and a non-empty `screens[]` enter the prototyping scope;
`prototyping-grill` § Scope says which of them one invocation covers. The
primary contract comes from the request, or from
`qfai.config.yaml#prototyping.primaryUiContract`; the request wins. Both take
only a full `UI-NNNN` ID. A value in another form is refused, naming the
`UI-NNNN` shape and the value received, and is never normalised. When the
configured value is refused and the request names no contract, the run stops
before writing anything, naming the key and the value; it does not pick another
contract.

The skill runs the build and review loop with the user. The `qfai` command has
no `prototyping` command group, and no command or check certifies the result:
prototyping completes when the user confirms the prototype.

In an ordinary prototyping run, every file the loop writes stays under
`.qfai/prototype/`: the session record, each iteration and its reviews, and the
handoff. A `restyle` loop writes those same files and, outside
`.qfai/prototype/`, edits only the project's stylesheet and motion entry
points: the repository paths its `final/handoff.json` lists under
`entryPoints.stylesheet` and `entryPoints.motion`. No `qfai` command writes any
of these files. A command reads the handoff record
`.qfai/prototype/final/handoff.json`, which
`npx qfai validate --profile saas-package` checks against the CLI-HANDOFF schema, and the plain text of the
current `index.html` pages, which `npx qfai validate` checks.

## Inputs Priority

When unsure, read inputs in this order:

- P1: `.qfai/assistant/rule/*`, and `.qfai/assistant/skill/qfai-grilling/SKILL.md` before either session — the one before the loop and the one each reviewed prototype resumes
- P2: `.qfai/assistant/rule/agent-selection.md`, the cards under `.qfai/assistant/agent/`, and project context in the story tree
- P3: root `DESIGN.md` — the brand identity every iteration is built and reviewed against
- P4: the UI contracts under `<contractsDir>/ui/**/*.{yaml,yml}` and the references each step lists
- P5: earlier iterations and their reviews under `.qfai/prototype/`

Prototyping takes its direction from P3 and P4, and opens no file under
`paths.deliberationDir`.

## Steps

| Step                    | Runs                                                                                                      |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| `prototyping-grill`     | Always, first: fixes the scope and settles by talking what the prototype is for                           |
| `prototyping-preflight` | Always: checks the UI contracts, root `DESIGN.md` and the Playwright environment                          |
| `prototyping-loop`      | Always: build, review, and put each reviewed prototype to the user until they accept                      |
| `prototyping-handoff`   | Only after the user confirmed the prototype: copy it and write the handoff (restyle: `handoff.json` only) |

A step's gate that ends the run ends the invocation: zero UI-bearing contracts
at preflight, an escalated decision before the first iteration, or a stop or a
no-question mode when the prototype is put to the user.

Read `.qfai/assistant/step/<step>/STEP.md` for the current step only, run it,
then move to the next.

Inside an `npx qfai workflow` run, the work order lists the steps to run and
this file adds nothing to it.
Select roles by `.qfai/assistant/rule/shared-skill-delegation-baseline.md`.

Questions to the user follow
`.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.
This skill's own are whether a reviewed prototype is done and a missing brand
intent.

### Reviewer Gate

After the last step, run one review through `common-review-cycle`: the code
review, by `implementation-reviewer` and `product-surface-reviewer`. The
reviewers judge the rendered
prototype, never the code alone. Their findings inform the user; they do not
decide completion.

## Completion

The invocation completes when the user confirms the prototype and
`prototyping-handoff` has written the handoff. A blocking finding the latest
review still lists at that point is named in the final report. Every decision
a session adopted is an Agent decisions row of the run's deliberation record,
and the final report does not list it. Ask about the actions under Next
only when proceeding requires the user's answer, as
`.agents/rules/user-questions.md` § 6 sets out. A completion-only report needs
no question. Under a no-question mode, list any remaining actions instead.

## Next

- `/qfai-implement` / `/qfai-verify`

## Default Autopilot Policy

- ask-user:
  - whether a reviewed prototype is done — this skill's own operation, because
    look and feel are the user's judgement

project_memory:

- Prototyping completes on the user's confirmation; no command certifies it.
- Every file the loop writes is under `.qfai/prototype/`, except the stylesheet and motion entry points a `restyle` loop edits; a `qfai` command reads only `final/handoff.json` and the plain text of the current `index.html` pages.

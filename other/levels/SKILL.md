---
name: levels
description: Conduct the connected level skills as one workflow. Asks the user what they want to do with a multi-select prompt, sets a target level per chosen skill, then runs the skills in a fixed safe order with a gate before each one. Use when the user runs /levels or asks to take a project through the whole level process.
summary: Run several skills as one workflow
argument-hint: "[new|raise|redesign|release|present] [audit|build] [from <phase>]"
model: inherit
---

# Levels

Arguments: `$ARGUMENTS`

Parse the arguments:

- **ROUTE**: `new`, `raise`, `redesign`, `release` or `present`. Optional shortcut. When given, it pre-selects skills and the question prompt in Step 1 is skipped.
- **MODE**: `audit` (every skill audits only) or `build` (skills may build). Default `audit`.
- **FROM**: a phase name to resume from. Default: the first phase not marked done in `LEVELS.md`.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the conductor. You do not audit, plan or build anything yourself, apart from the cross-layer check in Step 3. You decide which level skill runs next, pass it context, and keep the record. Every skill keeps its own rules, its own delegation gate and its own model warnings.

## Phases

| Phase | Skills, in order | Skipped when |
|---|---|---|
| Orient | `levels-status` | never |
| Define | `idea-level` | a confirmed blueprint or a working product exists |
| Shape | `ux-level`, `restyle-level` | the project has no interface |
| Build | `data-level`, then `backend-level`, then `design-level` | nothing chosen to build. Skip `data-level` when nothing is stored. Skip a layer that does not exist or is not in scope |
| Harden | `test-level`, `security-level`, `perf-level`, `code-level` | never as a whole. Skip single skills by the level plan |
| Release | `docs-level`, `ship-level` | the product is not going to be run by anyone else or anywhere else |
| Present | `pitch-level` | nobody needs persuading |

The order inside a phase is fixed, whatever order the user picked things in. Flow comes before look. Stored data comes before the layers that use it. Tests come before any skill that changes working code. Structure work comes last in Harden. Written steps come before the release rehearsal that follows them.

## Routes

Shortcuts for the common selections:

- **new**: Define, Shape, Build, Harden, Release.
- **raise**: the skills `levels-next` ranks highest, one at a time.
- **redesign**: Shape, then `design-level` in `build` mode, then `test-level`.
- **release**: `test-level`, `security-level`, then Release.
- **present**: Present only.

## Step 1: Orient and ask

1. Run `levels-status`. Read `LEVELS.md` and its flow section if present.
   If `LEVELS.md` does not exist, print one line before the prompt: `New here? Run /levels-help for a short guide.`
2. If a flow is recorded as unfinished and no ROUTE was given, ask first: **Resume it** (Recommended), or **Start a new selection**.
3. If no ROUTE was given, ask what the user wants to do. Use one AskUserQuestion call with four questions, each with `multiSelect: true`. The user may tick any number in each, or none.

   - **Plan and shape**, "What do you want to work out?"
     - Find or sharpen the idea (`idea-level`)
     - Fix how tasks flow (`ux-level`)
     - Pitch new looks or layouts (`restyle-level`)
   - **Build**, "What do you want built or raised?"
     - Interface (`design-level`)
     - Server and logic (`backend-level`)
     - Stored data and migrations (`data-level`)
   - **Harden**, "What do you want made safer?"
     - Tests (`test-level`)
     - Security (`security-level`)
     - Speed (`perf-level`)
     - Code structure (`code-level`)
   - **Ship and show**, "What do you want ready for others?"
     - Documentation (`docs-level`)
     - Release and deploy (`ship-level`)
     - Pitch or presentation (`pitch-level`)

   Write each option's description from the project state: the current level from the levels block, and the count of open gaps. From the state, mark up to two options per question as recommended: put them first and end the label with "(Recommended)". Leave out options that cannot apply, such as interface options in a project with no interface, and say which were left out and why.

4. Resolve the selection:
   - Nothing ticked anywhere: run `levels-next` and offer its single recommendation.
   - A ticked skill depends on one not ticked (a build with no tests after it, a release with no written steps, a restyle on a flow never checked): name the missing skill and ask once whether to add it. Follow the answer.
5. Ask once, in one round, only what `LEVELS.md` does not answer: what the product is for, who uses it, where it runs, any date, and how much model spend the user accepts for this run (low, medium, no limit).
6. Write the selection and the answers to the shared part of `LEVELS.md` so no later skill asks them again.

## Step 2: Level plan

1. Put the selected skills into phase order.
2. Show one table: each selected skill, its current level, the target level you propose, and one line of reason. Size targets to the product. A small tool does not need level 4 everywhere.
3. With a low spend limit, propose running fewer of the selected skills first, not lower quality inside each one. Say which you would defer.
4. Wait for the user to confirm or edit the table. Record it in the flow section.

## Step 3: Run

For each skill in the plan, in order:

1. Print one line: `Phase <name> → <skill> <level> <mode>`.
2. Ask with AskUserQuestion: **Run** (Recommended), **Skip**, **Change level or mode**, **Stop here**. State that the skill starts its own model spend.
3. Invoke the skill with the Skill tool, passing level, mode and scope. Tell it that `levels` called it: it reuses the shared record, reports back, and offers no handoff of its own.
4. When it returns, read its findings for anything that belongs to another skill, and apply the back-edge table.
5. Update the flow section: skill, level reached, open gaps, date.
6. When `backend-level` and `design-level` have both run in this flow, run the cross-layer check once, by reading both sections of the record and the code they cite:
   - Every state the backend can return (loading, empty, error, partial, conflict, rate-limited, offline, expired session) has a designed state in the interface.
   - Every edge case the backend handles is shown to the user in a way they can act on.
   - Every action in the interface maps to a backend entry point that validates it. Nothing is enforced only in the interface.
   - Live data in the interface matches what the backend can push or be polled for under the hosting profile.

   Queue each failure for the layer skill that owns it, by the back-edge rule. Record the result in the flow section.

In `audit` MODE, after the last skill, show one merged list of gaps across all skills, ranked by risk, and ask which to build. Then run those skills again in `build` mode in phase order.

## Back edges

A finding that belongs to another skill does not start that skill at once. Queue it, then offer it at the next gate with the evidence. This applies even when the user did not select that skill in Step 1.

| From | Finding | Queue |
|---|---|---|
| any skill | a bug in a layer it does not own | `backend-level` or `design-level`, scoped to the bug |
| `test-level` | a failing test that shows a product bug | the owning layer skill, then `test-level` again on that path |
| `security-level` | a fix that changes stored data | `data-level` |
| `perf-level` | a slow query or oversized response | `backend-level` or `data-level` |
| `ship-level` | missing health check, shutdown or startup validation | `backend-level` |
| `ux-level` | the flow is sound and the look is the complaint | `restyle-level` |
| `restyle-level` | a direction is chosen | `design-level` in `build` mode |
| `design-level`, `restyle-level` | no clear concept to design from | `idea-level` |
| `pitch-level` | a claim with no proof behind it | `test-level` or `perf-level` |

Rules:

- A queued skill runs once per finding. If the same finding returns after its fix, stop and report it to the user instead of running the skill a third time.
- After any skill changes working code outside Harden, queue `test-level` for the changed paths.
- Never run two building skills at the same time on the same files.

## Step 4: Close

After the last skill, or when the user stops:

1. Run `levels-status` and show the before and after table.
2. List what was skipped, what is queued and not run, and every step the user must do by hand (live deploy steps, replaced secrets, decisions left open).
3. Run `levels-next` and show its single recommendation.

## Record

Keep a flow section in `LEVELS.md`: the selection, mode, the level plan, each skill with its status (done, skipped, queued, stopped) and date, and the queue. Keep the levels block and every other skill's section intact. Add one row to the levels block:

```
<!-- levels
flow: phase=harden left=3
-->
```

## Quality bar

No skill run without the user's yes. No skill run that the user did not select, unless a finding queued it and the user approved it at the gate. No phase reported done unless its skill reported back. No finding dropped between skills: every one is fixed, queued or listed as open. The conductor never audits, plans or edits.

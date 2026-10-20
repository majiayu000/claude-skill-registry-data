---
name: <name>-level
description: Audit <what part of a project> against a 5-level <what the scale measures> scale, propose options, then split the chosen work into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /<name>-level or asks to <the requests that should trigger it>.
summary: <Six words or fewer for the skill table, starting with a verb>
argument-hint: "[level 1-5] [audit|build] [scope path]"
model: inherit
---

# <Name> level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **SCOPE**: any path in the arguments limits the audit to that area. Default: <the whole of this layer>.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the <role> lead on this project. Work to the LEVEL. The levels describe <what they measure>, not <a tool, stack or style>. Keep the project's <existing choices> unless the user asks to change them.

<One or two sentences on what this skill never does, if it has a hard limit. Delete if none.>

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **<Name>.** <Requirements, as things that can be checked.>
2. **<Name>.** <Requirements.>
3. **<Name>.** <Requirements.>
4. **<Name>.** <Requirements.>
5. **<Name>.** <Requirements.> Only choose this when <the condition that justifies it>.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, <make the decisions that belong to the plan> or review their own work.

## Step 0: <Kind of> context

Before the audit, establish <what the audit depends on>.

1. Look first. Read <the files that answer the questions>. Read `LEVELS.md` if it exists and reuse <the profiles this skill needs>.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **<Question>**: <option> / <option> / <option>.
   - **<Question>**: <option> / <option> / <option>.

   Round two, only what still matters:
   - **<Question>**: <what to ask>.
   - **<Question>**: <what to ask>.

3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it as a risk.
4. Print a short <kind of> profile and wait for the user to confirm or correct it.

## Step 1: Audit (Opus)

1. <How to examine this layer. Say what to run and what to read.>
2. State the level the project is at now, with one line of evidence per requirement (file and line, or command output). Say what is already sound and must be kept.
3. List every unmet requirement between the current level and the target LEVEL, ranked by <this layer's order of harm>.
4. For each of the top gaps, give two or three distinct options. For each: what it changes, what it costs (<the costs that matter here>), when it is the wrong choice. Mark the one you recommend and why.
5. Add a short list of optional ideas from one level above the target, labelled as stretch.
6. If the target LEVEL is wrong for this product, say so and name the level you would pick.
7. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen work into sub-plans that can each be done and checked alone. One sub-plan changes <one unit of work for this layer>. There is no fixed count: let the size of the project and of the chosen work set it. Do not pad a small job with trivial sub-plans, and do not merge unrelated work to keep the count low.
2. Each sub-plan states:
   - Goal, in one sentence.
   - Files to change, and files it must not touch.
   - Exact steps, with <the values to use>. Leave no <kind of> decision to the executor.
   - Done check: what to run or look at to confirm it worked.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: <work that can be fully written out in advance>.
   - Sonnet when needed: <work that cannot>.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans. Mark which can run in parallel (no shared files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, goal, files, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
4. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the context it needs.
- Run parallel sub-plans in one message. Run sequential ones in order.
- <What executors in this layer never do.>
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish, <how to check the result>. Repeat the audit and report the level reached, what moved and what is still open.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its <name> section with: <the profile>, target and reached level, open gaps, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open gaps. Tools read it, so keep the format exact.

```
<!-- levels
<key>: 2/3 gaps=5
-->
```

**Handoffs from this skill.**

- <A finding that belongs to another layer>: offer `<existing-skill>`, <with what context>.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

<The few things that must be true before anything is reported as done. Each one checkable.>

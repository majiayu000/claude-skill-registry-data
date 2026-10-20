---
name: design-level
description: Audit a project's interface against a 5-level design sophistication scale, propose options, then split the chosen work into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /design-level or asks to raise, rate or audit design sophistication.
summary: Raise the quality of the interface
argument-hint: "[level 1-5] [audit|build] [a11y]"
model: inherit
---

# Design level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 4.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **ACCESSIBILITY**: on only if the arguments contain `a11y`. When on, also require WCAG AA contrast, keyboard access, visible focus and reduced-motion support, and audit against them. When off, do not raise these.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the design lead on this project. Work to the LEVEL. The levels describe sophistication, not a theme. Choose the visual world that suits this project and its users.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Clean.** Consistent spacing, one type scale, a small palette with roles, text that is easy to read on its background, works at phone width. Component-library defaults are acceptable.
2. **Considered.** All colour and spacing come from tokens. Each typeface has one job, two or three families at most. Loading, empty and error states are designed. Hover, focus and pressed states on every control. Numbers that change keep a fixed width.
3. **Branded.** One concept drives every surface. A real logo mark plus wordmark, reused at every size including the favicon. No default component-library look. Small screens get their own layout, with navigation and primary action placed for thumb reach. The entry surface states what the product is, shows real content and gives one primary action.
4. **Studio.** A hand-built signature centrepiece that belongs to this product only and responds to the user. Motion is a system: one shared transition mechanism with variants per page or state, shared timing and easing. Live data is shown as live, with staged warnings and an unmistakable resolved state. Loops pause when the page is hidden, navigation never depends on an animation finishing. A stated performance budget, with effects reduced on weak devices.
5. **Showcase.** Level 4 plus original interaction ideas not seen elsewhere, custom illustration or imagery, opt-in sound or haptics, narrative structure on long pages, and detail that holds at every size and state. Only choose this when the product's success depends on the impression it makes.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, make design decisions or review their own work.

## Step 0: Design context

Before the audit, establish who the interface is for and what must be kept.

1. Look first. Read the interface code, styles, tokens, any logo or brand files, and the README. Read `LEVELS.md` if it exists and reuse the user profile, the hosting profile (devices, network) and any blueprint.
2. Ask the user only what is still open, with AskUserQuestion, in one round:
   - **Who uses it**: who they are and what they come to do.
   - **Where it is used**: phone / desktop / both, and which matters most.
   - **What must stay**: an existing brand, logo, palette or component library that must be kept, or nothing.
   - **Tone**: two or three words for how it should feel, or "you choose".
3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it as a risk.
4. Print a short design profile and wait for the user to confirm or correct it.

## Step 1: Audit (Opus)

1. Read the existing interface. State the level it is at now, with one line of evidence per requirement (file, screen or element). Say what is already good and must be kept.
2. List every requirement between the current level and the target LEVEL that is not met, ranked by how much it holds the design back.
3. For each of the top gaps, give two or three distinct options. For each: what it changes, what it costs (effort, risk, performance), when it is the wrong choice. Mark the one you recommend and why.
4. Add a short list of optional ideas from one level above the target, labelled as stretch.
5. If the target LEVEL is wrong for this product, say so and name the level you would pick.
6. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen work into sub-plans that can each be done and checked alone. One sub-plan changes one concern in as few files as possible. There is no fixed count: let the size of the project and of the chosen work set it. A small change may need two or three sub-plans, a full redesign of a large project may need dozens. Do not pad a small job with trivial sub-plans, and do not merge unrelated concerns to keep the count low.
2. Each sub-plan states:
   - Goal, in one sentence.
   - Files to change, and files it must not touch.
   - Exact steps, with the values to use (tokens, sizes, timings, copy). Leave no design decision to the executor.
   - Done check: what to run or look at to confirm it worked.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: mechanical edits, token and style changes, copy, applying a fully specified pattern, running build, tests and lint.
   - Sonnet only when needed: work across several files that must stay consistent, new component logic, animation or state code, anything where the steps cannot be fully written out in advance.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans. Mark which can run in parallel (no shared files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, goal, files, model, parallel or sequential.
2. Print a warning line with the totals, with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
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
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish, check every changed screen at desktop and phone width with real content. Repeat the audit and report the level reached, what moved and what is still open. For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers: the constraint profile, the hosting profile (devices, network, load) and any blueprint. At the end, create or update its design section with: the design profile, target and reached level, what was chosen, open gaps, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open gaps. Tools read it, so keep the format exact.

```
<!-- levels
design: 3/4 gaps=5
-->
```

**Handoffs from this skill.**

- A gap that the interface cannot close alone, such as a state the backend never reports, missing live data, or a rule enforced only in the interface: offer `backend-level`, scoped to the entry points involved. List the exact states or data the interface needs.
- The audit finds no clear concept to carry through the design (level 3 cannot be reached because the product does not know what it is): offer `idea-level` with the current product as the seed.
- The user wants both layers raised: say that `levels` runs `backend-level` and `design-level` in order with a cross-layer check, and give the command. Do not start it from here.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff. When called with a blueprint and no existing interface, skip the audit and plan the first version from the blueprint at the target LEVEL.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

Real content on every screen, no placeholder text, nothing reported as done unless checked.

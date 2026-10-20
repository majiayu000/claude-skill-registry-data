---
name: ux-level
description: Audit how easily real users complete their tasks against a 5-level usability scale, by walking each key task as a first-time user and checking flow, feedback, error recovery and wording, then propose options and split the chosen fixes into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Covers behaviour and flow, not visual style. Use when the user runs /ux-level or asks to audit or improve usability, flows, onboarding or interface wording.
summary: Check whether users can finish their tasks
argument-hint: "[level 1-5] [audit|build] [scope: task or screen]"
model: inherit
---

# UX level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **SCOPE**: any task, screen or path in the arguments limits the audit to it. Default: every key task.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the experience lead on this project. Work to the LEVEL. The levels describe how easily the intended users get their tasks done, not how the product looks. This skill changes flow, behaviour, feedback and wording. It does not restyle: colour, type, motion and visual identity belong to `design-level`. Keep the product's content and rules unless the user asks to change them.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Possible.** Each key task can be completed. Every control says what it does. Nothing leads to a dead end.
2. **Clear.** At every step the user can tell where they are, what just happened and what to do next. Errors say what went wrong and how to fix it, in the user's words. One name per thing and one pattern per kind of action, everywhere. Forms keep what was typed and point at the field that needs fixing.
3. **Guided.** A new user reaches a first success without outside help. Empty screens say what belongs there and how to start. Actions that cannot be undone ask first, and the rest can be undone. Work in progress survives a refresh, a lost connection or coming back later. The flow suits the real setting: the device, the surroundings, the time pressure, the interruptions.
4. **Observed.** People from the real audience have been watched doing the key tasks. Steps, time, mistakes and questions were recorded. What they struggled with was fixed and watched again. The less common paths are designed too: a mistake part way, a second device, two people at one screen, returning after a break.
5. **Tuned.** Use is measured continuously and each key task has a known success rate. Changes are tried against each other. Regular users have faster paths. Research with users is routine. Only choose this for a product with enough ongoing use to measure.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, decide how a flow should work, write their own wording or review their own work.

## Step 0: User context

Before the audit, establish who uses the product, where, and for what.

1. Look first. Read the routes, screens, forms and messages. Read `LEVELS.md` if it exists and reuse the constraint, hosting and reader profiles.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Who uses it**: the kinds of user, and how familiar each is with products like this.
   - **Key tasks**: the three to five things users come to do, in the user's own words, and what counts as done.
   - **Setting**: at a desk / on a phone on the move / in a busy or bright place / on a shared or public device / under a time limit.
   - **Help available**: someone nearby to ask / written instructions / nobody.

   Round two, only what still matters:
   - **Where people get stuck now**: questions asked again and again, steps people get wrong, places they give up.
   - **Stakes of a mistake**: nothing lost / lost time / lost work, money or standing.
   - **Sessions**: one sitting or several, one person or a group, one device or more.
   - **Access to users**: whether real users can be watched, and how many.
   - **Fixed parts**: flows, rules or wording that must not change.

3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it.
4. Print a short user profile: each kind of user, their key tasks with the finish line for each, and the setting. Wait for the user to confirm or correct it.

Judge every flow against this profile. A step that is fine at a desk can fail on a shared station under a countdown.

## Step 1: Audit (Opus)

1. Task walkthrough. Run the product if it can be run, and use it as a first-time user from the profile. For each key task record every step: what is on screen, what the user must already know, what they must decide, what they must type, and what could go wrong. Count the steps and the decisions. Mark each point where a user would hesitate, guess, backtrack or need to ask. If the product cannot be run, do the walkthrough from the code and say that confidence is lower.
2. For each task, also walk the paths that are not the ideal one: a wrong entry, a refresh, a lost connection, going back, leaving and returning, running out of time, doing it a second time.
3. Check each screen in scope against these categories. For each record: sound, weak, or does not apply.
   - **Orientation**: where am I, how did I get here, how do I leave, how far along am I.
   - **Feedback**: every action shows a result, waits show progress, success and failure cannot be confused.
   - **Next step**: the main action is obvious, and there is one.
   - **Errors**: prevented where possible, explained in the user's terms, fixable in place, nothing typed is lost.
   - **Consistency**: same word, same place and same behaviour for the same thing.
   - **Wording**: plain, specific, in the user's vocabulary, no internal terms, labels that say what happens.
   - **Forms**: only needed fields, sensible defaults, the right input type, forgiving formats.
   - **Memory load**: nothing to remember from an earlier screen, nothing to work out in the head.
   - **First use**: a new user knows what this is and what to do first.
   - **Empty, waiting and finished states**: each says what is going on and what to do.
   - **Safety**: undo or confirm on anything that loses work, no easy accidental triggers.
   - **Setting fit**: target sizes, reading distance, one-handed use, noise, glare, time pressure, shared devices, as the profile requires.
4. For each weak point, write what the user experiences, in one or two sentences, and cite the screen and the file. Label every finding as expert review. Do not present it as something users were seen doing.
5. State the level the product is at now, with one line of evidence per requirement. Say what already works well and must be kept.
6. List the findings ranked by harm: a task that cannot be finished first, then lost work, then errors a user cannot recover from, then confusion that needs outside help, then friction.
7. For each of the top findings, give two or three distinct options. For each: what the user would experience instead, what it costs (effort, risk to other flows, new states the server must support), when it is the wrong choice. Mark the one you recommend and why. Prefer removing a step over explaining it.
8. Add a short list of optional ideas from one level above the target, labelled as stretch.
9. If the target LEVEL is wrong for this product, say so and name the level you would pick. Level 4 needs real users: if none can be watched, say that level 4 cannot be reached and stop at 3.
10. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Observation kit (level 4 and above)

This skill cannot watch people. For level 4 it prepares the session and works from what the user brings back.

1. Write a session script: an opening that asks the person to think aloud and says the product is being tested, not them; the key tasks as goals, with no hints about how; and what to note for each (finished or not, time, wrong turns, questions, words they used).
2. State how many people and of which kind. Three to five from the real audience is enough to find the main problems.
3. The user runs the sessions and reports back. Record the results as observed, separate from expert review findings.
4. Re-rank the findings using what was observed. Where observation contradicts the expert review, observation wins.

Never invent observations, quotes, success rates or user opinions.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen work into sub-plans that can each be done and checked alone. One sub-plan changes one step, state or message set. There is no fixed count: let the size of the product and of the chosen work set it. Do not pad, and do not merge unrelated flows.
2. Each sub-plan states:
   - Goal, in one sentence, as what the user will be able to do.
   - Files to change, and files it must not touch.
   - Exact behaviour: each state, what triggers it, what is shown, and where the user can go next.
   - Exact wording for every label, message and hint. Leave no wording to the executor.
   - Visual treatment: reuse the named existing component or pattern. No new styling.
   - Done check: the walkthrough steps to repeat, including the wrong-entry and refresh paths, and the expected result of each.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: replacing wording, labels and messages, adding a fully specified empty, confirm or error state that follows an existing pattern, field types and defaults, reordering content.
   - Sonnet when needed: restructuring a flow, form validation logic, saving and resuming progress, undo, first-run guidance, anything that changes state handling across screens.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans. Mark which can run in parallel (no shared files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, task it serves, goal, files, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. List every change to a flow that existing users already know, since it may surprise them.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the user profile.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors use the wording given, word for word. They do not restyle, do not change rules or content, and do not remove a step the sub-plan did not name.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish, repeat the full task walkthrough from Step 1, including the paths that are not the ideal one, at the device sizes the profile names. Compare steps, decisions and hesitation points before and after for each task. Confirm no other flow was broken. Report the level reached, findings closed and open, and which results are expert review and which were observed.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its UX section with: the user profile, target and reached level, steps and decisions per key task before and after, open findings marked as expert review or observed, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open findings. Keep the format exact.

```
<!-- levels
ux: 2/3 gaps=8
-->
```

**Handoffs from this skill.**

- A fix needs visual work, such as a new component, a clearer hierarchy or a designed state with no existing pattern to reuse: offer `design-level`, with the list of states.
- A fix needs the server to do something new, such as saving progress, allowing undo, or reporting why something failed: offer `backend-level`, scoped to that entry point.
- Users need written help outside the product: offer `docs-level`, with the questions they ask.
- The repaired flows should be protected from breaking again: offer `test-level`, with the walkthrough steps as cases.
- The key tasks themselves are unclear, or the product is solving the wrong problem for these users: offer `idea-level`, with the product as the seed.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

Every finding tied to a real task and a real screen. Expert review never presented as observed behaviour. No invented users, quotes or numbers. No restyling. No wording left to an executor. Nothing reported as fixed until the walkthrough was repeated.

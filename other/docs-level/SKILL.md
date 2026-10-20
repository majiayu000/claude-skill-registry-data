---
name: docs-level
description: Audit a project's documentation against a 5-level scale, checking that it is accurate against the code and usable by the people who read it, then propose options and split the chosen writing into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /docs-level or asks to audit, write or improve documentation.
summary: Make documentation accurate and usable
argument-hint: "[level 1-5] [audit|build] [scope path]"
model: inherit
---

# Docs level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated writing). Default `audit`.
- **SCOPE**: any path in the arguments limits the audit to that area or document. Default: the whole project.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the documentation lead on this project. Work to the LEVEL. The levels describe how well the documentation serves its readers, not how much of it there is. Keep the project's existing format, location and tone unless the user asks to change them. Shorter and correct beats longer and vague.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Present.** A README says what the project is, who it is for, and how to install and run it.
2. **Usable.** A newcomer can set up and run the project from the written steps alone. Every configuration value is described. The common tasks are covered. Examples run as written. Known problems and their fixes are listed.
3. **Complete.** Each kind of reader has what they need: the person using it, the person running it, the person changing it. The interface or API reference matches the code. An overview explains how the parts fit and why they are built that way. Changes between versions are recorded. Documentation lives with the code it describes.
4. **Maintained.** Documentation is checked automatically: examples run as tests, links are checked, reference pages are generated from the code where possible. Important decisions are recorded with their reasons. Runbooks cover likely failures. A newcomer has walked the onboarding path and the time it took is known. Updating documentation is part of every change.
5. **Published.** A searchable site, versioned with the product. Tutorials, task guides, reference and explanation are kept as separate kinds of page. Readers can report problems. Translations where the audience needs them. Only choose this for a product with outside users or contributors.

## Models

Planning and audit run on Opus only. Writing runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never does the writing. Executors never change scope, decide what a reader needs or review their own work.

## Step 0: Reader context

Before the audit, establish who reads the documentation and what they need from it.

1. Look first. List every document: README, guides, comments meant for readers, in-app help, reference pages, changelog, decision notes. Read `LEVELS.md` if it exists and reuse the constraint, hosting and release profiles.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Who reads it**: people using the product / people running it on the day / people changing the code / people judging or evaluating it / the builder later on. More than one may apply.
   - **Their background**: new to the field / comfortable with the tools / expert.
   - **What they ask most**: the questions the user already answers by hand again and again.
   - **Where it is read**: in the repository / on a site / inside the product / printed or offline.

   Round two, only what still matters:
   - **Language and tone**: language, formal or casual, any house style to match.
   - **What must stay out**: internal addresses, credentials, unreleased plans, anything private.
   - **Upkeep**: who updates documentation, and how often the product changes.
   - **Handover**: whether someone else will take the project over, and when.

3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it.
4. Print a short reader profile: each kind of reader, what they need to do, and what they already know. Wait for the user to confirm or correct it.

Do not write for a reader the profile does not include. A solo tool does not need a contributor guide.

## Step 1: Audit (Opus)

1. Follow-the-docs test. Copy the repository to a throwaway folder with nothing installed. Do exactly what the documentation says, as the least experienced reader in the profile, using only what is written. Record every step that fails, is missing, is out of order or assumes unwritten knowledge. Do not touch the user's working files.
2. Accuracy check, documentation against code. For every command, path, option, setting, route, function and screen the documentation names, confirm it exists and behaves as described. Record each mismatch with both locations.
3. Coverage check, code against documentation. For every entry point, configuration value, command and user-facing feature in scope, record: documented, documented in part, or not documented.
4. Reader check. For each reader in the profile, list the tasks they need to do and whether the documentation gets them there. Flag text that is correct but unusable: buried, out of order, full of undefined terms, or written for a different reader.
5. Flag what should be removed: duplicated, outdated or contradictory pages, and anything the profile says must stay out. Report a credential or private address found in documentation as urgent.
6. State the level the project is at now, with one line of evidence per requirement. Say what is already good and must be kept.
7. List every gap, ranked by harm: wrong instructions first, then missing steps that block a reader, then missing reference, then clarity.
8. For each of the top gaps, give two or three distinct options. For each: what it adds, what it costs to write and to keep current, when it is the wrong choice. Mark the one you recommend and why. Prefer generating from the code and fixing an existing page over adding a new one.
9. Add a short list of optional ideas from one level above the target, labelled as stretch.
10. If the target LEVEL is wrong for this product or its readers, say so and name the level you would pick.
11. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Where the documentation and the code disagree, do not assume which is right. Report it and ask.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Step 2: Execution plan (Opus)

After the user chooses, do not write directly.

1. Split the chosen work into sub-plans that can each be done and checked alone. One sub-plan covers one page or one section. There is no fixed count: let the size of the project and of the chosen work set it. Do not pad, and do not merge unrelated pages.
2. Each sub-plan states:
   - Goal, in one sentence, naming the reader it serves.
   - The file to add or change. Product code it must not touch.
   - An outline: the headings, and under each the points to make, in order.
   - Sources: the exact code files to read for the facts. Every claim must come from them.
   - Style: language, tone, length limit, and the terms to use for each thing.
   - Done check: the commands or steps in the page run as written, and each claim points to its source.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: setup steps, configuration tables, command lists, changelog entries, fixing mismatches, formatting, pages with a full outline and few sources.
   - Sonnet when needed: architecture overviews, reference pages that need many files read together, tutorials, explanations of why something is built as it is.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans. Mark which can run in parallel (different files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, page, reader, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. List any page the plan deletes or replaces, and wait for a separate yes for those.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: write in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the reader profile.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors write only what the sources show. They never invent a command, option, feature or behaviour, never describe planned work as existing, and never change product code. A fact they cannot confirm is reported back as a question, not written as a guess.
- Executors write plainly: the reader's task first, steps in the order they are done, one term per thing, no selling and no filler.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish:

1. Repeat the follow-the-docs test from Step 1 against the new documentation.
2. Check a sample of claims in every new or changed page against the code. Check all of them in setup and configuration pages.
3. Read each page as its reader: does it get them to the task, in order, without unexplained terms.
4. Report the level reached, mismatches fixed and remaining, coverage before and after, and questions the executors raised that the user must answer.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its docs section with: the reader profile, target and reached level, open gaps, unanswered questions, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open gaps. Keep the format exact.

```
<!-- levels
docs: 2/3 gaps=5
-->
```

**Handoffs from this skill.**

- The written setup is right but the project itself fails to build, start or configure: offer `ship-level`.
- The documentation and the code disagree and the code is the one that is wrong, or behaviour is undefined: offer `backend-level`, scoped to that entry point.
- Readers need help inside the product, or wording on screen is the problem: offer `design-level`, with the list of screens.
- Examples should run as tests so they cannot go stale: offer `test-level`, with the list of examples.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff. When called after a build, document what that build changed first.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

Nothing written that the code does not show. Every command and step run as written before it is reported as done. No page for a reader who does not exist. No credential or private detail in any document. No page deleted without a separate yes. Length is not a measure of quality.

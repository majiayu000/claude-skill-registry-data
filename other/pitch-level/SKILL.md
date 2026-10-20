---
name: pitch-level
description: Audit and build how a finished project is presented (demo, talk, deck, one-page summary, answers to hard questions) against a 5-level scale, fitted to a named audience and their criteria, using only claims the project can back. Opus shapes the story and reviews, Haiku and Sonnet draft materials. Use when the user runs /pitch-level or asks to prepare a demo, presentation, pitch, submission or showcase.
summary: Prepare a demo, talk or submission
argument-hint: "[level 1-5] [audit|build] [format: demo, deck, video, written]"
model: inherit
---

# Pitch level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated drafting). Default `audit`.
- **FORMAT**: any format named in the arguments limits the work to it. Default: whatever the occasion needs.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the presentation lead on this project. Work to the LEVEL. The levels describe how well the project's real strengths reach a specific audience, not how polished the slides are. This skill presents what exists. It never changes the product.

## Honesty rules

- Every claim must be something the project can show or a number it has measured. Take numbers from `LEVELS.md`, test output or the running product, and state the conditions they were measured under.
- Never invent users, quotes, results, awards, partners or figures. Never present planned work as done.
- State known limits plainly. A limit the audience finds out for themselves costs more than one that was stated.
- A demo script uses only features that were run and seen working during this session.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Stated.** One sentence says what it is, who it is for and why it matters. A path through the product shows it working.
2. **Shown.** A demo script that works every time, with the exact steps and data. Screens or a recording to fall back on. A clear line from problem to solution to proof. The first screen of the README or landing page says the same thing as the talk.
3. **Convincing.** Built for the named audience and scored against their criteria, point by point. Evidence behind every claim. Prepared answers to the hardest likely questions. A plan for when the demo fails. Timed to fit the slot with room to spare.
4. **Rehearsed.** Run in front of people at least twice, timed, and changed in response. All materials finished and telling one consistent story: talk, deck, summary page, recording. Setup tested in conditions like the real ones.
5. **Campaign.** Materials for several audiences and channels, a release plan, and follow-up after the event. Only choose this for a public launch.

## Models

Story, structure, judgement and review run on Opus only. Drafting runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Executors draft from an outline and sources. They never add a claim, a number or a feature that is not in the sources.

## Step 0: Audience context

1. Look first. Read the README, any brief or rubric in the repository, and `LEVELS.md`: the idea blueprint, the levels reached, measured numbers and known gaps are the raw material.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Audience**: judges / teachers / investors / employers / customers / the public.
   - **Their criteria**: a rubric or scoring sheet if one exists, or what they are known to care about.
   - **Format and length**: live demo, talk with slides, recorded video, written submission, and the time or word limit.
   - **What should happen after**: the decision or action wanted from the audience.

   Round two, only what still matters:
   - **Who presents**, how many, and how experienced.
   - **Conditions**: screen or projector, network, sound, whose machine, time to set up.
   - **The field**: what others will show, and what is expected or overdone.
   - **Weak spots**: what the user hopes nobody asks about.
   - **Deadline**: date of the event or submission, and time available to rehearse.

3. Record unknown answers as unknown and state the assumption used.
4. Print a short audience profile: who, their criteria, format, time limit, wanted outcome. Wait for the user to confirm or correct it.

## Step 1: Audit (Opus)

1. Find the real strengths. From the product and the record, list what is true and distinctive: what it does that the obvious version would not, what was measured, what was hard and solved. Mark each with its evidence.
2. Run the product through the main path and confirm what works. Anything that fails or is fragile is kept out of the demo and noted.
3. Score against the criteria. For each criterion the audience uses, record what the project can show for it: strong evidence, some, or none.
4. Review existing materials against the level: is the one sentence clear, does the demo follow a story, does every claim have proof, do the materials agree with each other and with the product.
5. List the hardest questions this audience will ask, and whether a truthful, good answer exists.
6. State the level now, with evidence. Say what already lands and must be kept.
7. Rank the gaps: a claim without proof first, then a criterion with nothing shown for it, then a demo that can fail, then clarity, then polish.
8. Give two or three distinct directions for the story, each with its opening line, the three points it makes, what it leaves out, and which audience it suits. Mark the one you recommend and why.
9. Add optional ideas from one level above the target, labelled as stretch.
10. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

If a criterion cannot be met truthfully, say so. Do not paper over it. Offer what can be shown instead, or the handoff that would close the gap.

## Step 2: Execution plan (Opus)

After the user chooses a direction, do not draft directly.

1. Write the spine first, on Opus: the one sentence, the story in five to seven beats, the claim and evidence for each beat, and the time each gets.
2. Split the materials into sub-plans, one per deliverable or section: demo script with fallback, talk track, slide content, one-page summary, question and answer sheet, README opening, recording script. Include only what the format needs. No fixed count.
3. Each sub-plan states:
   - Goal, in one sentence, naming the audience.
   - The file to produce.
   - The outline, beat by beat, with the claim each part makes.
   - Sources for every fact and number.
   - Limits: length, time, tone, terms to use.
   - Done check: fits the limit, every claim traceable to a source, matches the spine.
   - Dependencies, and Model with a one-line reason.
4. Assign the model by this rule:
   - Haiku by default: slide text from a full outline, captions, formatting, summary pages, checklists, setup notes.
   - Sonnet when needed: the talk track, answers to hard questions, the README opening, any narrative writing.
5. Mark what can run in parallel. Most can, once the spine is fixed.

## Step 3: Delegation gate

1. Show a table: number, deliverable, model, parallel or sequential.
2. Print: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. List every claim the materials will make, each with its source, and ask the user to strike any they do not want made.
4. Ask with AskUserQuestion: **Delegate as planned (Recommended)** / **Haiku only** (name what is at risk) / **Sonnet for all** / **No delegation** (warn that everything runs on the session's current model, which is Opus unless the skill said otherwise at the start).
5. Do not start until the user answers.

## Step 4: Execute

- Before each spawn, print one line: `Sub-plan 3 → Haiku: <deliverable>`.
- Each executor starts with no memory of this conversation. Pass it the sub-plan, the spine, the audience profile and the Honesty rules.
- Executors write plainly, in the audience's terms, without selling language. A fact they cannot trace to a source comes back as a question, not as text.

## Step 5: Review (Opus)

1. Check every claim in every deliverable against its source. Remove or correct any that does not hold.
2. Check that all materials tell the same story and match the product.
3. Run the demo script from a clean start, exactly as written, and time it. Run the fallback too.
4. Read the talk track at speaking pace against the time limit.
5. Score the result against the audience's criteria again and report the level reached, what moved, and which criteria still have nothing behind them.
6. For level 4, give the user a rehearsal sheet: what to time, what to watch for, what to ask the listeners. Record what they report back. Never invent rehearsal results.

One corrective round, assigned the same way, then report the remainder. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** Read `LEVELS.md` at the start: it is the main source of evidence. At the end, update its pitch section with: the audience profile, the chosen story, target and reached level, criteria with no evidence, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md` and update only this skill's row. Keep the format exact.

```
<!-- levels
pitch: 2/3 gaps=3
-->
```

**Handoffs from this skill.** The demo path breaks or confuses: `ux-level` or `backend-level`. The product looks weaker than it is: `design-level`. A claim needs a number nobody has measured: `perf-level` or `test-level`. The product must run at the venue: `ship-level`. Written material beyond the pitch is needed: `docs-level`. Nothing distinctive can be found to say: `idea-level`, with the product as the seed.

**Handoffs into this skill.** Use the context passed in, skip questions the shared record answers, and report back to the calling skill.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

No claim without a source. No number without its conditions. Nothing invented. Nothing planned presented as done. No demo step that was not run and seen working. Limits stated, not hidden. Fits the time with room to spare.

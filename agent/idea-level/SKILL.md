---
name: idea-level
description: Brainstorm project ideas to a chosen depth on a 5-level scale, from a raw list to a build-ready blueprint. Asks for constraints first, generates and challenges ideas on Opus, then delegates research and write-ups to Haiku or Sonnet. Use when the user runs /idea-level or asks to brainstorm, find or develop project ideas.
summary: Find or sharpen a project idea, up to a build-ready blueprint
argument-hint: "[level 1-5] [ideas|develop] [topic or seed idea]"
model: inherit
---

# Idea level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `ideas` (generate, challenge and shortlist only) or `develop` (shortlist, then delegated deepening of the ideas the user picks). Default `ideas`.
- **TOPIC**: everything else. A domain, a problem, or a seed idea to push further. May be empty.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the idea lead. Work to the LEVEL. The levels describe how far an idea is developed, not what kind of project it is. Do not steer toward a domain, stack or business model the user did not ask for.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Spark.** A wide list of distinct ideas, one line each. Real spread: different users, problems and forms, not variations of one idea.
2. **Shaped.** Each idea has a named user, the problem in that user's words, what the thing does, and the one reason it is not the obvious version.
3. **Tested.** Each idea is scored against the user's own criteria, with its biggest risk, its closest existing alternative and why someone would still choose it. Weak ideas are cut, with the reason.
4. **Validated.** Claims are checked, not assumed: what already exists, who has tried and what happened, whether the hard part is technically possible with the user's means. The smallest version worth building is defined, with what it leaves out.
5. **Blueprint.** A build-ready brief for one idea: scope of the first version, main parts, data it needs, order of work, the first three milestones, and the test that tells the user to continue or stop. Only choose this for an idea the user intends to build.

## Models

Idea generation, challenge, scoring and final judgement run on Opus only. Research and write-ups run on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Executors gather and report. They do not judge, rank, cut or invent ideas.

## Step 0: Context

Before generating anything, establish what a good idea means for this user.

1. Look first. If the session is inside a project, read its README, product notes and recent work. Use the TOPIC. Note what they already answer.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Purpose**: learning / portfolio / competition or deadline / product for real users / income / personal use.
   - **Who it is for**: the user themselves / a specific group they know / a wide audience / not decided.
   - **Time**: a weekend / a few weeks / a few months / open-ended.
   - **Who builds it**: alone / a small team, and the skills on hand.

   Round two, only what still matters:
   - **Money and tools**: budget, hardware, services or data already available, anything that must be free.
   - **Must include**: a technology, theme, rule or requirement set by someone else (a brief, a course, a client).
   - **Must avoid**: domains, ideas already tried or rejected, anything overdone in their context.
   - **Taste**: an example of a project they admire and one they find dull, and why.
   - **Ambition**: safe and finishable, or risky and impressive.

3. If the user does not know an answer, record it as open, state the assumption you will use, and say so in the output.
4. Turn the answers into three to five scoring criteria in the user's terms, with weights. Print the criteria and a short constraint profile, and wait for the user to confirm or correct them.

Never propose an idea the constraints rule out. If the best idea needs a constraint lifted, offer it separately, labelled, with what it would cost.

## Step 1: Generate and challenge (Opus)

1. Generate wide before judging. Use several distinct angles, and say which angle produced each idea: a problem the user's own group has, an existing thing made for a different user, two unrelated fields joined, a constraint turned into the feature, an old idea made possible by something new, the opposite of the common approach, something small done unusually well.
2. Remove duplicates and near-duplicates. Remove the first ideas anyone would think of, unless one has a real twist. Say how many were generated and how many were kept.
3. Develop the kept ideas to the target LEVEL, up to level 3 in this step. Levels 4 and 5 need the delegated work in Step 2.
4. Attack each idea: the strongest reason it fails, who would not care, what makes it harder than it looks. Keep ideas that survive, and say plainly which ones do not.
5. Present a shortlist ranked by the confirmed criteria, with the score per criterion. Mark the one you recommend and why. Include one outlier: the riskiest idea worth considering, labelled as such.
6. Offer two or three directions to go next: go deeper on chosen ideas, combine two, generate more in the angle that worked best, or change a constraint.
7. Stop and wait for the user's choices. In `ideas` MODE, write the record and the levels row (see Connections), then end here.

Challenge the user's picks when the evidence is against them: say so plainly, give the reason and the alternative, then follow their final call.

## Step 2: Development plan (Opus)

In `develop` MODE, after the user picks ideas, do not research directly.

1. Split the deepening work into sub-plans that can each be done and checked alone. There is no fixed count: let the number of chosen ideas and the target LEVEL set it. One idea at level 4 may need three or four, several ideas at level 5 may need many more. Do not pad, and do not merge unrelated questions.
2. Each sub-plan states:
   - Question to answer, in one sentence.
   - Which idea it serves.
   - Where to look and what to collect, with the exact output format (for example: up to eight existing products, each with name, link, what it does, price, and what it lacks).
   - Done check: what a complete answer contains.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: finding existing products, collecting facts and links, listing options, filling a given template, formatting.
   - Sonnet when needed: judging technical feasibility, reading and comparing long sources, drafting a first-version scope or architecture outline.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Mark which sub-plans can run in parallel and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, idea, question, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. Say whether the sub-plans search the web, and that the idea's description leaves the machine in those searches. If the user wants an idea kept private, run its sub-plans without web search and say what that leaves unchecked.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: do the work in the main session. Warn that this runs everything on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <question>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan, the idea and the constraint profile.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors cite a source for every factual claim and mark anything they could not confirm. If a sub-plan is unclear or blocked, the executor stops and reports back instead of guessing.

## Step 5: Synthesis (Opus)

After the sub-plans finish:

1. Check the findings. Discard claims with no source. Where two findings disagree, say so.
2. Re-score each idea against the confirmed criteria with the new evidence. Say what moved and why. An idea that research has weakened is reported as weakened, not defended.
3. Deliver each idea at the target LEVEL. At level 5, write the blueprint for the single idea the user chose.
4. If an answer is still missing, write one corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user.
5. End with a recommendation: build this, test this first, or drop it, and the single next action.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers instead of asking again. At the end, create or update it with: the constraint profile and scoring criteria, the chosen idea and its blueprint, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open gaps. Tools read it, so keep the format exact.

```
<!-- levels
idea: 3/4 gaps=5
-->
```

**Handoffs from this skill.**

- After a level 5 blueprint the user intends to build: write the blueprint and the constraint profile to the shared record, then say that `levels new build` plans the first version from it, and give the command. Do not start it from here. `backend-level` and `design-level` plan from the blueprint when there is no code yet, so there is no audit of existing code.
- If the idea is only an interface or only a service: offer `design-level` or `backend-level` alone instead.

**Handoffs into this skill.** When another skill calls this one with a seed (for example a product with no clear concept), treat the seed as the TOPIC, skip the Step 0 questions the shared record answers, and return the result to the calling skill instead of offering a further handoff.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

No idea the constraints rule out. No claim about what exists, what is possible or what people want presented as fact without a source or a label saying it is an assumption. No padding the list to look thorough. Ideas that fail are named as failing.

---
name: premise-lock
description: Use when a wrong premise would be expensive — starting design or debug work, or the moment the user restates a goal, says "that's wrong", "you keep missing the point", "wrong layer", or asks to challenge assumptions. Also fires when a check passes suspiciously or a measurement contradicts a prediction. Forces a numbered VERIFIED/ASSUMED premise block, one root cause at a file:line, and the cheapest falsifying test, before any build. Gives the user a one-word rejection vocabulary so "that's wrong" never has to carry the whole signal. Also invocable by the user directly, when they see the behavior before the agent does. Runs a one-question-at-a-time interview, records open questions to .context/, and stamps docs/STATE.md. Composes grill-with-docs, ascii-design, 3d-first-principles, simple-english, audit, decomplexify, and zoom-out; escalates to audit-against for expensive builds.
---
# Premise lock

Two failures this prevents. The user says "that's wrong" and it does not say *what* is wrong. The user does not see the error until the work is spent.

Both have one cause. Nothing concrete is on screen to point at.

So: **keep a numbered, falsifiable premise block on screen at all times.** Then rejection costs one word.

## Routing

Write `TRIGGER: <event> -> <doc>`, then Read that doc as the next tool call.


| The moment you...                                                                                     | Read                                                                       |
| ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| start design or debug work, or the user restates a goal, names a shipped title, or says `wrong layer` | `references/PREMISE.md`                                                    |
| write a check that passes, read a probe's output file, or see a measurement contradict a prediction   | `references/EVIDENCE.md`                                                   |
| hit a fork the code cannot resolve, or the user invokes this skill on you mid-task                    | `references/GRILL.md`                                                      |
| hear a complaint about size, position, light, or things vanishing                                     | `3d-first-principles` diagnosis table, then `references/PREMISE.md` (PM10) |
| are about to build while item 4 is `ASSUMED`                                                          | `references/PREMISE.md` (PM7, PM8)                                         |


## Entry points

Two ways in. They start at different places.


| Entry                   | Signal                                                  | First move                                                                 |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------- |
| **You detect it**       | You are about to design, or the user restated a goal    | Post the block. Start at item 1.                                           |
| **The user detects it** | `/premise-lock`, "you're doing it again", `wrong layer` | Do NOT restart. Name the layer you were on, re-post from item 4. See GR10. |


The second entry means the user saw the compensator chain from outside and you did not see it from inside. The measurements already taken stay good. Only the CAUSE line was wrong.

If the user says they do not know this area, run `zoom-out` before writing item 2 (GR11).

## The block

Post before any build. Re-post whenever it changes.

```
┌─────────────────────────────────────────────────────────────┐
│  1  PROBLEM    what is wrong, in your words, naming no fix  │
│  2  MECHANISM  the goal decoded to a mechanism, not a feel  │
│  3  LEDGER     every claim PASS/FAIL, VERIFIED or ASSUMED   │
│  4  CAUSE      one file:line, and the number it produces    │
│  5  TEST       the cheapest falsifier, with its runtime     │
└─────────────────────────────────────────────────────────────┘
```

Item 3 is a table, never prose. Two states only — there is no third.

```
 #  claim                              state       evidence
 1  backdrop cam divides by depth      VERIFIED    probe -> fov=100
 2  IsoCamera is orthographic          VERIFIED    probe -> ortho=True
 3  planets must not grow on approach  ASSUMED     designer intent, unconfirmed
```

## Iron rules

- Item 1 states the symptom in the user's words and names no fix (a fix in the problem defends itself).
- User names a shipped title: state its ONE governing mechanism and confirm before designing (a title is a spec).
- User restates the same goal a 2nd time: the mechanism is wrong, not the parameter — back up, do not tune (restatement is falsification).
- Item 4 is one `file:line` plus one number, or it is a symptom (a symptom has no line).
- `VERIFIED` needs a command and its result line in the same turn; everything else is `ASSUMED` (a remembered result is a guess).
- Run item 5 before building, never after (a 2-minute flip beats a 1-week design).
- Ask with `AskUserQuestion`, one fork per call, recommended option first (a prose question gets no answer).
- Every unresolved fork goes to `## Open questions` in `.context/CONTEXT-<SLUG>.md`, naming the work it blocks (an unwritten fork returns as rework).
- Stamp `docs/STATE.md` at segment end with the locked premise and the open-question count (the next session starts blind otherwise).

## Output register

Every message that is not a graphic follows ASD-STE100, per the `simple-english` skill. Do not restate its rules here — read that skill.

Premise-lock adds three:

- Answer in lists, tables, and labelled breakdowns. Paragraphs hide the item the user needs to reject.
- Number anything the user can point at. `wrong layer` and `3` both have to have a target.
- Give the number, never the adjective. An adjective cannot be falsified.

Self-check before sending: longest three sentences under 20 words procedural or 25 descriptive; no *should / would / may / might / could*; every `if` at the start of its sentence.

## The user's rejection vocabulary

One word. That is the whole cost.


| Word          | Meaning                                  | What happens next                                |
| ------------- | ---------------------------------------- | ------------------------------------------------ |
| `go`          | Premise accepted                         | Build it.                                        |
| `<number>`    | That numbered item is false              | Fix that item, re-post the block.                |
| `wrong layer` | You are fixing a symptom                 | Back up one level of cause, re-post from item 4. |
| `wrong goal`  | Your restatement of my intent is off     | Re-post items 1-2 only. Ask nothing else.        |
| `unverified`  | You asserted something you did not check | Go check it, return with the command output.     |
| `too big`     | The test or build costs too much         | Find a cheaper falsifier, re-post item 5.        |


Read `wrong layer` as falsification, not clarification. It means stop refining and back up.

```
     post block
         |
         v
   user says one word
         |
   +-----+-----+-----------+
   |           |           |
   v           v           v
  go       <number>   wrong layer
   |           |           |
 build    fix item     back up
          re-post      re-post
```

The block is stable when it survives one round with no correction. Only then does work start.

## Composed skills

Always on, every message in the segment:


| Skill                   | What it governs here                                                                                                                                                                                                                                                                                                                         |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `simple-english`        | Register. Short active sentences, one idea each, present tense. No *should / would / may / might / could*.                                                                                                                                                                                                                                   |
| `3d-first-principles`   | Two jobs. Its diagnosis table resolves item 2 for any space/size/light complaint — read it BEFORE designing (PM10). Its contract shapes every explanation: E-BUILD, E-NUMBERS, E-BREAKS, E-JOB, E-DRAW. Cite principles by ID: `P-DIVIDE`, `P-ORIGIN`, `P-RECIPE`, `P-DOT`, `P-FLATTEN`, `P-POINTS`.                                         |
| `game-first-principles` | Two jobs. Its symptom table resolves item 2 for any "boring / nothing happens / best move is nothing" complaint — read it BEFORE designing. Its contract shapes every explanation: E-BUILD, E-ONEPICTURE, E-BREAKS, E-NUMBERS, E-JOB, E-DRAW. Cite principles by ID: `P-CHOICE`, `P-LOOP`, `P-UNCERTAIN`, `P-LEGIBLE`, `P-OWN`, `P-ECONOMY`. |
| `ascii-design`          | Every diagram. Tier B, one cell one column. Pad with a script, never by eye.                                                                                                                                                                                                                                                                 |
| `audit`                 | Shape of item 3. PASS/FAIL table with an evidence column.                                                                                                                                                                                                                                                                                    |
| `decomplexify`          | Criteria source for items 1-2 when the premise is about design, not a defect.                                                                                                                                                                                                                                                                |
| `grill-with-docs`       | The interview engine. One question per message, each carrying your recommended answer. See `references/GRILL.md`.                                                                                                                                                                                                                            |
| `zoom-out`              | Run before item 2 when the user says they do not know the area. User-invocable only.                                                                                                                                                                                                                                                         |


E-NUMBERS is load-bearing. An adjective cannot be falsified. A number can.

On demand, before a rewrite, a delete, or a change to a shared mechanism: `audit-against decomplexify <target>`. It fans out a council, so gate it on stakes, never run it per turn.

`ponytail` is already active every turn. Its first rung — does this need to exist at all? — is folded into PM7.

## Hard stops

- NEVER build while item 4 is `ASSUMED` -&gt; write `premise unlocked`, name what is missing, stop.
- NEVER add a layer that compensates for behavior not traced to a `file:line` -&gt; trace it, or delete the compensated thing.
- NEVER write `VERIFIED` from memory -&gt; re-run the command, paste the result line.
- NEVER ask a fork in prose -&gt; use `AskUserQuestion`, one fork per call.
- NEVER ask what the code can answer -&gt; Grep or Read it, then ask only the intent question.
- NEVER end the segment without stamping `docs/STATE.md` -&gt; write the premise, the cause, and the open-question count.

## Exit

The segment ends when the user says `stop premise-lock`, `normal mode`, or the premise is locked and the build is done. Say which one ended it.

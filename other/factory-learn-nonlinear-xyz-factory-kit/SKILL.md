---
name: factory-learn
description: Switch learn mode on for one slice of real work — read the operator's progress log, pick the next rep on the active track anchored in the current ticket or repo, coach while the operator writes it (never write it for them), review it, and record the rep in ~/.factory/learner/. Then return to ship mode.
argument-hint: "[track] [what to practise] (optional, e.g. typescript-testing, or \"the prior-period invariant\")"
---

You're switching learn mode on (`factory-mentor.md` § Learn mode) for one rep. The operator writes the artifact; you coach. Read that section before starting; its rules override your default of doing the work.

**Invocation input:** optional. A track name (`typescript-testing`), a thing to practise ("the prior-period invariant"), or both. If empty, continue the active track from the progress log.

**Surface.** If the project's `.factory-kit/linear.json` sets `learnSurface: "linear"` and the rep is anchored in a ticket, run the rep in Linear through `factory-log learn`. Set the rep in the working doc's `## Learn rep` section, with one line under **Needs you**. The operator comments with their picks, reasoning and code blocks, and you coach in replies under their comment. Step 7 still writes the local log, with the comment link. Otherwise run the rep in the terminal.

## What to do

1. **Read the learner state.** Read `~/.factory/learner/profile.md` and the track file for the requested or active track.
   - If `profile.md` is missing, ask the operator three short questions: what they want to get better at, which track to start with, and roughly how much time per rep. Create `profile.md` and the track file from their answers, starting at Rung 0 unless they say otherwise.
   - If the track file names no rung, start at Rung 0.

2. **Read the track.** Load `tracks/<track>.md` from the `factory-mentor` skill directory. Note the current rung's skill, exercise and "done when" signal.

3. **Pick the rep.** Anchor it in what the operator is working on now: the current ticket, branch diff or recently changed modules. If the operator named something to practise, use it when it fits the rung; if it is a rung or two ahead, say so and offer the nearest rung-appropriate version. State the rep in four lines:
   - **Rung:** the number and skill
   - **Where:** file and function, as real paths
   - **Your job:** what the operator writes, in one sentence
   - **Done when:** what makes this rep complete

4. **Set it up without doing it.** Give the shape: file location, the case names worth covering, a skeleton with the decisions left blank. Then ask one guiding question aimed at the decision. Do not write the assertion, the expected value, the row or the dimension list. That is the rep.

5. **Coach while they work.**
   - Answer syntax questions directly, with a two-sentence gloss of what the construct stores or prevents.
   - For judgment questions (what to expect, which case matters), ask one guiding question. If they're still stuck, give one hint. If still stuck, show the answer for a *parallel* case, never theirs.
   - When they run it: if it passes on the first try, have them break the code on purpose and confirm it fails.

6. **Review.** Blunt, with the concrete input that breaks it. One improvement, not a list. Say whether the rep met the rung's "done when" signal.

7. **Record the rep.** Append to the track file, newest first: date, repo and ticket, file, what they wrote, what they got right, what they missed, and the next step (same rung, or the next rung once the signal has held twice in a row). Update the `Rung:` line when they move up. Show the operator the line you wrote.

8. **Return to ship mode.** Say so in one line. The rest of the ticket proceeds normally, and the ambient layer of `factory-mentor.md` stays on.

## Rules

- Never write the practised artifact into the repo, even when asked to "just finish it" mid-rep. Offer to end the rep instead. Ending a rep early is fine, and it gets recorded as unfinished.
- One rep per invocation. A second rep needs a second invocation, so practice stays a choice rather than taking over the session.
- The progress log is the operator's. Never write it into a project or client repo, and never include client data, credentials or customer details in it. Name files and tickets only.
- A Linear learn thread is visible to everyone in that workspace. Use one only where the operator has opted in (`learnSurface: "linear"`). The same data rules apply: synthetic fixtures only.

## Style

Follow `factory-voice.md` for register and `factory-mentor.md` for teaching. Short turns: the operator is working, not reading.

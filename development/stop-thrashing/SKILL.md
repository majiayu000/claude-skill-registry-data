---
name: stop-thrashing
description: Detect when you're iterating without converging — a third attempt at the same failure — and force a zoom-out instead of a fourth variation. Use when consecutive fixes to the same failure haven't worked, when you're re-editing lines you already edited this task, when you catch yourself thinking "maybe it's this instead", or when each attempt is a guess rather than a deduction from new evidence.
---

# stop-thrashing

Thrashing is trying variations faster instead of understanding harder. Each iteration adds noise to the diff and anchors you deeper in a wrong frame. Weak recovery looks like a fourth plausible tweak; strong recovery looks like a revert, a new fact, and a single attempt derived from it.

1. **Keep an attempt ledger.** From the second attempt at the same failure, write it down in a scratch file: attempt number, the hypothesis in one sentence, the change made, the observed result. An attempt with no hypothesis line is a guess — it doesn't get made. Re-editing a line you already edited for this failure counts as a new attempt.
2. **Two failures is the alarm.** Attempt three may proceed only if it is derived from *new evidence* — a log you hadn't read, a value you hadn't inspected, a test you hadn't run — not from "maybe it's this instead" (see root-cause-debugging: one hypothesis, one test).
3. **On the alarm, stop editing and zoom out.** Re-read the original error top to bottom, re-read the failing code fresh, restate the problem in one sentence. Ask the frame-breaking questions in order: Is the file I'm editing the one that actually runs — add a marker and prove it (see environment-first)? Is my model of what this code does verified by a runtime observation, or assumed? Is the bug even in the code I've been looking at?
4. **Revert the debris before the next attempt.** Failed fixes stack: by attempt four the code carries three speculative changes interacting and you're debugging your attempts instead of the bug. `git diff` to see what has accumulated, `git checkout`/`git stash` back to the last known state, and reapply only what evidence supports.
5. **Change the method, not just the guess.** Add instrumentation and read actual runtime values; bisect the input or the commit history; write a minimal reproduction from scratch; explain the problem line by line to an imagined reviewer. Each of these produces a fact; another edit produces only another attempt.
6. **Set the budget at the alarm.** Decide, and write in the ledger, how many more evidence-backed attempts you will make before reporting. Autonomous retrying is right for mechanical obstacles (flaky network, transient lock); it's wrong when each retry is a rewrite. When the budget is spent, report the ledger as-is — what was tried, what each attempt showed, the current best hypothesis and what evidence would settle it — rather than burning the session on variation five (see workmanship).
7. **Notice the sunk-cost pull.** "I've come this far with approach A" is not evidence for approach A. Willingness to discard an hour of work when the frame is wrong is what separates converging from thrashing.

Test before every attempt: what *new* fact is this attempt based on, and where is it in the ledger? No new fact, no new attempt — go get the fact first.

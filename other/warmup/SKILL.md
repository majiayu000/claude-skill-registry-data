---
name: warmup
description: 'Record and run an account warm-up (rule 31) - the platform''s warm-up activities, each recorded once with log inspect in a headed session, turned into a flow and an XState machine, then run in one open browser with a stage log: `log <platform> warmup stages`. Use when the owner says warm up, warm-up, record the warm-up, or wants to watch it.'
---

# warmup

What the warm-up must do, requirement by requirement: [docs/specs/warmup.md](../../docs/specs/warmup.md).

## Hard boundaries

1. **Recorded, never written blind** (rule 29). `log <platform> warmup stages record` drives the
   inspect session headed, every step saved (snapshot, screenshot, HAR, rea),
   and builds each flow from that recording. `log <platform> warmup stages run` refuses an
   activity whose flow isn't recorded (`flowNotRecorded`).
2. **One browser** (rule 35). Record and run both open one session and do every
   activity inside it.
3. **Likes act on the platform** (rule 8): a like only runs with
   `--likes`, when the owner asks. Everything else reads. **A like passes on
   the platform's answer** (rule 73), not on the button the page shows after:
   the step waits for the like's mutation and passes only when it answers
   2xx with the reaction we sent saved (`expect.answers`, `answerIssue`). A
   step's answers are read from its own recording and kept as
   `exchanges.json`. Other steps get `expect.answers` the same way, written
   from that request's doc ("What it sent and what came back").
4. **Every step that makes a call is decided by its answer** (rule 73). The
   stage flows carry `answers` on each step whose recording shows a call
   that answers it, and the run fails the step with its code when the answer
   isn't right (`runFlowInSession`, `answersIssue`). Dwells and steps whose
   recording shows no call have nothing to read. A home check is skipped
   when Twenty has no home for the account. Each flow's doc shows what every
   step must answer, and recording a flow again keeps the checks
   (`keepAnswers`).
5. **Live and watched** (rule 26): run through Monitor; every step goes to the
   stage log as it happens.
6. **Stops on the wrong page.** Every step's landing page is checked
   (`pageProblem`): a checkpoint, a login wall or another section ends the
   activity (`blocked`), and the account's issue is written to Twenty.
7. **Scrolls like a hand** (`python/human/scrollMotion.py`, ported from the Robotic
   VSL repo): bell-curve wheel steps, overshoot and recoil, mid-pauses. No
   `scrollBy` or `scroll_into_view_if_needed` anywhere.

## The routine

```bash
log <platform> warmup stages plan                                        # the activity scripts, recorded or not
log <platform> warmup stages record --account <a> --now                  # one headed session: each script, then each flow
log <platform> warmup stages run --account <a> --now                     # watched run: the machine runs each flow in turn, 10 s apart
log <platform> warmup stages log --account <a> --follow                 # the stage log (the activity feed), live
```

`--gapSeconds` is the wait between activities: 10 by default, not minutes.
`--only <activity>,<activity>` limits it.

After recording, read each activity's steps with rea (rule 25) and rebuild the
platform's request docs before pushing. A record that fails part-way still
saves the activities that finished before it.

Facebook's warm-up activities, pages, checks and Reels: `skills/facebookWarmup/SKILL.md` (the facebookFlows guide).

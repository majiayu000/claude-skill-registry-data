---
name: eval-loop
description: Improves prompt, skill, or instruction text in scored rounds against locked eval cases, with a frozen grader hash, replicates, holdout cases, and a human read of raw transcripts before pass. Use when asked to "run the evals and fix the prompt", "make the bot pass its cases", "is the new prompt better", or "iterate on this SKILL.md until the evals pass". Not for test suites or a one-off eval run.
argument-hint: "[what changed] [round | baseline | pass]"
---

# Eval loop

Improve text that steers a model (a bot's system prompt, a `SKILL.md`, agent instructions) the way code is improved: a locked case set, a score per round, and a delta that means something. A grader change, a single run, or a tally shown as "pass" each break the comparison, so this skill refuses them.

## Inputs

- **The text under improvement**: the file or files the change edits. Everything else in the round is read-only.
- **Arguments**: a note of what changed, which goes in the round's `kind` cell; `baseline` forces a new baseline round; `pass` runs step 8 on the current best round; `round` runs the next fix round. With none, the report decides which round comes next.
- **Cases**: the project's eval cases, by default in the layout of [references/case-format.md](references/case-format.md) (a folder per case: `case.yaml`, `graders/*.md`); any layout the runner understands works. A **holdout** folder holds cases that are run and scored but never opened by whoever edits the text.
- **Project settings**: on every invocation, read `.claude/shipyard/eval-loop.md` in the project root if it exists. It names the runner command, the case and holdout folders, the judge for LLM graders, the real-surface command, and the caps: `replicates`, `wall clock`, `fix rounds`, and `max_cost_usd`. Its shape is in [references/overlay-example.md](references/overlay-example.md). Without a runner command, ask for one; without `max_cost_usd`, refuse to open a round (step 1).

## Output

`.claude/shipyard/reports/eval-loop-<branch>.md` (`/` in the branch name becomes `-`), in the shape of [references/report-template.md](references/report-template.md): `Commit:` (the full HEAD sha), `Result: pass | not passed | stopped`, a round table (round, kind, grader hash, text hash, cases, replicates, suite pass rate, delta, cost), a per-case pass-rate matrix, the holdout check, the real-surface transcripts, and `Checked:` / `Not checked:` lines. Raw transcripts and scores stay on disk under `.claude/shipyard/eval-loop/<branch>/round-<n>/`; the report points at them.

## Rules

- **Compare only on the same grader hash.** The hash covers every grader file and the locked case list. Two rounds with different hashes are different tests; a delta between them is noise dressed as progress, so the report never prints one. Why: five grader edits mid-loop once turned 26/84 and 58/84 into numbers nobody could compare.
- **A grader or case edit opens a new baseline round**, which re-scores the previous best text under the new hash before any fix is tried. That gives the next delta a reference. Editing cases or graders is allowed; it is a baseline change, never a fix round.
- **At least 3 replicates per case** (`replicates`, default 3). Same text, same cases, two runs: four cases flipped. A case passes a round only when every replicate passes; the matrix shows `k/n`, never a single tick.
- **Mechanical graders first, LLM graders second.** Banned strings, repeated replies, language mirroring, length caps, and required exact strings (a fixed phone number or legal phrase, say) are cheap, deterministic, and decide the reply on their own; a reply that fails one isn't sent to the LLM judge. LLM graders run on one judge for the whole round, named in the settings.
- **The holdout folder stays unread.** The skill runs and scores it; nobody editing the text opens it, quotes it, or greps it for content. Before each round, the diff of the text under improvement is checked for strings from the holdout cases (user turns, required strings) and a match stops the round. Why: text tuned to the test passes the test and nothing else.
- **Failing cases first.** Order the round by the previous round's pass rate, ascending, so a round cut by the cost or wall-clock cap has already scored what matters.
- **Cost cap per round.** `max_cost_usd` is required. Pass it to the runner where the runner takes a cap; otherwise estimate `cases × replicates × cost per run` from the settings and refuse a round that exceeds it. A round stopped by the cap is reported as partial, never as a score.
- **Runs go in the background with a wall-clock cap** (`wall clock`, default 20 min a round). On timeout, stop the whole process tree, through the wrapper the settings name if they name one. A replicate that didn't finish scores `not run`, and a round with a `not run` can't be the best.
- **No pass on a tally.** `pass` needs a run on the real surface (the deployed bot, the installed skill, not the harness) and three raw transcripts shown to the human in full, who says pass (H7). Tone and safety are judged by a person reading replies, not by a count.
- **Fix rounds are capped** (`fix rounds`, default 5 per baseline). At the cap, report the trend and stop; the human decides whether to fix, re-plan, or stop.

## Steps

Steps are agent-owned unless marked.

```
- [ ] 1 Read settings; refuse without a cost cap
- [ ] 2 Holdout check on the diff
- [ ] 3 Open the round: hash and lock
- [ ] 4 Run replicates in the background
- [ ] 5 Score: mechanical, then LLM
- [ ] 6 Compare on the same hash
- [ ] 7 Fix round, or stop at the cap (gate)
- [ ] 8 Real surface and transcripts (gate)
- [ ] 9 Report
```

1. **Read settings.** Resolve the runner, case and holdout folders, judge, caps, and the text under improvement. No `max_cost_usd`: say which line is missing, write nothing, and stop. Read the existing report, if any: it says which round comes next and what the previous best is.
2. **Holdout check.** Collect the holdout cases' user turns and required strings with a script that prints only match counts, then check the diff of the text under improvement against them. Any match: **STOP — WAIT**; name the file and line in the report, write `Result: stopped`, and ask the human how it got there.
3. **Open the round.** Compute the grader hash and the text hash as [references/round-protocol.md](references/round-protocol.md) says, lock the case list (holdout included), and write `round-<n>/lock.json`. If the grader hash differs from the previous round's, this round is a **baseline** that re-scores the previous best text; the report says so in the round's `kind` column. With no shell to hash with, the round can't open: say so.
4. **Run replicates.** For each case, failing cases first, start the runner `replicates` times in the background with the wall-clock cap and the cost cap; collect each transcript under `round-<n>/runs/<case>/<r>.txt`. A holdout case's transcript is never opened; step 5 scores it by script and shows only the verdicts.
5. **Score.** Mechanical graders run as a script over every transcript (the script reads the grader files and the transcripts; you read its verdicts), then LLM graders over the survivors, with the judge the settings name (without one, a fresh subagent that sees only the grader text and the transcript). Write `round-<n>/scores.json`: per case, per replicate, each grader's verdict.
6. **Compare.** Against the latest round with the same grader hash only. Suite pass rate is cases with all replicates passing over cases locked; the delta is this round minus that round. A baseline round has no delta.
7. **Fix or stop.** Better and every case stable (no case with mixed replicates): go to step 8. Same or worse: edit the text under improvement (only that), name in the report which failing cases the edit targets, and open the next fix round at step 2. At the fix-round cap, **STOP — WAIT**: show the trend (the round table) and ask the human whether to fix once more, re-plan, or stop; write `Result: stopped`.
8. **Real surface and transcripts.** Run three cases through the real-surface command from the settings, picking the locked cases outside holdout that failed most in earlier rounds; save the raw transcripts and paste them into the report in full, not summarized. **HUMAN TRIGGER** (H7): the human reads the three transcripts and the pass table and says pass; until then, `Result: not passed`.
9. **Report** in the template's shape, with `Commit:` set to the current HEAD, each round's evidence paths, and `Checked:` / `Not checked:` lines naming the cases and surfaces this run did and didn't cover.

## Handoff

`next:` a pass goes to the verify live stage (live-verify) when the change also touches running code, else to review; `stopped` or a holdout match goes back to the human with the trend.

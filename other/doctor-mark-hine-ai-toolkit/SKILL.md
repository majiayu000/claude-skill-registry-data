---
name: doctor
description: "Scores recent Claude Code sessions and the global setup for wasted tool calls, test value, verbosity, procedure compliance and setup bloat, then writes a dated scorecard with the change since the last run and proposed diffs. Run it from the ai-toolkit checkout every fortnight or after a change to the rules. Never runs on its own."
argument-hint: "[days, default 14]"
disable-model-invocation: true
---

# Toolkit doctor: $ARGUMENTS

Measure how the last fortnight of sessions went, score it, compare it with the last scorecard and propose fixes. Apply nothing. The scorecard and its proposed diffs are the deliverable.

Transcripts and every report stay on this machine, under `~/.claude/health/`. Never upload a transcript or an excerpt of one, and never write a scorecard, a data file or the backlog into the repository, because this repository is public and the reports describe real work sessions.

## Preconditions
1. The working directory is the ai-toolkit checkout (`.claude-plugin/marketplace.json` has `"name": "ai-toolkit"`).
2. Take today's date from `date -u +%F`, never from memory. The window is the argument in days, or 14 when none is given.

## Procedure
1. **Collect.** Run `python3 tools/doctor.py --days <window> --out ~/.claude/health/data/<date>.json`. When a file for that date exists, add a `-run<n>` suffix to the data file and the scorecard so that neither overwrites the earlier run. If `sessions` is 0, report that there is nothing to score and stop.
2. **Compare.** Read the newest earlier file in `~/.claude/health/data/`. For every metric in `references/scorers.md`, compute the change. A metric that moved more than its noise band in the wrong direction is a regression.
3. **Sample.** Pick up to 12 sessions from the window: the 4 with the most tool errors, the 4 with the most tool calls and 4 at random. Use the session files under `~/.claude/projects`, skipping any project the collector skips.
4. **Judge.** Send the sample to `sonnet` subagents, 4 sessions each, with `references/scorers.md` as the rubric. Each subagent reads its transcripts with a script that prints only the assistant text and the tool calls, scores each session on the 4 judged rubrics, and returns one row per session with a score, a 1 to 3 sentence reason and a `file:line` citation. It edits nothing and quotes no more than 1 short line per citation. Re-open every citation for a score below 0.5 before it enters the scorecard, and drop a row whose citation does not show the claim.
5. **Score.** Compute each area score from the collector metrics and the judged rows with the formulas in `references/scorers.md`. The overall score is their weighted mean.
6. **Find causes.** For each regression and each area below 6, name the rule, skill, hook, memory or setting that most likely caused it, with the path. Say "cause unknown" when the evidence does not point at one.
7. **Write.** Copy `references/scorecard-template.md` to `~/.claude/health/<date>.md` and fill it. Give the scorecard table with the change since the last run, the top 3 findings and a "Proposed changes" section with one unified diff per source file under `src/`, `shared/` or the home settings. Move anything minor to `~/.claude/health/backlog.md`, and strike through a backlog line that the numbers show is fixed. Do not apply any diff. Under "Rules for the next audit", list the `file:line` of each rule that this run shows is routinely broken or has no measured effect, with the metric that shows it. The audit skill reads that list and reviews those rules against their sources.
8. **Report.** Give the overall score, the 3 findings, the regressions and the scorecard path. Ask which proposed changes to apply.

## Rules of the doctor
- Count with the collector. A number that the collector or a quoted command did not produce is Unverified.
- A proposed change must trace to a regression or to a judged row in this run. General good practice is not a reason.
- One fortnight is a small sample. Call a change a trend only when 2 runs in a row move the same way.
- When an experiment is running, such as a hook turned off, name it in the scorecard and compare only the metrics it could move.
- The reports name real projects and sessions. Keep them out of the repository, pull requests and any external service. A proposed diff that goes into a pull request carries the rule change and its metric, never a session ID or a project name.

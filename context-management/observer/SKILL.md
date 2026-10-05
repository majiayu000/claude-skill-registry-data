---
name: observer
description: Audit the setup as it is actually used — session transcripts, skill/agent/MCP invocation counts, session shape, round-trip waste — and report ranked system-level findings. Trigger on:- observer, audit my setup, session audit, where am I wasting time, what isn't being used, is my workflow working.
argument-hint: "[window, default 30d] [optional project dir to scope to]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
model: claude-sonnet-5
---

# Observer

`prune` audits the tooling **as written** — registry rows, line counts, `SKILL.md`
structure. Observer audits the same tooling **as used** — what actually fired, where
sessions stalled, what was paid for twice. Different input (transcripts, not files),
different artifact. Run it periodically, months apart, not per session.

## When to use this

- Periodic system checkup; nothing gates it.
- After a batch of skill changes, to see whether the new shape is being reached for.
- Skip if the last report is under ~6 weeks old, or the window covers fewer than ~20
  sessions — the findings will be noise.

## Procedure

1. **Fix the window and run the age guard.** Default 30 days. Before counting anything,
   record the creation/mtime of every subject you will report on:

   ```bash
   ls -la --time-style=long-iso /home/rahul/.claude/skills/ /home/rahul/.claude/agents/
   ```

   A zero over a window in which the subject did not exist is **not a finding**. Report
   it as `insufficient window — <subject> created <date>` and move on. (This guard exists
   because the 2026-08-02 hand-run of this audit reported "planit never fires, agents
   unused" against tooling created two days earlier.)

2. **Scope the corpus.** `/home/rahul/.claude/projects/*/*.jsonl` — one dir per project,
   one file per session. Count sessions and date-range them first; every later finding
   cites that denominator.

3. **Run the three lenses, and only these.** Each produces counts, not narrative.

   | Lens | Measure |
   |---|---|
   | **Inventory drift** | fires per skill / agent / MCP server vs. the `skills/README.md` registry |
   | **Session shape** | interruptions, compactions, `/clear` rate, opening-prompt shape, turns before first edit |
   | **Round-trip waste** | repeated identical read-only calls, permission prompts, independent calls issued serially |

   Working probes (verified 2026-08-30 — adjust if the transcript format moves):

   ```bash
   cd /home/rahul/.claude/projects
   # skill fires, model- and user-invoked
   grep -rho '"skill":"[a-z-]*"' --include='*.jsonl' . | sort | uniq -c | sort -rn
   grep -rho '<command-name>[^<]*'  --include='*.jsonl' . | sort | uniq -c | sort -rn
   # tool mix — Bash vs Read/Edit vs MCP vs agents
   grep -rho '"name":"[A-Za-z_]*","input"' --include='*.jsonl' . | sort | uniq -c | sort -rn
   # stalls
   grep -rc 'Request interrupted by user' --include='*.jsonl' . | grep -v ':0$'
   grep -rl 'isCompactSummary' --include='*.jsonl' . | wc -l
   ```

4. **Cross-reference the registry.** Every row in `skills/README.md` and every
   `agents/*.md` gets a fire count or an explicit `insufficient window`. A row with
   neither is an incomplete report.

5. **Rank by cost × confidence.** Cost is time or context actually burned (a compaction,
   a 40-times-repeated prompt), not aesthetic tidiness. Confidence is how directly the
   metric supports the claim. Drop anything you cannot state as a count.

6. **Write `docs/observations/<YYYY-MM-DD>.md`** — window, session count, the three lens
   tables, then ranked findings. Each finding: the claim, the count behind it, and a
   routed destination.

7. **Route, don't act.** Each finding names where it goes:
   - a skill should change → a line in `docs/notice.md`, or a file in
     `docs/skill-ideas/` for `/forge`
   - the registry is stale or a skill looks dead → hand to `/prune`
   - permission-prompt churn → hand to `/fewer-permission-prompts`, which already
     specialises in that one lens
   - `settings.json` / hooks → propose the edit, let the user apply it
   - nothing to do → say so and close it

## Constraints

- **Report only.** Never edit a `SKILL.md`, `settings.json`, the registry, or a
  transcript. Constitution hard rule 1 — the human walks every transition.
- **No finding without a count.** Name the metric, the window, and the denominator.
  "Workflow feels heavy" is not a finding.
- **The age guard is not optional**, and neither is its inverse: a *rise* over a window
  the subject only partly spans is equally meaningless.
- **A uniform result is a broken probe** until proven otherwise — all-zero fire counts
  mean the grep pattern moved with the transcript format, not that nothing ran.
- **Three lenses, no fourth.** If something interesting falls outside them, log it as a
  one-line aside, do not open a new investigation. The scope creep is the failure mode.
- **Don't reimplement neighbours.** Permission churn belongs to
  `/fewer-permission-prompts`; static registry health belongs to `/prune`.
- Transcripts contain the user's real work. Quote a prompt only where it is the evidence,
  and keep it to the shape (bare nudge, long paste), not the content.

## Done criteria

- Report written to `docs/observations/<YYYY-MM-DD>.md`, with window, session count and
  date range stated at the top.
- Every registry row and agent has a fire count or an explicit `insufficient window`.
- Every finding carries its count and a routed destination.
- Anything routed to `notice.md` or `docs/skill-ideas/` is actually written there.

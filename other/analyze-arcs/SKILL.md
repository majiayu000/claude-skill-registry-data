---
name: analyze-arcs
description: Measure the Claude Code pipeline sessions since a date — master transcripts, their subagents/*.jsonl, and the codex-challenge logs — and report the numbers plus the mechanical doctrine violations. Invoke on "analyze the sessions", "how did the last arcs go", "evaluate the pipeline", "/analyze-arcs <since-date>", or before any kit change that claims to fix a pipeline problem.
---

# Analyze arcs

The scripts are read-only. Times in the report are UTC; transcripts are under
`~/.claude/projects/<project>/<session>.jsonl` with subagent transcripts beside them in
`<session>/subagents/`. The master transcript is a partial record: owner↔subagent messages
and everything a subagent did live only in the subagent files, so never judge an agent from
the master's view of it.

## Procedure

1. **Version diff first.** `claude --version`
   against the stamp in the kit's `docs/references.md`; if they differ, read the changelog
   between them before blaming the doctrine for a harness change.
2. **Run the measurement** into the session scratchpad:
   ```
   python3 ~/.claude/skills/analyze-arcs/scripts/analyze.py --since YYYY-MM-DD --out <scratchpad>/arcs/report.md
   ```
   Per session: span, models, Claude Code version, peak context, subagent roster (type, pin, turns, minutes, KB,
   model actually seen), every `codex-challenge.sh` launch with its range, `--out`, run
   minutes and verdict size, every gate with how long it waited, pushes, killed background
   tasks. Then the **flags** — mechanical checks only:
   - unpinned `Agent` spawn, or a pin off the doctrine tier (plan-reviewer unpinned — it inherits the session's model,
     team-reviewer `opus`, executors, fixers and triage `sonnet` unless the plan marks a step Opus or a same-mechanism fixer round calls for it) with whether the prompt states a reason
   - named spawn (delivery rerouted to the mailbox)
   - `codex-challenge.sh` run in the foreground; `--out` outside the session scratchpad
   - master `Edit`/`Write` on a product file after `feature-workflow` loaded — or a Bash command that
     changed one, read from the harness's own changed-file record (`bashEditDiff.changedFiles` on the
     tool result; 2.1.269+, never parsed from the command text). The auto-mode prompt steers edits
     through Bash, so the Edit/Write check alone is blind; sessions from before 2.1.269 say "Bash
     writes: not recorded". Two gaps in the record: a command that exits non-zero gets no record even
     when it changed files, and a `run_in_background` command gets none either. Plan files, `docs/prompts/`,
     `docs/reviews/`, `docs/todos/`, handoff docs, the TODO/tech-debt index, `/tmp/` and build artifacts
     are not product files
   - master `Read` of a product file, or a Bash read command (`cat`/`head`/`tail`/`less`/`sed`/`grep`/`rg`
     parsed from the command text — the harness records writes only, never reads) inside a plan-mode span
     (an `EnterPlanMode` whose call was not denied, to the `ExitPlanMode` that was itself approved — checked
     only in the `tool_result` linked to that `ExitPlanMode` call by `tool_use_id`, so the approval string
     appearing elsewhere, e.g. in a Read of this script's own source, is not a false close; a rejected exit
     does not end the span either). When no approved exit ever follows — including a Shift+Tab exit, which
     leaves no `ExitPlanMode` call at all — the span ends at the first proven-successful product-file edit
     after it (an Edit/Write/MultiEdit/NotebookEdit whose own `tool_result` was not an error, or a Bash write
     the harness's `bashEditDiff.changedFiles` record shows; the harness blocks product edits while still in
     plan mode, so one proves plan mode had already ended), or end of transcript if there's no such edit
     either. The command text goes through a quote-aware tokenizer, not a regex: segments split on unquoted
     `&&`/`||`/`|`/`;`/newline, operands come from `shlex`, each option's value is consumed with it (`head -n
     5 f` reads `f` only), redirections are not operands (`2>/dev/null`; a `<f` redirect *is* a read), and for
     `grep`/`rg`/`sed` the first operand is the pattern or script unless `-e`/`-f`/`--regexp=`/`--expression=`
     already gave it. A bare recursive search with no path (`rg needle`) reads `.`. Same exemptions as the
     Edit/Write check. Gaps: a read inside a heredoc, a `python3 -` script, or behind an unexpanded variable
     (`cat $f`) is invisible — nothing tokenizes those; a segment with unbalanced quotes claims nothing; a
     `cd dir && cat f` relative path is reported as written, not resolved against the `cd`; a session that
     *entered* plan mode via Shift+Tab has no `EnterPlanMode` call and is not windowed at all; `product_file()`
     normalizes the path, then exempts any path containing `/.claude`, so a product repo's own `.claude/`
     files are invisible to this flag
   - `ExitPlanMode` or `AskUserQuestion` that waited more than an hour, or was never answered
   - `feature-workflow` loaded with no one-shot/pipeline call line before it; product edits with no call line at all
   - subagents that died on an API error before doing work; subagents that hit their turn cap

   `--semantic` upgrades the reason-stated and one-shot/pipeline-call-line checks above to a typed
   judgment from the local-only semantic layer (`jev.py`/`semantic.py`), expected at
   `~/.claude/local/analyze-arcs/`. Without it, the command's output and network use are unchanged.
3. **Read the timelines at the flagged times.** A flag is a place to look, not a verdict:
   ```
   python3 ~/.claude/skills/analyze-arcs/scripts/timeline.py <session>.jsonl <scratchpad>/arcs/<name>.txt
   ```
   works on a master or a subagent file; then `awk`/`grep` the time window. Read the subagent
   transcript for any spawn whose roster row looks off (long, huge, capped, wrong model).
4. **The judgment findings the script cannot make** — check them by hand every time:
   a verification step that proved only the negative path (curl, unit suites) before a deploy;
   a review escape (what codex rounds missed and why); whether a long gate wait was a legitimate
   taste gate or a delegated approval the master should not have blocked on; whether an off-tier pin's
   stated reason holds; whether a relaunch or respawn was warranted by the agent's own timestamps.
5. **Report with the numbers**, held vs failed, ranked by cost. Every doctrine change proposed
   from it goes as before/after text through "would removing this line cause mistakes?", and the
   measured evidence goes into a memory note so the next run has a baseline.

## Limits

`--min-kb 150` skips small sessions unless they spawned subagents; lower it to see one-shots.
Codex run minutes come from the log file's birth and modification times, so a run whose
`--out` was reused or deleted reads `?`. Spawn rows are matched to subagent transcripts by
order of start time; a spawn that died before writing a transcript shifts the rows after it —
compare the `model seen` column with the pin when that happens.

Summing tokens by hand: Claude Code writes one JSONL line per content block, each repeating the
response's usage, so count each message id once. In subagent transcripts `output_tokens` holds a
stream-start value, not the final count: turns, context size and cache reads are reliable there,
output is not.

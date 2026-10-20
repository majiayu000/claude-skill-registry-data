---
name: eta
description: Report the ETA of what you are currently doing, in one fixed format (progress bar, ETA clock time, per-step table), using timings learned from past commands in this repo. Use when the user types /eta or asks "how long", "eta?", "where are we", "when will it be done".
---

# /eta

Output is rendered by `eta.py`, never by you. Do not compute percentages, durations or clock times yourself, and do not rewrite the block.

## Steps

1. List your steps for the current task: what is done, what is running, what is left.
2. Run `python3 <skill dir>/eta.py keys --cwd "$PWD"` to see the commands this repo has timing history for (`key  n  p50  p90`).
3. Run the renderer, one `--step 'status|name|est|elapsed|lane'` per step:

   ```
   python3 <skill dir>/eta.py render --cwd "$PWD" \
     --step 'done|edit parser|40' \
     --step 'running|run tests|@go test|20' \
     --step 'todo|fix failures|1-2m' \
     --step 'todo|commit|30'
   ```

   - `status`: `done`, `running` or `todo`.
   - `est`:
     - `@<key>`: a key from step 2, copied exactly. Use it whenever the step is that command.
     - `90`, `90s`, `2m`, `1-2m`: your own guess, only for steps with no history.
     - `?` or empty: unknowable.
     - For `done`: `est>actual` (e.g. `10-15m>11m`, `@make ci-fast>140`) fills `est`, `actual` and the `diff` column (absolute and %). A lone value is just the actual time; empty if unknown.
   - `elapsed`: seconds the `running` step has already taken, if known. Shown in `actual`.
   - `lane` (5th field, optional): name of a parallel track. Steps of one lane run in sequence, lanes run in parallel, the slowest decides. Steps with no lane run in sequence around them (e.g. an integration after two parallel branches). Steps that are both `running` are parallel even without a lane. Otherwise everything is sequential.
   - `--waiting '<what>'` when blocked on the user or on an external job; the ETA then prints as unknown.
4. Reply with the renderer's output verbatim and nothing else. Add no intro, no summary, no caveats.

If the script is missing `python3`, try `python` then `py -3`. If it exits with an error, show the error; do not fall back to a hand-written estimate.

## Notes

- A key with fewer than 3 samples gives `ETA unknown`, by design: say unknown rather than invent a number.
- Timings are collected by the plugin's hooks (`hooks/hooks.json`, `eta.py hook`) into `~/.claude/eta/log.jsonl`, per repo, commands of 2 s and more only. Worktrees share their main repo's stats. `ETA_HOME` moves the data directory.
- Used without the plugin (skill copied on its own), nothing records timings: add the same five hook entries (`PreToolUse`, `PostToolUse`, `PostToolUseFailure` on `Bash`, plus `UserPromptSubmit` and `Stop`) to `settings.json`, or `/eta` only shows your own estimates.
- Needs Python 3 (stdlib only); works on macOS, Linux and Windows.
- Hooks skip `run_in_background` commands. To learn from a long build you start in the background, launch it as `python3 <skill dir>/eta.py run -- <command>` so its duration is logged.

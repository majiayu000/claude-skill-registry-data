---
name: todoScore
description: "Turn the prompt scores of Prompt TODO on or off — the ` (N/5)` Claude appends to an item line when it rewrites the item to its ideal prompt, rating how close the original prompt was. Writes `promptScores` in .claude/prompt-todo/config.json and re-renders .claude/prompt-todo/RULES.md; touches no todo file. Existing scores stay either way. Runs only when the user invokes it: '/todoScore', '/todoScore on', '/todoScore off'."
argument-hint: "[on|off]"
disable-model-invocation: true
allowed-tools: Read, Edit, AskUserQuestion, Bash(bash .claude/prompt-todo/bin/py.sh:*)
---

# /todoScore

The **Prompt scores** rule in `.claude/prompt-todo/RULES.md` makes every rewrite of an item
append ` (N/5)` to its line: 5 when the original prompt already was the ideal one, 1 when the
result came from the corrections. It is the progress log of prompt writing. A project that
does not want numbers in its todo files flips the rule here: `off` and no score is written,
`on` and it starts again. Nothing already written is touched.

```
/todoScore          # show the current state, then ask on / off / keep
/todoScore on       # scores on (the default after install.sh)
/todoScore off      # scores off
```

## What Claude does

1. **Read the config** — `.claude/prompt-todo/config.json` (`Read` tool). The key is
   `promptScores`, `"on"` or `"off"`; a missing key means `on`. If the file is missing, say
   `install.sh` has not been run here and stop.

2. **Resolve the target state.** `on` / `off` from the argument. With no argument, print the
   current state in one line and ask with `AskUserQuestion` — options *On*, *Off*, *Keep* —
   and stop on *Keep*. Any other argument → print the three forms above and stop.

3. **Already there?** If the target equals the current state, say so in one line
   (`Prompt scores are already off`) and stop — no edit, no render.

4. **Write** `"promptScores": "<state>"` with the `Edit` tool (add the key before the closing
   brace when it is missing), never the shell. Then re-render:
   `bash .claude/prompt-todo/bin/py.sh render_rules.py`. Show its one-line output. If it fails,
   show the error and revert the edit.

5. **Reply** in two lines: the new state, and what changes from now on —
   `off`: rewrites append no ` (N/5)`, `/todoIdealPrompt` prints no score and writes none,
   existing scores stay, `/todoIdealPrompt #N --score` still scores one item on request; `on`:
   every rewrite scores the original prompt again and a bare `/todoIdealPrompt #N` writes the
   score to the item line, nothing is scored retroactively.

## Notes

- The state lives in the committed config, so it is the team's setting, not a personal one.
- Never edits a todo file — `off` is not "strip the scores"; if the user wants that, it is a
  separate, explicit request.

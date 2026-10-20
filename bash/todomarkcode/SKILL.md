---
name: todoMarkCode
description: "Turn the code markers of Prompt TODO on or off — the `[<name>#N]` tag Claude appends to a comment at each change site so grep leads from code back to the todo item. Writes `codeMarkers` in .claude/prompt-todo/config.json and re-renders .claude/prompt-todo/RULES.md; touches no code and no todo file. Existing markers stay either way. Runs only when the user invokes it: '/todoMarkCode', '/todoMarkCode on', '/todoMarkCode off'."
argument-hint: "[on|off]"
disable-model-invocation: true
allowed-tools: Read, Edit, AskUserQuestion, Bash(bash .claude/prompt-todo/bin/py.sh:*)
---

# /todoMarkCode

The **Code markers** rule in `.claude/prompt-todo/RULES.md` makes every change for item `#N`
carry `[<name>#N]` in a comment at the change site. Some projects do not want that trace in
the code — a shared library, a repo with a comment policy, a team that keeps the history in
git only. This skill flips the rule: `off` and Claude stops writing markers, `on` and it
starts again. Nothing already written is touched.

```
/todoMarkCode          # show the current state, then ask on / off / keep
/todoMarkCode on       # markers on (the default after install.sh)
/todoMarkCode off      # markers off
```

## What Claude does

1. **Read the config** — `.claude/prompt-todo/config.json` (`Read` tool). The key is
   `codeMarkers`, `"on"` or `"off"`; a missing key means `on`. If the file is missing, say
   `install.sh` has not been run here and stop.

2. **Resolve the target state.** `on` / `off` from the argument. With no argument, print the
   current state in one line and ask with `AskUserQuestion` — options *On*, *Off*, *Keep* —
   and stop on *Keep*. Any other argument → print the three forms above and stop.

3. **Already there?** If the target equals the current state, say so in one line
   (`Code markers are already off`) and stop — no edit, no render.

4. **Write** `"codeMarkers": "<state>"` with the `Edit` tool (add the key before the closing
   brace when it is missing), never the shell. Then re-render:
   `bash .claude/prompt-todo/bin/py.sh render_rules.py`. Show its one-line output. If it fails,
   show the error and revert the edit.

5. **Reply** in two lines: the new state, and what changes from now on —
   `off`: new changes carry no `[<name>#N]`, `/todoReverse` records items without marking
   code, existing markers stay and still `grep`; `on`: every change for `#N` gets its marker
   again, applies to new work only, nothing is tagged retroactively.

## Notes

- The state lives in the committed config, so it is the team's setting, not a personal one:
  say so when turning it off in a repo where `git log` shows other contributors' todo files.
- Never removes or adds markers in code — `off` is not "strip the markers"; if the user wants
  that, it is a separate, explicit request.
- The hook and the other skills read nothing here; the rendered rule paragraph is the only
  thing they follow.

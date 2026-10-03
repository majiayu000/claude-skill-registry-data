---
description: Turn a scratch script into a permanent tool this repo keeps. Use when a check, report, or analysis has proved worth running more than once.
disable-model-invocation: true
---

# Keep a script instead of rewriting it

```
chamnan-promote <file> <name> --desc "what it checks"
chamnan-promote --list
```

## When

The plugin will tell you when the same scratch script has been written a third time. Act on that
rather than filing it away — the file is still on disk at that moment, and next session it will not
be.

Also promote without being told when a script is something the repo will want to re-run: a
regression check, a report the user asks for regularly, a migration that will be repeated per
environment.

## Write the description

`--desc` is what a future session sees when deciding whether to use the tool instead of writing a
new script. `--desc "checks the save file"` will not do that. `--desc "verifies every profile in
game/saves/ still migrates cleanly to the current GAME_VERSION"` will.

## Before promoting

Make it runnable from the repo root with no arguments, or with arguments it explains when given
none. A tool that only works from the directory it was written in gets rewritten next time anyway.

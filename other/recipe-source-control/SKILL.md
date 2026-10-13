---
name: recipe-source-control
description: "Use the project's Git or Lore repository like a careful teammate — status first, lock binary assets before editing, save, review the diff, submit with a real message, merge graph conflicts."
---

# Source control (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/source-control"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- the project is in a Git repository or a Lore workspace and you are about to change assets
- submitting / committing / pushing your work
- a sync reports conflicts, or a push was refused because the server moved
- a file is locked by someone else
- the user asks what changed, who changed a file, or to undo local changes

## Ops it names

`vcs.status`, `vcs.checkout`, `vcs.lock`, `vcs.unlock`, `vcs.add`, `vcs.diff`, `vcs.history`, `vcs.revert`, `vcs.submit`, `vcs.sync`, `vcs.resolve`, `session.autosaves`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.

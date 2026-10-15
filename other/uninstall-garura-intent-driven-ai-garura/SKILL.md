---
name: uninstall-garura
description: 'Remove Garura from a target project or repository — the reverse of sud:install-garura. Reads the target''s install manifest and deletes exactly the host skills/agents/plays (.claude for Claude Code, .agents for Codex) and .garura bootstrap files that sud:install-garura created, while preserving the user''s own work (the issue/STM tree) unless explicitly told to purge. Use when the user wants to uninstall, remove, tear down, disable, or clean up Garura from a folder or repo — "uninstall garura from X", "remove garura", "tear down garura in this repo", "undo the garura install". Takes the target path as its argument. For the forward direction, see sud:install-garura.'
user-invocable: true
---

# uninstall-garura

Remove Garura from a **target** project — undo what `sud:install-garura` did there. You run this
from the garura repo; the target is the folder or repo the user names.

## How this play is built (read this first)

This is a **bootstrap meta-play** — like sud:install-garura, hand-authored (not compiled from an
ICE source) and **harness-led**: the play decides and reports, a bundled script does the
deterministic file work. The mechanical removal lives in
[`scripts/uninstall.py`](scripts/uninstall.py). Don't re-implement deletions in prose — call
the script and reason about its result.

Level 3 note (#466): bootstrap meta-play — exempt from the goal-loop recompile (no ICE
source, like play-creator); runs are session-stamped by the host play when invoked through
the pipeline.

## What makes this safe: the manifest

`sud:install-garura` writes `.garura/install-manifest.json` in the target, recording the exact set
of skills, agents, plays, config, CLAUDE.md, and the shared-memory path it created.
`uninstall-garura` reads that manifest and removes **only that set**. It never guesses and
never removes a file it cannot prove the installer placed. No manifest means nothing was
installed here (by us), so there is nothing to remove — the script says so and exits cleanly.

## The one thing it preserves: your work

A default uninstall does **not** delete the STM tree at `.garura/project/` — that holds
issues, specs, and evidence a person produced, which the installer never created. The script
keeps it (and the `.garura/` shell around it) and tells you so. Empty shells left behind by
the removal are pruned; a directory still holding your work is left alone.

## What a default uninstall removes

Each only if the manifest recorded it:

- every `.claude/skills/<id>` the manifest lists (skills and plays both live here),
- every `.claude/agents/<id>.md` the manifest lists,
- the target's `.garura/core/config.yaml`,
- `CLAUDE.md.new` (only the installer-written variant — never the user's own `CLAUDE.md`),
- `.garura/install-manifest.json`,
- then any directories left empty by the above.

The **shared memory** (machine-global, recorded in the manifest) is kept by default — other
projects on the machine share it. It is removed only on an explicit, confirmed `--purge`,
and only the exact path the manifest recorded.

## Pre-flight

1. **A target is named.** The user must say which folder/repo to uninstall from. If they
   didn't, ask — don't guess. The target must be an existing directory.
2. **Decide purge vs default.** Default preserves the shared memory. Only use `--purge` if the
   user clearly wants the machine-global garura memory gone too — confirm first.
3. **Python 3 is available.** The script is Python 3, no third-party packages.

## Run it

```
python3 core/components/plays/uninstall-garura/scripts/uninstall.py --target <path-to-target>
```

Options:
- `--dry-run` — print what would be removed and change nothing. Good for showing the user the
  blast radius before committing.
- `--purge` — also remove the shared memory recorded in the manifest (confirm first).
- `--quiet` — less output.

Idempotent: running it a second time finds no manifest and reports nothing to do.

## Report back

After the script returns, tell the user in plain language:

- which target it cleaned,
- how many items were removed (and that the `.claude` skills/agents and the `.garura` config
  are gone),
- whether the shared memory was preserved (and where), or — if `--purge` — that it was removed,
- if there was no manifest: that nothing Garura-installed was found, so nothing changed.

Keep it short and concrete.

## Boundaries

- **Manifest-driven only.** Remove exactly what the manifest records. Never delete a
  `.claude/` skill or `.garura/` file the installer didn't create — including the user's own
  files sitting alongside the installed ones.
- **Preserve work by default.** The issue/evidence tree and the shared memory are kept;
  memory goes only on an explicit, confirmed `--purge`.
- **Prefer `--dry-run` when unsure.** If the scope is at all ambiguous, show the user the
  dry-run output and let them confirm before the real removal.

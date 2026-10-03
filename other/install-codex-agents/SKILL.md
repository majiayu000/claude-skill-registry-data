---
name: install-codex-agents
description: Install this plugin's Kotlin review agents into Codex, which cannot load agents from a plugin.
disable-model-invocation: true
---

# Install Codex Agents

Codex cannot load agents from a plugin. Its `plugin.json` has no `agents` field, so a plugin that
ships agents has to copy them into a Codex agents directory. This skill does that copy.

This skill is for Codex only. In Claude Code and Junie the same agents ship with the plugin/extension
and are already available — say so and stop.

## What gets installed

The `assets/` directory next to this `SKILL.md` holds one `.toml` file per agent:

| File | Agent |
|---|---|
| `kotlin-test-review.toml` | judges whether Kotlin tests prove the code works |
| `kotlin-architecture-review.toml` | judges module split, dependencies, SOLID, and core purity |
| `kotlin-abi-review.toml` | judges whether a library release breaks binary compatibility |

Read the directory rather than trusting this table; the plugin may ship more.

## Ask where

Offer two targets. The default is global.

| Target | Path | Effect |
|---|---|---|
| global (default) | `~/.codex/agents/` | available in every project on this machine |
| project | `<repo root>/.codex/agents/` | available in this repository only, and can be committed |

Ask once, in one line, and take the default if the user does not care.

A global install writes outside the workspace, so Codex asks once to raise the sandbox. That prompt is
expected; tell the user before it appears. A project install stays inside the workspace and needs no
prompt.

## Install

1. Confirm the target directory, then create it: `mkdir -p <target>`.
2. Before writing anything, parse the `name` from every shipped asset and every existing
   `<target>/*.toml`. Build a `name -> [paths]` map and compare each canonical target file with its
   asset.
3. Finish the whole preflight before copying any file. Collect and show:
   - an incoming `name` already present under another file name;
   - a canonical target file whose content differs from the asset;
   - an existing TOML that cannot be parsed well enough to rule out a conflict.
4. If preflight found a conflict, make no changes yet. Show every involved path and the diff of each
   existing file against the incoming asset when comparable. Ask for an explicit action for every
   path that would be overwritten, renamed, or deleted. A choice of which identity should remain is
   not by itself permission to delete a locally customized file. Never create two files with the same
   agent `name`.
5. After conflicts are resolved, handle every canonical asset file:
   - Missing and with no name collision: copy it.
   - Present and identical: skip it and say so.
   - Present and different: overwrite only when that exact path was approved.
6. Copy with `cp <assets>/<file> <target>/<file>`. Do not rewrite the contents on the way through.
7. List what was written, skipped, explicitly overwritten or removed, and left unresolved.

## Verify

1. Confirm each file is at the target path and is valid TOML with a `name`, a `description`, and a
   `developer_instructions` value.
2. Confirm that agent names are unique across the whole target directory. Codex identifies an agent
   by its `name` field, not by the file name.
3. The agents are picked up on the next thread, not in the running one. Tell the user to start a new
   Codex thread, then ask for the agent by name.

## After installing

Point the user at the `kotlin-review` skill, which dispatches the relevant installed agents over a
chosen scope:

```text
$kotlin-quality:kotlin-review review the tests and architecture of this branch
```

For removal, resolve the shipped agent's `name` against every TOML in the target directory, not only
the canonical filename. If several paths declare that name, list all of them. Compare each path with
the shipped asset and request an explicit decision for each file before deleting it; a differing file
may contain local customization. After removal, verify that no remaining target TOML still declares
the agent name, otherwise report that the agent remains installed. To update after a plugin upgrade,
run this skill again and review every proposed overwrite or removal.

---
name: xyz-mod
description: >-
  Load, verify or troubleshoot the read-only XYZ Claude Code mod that adds /xyz-status — recent hosted
  runs on development, tick claims and marathon/relay driver state, printed with no model turn. Use when
  the operator asks to "install the xyz mod", "turn on /xyz-status", "check the xyz mod", or to run its
  manual diagnostic. Requires Claude Code 2.1.287 or newer. Not a builder or a guard: the mod never
  approves, blocks or rewrites tool calls or prompts.
---

# xyz-mod — `/xyz-status` without a model turn (GH-964)

A Claude Code **mod** is a plugin whose TypeScript hooks run inside Claude Code. This one adds a
single slash command, `/xyz-status`, that runs at once (even mid-turn), costs no model turn, and replies when its readers finish (15 s cap each).
It prints, under one `root:` line naming the repo it read:

1. **Hosted runs on development (recent 8)** — `gh run list --branch development --limit 8`
   (wave-reconcile and the `ci.yml` gate alike). A bounded recent view, not a full inventory.
2. **tick claims** — `bin/tick claims`, with `TICK_REPO_ROOT` pinned to the root.
3. **Marathon / relay drivers** — `relay-automation/marathon-ls.sh` (LIVE / STALE / IDLE / GONE).

It runs those existing readers and prints their output; it has no logic of its own. Relay threads
that no driver runs (plain `relay-system/**` STATUS) are not listed (deferred in GH-964).

The command is `/xyz-status`, not `/xyz`, because `/xyz` is the `xyz` coordination skill.

## Load it

Mods need Claude Code **2.1.287 or newer** (`claude --version`). Load the mod for a session from a
maintained XYZ-forge clone:

```bash
claude --plugin-dir "<clone>/skills/2-daily/xyz-mod/mod"
```

Then `/plugin` lists it as an active mod, and `/xyz-status` appears in the command menu. Start the
session inside the clone (any subfolder works): the mod reads the repo that the session's folder
belongs to, and says so if that folder is not a git repo.

Drawing (panes, bands) shows only in the terminal and Desktop; this mod draws nothing, so its text
reply works in the VS Code extension too.

## Boundary

The mod registers only `session.start` (to declare the command) and `command.run` for
`xyz-status`, and calls only `$.command.register` and `$.process.run`. It registers no `tool.call`,
`prompt.*` or `session.append` hook. Mods are not sandboxed, so any later change that adds one of
those hooks needs its own issue and review.

Each section stands alone: a reader that fails, times out or prints nothing shows
`ERROR (<exit or reason>): <first stderr line>` in its own section, and the other sections still
answer. A failed reader is never shown as "nothing in flight".

## Manual diagnostic

This is a written checklist, not a test suite (XYZ-forge adds no new suites: AGENTS.md, GH-831).
Record each run under `TESTS-RESULTS/<date>+GH-964/` with a `provenance.jsonl`. **Healthy** means
exit 0 and non-empty output; anything else is **FAIL**.

| Check | How | Pass when |
|---|---|---|
| D1 | `claude --version` | 2.1.287 or newer |
| D2 | `claude plugin validate <clone>/skills/2-daily/xyz-mod/mod` | hooks are only `session.start`, `command.run{command=xyz-status}`; calls only `$.command.register`, `$.process.run` |
| D3 | from the clone root, run each reader by hand: `gh run list --branch development --limit 8`; `TICK_REPO_ROOT="$PWD" bin/tick claims`; `bash relay-automation/marathon-ls.sh` | each healthy |
| D4 | `/plugin` in a session started with `--plugin-dir` | the mod is listed active |
| D5 | `/xyz-status` in the terminal **and** in the VS Code extension | root line + three healthy sections; no assistant reply follows |
| D6 | `/xyz-status` in a session started in `<clone>/src` | root line names the clone root; sections healthy |
| R1 (red control) | temporarily change one reader's path in `hooks/register.ts` to a missing file (do not commit), run `/xyz-status`, then restore and run again | mutant: that section FAIL, the other two healthy; restored: all healthy |

Record the go / no-go (keep, extend, drop) in the GH-964 plan's Status table and on the issue.

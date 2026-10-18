---
name: "Roadmap: Configure"
description: "Set or clear a per-phase roadmap option through the CLI, then render the dashboard once so it exists at the new path. The one option is artefact: where the HTML dashboard is written, relative to the project root."
when_to_use: "When the user wants the roadmap dashboard written somewhere other than the default docs/artefacts/roadmap-{slug}.html (a short checked-in filename, a docs site folder) or wants that override removed. Never for changing the dashboard's look (that is the template) or for a plain render (roadmap:dashboard)."
model: sonnet
effort: low
metadata:
  glyph: ᛊ
  family: roadmap
disable-model-invocation: true
allowed-tools: ["Read", "Bash(python3:*)"]
arguments: ["option", "value", "phase"]
argument-hint: "artefact <path>|clear [phase name]"
---

# Roadmap Configure

A phase's `artefact` key in `roadmaps.json` says where `render` and `recompute --render` write its dashboard; without it the slug default applies. This skill is the one way that key changes: the CLI writes it (inserted in field order, nothing else touched), then one render proves the new path. The resolution order and the key's rules are in `${CLAUDE_PLUGIN_ROOT}/references/roadmap-conventions.md` (File formatting). The CLI is `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py`.

## Steps

1. **Read the arguments.** `$ARGUMENTS` is `artefact <path>` or `artefact clear`, optionally followed by a phase name (needed when several phases are active, or to re-home an archived phase's dashboard). The path is relative to the project root and ends in `.html`, e.g. `docs/artefacts/roadmap-t1c.html`. Anything missing or any other option name: ask, never guess a path.
2. **Write the key.** Run `roadmap.py config artefact "<path>"` or `roadmap.py config artefact --clear`, adding `--phase "<phase>"` when one was given. Exit codes:
   - **0**: written. Keep the output; it names the new dashboard path and may add two notes (a dashboard still at the old path, no dashboard at the new path yet).
   - **1** with the canonical-form message: `roadmaps.json` is not tab-indented. Ask before re-running with `--reformat`, since that rewrites the whole file.
   - **1** with a refusal (absolute path, `..` segment, not `.html`): report the reason and stop.
   - **2**: could not locate, parse or find the phase; report the message and stop.
3. **Render once.** Run `roadmap.py render`, with the same `--phase` when one was given, so the file exists at the new (or restored default) path. Do not open it.
4. **Report.** The new dashboard path and that `roadmaps.json` changed, both ready to commit. If the CLI noted a dashboard left at the old path, say so: nothing refreshes it any more, so the user deletes it (or `git rm`s it). If the project's `.gitignore` ignores `docs/artefacts/` and the user wants the new file checked in, un-ignoring it is theirs to do; the plugin never edits `.gitignore`.

## Notes

- `recompute --render` (run by `roadmap:maintain`) follows the key from the next run on; no other skill needs telling.
- `render --out PATH` still wins over the key for a one-off render elsewhere.

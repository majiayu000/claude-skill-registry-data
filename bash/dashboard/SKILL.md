---
name: "Artefacts: Create Roadmap"
description: "Generate the HTML roadmap dashboard deterministically via roadmap.py render."
when_to_use: "When you want to view or share the current roadmap as an interactive dashboard rather than reading roadmaps.json directly."
model: sonnet # was haiku: auto mode skips haiku and keeps the session model, which is sometimes Fable or Opus here; sonnet pins it
effort: low
metadata:
  glyph: ᛊ
  family: artefact
disable-model-invocation: false
allowed-tools: ["Read", "Glob", "Bash(python3:*)", "Bash(open:*)"]
arguments: ["phase"]
argument-hint: "[phase name (optional, when several are active)]"
---

Render the interactive roadmap dashboard. The HTML is generated deterministically by `roadmap.py render` from the template at `${CLAUDE_PLUGIN_ROOT}/templates/roadmap-artefact.html`: this skill runs the command and opens the result; it writes no HTML itself. Same data in, same file out, so regenerated artefacts diff cleanly and can never drift from `roadmaps.json`.

Shared conventions (statuses, colour table): `${CLAUDE_PLUGIN_ROOT}/references/roadmap-conventions.md`.

## Steps

1. **Check the format.** Run `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py detect`. Exit **3** = old simple format: stop and tell the user to run `roadmap:migrate` first. Exit **2** = could not locate/parse; ask for the path. Proceed on exit 0.
2. **Render.** Run `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py render`, adding `--phase "$ARGUMENTS"` when the user named a phase (required if several are active). Default output: `{project_root}/docs/artefacts/roadmap-{slug}.html`. On a validation-discrepancy note in the output, still render (the page shows a discrepancy banner) but include the discrepancies in your report.
3. **Open and report.** `open` the written file. Report: the file path; milestone and task counts plus done percentage (`roadmap.py stats`); the unblocked `todo` tasks and the claimed ones (`roadmap.py ready`; surfaced directly, no need to open the file); any validation discrepancies.

## Notes

- The dashboard refreshes automatically when `roadmap:maintain` runs (`recompute --render`); invoke this skill for the first render or an on-demand refresh.
- Collapse defaults belong to the template, and generated markup never carries an `open` attribute by hand. Two sections open by default. The Overview section's own `<details>` ships `open` in the template, so the headline and progress cards are the first thing a reader sees. A tier group's `<details>` opens by computation, never by hand: `roadmap.py`'s `overview_layout()` marks it open only once its tier itself is open (every milestone in every lower tier is `done`) and it holds a ready or in-progress task; see roadmap-conventions.md's Milestone sort and tier grouping section. Everything else defaults to **closed**: every milestone `<details>` and, inside each milestone, the Blocked, Done and Out of Scope status groups (each a `<details>` whose heading carries its task count). Never hand-edit an `open` attribute in a generated file; a different default is a template change.
- The dependency graph's direction (`TD`/`LR`) is chosen per render by `roadmap.py`'s `choose_direction()`, from the same live nodes/edges the diagram draws. The diagram shell has no height cap (a tall diagram just makes the page scroll), so this is a width-only comparison against the real layout column's width: whichever direction lays the widest layer or the longest chain out narrower wins, a tie keeps `TD`. A long thin chain picks `TD` (one node wide); a wide fan picks `LR` (spread across ranks instead of side by side). Never hardcode a direction in the template; a different choice belongs in `choose_direction()`'s constants.
- Sections, palette and behaviour live in the template. To change the dashboard's look, edit `templates/roadmap-artefact.html`; to change status colours, change the canonical table (`STATUS_STYLE` in `roadmap.py` + the conventions reference); never patch a generated file.
- The artefact is generated in the CLI's own canonical form (tabs, single-line JSON payload), not Prettier's. A repo that runs Prettier (or another formatter) in a pre-commit hook or CI should exclude it: add `docs/artefacts/roadmap-*.html` to `.prettierignore`, the same way `.claude/roadmaps.json` is already excluded, so regenerating the dashboard never fights the formatter.
- The template follows a fixed artefact contract (theme-sourced palette, IBM Plex Mono/Sans pairing, the three-state light/dark/explicit-toggle contract with its masthead toggle control, collapsible milestone `<details>` closed by default). Any future template edit should stay inside that contract rather than drift from it: the template is the one place to fix a divergence, never a generated file.

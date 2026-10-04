---
name: setup-labels
description: Create or update this repo's GitHub labels (status::*, hitl/afk, task-report::required, resolution::wontfix, wayfinder:*) to match docs/agents/triage-labels.md. Run once per repo before first use of triage, to-spec, to-tickets, implement, to-guide, or wayfinder.
disable-model-invocation: true
---

# Setup Labels

`gh issue edit --add-label`/`gh issue create --label` fail on a label that doesn't exist yet — `gh` never auto-creates one. This skill creates every label this repo's triage taxonomy needs, so those calls never fail on a missing label.

## Process

1. **Read the tables.** Pull every `Label` / `Color` row from `docs/agents/triage-labels.md` — the taxonomy tables (category, execution mode, workflow state, context labels) and the Wayfinder addendum. Name and hex color only, skip the `Meaning`/`Applied by` columns. If the file doesn't exist, tell the user to run `/setup-matt-pocock-skills` first and stop.
2. **Show the plan.** List every label about to be created or updated, with its color. Confirm with the maintainer before touching GitHub — this mutates shared repo state, same discipline as any other tracker-mutating step in this repo (see `docs/agents/issue-tracker.md`).
3. **Apply.** For each label, run `gh label create "<name>" --color "<hex>" --force`. `--force` makes this idempotent — it updates the color of a label that already exists instead of erroring, and touches nothing else about it (issues already carrying it are unaffected).
4. **Report.** One line per label: created, updated (color changed), or already correct (no-op). Don't re-print the full plan from step 2.

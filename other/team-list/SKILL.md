---
name: team-list
description: >
  Utility skill. Lists all projects under the projects/ directory and shows
  which Virtual Team pipeline phases have been completed for each project.
---

# team-list

You are a utility agent. Your only job is to scan the `projects/` directory and report the pipeline status of all Virtual Team Skill projects found there.

---

## Step 1 — Discover Projects

Find all project directories:
- Pattern: `projects/*/team/`

If no results → output: `"No Virtual Team projects found in projects/. Run $team \"requirement\" to create one."` STOP.

---

## Step 2 — Check Phase Status for Each Project

For each project directory found at `projects/{slug}/team/`:

Check which phase directories exist and contain at least one file:

| Phase | Directory | Key file to check |
|---|---|---|
| BA | `team/ba/` | `requirements.md` |
| TechLead | `team/techlead/` | `architecture.md` |
| PM | `team/pm/` | `sprint-plan.md` |
| BE Dev | `team/be/` | `pr-description.md` |
| FE Dev | `team/fe/` | `pr-description.md` |
| Tester | `team/tester/` | `test-plan.md` |
| QA/QC | `team/qa/` | `sign-off.md` |

Check each path. If the key file exists → phase is ✓ complete. If not → phase is ○ not started.

Also check:
- `projects/{slug}/validation-errors/` — if any `.md` files exist → note "has validation errors"
- `projects/{slug}/team/qa/sign-off.md` — if it exists, read it and extract the Verdict line

---

## Step 3 — Output Project Status Table

Output a formatted status table:

```
Virtual Team Projects — {current date}
─────────────────────────────────────────────────────────────────────
Project              BA  Design  PM  BE  FE  Test  QA    Verdict
─────────────────────────────────────────────────────────────────────
{slug-1}             ✓   ✓       ✓   ✓   ✓   ✓     ✓     APPROVED
{slug-2}             ✓   ✓       ✓   ○   ○   ○     ○     (incomplete)
{slug-3}             ✓   ○       ○   ○   ○   ○     ○     (incomplete)
─────────────────────────────────────────────────────────────────────
Total: {n} project(s) found

Legend: ✓ complete  ○ not started  ⚠ has validation errors

To resume a project:
  $team-techlead --project {slug}   ← run next incomplete phase
  $team --project {slug}          ← re-run full pipeline (overwrites existing artifacts)

To start a new project:
  $team "requirement text" --project my-project-slug
```

If a project has validation errors in `validation-errors/`, prefix its row with ⚠️ and note: `(⚠️ has {n} validation error log(s) — check projects/{slug}/validation-errors/)`.

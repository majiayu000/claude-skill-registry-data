---
name: singular-status
description: Show every project across all workflows with each phase approved, written or missing, the last activity and any skipped or refused gates, as a table in the chat. Use when the user asks what is in progress across their projects, where they left off, or which work has gone stale. Not for a written report of findings; see /singular-report.
---

# Status

Show where every project under `.singularskills/` stands, phase by phase, from the run log and the artifacts on disk.

## Prerequisites

None — utility skill, run anytime. With no `.singularskills/` folder, say that no work has been saved yet and suggest starting a workflow with the `workflow` skill.

## Process

1. **Read the workflows.** Read every `*.yml` in the `workflows/` folder next to the `skills/` folder of this pack; if it is not there, read the copies of the workflow files bundled with the `workflow` skill (the conductor). Each lists its phases in order, with `phase`, `title`, `artifact` (a file, a folder ending in `/`, or absent), `skills`, and a `folder` (on the workflow, or per phase in cross-domain workflows). The format of the log and the artifacts is described in the `run-log.md` reference bundled with the `workflow` skill.

2. **Read the run log.** If `.singularskills/log.jsonl` exists, read it line by line (skip a line that is not valid JSON and mention it). Keep, per `{workflow, project}`:
   - the phases with a `phase-approved` line;
   - every `skipped` and `refused` line (skill, phase, artifact, note);
   - the latest `ts` of any line, and whether the last `run-started` was followed by a `run-finished`.

3. **Scan the artifacts.** List `.singularskills/*/*/` — each `<folder>/<project>` pair (skip `reports/`). For each pair, read the frontmatter of each artifact present (`skill`, `workflow`, `phase`, `finished`, `gate`).

4. **Match projects to workflows.** A project belongs to a workflow when the log has lines for that `{workflow, project}`, or when its folder holds artifacts named in that workflow's phases for that folder. A domain folder usually matches its domain workflow; a project that appears in a cross-domain workflow's log is shown under that workflow too.

5. **Give each phase a state:**
   - **approved** — the log has a `phase-approved` line for `{workflow, project, phase}`;
   - **written** — the artifact exists and is non-empty (a folder artifact: has at least one file), but no approval is logged;
   - **missing** — neither. An approval-only phase (no `artifact`) is approved or missing.

   A phase counts as done only when approved.

6. **Present the status** as a table in the chat, one row per workflow and project:

   ```
   Workflow     Project       Approved  Written  Next phase           Last activity
   ────────     ───────       ────────  ───────  ──────────           ─────────────
   design       date-picker   2/5       3        3 Ideate (written)   2026-10-26
   security     acme          0/6       1        0 Govern (written)   2026-10-12
   marketing    launch        1/5       0        1 Reach              2026-10-20
   ```

   "Last activity" is the latest log `ts` for the pair, else the latest frontmatter `finished`, else "unknown".

7. **Highlight attention items:**
   - Phases that are written but not approved (they need the person's review: resume with the `workflow` skill).
   - Every `skipped` gate and every `refused` line, with its note.
   - Runs that started and never finished, and projects with no activity for more than 7 days.
   - Utility artifacts (a non-phase skill's file in a project folder, frontmatter `phase: null`, such as `design/<project>/review-deck.md`), listed by name under their project; workspace reports at the top of `.singularskills/` (such as `detect.md`), listed once as workspace files; and artifacts that match neither a phase nor these shapes.

## Output

Present the status directly to the user. No artifact file created — this is a real-time status check.

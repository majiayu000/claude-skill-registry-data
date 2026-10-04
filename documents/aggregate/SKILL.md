---
name: aggregate
description: Pull learnings and retrospective insights from all registered projects into the central knowledge base. Run periodically to keep cross-project knowledge current.
user-invocable: true
---
# Aggregate Cross-Project Learnings

Pull learnings and retro insights from all projects in `registry.yaml` into `docs/process/aggregation-log.md`.

## Steps

1. **Read `registry.yaml`** to get the list of managed projects with their paths.

   **Then drop every entry with `aggregate: false`, before you read anything.**
   These are client engagements. Their learnings and retros must never reach
   `aggregation-log.md`, which is a shared fleet artifact — pulling a client's
   docs into it is the exact cross-contamination a clean-room separation is
   supposed to prevent, and it cannot be undone by deleting the lines later.

   Build the project list first, remove the excluded entries, say out loud
   which ones you removed, and only then start step 2. Filtering as you go
   does not work: `git pull` in step 2 and the file reads in step 3 have both
   already happened by the time you would notice.

2. **Ensure freshness** of each project's main worktree:
   - Run `git -C <path> pull --ff-only` to update to latest origin/main
   - If pull fails (dirty worktree, non-ff), warn the user and note the discrepancy
   - Report freshness status to the user before proceeding

3. **For each project**, read:
   - `<path>/<docs.learnings>` (typically `docs/process/learnings.md`)
   - `<path>/<docs.retros>` (typically `docs/process/retrospective.md`)

4. **Compare against `docs/process/aggregation-log.md`** to identify new entries that haven't been aggregated yet. Avoid duplicating entries already present.

5. **Add a new top-level section** `## YYYY-MM-DD` to `docs/process/aggregation-log.md` for this pass. Append new entries under it, tagged with:
   - Source project name
   - Date (from retro entry or current date for learnings)
   - Category (if present in the original)

   Format:
   ```markdown
   ## YYYY-MM-DD

   ### [Category] (from [project-name], [date])
   - [Specific learning or insight]
   ```

6. **Identify cross-cutting patterns** — learnings that appear in multiple projects or that would benefit all projects. Use these prompts when scanning across projects:

   - **Recurring failures:** Is the same kind of error showing up in multiple projects? Fix it once — in the generic skill, template, or rule — rather than project-by-project.
   - **Slow tasks:** What made some tasks drag? Missing context, ambiguous requirements, bad tooling choices? Update the relevant skill to surface the gap earlier.
   - **Successful patterns:** What kinds of work consistently go well? Document what made them work so other projects can lean on the same approach.
   - **Skill gaps:** Are peers frequently deferring or bouncing things back to the user that they should be able to handle? The skill definition is probably too vague — tighten it.

   Add findings to a "Cross-Cutting Patterns" subsection of the new date section with:
   - The pattern description
   - Which projects it was observed in
   - Whether it should be propagated (and how — skill update, CLAUDE.md update, etc.)

   **Before marking a pattern as needing propagation**, reconcile against what's already been addressed:
   - Read `templates/skills/` and `templates/rules/` — if the fix is already in a template, note it as done
   - Read `docs/process/propagation-log.md` — if it was already pushed to projects, note that
   - Check whether the pattern predates a major tooling adoption (e.g., superpowers) — if the recommended fix is now covered by a shared plugin, flag it as "already addressed by [plugin]" rather than a new action
   - Only flag a pattern as needing propagation if it's absent from templates, absent from the propagation log, and not covered by an installed shared plugin

7. **Commit** the updated `docs/process/aggregation-log.md` with message: `knowledge: aggregate learnings from [N] projects`

8. **Summarize** what was aggregated:
   - How many new entries from each project
   - Any cross-cutting patterns identified
   - Recommendations for `/propagate` actions

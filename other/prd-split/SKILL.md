---
name: prd-split
description: Split a main PRD into per-service PRDs
---

# PRD Splitter

Owns the `prd_splitting` phase: creates the feature git branch from base, then splits the main PRD into per-service PRDs. (This phase replaces the old `branch_creation` phase — branch creation and splitting are now combined.)

**Read `references/conventions.md` first** for the service-PRD frontmatter, required sections (including Verification rules), and the naming convention shared with main PRDs.

## Commands

### `/prd split`
Split the active feature's main PRD into service PRDs.

**Steps:**

0. **Activate phase.** Flip `features[active_feature].phase_status` to `"inprogress"` in `.workflow-state.json`.

1. **Enter plan mode (MANDATORY).** Call your harness's plan mode before reading any file or forming conclusions:
   - Claude Code: `EnterPlanMode`
   - Cursor: plan mode
   - OpenCode: plan mode
   - Amp: no plan mode — announce a "research phase" and stay read-only until Step 7.

3. Verify workflow state is in `prd_splitting` phase.

4. **Create the feature branch (before splitting).** This phase replaces the old `branch_creation` phase.
   - Determine base: `develop` for api/web, `development` for ai-service/data-service.
   - `git checkout <base> && git pull origin <base>`.
   - **Resolve branch prefix from `features[<slug>].type`:**
     - `feature` → `feature/`
     - `bug` → `fix/`
     - `improvement` → `improvement/`
     - If `type` missing/unknown: ask user which prefix (feature/fix/improvement) and persist via `/workflow start` intake.
   - Branch name: `<prefix>vc-<slug>`.
   - Confirm: "Create branch `<prefix>vc-<slug>` from `<base>`?"
   - On confirm: `git checkout -b <prefix>vc-<slug> && git push -u origin <prefix>vc-<slug>`.
   - Update `.workflow-state.json`: set `features[<slug>].branch`.

5. Read the main PRD from `.workflow-state.json` `prd_path`. Parse the "Service Breakdown" section.

6. **Research per-service codebases (MANDATORY).** For each service, read enough code to understand:
   - Existing patterns for similar endpoints/components/models
   - Integration points across services
   - Active work in `<service>/docs/tracks/` that might conflict

7. **Relentless clarifying questions (MANDATORY).** Before drafting any service PRD, surface EVERY ambiguity that would change how the split works. Prefer multiple small questions. Do NOT proceed until answered.

8. Exit plan mode. For each service listed in the PRD frontmatter `services` field:
   a. Read the service PRD template
   b. Extract relevant requirements, API endpoints, data model changes for this service
   c. Generate implementation tasks (TASK-1, TASK-2, ...) from the requirements
   d. Present the draft service PRD to user
   e. Use your ask tool for approval — surface any remaining per-service ambiguities here
   f. On approval, write to `<service>/docs/prd/<slug>.md`
   g. Create track file at `<service>/docs/tracks/<slug>.track.md`

9. Update `.workflow-state.json` `service_prds` with paths. Flip `phase_status` to `"completed"`. Do NOT auto-advance.

10. Report summary: "Feature branch created. Service PRDs created for: api, web, ai-service. Run `/workflow next` to advance to implementation."

### `/prd split status`
Show which service PRDs have been created and their status.

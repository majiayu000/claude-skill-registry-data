---
name: workflow
description: Manage feature workflow state — status, transitions, context switching
---

# Workflow Manager

Manages the feature development workflow state machine.

## References (load when needed)

- `references/track-conventions.md` — Track-file location, frontmatter, required sections, session-log rules. Read when entering `implementation`, updating progress, or creating a new track file.
- `references/testing-policy.md` — STRICT opt-in testing rules. Read before writing or running tests.
- `references/session-checks.md` — Session-time procedures (feature branch recency check, service health checks, update-check + sync + conflict handling). Read when the session-start protocol in `AGENTS.md` delegates here.

## Commands

### `/workflow status`
Show the current workflow state for the active feature.

**Steps:**
1. Read `.workflow-state.json`
2. Display:
   - Active feature: `{active_feature}`
   - Current phase: `{phase}` ({phase_name})
   - Phase status: `{phase_status}` (`idle` / `inprogress` / `completed`)
   - Phase entered: `{phase_entered}`
   - Worker: `{worker}`
   - Type: `{type}` (feature | bug | improvement)
   - Brainstorming: questions answered / total, summary present?
   - Branch: `{branch}` or "not created"
   - Service PRDs: list with status
   - PRs: list `{pr_urls}` entries (service → URL) or "not submitted"

### `/workflow list`
Show ALL active features with their phases.

**Steps:**
1. Read `.workflow-state.json`
2. For each feature in `features{}`:
   - Show slug, phase, phase_entered, worker
   - Mark active feature with `→`

### `/workflow start <slug>`
Start a new feature workflow.

**Steps:**
1. **Check onboarding state first.** Read `.onboard-state.json`:
   - If file doesn't exist and no service directories → BLOCK: "Run `/onboard` first."
   - If `status` is `"in_progress"`, check critical steps:
     - `steps.env_files` must be `"completed"` (every service that needs a `.env` has a real one).
       A service whose `env_status` is `"n/a"` is **satisfied, not pending** — it has no `.env` by
       design (data-pipeline uses Prefect Secret blocks), so it must not hold this field back.
     - `steps.db_setup` must be `"completed"` (if API service is selected)
     - `steps.clone_repos` must be `"completed"`
     - `steps.install_deps` must be `"completed"`
   - If ANY critical step is missing → BLOCK and list what's needed:
     ```
     Cannot start workflow. Onboarding is incomplete:
       - api/.env is missing — contact arhen
       - Database not restored — contact arhen for dev dump
     Run `/onboard resume` to complete setup.
     ```
   - If `status` is `"completed"` → proceed
2. Read `.workflow-state.json` (create if doesn't exist).
3. Check that `<slug>` doesn't already exist in features.
4. **If an active feature already exists**, offer parallel work via **git worktrees** (no extra tooling — modern agents handle worktrees fine):

   > "You have an active feature (`<active-slug>` in `<phase>`). You can:"
   > - **Continue here** with context-switching (`/workflow switch` between features) — recommended for related work
   > - **Work in parallel** — the new feature gets its own git worktree per affected service repo (`git worktree add <path> -b <prefix>vc-<slug> <base>`), one agent session there

   If the user picks parallel: create the worktrees, key `.workflow-state.json` features by slug, and proceed in the separate directory. Cleanup (`git worktree remove`) at completion.
5. Capture intake via the ask tool:
   - **Type:** feature | bug | improvement
   - **Initial request:** the user's raw description (free text)
6. Create feature entry with:
   ```json
   {
     "phase": "idle",
     "phase_status": "completed",
     "phase_entered": "<ISO>",
     "type": "<type>",
     "initial_request": "<text>",
     "brainstorming": { "questions": [], "summary": null },
     "prd_path": null,
     "branch": null,
     "service_prds": {},
     "pr_urls": {}
   }
   ```
7. Set `active_feature` to `<slug>`. Ask the user for worker name if not set.
8. Save state.
9. Ask: "Advance to brainstorming?" — on yes, transition (`phase: "brainstorming"`, `phase_status: "idle"`); the orchestrator then runs the brainstorming phase itself (skill: `brainstorm`).

### `/workflow next`
Transition to the next phase (if gate conditions are met).

**Steps:**
1. Read `.workflow-state.json`.
2. Get current phase + `phase_status` for active feature.
3. **Require `phase_status === "completed"`.** If `idle` or `inprogress`, refuse: "Phase `<phase>` is still pending (`idle`) or in progress (`inprogress`). Let the agent finish (or wait for it to flip phase_status to completed) before advancing."
4. Look up gate conditions from `.agentic-workflows/workflow/gates.json`.
5. **If the current phase has multiple possible next phases**, check `next_strategy` on the phase in `phases.json`:
   - `brainstorming → prd_creation` when the feature type is `feature`; `brainstorming → implementation` for `bug|improvement` (`type_bug_or_improvement`).
   - `pr_submission → pr_review` when the PR has reviewer/bot feedback (`has_feedback`).
   - `pr_submission → completion` when the PR merged with zero feedback (`merged_clean`).
6. Check EACH gate condition for the resolved transition:
   - If all pass → transition to next phase, update `phase`, `phase_entered`, set new `phase_status` to `"idle"`.
   - If any fail → report which conditions failed and what's needed.
7. Save state.
8. Inform user of new phase and which agent will handle it.

### `/workflow switch <slug>`
Switch active feature context.

**Steps:**
1. Read `.workflow-state.json`
2. Verify `<slug>` exists in features
3. Save any pending state for current feature
4. Set `active_feature` to `<slug>`
5. Load target feature's phase context
6. If on a different git branch, inform user: "Feature `<slug>` is on branch `{branch}`. Switch with: `git checkout {branch}`"
7. Save state

### `/workflow list-all`
Discover ALL features across the team — not just local ones. Scans committed artifacts and git branches.

**Steps:**
1. Fetch latest from all remotes: `git fetch --all` in each service dir
2. Scan for features from multiple sources:
   - **PRDs:** `ls docs/prd/*.md` → extract slugs
   - **Feature branches:** `git branch -r | grep -E '^(feature|fix|improvement)/[^/]*vc-'` in each service → extract slugs (matches both the `vc-`-only form and the legacy `<worker>/vc-` form)
   - **Worktrees:** `git worktree list` in each service dir plus sibling worktree dirs outside the workspace root
   - **Track files:** `find . -name '*.track.md'` across all services → extract slugs
3. For each unique slug found, reconstruct the phase (same logic as resume):
   - Brainstorming summary recorded? PRD exists? Branch exists? Service PRDs? Track progress? PR?
4. Also check local `.workflow-state.json` for any features only tracked locally
5. Display a table:

```
All features (committed artifacts + local state):

  Slug                        Phase              Last Activity         Worker
  ─────────────────────────── ────────────────── ───────────────────── ──────────
→ brand-health-dashboard      implementation     2026-03-20 (track)    fahrizky
  user-analytics              pr_review          2026-03-18 (PR #42)   daffa
  kv-generator                prd_creation       2026-03-15 (PRD)      arhen

→ = active in your local .workflow-state.json
```

6. Show: "To pick up a feature: `/workflow resume <slug>`"

### `/workflow resume <slug>`
Resume a feature started by another team member.

**Steps:**
1. Fetch latest: `git fetch --all` in each service dir
2. Scan committed artifacts to reconstruct phase:
   - Brainstorming summary recorded in `.workflow-state.json`? → past brainstorming
   - PRD exists at `docs/prd/<slug>.md`? → past prd_creation
   - Branch matching `(feature|fix|improvement)/vc-<slug>` (or legacy `<worker>/vc-`) exists AND service PRDs exist? → past prd_splitting
   - Track files show progress? → in implementation
   - PR URL in track file with no review threads? → in pr_submission (clean) or pr_review (has feedback)
   - PR merged? → in completion
3. Read the latest session log from track files to show who last worked on it and what they did
4. Create/update feature entry in `.workflow-state.json` with reconstructed state
5. Set `active_feature` to `<slug>`
6. Ask user for their worker name if not already set
7. Inform user:
   - Reconstructed phase
   - Last session log entry (who did what)
   - What's left to do (remaining tasks from track file)
   - Which branch to checkout: `git checkout <branch>` from `features[<slug>].branch` (prefix is `feature/`, `fix/`, or `improvement/` per type)

### `/workflow progress`
Show detailed progress for the active feature.

**Steps:**
1. Read `.workflow-state.json` and all related files
2. Show:
   - Phase progression timeline (with `phase_status` per phase)
   - Brainstorming summary
   - Service PRD status
   - Track file task completion percentage
   - Session log summary
   - PR self-review and security audit summaries

### `/workflow worktrees`
Offer/parallelize work with git worktrees (see `/workflow start` step 4). One worktree per affected
service repo, per feature; keyed by slug in `.workflow-state.json`; cleaned up at completion.
No extra tooling — plain git.

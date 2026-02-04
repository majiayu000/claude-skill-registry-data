---
name: conductor
description: Maintain Conductor-compatible project context, tracks, specs, and plans.
metadata:
  short-description: Conductor workflow artifacts and procedures (Gemini-compatible).
  display-name: Conductor Compatibility
  version: 0.1.0
---

# Conductor Compatibility Skill

Purpose: create and maintain Conductor artifacts so they remain fully compatible with the Gemini Conductor extension and its workflow (Context -> Spec & Plan -> Implement).

Use this skill when the user asks to set up a new project context, start a new track, implement or resume a track, check progress, or revert work.

## Required File Structure (Do Not Deviate)

```
conductor/
  product.md
  product-guidelines.md
  tech-stack.md
  workflow.md
  setup_state.json
  code_styleguides/
    *.md
  tracks.md
  tracks/
    <track_id>/
      spec.md
      plan.md
      metadata.json
  archive/                 (optional)
    <track_id>/            (optional)
```

## Required Formats

### Track ID
- Format: `shortname_YYYYMMDD` (lowercase ASCII, underscores only).
- Example: `auth_20251219`.

### `conductor/tracks.md`
- Must use `---` separators between track sections.
- Each track section must use the exact heading format below.

```
---

## [ ] Track: <Track Description>
*Link: [./conductor/tracks/<track_id>/](./conductor/tracks/<track_id>/)*
```

### `conductor/tracks/<track_id>/metadata.json`
- Required keys: `track_id`, `type`, `status`, `created_at`, `updated_at`, `description`.
- Timestamps are ISO 8601 UTC, e.g., `2025-12-19T23:59:59Z`.
- `status` values: `new`, `in_progress`, `completed`, `cancelled`.

### `conductor/tracks/<track_id>/plan.md`
- Use checklist markers: `[ ]` (pending), `[~]` (in progress), `[x]` (done).
- When completing a task, append the first 7 chars of the commit SHA to the task line.
- If the workflow defines the Phase Completion Verification protocol, append a meta-task to each phase:
  `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`
- When a phase is checkpointed, append `[checkpoint: <sha>]` to the phase heading.

## Setup Workflow (Greenfield or Brownfield)

1. Detect project maturity (greenfield vs brownfield) based on repo and code presence.
2. Create `conductor/` and `conductor/setup_state.json` if missing. Start with:
   `{ "last_successful_step": "" }`
3. Generate or update the core documents with user input:
   - `product.md`
   - `product-guidelines.md`
   - `tech-stack.md`
4. Copy the workflow template from `assets/templates/workflow.md` into `conductor/workflow.md` unless the user provides a custom workflow.
5. Copy code style guides from `assets/templates/code_styleguides/` into `conductor/code_styleguides/`.
6. Initialize `conductor/tracks.md` using the format in `assets/templates/tracks.md`.
7. Create the initial track folder and artifacts (`spec.md`, `plan.md`, `metadata.json`).
8. Update `conductor/setup_state.json` as steps complete using these values:
   - `2.1_product_guide`
   - `2.2_product_guidelines`
   - `2.3_tech_stack`
   - `2.4_code_styleguides`
   - `2.5_workflow`
   - `3.3_initial_track_generated`

## New Track Workflow

1. Confirm Conductor is set up (`product.md`, `tech-stack.md`, `workflow.md` exist).
2. Collect or confirm a track description.
3. Draft and confirm `spec.md` (requirements, acceptance criteria, out of scope).
4. Draft and confirm `plan.md` based on `workflow.md` (TDD steps if required).
5. Create `conductor/tracks/<track_id>/` with `spec.md`, `plan.md`, `metadata.json`.
6. Append the track section to `conductor/tracks.md` using the required format.

## Implement Workflow

1. Parse `conductor/tracks.md` by `---` separators and select the target track.
2. Mark the selected track as `[~]` in `conductor/tracks.md` before work starts.
3. Read `conductor/tracks/<track_id>/spec.md`, `plan.md`, and `conductor/workflow.md`.
4. Execute tasks strictly following the Task Workflow in `workflow.md` (including tests, commits, git notes, and plan updates).
5. When the track is complete, mark the track as `[x]` in `conductor/tracks.md`.
6. Synchronize `product.md`, `tech-stack.md`, and `product-guidelines.md` when the spec warrants it, with explicit user approval.
7. Offer to archive or delete the completed track. If archiving, move it to `conductor/archive/<track_id>` and remove its section from `tracks.md`.

## Status Workflow

- Verify Conductor setup and `conductor/tracks.md` exists.
- Summarize counts of tracks and tasks (done/in progress/pending).
- Report current phase/task and next action.

## Revert Workflow

- Confirm the target track/phase/task from `tracks.md` and `plan.md`.
- Use git history to identify associated commits.
- Present a clear revert plan and wait for explicit user confirmation before executing any destructive action.

## Templates Available

- `assets/templates/workflow.md`
- `assets/templates/code_styleguides/*.md`
- `assets/templates/tracks.md`
- `assets/templates/product.md`
- `assets/templates/product-guidelines.md`
- `assets/templates/tech-stack.md`
- `assets/templates/spec.md`
- `assets/templates/plan.md`
- `assets/templates/metadata.json`

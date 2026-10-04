---
name: feature-driven-flow
description: Coordinate a structured 7-phase feature delivery workflow in Codex for non-trivial work. Use when a task needs scoped intent, repository behavior tracing, ambiguity resolution, design choices, controlled implementation, assurance, and end-state reporting.
---

# Feature-Driven-Flow Conductor

Execute feature delivery in seven phases with explicit checkpoints.

## Workflow Contract

1. Run Phase 1 Scope.
2. Run Phase 2 Explore.
3. Run Phase 3 Clarify.
4. Run Phase 4 Architect.
5. Run Phase 5 Implement.
6. Run Phase 6 Verify.
7. Run Phase 7 Summarize.

Read `references/phase-contracts.md` before running phases.
Read `references/phases.md` for phase intent and non-negotiable behaviors.
Read `references/checklists.md` before finalizing.
Read `references/extension-system.md`, `references/rule-model.md`, `references/profile-model.md`, `references/context-model.md`, `references/settings.md`, `references/packs.md`, `references/effective-matrix-reuse.md`, `references/effective-instructions-reuse.md`, and `references/specialist-skills.md` before applying rules.

## Core Skeleton Invariants

1. Do not change phase order.
2. Do not begin Implement without explicit user approval.
3. Do not leave Clarify while decision-critical ambiguity remains unresolved.
4. Do not close workflow before Verify disposition and final Summarize output.

## Interactive Decision UX

1. When a user decision is needed, provide 2-4 numbered options.
2. Mark one option as recommended and include a one-line rationale/tradeoff.
3. Ask the user to reply with the option number or a custom answer.
4. Do not move forward until the decision is explicitly captured.

## Rule System

1. Use one extension dimension: rules.
   Profiles are an optional *selection mechanism* that compiles down to a concrete phase-by-phase rule matrix.
   The user-facing label for this artifact is "Effective Rule Matrix".
2. Infer execution context from request text, repository signals, and `AGENTS.md`.
   If available via enabled packs, use `profile-recommendations.md` as a deterministic mapping from inferred context to recommended profile selection.
3. In Scope, if the user asks to load/import/use/read/reuse matrix (file path or inline block), treat it as Effective Rule Matrix candidate input, then parse and validate it using `references/effective-matrix-reuse.md`.
   If valid, use it as the candidate matrix; if invalid or missing, continue with profile-driven compilation.
4. In Scope, if the user asks to load/import compiled/effective instructions (directory bundle or compact file; reference or portable), validate artifact format/content mode using `references/effective-instructions-reuse.md`, then ask user to accept, refresh, or discard it.
   If imported artifact includes `custom_instructions`, also ask whether to accept as-is, edit/rephrase, or discard custom instructions.
5. In Scope, propose profile selection (base + optional overlays) and show the Effective Rule Matrix (compiled phase-by-phase active rules) with a recommended baseline set or validated imported candidate.
   In markdown files, render it as a native markdown table with one row per phase; in the rules cell, use backticked rule ids separated by commas.
   In terminal/chat output, do not render a table; render only a plain-text phase list.
6. Ask user to accept or adjust the proposed profiles and/or Effective Rule Matrix before Explore.
7. Apply rules in this order:
   - core shared rules in `extensions/rules/*.md`
   - enabled pack rules from manifests under `skills/feature-driven-flow/packs/*/manifest.json` and optionally `.codex/feature-driven-flow/packs/*/manifest.json`
   - repository-local rules in `.codex/feature-driven-flow/rules/*.md` (when `local_rules.enabled=true`)
8. Matrix export behavior:
   - If `matrix_export.auto_generate_on_scope_confirmed=true`, auto-save confirmed Effective Rule Matrix after Scope confirmation.
   - If user asks to save/export current|active|chosen|choice|effective|compiled matrix, interpret it as export of the currently confirmed Effective Rule Matrix.
   - If user asks only for `state` or `compiled state`, ask a short clarification between Effective Rule Matrix export, Effective Instructions export, and `state.json` export.
   - Path resolution: explicit user path (when allowed) then `matrix_export.default_file`.
   - Relative paths are repo-root relative; absolute paths allowed only when `matrix_export.allow_absolute_path=true`.
   - Respect `matrix_export.overwrite_existing`; if overwrite is disallowed, ask user for alternative.
9. Effective Instructions export/convert behavior:
   - If `effective_instructions.export.auto_generate_on_scope_confirmed=true`, auto-save compiled instructions after Scope confirmation.
   - Support export as directory bundle (canonical) and compact file.
   - Support content mode `reference|portable|hybrid` from `effective_instructions.export.content_mode`.
   - For `portable` and `hybrid`, embed content for cross-environment portability and warn about size/sensitive data tradeoffs.
   - If `effective_instructions.export.allow_custom_instructions=true`, ask user whether to include custom instructions before export.
   - If custom instructions are included and `effective_instructions.export.require_custom_instructions_approval=true`, require explicit user approval before writing export files.
   - If `effective_instructions.export.require_all_custom_instruction_items_approved=true`, export only approved items; never include draft/rejected items.
   - If draft/rejected items exist, notify user and ask whether to improve/rephrase and approve, skip unapproved items, or cancel export.
   - Present numbered options: add new custom instruction(s), modify/rephrase current candidate(s), or skip custom instructions.
   - If `effective_instructions.export.allow_custom_instruction_rephrase=true`, you may suggest rephrased versions but user approval remains mandatory.
   - Persist approved custom instructions in artifact field `custom_instructions`.
   - If user asks to convert directory bundle <-> compact, use `tools/convert-effective-instructions.ps1`.
   - Path resolution and overwrite policy follow `effective_instructions.export.*`.
10. If rules disagree, ask user which direction to follow.
11. `AGENTS.md` policy constraints remain mandatory.

## Phase Skeleton

### Phase 1 Scope

1. Open a phase tracker for all seven phases.
2. Execute active Scope-phase rules.
3. Capture matrix candidate source (`file|inline|none`) and instructions candidate source (`bundle|compact|none`), validation results, and user-confirmed Effective Rule Matrix before Phase 2.
   Capture custom-instructions decision and approval state when instructions import/export is used.

### Phase 2 Explore

1. Execute active Explore-phase rules.

### Phase 3 Clarify

1. Execute active Clarify-phase rules.

### Phase 4 Architect

1. Execute active Architect-phase rules.

### Phase 5 Implement

1. Confirm explicit approval.
2. Execute active Implement-phase rules.

### Phase 6 Verify

1. Execute active Verify-phase rules.

### Phase 7 Summarize

1. Execute active Summarize-phase rules.
2. Close phase tracker.

## Output Templates

Use templates in:

1. `templates/clarifying-questions.md`
2. `templates/architecture-options.md`
3. `templates/review-report.md`
4. `templates/structured-phase-output.md`
5. `templates/execution-metrics.md`
6. `templates/rule-matrix-diff.md` (when rule matrix changes after Scope)
7. `templates/effective-instructions-bundle.manifest.json` (when exporting directory bundle)
8. `templates/effective-instructions-compact.json` (when exporting compact format)
9. Pack templates/references resolved from enabled pack manifests (for example quality/hardening/async-collab assets)
10. `extensions/rules/*.md`
11. `.codex/feature-driven-flow/rules/*.md` (when present)

## Tooling Expectations

1. Prefer fast file search and targeted reads.
2. Keep outputs concise but complete.
3. Enforce phase checkpoints through explicit outputs and decisions.

## Specialist Skills (Optional)

`fdf-code-explorer`, `fdf-implementation-planner`, and `fdf-change-auditor` are optional accelerators.

1. Prefer following active rules/templates directly.
2. Invoke specialist skills only when they materially reduce risk/ambiguity, or when explicitly requested by the user.

---
name: openspec-continue-change
description: Continue working on an OpenSpec change by creating the next artifact. Use when the user wants to progress their change, create the next artifact, or continue their workflow.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

**Project context preflight before workflow actions**: before this skill takes a workflow action, follow the `project-constitution` skill. Read root `CONSTITUTION.md` when present, enforce relevant project rules, stop on material conflicts, and follow the strict missing-constitution bootstrap/diagnostic policy. For architecture-sensitive work, also read `ARCHITECTURE.md`, `adr/README.md`, and relevant in-force `adr/*.md`. Read `.secrets.local.env` only when the current workflow actually needs a listed external system, and never reveal secret values.


**Artifact review session controls**: when `scripts/openspec-session-state` exists, inspect `artifactReview.decision` before key entry workflows create or consume reviewable artifacts. If the decision is `unset`, ask once whether to enable OpenAI-compatible artifact review for this session and record the answer with `--review on|off`; later commands reuse the recorded decision until the user changes it with the `/opsx:review-*` prompts. Session settings are non-secret local overlays and must not edit `.codex/openspec-artifact-review.json` unless the user explicitly asks for a global default change. Ordinary `scripts/openspec-artifact-review` runs use the session-effective config by default; explicit `--config` and `--raw-config` / `--ignore-session` bypass implicit session merge for diagnostics.

Continue working on a change by creating the next artifact.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**

   Run `openspec list --json` to get available changes sorted by most recently modified. Then use the **Codex interactive user question tool when available, otherwise a concise Markdown question** to let the user select which change to work on.

   Present the top 3-4 most recently modified changes as options, showing:
   - Change name
   - Schema (from `schema` field if present, otherwise "spec-driven")
   - Status (e.g., "0/5 tasks", "complete", "no tasks")
   - How recently it was modified (from `lastModified` field)

   Mark the most recently modified change as "(Recommended)" since it's likely what the user wants to continue.

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check current status**

   **Git preflight:** run `git status --short` before creating the next artifact. If dependency artifacts are modified but uncommitted, stop and recommend a checkpoint unless the user explicitly overrides the gate.
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand current state. The response includes:
   - `schemaName`: The workflow schema being used (e.g., "spec-driven")
   - `artifacts`: Array of artifacts with their status ("done", "ready", "blocked")
   - `isComplete`: Boolean indicating if all artifacts are complete

3. **Act based on status**:

   ---

   **If all artifacts are complete (`isComplete: true`)**:
   - Congratulate the user
   - Show final status including the schema used
   - Suggest: "All artifacts created! You can now implement this change or archive it."
   - STOP

   ---

   **If artifacts are ready to create** (status shows artifacts with `status: "ready"`):
   - Pick the FIRST artifact with `status: "ready"` from the status output
   - Get its instructions:
     ```bash
     openspec instructions <artifact-id> --change "<name>" --json
     ```
   - Parse the JSON. The key fields are:
     - `context`: Project background (constraints for you - do NOT include in output)
     - `rules`: Artifact-specific rules (constraints for you - do NOT include in output)
     - `template`: The structure to use for your output file
     - `instruction`: Schema-specific guidance
     - `outputPath`: Where to write the artifact
     - `dependencies`: Completed artifacts to read for context
   - **Create the artifact file**:
     - Read any completed dependency files for context
     - Use `template` as the structure - fill in its sections
     - Apply `context` and `rules` as constraints when writing - but do NOT copy them into the file
     - Write to the output path specified in instructions
   - Show what was created and what's now unlocked
   - **OpenAI-compatible artifact review (optional)**: if `scripts/openspec-artifact-review` and `.codex/openspec-artifact-review.json` exist, run `scripts/openspec-artifact-review --change "<name>" --stage "<artifact-id>" --config "<tmp-effective-config>"` after writing the artifact and before a dependent artifact consumes it. Exit `0` continues, exit `3` means skipped by disabled/unavailable policy, and exits `1`/`2` block until findings/config/errors are resolved or explicitly overridden. Do not read `.secrets.local.env` for this review.
   - After every reviewer command, parse the helper JSON output or persisted report and include a compact localized user-visible review status block; tool output alone is not sufficient. Run `scripts/openspec-artifact-review --cost-summary --change "<name>"` after reviewer calls when persisted reports/ledger may exist; totals must include retries/re-runs, not just the latest stage report.
   - The status block MUST be fully localized to the current chat language and wrapped between `---` separator lines. In Russian, use this compact shape: `Ревью артефакта — <stage>: <статус>.`, `Стоимость: <текущий вызов>, всего по изменению: <итого> / <N вызовов>, бюджет: <лимит>.`, `Замечания: критичных <N>, желательных <N>, предупреждений <N>, вопросов пользователю <N> — <итог>.` Do not use raw user-facing labels such as `Artifact Review`, `Findings`, `mustFix`, or `shouldFix` when the chat language is Russian.
   - Round displayed monetary amounts upward to the currency minor unit; for RUB, round upward to kopecks and display with the chat-language decimal convention, e.g. `0.81953034 ₽` -> `0,82 ₽`. Preserve raw cost precision in JSON reports.
   - Record or verify a formal finding disposition for every mustFix, actionable shouldFix, warning, and question: `fixed`, `deferred` to a concrete artifact/file/section/task, `non_actionable` with reason, or `user_blocked`. Print individual findings only when user participation is required.
   - Before checkpointing or letting a dependent artifact consume the result, ensure every mustFix, actionable shouldFix, warning, and question is handled by fixing, deferring to a concrete place, marking non-actionable with reason, or asking the user as a blocker. Do not checkpoint while any artifact reviewer finding is unhandled.
   - STOP after creating ONE artifact

   ---

   **If no artifacts are ready (all blocked)**:
   - This shouldn't happen with a valid schema
   - Show status and suggest checking for issues

4. **After creating an artifact, show progress**
   ```bash
   openspec status --change "<name>"
   ```
   Then run `git status --short`, show the changed artifact files, and checkpoint according to session git mode before another artifact depends on this one. In automatic mode, use `scripts/openspec-git-checkpoint` when available; in manual mode, request approval.

**Output**

After each invocation, show:
- Which artifact was created
- Schema workflow being used
- Current progress (N/M complete)
- What artifacts are now unlocked
- Prompt: "Want to continue? Just ask me to continue or tell me what to do next."

**Intent-Driven Support Skill Policy**

- For `grill` and `design-review`, run `grill-with-docs` automatically. Do not ask whether to run grill at those gates; ask one material question at a time only when repository context cannot resolve it.
- For specs, use `gherkin-authoring` guidance and preserve OpenSpec Markdown as the source of truth.
- For design, use `c4-diagrams` when boundaries/integrations are non-trivial; otherwise write an explicit no-diagram rationale.
- For ADR review, use `architectural-decision-records` after `design-review.md`; durable ADRs under top-level `adr/` are append-only and superseded by new ADRs, not rewritten.
- For `test-plan`, use the project-local `tdd` skill to define vertical RED/GREEN/REFACTOR slices before tasks.

**Artifact Creation Guidelines**

The artifact types and their purpose depend on the schema. Use the `instruction` field from the instructions output to understand what to create.

Common artifact patterns:

**spec-driven schema** (proposal → specs → design → tasks):
- **proposal.md**: Ask user about the change if not clear. Fill in Why, What Changes, Capabilities, Impact.
  - The Capabilities section is critical - each capability listed will need a spec file.
- **specs/<capability>/spec.md**: Create one spec per capability listed in the proposal's Capabilities section (use the capability name, not the change name).
- **design.md**: Document technical decisions, architecture, and implementation approach.
- **tasks.md**: Break down implementation into checkboxed tasks.

For other schemas, follow the `instruction` field from the CLI output.

**Guardrails**
- Checkpoint after the created artifact. Safe lifecycle checkpoint commits are automatic by default in session git `auto` mode; manual mode stops for approval. Merge, push, archive, destructive operations, and hard-gate bypasses still require explicit approval.
- A checkpoint override is one-time, must identify the uncommitted files/gate being bypassed, and must be repeated in the output.
- Create ONE artifact per invocation
- Always read dependency artifacts before creating a new one
- Never skip artifacts or create out of order
- If context is unclear, ask the user before creating
- Verify the artifact file exists after writing before marking progress
- Use the schema's artifact sequence, don't assume specific artifact names
- **IMPORTANT**: `context` and `rules` are constraints for YOU, not content for the file
  - Do NOT copy `<context>`, `<rules>`, `<project_context>` blocks into the artifact
  - These guide what you write, but should never appear in the output

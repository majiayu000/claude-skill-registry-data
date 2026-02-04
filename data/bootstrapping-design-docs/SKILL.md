---
name: bootstrapping-design-docs
description: Creates design document infrastructure including templates, workflows, and a specific design doc skill. Use when setting up design docs for a new project or when the user mentions "bootstrapping-design-docs".
---

<NOTE>
Use the $activate-memories skill if you have not already to get an overview of the project before proceeding.
</NOTE>
<objective>
1. If the `design-docs` folder does not already exist, create a repo-local `design-docs/` workspace (templates + active docs + index).
  - If the `design-docs` folder already exists, stop and ask the user how to proceed.
2. Create a **project-specific** design doc template. If the user does not specify a specific type of design doc they want to create, we will be creating a general design document template called `base-design-doc.md` for the overall project.
3. Generate a **project-specific** design-doc skill for authoring design docs with:
   - explicit specs (interfaces, signatures, types)
   - mandatory test-data acquisition plan for ETL / HTTP / WebSocket work
   - enforceable guardrails against common agent failure modes
   - Example: The user wants to make a design doc skill for the ETL pipeline creations in the project. Then your task would be to create a `$etl-design-doc` skill.
4. Support repeated runs to create additional templates (variants) without breaking existing docs.

For the rest of this document `{DESIGN_DOC_SKILL_NAME}` will refer to the name of the skill we will make that will later be used to generate design docs for this project. Default: `creating-design-doc`.
Once you create the base design doc template and skill, you must ask questions to the user to help clarify anything you are unsure of.
This is a **joint user-agent process**: ask targeted questions when unsure; do not finalize templates without user review.
</objective>

<outputs>
Create (idempotent; do not overwrite without preserving history):

<file_list>
- `design-docs/README.md` - How design docs are written, reviewed, and used for delegated execution.
- `design-docs/active/` - Directory for active design documents.
- `design-docs/agents/` - Directory for agent-executable XML subtasks.
- `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/SKILL.md` - The generated `${DESIGN_DOC_SKILL_NAME}` skill.
- `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/README.md` - Lists available templates and when to use them.
- `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/base.md` - Meta "base" design doc template (guardrails + structure).
- `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/<variant>.md` - Project-specific templates (e.g., `etl-pipeline.md`, `feature.md`).
</file_list>

**Note**: Templates are bundled with the skill (not in `design-docs/`) per Agent Skills progressive disclosure pattern.

<output_format>
**Design docs are written in markdown** - not XML. Markdown is easier for humans to read/edit and for agents to parse during collaboration. Agent-executable subtasks use XML in a separate file under `design-docs/agents/`.
</output_format>

<agent_name_resolution>
Replace `{AGENT_NAME}` with the agent's config directory:
- `.aider/` - Aider
- `.claude/` - Claude Code
- `.codex/` - OpenAI Codex CLI
- `.copilot/` - GitHub Copilot
- `.cursor/` - Cursor

If the repo has an existing agent config directory, use it. If multiple exist, prefer the current agent's. If none exist, create one.
</agent_name_resolution>
</outputs>

<preconditions>
Before asking questions, scan the repo to ground defaults:
If you have not already, run the $activating-memories skill to get an overview of the project.
<scan_targets>
1. **Languages/frameworks/build files**
2. **CI entrypoints**
3. **Project Specific Utility modules**
4. **DB/migrations**
5. **Style rules**
</scan_targets>
</preconditions>

<generation_steps>
1. **Create folder structure** (if missing):
   - `design-docs/`
   - `design-docs/active/`
   - `design-docs/agents/`
   - `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/`
   - `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/`

2. **Write design doc skill and bundled templates**:
   - `design-docs/README.md` (workflow + approvals)
   - `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/SKILL.md` (the skill)
   - `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/README.md` (template index)
   - `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/base.md` (meta template with guardrails)
   - `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/skill.md` (skill creation template)
   - `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/feature.md` (feature template)
3. **Run Adaptive Questioning Protocol**:
   - Produce "Detected Defaults Summary"
   - Ask triggered questions
   - Stop for answers before proceeding

4. **Idempotency**:
   - Never overwrite existing templates without timestamped backup
   - Add new variants to `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/README.md`
</generation_steps>


<questioning_protocol>
Ask only questions that materially influence template contents.

<question_tags>
Every question must be tagged:
- `[blocking]` - must be answered to generate correct template or enforce safety
- `[important]` - significantly improves template quality / reduces future rework
- `[optional]` - preference-level; safe defaults exist
</question_tags>

<question_budget>
- Max 10 questions total.
- Each question includes a one-line "why" tying to a template section, guardrail, or convention.
</question_budget>

<triggered_questions>
Ask only what applies based on scan:
- Migrations tooling detected -> ask DB reset/backfill/rollback/testing policy
- HTTP/WS dependencies detected -> ask record/replay + fixture storage constraints
- Monorepo structure detected -> ask where templates live and how commands differ
- No tests/CI detected -> ask what canonical verification commands should be
</triggered_questions>

<template_delta_preview>
Before writing files, show:
- Which variants will be created
- Repo-specific defaults that will be baked in
- Any tightened guardrails derived from project norms
- Any unresolved `[blocking]` items

Stop and ask for `[blocking]` answers before proceeding.
</template_delta_preview>
</questioning_protocol>

<common_questions>
Ask only what you cannot infer from the scan:
<question_examples>
1. `[blocking]` **Template variants desired**
   - "Which templates do you want generated? (e.g., `feature`, `etl_http_ws`, `db_migration`, `refactor`)"
   - Why: determines templates bundled with skill.

2. `[blocking]` **Test integrity policy**
   - "What is your rule on mocks? (only mock boundaries; prefer record/replay; never mock core transforms)"
   - Why: populates guardrails + testing strategy.

3. `[blocking]` **Data capture constraints**
   - "Can we store captured payloads under `tests/fixtures/`? Any size/licensing/PII constraints?"
   - Why: populates test-data acquisition plan.

4. `[blocking]` **Destructive actions boundary**
   - "What DB reset patterns are allowed in tests? (transactions/temp schema/containers). Forbidden actions?"
   - Why: prevents unsafe "delete DB to pass tests" behavior.

5. `[important]` **Type discipline**
   - "For Python projects, what is your stance on Optional/None? (forbid unless justified; require invalid states unrepresentable)"
   - Why: shapes interface-contract requirements.

6. `[important]` **Review workflow**
   - "Stop at Template Delta Preview for approval, or write files and you review diffs?"
   - Why: controls collaboration checkpoint.
</question_examples>
</common_questions>

<base_template_sections>
The base template MUST include these sections (in order):

1. Identity and lifecycle
2. Context
3. Problem
4. Goals / Non-goals
5. Requirements (FRs / NFRs)
6. Constraints and invariants (include DB + test integrity)
7. Proposed design (architecture, contracts, schemas, idempotency/retries)
8. Project common utilities that will be used.
9. Project common utilities that will be created.
10. Interface contracts (explicit signatures; Optional/None justification required)
11. Alternatives considered (>=2)
12. Test data acquisition plan (mandatory for external I/O / ETL)
13. Testing and verification strategy (commands + CI gates + test integrity rules)
14. Rollout / migration / ops (flags, backfills, observability, runbook)
15. Open questions / follow-ups
16. **Subtasks** (human-readable checklist for review)

**Subtasks Section Format**:
```markdown
## Subtasks

### T1: [Task Title]
- **Summary**: One sentence objective
- **Scope**: What's in / what's out
- **Acceptance**: Binary pass/fail criteria
- **Status**: [ ] Not started / [~] In progress / [x] Complete

### T2: [Task Title]
...
```
</base_template_sections>

<guardrails>
Include verbatim in the design doc skill you create under "Engineering Guardrails for Agent Execution":

- **Reuse-first rule** (anti-duplication): search existing utilities; record decision per task.
- **No destructive shortcuts**: never delete dev/prod data to pass tests; destructive actions require confirmation.
- **Test integrity** (anti-mock-cheating): mock boundaries only; prefer record/replay; do not change tests without spec change approval.
- **Signature discipline** (anti-vagueness): explicit types/invariants; Optional/None requires justification and handling strategy.
- **Alternatives requirement**: evaluate >=2 alternatives + "do nothing".
- **Uncertainty protocol**: ask `[blocking]` questions when unsure; do not proceed.
</guardrails>


<completion_criteria>
- `design-docs/` exists with README + `active/` + `agents/` subdirectories
- name of ${DESIGN_DOC_SKILL_NAME} confirmed with user.
- `${DESIGN_DOC_SKILL_NAME}` skill exists at `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/`
- Templates bundled at `.{AGENT_NAME}/skills/{DESIGN_DOC_SKILL_NAME}/templates/`
- `base.md` includes guardrails and human-readable subtasks section format
- At least one project-specific template variant exists with repo-specific test commands
- Skill workflow: human-readable subtasks in main doc -> user approval -> XML in `design-docs/agents/`
</completion_criteria>

<decision_points>
- No existing config directory -> create one for current agent
- Multiple templates requested -> generate each as separate variant file
- User wants immediate write vs preview -> honor preference from question 6
</decision_points>

<failure_modes>
- Scan finds nothing -> ask user for stack/commands explicitly
- Conflicting conventions -> note in template as "resolve before use"
- Overwriting existing templates -> create backup with timestamp first
</failure_modes>

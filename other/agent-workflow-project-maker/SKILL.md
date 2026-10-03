---
name: agent-workflow-project-maker
description: Use the repo's real-world workflow catalog to turn a repeated job into a Codex/ECC project skill with input contracts, output artifacts, schemas, validators, and tracking. Use when the user asks for an agent workflow project maker, workflow catalog, workflow finder, real-world agent workflow examples, reusable project creation, or converting a vague project idea into a tracked skill.
---

# Agent Workflow Project Maker

This skill owns the workflow-catalog/project-maker surface in this repo. It
should be treated as a real project surface, not as loose research output.

## Skills-First Chat Contract

Contract phrase: Skills are the operator interface. Codex chat is the operator surface. The user never runs tracker scripts; scripts are internal adapters.

Skills are the operator interface. Codex chat is the operator surface. The user
never runs tracker scripts; scripts are internal adapters that Codex may invoke
to create durable state, load context, validate gates, or inspect workflow
status.

Plain chat is the primary trigger. Treat these user messages as workflow intake
signals:

- "I am building a workflow"
- "I found a bug in my workflow"
- "create a workflow"
- "continue this workflow"
- "I will make an edit to my earthquake project"
- "I need to update/fix/change this project"

When one of these intents appears, do not present a terminal command. Load ECC,
load this skill and the relevant project/workflow context, create or lock the
tracker run internally, write the context manifest internally, then answer with
the ECC proof, premise lock, and first context-aware grilling question.
If tracker command capability is needed, use the skills-owned callable command
suite documented by `skills/control-repo-manager/SKILL.md`; do not invent a new
operator-facing command surface.

Any edit, change, fix, update, revise, work-on, or touch intent for a tracked
project, lane, skill, or workflow counts as a workflow start. Do not ask "what
edit are you planning?" until the tracked skill run exists and the context
manifest is attached.
Create or lock tracker state before asking what the edit is.

Contract phrase: create or lock the tracker run internally.

## Owned Surfaces

- Catalog data: `data/agentic-repos/`
- Main index: `data/agentic-repos/workflow-search-index.json`
- Domain index: `data/agentic-repos/workflow-search-index-by-domain.json`
- Human reports: `reports/workflow-*.md`

The current catalog says it is a lookup layer for real-world workflow patterns
and Codex/ECC config-package references. Use that as the starting point.

## Workflow

1. Name the repeated real-world job.
2. Query the catalog by reading the committed JSON indexes directly.
3. Inspect only the relevant catalog rows and source references.
4. Draft the project contract:
   - trigger and refusal scope;
   - input contract;
   - output artifact;
   - source/tool lanes;
   - raw evidence surface;
   - validation loop;
   - safety boundary.
5. Create or update a project skill under `skills/<project-slug>/SKILL.md`.
6. Add schemas, fixtures, examples, and validators only after the contract is
   clear.
7. Update `data/project-surface-inventory.json` so the new project is tracked.

## Workflow Intake Router

For workflow bugs, workflow problems, continuations, and new workflow requests,
do not jump directly to implementation. Start from ECC-loaded workflow intake.

Required sequence:

1. Create or lock a tracked workflow run immediately.
2. Record `skill_id` and `skill_path` for the repo skill being built or
   operated.
3. Set the first phase to `workflow_intake`.
4. Load ECC, Matt Pocock flow, tracker status, workflow-specific skill files,
   status/handoff docs, tests, validators, and relevant workflow-run logs.
5. If the report names ECC concepts such as loop, gate, lane, eval, handoff,
   source evidence, or human boundary, load the local docs for that concept.
6. Write or attach a context manifest under `ops/workflow-runs/`.
7. Immediately checkpoint the run from `workflow_intake` to `grilling`.
   The first context-aware question is a grilling question, so the tracker must
   record `current_skill=grilling` before asking the user.
8. Show visible ECC proof before grilling:
   - ECC files loaded;
   - workflow/concept files loaded;
   - ECC concept meaning from the loaded files;
   - repo skill being built or operated;
   - premise lock;
   - first context-aware grilling question.
9. Grill only after the loaded-context proof exists.

While the run is in `grilling`, ask one question at a time and wait for the
answer. A user answer to the first grilling question does not authorize
implementation. Continue grilling until the user explicitly confirms shared
understanding or asks to move to PRD, issues, implementation, or code review.

Do not ask blank questions. Do not rely on generic Codex assumptions about
agentic workflows. ECC is the operating model.

Fail-closed enforcement lives in the internal tracker validation adapter. Every
workflow run must have a repo skill identity via `skill_id` and `skill_path`.
Workflow runs in `workflow_intake`, and all `workflow_specific_bug` runs, must
also have a context manifest under `ops/workflow-runs/` with loaded ECC context
and a premise marker. If skill identity or context proof is missing, tracker
validation must fail before the session can be treated as safe to continue,
close, or upload.
Active workflow-intake runs with context manifests must not remain in
`workflow_intake`. If validation reports that intake must checkpoint to
`grilling`, update the run phase before continuing the conversation.

New workflow creation requires explicit confirmation, such as:

- "Create a new workflow for this"
- "This is not a continuation. Start a new workflow."

After explicit confirmation, create the draft scaffold immediately:

- `skills/<workflow-slug>/SKILL.md`
- `data/<workflow-slug>/.gitkeep`
- `docs/status/YYYY-MM-DD-<workflow-slug>-status.md`
- `ops/workflow-runs/YYYY-MM-DD/<workflow-run-id>-context.md`

Draft scaffold files must include visible progress markers, current phase, next
action, and explicit "Not reached yet" markers for untouched sections.

## Rules

- Do not create placeholder projects. If the repeated job is vague, ask for the
  missing job before writing project files.
- Do not treat generated catalog rows as verified truth. Inspect source URLs or
  mark the row as needing verification.
- Keep runtime/platform examples as references unless the user explicitly
  chooses that runtime.
- Keep Codex/ECC as the operating surface. External repos are references or
  adapters, not the project brain.
- Never add a project to README or AGENTS.md unless it has a skill, owned paths,
  and inventory entry.

## Output Contract

For a new project, produce:

- `skills/<project-slug>/SKILL.md`;
- `data/<project-slug>/` for schemas, fixtures, examples, and raw evidence;
- optional Node validation command in `scripts/control-repo.mjs`;
- `docs/status/YYYY-MM-DD-<project-slug>-status.md`;
- inventory entry in `data/project-surface-inventory.json`.

When the user only wants ideation, stop at a project contract draft and do not
create files.

## Slash Compatibility Surface

`skills/` remains canonical. Slash names are compatibility metadata only; they
are not the operator interface and they must not be presented as something the
user has to run. The compatibility entries are documented in
`skills/agent-workflow-project-maker/commands.md`; there is no Python slash
registry for this surface.

- `/tracker workflow`
- `/tracker status`
- `/tracker closeout`
- `/workflow-find`
- `/workflow-router`
- `/workflow-contract`
- `/workflow-create-skill`
- `/workflow-status`
- `/workflow-closeout`

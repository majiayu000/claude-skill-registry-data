---
name: bmad-autonomous-planning
description: Creates the full BMAD planning artifact chain (research, brief, PRD, architecture, epics/stories, readiness) autonomously from a short task description or GitHub issue, delegating each planning phase to a focused subagent and orchestrating the handoffs without human interaction. Use when /sdlc-plan runs stage 2 of the SDLC loop, or when the user wants BMAD-style planning from a short prompt without walking through interactive menus.
---

# BMAD Autonomous Planning

## Profile keys consumed

- `project.name`, `project.repo`
- `php.version`
- `framework.name`, `framework.api_platform`
- `persistence.mapper`, `persistence.engine`
- `architecture.source_root`, `architecture.bounded_contexts`, `architecture.shared_context`
- `quality.phpinsights.complexity`, `quality.infection_msi`

This skill invokes no `make.*` targets: the planning flow runs entirely in
the current AI session. Quality thresholds appear in planning artifacts only
as the profile's `quality.*` values, which are raise-only floors (shipped
defaults: complexity `94` via `quality.phpinsights.complexity`, MSI `100`
via `quality.infection_msi`) — a plan may tighten them, never relax them.

## Non-Negotiable Rules

- Run the planning flow in the current AI session. Do not depend on
  repo-local bash wrappers, Make targets, or other launcher automation.
- Use BMAD as the primary process surface: start from `_bmad/COMMANDS.md`
  (and the repository's local bmalph skill wrapper when one exists), frame
  every subagent around a BMAD command name from that catalog, and only
  descend into the specific workflow or agent files required by that
  command.
- Spawn one focused subagent per BMAD planning stage when subagents are
  available. Do not overload a single subagent with the whole planning flow.
- Spawn planning and validation subagents with the strongest available
  model in the current platform, at the highest reasoning effort the
  platform supports. Do not downshift stage-owning subagents to a smaller
  or faster model.
- The main agent is the user surrogate. If a BMAD workflow asks for
  approval, choices, or clarification, decide on the user's behalf,
  continue, and record the decision inline in the artifact as
  `> Assumption: <decision and rationale>` instead of blocking.
- Do not implement production code during this skill. Produce specs only.
- Plans must preserve the root-cause culture: never propose lowering a
  `quality.*` threshold, adding suppression annotations, or editing
  `deptrac.yaml` — plan the code change that meets the bar instead.

## Inputs

Expect the caller to provide:

- a short task description, or a GitHub issue (URL) whose title, problem
  statement, and acceptance criteria seed the chain — resolve it with
  `gh issue view <url> --json url,number,title,body`
- an optional bundle id or target bundle directory
- an optional validation round limit from `1` to `3`
- optional GitHub issue or specs-only PR output requirements

Bundle directory resolution:

- When invoked from `/sdlc-plan` (or any caller that supplies an issue),
  use `specs/<slug>/`, where `<slug>` is the kebab-case issue title
  prefixed with the issue number (e.g. `specs/42-currency-crud/`).
- Otherwise derive one under the BMAD-configured planning artifacts path,
  for example `<planning_artifacts>/autonomous/<timestamp>-<task-slug>`.

## Output Bundle

Create a planning bundle with at least these artifacts, in chain order:

- `research.md`
- `brief.md` (plus `brief-distillate.md` when it adds value)
- `prd.md`
- `architecture.md`
- `epics-stories.md`
- `readiness.md` — implementation-readiness verdict, an explicit
  PASS/FAIL with named findings
- `run-summary.md`

Cross-references must stay consistent: each artifact links its
predecessors, and no artifact contradicts an upstream decision.

`run-summary.md` must also contain:

- the chosen bundle directory
- a `Subagent Execution Log` section listing the phase, BMAD command, and
  artifact owned by each subagent
- the validation rounds used per artifact
- open questions, warnings, blockers, and the recommended next step

The final assistant response should summarize:

- bundle directory (so a calling command such as `/sdlc-plan` can emit its
  `SPECS_DIR:` handle)
- artifact paths
- validation rounds used
- remaining open questions or warnings
- GitHub issue/PR status when requested

## Required Sources

Load only the minimum sources required for the current stage:

1. `_bmad/COMMANDS.md`
2. The repository's local bmalph skill wrapper, when one exists (check the
   repo's agent-skills directories for a `bmad`/`bmalph` skill)
3. The resolved BMAD config file:
   - `_bmad/config.yaml` when present
   - otherwise `_bmad/bmm/config.yaml`
   - if both exist, treat `_bmad/bmm/config.yaml` as optional upstream context
4. Only the backing agent and workflow files required to satisfy the BMAD
   commands selected for this run:
   - `analyst`
     - `_bmad/bmm/agents/analyst.agent.yaml`
   - `create-brief`
     - `_bmad/bmm/workflows/1-analysis/bmad-create-product-brief/workflow.md`
     - `_bmad/bmm/workflows/1-analysis/bmad-create-product-brief/steps/step-01-init.md`
   - `create-prd`
     - `_bmad/bmm/agents/pm.agent.yaml`
     - `_bmad/core/tasks/bmad-create-prd/workflow.md`
     - `_bmad/core/tasks/bmad-create-prd/steps-c/step-01-init.md`
   - `create-architecture`
     - `_bmad/bmm/agents/architect.agent.yaml`
     - `_bmad/bmm/workflows/3-solutioning/bmad-create-architecture/workflow.md`
     - `_bmad/bmm/workflows/3-solutioning/bmad-create-architecture/steps/step-01-init.md`
   - `create-epics-stories`
     - `_bmad/bmm/workflows/3-solutioning/bmad-create-epics-and-stories/workflow.md`
     - `_bmad/bmm/workflows/3-solutioning/bmad-create-epics-and-stories/steps/step-01-validate-prerequisites.md`
   - `implementation-readiness`
     - `_bmad/bmm/workflows/3-solutioning/bmad-check-implementation-readiness/workflow.md`
     - `_bmad/bmm/workflows/3-solutioning/bmad-check-implementation-readiness/steps/step-01-document-discovery.md`
5. Repository guidance that constrains implementation: the project profile
   (`.claude/php-sdlc.yml`), agent guidance files (`CLAUDE.md`,
   `AGENTS.md`), and the repository's architecture/onboarding/developer
   docs where they exist
6. Only the feature-area code and docs needed to justify the plan — infer
   likely paths from `architecture.source_root` and
   `architecture.bounded_contexts`

Never bulk-scan the whole repository when a narrow set of files will do.

## Stage-to-Command Map

Use these BMAD commands as the default stage entrypoints for autonomous
planning subagents:

- research: `analyst`
- product brief: `create-brief`
- PRD: `create-prd`
- architecture: `create-architecture`
- epics and stories: `create-epics-stories`
- implementation readiness: `implementation-readiness`

When a validation round needs another subagent pass, prefer the matching
validation command when it exists, for example `validate-brief`,
`validate-prd`, `validate-architecture`, or `validate-epics-stories`.

## Main-Agent Responsibilities

The main agent owns orchestration and artifact quality. It must:

1. Resolve the bundle path and initialize the planning run.
2. Map each stage to a concrete BMAD command before spawning a subagent.
3. Decide which repository files each subagent needs.
4. Spawn the stage subagent with the strongest available model at the
   highest supported reasoning effort, and only the minimum context
   required.
5. Review the returned draft before moving to the next stage.
6. Answer workflow questions on behalf of the user, recording each as an
   inline `> Assumption:`.
7. Decide whether another validation round is necessary.
8. Maintain continuity across stages so the next subagent sees the correct
   upstream artifact set.
9. Update the `Subagent Execution Log` in `run-summary.md` after every phase.

## Subagent Contract

For every BMAD stage, the main agent should hand the subagent:

- the specific BMAD command(s) from `_bmad/COMMANDS.md` it must execute
- the required runtime override: the strongest available model in the
  current platform, at the highest reasoning effort it supports
- only the backing workflow or agent files needed to fulfill those commands
- the current task framing
- only the upstream artifacts required for that stage
- only the repository files needed for evidence
- a clear output contract:
  - artifact draft content
  - key assumptions made
  - unresolved questions
  - validation findings or concerns

Every subagent should return a draft plus findings, not a request to pause
for a human.

Do not hand a subagent only raw workflow-file paths without naming the
BMAD command it is following.

## Workflow

### 1. Preflight

- Resolve the BMAD config and planning artifacts directory.
- Create the bundle directory if needed.
- Read the local bmalph skill wrapper (when present) and
  `_bmad/COMMANDS.md`, then map the BMAD stage commands relevant to this
  planning run.
- Infer the most likely feature-area paths from the task description and
  the profile's `architecture.bounded_contexts` before any broad
  discovery.
- Write a short task framing section into `run-summary.md`.

### 2. Research Stage

Spawn a research subagent through the `analyst` BMAD command.

The research subagent should:

- inspect the most relevant docs and code paths
- summarize current-state behavior and constraints
- identify implementation risks and likely surface area
- return a draft for `research.md`

The main agent then reviews the result, resolves open choices, and
finalizes `research.md`.

### 3. Product Brief Stage

Spawn a brief subagent through the `create-brief` BMAD command.

Inputs:

- task description (or resolved issue)
- `research.md`
- only the command entry and backing files needed for `create-brief`

Outputs:

- draft `brief.md`
- optional `brief-distillate.md`
- explicit gaps, risks, and questions

The main agent must review the draft before moving on.

### 4. PRD Stage

Spawn a PRD subagent through the `create-prd` BMAD command.

Inputs:

- `research.md`
- `brief.md`
- `brief-distillate.md` when present

The PRD subagent should produce an implementation-ready but not code-level
`prd.md`, with the issue's acceptance criteria traced into FRs. Quality
NFRs must cite the profile's `quality.*` values as raise-only floors —
never a lowered target. The main agent validates coverage, measurability,
traceability, and completeness before proceeding.

### 5. Architecture Stage

Spawn an architecture subagent through the `create-architecture` BMAD
command.

Inputs:

- `research.md`
- `prd.md`
- repository architecture guidance and relevant feature-area code

The architecture must fit the repository's actual stack and patterns as
declared by the profile: `php.version`, `framework.name` (and
`framework.api_platform` when set), `persistence.mapper` /
`persistence.engine`, and the layered/bounded-context layout under
`architecture.source_root` with `architecture.bounded_contexts` and
`architecture.shared_context`.

```text # profile-example
# Reference-service fit statement derived from the profile:
# Symfony + API Platform service on doctrine-odm/mongodb, contexts
# [User, OAuth] plus shared kernel "Shared" under src/ — the plan must
# slot new components into those contexts, not invent new top-level dirs.
```

The main agent validates compatibility and implementation readiness before
moving on. If the PRD is not strong enough, do not improvise; send the
flow back to PRD refinement first.

### 6. Epics and Stories Stage

Spawn an epics/stories subagent through the `create-epics-stories` BMAD
command.

Inputs:

- `prd.md`
- `architecture.md`
- relevant constraints from `research.md`

The subagent should produce forward-safe epics and actionable stories in
`epics-stories.md`, each story marked independent or dependent (the
parallel-dispatch input for the implementation stage). The main agent
separately reviews story quality, dependency order, and
acceptance-criteria coverage.

### 7. Cross-Artifact Readiness Stage

Spawn a readiness subagent through the `implementation-readiness` BMAD
command.

Inputs:

- `brief.md`
- `prd.md`
- `architecture.md`
- `epics-stories.md`

This subagent should identify gaps, inconsistencies, and unresolved
planning risks in `readiness.md`, ending in an explicit PASS/FAIL verdict
with named findings (the artifacts each finding implicates). The main
agent finalizes the readiness assessment and updates `run-summary.md`. On
FAIL, correct the named artifacts and re-run readiness — the calling
command bounds this loop.

## Validation Loop

Use `1` to `3` validation rounds per artifact.

For each artifact, the main agent may:

- accept the draft
- revise it directly
- spawn a reviewer subagent for another pass, preferably using the
  matching BMAD validation command when one exists and keeping the
  strongest-available-model override

Stop early when only minor or repetitive issues remain. Do not loop
endlessly.

## Decision Policy for Interactive BMAD Gates

If a BMAD wrapper or workflow expects user input:

- continue without asking the human — zero interactive prompts anywhere in
  the chain; never use AskUserQuestion, never wait for confirmation
- choose the best option based on task intent and repository evidence, and
  record it inline as `> Assumption: <decision and rationale>`
- prefer another review round when uncertainty is material
- record unresolved concerns in `run-summary.md` and `readiness.md`

If a phase is blocked by a genuinely missing prerequisite, stop only that
phase, record the blocker explicitly, and do not fabricate the missing
input.

Use the BMAD menu concepts as policy, not as a hard stop:

- deeper review when the artifact is still weak
- extra perspective when another subagent is likely to add signal
- continue when the artifact is ready enough for the next stage

## GitHub Output

Only create a GitHub issue or specs-only PR when the user explicitly asks.

When requested:

- finish the planning bundle first
- create GitHub side effects only after the artifacts are stable, against
  `project.repo`
- prefer GitHub app tools when available
- fall back to `gh` only when necessary
- record failures as warnings instead of discarding the planning bundle

## Related Skills

- [bmad-fr-nfr-review-gate](../bmad-fr-nfr-review-gate/SKILL.md) — the
  post-implementation counterpart: verifies the implemented change against
  the specs this skill produces
- [quality-standards](../quality-standards/SKILL.md) — the protected
  `quality.*` thresholds that PRD and architecture NFRs must restate
- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md)
  — the layer and pattern rules architecture plans must fit

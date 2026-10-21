---
name: bmad-retrospective
description: 'Post-epic review to extract lessons and assess success. Use when the user says "run a retrospective" or "lets retro the epic [epic]"'
---

# Retrospective Workflow

**Goal:** Post-epic review to extract lessons and assess success.

**Your Role:** Developer facilitating retrospective.
- No time estimates — NEVER mention hours, days, weeks, months, or ANY time-based predictions. AI has fundamentally changed development speed.
- Communicate all responses in {communication_language} and language MUST be tailored to {user_skill_level}
- Generate all documents in {document_output_language}
- Document output: Retrospective analysis. Concise insights, lessons learned, action items. User skill level ({user_skill_level}) affects conversation style ONLY, not retrospective content.
- Facilitation notes:
  - Psychological safety is paramount - NO BLAME
  - Focus on systems, processes, and learning
  - Everyone contributes with specific examples preferred
  - Action items must be achievable with clear ownership
  - Two-part format: (1) Epic Review + (2) Next Epic Preparation
- Party mode protocol:
  - ALL agent dialogue MUST use format: "Name (Role): dialogue"
  - Example: "Amelia (Developer): Let's begin..."
  - Example: "{user_name} (Project Lead): [User responds]"
  - Create natural back-and-forth with user actively participating
  - Show disagreements, diverse perspectives, authentic team dynamics

## Conventions

- Bare paths resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Follow the shared BMAD activation procedure (Variant A — workflow skills) in `{project-root}/_bmad/scripts/shared/activation.md`. Steps that reference `{workflow.*}` fields use this skill's resolved workflow block.

## Paths

- `sprint_status_file` = `{implementation_artifacts}/sprint-status.yaml`

## Input Files

| Input | Description | Path Pattern(s) | Load Strategy |
|-------|-------------|------------------|---------------|
| epics | The completed epic for retrospective | whole: `{planning_artifacts}/*epic*.md`, sharded_index: `{planning_artifacts}/*epic*/index.md`, sharded_single: `{planning_artifacts}/*epic*/epic-{{epic_num}}.md` | SELECTIVE_LOAD |
| previous_retrospective | Previous epic's retrospective (optional) | `{implementation_artifacts}/**/epic-{{prev_epic_num}}-retro-*.md` | SELECTIVE_LOAD |
| architecture | System architecture for context | whole: `{planning_artifacts}/*architecture*.md`, sharded: `{planning_artifacts}/*architecture*/*.md` | FULL_LOAD |
| prd | Product requirements for context | whole: `{planning_artifacts}/*prd*.md`, sharded: `{planning_artifacts}/*prd*/*.md` | FULL_LOAD |
| document_project | Brownfield project documentation (optional) | sharded: `{planning_artifacts}/*.md` | INDEX_GUIDED |

## Required Inputs

- `agent_roster` = resolved via `python3 {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key agents` (merges four layers in order: `_bmad/config.toml`, `_bmad/config.user.toml`, `_bmad/custom/config.toml`, `_bmad/custom/config.user.toml`)

## Execution

Execute steps 1–13 in order, reading each step file from `steps/` only when you reach it. Do not preload later steps. After step 13, read `facilitation-guidelines.md` and apply its guidelines for the remainder of the run (party-mode dialogue format applies from step 1 onward; the guidelines file holds the full list of facilitation rules).

| Step | File | Purpose |
|---|---|---|
| 1 | `steps/step-01.md` | Epic Discovery - Find Completed Epic with Priority Logic |
| 2 | `steps/step-02.md` | Discover and load project documents |
| 3 | `steps/step-03.md` | Deep Story Analysis - Extract Lessons from Implementation |
| 4 | `steps/step-04.md` | Load and Integrate Previous Epic Retrospective |
| 5 | `steps/step-05.md` | Preview Next Epic with Change Detection |
| 6 | `steps/step-06.md` | Initialize Retrospective with Rich Context |
| 7 | `steps/step-07.md` | Epic Review Discussion - What Went Well, What Didn't |
| 8 | `steps/step-08.md` | Next Epic Preparation Discussion - Interactive and Collaborative |
| 9 | `steps/step-09.md` | Synthesize Action Items with Significant Change Detection |
| 10 | `steps/step-10.md` | Critical Readiness Exploration - Interactive Deep Dive |
| 11 | `steps/step-11.md` | Retrospective Closure with Celebration and Commitment |
| 12 | `steps/step-12.md` | Save Retrospective and Update Sprint Status |
| 13 | `steps/step-13.md` | Final Summary and Handoff |
---
name: superpowers-sage:plan-generator
description: >
  Generate implementation plans from approved designs — plan-generator,
  phase-based plans, parallel batch execution, task dependency graph,
  owner skill routing, acceptance criteria, global done criteria,
  plan frontmatter, layout contract, interaction contract, anti-drift rules,
  plan format, AD-2 byte-for-byte gate, scope definition, execution plan,
  phases and batches, task anatomy, plan file format
user-invocable: true
argument-hint: "[approved architecture spec path or feature topic]"
---

# Plan Generator

Generate implementation plans from approved architecture specs.

**Announce at start:** "I'm using plan-generator to transform the approved architecture into an executable implementation plan."

## Input

$ARGUMENTS

## HARD GATES

- Do not generate a plan without an approved architecture spec.
- Do not implement code in this skill.
- Do not mark the plan complete if dependencies are ambiguous.

## Procedure

### 1) Resolve and validate spec input

Accept one of:

- Direct spec path from arguments
- Most recent approved file in `docs/superpowers/specs/`

Reject if spec approval is missing.

### 2) Preflight — handoff payload validation

Before generating any plan files, validate the architecture spec against its claimed
sources (git refs, external APIs, content models). See `references/anti-drift.md` for
the full preflight protocol.

If the spec's "chosen approach" is "zero-migration port from legacy schema", emit
an AD-2 byte-for-byte gate per ported component. See `references/anti-drift.md`.

### 3) Parse architecture into implementation units

Extract:

- Components and responsibilities
- Data model decisions
- Integration points
- Quality constraints

Translate each into concrete implementation units.

### 4) Build dependency graph

Classify every unit:

- `parallel`: independent work
- `sequential`: depends on prior unit output
- `gated`: requires user/reviewer checkpoint

Document graph in the plan.

### 5) Assign execution strategy and skill routing

For each unit, define:

- Strategy: autonomous, interactive, or mixed
- Suggested skill(s): `superpowers-sage:building`, `superpowers-sage:modeling`, `superpowers-sage:designing`, `superpowers-sage:verifying`, and reference skills (`acorn-*`, `wp-*`) as needed
- Acceptance criteria

### 6) Generate plan directory and files

Create the directory and file structure as defined in `references/plan-format.md`.

> Full file templates and frontmatter schemas: `skills/plan-generator/references/plan-format.md`

### 7) Validate plan consistency

Check:

- Every component appears exactly once
- Every dependency has a source node
- No component is both parallel and sequential in the same stage
- Strategy aligns with risk/complexity
- Every interactive component has a visual checkpoint owner

> Full validation rules: `skills/plan-generator/references/anti-drift.md`

### 8) Final handoff for execution

Present concise execution summary (phases, parallel batches, checkpoints) and offer
`superpowers-sage:building`.

## Verification

Before completion, confirm all items:

- Approved source spec exists and is referenced in `source-spec`
- Plan directory exists with required files
- Dependency graph has no unresolved nodes
- Each component has acceptance criteria in its sub-plan

## Failure modes

- Spec missing or unapproved: block and request architecture approval.
- Dependency cycle detected: surface cycle and propose reordering.
- Incomplete component definitions: return to architecture spec for clarification.
- Too many cross-component dependencies: split into phased plan and mark phase gates.

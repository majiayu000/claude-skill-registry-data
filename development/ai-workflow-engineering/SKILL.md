---
name: ai-workflow-engineering
description: "Guide for creating reliable AI workflows and SOPs. Use when: (1) User wants to create a structured workflow for AI tasks, (2) User needs to build an SOP for complex processes, (3) User wants to ensure their workflow follows best practices for managing LLM uncertainty, (4) User mentions creating workflows for domains like code review, response analysis, documentation, or any structured process"
license: Public domain - shared for AI engineering community
---

# AI Workflow Engineering Pattern

## When to Use This Skill

Creating reliable AI workflows that manage LLM uncertainty through structured phases, explicit constraints, and human checkpoints. This is the universal pattern that emerged across PDD, HumanLayer, and Agent SOPs.

## The 5-Phase Universal Structure

All reliable AI workflows follow this pattern:

1. **Intake/Investigation** - Validate inputs before processing
2. **Decomposition/Planning** - Break work into components
3. **Iterative Execution** - Do work with checkpoints
4. **Validation/Review** - Test quality with metrics
5. **Decision Point** - Human chooses next action

## Creating a New Workflow

### Parameters to Gather

Ask user for:
- `workflow_domain` - What problem space (e.g., "code review", "meeting facilitation")
- `primary_goal` - Main outcome to achieve
- `target_users` - Who will use this (optional)
- `output_location` - Where to save artifacts (default: "./workflows")

**Key constraint:** Get all parameters upfront in single prompt

### Phase 1: Domain Analysis

Create `{output}/domain-analysis.md` documenting:

```markdown
## Problem Statement
[What makes this hard without structure]

## Failure Modes
- [What goes wrong without workflow]
- [Where LLM uncertainty is highest]

## Critical Decision Points
- [Where human judgment matters]

## Success Criteria
- [Observable outcomes]
```

**Checkpoint:** "Does this analysis capture the domain correctly?"

### Phase 2: Input/Output Specification

Define in `{output}/io-specification.md`:

**Required parameters:**
- Name, type, description
- Required vs optional
- Validation rules
- Default values

**Output artifacts:**
- What files/data produced
- Format specifications
- Success criteria

**Input methods:**
- Direct text, file upload, URL, API, etc.

**Checkpoint:** "Are I/O specs clear and testable?"

### Phase 3: Phase Decomposition

Create `{output}/phases.md` with structure:

```markdown
## Phase N: [Name]

**Objective:** [What this accomplishes]

**Entry criteria:** [What must be true to enter]

**Activities:**
- [Key actions in this phase]

**Outputs:** [Artifacts created]

**Exit criteria:** [What must be true to exit]

**Checkpoint:** [User decision at end]

**Can iterate back to:** [Which phases]
```

Include mermaid diagram showing phase transitions.

**Required phases:**
1. Intake (validate inputs)
2. Decomposition (structure work)
3. Execution (do work - can have sub-phases)
4. Validation (check quality)
5. Decision (user chooses next)

**Checkpoint:** "Do phases cover complete workflow?"

### Phase 4: Constraint Definition

Create `{output}/constraints.md` using RFC 2119 language:

**Format:**
```markdown
## Phase: [Name]

### Action Constraints
- You MUST [action] before [other action]
- You MUST NOT [anti-pattern] because [reason]
- You SHOULD [best practice] when [condition]
- You MAY [optional action] if [condition]

### Interaction Constraints
- You MUST ask ONE question at a time
- You MUST wait for user confirmation before [action]
- You MUST present [summary] at checkpoints

### Validation Constraints
- You MUST verify [condition] is met
- You MUST calculate [metric] and compare to [threshold]
```

**Critical:** Include rationale with "because" for key constraints.

**Anti-patterns:** Document common failures to prevent:
```markdown
- You MUST NOT list all questions at once because this overwhelms users
- You MUST NOT pre-populate answers because this assumes preferences
```

**Checkpoint:** "Any additional constraints or anti-patterns to add?"

### Phase 5: Checkpoint Design

Create `{output}/checkpoints.md`:

```markdown
## Checkpoint: [Name]

**Trigger:** [When this occurs]

**Present to user:**
- Current state: [Progress summary]
- Key findings: [Important discoveries]
- Quality metrics: [Scores/coverage]

**Options:**
[A] [Proceed option]
[B] [Iterate/revise option]
[C] [Change approach option]
[D] [Request info option]

**Question:** [Explicit question to user]

**Constraints:**
- You MUST wait for user response
- You MUST NOT auto-select option
```

**Key principle:** Checkpoints at natural decision points only (not purely informational).

**Checkpoint:** "Are these the right decision points?"

### Phase 6: Validation Framework

Create `{output}/validation-framework.md`:

```markdown
## Test: [Name]

**Purpose:** [What this validates]

**Method:** [How to perform test]

**Pass criteria:** [Observable conditions]
**Fail criteria:** [Observable conditions]
**Partial criteria:** [If applicable]

**Score calculation:** [If numeric]
```

**Required core tests:**
1. Completeness (all required elements present?)
2. Coverage (output addresses all input components?)
3. Specificity (output actionable and concrete?)
4. Context (output fits given constraints?)

**Success metrics:**
- Minimum passing score
- Excellent vs acceptable vs needs-revision thresholds

**Checkpoint:** "Are these the right quality criteria?"

### Phase 7: Artifact Specification

Create `{output}/artifacts.md`:

```markdown
## Artifact: [Name]

**Path:** {output}/[filename]
**Format:** [markdown/JSON/code/etc]
**Created:** [Which phase]
**Purpose:** [Checkpoint/intermediate/final]

**Required sections:**
- [Section 1]
- [Section 2]

**Lifecycle:** [Create → Update → Archive]
```

**Artifact types:**
- **Checkpoint artifacts** - Preserve state for resumption
- **Intermediate artifacts** - Support the process
- **Final artifacts** - Main deliverables

**Checkpoint:** "Will these artifacts support workflow needs?"

### Phase 8: Example Scenarios

Create `{output}/examples.md` with:

1. **Success scenario** - Everything goes smoothly
2. **Iteration scenario** - Multiple refinement cycles

Show for each:
- Initial inputs
- Interaction at checkpoints
- User responses
- Artifacts created
- Quality scores
- Final outputs

**Format:** Dialogue showing agent-user interaction

**Checkpoint:** "Do examples represent real usage?"

### Phase 9: Troubleshooting

Create `{output}/troubleshooting.md`:

```markdown
## Issue: [Name]

**Symptoms:** [How to recognize]
**Causes:** [Why it happens]
**Resolution:** [What to do]
**Prevention:** [How to avoid]
```

**Common issues to address:**
- Incomplete/ambiguous inputs
- User stuck at checkpoint
- Quality not improving with iteration
- Workflow too complex
- Context limits reached

**Checkpoint:** "What other issues to document?"

### Phase 10: Generate Final SOP

Create `{output}/workflow.sop.md`:

```markdown
# [Workflow Name]

## Overview
[What this does, when to use it]

## Parameters
[Required and optional inputs with constraints]

## Steps
### 1. [Phase Name]
[Description with constraints]
...

## Examples
[Usage scenarios]

## Troubleshooting
[Common issues]
```

Also create:
- `{output}/README.md` - Quick start guide
- Mermaid workflow diagram
- Quick reference card (optional)

**Checkpoint:** "Generate other formats? (SKILL.md, MCP prompt)"

### Phase 11: Validation

Run meta-validation checklist:

**Core Structure:**
- [ ] 5 core phases present
- [ ] Entry/exit criteria defined
- [ ] Clear checkpoints

**Constraints:**
- [ ] Uses MUST/SHOULD/MAY
- [ ] Includes rationales
- [ ] Testable/observable

**Checkpoints:**
- [ ] Prevents auto-progression
- [ ] Clear options presented
- [ ] Supports iteration

**Validation:**
- [ ] Success criteria defined
- [ ] Quality metrics present
- [ ] Pass/fail tests included

Create `{output}/validation-report.md` with scores:
- Completeness
- Clarity
- Actionability
- Robustness

**Checkpoint:** "What needs refinement before ready?"

### Phase 12: Iteration Checkpoint

Present summary:

```
Workflow Engineering Summary
============================
Domain: [workflow_domain]
Phases: [count] defined
Constraints: [count] explicit
Checkpoints: [count] decision points
Tests: [count] validation tests

Validation Score: X/10
Ready for use: [Yes/Needs revision]

Options:
[A] Ready - generate deliverables
[B] Revise sections (which?)
[C] Add examples/troubleshooting
[D] Simplify - too complex
[E] Test with real scenario first
```

### Phase 13: Delivery

Package all artifacts in `{output}/` directory.

Generate requested formats:
- Standard .sop.md (always)
- SKILL.md (if for Claude.ai)
- MCP prompt format (if for Claude Code)

Present:
```
Files created:
- workflow.sop.md (main SOP)
- README.md (quick start)
- [all other artifacts]

Next steps:
1. Review workflow.sop.md
2. Test with real scenario
3. Iterate based on results
4. Share with users

[A] Walk through with test case
[B] Generate additional formats
[C] Create training materials
[D] Done
```

## The 7 Universal Principles

Every workflow MUST follow:

1. **Explicit Over Implicit** - All constraints use MUST/SHOULD/MAY
2. **Validate Early/Often** - Check inputs, outputs, assumptions
3. **Human at Critical Points** - Checkpoints for decisions, not auto-pilot
4. **Observable/Measurable** - Every step produces artifacts, metrics
5. **Robust to Interruption** - Resume from checkpoints via artifacts
6. **Iterative by Design** - Non-linear, easy to revise, clear paths back
7. **Constrained but Flexible** - Rigid structure, flexible content

## Quick Reference: Constraint Language

**MUST** - Absolute requirement (testable pass/fail)
**MUST NOT** - Absolute prohibition (include "because")
**SHOULD** - Strong recommendation (can violate with reason)
**SHOULD NOT** - Strong discouragement
**MAY** - Optional (user's choice)

**Template:**
```
You MUST [action] before [other action]
You MUST NOT [anti-pattern] because [reason]
You SHOULD [best practice] when [condition]
You MAY [optional] if [condition]
```

## Common Workflow Domains

This pattern works for:

**Development:** Code review, design docs, API documentation, test strategy
**Communication:** Response quality, meeting facilitation, technical writing
**Analysis:** Problem decomposition, decision making, requirements gathering
**Planning:** Project/sprint planning, roadmap creation, resource allocation

## Meta-Validation Checklist

Quick check if workflow follows pattern:

- [ ] Has all 5 core phases
- [ ] Uses MUST/SHOULD/MAY language
- [ ] Has checkpoints with clear options
- [ ] Prevents auto-progression at decisions
- [ ] Has testable success criteria
- [ ] Calculates quality metrics
- [ ] Includes concrete examples
- [ ] Documents troubleshooting

## Why This Pattern Works

**Manages LLM uncertainty:**
- Constraints bound solution space
- Validation catches drift
- Checkpoints ensure alignment

**Decomposes complexity:**
- Explicit phases with clear outputs
- Iterative refinement over one-shot
- Context management via artifacts

**Coordinates human-AI:**
- Humans decide at critical points
- AI needs explicit permission
- Shared understanding of state

## Usage Notes

**For simple workflows:** May collapse some phases or reduce checkpoint frequency

**For complex workflows:** May expand execution phase into sub-phases, add more checkpoints

**Key principle:** Start simple, add structure only when needed

Always ask: "Does this constraint/checkpoint/test add value, or just complexity?"

## Version

v1.0 - Meta-pattern codified from PDD, HumanLayer, Agent SOPs convergence

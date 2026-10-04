---
name: sdlc-pipeline
description: >
  Use when user wants to run the complete end-to-end feature development pipeline.
  Triggers on "run sdlc pipeline", "start pipeline", "full feature workflow",
  "full lifecycle", "kick off pipeline", "/sdlc", or any request to execute all
  SDLC phases (requirements -> architecture -> design review -> impl planning ->
  implementation -> review -> verification -> risk -> PR) for a feature.
  Does NOT trigger for individual phases in isolation.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Skill
  - AskUserQuestion
---

# SDLC Pipeline Orchestrator

You are the pipeline conductor for the TriStar project (Triangle Smart Targeting and Real-Time Activation). Chain phase skills together in sequence, manage checkpoints, enforce iteration limits, and handle gated flow control. You do NOT implement any phase methodology -- delegate to specialized skills.

> **BEFORE EXECUTING ANY PHASE:** Read `references/execution-flow.md` for the full [1]-[10] per-phase instructions.

## Critical Path -- Execute This Checklist

For each phase in order (1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10):

1. Invoke the phase skill via `Skill` tool (except Phase 5 which is inline)
2. Validate the output artifact exists and has required fields
3. Update `pipeline_state.json`: set phase status = "completed", set current_phase = next phase name
4. Print summary text, then call `AskUserQuestion` tool for approval
5. On approval: invoke next phase immediately (no filler text)

10 phases, 10 state entries, 10 checkpoints. If you count fewer, something is wrong.

Phases: requirements -> architecture -> design-review -> impl-planning -> implementation -> simplify -> review -> verification -> risk -> pr

## CRITICAL: Skill Delegation Rules

**You MUST invoke each phase skill using the `Skill` tool.** Do not inline phase logic. Do not skip skill invocation. Do not write phase artifacts yourself.

**Phase 1 (Requirements) is especially strict:**
- You MUST invoke the `sdlc-requirements` skill via the Skill tool. Do NOT perform requirements analysis yourself.
- The requirements skill will ask the user clarifying questions. Do NOT skip this interrogation.
- The requirements skill will present a draft plan for user confirmation before writing `problem_spec.md`.

**Phase 6 (Simplify) delegates to the `simplify` skill:**
- Invoke `simplify` via the Skill tool after Phase 5 completes.
- After simplify returns, append a `## Simplification` section to `impl_manifest.md`.

**Phase 7 (Review) uses `code-review` skill:**
- The code-review skill auto-detects file types (TypeScript/React vs Python/FastAPI) and applies the appropriate checklist.

**Phase 8 (Verification) chains multiple checks:**
- First: invoke `sdlc-verify` for engineering verification (requirement coverage + test pass rate)
- Then: invoke `security-scan` for security audit
- Then: for offer-related code, invoke `loyalty-fraud-detection` skill (existing TriStar skill)
- Then: for activation-related code, invoke `semantic-context-matching` skill (existing TriStar skill)
- Verification fails if any domain skill flags severity === 'critical'

## Iron Laws

- NEVER INLINE PHASE LOGIC -- always invoke phases via the Skill tool, no exceptions.
- NEVER WRITE `problem_spec.md` YOURSELF -- only `sdlc-requirements` may produce it.
- NEVER PROCEED PAST A "reject" DESIGN REVIEW -- feed findings back to `sdlc-architecture`.
- NEVER SKIP THE INCREMENTAL TESTING PROTOCOL DURING IMPLEMENTATION -- test after each file change.
- NEVER EXCEED ITERATION LIMITS SILENTLY -- halt and report when limits are reached.
- NEVER SKIP PHASE 10 (PR CREATION) -- the pipeline is NOT complete until a PR is created.

## Overview

Orchestrates a complete SDLC workflow from requirements through PR creation for the TriStar project. Each phase is owned by a dedicated skill. The orchestrator runs in gated mode.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--feature=<name>` | Yes | Feature name (e.g., `designer-ui`, `hub-state`). Used in paths, branches, PR titles. |
| `--resume` | No | Restart from last saved checkpoint. |
| `--from=<phase>` | No | Start from: `requirements\|architecture\|design-review\|impl-planning\|implementation\|simplify\|review\|verification\|risk\|pr`. |
| `--waves` | No | Force wave-based parallel execution for Phase 5. |

### Validation

1. `--feature` must be a valid kebab-case identifier
2. `--resume` requires `.claude/checkpoints/<feature>/pipeline_state.json` to exist
3. `--from` must be one of the ten valid phase names

## Directory Structure

Create before first phase if absent:

```
docs/artifacts/<feature>/          # Spec artifacts (problem_spec.md, design_spec.md, design_review.md)
.claude/checkpoints/<feature>/     # Execution artifacts (impl_manifest.md, verification_report.md, risk_assessment.md, pipeline_state.json)
```

## Phase Definitions

| # | Phase | Skill Invoked | Output Artifact | Location |
|---|-------|---------------|-----------------|----------|
| 1 | Requirements | `sdlc-requirements` | `problem_spec.md` | `docs/artifacts/<feature>/` |
| 2 | Architecture | `sdlc-architecture` | `design_spec.md` | `docs/artifacts/<feature>/` |
| 3 | Design Review | `sdlc-design-review` | `design_review.md` | `docs/artifacts/<feature>/` |
| 4 | Impl Planning | `sdlc-impl-planning` | `implementation_plan.md` | `docs/artifacts/<feature>/` |
| 5 | Implementation | (inline -- main agent) | `impl_manifest.md` | `.claude/checkpoints/<feature>/` |
| 6 | Simplify | `simplify` | `## Simplification` in manifest | `.claude/checkpoints/<feature>/` |
| 7 | Review | `code-review` + `generate-tests` + `security-scan` | findings | (in context) |
| 8 | Verification | `sdlc-verify` + `security-scan` + `loyalty-fraud-detection` + `semantic-context-matching` | `verification_report.md` | `.claude/checkpoints/<feature>/` |
| 9 | Risk Assessment | `sdlc-risk` | `risk_assessment.md` | `.claude/checkpoints/<feature>/` |
| 10 | PR Creation | `create-pr` | PR URL | GitHub |

## Gate Behavior

After each phase, use `AskUserQuestion` tool to present the gate with three options:
- "Approve and continue" -> proceed to next phase IMMEDIATELY
- "Stop pipeline" -> save checkpoint, print resume command
- "Revise" -> re-run current phase with feedback

**After receiving "Approve and continue", the very next action MUST be invoking the next phase's skill. No summaries, no filler text. Just go.**

## Resume Logic

1. Read `.claude/checkpoints/<feature>/pipeline_state.json`
2. Display phase status table
3. Identify last completed phase
4. Load all completed phase artifacts
5. Resume from next pending phase

## Iteration Limits

| Loop | Max | Trigger |
|------|-----|---------|
| Design review rejects architecture | 3 | `verdict = "reject"` |
| Spec review requires implementation fixes | 2 | `spec_compliant = false` |
| Risk requires implementation fixes | 3 | `recommendation = "fix_first"` |
| Risk requires architecture redesign | 2 | `recommendation = "redesign"` |

## Required Artifact Sections

| Artifact | Required Sections |
|----------|-------------------|
| `problem_spec.md` | `## Meta`, `## Problem Statement`, `## Requirements`, `## Acceptance Criteria`, `## Constraints`, `## Non-Goals`, `## Assumptions`, `## Edge Cases`, `## Backward Compatibility`, `## Glossary` |
| `design_spec.md` | `## Meta`, `## Problem Spec Reference`, `## Current Architecture`, `## Architecture`, `## API Contracts`, `## Data Models`, `## Decisions (ADRs)`, `## Implementation Guidelines`, `## Testing Strategy`, `## Security Considerations` |
| `design_review.md` | `## Meta`, `## Summary`, `## Findings`, `## Sign-Off` |
| `implementation_plan.md` | `## Implementation Steps`, `## Pipeline Continuation`, `## Pre-Implementation Baseline` |
| `impl_manifest.md` | `## Summary`, `## Baseline Test Counts`, `## Final Test Counts`, `## Files Created`, `## Files Modified`, `## Test Files`, `## Simplification` |
| `verification_report.md` | `## Meta`, `## Summary`, `## Requirement Coverage`, `## Test Results`, `## Recommendations` |
| `risk_assessment.md` | `## Meta`, `## Summary`, `## Failure Modes`, `## Sign-Off` |

## References

- **Execution flow (full per-phase instructions):** `references/execution-flow.md`
- **Pipeline state JSON schema:** `references/pipeline-state-schema.md`
- **Artifact digest template:** `references/artifact-digest.md`
- **Subagent dispatch templates:** `appendix/subagent-prompts.md`
- Phase skills: `sdlc-requirements`, `sdlc-architecture`, `sdlc-design-review`, `sdlc-impl-planning`, `sdlc-verify`, `sdlc-risk`
- Review skills: `code-review`, `security-scan`, `generate-tests`
- Domain skills: `loyalty-fraud-detection`, `semantic-context-matching`
- PR skill: `create-pr` | Checkpoint utility: `sdlc-checkpoint`

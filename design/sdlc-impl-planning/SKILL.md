---
name: sdlc-impl-planning
description: Create an ordered implementation plan for a TriStar feature. Builds file dependency graph, maps acceptance criteria to files, defines wave-based execution order, and identifies risks.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# SDLC Implementation Planning Skill

## Prime Directive

**"Plan the work. Then work the plan."**

This skill converts architecture design into an actionable, ordered implementation plan. Every file to create or modify is listed with dependencies, acceptance criteria mappings, and test strategies.

## Arguments

- `--feature=<name>` (required) - Feature name matching existing artifacts

## Prerequisites

- `docs/artifacts/<feature>/problem_spec.md` must exist
- `docs/artifacts/<feature>/design_spec.md` must exist
- `docs/artifacts/<feature>/design_review.md` must exist with APPROVE or APPROVE_WITH_CONCERNS decision

## Process

### Step 1: Load Artifacts

Read all feature artifacts:
1. `docs/artifacts/<feature>/problem_spec.md` - Requirements and acceptance criteria
2. `docs/artifacts/<feature>/design_spec.md` - Component design, API contracts, data models
3. `docs/artifacts/<feature>/design_review.md` - Review findings and concerns to address
4. `docs/ARCHITECTURE.md` - System architecture baseline

### Step 2: Build Ordered File List

Extract every file that needs to be created or modified from the design spec:
- List each file with its COMP-ID from the design
- Note whether the file is NEW or MODIFIED
- Note the layer (Designer / Hub / Scout / Shared / Tests)
- Note the file type (TypeScript / Python / Config)

### Step 3: Compute Dependency Graph

For each file, determine its dependencies:
- Which other files must exist before this file can be implemented?
- Which shared types does it depend on?
- Which services does it call?
- Which models does it use?

Assign each file to a wave based on the TriStar dependency ordering (see references/tristar-dependencies.md):
- Wave 1: Shared types (no dependencies)
- Wave 2: Backend models (depends on shared types)
- Wave 3: Backend services (depends on models)
- Wave 4: Backend API routes (depends on services)
- Wave 5: Frontend services (depends on API contracts)
- Wave 6: Frontend components (depends on frontend services)
- Wave 7: Tests (depends on implementation)

### Step 4: Map Acceptance Criteria to Files

For each acceptance criterion from the problem spec:
- Which files are involved in satisfying this AC?
- Which test files verify this AC?
- Mark any AC that spans multiple waves (integration risk)

### Step 5: Map Test Strategy

For each implementation file:
- Corresponding unit test file path
- Key test scenarios (from testing.md patterns)
- Mock dependencies needed
- Integration test scenarios (if applicable)

### Step 6: Identify Risks

Flag implementation risks:
- Files in multiple waves that share state (race condition risk)
- Complex logic that needs careful testing (fraud detection, scoring)
- External API integrations that need mocking strategy
- Schema changes that affect multiple layers (Zod + Pydantic sync)
- Design review concerns that need special attention during implementation

### Step 7: Write Implementation Plan

Save to: `docs/artifacts/<feature>/implementation_plan.md`

### Step 8: Update Artifact Digest

Create or update `.claude/checkpoints/<feature>/artifact_digest.md` with:
- List of all artifacts produced so far
- Current pipeline stage (impl-planning complete)
- Next expected stage (implementation)

## Output Template

```markdown
# Implementation Plan: <feature-name>

## Overview
- Total files: N (M new, K modified)
- Waves: 7
- Estimated complexity: Low / Medium / High

## Wave Plan

### Wave 1: Shared Types
| # | File | Action | COMP-ID | Description |
|---|------|--------|---------|-------------|
| 1 | src/shared/types/offer-brief.ts | MODIFY | COMP-001 | Add new fields to OfferBrief |

**Wave 1 Verification:**
- [ ] TypeScript compiles without errors
- [ ] Zod schema validates correctly

### Wave 2: Backend Models
| # | File | Action | COMP-ID | Description |
|---|------|--------|---------|-------------|
| 2 | src/backend/models/offer_brief.py | MODIFY | COMP-002 | Mirror OfferBrief changes in Pydantic |

**Wave 2 Verification:**
- [ ] Pydantic model validates correctly
- [ ] Fields match Wave 1 Zod schema

### Wave 3: Backend Services
...

### Wave 4: Backend API Routes
...

### Wave 5: Frontend Services
...

### Wave 6: Frontend Components
...

### Wave 7: Tests
| # | File | Action | Tests For | Scenarios |
|---|------|--------|-----------|-----------|
| N | tests/unit/backend/test_offer_brief.py | NEW | COMP-002 | Validation, edge cases |

**Wave 7 Verification:**
- [ ] All unit tests pass
- [ ] Coverage > 80%
- [ ] Integration tests pass

## Acceptance Criteria Mapping

| AC ID | Description | Files | Test File | Wave |
|-------|-------------|-------|-----------|------|
| AC-001 | Given X, When Y, Then Z | file1, file2 | test_file | 3,4 |

## Risk Register

| Risk | Impact | Mitigation | Wave |
|------|--------|------------|------|
| R-001: Schema sync | High | Implement Wave 1+2 together, verify match | 1-2 |

## Design Review Concerns

| Finding | Severity | How Addressed |
|---------|----------|---------------|
| F-001: Missing error handling | Major | Added try/catch in Wave 4 files |

## Implementation Order Summary

1. Wave 1: Shared types (foundation)
2. Wave 2: Backend models (must match Wave 1)
3. Wave 3: Backend services (business logic)
4. Wave 4: Backend routes (API layer)
5. Wave 5: Frontend services (API clients)
6. Wave 6: Frontend components (UI layer)
7. Wave 7: Tests (verification layer)
```

## Reference Files

- `references/tristar-dependencies.md` - Layer dependency ordering and wave assignment rules

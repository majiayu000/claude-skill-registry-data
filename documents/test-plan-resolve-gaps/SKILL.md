---
name: test-plan-resolve-gaps
description: Cross-reference existing test plan gaps with new analyzer findings and documentation to determine which gaps are resolved and which remain open. Use after adding new documentation to identify what questions have been answered and what's still missing.
user-invocable: false
context: fork
model: claude-sonnet-4-6
allowedTools:
  - Read
---

# Test Plan Gap Resolver

Determine which test plan gaps are resolved by new documentation and analyzer findings, and which gaps remain open.

## Invocation

This skill is invoked by `/test-plan-update` as a forked sub-agent. It receives:
1. Old gaps from TestPlanGaps.md
2. New findings from the three analyzers
3. List of new documents added

## Inputs (passed inline in skill arguments)

The parent skill passes:
```
Old Gaps from TestPlanGaps.md:
## Scope & Endpoints
- <gap_1>
- <gap_2>

## Test Strategy & Risks
- <gap_3>

## Environment & Infrastructure
- <gap_4>
- <gap_5>

New Findings from Analyzers:
- Endpoints: <findings_from_test-plan.analyze.endpoints>
- Risks: <findings_from_test-plan.analyze.risks>
- Infrastructure: <findings_from_test-plan.analyze.infra>

New Documents Added:
- <doc_1_name> (e.g., "API Specification v2.0")
- <doc_2_name> (e.g., "Design Document - Catalog Architecture")
```

## Process

### Step 1: Parse Old Gaps

Extract gaps by section:
1. **Scope & Endpoints gaps** - missing API details, unclear scope, undefined endpoints
2. **Test Strategy & Risks gaps** - unclear priorities, missing risk mitigations, incomplete NFR assessments
3. **Environment & Infrastructure gaps** - missing test data specs, unclear dependencies, undefined test users

For each gap, identify what information would resolve it (often stated in the gap itself, e.g., "would be resolved by: API spec").

### Step 2: Analyze New Findings for Gap Resolution

For each old gap, check if new analyzer findings or documents address it:

**Scope & Endpoints gaps:**
- Gap: "Exact endpoint paths not specified"
  - Check if endpoints analyzer now has specific paths (e.g., `POST /api/v2/catalog/items`)
  - If yes → mark as resolved by endpoints analyzer findings

- Gap: "Expected response format unclear"
  - Check if new documents include API spec with response schemas
  - If yes → mark as resolved by specific document

**Test Strategy & Risks gaps:**
- Gap: "Priority criteria too generic"
  - Check if risks analyzer now has feature-specific priority definitions
  - If yes → mark as resolved

- Gap: "Missing risk mitigation for database failure"
  - Check if risks analyzer identified mitigation strategy
  - If yes → mark as resolved

**Environment & Infrastructure gaps:**
- Gap: "Test data schema not defined"
  - Check if infra analyzer or new docs specify test data requirements
  - If yes → mark as resolved

### Step 3: Identify New Gaps

Check if new analyzer findings revealed new gaps:
- Endpoints analyzer: new APIs without implementation details?
- Risks analyzer: new risks without mitigations?
- Infra analyzer: new dependencies without version specs?

Add these to the unresolved gaps list.

### Step 4: Semantic Matching Logic

Use intelligent matching, not just keyword search:

**Example 1: Endpoint gap**
- Old gap: "Catalog API endpoint paths not specified"
- New finding: "POST /catalog/items, GET /catalog/items/{id}, DELETE /catalog/items/{id}"
- **Match**: Both are about catalog API endpoints → RESOLVED

**Example 2: Test data gap**
- Old gap: "Expected hardware profile name format unclear"
- New finding: "Hardware profiles follow format: hwp-{accelerator}-{memory}-{version} (e.g., hwp-gpu-16g-v1)"
- **Match**: Both are about hardware profile naming → RESOLVED

**Example 3: Partial resolution**
- Old gap: "RBAC roles and permissions not specified"
- New finding: "Three roles: admin, developer, viewer"
- **Partial match**: Roles identified but permissions still missing → PARTIALLY RESOLVED (or keep as gap with note)

**Anti-hallucination**:
- Only mark gaps as resolved if new information truly addresses them
- If unsure → keep gap open (conservative approach)
- Don't invent resolutions

### Step 5: Output Structure

Return structured output for the parent skill:

```markdown
## Resolved Gaps

### Scope & Endpoints
- ✅ Exact endpoint paths not specified → **Resolved by**: API Specification v2.0 (POST /catalog/items, GET /catalog/items/{id}, DELETE /catalog/items/{id})
- ✅ Expected response format unclear → **Resolved by**: API Specification v2.0 (JSON schema provided)

### Test Strategy & Risks
- ✅ Priority criteria too generic → **Resolved by**: Analyzer findings (feature-specific P0: catalog operations affecting user workflows)

### Environment & Infrastructure
- ✅ Test data schema not defined → **Resolved by**: Design Document (catalog items require: id, name, category, tags array)

## Unresolved Gaps

### Scope & Endpoints
- Cypress test scenarios not specified — **Requires**: ADR / test specification
- Unit test file structure unclear — **Requires**: ADR / test specification

### Test Strategy & Risks
(No unresolved gaps in this section)

### Environment & Infrastructure
- Global namespace constant not confirmed (assumed redhat-ods-applications) — **Requires**: ADR / design doc

## New Gaps Identified

### Scope & Endpoints
- New catalog search API endpoints discovered but query parameter validation rules not specified — **Requires**: API spec addendum

### Environment & Infrastructure
- PostgreSQL version requirement not specified (catalog storage dependency) — **Requires**: infrastructure doc

## Statistics

- **Total gaps before**: 10
- **Gaps resolved**: 4
- **Gaps remaining**: 6
- **New gaps identified**: 2
- **Total gaps now**: 8

## Updated Gap Count

Open gaps: 8
Resolved gaps: 4
Status: Open (gaps remaining)
```

## What this skill does NOT do

- Does NOT modify TestPlanGaps.md — returns structured output for parent to apply
- Does NOT re-run analyzers — receives their findings as input
- Does NOT fetch new documents — receives document names as context
- Does NOT make assumptions about what resolves gaps — conservative matching only

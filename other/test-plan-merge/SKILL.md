---
name: test-plan-merge
description: Intelligently merge new analyzer findings into an existing test plan, preserving user edits while incorporating updates from new documentation. Use for test plan updates when re-analysis produces new findings that need to be integrated without overwriting human modifications.
user-invocable: false
context: fork
model: claude-sonnet-4-6
allowedTools:
  - Read
  - Write
---

# Test Plan Merger

Merge new analyzer findings into an existing test plan while preserving user customizations.

## Invocation

This skill is invoked by `/test-plan-update` as a forked sub-agent. It receives:
1. Old TestPlan.md content
2. New findings from the three analyzers
3. Context about what new documents were added

## Inputs (passed inline in skill arguments)

The parent skill passes:
```
Old TestPlan.md: <full_content>

New Findings from Analyzers:
- Interfaces: <findings_from_test-plan.analyze.endpoints>
- Risks: <findings_from_test-plan.analyze.risks>
- Infrastructure: <findings_from_test-plan.analyze.infra>

New Documents Added: <list_of_new_doc_names>
```

## Process

### Step 1: Parse Old TestPlan.md

Extract current content for each section:
1. Section 1 (Executive Summary): 1.1 Purpose, 1.2 Scope, 1.3 Test Objectives
2. Section 2 (Test Strategy): 2.1 Test Levels, 2.2 Test Types, 2.3 Priority Definitions
3. Section 3 (Test Environment): 3.1 Infrastructure & Configuration, 3.2 Test Data, 3.3 Test Users, 3.4 Test Tools
4. Section 4 (Interfaces Under Test)
5. Section 7 (Non-Functional Requirements)
6. Section 8 (Risks and Mitigations)

Store each section's content as baseline.

### Step 2: Parse New Analyzer Findings

Extract new findings:
- **From endpoints analyzer**: new scope items, new test objectives, new interfaces
- **From risks analyzer**: new test types, updated priority definitions, new risks, updated NFR assessments
- **From infra analyzer**: new environment requirements, new test data needs, new dependencies

### Step 3: Intelligent Merge Strategy

For each section, apply this merge logic:

**Section 1.1 (Purpose)**:
- If new findings contradict existing purpose → Update with new findings, note in change summary
- If new findings extend existing purpose → Merge additively
- If unchanged → Keep as-is (preserve user refinements)

**Section 1.2 (Scope)**:
- In-scope items:
  - Add new items from endpoints analyzer that weren't in old scope
  - Keep existing items that are still valid
  - Mark deprecated items (if new findings indicate they're removed)
- Out-of-scope items:
  - Keep as-is unless contradicted by new findings
  - Add new out-of-scope items if identified

**Section 1.3 (Test Objectives)**:
- Add new objectives from analyzers
- Keep existing objectives that are still valid
- Merge similar objectives (avoid duplication)

**Section 2.1 (Test Levels)**:
- If new levels identified → add to existing list
- Keep user-added descriptions

**Section 2.2 (Test Types)**:
- Add new types from risks analyzer
- Keep existing types

**Section 2.3 (Priority Definitions)**:
- If definitions are generic boilerplate → Replace with feature-specific definitions from risks analyzer
- If definitions are already feature-specific → Keep and only add new criteria if found

**Section 3 (Test Environment)**:
- Merge additively: add new requirements, test data, users
- Keep existing entries

**Section 4 (Interfaces Under Test)**:
- Add new interfaces from endpoints analyzer
- Keep existing interfaces
- Mark deprecated interfaces (if explicitly identified as removed)
- Preserve any user-added notes or clarifications

**Section 7 (Non-Functional Requirements)**:
- Update assessments from risks analyzer
- If was "Not Applicable" but new findings indicate it's now applicable → update
- If was assessed and new findings provide more detail → update assessment

**Section 8 (Risks and Mitigations)**:
- Add new risks from risks analyzer
- Keep existing risks
- If new findings indicate a risk is mitigated → mark as resolved or remove

**Sections 5, 6, 9 (Test Cases, E2E, Appendix)**:
- Do NOT modify — these are managed by `/test-plan-create-cases`

### Step 4: Generate Change Summary

Track all changes made:

**Format**:
```markdown
## Changes Made

### Section 1 (Executive Summary)
- Added 2 new in-scope items
- Updated purpose to reflect new API spec details

### Section 4 (Interfaces Under Test)
- Added 3 new interfaces: POST /catalog/items, GET /catalog/items/{id}, DELETE /catalog/items/{id}
- Marked deprecated: GET /legacy/catalog (removed in v2.0)

### Section 7 (Non-Functional Requirements)
- Updated Performance assessment: "Not Applicable" → "95th percentile latency < 200ms for catalog operations"

### Section 8 (Risks)
- Added new risk: "Catalog database migration during upgrade may cause downtime"

## User Edits Preserved

- Section 1.1 Purpose: kept user-refined language
- Section 2.3 Priority Definitions: kept feature-specific P0 criteria
- Section 4: preserved user notes on authentication requirements
```

### Step 5: Output Structure

Return structured output for the parent skill:

```markdown
## Updated Sections

### Section 1: Executive Summary

<full_updated_section_1_content>

### Section 2: Test Strategy

<full_updated_section_2_content>

### Section 4: Interfaces Under Test

<full_updated_section_4_content>

### Section 7: Non-Functional Requirements

<full_updated_section_7_content>

### Section 8: Risks and Mitigations

<full_updated_section_8_content>

## Change Summary

<change_summary_from_step_4>

## Merge Statistics

- Sections updated: <count>
- New items added: <count>
- Items updated: <count>
- Items deprecated: <count>
- User edits preserved: <count>
```

## Anti-hallucination Rules

- Do NOT invent new interfaces not present in the new analyzer findings
- Do NOT remove existing content unless explicitly contradicted by new findings
- Do NOT modify test case sections (5, 6, 9) — they're owned by other skills
- If unsure whether to keep or update a section → keep it (preserve user intent)
- Always prefer additive changes over destructive changes

## What this skill does NOT do

- Does NOT validate TestPlan.md frontmatter — parent skill handles that
- Does NOT re-run analyzers — receives their findings as input
- Does NOT update test cases — parent skill handles that via `/test-plan-create-cases`
- Does NOT write files directly — returns structured output for parent to apply

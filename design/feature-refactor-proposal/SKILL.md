---
name: feature-refactor-proposal
description: Analyze codebase against new feature requirements, map affected modules and dependencies, identify architectural risks, and propose a structured refactoring and implementation plan before writing code. Use when starting a new feature, planning refactoring, analyzing codebase impact, or reviewing feature feasibility.
---

# Feature Refactor Proposal

This skill provides a structured methodology for analyzing an existing codebase against new feature requirements, identifying technical debt and risks, and producing a clear refactoring and implementation proposal before writing code.

## When to Use

Use this skill when:

- Adding a complex new feature to an existing codebase
- Extending existing components or state management that could cause architectural regression
- Assessing feature feasibility and breaking changes before implementation
- Preparing an architecture proposal or technical design review for a feature request

## Workflow Decision Tree

```
User provides New Feature Requirements / Issue
  │
  ├── 1. Parse Requirements & Define Boundaries
  │     └─ Identify UI, state, API, and backend scope
  │
  ├── 2. Map Codebase Impact
  │     └─ Locate affected components, hooks, services, types
  │
  ├── 3. Evaluate Risks & Trade-offs
  │     └─ Consult [risk_checklist.md](references/risk_checklist.md)
  │
  ├── 4. Draft Refactoring & Implementation Plan
  │     └─ Use [proposal_template.md](references/proposal_template.md)
  │
  └── 5. Present Proposal & Verification Steps
        └─ Provide phased steps and validation commands
```

---

## Detailed Steps

### Step 1: Requirement Breakdown & Scope Mapping

1. Extract core requirements and non-goals from the user prompt or issue document.
2. Categorize requirements by impact layer:
   - **UI Layer**: Pages, components, modals, styles
   - **State Layer**: React state, context, custom hooks, global stores
   - **Service / API Layer**: Frontend API client, backend commands, Tauri IPC
   - **Data Layer**: Types, schemas, entities, database tables

### Step 2: Codebase Exploration & Dependency Tracing

1. Search for relevant existing files using `workspace__grepFiles` and `workspace__globFiles`.
2. Inspect target files with `workspace__readFile` to understand:
   - Current responsibilities and size of components
   - Existing data flow and state propagation
   - Shared dependencies and props interface
3. Map component dependencies to anticipate ripple effects when modifying signatures or state.

### Step 3: Risk Assessment & Architecture Trade-offs

1. Load and evaluate against [references/risk_checklist.md](references/risk_checklist.md):
   - **Type Safety**: Prop changes, boundary validation, schema changes
   - **State Complexity**: State duplication vs context extension vs hook extraction
   - **UI/UX Resilience**: Virtualized lists, scroll pinning, loading/error states
   - **Backward Compatibility**: Impact on other features using the same components
2. Compare architectural choices (e.g., Option A: Direct Extension vs Option B: Modular Refactoring).

### Step 4: Generate Proposal Report

1. Use the structure provided in [references/proposal_template.md](references/proposal_template.md).
2. Document:
   - Affected files and modification scope
   - Recommended refactoring approach with trade-off justification
   - Phased execution steps (Preparation/Refactor -> Feature Implementation -> Verification)
   - Specific verification criteria (`pnpm refactor:validate`, tests, manual checks)

---

## References

- **[proposal_template.md](references/proposal_template.md)**: Standard template for feature refactoring proposals.
- **[risk_checklist.md](references/risk_checklist.md)**: Architectural and quality risk review checklist.

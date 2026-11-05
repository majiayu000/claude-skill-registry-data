---
name: reviewing-architecture
description: Eng manager-mode plan review. Lock in the execution plan, data flow, diagrams, edge cases.
phase: 7 (Architect)
role: Lead
---

# Reviewing Architecture (Eng Review)

**Role Constraints:** Lead (Write/Bash access allowed).
**File Access:** Do NOT use literal placeholders for file paths. Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`.

## Objective
Act as an Engineering Manager to lock in the execution plan. Review architecture, data flow, edge cases, test coverage, and performance. 

## Execution Steps

1. **Gather Context:** Use `glob` and `read` to find and review the feature's `pitch.md`, `strategy-review.md`, and any existing technical drafts in the active feature directory under `.jonggrang/.output/features/`.
2. **Review Dimensions:**
   - **Architecture & Data Flow:** Does the data model support the feature? Are DB queries optimized? 
   - **Edge Cases & Error Handling:** What happens when APIs fail, inputs are malformed, or state is lost?
   - **Test Coverage:** What is the testing strategy (unit, integration, E2E)?
   - **Performance:** Are there N+1 query risks? Are assets optimized?
   - **Security:** Are inputs sanitized? Are permissions checked properly?
3. **Iterative Refinement:** Discuss identified technical gaps with the user and propose opinionated recommendations.
4. **Save Architecture Plan:** Once finalized, use the `write` tool to output the finalized technical decisions to `architecture-review.md` in the active feature directory.

## Completion Signal
When the architecture plan is finalized and saved, output exactly:

ARCHITECTURE_REVIEW_COMPLETE

---
name: vibe-check
description: Validate PRD quality and coherence before innovation phase using vibe-check MCP tool. Checks for requirement clarity, user story completeness, and identifies gaps. Returns coherent flag and issues list.
---

# Vibe Check - PRD Quality Gate

> **ROOT AGENT ONLY** - Uses vibe-check MCP tool, runs only from root agent.

**Purpose:** Validate PRD coherence before innovation
**Trigger:** After requirements-phase, before innovate-phase
**Input:** PRD content (from requirements-phase)
**Output:** Validation result (coherent, issues, recommendation)

---

## Overview

Quality gate using vibe-check MCP tool. Validates: (1) Internal consistency, (2) Clear/specific requirements, (3) User stories with AC, (4) No critical gaps. Prevents wasted innovation effort with incoherent PRD.

**When:** /architect only (skipped for /build and /audit with clearer requirements)

---

## Workflow

1. **Read PRD:** Load from `{projectFolder}/prd.md`
2. **Call MCP:** `vibe_check({ prdContent, projectContext? })`
3. **Parse response:** `coherent` (boolean), `issues` (array), `recommendation` ("proceed" | "revise")
4. **Decision gate:**
   - **If coherent:** Continue to innovate-phase (no user interaction)
   - **If not coherent:**
     - Report issues
     - Ask: Auto-revise or manual fixes?
     - Auto: Spawn BA to fix → requirements-phase → re-check (max 2 iterations)
     - Manual: Accept feedback → requirements-phase → re-check

---

## Validation Criteria

| Dimension    | Checks                               |
| ------------ | ------------------------------------ |
| Coherence    | PRD makes sense as a whole           |
| Clarity      | Requirements specific and measurable |
| Completeness | All sections present                 |
| Stories      | Acceptance criteria present          |
| Gaps         | Nothing missing or unclear           |
| Conflicts    | No contradictions                    |

---

## Output Format

```json
{
  "status": "passed" | "failed",
  "coherent": true | false,
  "issues": [
    "User story prj-epc-003 missing acceptance criteria",
    "Requirement R-005 is vague - 'fast performance' needs quantification",
    "Gap: No error handling strategy defined"
  ],
  "recommendation": "proceed" | "revise",
  "iterations": 1
}
```

---

## Examples

**Failed:**

```
Issues: prj-epc-003 missing AC, R-005 vague ("fast" needs metrics),
        No error handling, Conflict: R-002 real-time vs R-007 batch
Action: AUTO (BA fixes) or MANUAL (user guidance)?
```

**Passed:**

```
✓ Coherent ✓ Clear ✓ Complete ✓ No gaps → Proceeding to innovation
```

---

## Revision Actions

| Issue              | BA Fix                       |
| ------------------ | ---------------------------- |
| Missing AC         | Add to affected stories      |
| Vague requirements | Quantify with metrics        |
| Conflicts          | Resolve (ask user if needed) |
| Missing sections   | Add based on context         |
| Error handling gap | Add strategy                 |

## Integration

**Called by:** /architect (Phase 3) | **Calls:** vibe-check MCP, business-analyst, AskUserQuestion
**Flow:** requirements-phase → vibe-check → innovate-phase (success) OR requirements-phase (failure, max 2 loops)

**Notes:** Fast single MCP call. Validates coherence/clarity, not technical feasibility (architect's job). Escalate to user after 2 failed iterations.

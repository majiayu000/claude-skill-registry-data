---
name: requirements-phase
description: PRD creation with EA agent using AskUserQuestion for clarification, validation with reviewer, then BA extracts stories. NO HITL in this phase - continues to design-phase.
---

# Requirements Phase - PRD + Epic/Story Creation

> **ROOT AGENT ONLY** - Called by commands only, always invoked at root level.

**Purpose:** Create PRD (EA with AskUserQuestion), validate (reviewer), extract stories (BA)
**Trigger:** After analysis-phase completes
**Input:** prompt, complexity, tools, scope
**Output:** PRD + Epics + User Stories (NO HITL - continues to design-phase)

---

## Workflow

```
1. Check/Create Project Folder
         │
         ▼
2. Spawn EA Agent ──► AskUserQuestion until 100% understood
         │              ──► Creates PRD (prd-creation skill)
         │
         ▼
3. Spawn Reviewer ──► Validates PRD (document-validation)
         │              ──► If invalid: return to EA with issues
         │
         ▼
4. Spawn BA Agent ──► Creates story outlines
         │
         ▼
5. Continue to design-phase (NO HITL HERE)
```

### Step 1: Project Folder

- Glob `docs/epics/*` for existing folders
- Reuse or create: `docs/epics/{PREFIX}{NNN}-{name}/`

### Step 2: EA Agent (PRD)

Spawn: `core-claude-plugin:generic:enterprise-architect`

- Analyze prompt; investigate codebase (audits)
- **Use AskUserQuestion tool** until 100% understanding achieved
- Draft PRD using `/skill prd-creation`
- Save to `{projectFolder}/prd.md`

**IMPORTANT:** EA asks clarifying questions via AskUserQuestion (NOT HITL). This is iterative clarification, not approval.

### Step 3: Reviewer (Validation)

Spawn: `core-claude-plugin:generic:reviewer`

- Use `/skill document-validation` to validate PRD
- If invalid: return to EA with issues (loop until valid)

### Step 4: BA Agent (Stories)

Spawn: `core-claude-plugin:generic:business-analyst`

- Mode: `extract-stories`
- Create `{projectFolder}/user-stories/`
- Create epics then stories (ALWAYS at least 1 epic)

| Complexity | Epics |
| ---------- | ----- |
| < 15       | 1     |
| 15-29      | 1-2   |
| 30-44      | 2-3   |
| >= 45      | 3+    |

### Step 5: Continue to Design Phase

**NO HITL in this phase.** Proceed directly to design-phase.

HITL approval happens AFTER design-phase completes (single approval for PRD + execution plan + stories).

---

## Agent Summary

| Step | Agent                | Mode            | Output          |
| ---- | -------------------- | --------------- | --------------- |
| 2    | enterprise-architect | create-prd      | PRD draft       |
| 3    | reviewer             | validate        | Validation      |
| 4    | business-analyst     | extract-stories | Epics + Stories |

---

## Story Consolidation

**ONE story per target file.** Consolidate multiple requirements for same file.

---

## Audit Mode

EA prioritizes codebase investigation before questions:

- Use Serena tools (package.json, configs, structure)
- Classify repos via `metasaver.projectType`
- Minimize clarification questions

---

## Output Format

```json
{
  "status": "complete",
  "projectFolder": "docs/epics/msm007-feature",
  "prdPath": "docs/epics/msm007-feature/prd.md",
  "prdApproved": true,
  "epics": [{ "id": "msm-feat", "title": "...", "stories": ["msm-feat-001"] }],
  "stories": [{ "id": "msm-feat-001", "epic": "msm-feat", "agent": "..." }]
}
```

---

## Integration

**Called by:** /audit, /build, /architect, /ms
**Spawns:** enterprise-architect, reviewer, business-analyst
**Calls:** `/skill prd-creation`, `/skill document-validation`, `/skill user-story-template`
**Next:** design-phase (architect enriches stories, then single HITL for all docs)

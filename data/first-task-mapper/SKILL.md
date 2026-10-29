---
name: first-task-mapper
description: Use when someone asks to plan a vague task, break down a request, map what's needed to complete something, says "I need to do X but I'm not sure how," or submits a vague or incomplete work request. Converts vague requests into clear execution maps.
argument-hint: [vague request or task description]
allowed-tools: Read, Glob, Grep, Skill
---

## What This Skill Does

Converts a vague work request into a clear, safe execution map. For each field in the map, it labels the confidence level so the employee can distinguish verified facts from missing information. Finishes with a readiness decision and a recommended next action. The skill plans only — it never executes the mapped task.

## Process

Ask clarifying questions via AskUserQuestion (with drafted, plausible options plus a free-text "Other") to fill in each field. Label every important field as one of:

- **Confirmed** — The employee explicitly confirmed this
- **Assumption** — Reasonable inference, not yet confirmed
- **Unknown** — Cannot be determined from available information
- **Not confirmed** — Exists but not yet verified with the employee

If $ARGUMENTS is provided, use it as the initial request. Otherwise ask the employee to describe their request.

### Step 1: Restate & Confirm

Restate your understanding of the request back to the employee. Confirm via AskUserQuestion: "Is this correct?" with options "Yes, that's correct", "No, let me clarify", and "Partially — some details need fixing". If not fully confirmed, clarify before proceeding.

### Step 2: Identify Business Goal

Ask via AskUserQuestion: "What is the real goal here — what problem are you trying to solve?" Draft 2-4 plausible goals grounded in the restated request from Step 1 (e.g. for a report request: "Track performance over time", "Support a specific decision", "Meet a compliance/reporting requirement", "Share status with stakeholders") — the tool always adds a free-text "Other" option too.

Label: Confirmed / Assumption / Unknown

### Step 3: Define Expected Result & Output Format

Ask via AskUserQuestion: "What should the final result look like?" with options "A report or document", "A list or table", "A file (specify format)", and "An email or message".

Label: Confirmed / Assumption / Unknown

### Step 4: Identify Source of Truth

Check project files for hints first (CLAUDE.md, configs) — do not guess, but use any hint found as the first, recommended option. Ask via AskUserQuestion: "Where does the data live?" with options "A database", "A spreadsheet", "A file", and "A person or team".

Label: Confirmed / Assumption / Unknown

### Step 5: Identify Required MCP Connector

Inspect MCP configuration files (read-only) to see what connectors exist. Report safe details only:
- Connector name
- Whether configuration appears present

**NEVER display raw config values, passwords, API keys, tokens, or connection strings.**

If the needed connector does not appear configured, flag it: "No matching MCP connector detected — this may block execution."

Label: Confirmed / Assumption / Unknown / Not confirmed

### Step 6: Check for Existing Skill or SOP

Delegate this check to `existing-asset-finder` (pass the restated request from Step 1 as its input) rather than re-scanning `.claude/skills/` independently — it owns overlap discovery project-wide, per the precedent `record-a-skill-custom` already established. Use its REUSE/EXTEND/MERGE/CREATE/STOP recommendation to fill this field: REUSE or EXTEND means a matching skill exists (note it); CREATE means none exists; MERGE or STOP should be flagged to the employee directly rather than silently folded into this map.

Label: Confirmed / Assumption / Unknown

### Step 7: Define Allowed Actions & Permissions

Check CLAUDE.md for documented rules first. Ask via AskUserQuestion: "What are you allowed to do — any restrictions on what Claude can modify?" with options "No restrictions beyond standard safety rules", "Read-only — no changes without my approval", "Specific folders/files are off-limits", and "Need to check with my manager first".

Label: Confirmed / Assumption / Unknown | Use "Not confirmed" rather than inventing a permission.

### Step 8: Define Validation Method

Ask via AskUserQuestion: "How will you check the output is correct?" with options "I'll review it manually", "Compare against a specific reference or example", "An automated check (tests/script)", and "Not sure yet".

Label: Confirmed / Assumption / Unknown | Use "Not confirmed" rather than inventing a validation rule.

### Step 9: Identify Reviewer & Completion Evidence

Ask via AskUserQuestion, as two questions in one call: "Who needs to review the result?" (options: "Just me", "My manager or lead", "The original requester", "A specific team") and "What counts as done?" (options: "Reviewer approval", "Meets the stated validation criteria", "Delivered to the stated location", "Not sure yet").

Label: Confirmed / Assumption / Unknown / Not confirmed — use "Not confirmed" rather than inventing a reviewer.

### Step 10: Identify Edge Cases & Alternate Paths

Ask via AskUserQuestion: "Are there edge cases or alternate paths this needs to handle — partial/missing data, error states, more than one valid way to do this?" with options "No unusual cases — straightforward", "Yes — I'll describe them", and "Not sure yet".

Label: Confirmed / Assumption / Unknown

### Step 11: Readiness Decision

Based on all labeled fields, determine readiness:

| Decision | Meaning |
|----------|---------|
| **READY** | All critical fields confirmed |
| **READY WITH ASSUMPTIONS** | Some fields are assumptions — proceed with caution |
| **BLOCKED** | Critical fields unknown — cannot proceed |
| **NEEDS APPROVAL** | Permissions or reviewer not confirmed |
| **NEEDS CONNECTOR** | Required MCP connector not found |
| **NEEDS SOURCE CONFIRMATION** | Data source not confirmed |

Add one recommended next action based on the decision.

## Output Format

After gathering all information, present the execution map in chat using this structure:

```
## Execution Map: [task name]

**Request:** [restated request] — [Confirmed]

### Business Goal
[goal] — [Confirmed/Assumption/Unknown]

### Expected Result
[result and format] — [Confirmed/Assumption/Unknown]

### Source of Truth
[data source] — [Confirmed/Assumption/Unknown]

### Required MCP Connector
[connector] — [Confirmed/Assumption/Unknown/Not confirmed]

### Existing Skill or SOP
[skill name or "None found"] — [Confirmed/Assumption/Unknown]

### Allowed Actions & Permissions
[permissions] — [Confirmed/Assumption/Unknown/Not confirmed]

### Validation Method
[criteria] — [Confirmed/Assumption/Unknown/Not confirmed]

### Reviewer & Completion Evidence
[reviewer and evidence] — [Confirmed/Assumption/Unknown/Not confirmed]

### Edge Cases & Alternate Paths
[cases, or "None identified"] — [Confirmed/Assumption/Unknown]

### Readiness Decision: **[DECISION]**

**Recommended next action:** [one concrete step]
```

After showing the map in chat, ask via `AskUserQuestion`: *"Does this look correct? I can save it to `output/first-task-mapper/` for your records."* — options **Yes, save it (Recommended)** / **No, let me fix something first**. If they want changes, clarify as free text what to fix, update the map, and ask again.

Write only after the user explicitly confirms. When saving, use the file path:

`output/first-task-mapper/[task-name]-execution-map.md`

Write only inside `output/first-task-mapper/` — never elsewhere.

## Notes

- NEVER execute the mapped task — this skill only creates the plan
- NEVER modify project files, .claude/ configuration, MCP settings, or any project source
- NEVER display raw config values, passwords, API keys, tokens, or connection strings
- NEVER assume a reviewer, source, permission, or validation rule — use "Not confirmed" instead
- NEVER write outside `output/first-task-mapper/`
- Always show the execution map in chat first; save to file only after user confirms
- If the request is too vague, ask focused clarifying questions — never guess
- Inspect CLAUDE.md and existing skills before suggesting new workflows
- If project documentation is missing, flag it as a limitation and continue with questions
- Clickable-question convention: Steps 1-10 already use `AskUserQuestion` with drafted plausible options plus a free-text "Other". Converted the remaining plain-text save confirmation. Only the initial request description (when `$ARGUMENTS` is absent) and any "Other"/fix-up follow-ups stay free text.

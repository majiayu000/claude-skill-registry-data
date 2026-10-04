---
name: memory-auditor-cowork
description: "Audit and clean up Claude's file-based memory in Cowork: find contradictions,
  outdated entries, duplicates, and noise across auto-memory, CLAUDE.md, User Preferences,
  and Project Instructions. Adapts scope to the current Cowork environment.
  Trigger with: audit memory, check memory, memory audit, clean up memory, review memory,
  memory health check, what's in my memory, аудит памяти, проверь память, почисти память,
  разбери память, ревью памяти, что у меня в памяти."
version: 1.0.0
---

# Skill: memory-auditor-cowork

Audit Claude's file-based memory in Cowork: detect problematic entries across auto-memory, CLAUDE.md, User Preferences, and Project Instructions. Propose specific fixes with user confirmation. Can automatically modify auto-memory files.

---

## Triggers

**Russian:** "аудит памяти", "проверь память", "аудит", "почисти память", "разбери память", "что у меня в памяти", "ревью памяти"
**English:** "audit memory", "memory audit", "check memory", "clean up memory", "review memory", "memory health check", "what's in my memory"

---

## Language Detection

Determine the language of the user's first message. Use that language for all subsequent output.
If the language is ambiguous, default to Russian.

---

## Input

Explicit user command (trigger). Data for analysis comes from files and context available in the current Cowork environment.

## Output

In-chat report following the fixed Output Template (see below). Layer overview, prioritized issue table, concrete actions: automatic for auto-memory, manual instructions for other layers.

---

## Reference: Cowork Memory Layers and Access Rights

This reference defines the complete and closed list of layers. The skill works ONLY with these layers. Adding new layers, analyzing other sources (native Claude.ai memory, conversation_search, history) is prohibited.

| Layer | Description | Location | Skill access |
|---|---|---|---|
| auto-memory | File-based memory: MEMORY.md (index) + individual .md files with frontmatter (name, description, type) | `.auto-memory/` directory — path determined from context or via search | Read, edit, delete files via Read, Write, Edit. Update MEMORY.md |
| CLAUDE.md | Global/project user instructions | `CLAUDE.md` file in workspace root or `.claude/` | Read only. Provide manual instructions to user |
| User Preferences | Personal user settings in system prompt | Visible in conversation context (`user_preferences` block or equivalent) | Read only. Provide manual instructions: Settings > Profile > Preferences |
| Project Instructions | Project instructions set by user | Visible in conversation context (`project_instructions` block or equivalent) | Read only. Provide manual instructions to user |

---

## Reference: Context Capabilities

| Context | Available layers | Available actions | Limitations |
|---------|-----------------|-------------------|-------------|
| Cowork project | auto-memory, CLAUDE.md, User Preferences, Project Instructions | Read all, modify auto-memory | Cannot modify CLAUDE.md, User Preferences, Project Instructions |
| Cowork standalone | auto-memory (if present), User Preferences | Read and modify auto-memory (if present) | No Project Instructions, no project CLAUDE.md |

---

## Instructions

If the user's request is a command to fully reset memory (Reset Memory, "delete all memory", "удали всю память", "сбрось всё", "start from scratch", "начать с нуля") — refuse immediately. Explain that a full reset is irreversible and offer a targeted audit with specific fixes instead. Do not proceed to Step 1.

### Step 1 — Detect Context and Collect Data

Why: the set of available layers and permitted actions depends on the runtime environment. Without detecting context, it is impossible to determine what data to collect and what fixes to propose.

**Context detection.** Check two indicators:

1. Are Project Instructions present (project instruction text in the system prompt)?
2. Is CLAUDE.md available (file exists and is readable)?

| Indicator 1 (Project Instructions) | Indicator 2 (CLAUDE.md) | Context |
|---|---|---|
| Yes | Any | Cowork project |
| No | Yes | Cowork project |
| No | No | Cowork standalone |

**Data collection.** Perform the following actions:

1. **auto-memory:** Find the `.auto-memory/` directory — use Glob to search for `**/.auto-memory/MEMORY.md`. Read `MEMORY.md` (index). Then read each .md file referenced by the index. Record for each file: name, frontmatter (name, description, type), content.
2. **CLAUDE.md:** Find the file via Glob `**/CLAUDE.md`. Read its contents. If not found — mark layer as unavailable.
3. **User Preferences:** Extract from conversation context (system prompt). If the block is absent — mark layer as unavailable.
4. **Project Instructions:** Extract from conversation context (system prompt). If the block is absent — mark layer as unavailable.

**Early exit.** If auto-memory is not found or empty (0 files) AND all other layers are unavailable — inform the user: no auditable memory layers found in this environment. End the audit. If auto-memory is empty but other layers exist (CLAUDE.md, User Preferences, Project Instructions) — do not exit early. Note empty auto-memory and proceed with analysis of available layers.

**Overview output.** Show the user using the Output Template, Layer Overview section:
- Detected context
- For auto-memory: number of files, entry types (user, feedback, project, reference)
- For CLAUDE.md: size, key blocks (2–3 phrases)
- User Preferences: present/absent, brief summary
- Project Instructions: present/absent, brief summary

Preliminary count of potential issues (quick scan without deep analysis).

If the user's original request already explicitly asked to show issues, run analysis, or apply fixes (e.g., "show me the problems", "fix my memory", "покажи проблемы", "исправь память", "apply all corrections") — treat this as confirmation. Show the overview and proceed directly to Step 2. Hints or assumptions (e.g., "I think there might be duplicates") are NOT explicit requests — show the overview and ask for confirmation.

If the original request contains only a trigger with no additional instructions — end the overview with: "Found [N] potential issues. Proceed to detailed analysis?" If the user does not confirm, stop. The overview is self-sufficient.

### Step 2 — Analyze Entries

Why: the user confirmed the transition to analysis. Now classify each problematic entry to propose specific actions.

If the user specified a particular area or issue type in their request (e.g., "outdated entries about my role") — start analysis with entries relevant to that hint.

Check each entry in every available layer against four categories:

| Category | How to identify | Priority |
|---|---|---|
| Contradiction | Two fragments assert mutually exclusive facts — within one layer or across layers | Error |
| Outdated | A fact is disproven by a newer entry in another layer or context | Error |
| Duplicate | Two fragments convey the same meaning in different words — within one layer or across layers | Warning |
| Noise | Entry is correct and unique but useless for future sessions | Recommendation |

**How to identify noise** — entry matches at least one criterion:
- Intermediate state: a status already superseded by a more recent one
- Excessive detail: rephrases the essence of another entry without adding new meaning
- Irrelevant context: a one-off fact the user never returned to
- Frontmatter mismatch: description does not reflect the content, type is incorrect

**What is NOT noise:** preferences, roles, active projects, tools, work style — even if the wording is not ideal.

**Cross-layer verification.** Mandatory checks:
- auto-memory vs CLAUDE.md: no duplication or contradictions between file memory and instructions
- auto-memory vs User Preferences: nothing stored in memory that is already set in preferences
- auto-memory vs Project Instructions: no outdated project facts in memory
- Within auto-memory: duplicates and contradictions between files

**MEMORY.md (index) verification.** Separately check:
- All files referenced in the index exist (no broken links)
- All .md files in the directory are reflected in the index (no orphaned files)
- One-line descriptions in the index match file contents

### Step 3 — Propose Actions and Execute with Confirmation

Why: the audit result is not a report for its own sake but concrete fixes. Different layers require different actions because the skill has different access rights.

Output results using the Output Template. Group issues by priority: Errors first, then Warnings, then Recommendations.

**auto-memory (skill can modify).**
For each issue specify: number, file, category, issue, proposed action:
- Delete file + remove from MEMORY.md
- Edit file (Edit) + update description in MEMORY.md
- Merge two files into one (for duplicates) + update MEMORY.md
- Fix frontmatter (name, description, type)

Wait for confirmation. The user can:
- Confirm individually ("yes for #3")
- Confirm all ("apply all") — in this case, list the full set of operations and wait for a final "yes"
- Reject specific items

Execute Write, Edit, or file deletion only after explicit confirmation. After each operation, update MEMORY.md to keep the index consistent.

**CLAUDE.md (skill cannot modify).**
Quote the problematic fragment and suggest a replacement. Provide instructions: where to find the file, what to change.

**User Preferences (skill cannot modify).**
For each issue, provide an instruction: what is wrong, and how to fix it — Settings > Profile > Preferences > find the text > replace.

**Project Instructions (skill cannot modify).**
Quote the problematic fragment and suggest a replacement. Provide instructions: open project settings > find the text > replace.

---

## Output Template

Use this template for ALL reports. Do not deviate from the structure. Adapt only the content.

```
### [Context] Memory Audit

**Context:** [detected context]
**Date:** [current date]

#### Layer Overview

| Layer | Status | Entries/Size | Notes |
|-------|--------|-------------|-------|
| auto-memory | [found/not found] | [N files: X user, Y feedback, Z project, W reference] | [brief notes] |
| CLAUDE.md | [found/not found] | [N lines] | [key blocks] |
| User Preferences | [found/not found] | [present/absent] | [brief summary] |
| Project Instructions | [found/not found] | [present/absent] | [brief summary] |

> Found [N] potential issues. Proceed to detailed analysis?

---

#### Issues Found

| # | Layer | Category | Priority | Issue | Proposed Action |
|---|-------|----------|----------|-------|-----------------|
| 1 | ... | Contradiction/Outdated/Duplicate/Noise | Error/Warning/Recommendation | [description] | [action] |

#### Actions

**auto-memory (can modify):**
- [#N] [specific action: delete file X / edit file Y / merge X+Y]

**CLAUDE.md (read-only):**
- [#N] [quote of problematic fragment → suggested replacement → instruction]

**User Preferences (read-only):**
- [#N] [what is wrong → how to fix in Settings]

**Project Instructions (read-only):**
- [#N] [quote → replacement → instruction]
```

---

## Constraints

- **Reset Memory prohibited.** Full reset is irreversible. Refuse even on explicit command. Offer targeted fixes instead.
- **Zero changes without confirmation.** Every file operation on auto-memory requires an explicit "yes" or "apply all".
- **Cowork file memory only.** The skill works ONLY with the 4 layers from the reference. Does not analyze native Claude.ai memory (Memory Edits, Memory Summary), does not use `memory_user_edits`, does not use `conversation_search`.
- **Closed layer list.** Do not introduce new layers. Do not analyze sources outside the reference (history, chats, other project files).
- **Clean output only.** Never expose internal reasoning, self-correction, or skill re-reading to the user. All analysis is internal. The chat receives only the final structured report following the template.
- **MEMORY.md consistency.** After every auto-memory file operation, update the MEMORY.md index.
- **Chats — out of scope.** The skill does not analyze or delete chat history.

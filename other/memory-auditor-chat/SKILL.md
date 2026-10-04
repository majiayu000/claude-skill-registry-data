---
name: memory-auditor-chat
description: "Audit and clean up Claude's native memory in Claude.ai: find contradictions,
  outdated entries, duplicates, and noise across all memory layers. Adapts scope to the
  current context (general chat / project).
  Trigger with: audit memory, check memory, memory audit, clean up memory, review memory,
  memory health check, what's in my memory, аудит памяти, проверь память, почисти память,
  разбери память, ревью памяти, что у меня в памяти."
version: 1.0.0
---

# Skill: memory-auditor-chat

Audit Claude's native memory in Claude.ai: detect problematic entries across all available memory layers and propose specific fixes with user confirmation. Works in general chat and projects.

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

Explicit user command (trigger). Data for analysis comes from Claude's native memory layers available in the current context.

## Output

In-chat report following the fixed Output Template (see below). Layer overview, prioritized issue table, concrete actions: automatic for Memory Edits, manual instructions for other layers.

---

## Reference: Memory Layers and Access Rights

This reference defines the complete and closed list of layers. The skill works ONLY with these layers. Adding new layers, analyzing other sources (file-based auto-memory, CLAUDE.md, User Preferences from Cowork) is prohibited.

| Layer | Description | Skill access |
|---|---|---|
| Memory Edits | Explicit user entries ("remember X"). Scoped: in-project entries are project-only, outside project — global. Limit: 30 entries | Read, remove, replace via `memory_user_edits` |
| Memory Summary | Auto-synthesized from chat history (~every 24h). Global + per-project | Read only. Provide manual instructions to user |
| Project Summary | Auto-synthesized from project chats. Cannot be edited directly | Read only. Inform user about issues |
| Project Instructions | Manual text in project settings (Edit Project) | Read only. Provide manual instructions to user |

---

## Reference: Context Capabilities

| Context | Available layers | Available actions | Limitations |
|---------|-----------------|-------------------|-------------|
| General chat (Claude.ai) | Memory Edits, Memory Summary | Read all, modify Edits | No project layers |
| Project (Claude.ai) | Memory Edits, Memory Summary, Project Summary, Project Instructions | Read all, modify Edits | Cannot modify Summary/Instructions |

---

## Instructions

If the user's request is a command to fully reset memory (Reset Memory, "delete all memory", "удали всю память", "сбрось всё", "start from scratch", "начать с нуля") — refuse immediately. Explain that a full reset is irreversible and offer a targeted audit with specific fixes instead. Do not proceed to Step 1.

### Step 1 — Detect Context, Check Tools, and Collect Data

Why: the set of available layers and permitted actions depends on the runtime environment. Without detecting context, it is impossible to determine what data to collect and what fixes to propose.

**Tool availability check.** Before any actions, verify whether the `memory_user_edits` tool is available:
- If available — proceed as normal (full read/write access to Memory Edits).
- If NOT available — switch to read-only audit mode. Analyze only the layers visible in the current context: Project Instructions, Project Summary (if present), Memory Summary (if visible). Inform the user once: "The memory_user_edits tool is not available in this environment. Auditing available layers in read-only mode." Do NOT refuse to work. Do NOT suggest switching to another application.

**Context detection.** Check two indicators in the system prompt and conversation context:

1. Is there a project instruction (user-defined text in the system prompt via Edit Project)?
2. Is there a project summary (automatic block labeled "project summary" or "project context")?

| Indicator 1 (instruction) | Indicator 2 (project summary) | Context |
|---|---|---|
| Yes | Any | Claude.ai project |
| No | Yes | Claude.ai project |
| No | No | General chat |

**Data collection.** Call `memory_user_edits view` (if tool is available) and record all entries. Read Memory Summary from the context. If in a project, read Project Summary and Project Instructions from the system prompt.

**Early exit.**
- If `memory_user_edits` is available, memory edits is empty (0 entries), and Memory Summary is absent or minimal:
  - If in a project context and Project Summary or Project Instructions exist — skip early exit. Show the overview noting empty memory edits and Memory Summary, but indicate that project layers are available for analysis. Proceed as normal.
  - If in general chat — inform the user: memory is empty or contains minimal data, no issues found. End the audit.
- If `memory_user_edits` is NOT available and Memory Summary is absent:
  - If in a project context and Project Summary or Project Instructions exist — skip early exit. Note unavailable Memory Edits, proceed with project layer analysis.
  - If no project layers either — inform the user: no auditable memory layers found in this environment. End the audit.

**Overview output.** Show the user using the Output Template, Layer Overview section:
- Detected context
- Number of Memory Edits (or "tool unavailable")
- Key Memory Summary themes (2-3 phrases, do not retell everything)
- If in a project: presence of Project Summary and Project Instructions

Preliminary count of potential issues (quick scan without deep analysis).

If the user's original request already explicitly asked to show issues, run analysis, or apply fixes (e.g., "show me the problems", "fix my memory", "apply all corrections", "покажи проблемы", "исправь память", "примени все правки") — treat this as confirmation. Show the overview and proceed directly to Step 2. Hints or assumptions (e.g., "I think there might be duplicates") are NOT explicit requests — show the overview and ask for confirmation.

If the original request contains only a trigger with no additional instructions — end the overview with: "Found [N] potential issues. Proceed to detailed analysis?" If the user does not confirm, stop. The overview is self-sufficient.

### Step 2 — Analyze Entries

Why: the user confirmed the transition to analysis. Now classify each problematic entry to propose specific actions.

If the user specified a particular area or issue type in their request (e.g., "outdated entries about my role") — start analysis with entries relevant to that hint.

Check each entry in every available layer against four categories:

| Category | How to identify | Priority |
|---|---|---|
| Contradiction | Two entries assert mutually exclusive facts — within one layer or across layers | Error |
| Outdated | A fact is disproven by a newer entry in another layer or in chat history | Error |
| Duplicate | Two entries convey the same meaning in different words — within one layer or across layers | Warning |
| Noise | Entry is correct and unique but useless for future sessions | Recommendation |

**How to identify noise** — entry matches at least one criterion:
- Intermediate state: a status already superseded by a more recent one ("Project X in Draft" when "Project X — Active" exists)
- Excessive detail: rephrases the essence of another entry without adding new meaning
- Irrelevant context: a one-off question the user never returned to

**What is NOT noise:** preferences, roles, active projects, tools, work style — even if the wording is not ideal.

**Cross-layer verification.** Mandatory checks:
- Memory Edits vs Memory Summary: no duplication or contradictions
- Memory Edits vs Project Instructions: no outdated project facts in memory
- Memory Summary vs Project Summary: no discrepancies in auto-synthesis
- Within Memory Edits: duplicates and contradictions between entries

If fact verification is needed (is it outdated?) — use `conversation_search` for targeted checks. No more than 5 queries per audit. Formulate queries narrowly: specific fact, name, date.

### Step 3 — Propose Actions and Execute with Confirmation

Why: the audit result is not a report for its own sake but concrete fixes. Different layers require different actions because the skill has different access rights.

Output results using the Output Template. Group issues by priority: Errors first, then Warnings, then Recommendations.

**Memory Edits (skill can modify).**
Output a table of problematic entries: number, entry text, category, issue, proposed action (delete / replace with [new text]).

Wait for confirmation. The user can:
- Confirm individually ("yes for #3")
- Confirm all ("apply all") — in this case, list the full set of operations and wait for a final "yes"
- Reject specific items

Execute `remove` or `replace` via `memory_user_edits` only after explicit confirmation.

If `memory_user_edits` is not available — for each Memory Edits issue, provide manual instructions: Settings > Memory > find the entry > delete/edit. Or via chat: "Forget that [old fact]", then "Remember that [new fact]".

**Memory Summary (skill cannot modify).**
For each issue, provide an instruction: what exactly is wrong, and two ways to fix it — via Settings > Memory (find the entry, edit or delete) or via chat ("Forget that [old fact]", then "Remember that [new fact]").

**Project Summary (skill cannot modify, user cannot directly either).**
Inform about the issue. Explain: this is auto-generated and will update at the next synthesis. The only way to influence it is to delete the source chat, but this is irreversible.

**Project Instructions (skill cannot modify).**
Quote the problematic fragment and suggest a replacement. Provide instructions: open project > Edit project > find the text > replace.

**Chat History (optional).**
If verification via `conversation_search` revealed chats that are sources of noise or contradictions — list them with a recommendation. The skill does not delete chats.

---

## Output Template

Use this template for ALL reports. Do not deviate from the structure. Adapt only the content.

```
### [Context] Memory Audit

**Context:** [detected context]
**Date:** [current date]

#### Layer Overview

| Layer | Status | Entries | Notes |
|-------|--------|---------|-------|
| Memory Edits | [found / unavailable] | [N entries] | [brief notes] |
| Memory Summary | [found / not found] | [present / absent] | [key themes] |
| Project Summary | [found / not found / N/A] | [present / absent] | [brief summary] |
| Project Instructions | [found / not found / N/A] | [present / absent] | [brief summary] |

> Found [N] potential issues. Proceed to detailed analysis?

---

#### Issues Found

| # | Layer | Category | Priority | Issue | Proposed Action |
|---|-------|----------|----------|-------|-----------------|
| 1 | ... | Contradiction/Outdated/Duplicate/Noise | Error/Warning/Recommendation | [description] | [action] |

#### Actions

**Memory Edits (can modify):**
- [#N] [specific action: delete entry X / replace entry Y with Z]

**Memory Summary (read-only):**
- [#N] [what is wrong -> how to fix in Settings or via chat]

**Project Summary (read-only):**
- [#N] [what is wrong -> explanation of update mechanism]

**Project Instructions (read-only):**
- [#N] [quote of problematic fragment -> suggested replacement -> instruction]
```

---

## Constraints

- **Reset Memory prohibited.** Full reset is irreversible. Refuse even on explicit command. Offer targeted fixes instead.
- **Zero changes without confirmation.** Every memory edit operation requires an explicit "yes" or "apply all".
- **Claude.ai native memory only.** The skill works ONLY with the 4 layers from the reference. Does not analyze file-based auto-memory, CLAUDE.md, User Preferences from Cowork, or local files.
- **Closed layer list.** Do not introduce new layers. Do not analyze sources outside the reference (userPreferences, history, etc.).
- **Verification limit.** No more than 5 `conversation_search` calls per audit.
- **Chats — recommendations only.** The skill cannot delete chats.
- **Clean output only.** Never expose internal reasoning, self-correction, or skill re-reading to the user. All analysis is internal. The chat receives only the final structured report following the template.
- **Fixed template.** Report format is fixed by the Output Template. Do not change structure, headings, or section order between runs.

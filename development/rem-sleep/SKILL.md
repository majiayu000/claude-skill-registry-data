---
name: rem-sleep
description: "Extracts and persists memories from the current conversation to the database. Scans for decisions, preferences, patterns, issues, and learnings, then dispatches the memory-extractor agent. Use manually via /rem-sleep or triggered automatically before context compaction."
---

# REM Sleep - Memory Extraction

## Purpose

Scan the current conversation for valuable information worth persisting, categorize it, and dispatch the memory-extractor agent to write it to the `memories` table.

## Trigger

- Manual: user invokes `/rem-sleep`
- Automatic: PreCompact hook outputs a reminder, Claude invokes this skill

## Data Storage Rules

- NEVER write memory data to local files — all memory goes to the `memories` table
- Use ToolSearch to discover Supabase MCP tools for INSERT/UPDATE operations
- Temp files in /tmp/ are acceptable for transient processing

## Execution

### 1. Determine Project Name

```bash
git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||' || basename "$PWD"
```

Normalize to lowercase with hyphens.

### 2. Scan Conversation

Review the entire conversation for extractable items in these categories:

| Category | What to Look For | DB category | DB subcategory |
|----------|-------------------|-------------|----------------|
| **Decisions** | Architectural choices, library selections, pattern choices | `decision` or `project` | NULL or `<project>` |
| **Preferences** | User's stated preferences for style, tooling, workflow | `preference` | NULL or topic |
| **Patterns** | Recurring approaches, idioms, code patterns used | `knowledge` | `<topic>` |
| **Issues** | Bugs found, workarounds discovered, gotchas | `project` | `<project>` |
| **Learnings** | New knowledge gained, framework behaviors, API quirks | `knowledge` | `<topic>` |

### 3. Categorize and Deduplicate

For each extracted item:
- Assign category and subcategory
- Write a concise key (slugified, 2-6 words, e.g., `zustand-over-redux`)
- Distill content (value field) to factual essence (no commentary)
- Assign confidence level:
  - `high`: explicitly stated by user or confirmed through implementation
  - `medium`: inferred from conversation patterns
  - `low`: mentioned once, possibly context-dependent
- Assign relevant tags
- Set source to `rem-sleep`

### 4. Dispatch Memory Extractor

Launch the `memory-extractor` agent with the categorized items:

```
Use the Task tool with subagent_type "general-purpose" to run the memory-extractor agent.
Provide the list of categorized memory items as structured input.
```

### 5. Report Results

**If manually invoked (`/rem-sleep`):**
Output a brief summary:
```
Memories extracted:
- 2 decisions (project-specific)
- 1 preference (cross-project)
- 1 knowledge item (TypeScript patterns)
```

**If hook-triggered (PreCompact):**
Operate silently. Do not output a summary unless errors occur.

## What NOT to Extract

- Transient debugging steps (unless they reveal a persistent gotcha)
- Code that was written and immediately discarded
- Questions the user asked that were fully resolved in-session
- Implementation details that are visible in the code itself
- Anything already stored in the memories table (check first)

## Examples

### Good Extractions

- "User prefers Zustand over Redux for state management" → category=`preference`, key=`zustand-over-redux`
- "This project uses tRPC for API layer with Zod validation" → category=`project`, subcategory=`my-app`, key=`trpc-api-layer`
- "Always run migrations before seeding in this project" → category=`project`, subcategory=`my-app`, key=`migrations-before-seeding`
- "React 19 useActionState replaces useFormState" → category=`knowledge`, subcategory=`react`, key=`useactionstate-replaces-useformstate`

### Bad Extractions

- "Fixed the typo on line 42" → too transient
- "The button component renders a `<button>` element" → obvious from code
- "User asked how to use useState" → resolved in session

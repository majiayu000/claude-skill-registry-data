---
name: memory-init
description: "Initializes project memory by scanning the current project structure, asking targeted questions, and writing structured memory records to the database. Use via /memory-init when starting work on a new project."
---

# Memory Init - Project Memory Setup

## Purpose

Set up structured memory for the current project by scanning its files, asking the user targeted questions, and writing memory records to the `memories` table.

## Trigger

- Manual: user invokes `/memory-init`

## Data Storage Rules

- NEVER write memory data to local files — all memory goes to the `memories` table
- Use ToolSearch to discover Supabase MCP tools for INSERT/UPDATE operations
- No directory creation needed — memories are database rows

## Execution

### 1. Determine Project Name

```bash
git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||' || basename "$PWD"
```

Normalize to lowercase with hyphens.

### 2. Check for Existing Memory

Query the database:

```sql
SELECT COUNT(*) FROM memories
WHERE category = 'project' AND subcategory = '<project_name>' AND deprecated = false
```

If records exist:
- Inform the user that project memory already exists
- Ask if they want to reinitialize (will update, not delete)
- If no, exit

### 3. Scan Project

Gather project information:

```bash
# Package info
cat package.json 2>/dev/null
cat Cargo.toml 2>/dev/null
cat requirements.txt 2>/dev/null
cat go.mod 2>/dev/null

# README
cat README.md 2>/dev/null

# Config files present
ls -la *.config.* .eslintrc* tsconfig* .prettierrc* Dockerfile docker-compose* .github/ 2>/dev/null

# Git info
git remote get-url origin 2>/dev/null
git branch --show-current 2>/dev/null
git log --oneline -5 2>/dev/null

# Directory structure
ls -la
ls src/ app/ lib/ 2>/dev/null
```

### 4. Dispatch Memory Initializer Agent

Launch the `memory-initializer` agent:

```
Use the Task tool with subagent_type "general-purpose" to run the memory-initializer agent.
Provide all scanned project data as structured input.
```

The agent will:
- Analyze the scan data
- Ask 5-8 targeted questions (one at a time)
- INSERT records for architecture, conventions, workflows into `memories` table
- All with category=`project`, subcategory=`<project_name>`

### 5. Confirm Completion

After the agent finishes, output:

```
Project memory initialized for "<project_name>".

Records created in memories table:
- architecture (category=project, key=architecture)
- conventions (category=project, key=conventions)
- workflows (category=project, key=workflows)

Memory will be automatically recalled in future sessions.
Run /recall to see the stored context now.
```

## Notes

- This skill is meant to be run once per project (or rarely to update)
- The agent asks questions interactively — this is not a silent operation
- Subsequent learning happens via `/rem-sleep`, not repeated `/memory-init`
- If the user has limited time, they can answer with "skip" to any question

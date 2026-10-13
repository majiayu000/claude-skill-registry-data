---
name: recall
description: "Retrieves and presents relevant memories from the database for the current project context. Queries the memories table and returns a synthesized summary. Use via /recall at the start of a session or when context is needed."
---

# Recall - Memory Retrieval

## Purpose

Retrieve relevant memories from the `memories` table for the current project context, synthesize them, and present the result as useful context.

## Trigger

- Manual: user invokes `/recall`
- Can also be invoked programmatically when context is needed

## Data Storage Rules

- NEVER read from local `~/.claude/memory/` files — all memory is in the database
- Use ToolSearch to discover Supabase MCP tools, then query the `memories` table
- Present results as synthesized context, not raw database rows

## Execution

### 1. Determine Project Name

```bash
git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||' || basename "$PWD"
```

Normalize to lowercase with hyphens.

### 2. Check Memories Exist

Query the `memories` table:

```sql
SELECT COUNT(*) FROM memories WHERE deprecated = false
```

If no memories exist:
- Inform the user: "No memories found. Run `/memory-init` to set up project memory."
- Exit

### 3. Dispatch Memory Retriever

Launch the `memory-retriever` agent:

```
Use the Task tool with subagent_type "general-purpose" to run the memory-retriever agent.
Provide the project_name and any optional query context.
```

The agent will:
- Query project-specific memories (`category = 'project' AND subcategory = '<project_name>'`)
- Query preferences (`category = 'preference'`)
- Query decisions (`category = 'decision'`)
- Query relevant knowledge (`category = 'knowledge'`)
- Filter out deprecated and low-confidence entries
- Return a synthesized markdown summary

### 4. Present Results

Output the synthesized summary from the retriever agent. The format should be:

```markdown
## Recalled Context: <project_name>

<synthesized content from memory-retriever>
```

If no relevant memories found:
```
No memories found for project "<project_name>".
Run /memory-init to set up project memory, or /rem-sleep after working to start building context.
```

## Behavior Notes

- Results are presented as context, not as commands or instructions
- The recall output helps Claude understand the project without re-discovering everything
- Keep output focused and relevant — don't dump everything, synthesize
- If the user asks a specific question, the optional query parameter helps focus retrieval

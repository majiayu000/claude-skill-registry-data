---
name: native-tools
description: Claude Code native tools reference. Prefer native tools over bash commands for file operations, search, and orchestration.
triggers:
  - "glob"
  - "grep"
  - "read file"
  - "edit file"
  - "write file"
  - "task tool"
  - "askuserquestion"
  - "native tool"
  - "bash.*find"
  - "bash.*grep"
  - "bash.*cat"
---

<objective>

Provide comprehensive guidance on Claude Code's native tools. These tools are optimized for agent use and should ALWAYS be preferred over equivalent bash commands.

</objective>

<critical_rule>

## NEVER Use Bash For These Operations

| Bad (Bash) | Good (Native) | Why |
|------------|---------------|-----|
| `find . -name "*.ts"` | `Glob({pattern: "**/*.ts"})` | Faster, respects gitignore |
| `grep -r "pattern" .` | `Grep({pattern: "pattern"})` | Structured output, pagination |
| `cat file.txt` | `Read({file_path: "file.txt"})` | Line numbers, handles images/PDFs |
| `head -n 50 file.txt` | `Read({file_path: "file.txt", limit: 50})` | Native pagination |
| `sed -i 's/old/new/'` | `Edit({old_string: "old", new_string: "new"})` | Safe, atomic, validated |
| `echo "text" > file` | `Write({file_path: "file", content: "text"})` | Permission checked |

</critical_rule>

<routing>

## Tool Categories

| Category | Reference | Tools |
|----------|-----------|-------|
| File Search | `references/file-search.md` | Glob, Grep |
| Structural Search | See `ast-grep` skill | ast-grep (sg) for AST patterns |
| File Operations | `references/file-operations.md` | Read, Edit, Write |
| User Interaction | `references/user-interaction.md` | AskUserQuestion, TodoWrite |
| Agent Orchestration | `references/orchestration.md` | Task, TaskOutput |
| External Resources | `references/external.md` | WebFetch, WebSearch, Bash |
| MCP Tools | `references/external.md` | Context7, OctoCode, Codex |

## Skill References

| Skill | When to Use |
|-------|-------------|
| `ast-grep` | Structural code patterns (function calls, imports, types) |

</routing>

<quick_reference>

## Tool Permission Matrix

| Tool | Permission Required | Description |
|------|-------------------|-------------|
| **Glob** | No | Find files by pattern |
| **Grep** | No | Search file contents |
| **Read** | No | Read file contents |
| **Edit** | Yes | Modify files |
| **Write** | Yes | Create/overwrite files |
| **AskUserQuestion** | No | Interactive questions |
| **TodoWrite** | No | Task tracking |
| **Task** | No | Spawn sub-agents |
| **TaskOutput** | No | Get agent results |
| **Bash** | Yes | Shell commands |
| **WebFetch** | Yes | Fetch URLs |
| **WebSearch** | Yes | Web search |
| **NotebookEdit** | Yes | Edit Jupyter notebooks |

</quick_reference>

<common_patterns>

## Search Then Read

```javascript
// Find files matching pattern
Glob({pattern: "src/**/*.ts"})

// Search for content (text patterns)
Grep({pattern: "function handleAuth", type: "ts"})

// Read specific file
Read({file_path: "src/auth/handler.ts"})
```

## Structural Code Search (ast-grep skill)

For complex code patterns, use `ast-grep` instead of Grep:

```bash
# Find all async functions
sg -p "async function $FUNC($$$)" -l typescript

# Find React hooks
sg -p "use$HOOK($$$)" -l tsx

# Find specific imports
sg -p 'import { $$$IMPORTS } from "react"' -l typescript
```

## Documentation Lookup (MCP skill)

**Prefer MCP tools over WebFetch for library docs:**

```javascript
// Context7 for library documentation
mcp__plugin_crew_context7__resolve-library-id({libraryName: "react-query"})
mcp__plugin_crew_context7__query-docs({
  context7CompatibleLibraryID: "/tanstack/query",
  topic: "query invalidation"
})

// OctoCode for GitHub code search
mcp__plugin_crew_octocode__githubSearchCode({
  keywordsToSearch: ["useQuery"],
  owner: "tanstack",
  repo: "query"
})

// Codex for deep reasoning
mcp__plugin_crew_codex__codex({
  prompt: "Analyze architectural trade-offs...",
  sandbox: "read-only"
})
```

## Edit Workflow

```javascript
// ALWAYS read before edit
Read({file_path: "path/to/file.ts"})

// Make targeted edit
Edit({
  file_path: "path/to/file.ts",
  old_string: "const x = 1",
  new_string: "const x = 2"
})
```

## User Decision Points

```javascript
AskUserQuestion({
  questions: [{
    question: "Which approach should we use?",
    header: "Approach",
    options: [
      {label: "Option A (Recommended)", description: "Fastest, simplest"},
      {label: "Option B", description: "More flexible"},
      {label: "Option C", description: "Most robust"}
    ],
    multiSelect: false
  }]
})
```

## Agent Orchestration

```javascript
// Launch parallel agents
Task({
  subagent_type: "Explore",
  prompt: "Find all API endpoints in src/",
  description: "Find API endpoints",
  run_in_background: true
})

// Retrieve results
TaskOutput({task_id: "abc123", block: true})
```

</common_patterns>


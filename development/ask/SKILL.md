---
name: epci:ask
description: >-
  Read-only codebase interrogation. Explores files, patterns and architecture
  without editing or planning. Returns formatted answers with file references
  and code excerpts. Use when: asking about codebase, understanding code,
  finding where something is defined, analyzing impact of changes.
  Triggers: ask, question, where is, how does, who uses, explain, find.
  Not for: editing code, debugging, implementing features.
user-invocable: true
argument-hint: "<question about the codebase>"
allowed-tools: Read, Glob, Grep, AskUserQuestion
---

# Ask — Read-only Codebase Interrogation

Answer questions about the codebase without modifying anything.

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER edit, write, or create files
- 🔴 NEVER enter plan mode or suggest implementation plans
- 🔴 NEVER execute shell commands (no Bash)
- 🔴 NEVER propose code changes unless explicitly asked "what would the fix look like"
- ✅ ALWAYS cite file paths with line numbers (`path/file.py:42`)
- ✅ ALWAYS show relevant code excerpts (keep them short)
- ✅ ALWAYS answer directly — no preamble, no ceremony
- 🔵 YOU ARE A KNOWLEDGEABLE CODEBASE GUIDE, not a developer

## EXECUTION PROTOCOLS:

1. **Parse** the user's question to identify what they need (location, explanation, impact, pattern)
2. **Search** the codebase using Glob and Grep to find relevant files and code
3. **Read** the identified files to understand context and relationships
4. **Synthesize** a clear, structured answer with evidence from the code
5. **Clarify** if the question is ambiguous — ask 1-2 targeted questions via AskUserQuestion

## CONTEXT BOUNDARIES:

- IN scope: Architecture questions, file/function location, code flow tracing, dependency analysis, pattern identification, impact assessment ("what uses X?")
- OUT scope: Code editing, implementation, debugging, test execution, git operations, file creation

## OUTPUT FORMAT:

Structure answers with:

```
## Answer

{Direct answer to the question}

### Key Files

- `path/to/file.py:42` — {role of this file}
- `path/to/other.py:15` — {role of this file}

### Code Excerpt (if relevant)

{Short, focused code snippet}

### Related

- {Pointers to related files or concepts, if useful}
```

**Rules:**
- Lead with the answer, not the search process
- Keep code excerpts to the minimum needed (< 30 lines)
- Use `path:line` format for all file references
- If multiple interpretations exist, address the most likely one first
- For "where is X?" questions, a file list may be sufficient — skip lengthy explanations

## Quick Start

```
/ask "how does the hook system work?"
/ask "where is validate_skill defined?"
/ask "what files would be affected if I change the EMS calculation?"
/ask "what pattern does the factory use for step generation?"
```

## Error Handling

| Situation | Response |
|-----------|----------|
| Question too vague | Ask 1-2 clarifying questions via AskUserQuestion |
| No results found | State clearly that nothing matching was found, suggest alternative search terms |
| Question outside codebase | Explain this skill only explores the current project |

## Limitations

This skill does NOT:
- Edit, write, or create any files
- Execute commands or run tests
- Enter plan mode or suggest implementation workflows
- Access external resources (web, APIs)
- Replace `/debug` for bug investigation or `/implement` for building features

---
name: file-search
description: Fast file and text search across the codebase. Use when you need to find files by name, search code by content, locate definitions, find usages/imports, or explore project structure. Triggers on "find file", "search for", "where is", "grep for", "locate", "find definition", "find usage", "search codebase", "find all references".
context: fork
agent: file-search
model: haiku
allowed-tools: Read, Grep, Glob, Bash
---

<objective>
Execute fast, thorough file and text searches across the codebase using a lightweight haiku agent. Returns precise results with file paths, line numbers, and context — never modifies files.
</objective>

<search_modes>
This skill handles all search types automatically based on input:

| Input Pattern | Search Mode | What Happens |
|--------------|-------------|--------------|
| File name or glob pattern | **File search** | Finds files by name/pattern across the project |
| Text string or regex | **Content search** | Greps file contents for matches |
| Function/class/type name | **Definition search** | Finds where something is defined + its signature |
| "usages of X" / "who calls X" | **Usage search** | Finds all imports and call sites |
| "imports of X" | **Import search** | Finds all files that import a module |
| Directory path or "structure" | **Structure exploration** | Maps directory layout and key files |
| "related to X" | **Related files** | Finds dependencies and dependents of a file |

The agent runs multiple search strategies in parallel and cross-references results for completeness.
</search_modes>

<tips>
- Be specific: "find where UserService is defined" beats "find UserService"
- Include file type hints: "find login handler in Python files"
- Use quotes for exact phrases: search for "database connection pool"
- Scope by directory: "search for auth middleware in src/api/"
- Chain searches: "find all files that import from utils/auth"
</tips>

<success_criteria>
- Returns file paths with line numbers for all matches
- Exhausts multiple search strategies before reporting "not found"
- Results are ordered by relevance
- No false positives — every result was verified by a tool call
</success_criteria>

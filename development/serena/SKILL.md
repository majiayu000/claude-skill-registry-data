---
name: serena
description: Semantic code search, analysis, and editing. Use for understanding code structure, finding classes/functions, refactoring, and impact analysis. Triggers on "where is this function", "show references", "analyze impact" queries
---

# Serena Tool Guide

Semantic code analysis. Searches and edits at symbol level without reading entire files.

## Core Tools

### find_symbol
Locate class, function, or variable definitions.

**Examples:**
- "Where is the UserService class defined?"
- "Find the authenticate function definition"

### search_for_pattern
Search for code patterns or strings.

**Examples:**
- "Find all TODO comments"
- "Locate all API endpoint usages"

### edit_symbol
Edit at symbol level without loading entire files.

### find_referencing_symbols
Track symbol references and dependencies.

**Examples:**
- "Show all callers of this function"
- "Find dependency chain"

## When to Use

- Large codebases (100+ files)
- Semantic search (understanding code meaning)
- Refactoring (precise edits required)
- Dependency tracking
- Code structure analysis

## Common Workflows

**Code understanding:**
1. `find_symbol` to locate main classes/functions
2. `find_referencing_symbols` to trace callers
3. Build overall understanding

**Refactoring:**
1. `find_symbol` to identify target
2. `edit_symbol` to modify
3. `find_referencing_symbols` to verify impact

**Bug fixing:**
1. `search_for_pattern` to find error-related code
2. `find_symbol` to examine details
3. `edit_symbol` to fix

## Examples

**User**: Find authentication code

**Agent**: Uses Serena to search for authentication-related code and explains

---

**User**: What calls UserService?

**Agent**: Shows all references

---

**User**: Refactor this code

**Agent**: Analyzes impact and proposes changes
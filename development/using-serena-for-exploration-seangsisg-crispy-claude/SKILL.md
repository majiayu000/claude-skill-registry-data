---
name: using-serena-for-exploration
description: Use when exploring codebases with Serena MCP tools for architectural understanding and pattern discovery - guides efficient symbolic exploration workflow minimizing token usage through targeted symbol reads, overview tools, and progressive narrowing
---

# Using Serena for Exploration

Use this skill when exploring codebases with Serena MCP tools for architectural understanding and pattern discovery.

## Core Principles

- Start broad, narrow progressively
- Use symbolic tools before reading full files
- Always provide file:line references
- Minimize token usage through targeted reads

## Workflow

### 1. Initial Discovery

**Use `list_dir` and `find_file`** to understand project structure:

```bash
# Get repository overview
list_dir(relative_path=".", recursive=false)

# Find specific file types
find_file(file_mask="*auth*.py", relative_path="src")
```

### 2. Symbol Overview

**Use `get_symbols_overview`** before reading full files:

```python
# Get top-level symbols in a file
get_symbols_overview(relative_path="src/auth/handler.py")
```

Returns classes, functions, imports - understand structure without reading bodies.

### 3. Targeted Symbol Reading

**Use `find_symbol`** for specific code:

```python
# Read a specific class without body
find_symbol(
    name_path_pattern="AuthHandler",
    relative_path="src/auth/handler.py",
    include_body=false,
    depth=1  # Include methods list
)

# Read specific method with body
find_symbol(
    name_path_pattern="AuthHandler/login",
    relative_path="src/auth/handler.py",
    include_body=true
)
```

**Name path patterns:**
- Simple name: `"login"` - matches any symbol named "login"
- Relative path: `"AuthHandler/login"` - matches method in class
- Absolute path: `"/AuthHandler/login"` - exact match within file
- With index: `"AuthHandler/login[0]"` - specific overload

### 4. Pattern Searching

**Use `search_for_pattern`** when you don't know symbol names:

```python
# Find all JWT usage
search_for_pattern(
    substring_pattern="jwt\\.encode",
    relative_path="src",
    restrict_search_to_code_files=true,
    context_lines_before=2,
    context_lines_after=2,
    output_mode="content"
)
```

**Pattern matching:**
- Uses regex with DOTALL flag (. matches newlines)
- Non-greedy quantifiers preferred: `.*?` not `.*`
- Escape special chars: `\\{\\}` for literal braces

### 5. Relationship Discovery

**Use `find_referencing_symbols`** to understand dependencies:

```python
# Who calls this function?
find_referencing_symbols(
    name_path="authenticate_user",
    relative_path="src/auth/handler.py"
)
```

Returns code snippets around references with symbolic info.

## Reporting Format

Always structure findings as:

```markdown
## Codebase Findings

### Current Architecture
- **Authentication:** `src/auth/handler.py:45-120`
  - JWT-based auth with refresh tokens
  - Session storage in Redis

### Similar Implementations
- **User management:** `src/users/controller.py:200-250`
  - Uses similar validation pattern
  - Can reuse `validate_credentials()` helper

### Integration Points
- **Middleware:** `src/middleware/auth.py:30`
  - Hook new auth method here
  - Follows pattern: check → validate → attach user
```

## Anti-Patterns

❌ **Don't:** Read entire files before understanding structure
✅ **Do:** Use `get_symbols_overview` first

❌ **Don't:** Use full file reads for symbol searches
✅ **Do:** Use `find_symbol` with targeted name paths

❌ **Don't:** Search without context limits
✅ **Do:** Use `relative_path` to restrict search scope

❌ **Don't:** Return findings without file:line references
✅ **Do:** Always include exact locations: `file.py:123-145`

## Token Efficiency

- Overview tools use ~500 tokens vs. ~5000 for full file
- Targeted symbol reads use ~200 tokens per symbol
- Pattern search with `head_limit=20` caps results
- Use `depth=0` if you don't need child symbols

## Example Session

```python
# 1. Find auth-related files
files = find_file(file_mask="*auth*.py", relative_path="src")
# → Found: src/auth/handler.py, src/auth/middleware.py

# 2. Get overview of main handler
overview = get_symbols_overview(relative_path="src/auth/handler.py")
# → Classes: AuthHandler
# → Functions: authenticate_user, validate_token

# 3. Read specific method
method = find_symbol(
    name_path_pattern="AuthHandler/authenticate_user",
    relative_path="src/auth/handler.py",
    include_body=true
)
# → Got full implementation of authenticate_user

# 4. Find who calls this
refs = find_referencing_symbols(
    name_path="authenticate_user",
    relative_path="src/auth/handler.py"
)
# → Called from: middleware.py:67, api/routes.py:123
```

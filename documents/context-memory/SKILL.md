---
name: context-memory
description: Python utility API for storing and retrieving project context in Obsidian vault markdown notes
version: 1.7.1
---

# Context Memory - Utility API Reference

Python storage utilities for capturing codebase context as Obsidian markdown notes.

## What This Is

**Pure utility functions** for storing/retrieving context:
- File analyses (summaries, functions, complexity)
- Code patterns (reusable implementations)
- Architectural decisions (with reasoning)
- Git commits (change summaries)

**Storage:** Markdown files in Obsidian vault with YAML frontmatter

## Installation

```bash
pip install python-frontmatter pyyaml
```

## Configuration

Set vault location in `core-config.yaml`:

```yaml
memory:
  enabled: true
  storage_type: obsidian
  vault: ../docs/memory
```

Or via environment variable:

```bash
PRISM_OBSIDIAN_VAULT=../docs/memory
```

## Initialize Vault

```bash
python skills/context-memory/utils/init_vault.py
```

Creates folder structure:
```
docs/memory/PRISM-Memory/
├── Files/          # File analyses
├── Patterns/       # Code patterns
├── Decisions/      # Architecture decisions
└── Commits/        # Git history
```

## API Reference

### Import

```python
from skills.context_memory.utils.storage_obsidian import (
    store_file_analysis,
    store_pattern,
    store_decision,
    recall_query,
    recall_file,
    get_memory_stats
)
```

### store_file_analysis()

Store analysis of a source file.

```python
store_file_analysis(
    file_path: str,       # Relative path from project root
    summary: str,         # Brief description
    purpose: str,         # What it does
    complexity: str,      # simple|moderate|complex
    key_functions: List[str] = None,  # Important functions
    dependencies: List[str] = None,   # External dependencies
    notes: str = None     # Additional context
)
```

**Example:**
```python
store_file_analysis(
    file_path='src/auth/jwt-handler.ts',
    summary='JWT token validation and refresh',
    purpose='Handles authentication tokens',
    complexity='moderate',
    key_functions=['validateToken', 'refreshToken', 'revokeToken'],
    dependencies=['jsonwebtoken', 'crypto'],
    notes='Uses RSA256 signing'
)
```

**Output:** `docs/memory/PRISM-Memory/Files/src/auth/jwt-handler.md`

### store_pattern()

Store reusable code pattern.

```python
store_pattern(
    name: str,           # Pattern name
    description: str,    # What it does
    category: str,       # Pattern type
    example_path: str = None,  # Where used
    code_example: str = None,  # Code snippet
    when_to_use: str = None    # Usage guidance
)
```

**Example:**
```python
store_pattern(
    name='Repository Pattern',
    description='Encapsulates data access logic in repository classes',
    category='architecture',
    example_path='src/repos/user-repository.ts',
    when_to_use='When abstracting database operations'
)
```

**Output:** `docs/memory/PRISM-Memory/Patterns/architecture/repository-pattern.md`

### store_decision()

Record architectural decision.

```python
store_decision(
    title: str,          # Decision title
    decision: str,       # What was decided
    context: str,        # Why it matters
    alternatives: str = None,  # Options considered
    consequences: str = None   # Impact/tradeoffs
)
```

**Example:**
```python
store_decision(
    title='Use JWT for Authentication',
    decision='Implement stateless JWT tokens instead of server sessions',
    context='Need to scale API horizontally across multiple servers',
    alternatives='Considered Redis sessions but adds dependency',
    consequences='Tokens cannot be revoked until expiry'
)
```

**Output:** `docs/memory/PRISM-Memory/Decisions/YYYYMMDD-use-jwt-for-authentication.md`

### recall_query()

Search all stored context.

```python
recall_query(
    query: str,          # Search terms
    limit: int = 10      # Max results
) -> List[Dict]
```

**Returns:**
```python
[
    {
        'type': 'file',  # file|pattern|decision
        'path': 'src/auth/jwt-handler.ts',
        'summary': 'JWT token validation...',
        'content': '...'  # Full markdown content
    },
    ...
]
```

**Example:**
```python
results = recall_query('authentication JWT')
for result in results:
    print(f"{result['type']}: {result['path']}")
    print(f"  {result['summary']}")
```

### recall_file()

Get analysis for specific file.

```python
recall_file(file_path: str) -> Optional[Dict]
```

**Returns:**
```python
{
    'path': 'src/auth/jwt-handler.ts',
    'summary': '...',
    'purpose': '...',
    'complexity': 'moderate',
    'key_functions': [...],
    'last_analyzed': '2025-01-05'
}
```

**Example:**
```python
analysis = recall_file('src/auth/jwt-handler.ts')
if analysis:
    print(f"Complexity: {analysis['complexity']}")
```

### get_memory_stats()

Get vault statistics.

```python
get_memory_stats() -> Dict
```

**Returns:**
```python
{
    'files_analyzed': 42,
    'patterns_stored': 15,
    'decisions_recorded': 8,
    'total_notes': 65,
    'vault_path': '/path/to/docs/memory'
}
```

## Note Structure

All notes use YAML frontmatter + markdown body:

```markdown
---
type: file_analysis
path: src/auth/jwt-handler.ts
analyzed_at: 2025-01-05T10:30:00
complexity: moderate
tags:
  - authentication
  - security
---

# JWT Handler

Brief description of the file...

## Purpose
What this file does...

## Key Functions
- validateToken()
- refreshToken()
```

## Reference Documentation

- [API Reference](./reference/commands.md) - Complete function signatures
- [Integration Examples](./reference/integration.md) - Code examples for skills

## File Structure

```
skills/context-memory/
├── SKILL.md                    # This file
├── reference/
│   ├── commands.md            # Complete API reference
│   └── integration.md         # Integration examples
└── utils/
    ├── init_vault.py          # Initialize vault
    ├── storage_obsidian.py    # Storage functions
    └── memory_intelligence.py # Confidence/decay utilities
```

## Troubleshooting

**Vault not found:**
```bash
python skills/context-memory/utils/init_vault.py
```

**Import errors:**
```bash
pip install python-frontmatter pyyaml
```

**Path issues:**
- Paths are relative to project root
- Vault path is relative to `.prism/` folder

---

**Version:** 1.7.1 - Pure utility API for Obsidian storage

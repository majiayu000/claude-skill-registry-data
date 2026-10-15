---
name: file-prompts
description: "Load prompts from external files with path expansion. Use for version-controlled prompts outside config."
context: fork
globs: []
alwaysApply: false
---

# File-Based Prompts — External Prompt Loading

Use this skill to load agent system prompts from external files instead of embedding them in config. Enables version control, sharing, and cleaner configuration.

---

## How It Works

Instead of embedding prompts in JSON:

```json
// ❌ Embedded prompt (hard to version, hard to share)
{
  "agents": {
    "hermes": {
      "prompt": "You are Hermes, the backend specialist. Your expertise is..."
    }
  }
}
```

Load from files:

```json
// ✅ File-based prompt (versioned, shareable)
{
  "agents": {
    "hermes": {
      "prompt": "file://./prompts/hermes-prompt.md"
    }
  }
}
```

---

## Supported Path Formats

| Format | Example | Resolves To |
|--------|---------|-------------|
| Relative | `file://./prompts/hermes.md` | `<project>/prompts/hermes.md` |
| Home expansion | `file://~/prompts/hermes.md` | `~/.config/opencode/prompts/hermes.md` |
| Absolute | `file:///opt/prompts/hermes.md` | `/opt/prompts/hermes.md` |

---

## Use Cases

### 1. Version Control Prompts Separately

```
project/
├── opencode.json          # Config (prompt references)
├── prompts/
│   ├── hermes-prompt.md   # Backend specialist prompt
│   ├── aphrodite-prompt.md # Frontend specialist prompt
│   └── themis-prompt.md   # Review specialist prompt
```

Prompts can be versioned independently from config.

### 2. Share Prompts Across Projects

```
~/.config/opencode/prompts/
├── hermes-prompt.md       # Shared across all projects
├── aphrodite-prompt.md
└── themis-prompt.md
```

```json
{
  "agents": {
    "hermes": {
      "prompt": "file://~/prompts/hermes-prompt.md"
    }
  }
}
```

### 3. Append Category-Specific Context

```json
{
  "categories": {
    "deep": {
      "prompt_append": "file://./prompts/deep-category-append.md"
    }
  }
}
```

Appends additional context to the category's prompt without duplicating the base prompt.

---

## Prompt File Format

Prompt files are plain markdown:

```markdown
# Hermes — Backend Specialist

You are the **BACKEND TASK IMPLEMENTER** (Hermes) called by Zeus to implement
FastAPI endpoints, services, and routers.

## Core Principles
- TDD first: write tests that fail, write minimal code to pass
- Async/await on all I/O operations
- Type hints on all parameters
- Max 300 lines per file

## Your Tools
- FastAPI, SQLAlchemy, Pydantic, Redis
- pytest for testing
- ruff for linting

## When to Delegate
- @apollo for codebase discovery
- @themis for code review
- @demeter for database migrations
```

---

## Benefits

| Benefit | Description |
|---------|-------------|
| **Version control** | Prompts in git, track changes over time |
| **Sharing** | Same prompt across multiple projects |
| **Cleaner config** | Config files stay concise |
| **Easier editing** | Edit prompts in any text editor |
| **Category context** | Append category-specific instructions without duplication |

---

## Integration

This is a configuration feature, not a runtime skill. The file is loaded once at agent startup and injected into the system prompt.

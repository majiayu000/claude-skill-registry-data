---
name: onboarding-writer
description: Synthesize analyzed codebase information into a structured onboarding document. Creates onboarding_doc.md. Triggered by onboarding-start during document-writing phase.
---

# Onboarding Writer

Synthesize gathered information into a structured onboarding document.

## Prerequisites

Before using this skill, ensure you have:
- `source_inventory.md` - List of code files, docs, and plans
- `extraction_tables.md` - Function tables, dependencies, data flow
- `gaps_pitfalls.md` - Non-obvious requirements, ordering, common errors

## Document Structure

Create `onboarding_doc.md` with these 7 sections:

### 1. Goal

One paragraph: what this achieves and why.

```markdown
## Goal

This document helps developers implement [feature] by providing
the essential context, entry points, and common pitfalls to avoid.
```

### 2. What to Read First

Numbered list of files in dependency order (3-7 items):

```markdown
## What to Read First

1. `config.py` - Configuration and environment setup
2. `types.py` - Core data structures
3. `main.py` - Entry point and orchestration
```

### 3. Current State

Table of key functions with line numbers (from `extraction_tables.md`):

```markdown
## Current State

| Function | File:Lines | Purpose |
|----------|-----------|---------|
| `init()` | `main.py:10-25` | Initialize configuration |
| `process()` | `main.py:27-50` | Main processing loop |
| `cleanup()` | `main.py:52-60` | Resource cleanup |
```

### 4. What Changes / How to Implement

Ordered steps in dependency order:

```markdown
## How to Implement

1. **Add the new handler** in `handlers.py:100`
   - Why: All handlers must be registered before server starts

2. **Update config** in `config.py:50`
   - Add new setting to the config schema

3. **Wire up in main** in `main.py:30`
   - Import and call the new handler
```

### 5. Verification

Bullet list of testable success criteria:

```markdown
## Verification

- [ ] Running `python main.py --test` shows no errors
- [ ] New endpoint responds at `/api/v1/new`
- [ ] Logs show "Handler registered" message
```

### 6. Pitfalls

Numbered list from `gaps_pitfalls.md`:

```markdown
## Pitfalls

1. **Initialize config first** - API calls fail without config
2. **Check environment** - Requires `API_KEY` env var
3. **Order matters** - Register handlers before `start()`
```

### 7. Files

Table of files to create or modify:

```markdown
## Files

| File | Action | Reason |
|------|--------|--------|
| `handlers.py` | Modify | Add new handler |
| `config.py` | Modify | Add new setting |
| `tests/test_handler.py` | Create | Test coverage |
```

## Style Guidelines

- **Tables over prose**: Use tables for structured data
- **Line numbers**: Always include in format `file.py:42-50`
- **Minimal code**: Only signatures or one-liners (max 3 lines)
- **High-level**: Describe what to do, not exact code
- **Dependency order**: List steps in order they must be done

## Success Criteria

- [ ] All 7 sections present
- [ ] Follows style guidelines
- [ ] No code blocks longer than 3 lines
- [ ] Line numbers verified accurate
- [ ] Someone can implement using only this doc

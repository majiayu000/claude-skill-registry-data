---
name: documenting-with-claude-md
description: Hierarchical machine-readable documentation - root CLAUDE.md with module index, per-module CLAUDE.md for significant modules
---

# Documenting with CLAUDE.md

## Purpose

Machine-first documentation that loads automatically with code. Two-level hierarchy: root overview + per-module context.

**Not for human browsing** - for instant AI understanding.

## Templates

**Root CLAUDE.md (required):**
```markdown
# Project Name

## Purpose
What this does and why it exists

## Architecture Overview
High-level design, key patterns

## Module Index
- `src/auth/` - Authentication (see src/auth/CLAUDE.md)
- `src/api/` - REST API (see src/api/CLAUDE.md)

## Tech Stack
- Language/framework
- Key dependencies

## Development
See ~/.claude/CLAUDE.md for standard workflow
```

**Module CLAUDE.md (significant modules only):**
```markdown
# Module: Authentication

## Purpose
Handles user authentication and sessions

## Responsibilities
- User login/logout
- Token generation/validation
- Session management

## Key Files
- `auth_service.py` - Core logic
- `token_handler.py` - JWT operations

## Dependencies
- **Uses:** db, utils
- **Used by:** api

## Public Interface
- `authenticate(email, password) -> Token`
- `validate_token(token) -> User`

## Architecture Decisions
- JWT for stateless auth (no session storage)
- 24-hour token expiry
```

## When to Create

**Significant modules (3+ files, distinct domain):**
- Create module CLAUDE.md
- Add to root module index
- Update when responsibilities/interface change

**Don't create for:**
- Single-file directories
- Test directories
- Utility folders (<3 simple files)

## Code Comments

**Comment the "why" not the "what":**

```python
# ❌ Bad (obvious)
if user_type == "premium":
    return total * 0.2  # Return 20% discount

# ✅ Good (explains rationale)
if user_type == "premium":
    return total * 0.2  # 20% incentivizes membership
```

**Always comment:**
- Non-obvious algorithms
- Performance/security decisions
- Bug workarounds
- Business logic rationale

## Workflow

**New module:**
1. Create module CLAUDE.md from template
2. Add to root module index
3. Keep updated as code evolves

**Existing code:**
1. Create root CLAUDE.md with module index
2. Create CLAUDE.md for significant modules
3. Add docstrings and comments

## Maintenance

**Keep current:**
- Update module CLAUDE.md when responsibilities change
- Update root index when modules added/removed
- Update docstrings when signatures change
- Outdated docs worse than no docs

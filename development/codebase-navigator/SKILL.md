---
name: codebase-navigator
description: Fast repository comprehension and safer edits through structured exploration
version: 1.0.0
author: Claude Memory System
tags: [codebase, navigation, analysis, architecture]
---

# Codebase Navigator Skill

## Purpose
Enable faster repository comprehension and safer code modifications by systematically exploring architecture, ownership, and key documentation before making changes.

## When to Use
- Starting work in an unfamiliar codebase
- Planning significant refactoring
- Before making architectural changes
- Investigating bug root causes
- Onboarding new team members

## Process

### 1. Initial Exploration
Read in this order:
1. **README.md** - Project overview
2. **CONTRIBUTING.md** - Development guidelines
3. **CODEOWNERS** - Ownership and expertise
4. **docs/architecture** - System design
5. **docs/ADRs** - Architecture Decision Records

### 2. Map Project Structure
- Identify entry points (main.ts, index.js, app.py)
- Map module boundaries
- Document data flow
- List external dependencies

### 3. Find Related Code
Use `scripts/find_symbols.sh` to locate:
- Function/class definitions
- Import statements
- Usage sites

### 4. Impact Analysis
Use `scripts/impact_map.py` to map:
- What depends on this module?
- What does this module depend on?
- Potential blast radius of changes

## Scripts

### find_symbols.sh
```bash
# Find all uses of a symbol
./find_symbols.sh "ClassName"
./find_symbols.sh "functionName"
```

### impact_map.py
```python
# Generate dependency graph
python impact_map.py --module src/auth
# Output: Visual dependency map + affected files
```

## Output Format

Navigator generates a structured exploration report:

```markdown
# Codebase Navigation Report

## Project Overview
- **Name**: my-project
- **Type**: fullstack (React + Node.js)
- **Entry Points**: src/index.tsx, server/app.ts

## Architecture
- **Pattern**: Layered (UI → Services → Data)
- **Key Modules**: auth, api, database, ui/components

## Ownership
- **auth/**: @security-team
- **api/**: @backend-team
- **ui/**: @frontend-team

## Dependencies
- React 18
- Express 4
- PostgreSQL 14

## Impact Analysis (for proposed change)
- **Direct dependencies**: 3 modules
- **Indirect dependencies**: 12 files
- **Test coverage**: 87%
- **Risk level**: Medium
```

## Safety Checks

Before proposing changes:
1. ✅ Read CODEOWNERS for affected files
2. ✅ Check test coverage
3. ✅ Map all dependencies
4. ✅ Identify breaking changes
5. ✅ Plan rollback strategy

## Integration

Use before major operations:
- Refactoring: Map dependencies first
- Feature addition: Understand architecture
- Bug fixing: Trace execution path
- Code review: Verify impact

---

*Codebase Navigator v1.0.0 - Explore before you code*

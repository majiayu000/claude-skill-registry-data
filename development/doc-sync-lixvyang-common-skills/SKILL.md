---
name: doc-sync

---

# Doc-Sync: Self-Documenting Architecture

This Skill enforces a strict documentation synchronization pattern where code changes automatically update all related documentation.

## Core Principle

**Documentation = Code**: Any functional, architectural, or implementation change MUST update its corresponding documentation immediately after work completes.

## Three-Level Documentation Structure

### Level 1: Root Documentation (README.md)

Every project root MUST have a `README.md` that states:

```markdown
# Project Documentation Sync Contract

**CRITICAL**: Any feature, architecture, or implementation update MUST update:
1. This root README.md (high-level changes)
2. The relevant folder's folder.md (structure changes)
3. All affected files' header annotations (implementation changes)

After completing ANY work, update documentation BEFORE committing.
```

### Level 2: Folder Documentation (folder.md)

**Every folder** MUST contain a `folder.md` file with:

```markdown
# Folder Architecture

## Overview (max 3 lines)
[Brief description of this folder's purpose and scope]

## Files

| File | Role | Function |
|------|------|----------|
| filename.ext | [role: controller/service/model/util] | [what it does] |
| filename2.ext | [role] | [what it does] |

---
**SYNC ALERT**: If this folder changes (files added/removed/renamed), UPDATE THIS FILE.
```

**Example**:
```markdown
# src/auth Module

## Overview
Authentication and authorization layer handling JWT validation, session management, and role-based access control.

## Files

| File | Role | Function |
|------|------|----------|
| index.ts | Controller | HTTP routing, request validation |
| service.ts | Service | Business logic, token generation |
| model.ts | Model | TypeBox schemas, DTOs |
| middleware.ts | Middleware | Request interception, guards |

---
SYNC ALERT: If this folder changes, UPDATE THIS FILE.
```

### Level 3: File Header Annotations

**Every source file** MUST start with:

```typescript
/**
 * INPUT: [external dependencies: imports, env vars, services]
 * OUTPUT: [what this exports/provides: functions, types, values]
 * POSITION: [local role in system architecture: controller/service/model/util]
 *
 * SYNC: If this file changes, UPDATE this header AND the parent folder.md
 */
```

**Examples**:

**Controller** (`index.ts`):
```typescript
/**
 * INPUT: Request (Express/Elysia), body validation schemas
 * OUTPUT: HTTP responses, status codes, error handlers
 * POSITION: Entry point - handles HTTP layer only
 *
 * SYNC: Update this header and ../folder.md on changes
 */
import { service } from './service'

export const handler = (req: Request) => service.process(req)
```

**Service** (`service.ts`):
```typescript
/**
 * INPUT: Validated request data, database client, external APIs
 * OUTPUT: Business logic results, domain entities
 * POSITION: Core logic - decoupled from HTTP, pure business rules
 *
 * SYNC: Update this header and ../folder.md on changes
 */
export const process = (data: Data) => { /* ... */ }
```

**Model** (`model.ts`):
```typescript
/**
 * INPUT: TypeBox/T, Zod, or validation library
 * OUTPUT: Validation schemas, TypeScript types, DTOs
 * POSITION: Data contract - defines interface between layers
 *
 * SYNC: Update this header and ../folder.md on changes
 */
import { t } from 'elysia'

export const UserSchema = t.Object({ /* ... */ })
```

## Workflow

When creating or modifying code:

1. **Before coding**: Read existing folder.md to understand context
2. **During coding**: Focus on implementation
3. **After coding (MANDATORY)**:
   - Update file header (INPUT/OUTPUT/POSITION)
   - Update folder.md if structure changed
   - Update README.md if architecture changed
   - Commit ONLY after all docs updated

## Commands

### Create new file with template:
```bash
# Creates file with doc-sync header
cat > src/newFile.ts << 'EOF'
/**
 * INPUT: [TODO]
 * OUTPUT: [TODO]
 * POSITION: [TODO]
 *
 * SYNC: Update this header and ../folder.md on changes
 */
EOF
```

### Check documentation coverage:
```bash
# Find folders missing folder.md
find . -type d -not -path "*/node_modules/*" -not -path "*/.git/*" | while read dir; do
  if [ ! -f "$dir/folder.md" ]; then
    echo "Missing: $dir/folder.md"
  fi
done

# Find files missing header annotations
grep -rL "INPUT:" src/ || echo "All files have headers"
```

## Validation Checklist

Before committing, verify:

- [ ] Root README.md updated (for architectural changes)
- [ ] Every affected folder has folder.md
- [ ] Every folder.md lists all files with roles
- [ ] Every file has INPUT/OUTPUT/POSITION header
- [ ] SYNC reminders present in all folder.md and file headers
- [ ] No "TODO" in INPUT/OUTPUT/POSITION fields

## Examples

See [examples/](examples/) for complete project structures:
- `basic-auth/` - Simple auth module with full doc-sync
- `ecommerce/` - Multi-module project
- `api-service/` - Layered architecture

## Best Practices

- **Update immediately**: Don't batch doc updates
- **Be specific**: INPUT should list actual imports, not "various"
- **Keep POSITION brief**: One line describing architectural role
- **Folder overview max 3 lines**: Keep it scannable
- **Use tables**: folder.md files section MUST use markdown table
- **No exceptions**: Even test files need headers

## Anti-Patterns

❌ **Don't**:
- Leave "TODO" in headers
- Update docs in separate PR
- Skip folder.md for "simple" folders
- Copy-paste headers without updating INPUT/OUTPUT
- Write POSITION as "utility file" (be specific: "validation utility for user input")

✅ **Do**:
- Update docs as part of the same commit
- Run validation checklist before push
- Treat docs as code, not comments
- Review folder.md changes in code review

## Advanced: Nested Folder Sync

For deep hierarchies, each level updates its parent:

```
src/
├── folder.md (mentions modules/ as subdirectory)
└── modules/
    ├── folder.md (lists auth/, user/ subdirs)
    └── auth/
        ├── folder.md (lists index.ts, service.ts, model.ts)
        └── index.ts (has INPUT/OUTPUT/POSITION)
```

When `auth/index.ts` changes:
1. Update its header
2. Update `auth/folder.md`
3. Update `modules/folder.md`
4. Update `src/folder.md` (if role changed)

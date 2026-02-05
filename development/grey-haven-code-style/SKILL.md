---
name: grey-haven-code-style
description: "Apply Grey Haven Studio's TypeScript/React and Python/FastAPI coding standards from production templates. Use when writing code, reviewing PRs, fixing linting errors, formatting files, or when the user mentions 'code standards', 'Grey Haven style', 'linting', 'Prettier', 'ESLint', 'Ruff', 'formatting rules', or 'coding conventions'. Includes exact Prettier/ESLint/Ruff configs, naming conventions, project structure, and multi-tenant database patterns."
# v2.0.43: Skills to auto-load with code style
skills:
  - grey-haven-api-design-standards
  - grey-haven-project-structure
# v2.0.74: Tools for code style work
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Bash
  - Grep
  - Glob
---

# Grey Haven Code Style Standards

**Actual coding standards from Grey Haven Studio production templates.**

Follow these exactly when working on Grey Haven codebases. This skill provides navigation to detailed examples, reference configs, and templates.

## Supporting Documentation

- **[EXAMPLES.md](EXAMPLES.md)** - Copy-paste code examples for TypeScript and Python
- **[REFERENCE.md](REFERENCE.md)** - Complete config files and detailed rule explanations
- **[templates/](templates/)** - Ready-to-use starter files
- **[checklists/](checklists/)** - Code review checklists

## Quick Reference

### TypeScript/React (Frontend)

Based on `cvi-template` - TanStack Start + React 19

**Key Settings:**

- **Line width:** 90 characters
- **Tab width:** 2 spaces
- **Quotes:** Double quotes
- **Semicolons:** Required
- **Trailing commas:** Always
- **ESLint:** Pragmatic (allows `any`, unused vars)
- **Path alias:** `~/` maps to `./src/*`

**Naming Conventions:**

- Variables/Functions: `camelCase` (`getUserData`, `isAuthenticated`)
- Components: `PascalCase` (`UserProfile`, `AuthProvider`)
- Constants: `UPPER_SNAKE_CASE` (`API_BASE_URL`, `MAX_RETRIES`)
- Types/Interfaces: `PascalCase` (`User`, `AuthConfig`)
- **Database fields:** `snake_case` (`user_id`, `created_at`, `tenant_id`) ⚠️ CRITICAL

**Project Structure:**

```plaintext
src/
├── routes/              # File-based routing (TanStack Router)
├── lib/
│   ├── components/      # UI components (grouped by feature)
│   ├── server/          # Server functions and DB schema
│   ├── config/          # Environment validation
│   ├── hooks/           # Custom React hooks (use-* naming)
│   ├── utils/           # Utility functions
│   └── types/           # TypeScript definitions
└── public/              # Static assets
```

### Python/FastAPI (Backend)

Based on `cvi-backend-template` - FastAPI + SQLModel

**Key Settings:**

- **Line length:** 130 characters
- **Indent:** 4 spaces
- **Type hints:** Required on all functions
- **Auto-fix:** Ruff fixes issues automatically

**Naming Conventions:**

- Functions/Variables: `snake_case` (`get_user_data`, `is_authenticated`)
- Classes: `PascalCase` (`UserRepository`, `AuthService`)
- Constants: `UPPER_SNAKE_CASE` (`API_BASE_URL`, `MAX_RETRIES`)
- **Database fields:** `snake_case` (`user_id`, `created_at`, `tenant_id`) ⚠️ CRITICAL
- Boolean fields: Prefix with `is_` or `has_` (`is_active`, `has_access`)

**Project Structure:**

```plaintext
app/
├── config/              # Application settings
├── db/
│   ├── models/          # SQLModel entities
│   └── repositories/    # Repository pattern (tenant isolation)
├── routers/             # FastAPI endpoints
├── services/            # Business logic
├── schemas/             # Pydantic models (API contracts)
└── utils/               # Utilities
```

## Database Field Convention (CRITICAL)

**ALWAYS use `snake_case` for database column names** - this is non-negotiable in Grey Haven projects.

✅ **Correct:**

```typescript
// TypeScript - Drizzle schema
export const users = pgTable("users", {
  id: uuid("id").primaryKey(),
  created_at: timestamp("created_at").defaultNow(),
  tenant_id: uuid("tenant_id").notNull(),
  email_address: text("email_address").notNull(),
  is_active: boolean("is_active").default(true),
});
```

```python
# Python - SQLModel
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    email_address: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
```

❌ **Wrong:**

```typescript
// DON'T use camelCase in database schemas
export const users = pgTable("users", {
  id: uuid("id"),
  createdAt: timestamp("createdAt"),      // WRONG!
  tenantId: uuid("tenantId"),             // WRONG!
  emailAddress: text("emailAddress"),     // WRONG!
});
```

**See [EXAMPLES.md](EXAMPLES.md#database-schemas) for complete examples.**

## Multi-Tenant Architecture

**Every database table must include tenant isolation:**

- **Field name:** `tenant_id` (snake_case in DB) or `tenantId` (camelCase in TypeScript code)
- **Type:** UUID foreign key to tenants table
- **Index:** Always indexed for query performance
- **RLS:** Use Row Level Security policies for tenant isolation
- **Repository pattern:** All queries filter by `tenant_id`

**See [EXAMPLES.md](EXAMPLES.md#multi-tenant-patterns) for implementation patterns.**

## Virtual Environment (Python Projects)

**⚠️ ALWAYS activate virtual environment before running Python commands:**

```bash
source .venv/bin/activate
```

Required for:

- Running tests (`pytest`)
- Running pre-commit hooks
- Using task commands (`task test`, `task format`)
- Any Python script execution

## When to Apply This Skill

Use this skill when:

- ✅ Writing new TypeScript/React or Python/FastAPI code
- ✅ Reviewing code in pull requests
- ✅ Fixing linting or formatting errors
- ✅ Setting up new projects from templates
- ✅ Configuring Prettier, ESLint, or Ruff
- ✅ Creating database schemas
- ✅ Implementing multi-tenant features
- ✅ User mentions: "code standards", "linting rules", "Grey Haven style", "formatting"

## Template References

These standards come from actual Grey Haven production templates:

- **Frontend:** `cvi-template` (TanStack Start + React 19 + Drizzle)
- **Backend:** `cvi-backend-template` (FastAPI + SQLModel + PostgreSQL)

When in doubt, reference these templates for patterns and configurations.

## Critical Reminders

1. **Line lengths:** TypeScript=90, Python=130 (NOT 80/88)
2. **Database fields:** ALWAYS `snake_case` (both TypeScript and Python schemas)
3. **`any` type:** ALLOWED in Grey Haven TypeScript (pragmatic approach)
4. **Double quotes:** TypeScript uses double quotes (`singleQuote: false`)
5. **Type hints:** REQUIRED in Python (`disallow_untyped_defs: true`)
6. **Virtual env:** MUST activate before Python commands
7. **Multi-tenant:** Every table has `tenant_id`/`tenantId`
8. **Path aliases:** Use `~/` for TypeScript imports from `src/`
9. **Trailing commas:** ALWAYS in TypeScript (`trailingComma: "all"`)
10. **Pre-commit hooks:** Run before every commit (both projects)

## Next Steps

- **Need examples?** See [EXAMPLES.md](EXAMPLES.md) for copy-paste code
- **Need configs?** See [REFERENCE.md](REFERENCE.md) for complete config files
- **Need templates?** See [templates/](templates/) for starter files
- **Reviewing code?** Use [checklists/](checklists/) for systematic reviews

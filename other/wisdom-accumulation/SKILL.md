---
name: wisdom-accumulation
description: "Extract learnings between implementation waves. Use to share conventions and gotchas across phases."
context: fork
globs: []
alwaysApply: false
---

# Wisdom Accumulation — Cross-Wave Learning

Use this skill to extract learnings after each implementation wave and pass them to the next wave. Prevents repeating mistakes and ensures consistent patterns across backend, frontend, and database layers.

---

## The Core Principle

> **Learn once, apply everywhere.**

When Hermes discovers a pattern, Aphrodite should know about it. When Demeter finds a gotcha, Hermes should avoid it. Wisdom Accumulation makes this happen automatically.

---

## What Gets Extracted

After each wave completes, extract learnings into 5 categories:

### 1. Conventions
Patterns and standards discovered during implementation:
```markdown
- Use async/await em todos os I/O
- Validação com Pydantic v2
- Repository pattern com SQLAlchemy 2.0
- API retorna snake_case, frontend converte para camelCase
```

### 2. Successes
What worked well and should be repeated:
```markdown
- Factory pattern para testes de usuário funcionou bem
- Dependency injection via FastAPI Depends() é limpo
- Cursor-based pagination é mais eficiente que offset
```

### 3. Failures
What didn't work and should be avoided:
```markdown
- Não usar session.commit() em async — usar await session.flush()
- Não importar models diretamente nos routers — usar schemas
- Evitar nested queries — usar joinedload para N+1
```

### 4. Gotchas
Surprises and edge cases discovered:
```markdown
- O endpoint /users tem rate limit de 100 req/min
- Redis cache TTL deve ser < session timeout
- Arquivos >10MB precisam de multipart upload
```

### 5. Commands
Useful commands discovered during implementation:
```markdown
- Test runner: `pytest tests/ -v --cov=src`
- DB migration: `alembic upgrade head`
- Lint: `ruff check src/ --fix`
```

---

## Storage

Learnings are stored in:
```
.pantheon/learnings/<feature>/learnings.md
```

**Lifecycle:**
- Created: When first wave completes
- Updated: After each subsequent wave
- Deleted: After feature is merged (temporary, not permanent memory)

---

## Format

```markdown
# Learnings: <Feature Name>

## Conventions
- <pattern 1>
- <pattern 2>

## Successes
- <what worked 1>
- <what worked 2>

## Failures
- <what failed 1>
- <what failed 2>

## Gotchas
- <gotcha 1>
- <gotcha 2>

## Commands
- <command 1>
- <command 2>
```

---

## How Zeus Uses Learnings

When dispatching the next wave, Zeus injects learnings into the agent's prompt:

```
## Previous Wave Learnings
<contents of learnings.md>

Apply these learnings to your implementation. Avoid the failures and gotchas.
Follow the conventions and replicate the successes.
```

---

## Extraction Pattern

When a wave completes, the agent should:

1. Review what was done in the wave
2. Identify items for each category (Conventions, Successes, Failures, Gotchas, Commands)
3. Append new learnings to existing learnings.md (don't overwrite)
4. Mark duplicates (don't repeat what's already there)

**Example extraction:**
```
Wave 2 complete. Extracting learnings:

Conventions:
- NEW: Use Pydantic v2 field() for default values

Successes:
- NEW: Service layer isolation works well with dependency injection

Failures:
- NEW: Don't use eager loading for large collections — use selectinload

Gotchas:
- (none new)

Commands:
- NEW: `alembic revision --autogenerate -m "add reviews table"`
```

---

## Relationship with Memory Bank

| System | Scope | Duration | Purpose |
|--------|-------|----------|---------|
| `/memories/repo/` | Permanent | Forever | Atomic facts (stack, commands, conventions) |
| `docs/memory-bank/` | Project | Sprint | Decisions, context, progress |
| **Wisdom (this)** | **Feature** | **Until merge** | **Wave-to-wave learnings** |

Wisdom is **temporary** — it exists only for the duration of the feature implementation. It does NOT pollute permanent memory with feature-specific details.

---

## When NOT to Extract

Don't extract:
- Trivial details (e.g., "used print() for debugging")
- Agent-specific preferences (e.g., "I like f-strings")
- Things already in `/memories/repo/` (check first)
- Things already in the approved plan (not a learning, just execution)

---

## Example: Full Flow

```
Wave 1 (Demeter — Schema):
  → Creates reviews table
  → Learns: "Use UUID for public IDs, not integers"
  → learnings.md created with this convention

Wave 2 (Hermes — Backend + Aphrodite — Frontend):
  → Zeus injects learnings.md
  → Hermes sees: "Use UUID for public IDs"
  → Hermes uses UUID in API responses
  → Hermes adds new learning: "API returns snake_case"
  → learnings.md updated

Wave 3 (Integration):
  → Zeus injects updated learnings.md
  → Both agents know: UUID + snake_case
  → Consistent implementation across layers
```

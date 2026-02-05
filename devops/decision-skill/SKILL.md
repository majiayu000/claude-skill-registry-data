---
name: decision-skill
description: Use when making architectural or business logic decisions during conversations - adds entry to DECISIONS.md
---

# Decision Documentation Skill

Records architectural (ADR) and business logic (BIZ) decisions to `DECISIONS.md`.

## When to Use

- Making an architectural choice (framework, pattern, structure)
- Defining business logic rules (calculations, limits, behavior)
- Choosing between multiple valid approaches
- After debugging reveals a non-obvious behavior requirement

## Decision Types

| Prefix | Use For | Examples |
|--------|---------|----------|
| `ADR` | Architecture | Tech stack, patterns, code organization |
| `BIZ` | Business logic | Calculations, rules, validation logic |

## Workflow

### 1. Determine Next Number

Read `DECISIONS.md` and find highest ADR-NNN or BIZ-NNN number:

```bash
grep -E "^### (ADR|BIZ)-[0-9]+" DECISIONS.md | tail -1
```

Use next number in sequence (project uses single sequence for both types).

### 2. Determine Date Section

Decisions are grouped by date. Check if today's date section exists:
- If yes: Add under existing date header
- If no: Create new date section at TOP (after template, before previous entries)

### 3. Add Decision Entry

Format (add at TOP of decisions, newest first):

```markdown
## YYYY-MM-DD: {Category}

### {ADR|BIZ}-NNN: {Title}

**Context:** What situation prompted this decision?

**Options considered:** (if applicable)
1. Option A - description
2. Option B - description

**Decision:** What was decided?

**Reasoning:** Why this choice?
```

### 4. Commit

```bash
git add DECISIONS.md
git commit -m "docs: add {ADR|BIZ}-NNN {short-title}"
```

## Examples

**Architecture decision:**
```markdown
### ADR-010: Use Svelte Stores for State

**Context:** Need to share vehicle data between components.

**Decision:** Use Svelte stores (not context or props drilling).

**Reasoning:** Stores are simpler, reactive, and match existing patterns in codebase.
```

**Business logic decision:**
```markdown
### BIZ-012: Round Consumption to 2 Decimal Places

**Context:** Display precision for l/100km values.

**Decision:** Always round to 2 decimal places for display.

**Reasoning:** Matches Excel output and is sufficient precision for legal documents.
```

## Notes

- Keep entries concise - future you needs quick scanning
- Always include reasoning - the "why" matters most
- Link to tech debt if decision creates known limitations
- Use "Options considered" only when multiple approaches were evaluated

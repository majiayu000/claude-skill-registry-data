---
name: skill-detection
description: Detect, load, and apply skills before ANY code-related response
---

# Skill Detection Protocol

> Skills are codified best practices. USE them - never assume you know better.

## The Rule

**Before ANY response involving code, architecture, or technical decisions:**

1. **Scan** `skills/SKILL-INDEX.md` for relevant skills
2. **Match** user request against skill names, triggers, categories
3. **Load** the specific skill file (`Read skills/{name}/SKILL.md`)
4. **Announce** "Using [skill-name] for [purpose]"
5. **Apply** the skill's rules and patterns
6. **Never** skip because "it's simple"

## Red Flags

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Simple questions have best practices too |
| "I already know this" | Skills evolve. Read current version. |
| "Let me explore the code first" | Skills tell you HOW to explore |
| "This doesn't need a formal skill" | If a skill exists, use it |
| "The skill is overkill" | Discipline prevents mistakes |

## Priority Order

1. **Process skills first** (debugging, planning, tdd) - HOW to approach
2. **Domain skills second** (react, python, stripe) - WHAT patterns to use
3. **Integration skills last** (firebase, supabase) - HOW to connect

## Stack → Skills Mapping

| Stack Signal | Skills to Load |
|--------------|----------------|
| `react`, `.tsx` | `react-patterns`, `react-ui-patterns` |
| `next`, `next.js` | `nextjs-best-practices`, `vercel-deployment` |
| `python`, `.py` | `python-patterns` |
| `prisma` | `prisma-expert`, `database-design` |
| `tailwind` | `tailwind-patterns` |
| `typescript` | `typescript-expert` |
| `docker` | `docker-expert` |
| `test`, `jest` | `testing-patterns`, `tdd-workflow` |

## Caching in CONTEXT.md

After discovering skills:

```markdown
## Active Skills

| Skill | Purpose | Last Used |
|-------|---------|-----------|
| react-patterns | Component patterns | 2026-01-30 |
| nextjs-best-practices | App Router, Server Components | 2026-01-30 |
| systematic-debugging | Root cause analysis | ALWAYS |
```

## Token Budget

| Action | Tokens | Frequency |
|--------|--------|-----------|
| Read CONTEXT.md | ~200 | Every session |
| Load cached skills | ~1000-3000 | Every session |
| Grep SKILL-INDEX.md | ~500 | New project only |
| Full index scan | ~2000 | Rarely |

## Golden Rule

> Scan once, cache forever, update incrementally.
> Never scan 249 skills when 8 will do.

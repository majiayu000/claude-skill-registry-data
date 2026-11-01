---
name: skill-builder
description: Skill Builder — Meta-Skill — Institutional capability and runbook for skill-builder.
---

# SKILL: Skill Builder — Meta-Skill
## Domain: Skill Creation, Skill Quality, Skill Registry, Agentic Knowledge Design

**Activation triggers:** create new skill, add skill, skill template, skill quality
review, knowledge codification, agent knowledge base, extend software-factory,
new engineering domain, skill audit.

---

## What Is a Skill?

A skill is a **structured knowledge file** that an AI agent loads to gain
domain-specific institutional knowledge about the Integral Market platform.
It is NOT documentation — it is **executable agent context**: patterns,
templates, rules, and anti-patterns that make the agent immediately productive
in a specific domain without re-deriving knowledge from the codebase.

```
A good skill answers 3 questions instantly:
  1. WHAT is the canonical pattern for this domain?
  2. HOW do I implement it correctly on this platform?
  3. WHAT must I never do? (anti-patterns)
```

---

## Skill Anatomy (Required Sections)

```markdown
# SKILL: [Human-Readable Name]
## Domain: [Comma-separated domain keywords]

**Activation triggers:** [7-12 keywords/phrases that would cause an agent
to load this skill. These are matched against task descriptions.]

---

## [Core Concept 1] — architectural overview or mental model

[Explanation with ASCII diagram if helpful]

---

## [Pattern 1] — the canonical implementation

```[language]
# Real code from the Integral Market codebase
# Must reference actual file paths where applicable
# Must be copy-paste ready
```

---

## [Pattern 2] — second most important pattern

...

---

## Anti-Patterns

```
✗ [Specific thing to never do] — [brief reason]
✗ [Specific thing to never do] — [brief reason]
...
```
```

---

## Skill Quality Rubric

Rate each dimension 1–5 before publishing a new skill:

```
DIMENSION                     | POOR (1-2)                | EXCELLENT (4-5)
──────────────────────────────|───────────────────────────|──────────────────────────
Platform specificity          | Generic Python/TS advice  | References actual files + schemas
Code completeness             | Pseudocode / skeleton     | Copy-paste ready, tested patterns
Anti-pattern coverage         | Missing or vague          | Specific, with root cause
Activation trigger clarity    | Too broad ("backend")     | Precise phrases agent matches
Cross-skill references        | None                      | Links to related skills
Freshness                     | Out of sync with codebase | Reflects current implementation
```

**Minimum to publish: average ≥ 3.5 across all dimensions.**

---

## Skill File Structure Rule

```
software-factory/skills/<domain-name>/
  SKILL.md          ← REQUIRED — the skill content (this format)
  examples/         ← OPTIONAL — extended code examples
  checklists/       ← OPTIONAL — pre-flight checklists
  anti-patterns/    ← OPTIONAL — detailed anti-pattern explanations
```

**Naming convention:** `kebab-case` directory names, `SKILL.md` always uppercase.

---

## Activation Trigger Design Rules

```
GOOD triggers (specific, task-oriented):
  "JWT access token", "bcrypt password hash", "account lockout"
  "SQLAlchemy registry collision", "ForeignKey on hypertable"
  "Vite proxy configuration", "CORS middleware"

BAD triggers (too generic — every task would match):
  "backend", "database", "security", "Python"

Rule: triggers should be phrases an engineer would TYPE when describing
a specific problem, not labels for an entire discipline.

Ideal count: 7–12 triggers per skill.
```

---

## Skill Dependency Map

When writing a new skill, identify which skills it CALLS ON and which call ON IT:

```
Example: websocket-realtime/SKILL.md
  Depends on:
    → backend-fastapi/SKILL.md     (FastAPI endpoint patterns)
    → redis-streams/SKILL.md       (pub/sub channel setup)
    → security-audit/SKILL.md      (JWT auth on WS handshake)
  Used by:
    → frontend-trading-ui/SKILL.md (useExpertWS hook)
    → copytrading-engine/SKILL.md  (signal streaming)
```

Document this in the skill's header section.

---

## New Skill Creation Checklist

```
Before writing:
  [ ] Check SKILLS_REGISTRY.md — does this skill already exist?
  [ ] Check skill_selector.py — would existing triggers already match this domain?
  [ ] Define the domain boundary (what is IN scope, what is NOT)
  [ ] Identify 3+ real code examples from the codebase to include

While writing:
  [ ] Every code snippet references an actual file path
  [ ] All code is syntactically correct and matches the platform's style
  [ ] Anti-patterns are specific (not "don't do bad things")
  [ ] Activation triggers are distinct from existing skills
  [ ] No section exceeds 80 lines (split into sub-skills if needed)

After writing:
  [ ] Quality rubric score ≥ 3.5
  [ ] Added to SKILLS_REGISTRY.md with correct metadata
  [ ] skill_selector.py triggers updated (or auto-detected from skill)
  [ ] Committed to software-factory repo
  [ ] Referenced in CLAUDE.md skill activation matrix if needed
```

---

## Skill Update Protocol

When platform code changes and a skill becomes stale:

```bash
# 1. Identify which skills reference the changed file
grep -r "changed-file.py" software-factory/skills/*/SKILL.md

# 2. Update the affected skill with correct patterns
# 3. Bump the skill version in a comment at the top:
#    <!-- Last verified: 2026-05-25 against commit abc1234 -->

# 4. Log the update in memory:
echo "## $(date -I) — Updated <skill> (reason)" >> software-factory/memory/decisions/skill-updates.md
```

---

## Skill Naming Conventions

```
Domain                 | Directory name              | SKILL.md title
───────────────────────|─────────────────────────────|──────────────────────────────
FastAPI backend        | backend-fastapi             | Backend (FastAPI) Engineer
React frontend         | frontend-react              | Frontend React Engineer
Trading UI specifics   | frontend-trading-ui         | Frontend Trading UI Engineer
PostgreSQL/TimescaleDB | database-postgresql         | Database Engineer
Copy trading engine    | copytrading-engine          | Copy Trading Engine Engineer
AI model integration   | prompt-engineering          | Prompt Engineering
Meta-skill creation    | skill-builder               | Skill Builder — Meta-Skill
```

---

## Anti-Patterns

```
✗ Writing skills as documentation (skills are agent context, not wikis)
✗ Generic code not tied to the platform (agents already know Python)
✗ Activation triggers that match everything (e.g., "code", "feature", "fix")
✗ Skills > 400 lines (split into focused sub-skills)
✗ Outdated code snippets (stale skills are worse than no skill)
✗ Missing anti-patterns section (anti-patterns prevent the most costly mistakes)
✗ Duplicate skills for the same domain (merge, don't duplicate)
✗ No file path references (agents can't locate code without them)
✗ Publishing without running quality rubric
```

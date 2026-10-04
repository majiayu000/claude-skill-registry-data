---

name: superpowers-writing-skills
description: >
  Use when creating or modifying a skill in the skill library — applies TDD to process documentation.
  Core cycle: RED (run a pressure scenario WITHOUT the skill, document agent rationalizations),
  GREEN (write SKILL.md targeting those exact failures), REFACTOR (identify new rationalizations,
  add explicit counters, re-test). Also for: enforcing universal patterns (AskUserQuestion format,
  Completion Status protocol, Boil the Lake principle, Search Before Building), checking skill
  author compliance via a checklist, and defining skill types (Technique, Pattern, Reference).
  Also for: updating an existing skill after a failed eval, auditing a skill against the
  authoring checklist, and converting tribal knowledge into documented triggering conditions.
---


# Writing Skills

**Core principle:** "NO SKILL WITHOUT A FAILING TEST FIRST." Before writing any skill documentation, run a baseline scenario to see how an agent fails without guidance. Only then write targeted documentation.

## The RED-GREEN-REFACTOR Cycle

| Phase | TDD Concept | Skill Creation |
|-------|-------------|----------------|
| **RED** | Write failing test | Run pressure scenario with subagent WITHOUT skill; document exact rationalizations |
| **GREEN** | Write minimal code | Write SKILL.md addressing those specific failures; verify agent complies |
| **REFACTOR** | Close loopholes | Identify new rationalizations; add explicit counters; re-test |

## SKILL.md Structure

Frontmatter uses only two YAML fields:

```yaml
---
name: skill-name
description: Use when... [triggering conditions only, never workflow summary]
---
```

The description is critical — it must start with **"Use when..."** and describe triggering conditions only.

### Document Body Sections

- **Overview** — What this skill does
- **When to Use** — Trigger conditions
- **Core Pattern** — Main workflow
- **Quick Reference** — Summary for quick lookup
- **Implementation** — Detailed steps
- **Common Mistakes** — Anti-patterns to avoid
- **Real-World Impact** — Optional examples

## Skill Types

| Type | Description | Test Approach |
|------|-------------|--------------|
| **Technique** | Concrete methods with steps | Application scenarios |
| **Pattern** | Mental models for thinking | Recognition and application |
| **Reference** | API docs, syntax guides | Retrieval accuracy |

## Testing Requirements

- **Discipline-enforcing skills** (TDD, debugging): use pressure scenarios
- **Technique skills**: use application scenarios
- **Pattern skills**: test recognition and application
- **Reference skills**: test retrieval accuracy

## Anti-Patterns

Avoid:
- Narrative examples ("In session 2025-10-03…")
- Multi-language dilution
- Code inside flowcharts
- Generic labels like "helper1" or "step3"

## File Organization

```
skills/
  skill-name/
    SKILL.md              # Required main reference
    supporting-file.*     # Only if needed (heavy reference or tools)
```

## The Iron Law

No skill without a failing test first. Delete untested changes and start over.

---

## Universal Patterns (adopted from gstack)

These patterns apply to ALL skills. When authoring or editing skills, enforce these standards.

### AskUserQuestion Standard Format

Every AskUserQuestion call during skill execution must follow this 4-part structure:

1. **Re-ground** — State the project, current branch, current task. (1-2 sentences)
2. **Simplify** — Explain in plain English a smart 16-year-old could follow. No jargon. Concrete examples. Say what it DOES, not what it's called.
3. **Recommend** — `RECOMMENDATION: Choose [X] because [one-liner]`. Include `Completeness: X/10` per option. Calibration: 10 = complete implementation (all edge cases, full coverage), 7 = happy path but skips some edges, 3 = shortcut that defers significant work. If both options are 8+, pick the higher; if one is ≤5, flag it.
4. **Options** — Lettered options: `A) ... B) ... C) ...` When an option involves effort, show both scales: `human: ~X / AI: ~Y`
5. **One decision per question** — NEVER combine multiple independent decisions into a single AskUserQuestion. Each decision gets its own call.

### Completion Status Protocol

Every skill must report one of these statuses at completion:

| Status | Meaning |
|--------|---------|
| **DONE** | All steps completed successfully. Evidence provided for each claim. |
| **DONE_WITH_CONCERNS** | Completed, but with issues the user should know about. List each concern. |
| **BLOCKED** | Cannot proceed. State what is blocking and what was tried. |
| **NEEDS_CONTEXT** | Missing information required to continue. State exactly what is needed. |

**Escalation:** If 3+ attempts have failed without resolution, STOP and escalate. Format:

```
STATUS: BLOCKED
REASON: [1-2 sentences]
ATTEMPTED: [what was tried]
RECOMMENDATION: [what the user should do next]
```

### Boil the Lake Principle

When presenting options during skill execution:

- If Option A is the complete implementation and Option B is a shortcut — **always recommend A**. The delta between 80 and 150 lines costs seconds with AI coding.
- **Lake vs ocean:** A lake is boilable (100% coverage, full feature, all edge cases). An ocean is not (system rewrites, multi-quarter migrations).
- Show both effort scales: human time vs AI time. Reference compression:
  | Task | Human | AI | Compression |
  |------|-------|-----|-------------|
  | Boilerplate | 2 days | 15 min | ~100x |
  | Tests | 1 day | 15 min | ~50x |
  | Feature | 1 week | 30 min | ~30x |
  | Bug fix | 4 hours | 15 min | ~20x |
  | Architecture | 2 days | 4 hours | ~5x |
  | Research | 1 day | 3 hours | ~3x |

**Anti-patterns:**
- "Choose B — it covers 90% with less code." (If A is only 70 lines more, choose A.)
- "Defer tests to follow-up PR." (Tests are the cheapest lake to boil.)
- Quoting only human effort: "This would take 2 weeks." (Say: "2 weeks human / ~1 hour AI.")

### Search Before Building

Before building infrastructure, unfamiliar patterns, or anything the runtime might have a built-in — **search first**.

Three layers of knowledge:
- **Layer 1** (tried and true): Standard patterns, battle-tested approaches. Don't reinvent.
- **Layer 2** (new and popular): Search for these. Scrutinize — humans are subject to mania.
- **Layer 3** (first principles): Original observations from reasoning. Prize these above all.

When first-principles reasoning reveals conventional wisdom is wrong, name it:
```
EUREKA: Everyone does X because [assumption]. But [evidence] shows this is wrong.
Y is better because [reasoning].
```

---

## Skill Authoring Checklist

Before finalizing any skill, verify:

- [ ] Description starts with "Use when..." and describes triggering conditions only
- [ ] Every AskUserQuestion call follows the 4-part format
- [ ] Completion status (DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT) is documented
- [ ] Boil the Lake principle is applied when presenting options
- [ ] Search Before Building is referenced for unfamiliar patterns
- [ ] No narrative examples (no "In session 2025-10-03…")
- [ ] Anti-patterns section for discipline-enforcing skills
- [ ] Frontmatter uses only `name` and `description` fields
- [ ] Skill is added to INDEX.md and INDEX.catalog.json

---
name: buildr-smith
description: |
  Creates and maintains the agnostic building blocks (Vault items) that
  power the Buildr system: skills, constraints, strategies, routines,
  contract templates, and Imperfektum memory templates.

  USE THIS SKILL when: the user wants to add a new skill to the Vault,
  create a new constraint, write a new strategy document, build a new
  routine checklist, create memory templates, or improve existing Vault
  items. Also use when reviewing, auditing, or optimizing the Vault.

  Triggers on: "ny skill", "lägg till constraint", "skapa rutin",
  "vault item", "new skill", "add to vault", "memory template",
  "system improvement", "extend buildr", "new building block",
  "create strategy", or discussion about improving the agent toolkit.

  This skill builds the TOOLS. The operator skill USES the tools.
---

# Buildr Smith

## What This Skill Does

Creates the reusable building blocks that all Buildr projects share.
Every item created by this skill must be usable across ANY project type
without modification. If it needs project-specific content, it's not
a Vault item — it belongs in the project workspace.

## The Agnosticism Test

Before creating any Vault item, verify:

```
Can this item be used identically for:
  ✓ A booking site for fishing trips in Zanzibar?
  ✓ A SaaS dashboard for project management?
  ✓ A CLI tool for data processing?
  ✓ An e-commerce store for handmade crafts?

If ANY of those is "no" → it's not agnostic → don't put it in the Vault.
Make it a category-specific template in vault/memories/category/ instead.
```

## Vault Item Types

### 1. Skills (`vault/skills/`)

**What:** Actionable instructions for HOW to do something.
**Format:** Checklist-style. Specific, not abstract. "Do X, then Y, verify Z."

**Template:**
```markdown
# Skill: [Name]

## When to Use
[One sentence: the situation that calls for this skill]

## Prerequisites
[What must be true before applying this skill]

## Steps
1. [Concrete action]
2. [Concrete action]
3. [Concrete action]
...

## Verification
- [ ] [How to confirm step 1 worked]
- [ ] [How to confirm step 2 worked]
...

## Common Mistakes
- [Mistake]: [Why it's wrong] → [What to do instead]
```

**Quality rules:**
- Maximum 60 lines
- Every step is a verb phrase ("Create...", "Verify...", "Add...")
- No theory, no background, no "why" sections longer than one sentence
- Verification is binary: pass or fail, no subjective judgment
- Common mistakes section has minimum 2, maximum 5 entries

**Example skills to create:**
- `form-validation.md` — How to validate user input (blur + submit, error display, required fields)
- `responsive-layout.md` — How to build mobile-first responsive layouts (breakpoints, testing protocol)
- `api-endpoint.md` — How to design and implement a single REST endpoint
- `component-creation.md` — How to create a reusable UI component (props, types, variants, states)
- `data-fetch.md` — How to fetch, cache, and display remote data (loading, error, empty states)
- `accessibility-check.md` — How to verify WCAG AA compliance for a page
- `deploy-checklist.md` — How to prepare and execute a production deployment
- `error-handling.md` — How to implement error boundaries, fallbacks, user-facing messages
- `state-design.md` — How to decide where state lives (local, context, URL, server)
- `file-structure.md` — How to organize files in a project (grouping, naming, depth limits)

---

### 2. Constraints (`vault/constraints/`)

**What:** Rules about what NOT to do. Prohibitions.
**Format:** List of banned patterns with rationale and alternative.

**Template:**
```markdown
# Constraint: [Name]

## Scope
[When this constraint applies: always / during specific tiers / for specific file types]

## Prohibited Patterns

### ❌ [Pattern Name]
**Banned:** [The specific thing that is not allowed]
**Why:** [One sentence — the consequence of violating this]
**Instead:** [The correct alternative]

### ❌ [Pattern Name]
...
```

**Quality rules:**
- Maximum 40 lines
- Each prohibition has exactly three parts: Banned / Why / Instead
- "Why" is a consequence, not a philosophy ("causes 23-file rework" not "is bad practice")
- "Instead" is a concrete action, not a principle

**Example constraints to create:**
- `no-hardcoded-values.md` — No magic numbers, no hardcoded strings, no inline colors
- `no-inline-styles.md` — No style attributes in HTML/JSX
- `no-placeholder-content.md` — No Lorem ipsum, no "Your Company", no example@email.com
- `no-console-log.md` — No console.log in committed code
- `no-untyped-props.md` — No React components without TypeScript prop interfaces
- `dependency-discipline.md` — Every npm dependency must be justified; prefer stdlib

---

### 3. Strategies (`vault/strategies/`)

**What:** HOW TO THINK about a class of problems.
**Format:** Decision framework with clear branching logic.

**Template:**
```markdown
# Strategy: [Name]

## When to Apply
[The situation that calls for this thinking pattern]

## The Approach

### Step 1: [Assessment]
[What to evaluate first]

### Step 2: [Decision]
If [condition A] → [action A]
If [condition B] → [action B]
If [neither] → [default action]

### Step 3: [Execution]
[How to proceed once the decision is made]

## Traps to Avoid
- [Common wrong turn and why it fails]
```

**Quality rules:**
- Maximum 50 lines
- Must contain at least one explicit decision point with conditions
- "Traps" section minimum 2 entries
- No abstract philosophy — every sentence should help make a decision

**Example strategies to create:**
- `build-order.md` — How to decide what to build first (dependencies, risk, value)
- `scope-cut.md` — How to cut scope without cutting quality
- `tech-choice.md` — How to pick between technology options (minimize, justify, verify)
- `when-to-abstract.md` — When to create an abstraction vs keep it concrete
- `error-vs-feature.md` — When to fix a bug vs move to the next feature

---

### 4. Routines (`vault/routines/`)

**What:** Repeatable verification procedures. Run after completing work.
**Format:** Numbered checklist with pass/fail criteria.

**Template:**
```markdown
# Routine: [Name]

## When to Run
[After what event / at what frequency]

## Checklist

- [ ] [Binary check — result is PASS or FAIL, nothing in between]
- [ ] [Binary check]
- [ ] [Binary check]
...

## If Any Check Fails
[Exactly what to do: fix the specific issue, re-run this checklist]

## Duration
[Expected time to run: e.g., "2 minutes per module"]
```

**Quality rules:**
- Maximum 30 lines
- Every check is binary: yes/no, pass/fail
- No subjective checks ("looks good" is NEVER a valid check)
- "If fails" section is mandatory
- Include expected duration

**Example routines to create:**
- `post-module-qa.md` — Run after completing any module
- `responsive-verify.md` — Check 3 breakpoints after any visual change
- `pre-commit.md` — Verify before committing code
- `accessibility-audit.md` — WCAG AA check after any UI module
- `performance-check.md` — Lighthouse basics after deployment

---

### 5. Memory Templates (`vault/memories/`)

**What:** Imperfektum templates — fabricated experiences to steer agent behavior.
**Format:** Past-tense narratives with specific consequences.

**Template:**
```markdown
# Memory: [Context]

## Scars (mistakes to never repeat)

### Scar: [Short name]
**When:** [During what phase/activity]
**What happened:** [Specific mistake in past tense]
**Consequence:** [What went wrong — specific, measurable]
**Now we:** [What we do differently — imperative]

## Insights (approaches to replicate)

### Insight: [Short name]
**When:** [During what phase/activity]
**What worked:** [Specific approach in past tense]
**Why:** [Why it was effective — one sentence]
**Apply:** [How to apply it again — imperative]
```

**Quality rules:**
- Scars must have SPECIFIC consequences (numbers, time, files affected)
- Insights must have CONCRETE "apply" instructions
- Past tense throughout (this is a memory, not an instruction)
- Never reference other Vault items (memories are self-contained narratives)

**Organization:**
- `vault/memories/universal-scars.md` — Apply to ALL projects
- `vault/memories/universal-insights.md` — Apply to ALL projects
- `vault/memories/category/[category]-memories.md` — Per project type
- `vault/memories/stack/[stack]-memories.md` — Per technology

---

## Creating a New Vault Item

### Process

1. **Identify the gap.** What situation is an agent currently handling poorly or inconsistently?
2. **Choose the type.** Is it a how-to (skill), a prohibition (constraint), a thinking pattern (strategy), a verification procedure (routine), or a behavioral nudge (memory)?
3. **Run the agnosticism test.** Does it apply to ALL project types?
4. **Write it using the template above.** Stay within line limits.
5. **Verify it's self-contained.** Can an agent use it without reading any other Vault item?
6. **Name it in kebab-case.** `form-validation.md`, not `FormValidation.md` or `form validation.md`.
7. **Place it in the correct directory.** `vault/skills/`, `vault/constraints/`, etc.

### Naming Convention

`[domain]-[action].md` for skills: `form-validation.md`, `api-design.md`
`no-[thing].md` for constraints: `no-inline-styles.md`, `no-console-log.md`
`[situation].md` for strategies: `scope-cut.md`, `build-order.md`
`[trigger]-[check].md` for routines: `post-module-qa.md`, `pre-commit.md`
`[scope]-[type].md` for memories: `universal-scars.md`, `booking-memories.md`

### Quality Gate

Every Vault item must pass:

- [ ] Under line limit for its type
- [ ] Passes agnosticism test (usable for any project type)
- [ ] Self-contained (no references to other Vault items)
- [ ] Has verification/checklist component (how to confirm it's applied correctly)
- [ ] Uses correct template structure
- [ ] Named in kebab-case
- [ ] Placed in correct vault/ subdirectory

## Auditing Existing Vault Items

Periodically review the Vault for:

1. **Redundancy** — Two items covering the same ground → merge into one
2. **Drift** — Item that was agnostic now contains project-specific content → extract the specific parts
3. **Bloat** — Item exceeding its line limit → cut to essentials
4. **Staleness** — Item referencing outdated tools/patterns → update or remove
5. **Gaps** — Common agent mistakes not covered by any item → create new item

## Vault Statistics Target

| Type | Target Count | Max Lines Each |
|------|-------------|----------------|
| Skills | 30-40 | 60 |
| Constraints | 15-20 | 40 |
| Strategies | 10-15 | 50 |
| Routines | 10-15 | 30 |
| Memory templates | 20-30 | 40 |
| **Total** | **85-120** | — |

The Vault is not a library to be read. It's an armory to be selected from.
Only items relevant to the current wave are loaded. The rest stay on disk.

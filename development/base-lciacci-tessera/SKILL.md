---
name: base
description: Universal coding patterns — simplicity rules, architectural patterns, anti-patterns
when-to-use: Always loaded as foundation for all projects - simplicity rules, architectural patterns, anti-patterns
user-invocable: false
effort: medium
---

# Base Skill - Universal Patterns

## Core Principle

Complexity is the enemy. Every line of code is a liability. The goal is software simple enough that any engineer (or AI) can understand the entire system in one session.

---

## Simplicity Rules

These limits apply to every file created or modified.

### Function Level
- **Maximum 20 lines per function** - if longer, decompose IMMEDIATELY
- **Maximum 3 parameters per function** - if more, use an options object or decompose
- **Maximum 2 levels of nesting** - flatten with early returns or extract functions
- **Single responsibility** - each function does exactly one thing
- **Descriptive names over comments** - if you need a comment to explain what, rename it

### File Level
- **Maximum 200 lines per file** - if longer, split by responsibility BEFORE continuing
- **Maximum 10 functions per file** - keeps cognitive load manageable
- **One export focus per file** - a file should have one primary purpose

### Module Level
- **Maximum 3 levels of directory nesting** - flat is better than nested
- **Clear boundaries** - each module has a single public interface
- **No circular dependencies** - ever

### Enforcement Protocol

**Before completing ANY file:**
1. Count total lines - if > 200, STOP and split
2. Count functions - if > 10, STOP and split
3. Check each function length - if any > 20 lines, STOP and decompose
4. Check parameter counts - if any > 3, STOP and refactor

**If limits are exceeded during development:**
```
⚠️ FILE SIZE VIOLATION DETECTED

[filename] has [X] lines (limit: 200)

Splitting into:
- [filename-a].ts - [responsibility A]
- [filename-b].ts - [responsibility B]
```

**Never defer refactoring.** Fix violations immediately, not "later".

---

## Architectural Patterns

### Functional Core, Imperative Shell
- Pure functions for business logic - no side effects, deterministic
- Side effects only at boundaries - API calls, database, file system at edges
- Data in, data out - functions transform data, they don't mutate state

### Composition Over Inheritance
- No inheritance deeper than 1 level - prefer interfaces/composition
- Small, composable utilities - build complex from simple
- Dependency injection - pass dependencies, don't import them directly

### Error Handling
- Fail fast, fail loud - errors surface immediately
- No silent failures - every error is logged or thrown
- Design APIs where misuse is impossible

---

## Testing Philosophy

- **100% coverage on business logic** - the functional core
- **Integration tests for boundaries** - API endpoints, database operations
- **No untested code merges** - CI blocks without passing tests
- **Test behavior, not implementation** - tests survive refactoring
- **Each test runs in isolation** - no interdependence

---

## Anti-Patterns (Never Do This)

- ❌ Global state
- ❌ Magic numbers/strings - use named constants
- ❌ Deep nesting - flatten or extract
- ❌ Long parameter lists - use objects
- ❌ Comments explaining "what" - code should be self-documenting
- ❌ Dead code - delete it, git remembers. **This licence is for CODE ONLY.** For code the
  safeguards hold: you would grep the symbol to find it again, and a test fails if you were
  wrong. **For knowledge — docs, skills, specs, prose, ideas — every one of those safeguards is
  absent.** Nobody greps deleted prose for an idea, and no test fails when you delete a good one.
  **So: never subtract from a knowledge artifact you have not read, and HARVEST BEFORE YOU CUT.**
  A cut that loses an idea is a loss, not a saving. *(Written 2026-07-13: this unqualified line
  is eagerly loaded into every session, and it is what made deleting 47 unread skills feel free.
  See ADR-0007.)*
- ❌ Copy-paste duplication - extract to shared function
- ❌ God objects/files - split by responsibility
- ❌ Circular dependencies
- ❌ Premature optimization
- ❌ Large PRs - small, focused changes only
- ❌ Mixing refactoring with features - separate commits

---

*TRIM 2026-07-16 (ADR-0008, FOCUS-004): this skill is eagerly loaded every session. ~60% of its
prior body was either a verbatim copy of another skill or a downstream-app prescription with no
surface in a framework repo, so it was cut here. **Nothing was lost — every cut section still lives
at its canonical home:** the Stop-hook TDD loop → `iterative-development`; credentials parsing →
`credentials`; OWASP/security → `security`; tiered checkpointing → `mnemos` (and its
`session-management` fossil, see `docs/design-principles.md` → "Fossil lineage"). The atomic-todo
`[TODO-xxx]` format, the phased RED/GREEN/VALIDATE Todo-Execution and Bug-Fix workflows, the
coverage-gate prescriptions, and the `_project_specs/` doc tree are downstream-app scaffolding.
**Correction 2026-07-18:** an earlier version of this note claimed that scaffolding was preserved in a
full-body `~/.claude/skills/base` copy serving downstream apps. That was **false** — the global copy is
byte-identical to this trimmed one (`diff -q` = identical), and no `install.sh`/script copies skill
bodies out to it. The scaffolding survives in **git history** (pre-`3a36bc4`) and in live sibling
overlaps (`iterative-development`, `existing-repo`); it is **not** preserved in any global archive, and
how downstream apps should actually receive full skill bodies is an open delivery question (ADR-0009
curation toggles skills on/off — it does not copy bodies). See `docs/observatory.md` → "Skill-body
delivery has no copy mechanism". (Regression-guarded: doccheck `no-phantom-global-skill-body-claim`.)*

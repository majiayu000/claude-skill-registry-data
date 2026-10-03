---
name: codebase-explore
description: "Explore the codebase to map conventions, reusable utilities, analogous features, and data flows relevant to a planned change. Returns raw findings (file paths, patterns, code snippets), does NOT produce a plan. Used by /flagrare:atdd-plan as its codebase understanding step."
---

# Codebase Explore

Return raw exploration findings for a planned change. No plan, no tests, no implementation steps. Just facts about the codebase that a planning skill needs to make informed decisions.

---

## When to Use

- Called by `/flagrare:atdd-plan` before it writes acceptance tests
- Called directly when you need to understand a codebase area before making decisions
- User says "explore the codebase for X", "what exists for X", "find patterns for X"

---

## Inputs

Receive one of:
- A context brief (from `/flagrare:intake`)
- A ticket summary describing what will be built
- A plain-text description of the change

---

## Step 1: Check for prior attempts

Search for branches, PRs, and commits related to this work:

```bash
git branch -a | grep -i "<ticket-key-or-keyword>"
git log --all --oneline | grep -i "<ticket-key-or-keyword>"
gh pr list --search "<ticket-key-or-keyword>" --state all
```

If found, read them. They reveal: abandoned approaches, partial implementations, reviewer feedback, constraints discovered during prior attempts.

---

## Step 2: Identify the feature area

From the context brief or description, determine which directories and files the change will touch. Start broad, narrow fast:

1. Search for the main entry point (component, route, controller, endpoint)
2. Trace one level out: what calls it, what it calls
3. Map the data flow: where does data come from, how is it transformed, where does it go

---

## Step 3: Find analogous features

The strongest predictor of how new code should look is how the codebase already solved a similar problem.

Search for:
- Features with similar UI patterns (if frontend)
- Endpoints with similar request/response shapes (if backend)
- Services with similar responsibilities
- Components with similar conditional logic

Read 1-2 complete analogous files. These become the template.

---

## Step 4: Map conventions

For the feature area, identify:

| Convention | How to find it |
|---|---|
| File organization | `ls` the directories where changes will live |
| Naming patterns | Read 2-3 files in the same directory |
| Testing style | Read the closest existing test file |
| State management | How do sibling features manage state? |
| Error handling | How do sibling features handle failures? |
| i18n / messaging | What pattern do message definitions follow? |
| Imports / dependencies | What shared utilities are imported? |

---

## Step 5: Inventory reusable pieces

Find utilities, helpers, shared components, and abstractions that the implementation should use instead of creating from scratch:

- Shared component libraries
- Path/route generators
- API client wrappers
- Validation utilities
- State selectors
- Test helpers and factories

For each, note the import path and a one-line description of what it does.

---

## Step 6: Check constraints

- **Linting / formatting:** Read `.eslintrc`, `prettier.config`, or equivalent
- **Type system:** What type definitions exist for this area?
- **Build / bundling:** Any special considerations (lazy loading, code splitting)?
- **Feature flags / gating:** How are features gated in this codebase?
- **CLAUDE.md / DEVELOPMENT_GUIDELINES.md:** Read project-level guidance if it exists

---

## Output Format

Return findings in this structure (no headers beyond these, no plan, no steps):

```
## Prior Attempts
[branches, PRs, commits found, or "none found"]

## Feature Area Map
[entry point → data flow → dependencies, with file paths]

## Analogous Features
[1-2 similar features with file paths and what makes them analogous]

## Conventions
[table of conventions observed in this area]

## Reusable Utilities
[list: import path + one-line description]

## Constraints
[lint rules, type system requirements, gating, project guidelines]
```

---

## Anti-patterns

- Don't write a plan. Return findings only.
- Don't write tests or implementation steps. That's atdd-plan's job.
- Don't summarize or interpret beyond what you directly observed in the code.
- Don't read entire codebases. Focus on the feature area and one level out.
- Don't guess file paths. Verify they exist before reporting them.
- Don't skip Step 1 (prior attempts). Abandoned PRs contain critical context.

---

## Flow position

```
/flagrare:intake              ← context brief produced
     ↓
/flagrare:atdd-plan
     ├── /flagrare:codebase-explore   ← THIS SKILL (returns raw findings)
     ├── writes acceptance tests
     ├── names design patterns
     ├── SOLID audit
     └── gap review
```

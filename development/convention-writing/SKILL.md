---
name: convention-writing
description: How to analyze a codebase for recurring patterns and write effective convention specs that standardize them.
compatibility: opencode
metadata:
  audience: convention-author
  purpose: convention-authoring
---
## What I do

Teach the convention-author agent how to identify patterns worth standardizing, search a codebase for existing instances, and produce convention specs that are concrete, scoped, and actionable.

## When to use me

Load this skill when running the `/convention` command or when a delivery lead asks for a new convention to be documented. The convention-author should load this before analyzing the codebase or writing a convention spec.

## Identifying patterns worth standardizing

Not every repeated pattern deserves a convention. A pattern is worth standardizing when it meets at least two of these criteria:

- **Frequency**: It appears in 5+ files or will appear in future work.
- **Inconsistency**: The codebase already shows 2+ different ways of doing the same thing, and the variation causes friction (bugs, confusion, wasted review cycles).
- **Impact**: Getting it wrong has real consequences — security holes, performance problems, broken contracts, or painful debugging.
- **Onboarding cost**: New contributors (human or agent) consistently get it wrong without explicit guidance.

Do not write conventions for patterns that are self-evident from the language or framework, enforced by linting rules already in place, or only relevant to a single file.

## Searching for existing instances

Before writing a convention, gather evidence. The convention must be grounded in what the codebase actually does, not what you wish it did.

1. **Find the pattern in use.** Search for the most distinctive element — a function name, import path, annotation, file naming pattern, or structural marker. Use glob patterns to find files and grep to find usage.
2. **Count instances.** How many files follow the pattern? How many deviate? If deviations outnumber conforming instances, the convention is aspirational — note this explicitly and explain the migration path.
3. **Identify the best examples.** Find 2–3 files that implement the pattern cleanly. These become the Examples section of the convention spec.
4. **Identify the worst violations.** Find 2–3 files that get it wrong. These become the Anti-patterns section.
5. **Check for prior art.** Search the `.hero/conventions/` directory for existing conventions that overlap. If one exists, update it rather than creating a duplicate.

## Writing the convention spec

Convention specs live in `.hero/conventions/{slug}/spec.md`. Use the convention template from the spec-format skill.

### Frontmatter

```yaml
---
type: convention
status: draft
scope: [glob patterns]
tags: [relevant tags]
---
```

- `type` must be `convention`.
- `status` starts as `draft`. It moves to `active` after review confirms the convention reflects actual codebase practice (or a deliberate decision to change practice).
- `scope` is an array of glob patterns that identify which files this convention applies to. This is how `hero relevant` knows to surface the convention when an agent touches matching files.
- `tags` categorize the convention for search and filtering.

### Scope definition

Scope globs determine when `hero relevant` injects this convention into agent instructions. Get them right — too broad and the convention clutters every context block; too narrow and it misses files where it matters.

Good scope patterns:
- `src/api/**/*.ts` — all API route files
- `**/migrations/*.sql` — all SQL migration files
- `*.go` — all Go source files
- `src/components/**/*.tsx` — all React components
- `**/test/**` — all test files regardless of language

Bad scope patterns:
- `*` — matches everything, appropriate only for truly universal conventions (naming, commit messages)
- `src/**` — too broad for most conventions; be specific about which subdirectories

When in doubt, start narrow. You can always widen scope later.

### Pattern section

One clear statement of what this convention standardizes. Not a paragraph — a sentence or two. The reader should immediately understand what this is about.

Good: "All API error responses use the `ApiError` class and return a consistent `{ error, code, details }` shape."

Bad: "This convention is about how we handle errors in our API layer to ensure consistency across the codebase."

### When to apply section

State the conditions precisely. Name file types, modules, situations. The agent reading this needs to know: "Does this apply to the code I'm about to write?"

### How section

Show the specific implementation pattern. Include code snippets from the actual codebase. Reference real file paths. If there are multiple valid approaches within the convention, show each one and when to use which.

### Examples section

Pull real examples from the codebase. Include file paths. Show enough code to demonstrate the pattern in context, not just the single line that matches. Agents need to see the surrounding structure.

### Anti-patterns section

Show real violations from the codebase (or realistic constructed examples if the codebase is clean). Explain *why* each anti-pattern is problematic — not just "don't do this" but "this causes X problem."

### Exceptions section

Every convention has edge cases. Name them. If there are no exceptions, say "None identified" rather than leaving the section out — this signals the convention-author actually considered it.

## Consolidate vs split

Write one convention per concern. If you find yourself writing a convention that covers both "how to name files" and "how to structure API responses," split them. Each convention should be independently understandable and independently scoped.

Consolidate when two draft conventions have the same scope, the same audience, and would always be read together. In that case, merge them under the broader name.

## Quality bar

A convention is ready for `active` status when:
- The Pattern section is a single clear statement
- Scope globs are tested — they match the files you intend and don't match files you don't
- Examples reference real files in the codebase with real code
- Anti-patterns explain the *consequence* of violation, not just the violation itself
- The convention has been checked against existing conventions for overlap or conflict
- A reader who has never seen the codebase can follow the convention after reading this document

---
name: spec-guide
description: Use when authoring a new Executable Implementation Spec (EIS) from a natural-language description. Triggers on "write an EIS", "create new EIS", "executable implementation spec", "/create-feature". Teaches the EIS file format, numbering, required sections, the grounding rule (must verify against src/ before writing), and the wiki-companion rule (summary under docs/wiki/eis/ plus index update).
---

# EIS Writing

Author an EIS that follows the established format in `docs/eis/`. An EIS is a concrete, codebase-grounded implementation plan — not a design doc, not a PRD.

## 1. Naming & location

- Path: `docs/eis/EIS-<###>-<kebab-slug>.md` (three-digit zero-padded number).
- The number is the next unused integer. `ls docs/eis/EIS-*.md` to find the highest, then +1.
- Slug is lowercase kebab, 2–5 words, describes the feature (`stripe-integration`, `security-hardening`, `api-auth-tenant-isolation`).
- The raw EIS lives at `docs/eis/`. The directory `docs/wiki/eis/` is ONLY for wiki summaries — never put the full spec there.

## 2. Required sections (in order)

Every existing EIS uses these. Use the same names.

1. `# EIS-<###>: <Title Case Name>` — H1 title.
2. `## Problem` — what is wrong today, with file paths and line references. Often broken into numbered sub-problems (`### 1. …`). Cite real files.
3. `## Scope` — a markdown table listing affected files + the issue/status for each. Columns vary (`File | Issue | Severity` or `File | Status | Issue` or `File | Current Behavior | Gap`), pick what fits.
4. `## Solution Design` — the plan, broken into streams or numbered sub-sections, each with a short prose explanation and TypeScript code blocks showing the intended shape (imports, function signatures, key logic). Code is illustrative, not exhaustive.
5. `## Files to Create` — table: `File | Purpose`. Omit if nothing new is created.
6. `## Files to Modify (with specific changes)` — table: `File | Change`. The Change cell is a crisp imperative sentence per file.
7. `## Dependencies` — bullet list: other EIS that must land first, env vars required, schema/migration concerns, external services.
8. `## Complexity: <S|M|L>` — single letter, then bullets on scope size (file count, testing notes, risk areas).

Do not invent new top-level sections. If something doesn't fit, put it inside Solution Design as a numbered sub-section.

## 3. Template

```markdown
# EIS-<###>: <Title>

## Problem

<1–2 paragraphs stating the gap. Then numbered sub-problems:>

### 1. <Sub-problem>
- `src/path/to/file.ts` — what it does wrong.
- Consequence (security, correctness, UX).

### 2. <Sub-problem>
- …

## Scope

| File | Issue | Severity |
|------|-------|----------|
| `src/…` | <what's broken> | High/Medium/Low |

## Solution Design

### 1. <Stream or fix name>

<Prose.>

```typescript
// Illustrative code for src/lib/foo.ts
export function foo() { … }
```

### 2. <Next stream>

…

## Files to Create

| File | Purpose |
|------|---------|
| `src/lib/new-thing.ts` | <why> |

## Files to Modify (with specific changes)

| File | Change |
|------|--------|
| `src/app/api/x/route.ts` | <Imperative: "Add Zod validation via fooSchema.safeParse(body)"> |

## Dependencies

- EIS-XXX must land first because …
- Requires env var `FOO_SECRET`.
- Schema migration: add column `bar` to `Baz`.

## Complexity: M

- N new files (~X lines), M files modified.
- <Testing note>.
- <Risk note>.
```

## 4. Grounding rule (MANDATORY)

Before writing a single line of the EIS, you must have scanned the live codebase. Concretely:

- Use `Grep`/`Glob` to locate every file you will reference in Scope, Files to Create, and Files to Modify.
- Every file path in the EIS must exist (or be a believable new file under an existing directory).
- Every "currently does X" claim in Problem must be backed by lines you actually read.
- When Solution Design says "modify `functionName()` in `src/lib/foo.ts`", that function must exist there today (or the EIS must explicitly say it is being introduced).

If a natural-language request asks for something you cannot ground in the codebase, stop and ask the user to clarify — do not hand-wave paths.

## 5. Wiki companion rule

Every new EIS ships with a summary page plus an index update. When you create `docs/eis/EIS-<###>-<slug>.md`, also:

1. Create `docs/wiki/eis/EIS-<###>.md` — a 1-page wiki summary.
   - Wiki frontmatter (match the style already in `docs/wiki/eis/` — check an existing file or the wiki conventions first).
   - Short prose: what problem, what solution approach, complexity.
   - A link back to the raw source at `../../eis/EIS-<###>-<slug>.md`.
2. Update `docs/wiki/index.md` — add the new EIS to whatever list/section the index uses for EIS entries (mirror existing formatting).

Do not dump the full spec into the wiki file; the wiki is a navigable summary, the raw EIS is the source of truth.

## 6. Overlap check (before creating)

Read the titles + Problem sections of every existing `docs/eis/EIS-*.md`. If the NL description overlaps with an existing EIS (same files, same feature area, same gap):

- **Do not create a duplicate.**
- Either: extend the existing EIS (add a new sub-problem in Problem, new rows in Scope, new numbered Solution Design section). Return a clear diff of what you added.
- Or: abort and surface the conflict to the user — tell them which EIS overlaps and ask whether to extend it, supersede it, or proceed with a narrower scope.

Overlap signals: same `src/` files appear in the existing EIS's Scope table; same subsystem (auth, stripe, storefront, etc.); same issue numbers referenced.

## 7. Final checklist before returning

- [ ] Filename matches `EIS-<###>-<kebab-slug>.md`, number is next available.
- [ ] All 8 required sections present in order.
- [ ] Every file path referenced has been verified in the codebase.
- [ ] No duplicate of an existing EIS.
- [ ] Wiki summary at `docs/wiki/eis/EIS-<###>.md` created.
- [ ] `docs/wiki/index.md` updated.
- [ ] Complexity rating (S/M/L) set with justifying bullets.

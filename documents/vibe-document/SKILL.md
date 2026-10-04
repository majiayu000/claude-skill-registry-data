---
name: vibe-document
description: >
  Generates complete documentation for vibe-* projects — inline code docs,
  README.md, CHANGELOG.md, API reference, and component library docs.
  Scans all source files and documents everything in one session.
  Triggers on "document:" prefix, "write docs for", "generate documentation",
  "add JSDoc", "add docstrings", "document this feature", "we need a README",
  "generate a changelog", "document the API", "document the components",
  "missing docs", "no documentation".
  Runs automatically after vibe-init on undocumented legacy projects,
  after vibe-add-feature to document what was built, and when vibe-review
  flags missing documentation as P1 or P2.
  Always use when documentation is absent, incomplete, or out of date.
  Shows full doc plan first — writes everything on explicit approval.
---

# Vibe Document Skill

Generates complete, accurate documentation grounded in actual code.
Inline docs in source files. Standalone markdown docs at project root.
Everything documented in one session. No gaps left for later.

**Runs in agent mode (Claude Code / Cursor). Requires filesystem access.**

---

## The principle this enforces

Documentation written after the fact from memory is inaccurate.
Documentation generated from the actual code is honest.

This skill reads the source first, documents what it finds —
not what someone thinks is there.

---

## Entry points

### Entry point A — On demand
Triggered by: `document:`, "write docs for X", "generate documentation", "missing docs"

Default scope: scan all source files, document everything in one session.
If the user specifies a narrower scope ("document the API" / "document the auth module")
— scope to that area only. Confirm scope before proceeding.

Go to **Step 0**.

### Entry point B — After vibe-init
Triggered automatically at the end of a `vibe-init` session on a legacy project.

The codebase has just been scanned — CODEBASE.md is fresh and accurate.
No additional scanning needed for Step 1.
Scope: full project — everything.
Go to **Step 0** → skip the scan in Step 1, read directly from CODEBASE.md.

### Entry point C — After vibe-add-feature
Triggered automatically at the end of a `feature:` session.

Scope: files listed in `FEATURE_TASKS.md` under **Touches** + any new files created.
README.md is always updated regardless of scope.
**CHANGELOG.md: defer to `vibe-changelog` if it is available** (it owns changelog
generation — git-tag-scoped, dev + client versions). Only generate a CHANGELOG.md
here as a fallback when vibe-changelog isn't installed. This avoids two skills
writing conflicting CHANGELOG.md files.
Go to **Step 0**.

### Entry point D — After vibe-review flags docs
Triggered when `vibe-review` produces P1/P2 findings for missing documentation.

Read the review report to identify exactly which files were flagged.
Scope to those files only for inline docs.
README.md, CHANGELOG.md, API reference, component docs — update all.
Go to **Step 0**.

---

## Step 0 — Read project context

**Large codebase check — run first, before reading anything:**

```bash
find . -type f \
  \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.py" -o -name "*.dart" -o -name "*.go" -o -name "*.rb" \) \
  ! -path '*/node_modules/*' ! -path '*/.git/*' \
  ! -path '*/dist/*' ! -path '*/build/*' \
  ! -path '*.test.*' ! -path '*.spec.*' \
  | wc -l
```

**Set documentation budget by source file count:**

| Size | Source files | Strategy |
|------|-------------|----------|
| Small | < 30 | Document all files in one session |
| Medium | 30–80 | Document all files — batch by folder |
| Large | 80–150 | Document exports only per file; full docs on critical modules |
| XL | 150+ | Document by module — present module list, user picks priority order |

**For Large (80–150 source files):**
- Document every export (public API) fully
- For internal functions: one-line summary only, not full JSDoc
- Critical modules (entry points, services, API routes) get full documentation
- Tell the user: "Large project ([N] source files). Documenting all exports fully,
  internals with summaries. Run `document: [folder]` to get full docs on specific areas."

**For XL (150+ source files):**
- Do not attempt to document everything in one session — context will run out
- Present the module list from CODEBASE.md section 3
- Ask: "This project has [N] source files. Which modules should I document first?
  I'll work through them in priority order across sessions."
- Wait for the user to prioritise before proceeding
- Document chosen modules fully, flag the rest as pending

Store the size classification. Apply the strategy throughout Steps 1–7.

Read in this order:

1. `vibe/ARCHITECTURE.md` — naming conventions, code style, language (affects doc format)
2. `vibe/CODEBASE.md` — full file map, routes, components, patterns, stack
3. `vibe/SPEC.md` — feature descriptions and acceptance criteria (drives README content)
4. `vibe/DECISIONS.md` — all entries (drives CHANGELOG content)
5. `CLAUDE.md` — project overview, commands

**Detect documentation format from stack (CODEBASE.md section 1):**

| Language | Inline doc format |
|----------|------------------|
| TypeScript / JavaScript | JSDoc (`/** */`) |
| Python | Google-style docstrings (`"""`) |
| Dart / Flutter | DartDoc (`///`) |
| Go | GoDoc (`//`) |
| Ruby | YARD (`# @param`) |

**Detect existing docs:**
```bash
# Check for existing README
ls README.md README.rst README.txt 2>/dev/null

# Check for existing CHANGELOG
ls CHANGELOG.md CHANGELOG.txt 2>/dev/null

# Check for existing API docs
ls docs/ api-docs/ 2>/dev/null

# Sample inline doc coverage
grep -rn "/\*\*\|\"\"\"|\s*///" \
  --include="*.ts" --include="*.tsx" \
  --include="*.py" --include="*.dart" \
  . | grep -v node_modules | wc -l
```

---

## Step 1 — Scan source files

**Entry B:** Skip this step — CODEBASE.md already has the full file map.

**XL projects:** Skip this step — module list was confirmed with user in Step 0.
Scope is already set to chosen modules only.

**All other entries:**

Scan source files within scope. Apply the budget from Step 0:

```bash
find . -type f \
  \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.py" -o -name "*.dart" -o -name "*.go" -o -name "*.rb" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" \
  ! -path "*/dist/*" ! -path "*/build/*" \
  ! -path "*/__pycache__/*" ! -path "*/.next/*" \
  ! -path "*.test.*" ! -path "*.spec.*" \
  | sort
```

For each file, classify:
- `UNDOCUMENTED` — no inline docs at all
- `PARTIAL` — some functions/classes documented, some not
- `COVERED` — all exports documented

Read `UNDOCUMENTED` and `PARTIAL` files in full.
For `COVERED` files — skip inline docs, still include in API/component doc if applicable.

---

## Step 2 — Build the documentation plan

Read `references/DOC_PLAN_TEMPLATE.md` for the full format.

For each output type, list exactly what will be written:

**Inline docs:**
For each `UNDOCUMENTED` or `PARTIAL` file:
- File path
- Functions/classes/components to document (every export + every function)
- Current coverage: N documented, N missing

**README.md:**
- Exists: yes/no
- Action: create from scratch / update existing
- Sections: (see Step 4)

**CHANGELOG.md:**
- Exists: yes/no
- Action: create from scratch / update existing
- Entries to generate: N features, N fixes, N decisions (from DECISIONS.md)

**API reference (`docs/API.md`):**
- Routes to document: N endpoints (from CODEBASE.md section 5)
- Exists: yes/no

**Component docs (`docs/COMPONENTS.md`):**
- Components to document: N components (from CODEBASE.md section 7)
- Exists: yes/no

Present the full plan:

> "Documentation plan across [N] files:
> Inline docs: [N] files ([N] undocumented, [N] partial)
> README.md: [create / update]
> CHANGELOG.md: [N] entries from DECISIONS.md
> API reference: [N] endpoints
> Component docs: [N] components
>
> **Approve to begin writing. Say 'go' or 'approved'.**"

**Wait for explicit approval. Do not write anything before this.**

---

## Step 3 — Write inline docs

After approval, write inline docs first — they are the foundation everything else references.

Process files in this order:
1. Entry points and core modules (highest impact)
2. Services and utilities
3. Components
4. Helpers and minor utilities

**For each file:**

Read the file in full. For every function, class, and component — document it.

**Document every export AND every internal function.**
No exceptions — this was the chosen approach.

**JSDoc format (TypeScript / JavaScript):**
```typescript
/**
 * [One sentence — what this does, not how it does it]
 *
 * @param {Type} paramName - [what this parameter is]
 * @param {Type} paramName - [what this parameter is]
 * @returns {Type} [what is returned and when]
 * @throws {ErrorType} [when this throws, if applicable]
 *
 * @example
 * [Minimal working example — real values, not placeholders]
 */
```

**Google docstring format (Python):**
```python
def function_name(param: Type) -> ReturnType:
    """One sentence — what this does.

    Args:
        param: What this parameter is.

    Returns:
        What is returned and when.

    Raises:
        ErrorType: When this raises.

    Example:
        >>> function_name(value)
        expected_output
    """
```

**DartDoc format (Flutter / Dart):**
```dart
/// One sentence — what this does.
///
/// [param] is what this parameter is.
/// Returns [ReturnType] representing what.
///
/// Example:
/// ```dart
/// functionName(value);
/// ```
```

**Quality rules for all inline docs:**
- First line is always a sentence describing behaviour, not implementation
- No "this function does X" — just "Does X"
- Parameters described by what they represent, not their type
- Examples use real values — never `foo`, `bar`, `example`
- Never restate the function signature in prose
- Never document `console.log` calls or trivial one-liners

**For React/Vue components — document props:**
```typescript
/**
 * [What this component renders and when to use it]
 *
 * @param props.propName - [what this prop controls]
 * @param props.propName - [what this prop controls, and its default]
 *
 * @example
 * <ComponentName propName={value} />
 */
```

Write each file. Do not run anything — inline docs don't require execution.
After writing a file, move immediately to the next.

---

## Step 4 — Write README.md

Generate at project root. Two-section structure — one README, two audiences.

Read `references/README_TEMPLATE.md` for the full template.

```markdown
# [Project Name]

[One sentence — what this project does and who it's for]

---

## For the team

### What this is
[2-3 sentences — technical context, what problem it solves]

### Stack
| Layer | Technology | Version |
[From CODEBASE.md section 1]

### Getting started
```bash
# Install
[from CLAUDE.md / CODEBASE.md section 2]

# Development
[dev command]

# Tests
[test command]

# Lint
[lint command]
```

### Project structure
[Folder map from CODEBASE.md section 3 — key folders only]

### Architecture
[2-3 sentences from ARCHITECTURE.md overview]
Full detail: `vibe/ARCHITECTURE.md`

### Key decisions
[Top 3-5 decisions from DECISIONS.md — tech choices, not scope changes]

### Contributing
[Conventions from ARCHITECTURE.md — naming, commit format, branch strategy]

---

## For the client

### What was built
[Plain English — what the system does, what problem it solves]
[No technical jargon. Written for a non-technical reader.]

### Features
[Each feature from SPEC.md — one paragraph per feature, plain English]

### How to access
[URLs, login, credentials location — or "provided separately"]

### Reporting issues
[Who to contact and how]

---

*Last updated: [date] · Generated by vibe-document*
```

**If README.md already exists:**
Read it first. Preserve any sections not covered by the template.
Update outdated content. Add missing sections. Do not delete anything.

---

## Step 5 — Write CHANGELOG.md

Read `vibe/DECISIONS.md` in full.

Map every entry to a changelog category:

| DECISIONS.md type | CHANGELOG category |
|------------------|-------------------|
| `scope-change` (addition) | Features |
| `scope-change` (removal) | Removed |
| `drift` / `blocker-resolution` | Fixes |
| `tech-choice` | Decisions |
| `discovery` | Decisions |
| Bootstrap entry (vibe-init) | Project start |

Generate `CHANGELOG.md` at project root:

```markdown
# Changelog

All notable changes to this project are documented here.
Generated from vibe/DECISIONS.md — updated by vibe-document.

---

## Features

### [Feature name] — [date]
[One paragraph: what was added and what it enables]
[Source: D-[ID] in vibe/DECISIONS.md]

### [Feature name] — [date]
...

---

## Fixes

### [Fix description] — [date]
[One paragraph: what was broken, what was fixed]
[Source: D-[ID] in vibe/DECISIONS.md]

---

## Decisions

### [Decision title] — [date]
[One paragraph: what was decided and why]
[Source: D-[ID] in vibe/DECISIONS.md]

---

## Project start — [init date]
Project onboarded / initialised.
[Stack confirmed during init or brainstorm]

---

*Generated by vibe-document on [date]*
*Source: vibe/DECISIONS.md*
```

**Within each group: newest first.**
**If CHANGELOG.md already exists:** append new entries only. Never rewrite existing entries.

---

## Step 6 — Write API reference (docs/API.md)

Create `docs/` folder if it doesn't exist.

Read `vibe/CODEBASE.md` section 5 (routes/endpoints) in full.
For each route, read the actual handler file to understand request/response shape.

Generate `docs/API.md`:

```markdown
# API Reference

Base URL: `[from .env.example or CODEBASE.md]`
Authentication: `[observed auth pattern — Bearer token / cookie / none]`

---

## [Resource name — e.g. Authentication]

### [METHOD] [/path]

[One sentence — what this endpoint does]

**Authentication required:** [yes / no]

**Request**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| [field] | [type] | [yes/no] | [description] |

**Response — 200**
```json
{
  "[field]": "[type — description]"
}
```

**Response — [error code]**
```json
{
  "error": "[description of when this occurs]"
}
```

**Example**
```bash
curl -X [METHOD] [base-url][/path] \
  -H "Authorization: Bearer [token]" \
  -d '{"field": "value"}'
```

---
[Repeat per endpoint, grouped by resource]
```

**For each endpoint — read the actual handler:**
Request fields from the validation schema (Zod / Pydantic / Joi).
Response shape from what the handler returns.
Error responses from the try/catch or error middleware.
Never invent fields — document only what the code actually handles.

---

## Step 7 — Write component docs (docs/COMPONENTS.md)

Read `vibe/CODEBASE.md` section 7 (key components) in full.
For each component, read the actual source file.

Generate `docs/COMPONENTS.md`:

```markdown
# Component Library

All reusable components in this project.
Generated from source — props match actual implementation.

---

## [ComponentName]

**File:** `[path/to/Component.tsx]`

[One sentence — what this component renders and when to use it]

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| [prop] | [type] | [yes/no] | [value / —] | [description] |

### Usage

```tsx
<ComponentName
  requiredProp={value}
  optionalProp={value}
/>
```

### States

| State | When | What renders |
|-------|------|--------------|
| Default | [condition] | [description] |
| Loading | [condition] | [description] |
| Empty | [condition] | [description] |
| Error | [condition] | [description] |

### Notes

[Anything non-obvious about usage, composition, or constraints]

---
[Repeat per component]
```

**Props must be read from actual TypeScript interface / PropTypes / function signature.**
Never invent props. If a prop's purpose isn't clear from the name, read the component body.

---

## Step 8 — Update vibe docs

**vibe/CODEBASE.md:**
If `docs/` folder was created: add to section 3 (folder map).
If new documentation patterns were established: note in section 10.

**vibe/TASKS.md:**
Update "What just happened":
```
## What just happened
✅ Documentation complete — [date]
   Inline docs: [N] files documented
   README.md: [created / updated]
   CHANGELOG.md: [N] entries
   API reference: [N] endpoints — docs/API.md
   Component docs: [N] components — docs/COMPONENTS.md
```

**vibe/reviews/backlog.md:**
If any review P1/P2 docs findings triggered this run:
Mark them resolved: `✅ [finding] — RESOLVED by vibe-document [date]`

---

## Step 9 — Report

```
✅ vibe-document complete

INLINE DOCS
  Files documented:   [N]
  Functions covered:  [N]
  Components covered: [N]
  Format:             [JSDoc / docstrings / DartDoc]

STANDALONE DOCS
  README.md           [created / updated] — [N] sections
  CHANGELOG.md        [created / updated] — [N] entries
  docs/API.md         [created / updated] — [N] endpoints
  docs/COMPONENTS.md  [created / updated] — [N] components

REVIEW FINDINGS RESOLVED
  [List resolved P1/P2 items — or "None (on-demand run)"]

WHAT'S NEXT
  review:    ← docs findings should now be clear
  deploy:    ← README and CHANGELOG ready for handoff
```

---

## Absolute rules

**Never invent.** Every parameter description, response field, and prop comes
from reading the actual source. If it's not in the code, it's not in the docs.

**Never restate the signature.** "Takes a string and returns a boolean" when the
signature already shows `(name: string): boolean` is noise. Document the *why*
and *when*, not the *what* that's already visible.

**Never leave placeholders.** `@param name - The name parameter` is useless.
`@param name - The user's display name shown in the nav bar` is documentation.

**Always write the example.** Examples are the most-read part of any doc.
Every JSDoc and docstring gets one — using real values from the actual domain.

**Never modify test files.** This skill documents source files only.
Test files are self-documenting through their test names.

**README client section must be jargon-free.**
No mention of TypeScript, REST, ORM, or any technical term a non-developer
wouldn't recognise. If it's technical, it belongs in the team section.

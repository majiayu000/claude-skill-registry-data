---
name: reference-app
description: "Analyze a fully-built reference application that the user wants to use as a model. Reads its architecture, conventions, tech stack, and patterns; stores a structured summary in .claude/memory/reference/ so subsequent sessions can compare the current project against it."
argument-hint: "<path-to-reference-application>"
---

# /reference-app

Point Claude at another fully-developed application the user wants to use as a reference. Build a structured understanding of it. Store that understanding in memory so future sessions can compare the current project against it.

## When to use

- The user is starting a new project and wants it modeled on one they've already built.
- The user is reviewing the current project's code and wants you to compare it against an existing well-built example.
- The user is migrating, refactoring, or modernizing and the reference app shows the destination state.
- The user wants you to "understand" their full app even though you're working in a different directory today.

## Operating method — ASK FIRST, THEN ANALYZE

**Step 0: Confirm intent.**

Before reading anything, ask:

- "What would you like me to learn from this reference app?" — pattern conventions / architecture / specific module / all of it.
- "What does the current project share with the reference?" — same domain / same stack / similar feature / different / unsure.
- "Should I treat the reference as authoritative (apply its patterns here) or as inspirational (consider its patterns)?"

These three answers shape the depth and tone of the resulting memory. Don't skip them.

**Step 1: Validate the path.**

- Confirm the path exists and is readable.
- Check it has a recognizable project structure (package.json, pyproject.toml, go.mod, Cargo.toml, etc.). If not, ask the user what kind of project it is.

**Step 2: High-level scan (light pass).**

Read in this order, one file each, no deep dives yet:
- Top-level README.
- `CLAUDE.md` if it exists.
- The package/dependency manifest.
- The deployment / CI config.
- The directory tree (one level deep, maybe two).

**Step 3: Architecture map.**

- Identify the entry points (server start, client root, CLI commands).
- Identify the main modules and their responsibilities (one sentence each).
- Identify external dependencies that matter to the architecture (DB, queue, cache, auth, payment, etc.).
- Identify the testing approach (framework, layering).
- Identify the deploy target.

**Step 4: Convention mining.**

Read 5–10 representative files (one component, one route, one test, one util, one type definition, one style file). Extract:

- Naming conventions (camelCase, kebab-case, file-per-export, etc.).
- File organization (feature folders vs technical folders, co-located tests).
- Error handling pattern.
- API contract style (REST/GraphQL, error shape).
- State management approach.
- Styling approach.
- Logging and observability.
- Auth and session pattern.

**Step 5: Distinctive choices.**

What did this project do that's *different* from defaults? These are the high-information signals — they reveal taste and constraints.

- Custom build tooling.
- Hand-rolled abstractions where the framework would have done it.
- Strong opinions reflected in lints, hooks, or architecture rules.
- Specific tradeoffs visible in code comments or commit messages.

**Step 6: Write the memory.**

Create `.claude/memory/reference/<reference-app-name>.md` with the schema:

```markdown
---
name: ref-<app-name>
type: reference
description: <one-line, e.g., "Reference app: AcmeShop — Next.js + Drizzle + Postgres SaaS, used as architecture model">
created: <YYYY-MM-DD>
last-verified: <YYYY-MM-DD>
source-path: <path>
authority-level: authoritative | suggestive | inspirational
---

# Reference: <app-name>

> Authority: <as set by user in step 0>. Cite when applying.

## Stack
- Language(s):
- Frameworks:
- Database:
- Auth:
- Deployment:
- Testing:

## Architecture (one paragraph + a small Mermaid diagram if it helps)

## Key conventions
- File organization:
- Naming:
- API style:
- State management:
- Error handling:
- Styling:
- Tests:

## Distinctive choices
- Choice 1: what they did, what it cost, what it bought.
- Choice 2: …

## Useful prior art for the current project
(populated when comparing to current — left blank initially)

## What NOT to copy
(blank initially; filled in when patterns are noted to be tied to the source's specific constraints)
```

Add an entry to `.claude/memory/MEMORY.md` under the Reference section.

**Step 7: Confirm with the user.**

Show the resulting memory. Ask:
- "Does this match your understanding of the reference?"
- "Anything to correct or add?"
- "What part of this should I apply when working on the current project?"

## When the user later asks for a code review or build help

The memory is now in context. Use it like this:

- When the current project does something differently from the reference: surface it and ask. "Reference uses Drizzle; current project is using raw SQL queries. Intentional, or should we standardize?"
- When suggesting an approach: cite the reference. "In `acmeshop` (your reference) you used a feature-folder layout — same here?"
- Don't silently import a pattern. Always ask: "Reference handles this with X; want the same here?"

## Boundaries

- Never modify the reference app — read-only.
- Never assume the reference is current best practice. Patterns from one project may be wrong for another.
- Never bury the source. Every recommendation drawn from the reference cites it.
- Don't analyze without permission. Step 0 is mandatory.
- If the reference contains secrets visible in committed files, redact them in memory and tell the user they're in the reference repo (so they can rotate).

## Output format

```
## Reference: <app-name>
- Path: <path>
- Authority: <suggestive | authoritative>
- Memory written: .claude/memory/reference/<app-name>.md

## Quick summary
- Stack: <one line>
- Architecture shape: <one line>
- 3 most distinctive choices:
  1. …
  2. …
  3. …

## Ready to use
You can now ask things like:
- "Compare the auth in the current project to <ref>."
- "How does <ref> handle billing? Set up the same here."
- "Where does <ref> put feature flags? Should we follow that?"
- "Review my current code against <ref>'s conventions."
```

---
name: write-app-spec
description: Analyzes a codebase and writes a SPEC.md that documents the app's functionality, screens/pages, core logic, and data models in a PRD-adjacent but implementation-focused format. Use when the user asks to write a spec, create SPEC.md, document what the app does, or produce a functional specification. Triggers on requests like "write a spec for this app", "create SPEC.md", "document the features", or "write a PRD-like doc focused on functionality".
---

# write-app-spec

Explore the codebase, then write a SPEC.md documenting what the app does and how.

## Workflow

### 1. Explore

Before writing, identify:
- **Entry point / app shell** — routing, screen/state management, top-level data flow
- **Screens / pages** — one section per distinct screen or route
- **Core logic** — algorithms, calculations, data transformations (not UI)
- **Data model** — key data structures and their shapes

Use Glob + Read for targeted reads. For larger codebases, delegate to the Explore agent.

### 2. Write SPEC.md

Follow the format in [references/spec-format.md](references/spec-format.md).

Key rules:
- One `## Screen` section per distinct screen or route
- Use the **Behavior** subsection for edge cases and conditional logic
- Keep **Core Logic** separate from UI — describe inputs, process, and output
- Write in English unless the codebase is clearly in another language

### 3. Output

Write `SPEC.md` in the project root unless the user specifies otherwise.
After writing, give a one-line summary of what was documented.

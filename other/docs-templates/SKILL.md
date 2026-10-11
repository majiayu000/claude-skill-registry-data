---
name: docs-templates
description: Templates for docs/ — project, tech, architecture, standards.
---

## Source Synthesis Rule

Before generating each doc, read every relevant file found in the Project Docs Discovery scan:

1. **Read** the source file
2. **Synthesize** — extract and condense into the target section (tables or bullets; never copy verbatim)
3. **Add `## Source References`** at the end listing every file that contributed content

```markdown
## Source References
| File | Sections Fed |
|------|-------------|
| [ARCHITECTURE.md](../../ARCHITECTURE.md) | System Type, Layers, Module Map |
```

Rules: only list files that provided content; use paths relative to project root; omit section if no sources found; future `docs-sync` updates must preserve and extend this section.

---

## `docs/project.md`

```markdown
<!-- last-updated: [YYYY-MM-DD] -->
# Project: [name from README or directory]

## What It Does
[1-2 sentences from README or inferred from scan]

## Type & Config
PROJECT_TYPE: [new|inherited|maintenance]
TESTS_REQUIRED: [yes|no]
CICD_PLATFORM: [detected or answered in Step 3]
[CLOUD_PROVIDER: omit if not applicable]
[ISSUE_TRACKER: omit if none]

## Active Areas
[From git log — omit for new projects with no commits]
| Directory | Purpose | Last Active |
|-----------|---------|-------------|

## Key Constraints
[Hard rules from existing CLAUDE.md; omit if no prior CLAUDE.md]
```

---

## `docs/development/tech-stack.md`

```markdown
<!-- last-updated: [YYYY-MM-DD] -->
# Tech Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
[From package.json / composer.json / requirements.txt / Gemfile / go.mod / Cargo.toml / Dockerfile.
Include: language, framework, database, cache, queue, auth, test runner, CI/CD.
Omit rows for layers not present.]

## Dev Setup
[From README or package.json scripts — 1–3 commands; omit if unknown]

## Notable Dependencies
[Non-obvious deps that affect how agents write code — omit well-known framework staples]
```

---

## `docs/development/architecture.md`

```markdown
<!-- last-updated: [YYYY-MM-DD] -->
# Architecture

## System Type
[inherited/maintenance: infer from scan (e.g., "Decoupled REST API + React SPA")]
[new: <!-- TODO: software-architect to define -->]

## Layers
| Layer | Directory | Responsibility |
|-------|-----------|---------------|
[inherited/maintenance: infer from top-level directory structure]
[new: <!-- TODO: software-architect to define -->]

## Module Map
| Module/Service | Purpose | Key Entry Points |
|---------------|---------|-----------------|
[inherited/maintenance: populate from scan]
[new: <!-- TODO: software-architect to complete -->]
```

---

## `docs/development/code-standards.md`

```markdown
<!-- last-updated: [YYYY-MM-DD] -->
# Code Standards

## Detected Config
[From .eslintrc / .prettierrc / phpcs.xml / pyproject.toml / .rubocop.yml / golangci.yml.
Omit section if no config files found.]
| Tool | Config File | Key Settings |
|------|------------|-------------|

## Naming Conventions
<!-- TODO: software-architect to define, or auto-detect from existing code patterns -->

## Established Patterns
<!-- TODO: software-architect or code-reviewer to complete -->
```

---

## `docs/backlog/README.md`

```markdown
<!-- last-updated: [YYYY-MM-DD] -->
# Backlog

## Tracker
[From Step 3: "None" | "GitHub Projects: <url>" | "Jira: <workspace>" | "Linear: <team>" | ...]

## Sprint Files
| File | Sprint | Status |
|------|--------|--------|
| — | No sprints created yet | — |
```

---

## `docs/design/design-system.md` (UI projects only)

```markdown
<!-- last-updated: [YYYY-MM-DD] -->
# Design System

## UI Library
[Detected from package.json: shadcn/ui, MUI, Ant Design, Bootstrap, Chakra UI — or "Not yet chosen"]

## Color Tokens
<!-- TODO: ui-ux-designer to complete in Design Mode -->

## Typography Scale
<!-- TODO: ui-ux-designer to complete -->

## Component Inventory
<!-- TODO: ui-ux-designer to complete -->
```

---
name: setup-agent-code-style-deno
description: >-
  Use when the user asks to add Deno/TypeScript code-style rules to AGENTS.md,
  or during initial Deno project setup. Do NOT trigger for non-Deno TypeScript
  projects (use setup-agent-code-style-strict), or for runtime-agnostic style
  advice.
---

## Purpose
Integrates TypeScript/Deno coding standards into AGENTS.md to maintain consistency.

## Prerequisites
- AGENTS.md must exist in project root
- Project uses Deno

## File Target
- Target file is **AGENTS.md** (project agent definitions), NOT CLAUDE.md.
- If AGENTS.md does not exist, inform the user and stop.

## Injection Location
Add code style rules to AGENTS.md after the "Project tooling Stack" section, before "Architecture".

## Code Style Rules (to inject)

```markdown
## Code Style (Deno + TypeScript)

### Dependency Imports
- Use bare specifiers for dependencies defined in deno.json/imports
- Avoid direct jsr:/npm:/https: imports in source code
- Example: `import { assertEquals } from "@std/assert";` instead of `import { assertEquals } from "jsr:@std/assert";`
- **Exception:** Standalone scripts (e.g., in `framework/skills/*/scripts/`) that run without deno.json MUST use `jsr:` specifiers

### Dockerfile Optimization
- Use `deno compile` to create static binaries for production Docker images
- Implement multi-stage builds:
  - Compilation stage: `denoland/deno:latest`
  - Runtime stage: debian slim image
- Compile with explicit permissions: `--allow-net`, `--allow-read`, `--allow-env`
- Copy only compiled binary and necessary static files to runtime stage
- Set environment variables for proper network binding
```

## Workflow
- [ ] Read project AGENTS.md
- [ ] Locate "Architecture" section
- [ ] Insert code style rules before "Architecture"
- [ ] Verify proper markdown formatting
- [ ] No duplicate sections

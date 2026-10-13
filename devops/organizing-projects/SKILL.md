---
name: organizing-projects
description: >-
  Analyze, reorganize, and scaffold project repositories — structure audits, convention enforcement,
  migration planning, and new project scaffolding. Use this skill whenever someone asks about repo
  or codebase organization, project folder layout, naming conventions, monorepo decisions, file
  placement hygiene, structural debt, dead code, or how to start a new project with good structure.
  Triggers on: organize this project, clean up the repo, audit my structure, is this well organized,
  should this be a monorepo, fix my naming, restructure without breaking things, best layout for a
  new X project, scaffold a framework project, what folder structure should I use, or any question
  about where files should live. Even if the user mentions their codebase feels messy or asks about
  project conventions, use this skill.
version: "1.0.0"
---

<essential_principles>
**Philosophy**: Understand before restructuring. Detect before prescribing. Respect existing conventions unless they actively harm the project.

**Non-negotiable rules**:
- NEVER move, rename, or delete files without explicit user approval
- ALWAYS detect and respect .git, .env, symlinks, CI paths, Docker volumes, import aliases
- Flag security hygiene issues (exposed secrets, credentials in tracked files)
- Identify what's working well — don't reorganize for the sake of it
- Present all proposals as reviewable checklists with risk flags
- Scan for .gitignore gaps, leaked secrets, and tracked sensitive files before any restructuring

**Project classification taxonomy** (detect automatically from repo signals):

| Type | Key Signals |
|------|-------------|
| Single app (framework-specific) | package.json with framework dep, or pyproject.toml/setup.py with single entry point |
| Monorepo | packages/, apps/ dirs, workspace config (turbo.json, nx.json, pnpm-workspace.yaml) |
| Library/SDK | src/ + dist/ or build/, exports field in package.json, setup.py with packages= |
| Script collection | Flat structure, many small executables, no build system |
| Documentation site | docs/, mkdocs.yml, docusaurus.config.js, .vitepress/ |
| Data/ML project | notebooks/, data/, models/, requirements.txt with ML deps |
| Infrastructure/IaC | terraform/, .tf files, pulumi/, CDK dirs, ansible/ |
| Mixed workspace | Multiple of the above — needs triage before organizing |

**Organization quality signals** (score each 0-3):
- Convention consistency (naming, nesting depth, file placement)
- Discoverability (can a new dev find things in < 30 seconds?)
- Separation of concerns (config vs. code vs. docs vs. scripts vs. tests)
- Build/deploy hygiene (.gitignore coverage, artifact isolation)
- Documentation presence (README at root and key directories)
- Dead weight (orphaned files, stale branches, unused dependencies)
- Security posture (no secrets in tracked files, .env in .gitignore)
</essential_principles>

<intake>
**If the user's intent is already clear from their message, skip this menu and route directly using the routing table below. Show the menu only when intent is ambiguous.**

What would you like to do?

1. **Full project audit** — Comprehensive structure analysis with reorganization plan
2. **Quick health check** — Fast scan for common issues (naming, orphans, missing docs)
3. **Monorepo assessment** — Evaluate if/how to consolidate into monorepo structure
4. **Convention enforcement** — Standardize naming, nesting, and placement rules
5. **Migration planning** — Plan restructuring with ordered, risk-flagged steps
6. **New project scaffold** — Generate a best-practice starter structure for a greenfield project

**If intent is ambiguous, wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "full", "audit", "analyze", "organize", "clean up" | workflows/full-audit.md |
| 2, "quick", "health", "scan", "check" | workflows/quick-health-check.md |
| 3, "monorepo", "consolidate", "workspace" | workflows/monorepo-assessment.md |
| 4, "convention", "naming", "standardize", "fix naming" | workflows/convention-enforcement.md |
| 5, "migration", "restructure", "plan", "without breaking" | workflows/migration-planning.md |
| 6, "scaffold", "new project", "start a", "greenfield", "best layout for new", "what structure" | workflows/new-project-scaffold.md |

**Intent-based routing (if user provides clear intent):**
- "clean up this repo" → workflows/full-audit.md
- "is this well organized?" → workflows/quick-health-check.md
- "should this be a monorepo?" → workflows/monorepo-assessment.md
- "fix the naming" → workflows/convention-enforcement.md
- "how do I restructure without breaking things" → workflows/migration-planning.md
- "scaffold a Next.js app" / "best structure for a new Python service" → workflows/new-project-scaffold.md

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All in `references/`:
- **structure-patterns.md**: Best-practice layouts for every project type (Next.js, React, Python, Go, Rust, monorepo, IaC). Read when proposing target structure.
- **naming-conventions.md**: When to use kebab-case vs. snake_case vs. PascalCase, framework-specific rules, barrel file guidance. Read when auditing or enforcing naming.
- **risk-catalog.md**: Common things that break during restructuring (import paths, CI configs, Docker COPYs, alias maps, Vercel/Netlify configs, Prisma schema). Read before proposing any file moves.

All in `templates/`:
- **audit-report.md**: Output template for full audit results. Copy and fill for workflow 1.
- **migration-checklist.md**: Ordered migration steps with risk columns. Copy and fill for workflow 5.
</reference_index>

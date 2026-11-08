---
name: master-developer
description: Senior full-stack engineering workflow for Next.js, Node/Express, TypeScript, Prisma/PostgreSQL, Redis and Three.js work. Use when building or changing apps, APIs, bots, portfolios or 3D pages; fixing bugs; reviewing security (OWASP Top 10:2025); hardening, testing or deploying. Loads topic rules on demand.
---

# Master Developer

Working rules for production-quality code. Open only the reference files the task needs.

## Core rules
1. Read the code you will touch and its callers first. Follow the project's existing structure; add no files or features nobody asked for.
2. Do not break working code. New feature = new module; edit old files only when needed, with a small diff.
3. Start. Pick sensible defaults and say which. Ask one short question only when a wrong guess is costly or irreversible (data deletion, production deploy, paid services, public publishing).
4. Verify by running: `npx tsc --noEmit`, lint, tests, `npm run build`. Report results as they are, and name what was not run.
5. Security is part of every feature: validate input (Zod), authorize every route and object, parameterized queries, secure headers, no secrets in code, rate limits on public and auth routes.
6. Bug fixes: reproduce, find the root cause, fix it once in shared code, add a regression test. After three failed attempts, stop and report.
7. Never claim "100% secure" or "bug-free". Report evidence.
8. Output: new files whole, edits as diffs. End with what changed, what was not checked, and any risk.

## Which reference to open
| Task | File in `references/` |
|---|---|
| Starting any task, working style | senior-developer.md, project-rules.md, supreme-executor.md |
| Context and token use, long sessions | llm.md, token.save.md, token-compressor.md, infinite-runtime.md |
| UI, design tokens, layout | uiux.md, design-tokens.md, frontend-architecture.md |
| 3D, animation | threejs.md, performance.md |
| APIs and backend | api.md, backend.md |
| Database, Prisma, Supabase RLS | database.md |
| Encryption, hashing, JWT, key handling | security.md, crypto-vault.md |
| Security review (OWASP 2025) | security-check.md, web-analysis-shield.md |
| Scanning and self-testing own app | vulnerability.md, exploit-sandbox.md |
| Tests and quality gates | testing.md, zero-error-validator.md, absolute-perfection.md |
| Errors and bug loops | bugfix-loop.md, self-heal-engine.md |
| Release | deployment.md, auto-git-manager.md |
| Tools and MCP servers | mcp.md, mcp.json, auto-installer.md |
| New site, app or bot from a short request | omni-creator.md |
| Overview | master-manifest.md, singularity-core.md, CLAUDE.md |
| Reverse engineering (authorized targets only) | reverse-engineering.md |

## Companion skills in this plugin
Use these when the task matches; they are bundled unmodified (see THIRD_PARTY_NOTICES.md).
- Security and quality: security-review, security-scan, agent-security-hardening, mcp-dependency-review, tdd-workflow, verification-loop, coding-standards, e2e-testing, webapp-testing
- Backend and data: api-design, backend-patterns, database-migrations, postgres-patterns, prisma-patterns, docker-patterns, deployment-patterns, mcp-builder
- Frontend and UI/UX: frontend-patterns, frontend-a11y, nextjs-turbopack, web-design-guidelines (UI review), react-best-practices, composition-patterns, react-view-transitions
- Design (Anthropic): frontend-design, canvas-design, algorithmic-art, brand-guidelines, theme-factory, web-artifacts-builder; ui-ux-pro-max (searchable palettes, fonts, styles, UX rules: `python3 scripts/search.py "<product> <style>" --design-system`)
- Building skills and Claude API apps: skill-creator, claude-api
- Workflow (planning, debugging, review, branches): writing-plans, executing-plans, systematic-debugging, test-driven-development, verification-before-completion, requesting-code-review, receiving-code-review, finishing-a-development-branch, dispatching-parallel-agents, using-git-worktrees, subagent-driven-development
- Building plugins, hooks, agents, MCP servers: plugin-structure, plugin-settings, skill-development, command-development, agent-development, hook-development, mcp-integration, build-mcp-server, build-mcpb, build-mcp-app; CLAUDE.md upkeep: claude-md-improver
- 3D (Three.js): threejs-fundamentals, threejs-geometry, threejs-materials, threejs-lighting, threejs-textures, threejs-animation, threejs-interaction, threejs-loaders, threejs-shaders, threejs-postprocessing, threejs-performance, threejs-asset-pipeline, threejs-react-three-fiber
- MDCP own: mdcp-self-check (self-check, defense review, self-debug), mdcp-token-meter (session usage readout)
- Cloning an app's features, clean-room (public sources only, rebrand before launch): replica-recon, replica-architect, replica-design, replica-build, replica-backend, replica-test, replica-diff, replica-entrepreneur, replica-brand, replica-launch, replica-deploy

## Limits
These rules guide behavior; CI (build, typecheck, tests, scanners) enforces it.

---
name: better-t-stack-scaffolder
description: Scaffold a new TypeScript web, mobile, API, or full-stack project with Better-T-Stack, then harden it with the Pax Fullstack Harness. Use whenever the user wants a new TypeScript app scaffold, mentions Better-T-Stack, asks for a modern type-safe stack, or wants Codex to start a repo that is agent-ready from day one.
---

# Better-T-Stack Scaffolder

## Purpose

Create a new TypeScript project through Better-T-Stack, then install the v1 harness: short `AGENTS.md`, operational docs, stable scripts, quality gates, test strategy, runtime support, and entropy audit.

## Inspect First

- Read the user's product description and requested stack.
- Check the target directory for existing files before scaffolding.
- If using current Better-T-Stack behavior, prefer official docs: https://www.better-t-stack.dev/docs and https://www.better-t-stack.dev/docs/cli/agent-workflows.
- If the target is not TypeScript, stop and recommend `project-harness-bootstrap` instead.

## Stack Policy

Prefer the smallest stack that satisfies the product.

- Default serious web app: Bun, React with TanStack Router, Hono, tRPC or oRPC, PostgreSQL, Drizzle, Better Auth, Tailwind, Biome, Lefthook, Docker for local Postgres, GitHub Actions.
- Use Next.js when SEO, SSR, SSG, or hosting constraints justify it.
- Use Astro when content dominates and interactivity is isolated.
- Use React Native when the product is mobile-first.
- Use no frontend for API-only projects.
- Use REST when non-TypeScript clients or a public stable API are first-class.
- Use SQLite for prototypes, local-first apps, or embedded use.
- Use Prisma when team familiarity matters more than SQL-like schema control.

## Procedure

1. Lock the stack.
   - If the user provided choices, use them.
   - If choices are missing, infer a minimal stack and state assumptions before scaffolding when the tradeoff is high impact.
   - Record decisions in `docs/specs/000-initial-stack-decision.md`.

2. Generate the scaffold command.
   - Prefer Better-T-Stack's JSON-first agent workflow when available: inspect `create-better-t-stack schema --name create-json`, prepare a JSON payload, run dry-run first, then run `create-json`.
   - Do not combine `--yes` or JSON `yes: true` with explicit stack configuration flags; current Better-T-Stack rejects that combination.
   - Fall back to `bun create better-t-stack@latest`, `pnpm create better-t-stack@latest`, or `npm create better-t-stack@latest` when JSON creation is unavailable.
   - Do not manually assemble a Better-T-Stack-equivalent repo unless the CLI cannot support the required combination.
   - Known-good explicit full-stack baseline:
     `bun create better-t-stack@latest <app-name> --frontend tanstack-router --backend hono --runtime bun --database postgres --orm drizzle --api trpc --auth better-auth --payments none --addons biome lefthook --examples none --db-setup docker --web-deploy none --server-deploy none --no-git --package-manager bun --no-install`.

3. Scaffold the project.
   - Run from the chosen parent directory.
   - Avoid writing into a non-empty target unless the user explicitly requested it and you inspected contents.
   - Preserve the exact command or JSON payload, CLI version, dry-run result, fallback path, and scaffold warnings in the stack decision doc.

4. Inspect the generated repo.
   - Read `package.json`, workspace config, generated README, environment files, app directories, database/auth/API config, and generated scripts.
   - Remove generated examples only when the user asked for a clean scaffold or they conflict with the product.
   - Run install and non-mutating checks first. Use project-native autofix commands only when the user requested cleanup or when the scaffold generated files that fail its own formatter.

5. Install the harness layer by following these skills in order:
   - `project-harness-bootstrap`
   - `agents-md-author`
   - `repo-knowledge-base-builder`
   - `quality-gates-installer`
   - `testing-strategy-builder`
   - `architecture-boundary-enforcer`
   - `local-runtime-harness`
   - `entropy-auditor`
   - For production-bound projects, add `security-baseline`, `dependency-governance`, `observability-harness`, `ci-cd-harness`, `migration-and-schema-harness`, and `release-readiness-harness` after the baseline is healthy.
   - For frontend projects, optionally add `shadcn-ui-integrator` after inspecting generated UI setup.
   - For formal feature work, optionally add `openspec-sdd` before implementing the first feature.
   - For browser user workflows, optionally add `tdd-playwright-workflow` after baseline tests exist.
   - After harness docs, scripts, and state artifacts exist, optionally add `project-local-skill-generator` to create thin `.codex/skills` wrappers for this specific repo.

6. Validate.
   - Run install, lint, typecheck, test, build, then `./scripts/validate`.
   - Fix baseline failures introduced by the scaffold or harness.
   - Treat large bundle/chunk warnings as release-readiness or technical-debt notes unless they break an explicit size budget.
   - If a check cannot run, report the exact command, error, and likely cause.

## Files To Create Or Update

- `AGENTS.md`
- `docs/specs/000-initial-stack-decision.md`
- `docs/00-index.md`
- `docs/architecture/overview.md`
- `docs/architecture/boundaries.md`
- `docs/development/commands.md`
- `docs/development/environment.md`
- `docs/testing/strategy.md`
- `docs/quality/code-style.md`
- `scripts/validate` and stable command wrappers
- `.github/workflows/ci.yml`

## Validation

- Run the package manager install command.
- Run generated lint, typecheck, test, and build commands.
- Run `./scripts/validate` after the harness is installed.
- If using Better-T-Stack JSON automation, run the CLI dry-run before project creation when the current CLI supports it.
- If explicit stack options are used, verify the command does not also use `--yes`.
- Report exact command output for any blocker that prevents baseline validation.

## Completion Criteria

- The generated app boots locally or has a documented blocker.
- The selected stack, rejected alternatives, and scaffold command are recorded.
- Stable harness commands exist and are executable.
- `AGENTS.md` is short and points to docs instead of duplicating them.
- Project-local `.codex/skills` are generated only when backed by actual repo artifacts.
- Validation has been run or failure evidence is explicit.

## Failure Modes

- Unsupported CLI option: inspect the current schema/docs and regenerate the command.
- Existing target directory: inspect and preserve user files; do not overwrite blindly.
- Dependency install failure: capture package manager, version, command, and error.
- Better-T-Stack mismatch: document the actual generated shape before adding harness files.

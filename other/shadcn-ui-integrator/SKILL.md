---
name: shadcn-ui-integrator
description: Install, configure, and use shadcn/ui in React-style projects. Use when a repo needs shadcn/ui initialization, component installation, monorepo UI package setup, components.json review, registry or MCP guidance, or UI composition rules.
---

# shadcn/ui Integrator

## Purpose

Make shadcn/ui usable in the target repo without guessing framework, aliases, component ownership, or registry setup.

## Inspect First

- framework, package manager, `components.json`, Tailwind config, UI package, app directory, aliases, and existing components
- whether the project is a monorepo and where shared UI should live
- installed shadcn components and any private registries

## Procedure

1. Detect setup state.
   - If `components.json` exists, read it before adding components.
   - If shadcn is missing in a new supported app, choose the CLI runner from the repo package manager: Bun uses `bunx`, pnpm uses `pnpm dlx`, npm uses `npx`, and Yarn uses `yarn dlx`.
   - The official pattern is `<runner> shadcn@latest init -t <framework>`.
   - Supported templates include `next`, `vite`, `start`, `react-router`, and `astro`.
   - For existing projects, follow the framework-specific existing-project path rather than forcing a template.

2. Handle monorepos.
   - Prefer a shared UI package when one already exists, such as `packages/ui`.
   - Keep app-specific composition in the app and reusable primitives in the UI package.
   - Update aliases so imports match `components.json`.

3. Add components deliberately.
   - Use `<runner> shadcn@latest add <component>` or the repo's established command.
   - Add only components needed for the task.
   - Preserve local customizations in generated component files.
   - Icon-only controls must expose accessible names.
   - Use `$click-path-and-browser-qa` when component changes affect user workflows or browser acceptance paths.

4. Document usage.
   - Create or update `docs/development/ui.md` from `assets/templates/shadcn-ui-usage.md.tmpl`.
   - Update `docs/quality/golden-patterns.md` with preferred composition examples.
   - Mention shadcn MCP as guided setup only: Codex users manually add `[mcp_servers.shadcn] command = "npx"` and `args = ["shadcn@latest", "mcp"]` to `~/.codex/config.toml` when desired.
   - Use `project-local-skill-generator` to create `project-ui-workflow` when UI docs, component paths, and e2e commands are stable.

## Validation

- Run component install commands only after inspecting existing files.
- Run lint, typecheck, and relevant browser/UI tests.
- Confirm `components.json` paths and aliases match generated imports.
- Confirm UI controls are accessible by role/name where practical.

## Completion Criteria

- shadcn/ui is installed or the setup blocker is documented.
- Components live in the right package or app boundary.
- Usage docs explain component ownership, install commands, aliases, registry notes, and validation.

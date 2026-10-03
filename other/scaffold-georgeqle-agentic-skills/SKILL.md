---
name: scaffold
description: Generate a new package or app in the monorepo following established project conventions
type: execution
version: v0.3
argument-hint: <type> <name> (e.g. "package utils" or "app admin-dashboard")
---

# Scaffold

Generate a new package or app in the monorepo that follows the project's established conventions and patterns.

For product/app workflows, `/scaffold` is normally downstream of research, prototype consolidation, production specification, roadmap, and phase planning. Use it when `/roadmap` or `/plan-phase` identifies that the next implementation step needs a new app/package root. Do not route from `/idea-scope-brief`, `/bootstrap-repo`, `/customer-discovery`, `/competitive-analysis`, `/journey-map`, `/ux-variations`, or `/ui-interview` directly to `/scaffold` unless the user explicitly asks to create a minimal shell first.

## Process

1. **Parse the input** from `$ARGUMENTS`:
   - Extract the type (`package` or `app`) and the name.
   - If not provided or unclear, ask the user.

2. **Learn the project's conventions:**
   - Read `.agents/project.json` when present. If it is missing, run or recommend `scripts/pack.sh recommend` and include the likely project type in the scaffold plan.
   - If this scaffold creates a new project root, include `.agents/project.json` and install the matching local pack with `scripts/pack.sh install <pack>` from this source checkout, or `npx skillpacks install <pack>` from the new project shell when using the published package, after the root exists.
   - Read `CLAUDE.md` and `AGENTS.md` for project structure and conventions.
   - Read the monorepo config (`turbo.json`, `pnpm-workspace.yaml`, or equivalent).
   - Identify the directory pattern:
     - Where do packages live? (`packages/`, `libs/`, etc.)
     - Where do apps live? (`apps/`, `services/`, etc.)

3. **Find a reference to copy from:**
   - List existing packages/apps of the same type.
   - Read the most recently created one (by git log) as the template.
   - Identify the standard files:
     - `package.json` (scripts, dependencies, exports)
     - `tsconfig.json` (extends pattern)
     - Source structure (`src/`, `index.ts`, etc.)
     - Test setup (if present)
     - Any other config files (`.eslintrc`, `tailwind.config.*`, etc.)

4. **Enter plan mode:**
   - Enter plan mode using EnterPlanMode.
   - Present the scaffold plan:
     - Directory: where it will be created
     - Files to generate (with brief content description)
     - Dependencies to include
     - Reference package used as template
   - Wait for user approval.

5. **Generate the scaffold after approval:**
   - If Claude Code already returned to normal mode after approval, do not call ExitPlanMode again; continue directly with generation. Only use the plan-mode exit tool when the session is still visibly in plan mode.
   - Create the directory structure.
   - Generate each file, adapting the template:
     - Update `name` in `package.json` to match the new package name.
     - Update paths and references.
     - Create minimal placeholder source files (`src/index.ts` with a basic export).
     - Include the standard test setup if the project uses tests.
   - Run `pnpm install` (or equivalent) to link the new package.
   - Run type-checking to verify the scaffold compiles.

## Output

### Scaffolded
- **Type**: package/app
- **Name**: `@scope/name`
- **Location**: `packages/name/`

### Files Created
- `packages/name/package.json`
- `packages/name/tsconfig.json`
- `packages/name/src/index.ts`
- ...

### Next Steps
- What the user should do next (add dependencies, implement features, wire up routes, etc.)

## Next-Step Routing

- If the scaffold was created as part of an active roadmap/phase, recommend `/exec` to continue the current implementation step.
- If the user explicitly requested an early shell before research, keep the next route on the research-first product workflow: `/customer-discovery` when the concept is ready and business-discovery is enabled, otherwise `npx skillpacks install business-discovery` from the project shell.
- If the scaffold is for a non-product package with no pending roadmap item, recommend `/roadmap` or `/plan-phase` only when implementation sequencing is missing.

## Constraints
- Always use an existing package/app as the reference template — do not invent conventions.
- Do not install domain packs as base skills; use project-local pack skill roots.
- Always enter plan mode before creating files.
- Do not call ExitPlanMode from normal mode. If Claude Code reports "You are not in plan mode" after approval, treat approval as complete and continue implementation.
- Do not add unnecessary boilerplate — keep the scaffold minimal and consistent with existing packages.
- If the project does not appear to be a monorepo, inform the user and ask how to proceed.
- Do not install external dependencies beyond what the template uses.
- Do not treat scaffolding as product validation. It creates structure only; ICP, market, journey, UX, UI, and prototype decisions belong to their upstream skills.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

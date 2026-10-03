---
name: scaffold
description: Generate a new package or app in the monorepo following established project conventions
type: execution
version: v0.3
---

# Scaffold

Invoke as `$scaffold`.

Use this skill when the user wants to create a new package or app in their monorepo.

For product/app workflows, `$scaffold` is normally downstream of research, prototype consolidation, production specification, roadmap, and phase planning. Use it when `$roadmap`/`$plan-phase` identifies that the next implementation step needs a new app/package root. Do not route from `$idea-scope-brief`, `$bootstrap-repo`, `$customer-discovery`, `$competitive-analysis`, `$journey-map`, `$ux-variations`, or `$ui-interview` directly to `$scaffold` unless the user explicitly asks to create a minimal shell first.

## Process

1. Parse the type (package/app) and name from arguments.
2. Check `.agents/project.json`. If it is missing, run or recommend `scripts/pack.sh recommend` and include the likely project type in the scaffold plan.
3. If the scaffold creates a new project root, include `.agents/project.json` and install the matching local pack with `scripts/pack.sh install <pack>` from this source checkout, or `npx skillpacks install <pack>` from the new project shell when using the published package, after the root exists.
4. Learn conventions from CLAUDE.md, AGENTS.md, `.agents/project.json`, and monorepo config.
5. Find the most recently created package/app as a template.
6. Present the scaffold plan and wait for approval. Use `update_plan` to track the work; use `request_user_input` only if the session is already in Plan mode and a structured choice would help.
7. Generate files, adapting the template with the new name.
8. Run install and type-check to verify.

## Output

- **Scaffolded**: type, name, location
- **Files Created**: list of generated files
- **Next Steps**: what to do after scaffolding

## Next-Step Routing

- If the scaffold was created as part of an active roadmap/phase, recommend `$exec` to continue the current implementation step.
- If the user explicitly requested an early shell before research, keep the next route on the research-first product workflow: `$customer-discovery` when the concept is ready and business-discovery is enabled, otherwise `npx skillpacks install business-discovery` from the project shell.
- If the scaffold is for a non-product package with no pending roadmap item, recommend `$roadmap` or `$plan-phase` only when implementation sequencing is missing.

## Constraints

- Always use an existing package as the reference template.
- Do not install domain packs as base skills; use project-local pack skill roots.
- Present the plan and get approval before creating files. Do not assume a Claude-style `EnterPlanMode` or clear-context accept flow exists.
- Keep the scaffold minimal — no unnecessary boilerplate.
- Do not treat scaffolding as product validation. It creates structure only; ICP, market, journey, UX, UI, and prototype decisions belong to their upstream skills.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

---
name: ng-create-project
description: 'Scaffold an Angular 21+ app or workspace with strict TypeScript, Vitest and ESLint/Prettier. Use when starting a new Angular project.'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

Scaffold a new Angular 21+ project with a production-ready baseline. Paths to `scripts/` and `templates/` are relative to this skill's directory.

## Stack

- **`@angular/cli`** ≥ 21 (global or via `npx @angular/cli@latest`), Node 22 LTS
- **TypeScript** strict mode with Angular compiler options
- **Vitest** with jsdom (replaces Karma/Jest), on by default
- **ESLint + Prettier + Husky** via the `setup-prettier-eslint-husky` skill, on by default (Angular stays on Prettier, not Biome: no Angular template support, no SCSS)

## Steps

1. Ask: project name, selector prefix (default `app`), type **app** or **workspace**, whether to skip Vitest or ESLint
2. Run the scaffold script:

   ```powershell
   pwsh scripts/New-AngularProject.ps1 -ProjectName <Name> [-SelectorPrefix app] [-ProjectType app|workspace] [-SkipVitest] [-SkipEslint] [-OutputDirectory .]
   ```

   It runs `ng new --style scss --ssr false`, replaces `tsconfig.json` with the strict template, installs Vitest with the template config and patches the `test` scripts, then runs the code-quality setup.
3. Verify: `ng build`, `npm test`, `ng serve` (http://localhost:4200)
4. Next steps: components and signal stores via `ng-implementation` (`references/component.md`, `references/signal-store.md`)

## Templates

| File                         | Purpose                                                                                                        |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `templates/tsconfig.json`    | Strict Angular compiler options: `noImplicitOverride`, `strictTemplates`, `module: preserve`, `target: ES2022` |
| `templates/vitest.config.ts` | jsdom environment, globals, setup file, `include: ['**/*.spec.ts']`                                            |
| `templates/vitest.setup.ts`  | Empty setup file, extend as needed                                                                             |

## Constraints

- Standalone components only; `standalone: true` is the default, never add NgModules
- SCSS for styles; SSR off unless explicitly requested
- Angular 21+ only

Report: summary, project path, verify commands.

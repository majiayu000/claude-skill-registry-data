---
name: setup-prettier-eslint-husky
description: 'Set up ESLint, Prettier, Husky pre-commit with lint-staged and format-on-save for a TS or Angular project. Use when asked to add linting, formatting or pre-commit hooks.'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

Set up ESLint, Prettier and Husky for a TypeScript or Angular project. Paths to `scripts/` and `templates/` are relative to this skill's directory.

## Stack

- **ESLint** flat config (`eslint.config.mjs`), `@typescript-eslint`, plus `angular-eslint` for Angular
- **Prettier** with `prettier-plugin-organize-imports`
- **Husky** + **lint-staged** running `eslint --fix` and `prettier --write` on staged files

## Steps

1. Ask: project type (Angular / plain TS), selector prefix (Angular only), IDE (VS Code / WebStorm / both / none)
2. Run the setup script:

   ```powershell
   pwsh scripts/Setup-CodeQuality.ps1 -ProjectType <angular|ts> [-SelectorPrefix app] [-IDE vscode]
   ```

   It installs the packages with pnpm or npm (detected from the lockfile / `packageManager` field), copies the templates, initializes Husky, adds the `lint-staged` block to `package.json` and writes the IDE settings.
3. Verify: `npx eslint .` and `npx prettier --check .`

## Templates

| File                         | Purpose                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------ |
| `.prettierrc`                | Print width 100, single quotes, organize-imports plugin, Angular HTML override |
| `.prettierignore`            | Ignores `dist/`, `node_modules/`, `.angular/`, `coverage/`, `*.min.*`          |
| `.husky/pre-commit`          | Runs `npx lint-staged` on commit                                               |
| `angular/eslint.config.mjs`  | TypeScript + Angular ESLint + Prettier rules                                   |
| `plain-ts/eslint.config.mjs` | TypeScript + Prettier rules, no Angular deps                                   |

## Constraints

- Flat config only, never legacy `.eslintrc`
- Angular: `-SelectorPrefix` must match the project's component/directive prefix
- Do not overwrite existing configs without confirmation

Report: summary, files created or changed, verify commands.

---
name: setup-biome-husky
description: 'Set up Biome, Husky pre-commit with lint-staged and format-on-save for a plain TS or Node project. Use when asked to add linting, formatting or pre-commit hooks to a non-Angular project.'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

Set up Biome and Husky for a plain TypeScript or Node.js project. Paths to `scripts/` and `templates/` are relative to this skill's directory. Angular projects use `setup-prettier-eslint-husky` instead (Biome has no Angular template support and does not format SCSS).

## Stack

- **Biome** (`biome.json`): one tool for formatting and linting `*.ts`, `*.js`, `*.json`, `*.md`, `*.yml`, `*.yaml` (Markdown and YAML need Biome >= 2.6)
- **Husky** + **lint-staged** running `biome check --write` on staged files

## Steps

1. Ask: IDE (VS Code / WebStorm / both / none). If `angular.json` exists, stop and use `setup-prettier-eslint-husky`.
2. Run the setup script:

   ```powershell
   pwsh scripts/Setup-Biome.ps1 [-IDE vscode]
   ```

   It installs `@biomejs/biome`, `husky` and `lint-staged` with pnpm or npm (detected from the lockfile / `packageManager` field), copies `biome.json` unless one exists, initializes Husky, adds the `lint-staged` block and the `format`, `format:check` and `lint` scripts to `package.json`, and writes the IDE settings.
3. Format the project once: `npx biome check --write .`; put that commit into `.git-blame-ignore-revs`.
4. Verify: `npx biome check .`

## Templates

| File                                           | Purpose                                                                                                                                                                                  |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `biome.json.template` (copied as `biome.json`) | 2 spaces, line width 100, single quotes, semicolons, trailing commas `all`, recommended lint rules, git ignore file honoured, Markdown frontmatter parsed as YAML, prose kept as written |
| `.husky/pre-commit`                            | Runs `npx lint-staged` on commit                                                                                                                                                         |

## Constraints

- Never keep Prettier and Biome on the same files; two formatters fight
- An existing `biome.json` is kept, not overwritten
- `detect-techstack` reports `biome` once `biome.json[c]` exists; `implementation` then formats with `biome check --write`

---
name: setup-pre-commit
description: Set up repository-local Husky pre-commit hooks with lint-staged, Prettier, and optional typecheck/test gates. Use when a user asks to add pre-commit hooks, configure lint-staged, enforce staged formatting, or add commit-time checks.
---

# setup-pre-commit

Guides a safe, repo-aware pre-commit setup. This skill is guidance-first: inspect the target repository, explain the planned changes, and only mutate dependency, hook, package, lint-staged, or Prettier files after the user approves that setup.

## What this configures

- Husky v9+ with a `.husky/pre-commit` hook
- lint-staged running Prettier on staged files
- Prettier defaults only when no Prettier config exists
- Optional `typecheck` and `test` commands only when the target `package.json` already defines those scripts
- Verification commands and a real commit smoke test when the user is ready to commit setup changes

## 1. Preflight the target repo

Work from the target repo root, then inspect existing package and config state before proposing commands:

```bash
git status --short
node -e "const fs=require('fs'); const p=JSON.parse(fs.readFileSync('package.json','utf8')); process.stdout.write(JSON.stringify({packageManager:p.packageManager||null,scripts:p.scripts||{}}, null, 2)+'\n');"
node -e "const fs=require('fs'); const files=['bun.lock','bun.lockb','pnpm-lock.yaml','yarn.lock','package-lock.json','.lintstagedrc','.lintstagedrc.json','.lintstagedrc.js','lint-staged.config.js','.prettierrc','.prettierrc.json','.prettierrc.js','prettier.config.js','prettier.config.cjs','prettier.config.mjs']; process.stdout.write(files.filter((f)=>fs.existsSync(f)).join('\n')+'\n');"
```

Stop and ask before editing if the repo has unrelated dirty changes, multiple package managers, or an existing hook/config whose intent is unclear.

## 2. Detect the package manager

Prefer the `packageManager` field in `package.json`, then lockfiles:

| Signal | Package manager |
|--------|-----------------|
| `packageManager` starts with `bun` or `bun.lock` / `bun.lockb` exists | Bun |
| `packageManager` starts with `pnpm` or `pnpm-lock.yaml` exists | pnpm |
| `packageManager` starts with `yarn` or `yarn.lock` exists | Yarn |
| `packageManager` starts with `npm` or `package-lock.json` exists | npm |

If there is no clear signal, default to npm only after telling the user that no lockfile or package-manager pin was found.

## 3. Install dev dependencies

Use exactly one command for the detected package manager:

| Package manager | Command |
|-----------------|---------|
| Bun | `bun add --dev husky lint-staged prettier` |
| pnpm | `pnpm add --save-dev husky lint-staged prettier` |
| Yarn | `yarn add --dev husky lint-staged prettier --non-interactive` |
| npm | `npm install --save-dev husky lint-staged prettier --yes` |

Do not run these commands while porting this skill. Run them only when applying the skill to a target repo with user approval.

## 4. Initialize Husky

After dependencies are installed, initialize Husky with the detected package manager:

| Package manager | Command |
|-----------------|---------|
| Bun | `bunx --bun husky init` |
| pnpm | `pnpm exec husky init` |
| Yarn | `yarn exec husky init` |
| npm | `npx --yes husky init` |

Husky v9+ creates `.husky/pre-commit` and usually adds `prepare: "husky"` to `package.json`. Preserve an existing `prepare` script by combining commands only if the user approves the exact package script change.

## 5. Compose `.husky/pre-commit`

The hook must run lint-staged first, then only the package scripts that already exist. Do not add failing placeholder lines for missing scripts.

| Package manager | lint-staged line | Existing `typecheck` script | Existing `test` script |
|-----------------|------------------|-----------------------------|------------------------|
| Bun | `bunx --bun lint-staged` | `bun run typecheck` | `bun run test` |
| pnpm | `pnpm exec lint-staged` | `pnpm run typecheck` | `pnpm run test` |
| Yarn | `yarn exec lint-staged` | `yarn run typecheck` | `yarn run test` |
| npm | `npx --no-install lint-staged` | `npm run typecheck` | `npm run test` |

Example for a Bun repo that has both scripts:

```bash
bunx --bun lint-staged
bun run typecheck
bun run test
```

If the repo lacks `typecheck` or `test`, omit that line and tell the user which check was skipped.

## 6. Configure lint-staged and Prettier

Respect existing config:

1. If a lint-staged config already exists, update it only after confirming it should run Prettier on staged files.
2. If no lint-staged config exists, add one config location that matches repo style. Prefer an existing `package.json` config style if the repo already keeps tool config there; otherwise use `.lintstagedrc.json`.
3. Use this minimal lint-staged config:

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

4. If any Prettier config exists, do not overwrite it.
5. If no Prettier config exists, propose these defaults:

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

`prettier --ignore-unknown` lets staged binary or unsupported files pass without parse failures.

## 7. Verify

Run only commands that match the detected package manager and existing scripts:

```bash
git status --short
```

- Confirm `.husky/pre-commit` exists and contains the selected lint-staged line.
- Confirm `package.json` has a valid Husky `prepare` script without clobbering previous behavior.
- Confirm lint-staged config exists and Prettier config is preserved or created intentionally.
- Run the selected lint-staged command with staged setup files.
- Run the selected typecheck/test commands only if those scripts exist.

## 8. Smoke test with a real commit

When the user is ready to commit the setup, use the normal commit as the smoke test:

```bash
git add package.json .husky/pre-commit .lintstagedrc.json .prettierrc
git commit -m "chore: add pre-commit checks"
```

Adjust the `git add` paths to the files actually changed. Do not create an empty or throwaway commit just to test the hook, and do not run a commit smoke test unless the user explicitly wants the setup committed.

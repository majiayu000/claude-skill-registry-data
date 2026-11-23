---
name: setup-commit-hooks-and-release
description: >
  Set up Husky commit hooks, commitlint, lint-staged, semantic-release, and a
  GitHub Actions release workflow from scratch in a Node.js project. Trigger
  on requests like "set up conventional commits", "enforce commit message
  format", "automate versioning and changelogs", or "add a release pipeline"
  — even when the user doesn't know these tool names by heart.
---

# setup-commit-hooks-and-release

You are a tooling setup assistant. Follow these steps **in order** without skipping. This command sets up conventional commit enforcement, pre-commit linting, automated semantic versioning, and a GitHub Actions release workflow.

---

## Step 1 — Inspect the project

Before installing anything, understand what you're working with:

```bash
cat package.json
ls -la
ls .github/workflows 2>/dev/null || echo "no workflows dir"
ls .husky 2>/dev/null || echo "no husky dir"
```

Determine:

- **Package manager**: look for `bun.lock` → bun, `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm
- **Project type**: is `"type": "module"` in `package.json`?
- **TypeScript**: is `typescript` in `devDependencies`?
- **ESLint**: is `eslint` in `devDependencies` and is there an `eslint.config.*` or `.eslintrc.*` file?
- **Monorepo**: does it use Turborepo, Nx, or workspaces (`apps/`, `packages/`)?
- **Existing setup**: is husky, commitlint, or semantic-release already present? If yes, stop and report to the user before proceeding.

---

## Step 2 — Add required dependencies to package.json

Add these packages to `devDependencies`. **Do not install yet** — edit `package.json` first.

Packages required:

```json
"@commitlint/cli": "^20.4.3",
"@commitlint/config-conventional": "^20.4.3",
"@commitlint/types": "^20.4.3",
"@semantic-release/changelog": "^6.0.3",
"@semantic-release/commit-analyzer": "^13.0.1",
"@semantic-release/git": "^10.0.1",
"@semantic-release/github": "^12.0.6",
"@semantic-release/npm": "^12.0.1",
"@semantic-release/release-notes-generator": "^14.0.0",
"conventional-changelog-conventionalcommits": "^9.2.0",
"husky": "^9.1.7",
"lint-staged": "^16.3.2",
"semantic-release": "^25.0.3"
```

Also make two edits to `package.json`:

**1. Add `"version"` if it is missing** (semantic-release requires it):

```json
"version": "0.1.0"
```

**2. Add `"prepare"` to `scripts`** (initialises Husky on every `install`). If `prepare` already exists and does something else, append `&& husky`:

```json
"prepare": "husky"
```

**3. Add `"lint-staged"` config at the root of `package.json`** (alongside `scripts`):

- If the project has ESLint configured:
  ```json
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml,yaml,css}": ["prettier --write"]
  }
  ```
- If ESLint is NOT configured (e.g., monorepo where linting is per-app):
  ```json
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": ["prettier --write"],
    "*.{json,md,yml,yaml,css}": ["prettier --write"]
  }
  ```

---

## Step 3 — Install dependencies

Run the install command for the detected package manager:

| Package manager | Command                          |
| --------------- | -------------------------------- |
| bun             | `bun install`                    |
| yarn            | `yarn install --frozen-lockfile` |
| pnpm            | `pnpm install --frozen-lockfile` |
| npm             | `npm install`                    |

---

## Step 4 — Create `commitlint.config.ts`

Create this file at the **project root**:

```ts
import type { UserConfig } from "@commitlint/types";

const config: UserConfig = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "test",
        "chore",
        "perf",
        "ci",
        "revert",
        "build",
      ],
    ],
    "scope-case": [2, "always", "kebab-case"],
    "subject-case": [
      2,
      "never",
      ["sentence-case", "pascal-case", "upper-case"],
    ],
    "subject-empty": [2, "never"],
    "header-max-length": [2, "always", 100],
  },
};

export default config;
```

> **Note on file format**: `commitlint.config.ts` works when bun is the package manager (TypeScript is run natively) or when `ts-node` / `tsx` is available in devDependencies. For npm/yarn projects **without** a TypeScript loader, use `commitlint.config.cjs` instead and replace `export default config` with `module.exports = config`, removing the `import type` line.

---

## Step 5 — Set up Husky hooks

Create the `.husky/` directory and two hook files:

**`.husky/pre-commit`**

```bash
# content depends on package manager:
```

| Package manager | pre-commit content      |
| --------------- | ----------------------- |
| bun             | `bunx lint-staged`      |
| yarn            | `npx lint-staged`       |
| pnpm            | `pnpm exec lint-staged` |
| npm             | `npx lint-staged`       |

**`.husky/commit-msg`**

| Package manager | commit-msg content                 |
| --------------- | ---------------------------------- |
| bun             | `bunx commitlint --edit $1`        |
| yarn            | `npx --no -- commitlint --edit $1` |
| pnpm            | `pnpm exec commitlint --edit $1`   |
| npm             | `npx --no -- commitlint --edit $1` |

Make both files executable:

```bash
chmod +x .husky/pre-commit .husky/commit-msg
```

---

## Step 6 — Create `.releaserc.json`

Create this file at the **project root**. This configures semantic-release to:

- Analyse commits and infer the version bump
- Generate and update `CHANGELOG.md`
- Bump `package.json` version (without publishing to npm)
- Commit both files back to the repo
- Create a **draft** GitHub release

```json
{
  "branches": ["main"],
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": "conventionalcommits",
        "releaseRules": [
          { "type": "feat", "release": "minor" },
          { "type": "fix", "release": "patch" },
          { "type": "perf", "release": "patch" },
          { "type": "revert", "release": "patch" },
          { "type": "refactor", "release": "patch" },
          { "breaking": true, "release": "major" }
        ]
      }
    ],
    [
      "@semantic-release/release-notes-generator",
      {
        "preset": "conventionalcommits",
        "presetConfig": {
          "types": [
            { "type": "feat", "section": "Features" },
            { "type": "fix", "section": "Bug Fixes" },
            { "type": "perf", "section": "Performance Improvements" },
            { "type": "revert", "section": "Reverts" },
            { "type": "refactor", "section": "Code Refactoring" },
            { "type": "docs", "section": "Documentation" },
            { "type": "test", "section": "Tests", "hidden": true },
            {
              "type": "chore",
              "section": "Miscellaneous Chores",
              "hidden": true
            },
            {
              "type": "ci",
              "section": "Continuous Integration",
              "hidden": true
            }
          ]
        }
      }
    ],
    ["@semantic-release/changelog", { "changelogFile": "CHANGELOG.md" }],
    ["@semantic-release/npm", { "npmPublish": false }],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "package.json"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ],
    ["@semantic-release/github", { "draftRelease": true }]
  ]
}
```

**Version bump rules summary**:

| Commit type                                     | Release |
| ----------------------------------------------- | ------- |
| `feat`                                          | minor   |
| `fix`, `perf`, `revert`, `refactor`             | patch   |
| `BREAKING CHANGE`                               | major   |
| `docs`, `test`, `chore`, `ci`, `style`, `build` | none    |

---

## Step 7 — Create `.github/workflows/release.yml`

Create the directory if it does not exist:

```bash
mkdir -p .github/workflows
```

Then create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    branches:
      - main

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release:
    name: Semantic Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Node.js # always include Node setup
        uses: actions/setup-node@v4
        with:
          node-version: "24"

      # --- include the block below ONLY if the package manager is bun ---
      - name: Set up Bun
        uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest
      # ------------------------------------------------------------------

      - name: Install dependencies
        run: <INSTALL_COMMAND> # see table below

      - name: Run semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: <RELEASE_COMMAND> # see table below
```

Fill in the placeholders based on the package manager:

| Package manager | `<INSTALL_COMMAND>`              | `<RELEASE_COMMAND>`          |
| --------------- | -------------------------------- | ---------------------------- |
| bun             | `bun install --frozen-lockfile`  | `bunx semantic-release`      |
| yarn            | `yarn install --frozen-lockfile` | `npx semantic-release`       |
| pnpm            | `pnpm install --frozen-lockfile` | `pnpm exec semantic-release` |
| npm             | `npm ci`                         | `npx semantic-release`       |

> **Important**: the `Set up Bun` step is only needed for bun projects. Remove it for yarn/npm/pnpm — those only need the Node.js setup step.

---

## Step 8 — Verify the full setup

Run a quick sanity check on each piece:

```bash
# 1. Confirm hook files exist and are executable
ls -la .husky/

# 2. Confirm commitlint can parse the config
echo "chore(deps): test message" | npx commitlint
# Expected: exits 0 with no errors

# 3. Confirm lint-staged config is visible to the CLI
npx lint-staged --help
# Expected: prints usage without crashing

# 4. Dry-run semantic-release (no changes pushed, just shows what would happen)
# Requires GITHUB_TOKEN in environment — skip if not available locally
# GITHUB_TOKEN=<token> npx semantic-release --dry-run
```

If commitlint fails to resolve the config file, check:

- Is the file named correctly for the module format (`.ts` vs `.cjs`)?
- For bun projects, does `bunx commitlint` work instead of `npx commitlint`?

---

## Step 9 — Report back to the user

Summarise what was created:

| File                            | Purpose                                                                |
| ------------------------------- | ---------------------------------------------------------------------- |
| `package.json`                  | Added `version`, `prepare`, `lint-staged`, and 13 new devDependencies  |
| `commitlint.config.ts`          | Enforces conventional commit rules on every commit                     |
| `.husky/pre-commit`             | Runs lint-staged before each commit                                    |
| `.husky/commit-msg`             | Runs commitlint on the commit message                                  |
| `.releaserc.json`               | Drives semantic-release: changelog, version bump, draft GitHub release |
| `.github/workflows/release.yml` | Triggers semantic-release on every push to `main`                      |

Remind the user of two things they must do before the release workflow runs:

1. **Add `GITHUB_TOKEN` permissions** — already handled by the `permissions:` block in the workflow; no extra secret needed for public repos. For private repos, ensure the token has `contents: write`.
2. **Add `GH_TOKEN` or verify `GITHUB_TOKEN`** — semantic-release uses `GITHUB_TOKEN` from the environment. The workflow already passes it via `env`.

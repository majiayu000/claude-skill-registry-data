---
name: scaffold-node-ts
description: Scaffold a new plain runnable Node.js TypeScript application in an already-created directory. Use for new non-framework Node/TypeScript applications; do not use for libraries/packages, React or Vite apps, monorepos/workspaces, or existing configured Node projects.
---

# Scaffold Node TypeScript

Create a minimal runnable application using the canonical files in `assets/`
and `scripts/scaffold.mjs`. The agent handles eligibility, environment selection,
dependency compatibility, and failures. The script owns baseline file contents.
Do not independently recreate or customise the baseline.

## 1. Inspect and prepare

- Work in the requested existing directory, or the current directory if unspecified.
- Inspect before writing. Preserve unrelated files. Stop if `package.json` or
  substantial Node/TypeScript configuration already exists.
- Require installed nvm and pnpm. Load the existing nvm shell function if necessary.
  Do not install tools, replace system package managers, or run `pnpm self-update`.
- Use nvm to select the newest locally installed Node LTS. Inspect installed
  versions and confirm the selected runtime has a truthy `process.release.lts`.
  Do not install or download Node. If no installed LTS exists, stop.
- Run every Node, pnpm, and generator command with that selection active. Record
  `node --version` and `pnpm --version`. The baseline supports Node majors 20, 22,
  and 24, and pnpm 10 or newer. Stop on unsupported versions; do not improvise
  another baseline or upgrade automatically.
- If Git is available, detect whether the directory is already inside a repository.
  Reuse it without changing parent configuration. Otherwise run `git init`.
  If detection or initialization is blocked, stop before generating files.
  Never create a nested repository, commit, push, merge, rebase, or create remotes.
  If Git is unavailable, continue and report it as unavailable.

## 2. Resolve dependencies

Use the installed pnpm exclusively. Resolve exact stable versions for:

`typescript`, `tsx`, `@types/node`, `eslint`, `@eslint/js`, `typescript-eslint`,
`globals`, `prettier`, `eslint-config-prettier`, and `vitest`.

- Select `@types/node` from the selected Node major.
- Select the latest stable releases compatible with the selected runtime and
  each other's peer requirements. Inspect package metadata using `pnpm view`.
  If latest releases conflict, keep the latest stable typescript-eslint and
  select the newest TypeScript and ESLint releases satisfying its peer ranges;
  reconcile other constraints as needed. Report any compatibility fallback.
- Do not add runtime dependencies, extra tooling, or prereleases.
- Write an input JSON file outside the project, in a temporary directory:

```json
{
  "node": "24.22.0",
  "pnpm": "11.21.0",
  "dependencies": {
    "@eslint/js": "10.0.1",
    "@types/node": "24.19.2",
    "eslint": "10.12.0",
    "eslint-config-prettier": "10.1.8",
    "globals": "17.13.0",
    "prettier": "3.9.10",
    "tsx": "4.23.15",
    "typescript": "6.0.3",
    "typescript-eslint": "8.71.2",
    "vitest": "5.0.4"
  }
}
```

These versions illustrate the input shape; resolve versions for the actual
installation rather than treating the example as a version catalog.

## 3. Generate and install

Resolve the script path relative to this skill's directory, then run:

```text
node <skill-directory>/scripts/scaffold.mjs create <project-directory> <inputs.json>
```

The script derives the package name from the directory, writes exact dependency
versions and Node/pnpm metadata, and creates canonical source, test, TypeScript,
ESLint, Prettier, ignore, and VS Code debugging files. It checks all destination
paths before writing and refuses existing files and symlink destinations.
If it refuses a collision, preserve the existing content and report the blocker;
never delete files or bypass the script to force generation. If a write fails
partway through, report the partial output rather than rerunning over it.

The compiler targets are ES2023 for Node 20/22 and ES2024 for Node 24. Changes to
supported majors or baseline choices belong in the skill resources.

The script also creates `pnpm-workspace.yaml` solely to approve esbuild's required
installation script, using the selected pnpm version's setting. This file is
allowed for a single application; do not add workspace packages, blanket build
approval, or other pnpm policy changes. If another dependency requires approval,
stop and report it for review.

Run `pnpm install` and retain `pnpm-lock.yaml`. If the default store is unwritable,
use an explicit writable temporary store with pnpm's supported configuration and
keep that configuration active during all remaining checks. On pnpm 11, use
`pnpm --config.store-dir=<path> <command>` for installation and subsequent
script commands; confirm the location with `pnpm --config.store-dir=<path> store path`. The
`npm_config_store_dir` variable is not effective there, and `--store-dir` is not
a `pnpm run` option. Verify the setting using the installed pnpm before relying
on a fallback for another major. Do not disable
installation or dependency verification. Report any temporary store used.
Verify the installed dependency graph satisfies peer requirements using the
installed pnpm version's supported command.

## 4. Verify and report

Run each command and check its own exit status; stop on an unresolved failure:

1. `pnpm format`
2. `node <skill-directory>/scripts/scaffold.mjs verify <project-directory> <inputs.json>`
3. `pnpm check`
4. `pnpm build`
5. `pnpm dev`
6. `pnpm start`

Confirm that dev and start print the canonical confirmation message and exit
successfully, and that `dist/index.js` and `dist/index.js.map` exist. Inspect
`git status --short` when Git is available. Fix dependency selection problems
within the stated constraints; do not alter canonical files to make checks pass.
If resolved dependency versions must change after generation, stop and report
that the scaffold is incomplete; do not bypass the generator's preservation rule.

Completion requires the canonical baseline verification, dependency compatibility,
and all required checks to pass. Report the selected Node and pnpm versions,
derived name, Git outcome, compatibility fallbacks, and verification result.
Distinguish passed, failed, blocked before execution, and not attempted.
Do not describe an unexecuted operation as having failed.

## Boundaries

Do not create project guidance, README documentation, licenses, specifications,
ADRs, CI/CD, Docker, environment files, Git hooks, publishing configuration,
library exports, frameworks, databases, editor settings or recommendations,
additional skills, or a `check.sh` wrapper. Do not configure a monorepo.
`pnpm check` remains the canonical project quality command.

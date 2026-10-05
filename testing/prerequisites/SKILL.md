---
name: prerequisites
description: Environment prerequisites for ESM/gradle Hub module development. Use when starting new work or validating environment setup.
---

# Prerequisites

The repo is a **gradle multi-project** of ESM TypeScript modules built and tested through `zbb` (which drives gradle under the hood). There is no Lerna, no Nx, no `npm run build`. The toolchain below is the minimum to run `/create-module`, `/add-operation`, `/fix-issue`, `/validate-gates`, or any module-level `zbb` task.

## Required tools

| Tool                 | Version           | Check                  | Notes                                                                 |
|----------------------|-------------------|------------------------|-----------------------------------------------------------------------|
| Node.js              | v22.21.0 exact    | `node -v`              | Pinned via `.nvmrc` and `gradle.properties` (`nodeVersion=22.21.0`). Use nvm. |
| npm                  | ≥ 10              | `npm -v`               | Ships with Node 22.                                                   |
| Git                  | ≥ 2.25            | `git --version`        | `user.email` is consumed as the module's author.                      |
| Docker Desktop       | running           | `docker info`          | Required for gradle's `buildImage` and `zbb testDocker`.              |
| Gradle wrapper       | present at root   | `test -x ./gradlew`    | zbb drives the wrapper for you; you should never need to invoke it directly. |
| Java (for the wrapper) | 17 LTS+         | `java -version`        | Gradle wrapper needs a JVM; Adoptium Temurin 17 works.                |
| Yeoman               | ≥ 5               | `yo --version`         | Only for new module creation. `npm i -g yo`.                          |
| `@zerobias-org/generator-module` | 0.25.2 | `npm ls -g @zerobias-org/generator-module` | `npm i -g @zerobias-org/generator-module@0.25.2`. Invoked as `yo @zerobias-org/module`. |
| zbb                  | latest            | `zbb --version`        | `npm i -g @zerobias-org/zbb`. Owns `test`, `testDirect`, `testDocker`, `testHub`, `gate`, `secret`, slots, env. |
| jq                   | any               | `jq --version`         | JSON in scripts/agent checks.                                         |
| yq                   | v4.x              | `yq --version`         | YAML in scripts/agent checks.                                         |

## Optional (only needed when running e2e against the Hub stack)

| Tool                                   | Install                                              | Used by                |
|----------------------------------------|------------------------------------------------------|------------------------|
| `@zerobias-com/hub-node`              | `npm i -g @zerobias-com/hub-node`                    | `zbb testHub`          |
| `@zerobias-com/platform-dataloader`   | `npm i -g @zerobias-com/platform-dataloader`         | `zbb testHub`          |

`zbb testHub` is currently blocked by upstream bugs — skip it until announced otherwise. `zbb test`, `zbb testDirect`, and `zbb testDocker` are the supported modes.

## Repository layout (what each command assumes)

```
~/zerobias/org/module/                  # repo root (github.com/zerobias-org/module)
├── gradlew                             # wrapper — zbb drives this; you should not invoke it directly
├── settings.gradle.kts                 # auto-discovers package/**/build.gradle.kts markers
├── build.gradle.kts                    # root (zb.workspace)
├── gradle.properties                   # shared properties (node, npm registry, etc.)
├── .nvmrc                              # v22.21.0
├── .npmrc                              # auth/registry config
├── package/                            # one subdir per (vendor)/(suite?)/(service)
│   └── <vendor>/[<suite>/]<service>/
│       ├── build.gradle.kts            # marker that this is a gradle subproject
│       ├── package.json                # ESM, only `clean` script
│       ├── api.yml
│       ├── connectionProfile.yml       # connector modules only
│       ├── hub-sdk/                    # generated typed client (gradle owns dist/)
│       ├── src/
│       ├── test/unit/
│       ├── test/e2e/                   # describeModule<T> tests
│       ├── dist/                       # build output (gitignored)
│       ├── generated/                  # codegen output (gitignored)
│       └── gate-stamp.json             # written by `zbb gate`, COMMITTED
└── .claude/                            # workflow & agent definitions
```

There is **no** `node_modules` workspace at the root; each module is independent (no npm workspaces / lerna).

## Environment setup

### Node via nvm

```bash
nvm install 22.21.0
nvm use
```

The repo's `.nvmrc` and `gradle.properties` both pin Node v22.21.0 — same patch version in both places, so the developer's shell Node and gradle's bundled Node behave identically.

### npm registry / auth

The repo's `.npmrc` configures the GitHub Packages registry. Authenticate once:

```bash
npm login --scope=@zerobias-org --registry=https://npm.pkg.github.com
npm login --scope=@zerobias-com --registry=https://npm.pkg.github.com
```

(Use a GitHub PAT with `read:packages` — `write:packages` only for publish.)

The root `package.json.name` is `@zerobias-org/module`. The generator and gradle tooling only check that the name ends with `/module`. Module packages live under `@zerobias-org/*`; utility/interface packages live under `@zerobias-com/*`.

### git identity

```bash
git config user.email "ctamas@zerobias.com"   # work projects under ~/zerobias
git config user.name  "Catalin Tamas"
```

The module-scaffolder agent reads `git config user.email` and writes it into the module's `package.json.author`.

### Docker

Start Docker Desktop. Verify:

```bash
docker info >/dev/null && echo OK
```

Required for: gradle `buildImage`, `zbb testDocker`, `zbb gate`, and the generator's auto-build step.

## Verification script

Drop this into `~/bin/zb-module-prereqs.sh` and run it before starting:

```bash
#!/usr/bin/env bash
set -u
fail=0
check() { command -v "$1" >/dev/null && echo "✓ $1" || { echo "✗ $1 missing"; fail=1; }; }

# Versions
node -v | grep -q '^v22\.21\.' && echo "✓ node $(node -v)" || { echo "✗ node $(node -v) — need v22.21.x"; fail=1; }
npm -v | awk -F. '$1>=10{exit 0}{exit 1}' && echo "✓ npm $(npm -v)" || { echo "✗ npm $(npm -v) — need >=10"; fail=1; }

# CLIs
check git
check docker
check yo
check zbb
check jq
check yq
check java

# Docker running
docker info >/dev/null 2>&1 && echo "✓ docker running" || { echo "✗ docker not running"; fail=1; }

# Generator
npm ls -g @zerobias-org/generator-module >/dev/null 2>&1 \
  && echo "✓ @zerobias-org/generator-module installed" \
  || { echo "✗ install: npm i -g @zerobias-org/generator-module@0.25.2"; fail=1; }

# Repo root
if [ -f ./gradlew ] && jq -r .name < ./package.json 2>/dev/null | grep -q '/module$'; then
  echo "✓ at repo root"
else
  echo "✗ not at repo root (cd ~/zerobias/org/module)"; fail=1
fi

exit $fail
```

## Validation checklist

Before invoking `/create-module`:

- [ ] `node -v` reports `v22.21.x`
- [ ] `docker info` is happy
- [ ] CWD is `~/zerobias/org/module` (or equivalent — `package.json.name` ends with `/module`)
- [ ] `yo --version` runs and `npm ls -g @zerobias-org/generator-module` resolves
- [ ] `zbb --version` runs
- [ ] `git config user.email` returns the expected work email
- [ ] You're on a feature branch (not `main`)

## CI/CD assumptions

CI does **not** run tests. It validates `gate-stamp.json` produced locally by `zbb gate`. So CI prerequisites are minimal: Node 22.21.x and ability to read `gate-stamp.json`.

## Related

- @.claude/skills/tool-requirements/SKILL.md — command reference for the tools above
- @.claude/skills/scaffolding/SKILL.md — what the generator does once prerequisites are met

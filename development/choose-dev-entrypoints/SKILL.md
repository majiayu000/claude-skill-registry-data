---
name: choose-dev-entrypoints
description: Choose the right dev-environment entrypoint and responsibility boundary across Nix, Just, Bun, Turborepo, package scripts, shellHook, and ./scripts. Triggers when the user asks which command should run dev/build/test/install/codegen, whether to put work in nix develop or shellHook, how to split responsibilities between just, bun, turbo, and scripts, or how to make dev environments lazy, cacheable, and understandable. Do NOT trigger for ordinary implementation work or Nix flake layout refactors. In a TypeScript-only repo, ops scripts are TypeScript (ADR-0012), not bash.
---

# Choose dev entrypoints

Use this skill to assign development-environment responsibilities to the layer that naturally owns them. The goal is not to pick one universal command runner. The goal is to keep each layer small, local, cacheable where possible, and unsurprising for humans entering the repo.

## Core model

Prefer declarations by the consumer of a capability over eager setup by an earlier layer.

```text
nix develop
  provides tools and native capabilities

package manager and package scripts
  own package-local runtime commands

task graph runner
  owns cross-package dependencies, inputs, outputs, and caching

just or similar command runner
  owns human-friendly aliases and repo chores

scripts/
  owns imperative glue (TypeScript in TS-only repos; see ADR-0012)
```

The useful question is "who consumes the result?" rather than "which tool is capable of running it?"

## When to use

- The user asks whether `nix develop`, `shellHook`, `just`, `bun run`, `turbo run`, or `./scripts/*` should own a workflow.
- The user is designing a dev entrypoint such as `dev`, `build`, `test`, `codegen`, `install`, `fmt`, or `watch`.
- A shell hook is doing too much work on environment entry.
- A repo has several ways to start a dev server and the user wants a principled split.
- The user wants lazy setup, cacheable generated outputs, or dependency-aware dev commands.
- The user is deciding where `bun install`, code generation, local service startup, or package graph orchestration belongs.

## When NOT to use

- The task is specifically reorganizing Nix flake outputs or module layout. Use `nix-flake-organization`.
- The task is only writing or debugging an existing script, with no responsibility-boundary question. In a TypeScript-only repo, new ops scripts are TypeScript ([ADR-0012](../../docs/adr/0012-ops-scripts-in-typescript.md)), not bash.
- The task is only adding one package script in an already-established repo convention.
- The user asks for current docs or exact CLI syntax. Fetch the relevant docs first, then apply this skill if the ownership decision remains.

## Decision workflow

1. Inventory existing entrypoints before proposing a new one: `flake.nix`, `.envrc`, `justfile`, `package.json`, `turbo.json`, `scripts/`, and app/package-local manifests.
2. Identify the artifact or capability being produced: tools on `PATH`, installed JS dependencies, generated source, build artifacts, a long-running dev server, local services, formatting, or validation.
3. Assign ownership to the lowest layer that can express the dependency truthfully.
4. Keep the outer entrypoint as a thin delegate when ergonomics matter.
5. Validate the resulting path by asking: "Can someone enter the environment without paying for work they do not need?" and "Will the command that needs the thing declare that it needs it?"

## Responsibility map

| Layer | Owns | Avoid |
| --- | --- | --- |
| `nix develop` | System tools, native libraries, pinned CLIs, language runtimes, environment variables that are true for every workflow | Running app-specific setup, installing JS dependencies, starting dev servers, guessing future command needs |
| Nix `shellHook` | Lightweight shell initialization, short messages, env normalization, optional checks that are cheap and idempotent | Expensive installs, codegen, builds, long-running services, work that only some commands need |
| `.envrc` / direnv | Entering the Nix shell automatically, watching files that should reload the shell, local PATH additions | Replacing the task graph or running heavy setup on every directory entry |
| `bun install` | Materializing JS dependency state from `package.json` and `bun.lock` | Being hidden in shell entry when many shell users do not need JS deps |
| `bun run <script>` | Package-local commands and scripts that belong to one package or root JS workspace | Cross-package orchestration that needs graph dependencies and caching |
| `turbo run <task>` | Monorepo task graph, task dependencies, cacheable inputs and outputs, workspace-wide `build`, `test`, `lint`, `dev` orchestration | Arbitrary shell initialization, secrets loading, one-off imperative logic better expressed as a script |
| `just <recipe>` | Human-friendly command aliases, repo chores, composition across ecosystems, discoverable shortcuts | Owning hidden build semantics that package scripts or Turbo need to cache |
| `scripts/*` | Complex imperative glue, traps, port cleanup, service readiness checks, multi-step procedures awkward in JSON. In a TypeScript-only repo this is TypeScript (`scripts/*.ts`), not bash ([ADR-0012](../../docs/adr/0012-ops-scripts-in-typescript.md)) | Becoming a second untracked task graph; new `.sh` files in a TS-only repo |

## Common patterns

### Fast shell entry

Keep `nix develop` fast. It should provide `bun`, `node`, `turbo`, `just`, `buf`, `watchexec`, compilers, and other tools. It should not install dependencies or run codegen unless every shell entry genuinely needs that work.

If helpful, print a short hint:

```sh
echo "Run: turbo run dev"
echo "Run: turbo run deps"
```

### Dependency materialization

For JS dependencies, prefer an explicit task over a shell hook:

```json
{
  "tasks": {
    "deps": {
      "inputs": ["bun.lock", "package.json", "apps/*/package.json", "packages/*/package.json"],
      "outputs": ["node_modules/**", "apps/*/node_modules/**", "packages/*/node_modules/**"]
    },
    "dev": {
      "dependsOn": ["deps"],
      "cache": false,
      "persistent": true
    }
  }
}
```

Use this when the repo accepts caching or restoring dependency directories. If that is too large or platform-sensitive, keep `bun install --frozen-lockfile` as an explicit package-manager step and have the dev command fail clearly when dependencies are missing.

### Dev server entrypoints

Use package scripts for app-local dev servers:

```json
{
  "scripts": {
    "dev": "next dev"
  }
}
```

Use Turbo when the root command must coordinate packages:

```json
{
  "tasks": {
    "dev": {
      "dependsOn": ["^build"],
      "cache": false,
      "persistent": true
    }
  }
}
```

Use Just as the human-facing front door only when it delegates:

```just
dev:
    turbo run dev
```

### Generated files

If generated files are pure build artifacts, model inputs and outputs in Nix, Turbo, or the package's build tool. If generation is a dev-time side effect, put it behind a task or watcher that the consumer depends on.

Avoid making `shellHook` decide that all future commands need generated files. Prefer:

```text
dev -> codegen
test -> codegen
build -> codegen
```

over:

```text
enter shell -> maybe codegen for everyone
```

### Imperative glue

Use `scripts/dev.ts` when startup needs conditionals, traps, process cleanup, readiness checks, or multi-service orchestration that is hard to express in JSON. Call it from `bun run`, `turbo`, or `just` so the public entrypoint remains discoverable. In a TypeScript-only repo do not add `scripts/dev.sh` ([ADR-0012](../../docs/adr/0012-ops-scripts-in-typescript.md)).

```json
{
  "scripts": {
    "dev": "bun scripts/dev.ts"
  }
}
```

## Review checklist

- Shell entry remains cheap and useful even when the user does not need JS modules.
- Commands that need generated files or dependencies declare that relationship.
- Cacheable tasks declare accurate inputs and outputs.
- `just` recipes are thin aliases or repo chores, not hidden task semantics.
- Scripts contain real imperative complexity, not a parallel task graph.
- The public command a human should type is obvious from README, package scripts, or `just --list`.
- There is one canonical path for each workflow, with compatibility aliases only when they reduce friction.

## Tools

None. This is a pure prompt and review skill.

## Reference

No separate reference files. Use the responsibility map, common patterns, and review checklist above.

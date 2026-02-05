---
name: git-commit-messages
description: Generates consistent git commit messages following project conventions. Use when committing changes, creating PRs, or when asked to write commit messages.
---

# Git Commit Message Generator

## Format

```
type(scope): subject in imperative mood

- Body bullet in past tense with period.
- Another change description.
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | Added new functionality |
| `fix` | Fixed a bug |
| `refactor` | Restructured code, no behavior change |
| `chore` | Dependencies, tooling, configs |
| `docs` | Documentation |
| `test` | Tests |
| `cicd` | CI/CD pipelines, deployment |
| `ai` | AI/Claude configurations |

## Rules

1. **Subject**: Imperative mood, lowercase after colon, no period, max 72 chars
2. **Scope**: Derived from path. When changes span multiple scopes, omit the scope entirely
   - `authz` – Authorization stack and FGA models
   - `infra` – Kraftfiles, Dockerfiles, deployment configs
   - `nix` – Flake and Nix configuration
3. **Body**: Past tense, capital start, period at end
4. **No attribution**: Never include "Co-Authored-By", "Generated with", or any AI/author attribution
5. **AI-only changes**: When changes are exclusively AI-related (skills, prompts, Claude configs), always use `ai` type—never `refactor`, `chore`, or other types
6. **Preview before commit**: Always show the proposed commit message to the user for confirmation before executing the commit

## Examples

```
feat(authz): add task permissions with list inheritance
```

```
refactor(authz): split monolithic model into modules

- Separated projects.fga and tasks.fga into distinct files.
- Created fga.mod manifest to declare included modules.
```

```
chore(nix): update flake inputs to latest versions

- Bumped nixpkgs to 2025-12-21.
- Updated unikraft-nur to v0.12.5.
```

```
feat(infra): add Caddy reverse proxy for Unikraft deployment

- Added Kraftfile and rootfs for Caddy unikernel.
- Configured TLS termination and playground proxy.
```

```
docs: restructure README for improved clarity
```

```
chore: update dependencies and documentation

- Bumped openfga-cli to v0.7.8.
- Updated AGENTS.md with README references.
```

```
ai: secure Claude settings by restricting dangerous permissions
```

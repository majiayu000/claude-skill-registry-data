---
name: setup
description: Use when setting up a project, adding linting, formatting, git hooks, or type checking. Detects the language and installs that ecosystem's lint/format/hooks toolchain (JS/TS, Python, Go, Rust).
license: MIT
allowed-tools: Read Glob Write Edit Bash(nub:*) Bash(nubx:*) Bash(pnpm:*) Bash(pnx:*) Bash(npx:*) Bash(bunx:*) Bash(npm:*) Bash(bun:*) Bash(yarn:*) Bash(uv:*) Bash(poetry:*) Bash(pdm:*) Bash(pip:*) Bash(ruff:*) Bash(mypy:*) Bash(go:*) Bash(gofmt:*) Bash(goimports:*) Bash(golangci-lint:*) Bash(cargo:*) Bash(rustfmt:*) Bash(rustup:*) Bash(pre-commit:*) Bash(gitleaks:*) Bash(trufflehog:*)
model: haiku
effort: low
compatibility: Any language project; sets up that ecosystem's lint/format/hooks + a git secret scanner (GitLeaks default; TruffleHog accepted) (JS/TS best-supported, Python, Go and Rust via references/)
metadata:
  short-description: Lint, format, and git hook setup.
---

You are a tooling setup assistant. Detect the project's language, then auto-detect what's missing and install everything that's not already configured for that ecosystem.

## 0. Detect Language and Route

Detect the project's language from its manifest, then follow the matching setup guide:

| Language | Detected by | Setup guide |
|----------|-------------|-------------|
| **JS/TS** | `package.json` | the `rules/*.md` files below (Biome · Husky · commitlint · lint-staged · GitLeaks · TypeScript) |
| **Python** | `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg` | `references/python.md` (Ruff · mypy · pre-commit · GitLeaks) |
| **Go** | `go.mod` | `references/go.md` (gofmt · golangci-lint · pre-commit · GitLeaks) |
| **Rust** | `Cargo.toml` | `references/rust.md` (rustfmt · Clippy · pre-commit · GitLeaks) |

Load **only** the guide for the detected language. For a language not listed (e.g. Ruby), set up its standard formatter/linter and wire the project's secret scanner into a pre-commit hook, following the same shape; note that first-class support for it is not yet bundled. A secret scanner (GitLeaks default; TruffleHog accepted) is set up in **every** ecosystem — it is cross-language.

The rest of this file (Steps 1-5) is the **JS/TS** path. For Python, Go or Rust, follow the referenced guide, then jump to Step 5 (Supply Chain Hardening) which applies to any ecosystem.

## 1. Detect Package Manager

Detect the package manager from the lockfile, in this order: `nub.lock`, `pnpm-lock.yaml`, `bun.lock`/`bun.lockb`, `yarn.lock`, `package-lock.json`. With no lockfile, ask.

A `packageManager` or `devEngines.packageManager` field in `package.json` outranks any lockfile. Nub runs in compat-mode over another manager's lockfile, so `nub.lock` alongside `pnpm-lock.yaml` means nub — check the field before concluding from lockfiles alone.

Rule files use two placeholders. Replace `<pm>` with the detected manager and `<pmx>` with that manager's ephemeral package runner:

| Detected PM | `<pm>` | `<pmx>` |
|-------------|--------|---------|
| nub | `nub` | `nubx` |
| pnpm | `pnpm` | `pnx` |
| bun | `bun` | `bunx` |
| npm | `npm` | `npx` |
| yarn (v2+) | `yarn` | `yarn dlx` |
| yarn (v1) | `yarn` | `npx` |

Detect yarn version: `.yarnrc.yml` present → v2+; only `.yarnrc` or neither → v1.

Never write one manager's runner into another manager's project — a `pnx` line in a bun project's git hook fails at commit time, and it bypasses the store integrity and registry config that the project's real manager enforces.

## 2. Detect Existing Tooling

Before installing anything, scan for existing configurations:
- `biome.json` / `biome.jsonc` → Biome already configured
- `.husky/` directory → Husky already configured
- commitlint config listed in `rules/commitlint.md` → commitlint already configured
- `.lintstagedrc*` / `lint-staged` key in `package.json` → lint-staged already configured
- `gitleaks` or `trufflehog` in `.husky/pre-commit` → secret scanner already configured
- `tsconfig.json` → TypeScript already configured
- `.eslintrc*` / `eslint.config.*` → ESLint present (suggest migration to Biome)
- `.prettierrc*` / `prettier.config.*` → Prettier present (suggest migration to Biome)

**Skip tools that are already configured.** Report what was skipped at the end.

## 3. Install Tools

Read each rule file for detailed setup instructions and config files.

> **This stack is opinionated by design.** Tooling choices are subjective — Biome vs ESLint/Prettier, conventional commits vs none, Husky vs another hook manager are all legitimate positions. Each rule file documents its choice under `### Why This Matters` and names the mainstream alternative under `### Alternatives`. Two principles: you may decline any tool, and a deliberately-configured alternative is **kept, not swapped** — Step 2's detection exists so the skill fills genuine gaps rather than overriding working setups. Secret scanning is the one thing recommended for every project (GitLeaks default; TruffleHog accepted); only the scanner is swappable, not whether to scan.

### Auto-install (always set up when missing)

| Tool | Purpose | Rule |
|------|---------|------|
| Biome | Linting + formatting | `rules/biome.md` |
| Husky | Git hooks | `rules/husky.md` |
| commitlint | Conventional commits | `rules/commitlint.md` |
| lint-staged | Pre-commit linting | `rules/lint-staged.md` |
| Secret scanner | Secrets detection | `rules/secret-scanner.md` |
| TypeScript | Type checking | `rules/typescript.md` |

### Opt-in (only when explicitly requested)

| Tool | Purpose | Rule |
|------|---------|------|
| semantic-release | Automated versioning | `rules/semantic-release.md` |

## 4. Output Summary

After all tools are installed, display a summary:

```
## Setup Complete

### Installed
- [list of tools installed]

### Skipped (already configured)
- [list of tools skipped with reason]

### Next Steps
- Run `<pm> run check` to verify Biome is working
- Make a test commit to verify git hooks
```

## 5. Supply Chain Hardening

After tooling setup is complete, check if the `deps` skill is available by looking for `skills/deps/SKILL.md` relative to this skill's directory. If it exists, run `/deps` to harden the ecosystem's dependency supply chain (it detects the language too). If it does not exist, skip this step silently.

Requires git initialised in the project, and a secret scanner installed on the system (`brew install gitleaks` or equivalent) — it is wired into the pre-commit hook in every ecosystem.

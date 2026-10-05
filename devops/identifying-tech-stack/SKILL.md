---
name: identifying-tech-stack
description: Use when onboarding to a new project, evaluating migration feasibility, auditing dependency health, or needing to know what technologies power a codebase
---

## Announce at start: "Using codebase-analyzer to identify the tech stack."

## Overview

Catalog every technology, framework, library, and tool in use. First Track A skill -- its output informs all subsequent analysis. This skill goes beyond surface-level detection to reveal the project's true runtime reality: what actually ships, what was migrated halfway, and what the team struggles with.

## Process

1. Read package manifests (package.json, Cargo.toml, go.mod, requirements.txt, pom.xml, .csproj, Gemfile, etc.)
2. Identify build tools from config files (webpack.config, vite.config, tsconfig, Makefile, Dockerfile, Jenkinsfile)
3. Detect frameworks from code patterns and dependencies
4. Identify runtime/language versions (engines field, .python-version, .nvmrc, rust-toolchain.toml)
5. Map deployment infrastructure (Docker, K8s, serverless, CI/CD)
6. Flag outdated or deprecated dependencies
7. Produce tech stack report

## Diagnostic Reasoning

1. **Read package manifests in dependency order:** Lock files first (ground truth of what's installed), then manifests (declared intent). Divergence = dependency drift.

2. **Check scripts before dependencies:** `package.json` "scripts" reveal the ACTUAL build pipeline. If "build" runs webpack but devDependencies lists vite, someone migrated partially. Declared deps lie; scripts tell truth.

3. **Compare dependencies vs devDependencies placement:** Business logic in devDependencies = build-time-only (code generation). Test utilities in dependencies = production monitoring. Misplaced deps reveal team confusion.

4. **Look for overrides/resolutions:** Each override in `package.json` is a hidden story about a transitive dependency conflict. Count them -- more than 5 indicates dependency hell.

5. **Check engine pinning:** Pinned engines (`"node": "18.x"`) reveal deployment constraints. Absent engines with cutting-edge syntax = only runs on developer machines.

6. **Detect migration fossils:** Both `webpack.config` AND `vite.config` = migration in progress. Both `.eslintrc` AND `eslint.config` = migration stalled. Coexistence = incomplete transition.

## Trigger Signals

- **HIGH confidence**: Found .js.map files with no TypeScript source -> `trace-codebase-provenance`
- **HIGH confidence**: Unknown/custom build tools not in standard catalog -> `analyze-build-pipeline`
- **MEDIUM confidence**: Mixed language ecosystem -> affects analysis strategy
- **LOW confidence**: Standard tech stack, all well-known -> no deep dive needed

## Adversarial Lens

If the team wanted to hide their true tech stack, what would they change? Check for misleading package.json entries, fake build configs, or dependencies that are actually used but not listed (phantom deps). The declared stack is what they WANT you to see.

## Red Flags

- Reporting only top-level deps without checking transitive
- Missing the build tool chain (only listing languages)
- Not checking for lock files (package-lock, yarn.lock, Cargo.lock)

## When NOT to Use

When you only need to know "is this Python or JS?" -- just check file extensions. This skill is for deep stack understanding: dependency health, migration state, build pipeline truth, and team process gaps revealed by manifest structure. For simple language identification, file pattern matching suffices.

## SECURITY_SIGNAL

Watch for these during manifest analysis:

- **Outdated dependencies with known CVEs:** Check package-lock or Cargo.lock versions against known vulnerability databases. A dependency pinned to a version with published CVEs is a direct risk.
- **Private registries without auth:** `registry` fields pointing to private URLs without corresponding `.npmrc` or `.yarnrc.yml` credentials configuration = broken builds on fresh machines or leaked registry URLs.
- **Build tools with known supply-chain attacks:** `postinstall` scripts that download binaries, `npx` commands in CI that resolve to the network, or pre-built binary dependencies without integrity hashes.

## Output Contract

Write `docs/analysis/tech-stack.md` using standard contract.
Include: languages, frameworks, build tools, runtime versions, CI/CD, dependency health.

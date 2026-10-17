---
name: deps
description: Use when hardening a dependency supply chain, pinning versions, adding registry/security flags, or setting up Renovate. Detects the language and locks down install scripts, versions, and CI checks (JS/TS, Python, Go, Rust).
license: MIT
allowed-tools: Read Glob Grep Write Edit Bash(nub:*) Bash(nubx:*) Bash(pnpm:*) Bash(pnx:*) Bash(npx:*) Bash(bunx:*) Bash(npm:*) Bash(bun:*) Bash(yarn:*) Bash(uv:*) Bash(pip:*) Bash(pip-audit:*) Bash(go:*) Bash(govulncheck:*) Bash(cargo:*) Bash(cargo-audit:*) Bash(cargo-deny:*) Bash(gh:*) Bash(glab:*)
model: haiku
effort: medium
compatibility: Any language project; hardens that ecosystem's dependency supply chain (JS/TS best-supported, Python, Go and Rust via references/)
metadata:
  short-description: Dependency supply-chain hardening.
---

You harden dependency supply-chain security. Detect the project's language, then auto-detect what's already configured and apply only missing hardening measures for that ecosystem.

## 0. Detect Language and Route

Detect the project's language from its manifest, then follow the matching hardening guide:

| Language | Detected by | Hardening guide |
|----------|-------------|-----------------|
| **JS/TS** | `package.json` | the `rules/*.md` files below (pinning · release quarantine · Renovate · dependency review · package runner) |
| **Python** | `pyproject.toml`, `requirements*.txt`, `setup.py` | `references/python.md` (pin + hashes · pip-audit · Renovate/Dependabot · dependency review) |
| **Go** | `go.mod` | `references/go.md` (`go mod verify` · govulncheck · checksum DB · dependency review) |
| **Rust** | `Cargo.toml` | `references/rust.md` (commit `Cargo.lock` · cargo audit/cargo-deny · source policy · dependency review) |

Load **only** the guide for the detected language. For a language not listed (e.g. Ruby → `bundler-audit`), apply the same shape — pin versions, scan for vulnerabilities, automate updates, gate PRs — and note that first-class support for it is not yet bundled.

The rest of this file (Steps 1-4) is the **JS/TS** path. For Python, Go or Rust, follow the referenced guide, then use the shared summary format in Step 4.

## 1. Detect Package Manager

Detect the package manager from the lockfile, in this order: `nub.lock`, `pnpm-lock.yaml`, `bun.lock`/`bun.lockb`, `yarn.lock`, `package-lock.json`. With no lockfile, ask.

A `packageManager` or `devEngines.packageManager` field in `package.json` outranks any lockfile. Nub runs in compat-mode over another manager's lockfile, so `nub.lock` alongside `pnpm-lock.yaml` means nub — check the field before concluding from lockfiles alone.

Rule files use two placeholders. Replace `<pm>` with the detected manager and `<pmx>` with that manager's ephemeral package runner — see the mapping table in `rules/package-runner.md`.

## 2. Detect Existing Config

Before applying any hardening, scan for existing configurations:
- `renovate.json` / `.renovaterc` / `.renovaterc.json` / `renovate` key in `package.json` → Renovate already configured
- `.github/workflows/*.{yml,yaml}` containing `dependency-review` → dependency review exists
- `package.json` dependency versions without `^` or `~` prefixes → already pinned

**Skip rules whose checks already pass.** Report what was skipped at the end.

## 3. Apply Rules

Read each rule file for detailed instructions and config templates.

| Rule | Impact | File |
|------|--------|------|
| Release quarantine | MEDIUM | `rules/release-quarantine.md` |
| Version pinning | HIGH | `rules/version-pinning.md` |
| Renovate | MEDIUM | `rules/renovate.md` |
| Dependency review | HIGH | `rules/dependency-review.md` |
| Package runner | MEDIUM | `rules/package-runner.md` |

## 4. Output Summary

After all rules are processed, display a summary:

```
## Supply Chain Hardening Complete

### Applied
- [list of rules applied with brief description]

### Skipped (already configured)
- [list of rules skipped with reason]

### Manual Steps Required
- [any post-setup steps, e.g. "Run `<pm> exec husky` to reinitialise git hooks"]
```

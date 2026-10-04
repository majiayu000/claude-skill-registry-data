---
name: dep-guard
description: >-
  This skill should be used when the user asks to "install a package", "add a
  dependency", "check for vulnerabilities", "audit dependencies", or mentions
  "npm install", "pip install", "composer require", "yarn add", "pnpm add",
  "check vulnerability", "audit dependencies". Provides dependency security
  and version management by intercepting package installs to enforce latest
  versions and block vulnerable packages.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Dep Guard Skill

Automated dependency security enforcement. The PreToolUse hook intercepts all package install commands and enforces:

1. **Registry connectivity** — hard-blocks if offline (can't verify = can't install)
2. **Latest versions** — resolves and upgrades outdated version requests
3. **Vulnerability scanning** — checks OSV.dev for known CVEs before install

## How It Works

The `dep-guard.py` hook runs on every Bash command. If it detects an install command (npm install, pip install, composer require, etc.), it:

1. Pings the registry to confirm it's reachable
2. Extracts package names and requested versions
3. Queries the registry for latest versions
4. Queries OSV.dev for vulnerabilities against the target version
5. Makes a decision:

| Condition | Action |
|-----------|--------|
| Registry offline | BLOCK — hard stop until online |
| Scan failed | BLOCK — can't verify safety |
| Critical/High vuln | BLOCK — must find alternative |
| Medium vuln | WARN — allow with warning |
| Low/no vulns | ALLOW |
| Outdated version requested | BLOCK — provide corrected command |
| No version specified | ALLOW — will get latest automatically |
| Lockfile install (npm ci, etc.) | SKIP — no new packages |

## Supported Ecosystems

| Ecosystem | Install Commands | Registry | Vuln Source |
|-----------|-----------------|----------|-------------|
| npm | `npm install/i/add` | npmjs.org | OSV.dev (npm) |
| yarn | `yarn add` | npmjs.org | OSV.dev (npm) |
| pnpm | `pnpm add/install` | npmjs.org | OSV.dev (npm) |
| bun | `bun add/install` | npmjs.org | OSV.dev (npm) |
| pip | `pip install`, `uv add` | pypi.org | OSV.dev (PyPI) |
| composer | `composer require` | packagist.org | OSV.dev (Packagist) |

## Commands

- `/dep-check [package]` — Check a specific package before installing
- `/dep-audit [--fix]` — Audit all installed dependencies

## Logs

Debug logs are written to `/tmp/dep-guard.log` for troubleshooting.

## Critical Rule: No Wrapper Scripts

You MUST always run package install commands directly via the Bash tool. Never create a script in any language that internally invokes a package manager to circumvent the hook.

Prohibited patterns include:
- Writing Python, Node, shell, or any other script files that run install commands internally via process spawning
- Using inline interpreter calls (e.g. `python3 -c` or `node -e`) that wrap install commands
- Using remote execution (docker, ssh) to install packages outside the hook's reach

All of these bypass the dep-guard security hook. If the hook blocks an install, that block is intentional. Do not work around it. Instead, inform the user why the install was blocked and suggest an alternative package or version.

## Bypassing (Emergency Only)

If the hook blocks something incorrectly, the user can disable the plugin temporarily in `.claude/settings.json`. The hook should never be bypassed in normal operation.

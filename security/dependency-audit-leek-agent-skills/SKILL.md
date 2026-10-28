---
name: dependency-audit
description: Run a dependency audit for Composer or npm projects and propose a safe upgrade plan.
disable-model-invocation: true
context: fork
agent: leek-skills:dependency-auditor
background: false
argument-hint: "composer | npm (omit to auto-detect)"
allowed-tools: "Bash(composer outdated *) Bash(composer audit) Bash(composer audit *) Bash(npm outdated *) Bash(npm audit) Bash(npm audit *) WebFetch"
---

# Dependency Audit

## Goal

Deliver a dependency audit summary for the package manager this project uses.

In Claude Code with this plugin installed, this skill runs in its own `dependency-auditor` subagent (read-only, remembers packages the project has chosen to hold back); the report comes back to the main session when it finishes. In other harnesses it runs inline; the steps are the same.

## Detect package manager

**The package manager is `$ARGUMENTS`.** If it is `composer` or `npm`, audit only that manager, and stop and report if its manifest (`composer.json` or `package.json`) is missing. If it names any other manager, stop and report that only Composer and npm are supported. If it is empty, inspect the project root:

- `composer.json` present → **Composer** (PHP)
- `package.json` present → **npm** (JavaScript / TypeScript)
- Both present → audit **both**, report each section separately
- Neither present → stop and report that the directory is not a Composer or npm project

## Run

### Composer

```bash
composer outdated --direct || true
composer audit || true
```

### npm

```bash
npm outdated || true
npm audit || true
```

Run security audit when a lockfile makes the result meaningful (`composer.lock`, `package-lock.json`, or `npm-shrinkwrap.json`).

### Major bumps

For each major update, source its breaking changes from the package, not from memory: fetch its `CHANGELOG`, `UPGRADE` guide, or GitHub release notes for the versions crossed where the harness can reach the web (`WebFetch` in Claude Code), and cite the URL; otherwise read the changelog shipped under `vendor/<package>/` or `node_modules/<package>/` and mark the risk *unverified* (it covers only the installed version).

## Report

Summarize the result with:

- Package manager evidence (`composer.json` / `composer.lock`, or `package.json` / lockfile, plus framework hints when relevant)
- Outdated **direct** dependencies grouped by patch, minor, and major updates
- Security advisories from the audit command, grouped by severity, when available
- Recommended safe upgrade order, starting with low-risk patch and minor updates
- Breaking-change risks, required code changes, runtime/framework constraints, or test coverage gaps for major updates
- Exact verification commands the project should run after upgrades

Keep the report direct. Do not apply upgrades unless the user asks you to do the upgrade work.

## Guardrails

- Do not modify the check commands to force success.
- Do not skip, disable, or bypass checks to make the audit look clean.
- If package metadata is missing, dependency resolution fails, or audit output is blocked by registry/authentication issues, stop and report the blocker.

---
name: dependency-changes
description: Adding, upgrading, or removing dependencies — justification bar, registry-verified versions, changelog and pinned-constraint archaeology, matching package-manager and lockfile hygiene, one bump at a time, gates after. Use when adding, bumping, removing, or auditing a package; before editing package.json, pyproject.toml, Cargo.toml, go.mod, or any lockfile; on security advisories, audit/Dependabot alerts, deprecation or peer-dependency warnings, version-mismatch errors, or "update everything" requests.
---

# Dependency Changes

Weak dependency work types a version number from memory, runs whichever install command comes to mind, and declares success when the install exits 0. Strong dependency work queries the registry, uses the project's own package manager, changes one thing, runs the gates, and reads the lockfile diff before committing.

## Adding a dependency

1. **Clear the justification bar**: does the stdlib do it? Does an existing dependency (read the manifest — the codebase often already carries a lib covering 90%)? Is it small enough to write inline (a 20-line util beats a package)? Only then add.
2. **Vet it**: last release date, open-issue triage, download count, license, install footprint and transitive count (`npm info`, `pip show`, `cargo tree`, or the equivalent). 40 transitive deps for one function is a bad trade.
3. **Use the project's package manager exactly**: identify it from the lockfile present (`pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `uv.lock`, `poetry.lock`, `Cargo.lock`, ...) and use the matching tool. Never create a second lockfile kind; never hand-edit a lockfile; respect workspace/catalog conventions in monorepos.
4. **Pin the way neighbors pin**: exact vs caret vs range — copy the manifest's existing style.

## Upgrading

1. **Never write a version from memory.** Query the registry for the current version (`npm view <pkg> version`, `pip index versions <pkg>`, `cargo search <pkg>`, `go list -m -versions <mod>`) and read the currently installed version from the lockfile, not the manifest range. Paste both in your report.
2. **Read the changelog between installed and target** — the BREAKING sections and migration guides. For a major bump, budget for API changes instead of discovering them via type errors.
3. **Check for pinned-constraint reasons before bumping.** A dependency held at an old major is often deliberate. Search CLAUDE.md, README, comments, and `git log -S<pkg>` for the package name. "Upgrade everything" does not authorize breaking a documented pin.
4. **Check engine and peer constraints**: the target's required runtime version and peer ranges against what the project runs. A peer warning in the install output is an error that has not happened yet — report it, do not scroll past it.
5. **One bump at a time** (or one tightly coupled group, e.g. a framework and its plugins). A 15-package bump that breaks the build is unbisectable.
6. **Security advisories**: take the smallest version delta that clears the advisory; check whether the vulnerable path is reachable in this codebase when judging urgency.

## After ANY dependency change

- Full install with the project's tool, then the full gate suite: build/typecheck, lint, tests.
- Exercise the features that use the changed package at runtime — type-compatible is not behavior-compatible (defaults change, peer behavior shifts).
- Read the lockfile diff: it should touch what you expect. A one-package bump that rewrites 500 lockfile lines gets explained before it gets committed.
- Commit lockfile and manifest together, and (unless asked otherwise) separately from feature code.

## Removing

Grep for every import/require AND every string reference — plugins, rc files, build configs, and CI reference packages by name. Remove, reinstall, run gates. Dead dependencies are worth removing when noticed, as their own commit.

## Surface rather than push through

Typosquat-adjacent names, install scripts doing surprising work, an upgrade that forces a cascade (runtime version, framework major), a license change, or a registry version that differs from what the user asked for. These are decisions for the user, with your recommendation attached.

## Report

Include: package, installed → target version with the registry query that produced it, the changelog items that affect this codebase, install warnings, gate results, what you exercised at runtime, and the lockfile diff size.

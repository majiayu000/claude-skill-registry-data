---
name: mav-bp-dependency-management
description: Dependency management conventions for all projects. Covers lock files, version pinning, vulnerability scanning, license compliance, update strategy, and minimal dependency principle. Applied when adding, updating, or reviewing dependencies.
user-invocable: false
disable-model-invocation: true
---

# Dependency Management Standards

Maverick's hard rules for keeping dependencies intentional, pinned, secure, and maintained.

## Maverick's Rules

- **Lock files are committed and reviewed** — inspect lock diffs for unexpected transitive additions; never manually edit a lock file (regenerate from the manifest).
- **CI and production install from the lock, never resolve fresh** — `npm ci`, `yarn install --immutable`, `pnpm install --frozen-lockfile`, `uv sync --locked`, `cargo install --locked`, `bundle install --frozen`, or the ecosystem equivalent.
- **Vulnerability scanning is mandatory in CI** — runs on every PR plus a scheduled cadence against the default branch. Critical/high findings block merges; medium is fixed within the current iteration; false positives are suppressed only with a documented justification.
- **License allow-list** — acceptable by default: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, 0BSD, Unlicense. Copyleft (GPL/LGPL, and especially AGPL for SaaS) and unknown/no-license dependencies are blocked pending investigation. Audit transitive licenses too.
- **Minimal dependency principle** — no packages for trivial utilities, single-use wrappers, or stdlib-covered functionality. Do add packages for crypto/auth/security-sensitive logic — never roll your own.
- **Never `*` or `latest` version specifiers.** Exact pins for security-critical dependencies (auth, crypto); when in doubt, pin tighter.
- **Major version bumps get dedicated PRs** — one major at a time, never buried in feature PRs. Security patches fast-track after CI.
- **Abandoned packages (no releases/response in 12+ months)** — migrate to a maintained alternative, fork into the organisation, or inline the functionality.
- **Never `--force` or `--legacy-peer-deps`** — fix the underlying version conflict.

## Project Implementation Lookup

Check for `docs/maverick/skills/dependency-management/SKILL.md`. If present, read it — it wins on specifics (library, config, conventions). If missing, proceed with these standards and note the gap in your summary.

## Detecting Dependency Issues in Code Review

| Pattern | Issue | Fix |
| ------- | ----- | --- |
| Lock file not committed | Non-deterministic builds | Commit the lock file, use frozen install in CI |
| Lock file manually edited | Corrupted dependency resolution | Regenerate from manifest |
| New dependency for trivial functionality | Unnecessary surface area | Inline the logic or use standard library |
| Dependency with no license or copyleft license | Legal risk | Replace with a permissively licensed alternative |
| Major version bump buried in a large PR | Breaking changes may be missed | Isolate major bumps into dedicated PRs |
| `*` or `latest` in version specifiers | Unpredictable builds | Pin to a specific range |
| No vulnerability scanning in CI | Known CVEs may ship | Add `npm audit` / `pip-audit` / equivalent to pipeline |
| Dependency with no recent releases (12+ months) | Abandoned package risk | Evaluate alternatives or plan a fork |
| Large transitive dependency addition | Unexpected supply chain expansion | Investigate and consider lighter alternatives |
| `--force` or `--legacy-peer-deps` in install commands | Masking resolution conflicts | Fix the underlying version conflict |

<!-- maverick-plugin-version: 4.0.2-dev -->

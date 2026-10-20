---
name: dependency-management
description: >-
  Load this skill when adding, removing, or upgrading a dependency: evaluating whether a package is
  appropriate, deciding on pinning strategy, handling a major version upgrade, or running a security
  audit. Auto-load whenever a new package is being added with uv add or bun add, a dependency
  version is being changed, or a vulnerability is found in an existing package.
compatibility: >-
  Requires the target project's package manager on PATH and network access to the registry: `uv`
  with Python 3.12+ for Python projects, `bun` (or Node.js 20+ with npm) for JS/TS projects. Audit
  commands (`uv run pip-audit`, `bun audit`) need the same. Neither is assumed installed.
---

# Dependency Management

Every dependency change is evaluated before it lands, pinned per policy, and committed together
with its lockfile.

## Procedure

1. Evaluate the package before adding it:
   1. **Necessity** — can this be done with < 20 lines of code in-house?
   2. **Maintenance** — actively maintained? Last commit < 6 months?
   3. **Popularity and trust** — download volume, stars, known maintainers?
   4. **License** — compatible? Avoid GPL for proprietary code.
   5. **Size** — bundle/install size impact?

   If a dependency fails any of these, document why you're adding it anyway.

2. Apply the change:

   ```bash
   # Add (always commit the updated lockfile alongside the manifest)
   uv add httpx                 # Python runtime dep
   uv add --dev pytest          # Python dev/test dep
   bun add zod                  # TS runtime dep
   bun add --dev vitest         # TS dev dep

   # Remove (drops it from manifest + lockfile)
   uv remove httpx
   bun remove zod

   # Upgrade
   uv lock --upgrade-package httpx   # one package to its allowed range
   bun update zod
   ```

3. Commit `uv.lock` / `bun.lock` in the **same commit** as the manifest change — a manifest edit
   without its lockfile produces non-reproducible installs.

## Pinning policy

| Environment             | Pin level                |
| ----------------------- | ------------------------ |
| Production dependencies | Exact version            |
| Dev/test dependencies   | Minor version (`^1.2.0`) |
| CI tool versions        | Exact version            |

Never use `*` or `latest`. Note the syntax differs by ecosystem: npm/bun use caret ranges
(`^1.2.0`); Python uses comparison ranges (`>=1.2,<2.0`) or exact (`==1.2.0`). The lockfile pins
the exact resolved version regardless — the manifest range only bounds what an upgrade may pick.

## Security audits

Run before every release and in CI:

```bash
uv run pip-audit    # Python
bun audit           # TypeScript
```

Address all high-severity findings before release. Document accepted medium-severity exceptions
in `ARCHITECTURE.md` Key Decisions.

## Rules

Major version upgrades require:

1. A dedicated PR (not bundled with feature work)
2. A brief Key Decisions entry in `ARCHITECTURE.md` explaining the upgrade and breaking changes
   handled
3. Full test suite pass after upgrade

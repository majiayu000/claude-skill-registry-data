---
name: verify
description: "Run all local validation checks for Skoleoverblikket before declaring work done. USE THIS SKILL when the user says 'verify', 'check everything', 'validate', 'is this ready', 'does it compile', 'are there errors', or similar. Runs: Biome, TypeScript build, dotnet format, dotnet build, API integration tests, and ryni (Markdown links + skill metadata). Playwright e2e is the /test skill."
---

# Verify Skill

Runs all checks matching CI via `verify.ps1` at the repo root.

## Run

```powershell
# Check everything (auto-fixes dotnet formatting by default)
pwsh scripts/verify.ps1

# Report formatting violations instead of fixing
pwsh scripts/verify.ps1 -NoFix

# Skip integration tests (quick compile check)
pwsh scripts/verify.ps1 -SkipTests
```

The script runs all steps and **collects all errors before exiting** — you see every failure at once, not just the first one.

## Steps

1. **Biome** — `cd web && npx biome check src/`
2. **TypeScript build** — `cd web && npm run build`
3. **dotnet format** — auto-fixes by default; output suppressed. Use `-NoFix` to inspect violations.
4. **dotnet build** — Release, `-p:CI=true`
5. **API integration tests** — tUnit + Testcontainers (skipped with `-SkipTests`; needs Docker)
6. **ryni** — broken local Markdown links and invalid `SKILL.md` metadata (skipped with `-SkipDocs`). Checks a temp mirror of non-gitignored files, so `node_modules` and build output are ignored. Fails with an install hint if `ryni` is missing — run `scripts/setup.ps1`.

## Playwright e2e

Playwright is not part of `verify.ps1` — use the `/test` skill for that.

## Rules

- Run `verify.ps1` after every code change, before committing or declaring done
- Default is auto-fix; never pass `-NoFix` unless you want to see violations without changing files
- If Docker is not running, integration tests fail with a container error — say so explicitly rather than treating it as a code bug
- Do not report work as done until the script exits 0
- Script collects all failures before exiting — read the summary, not intermediate output

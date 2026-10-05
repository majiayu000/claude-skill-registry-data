---
name: preflight
description: "Pre-deploy verification gate. Checks git status, build, tests, migrations, secrets, and commit conventions. Reports READY or NOT READY. Read-only, no changes. Trigger words: preflight, pre-deploy check, ready to deploy, deployment checklist."
version: "2.0.0"
category: qa
platforms:
  - CLAUDE_CODE
---

You are a pre-deploy verification agent. Check everything before deploying.
Do NOT make any changes. Report only. Do NOT ask the user questions.

============================================================
CONFIGURATION
============================================================

Deploy flag behavior is configurable. By default, no deploy flag is required.
If the project's CLAUDE.md or package.json contains a `deployFlag` setting
(e.g., `deploy:username`, `deploy:prod`, `ship-it`), enforce that flag in the
last commit message. Otherwise, skip the deploy flag check entirely.

To detect: look for `deployFlag` in the project's CLAUDE.md, or a
`preflight.deployFlag` field in package.json / pyproject.toml. If found,
use that value. If not found, mark deploy flag check as N/A.

============================================================
CHECK 1: GIT STATUS
============================================================

Run these checks and record pass/fail:

1. **Uncommitted changes:** `git status --porcelain`
   - PASS if empty (clean working tree)
   - FAIL if any uncommitted changes exist

2. **Unpushed commits:** `git log origin/{branch}..HEAD --oneline 2>/dev/null`
   - PASS if empty (all pushed)
   - FAIL if unpushed commits exist — list them

3. **Branch up to date:** `git fetch origin && git diff HEAD origin/{branch} --stat 2>/dev/null`
   - PASS if no differences
   - WARN if remote has commits not in local

4. **Merge conflicts:** `git diff --check`
   - PASS if no conflict markers
   - FAIL if conflict markers found

============================================================
CHECK 2: BUILD VERIFICATION
============================================================

Auto-detect project type and run the appropriate build check.
Check these in order (first match wins):

**Scala/Play** (if `build.sbt` exists):
- Run `sbt compile`

**Flutter/Dart** (if `pubspec.yaml` exists):
- Run `flutter analyze`
- PASS if no issues, WARN if warnings only, FAIL if errors

**Node.js / TypeScript** (if `package.json` exists):
- If `tsconfig.json` exists: `npx tsc --noEmit`
- Else if `scripts.build` in package.json: `npm run build`
- Else: PASS (no build step)

**Python** (if `pyproject.toml` or `setup.py` or `setup.cfg` exists):
- If `pyproject.toml` has `[tool.mypy]`: `mypy .`
- Else if `ruff` is available: `ruff check .`
- Else: PASS (no static check configured)

**Go** (if `go.mod` exists):
- Run `go build ./...`

**Rust** (if `Cargo.toml` exists):
- Run `cargo check`

**Ruby/Rails** (if `Gemfile` exists):
- If Rails (`bin/rails` exists): `bin/rails db:prepare && bin/rails assets:precompile` (dry-run check only — skip if no DB)
- Else: `bundle exec ruby -c` on changed files

**Java/Kotlin** (if `pom.xml` exists):
- Run `mvn compile -q`
- Or if `gradlew` exists: `./gradlew compileJava`

For all: PASS if exit code 0, FAIL otherwise (unless noted above).

============================================================
CHECK 3: TEST SUITE
============================================================

Auto-detect and run the appropriate test command:

**Scala/Play:** `ENVIRONMENT=test sbt test`
**Flutter:** `flutter test`
**Node.js:** Check package.json scripts — prefer `vitest run`, then `jest`, then `npm test`
**Python:** `pytest` (or `python -m pytest`)
**Go:** `go test ./...`
**Rust:** `cargo test`
**Ruby/Rails:** `bundle exec rspec` or `bundle exec rails test`
**Java/Kotlin:** `mvn test -q` or `./gradlew test`

- PASS if all tests pass
- FAIL if any test fails — list failures

============================================================
CHECK 4: MIGRATION STATUS
============================================================

Auto-detect which migration framework is in use and check for
pending/unapplied migrations. Check all that match:

**Flyway** (if `src/main/resources/db/migration/` exists):
- List migration files sorted by version
- Check for files newer than last commit on base branch

**Prisma** (if `prisma/` dir or `prisma` in package.json):
- Check `npx prisma migrate status` or list files in `prisma/migrations/`
- WARN if unapplied migrations exist

**Alembic** (if `alembic/` dir or `alembic.ini` exists):
- List files in `alembic/versions/`
- Check for uncommitted migration files

**Django** (if `manage.py` exists and project uses Django):
- Check for unapplied migrations: `python manage.py showmigrations --plan | grep '\[ \]'`

**Rails** (if `db/migrate/` exists):
- List migration files, check for pending ones

**Knex** (if `knexfile` or `migrations/` with knex patterns):
- List files in migrations directory

**Sequelize** (if `migrations/` dir and sequelize in package.json):
- List migration files

For all frameworks:
- PASS if no pending migrations
- WARN if pending migrations exist — list them for review
- N/A if no migration framework detected

============================================================
CHECK 5: DEPENDENCY LOCK FILES
============================================================

1. Check if lock files have uncommitted changes:
   - `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - `pubspec.lock`
   - `Gemfile.lock`
   - `poetry.lock`, `uv.lock`, `Pipfile.lock`
   - `Cargo.lock`
   - `go.sum`
2. PASS if lock files are committed or unchanged.
3. WARN if lock files have uncommitted changes.

============================================================
CHECK 6: SECRETS SCAN
============================================================

Scan tracked files for accidentally committed secrets:

1. Search for common secret patterns in staged/committed files:
   - API keys: patterns like `AKIA[0-9A-Z]{16}`, `sk-[a-zA-Z0-9]{20,}`
   - Private keys: `-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----`
   - Tokens: `ghp_`, `gho_`, `github_pat_`, `xoxb-`, `xoxp-`
   - Generic secrets: lines matching `(password|secret|token|api_key)\s*[:=]\s*['"][^'"]{8,}`
     (skip if value is clearly a variable reference like `${}`, `process.env`, `os.environ`)
   - .env files tracked in git: `git ls-files | grep '\.env'` (exclude `.env.example`, `.env.sample`)

2. PASS if no secrets detected
3. FAIL if any potential secrets found — list file and line number

============================================================
CHECK 7: CONVENTION COMPLIANCE
============================================================

1. **Deploy flag** (configurable — see CONFIGURATION above):
   - If a deploy flag is configured, check if the last commit message contains it
   - PASS if present, FAIL if missing
   - N/A if no deploy flag configured

2. **No Co-Authored-By:** Check all commits on this branch for Co-Authored-By lines.
   `git log {base}..HEAD --format="%b" | grep -i "co-authored-by"`
   - PASS if none found
   - FAIL if any found — list the commits

3. **No AI attribution:** Check PR description (if PR exists) for AI/Claude references.
   `gh pr view --json body 2>/dev/null`
   - PASS if no AI references found
   - FAIL if references found

4. **Branch pushed:** Verify current branch exists on remote.
   - PASS if pushed
   - FAIL if not pushed


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate your work:

1. Re-run the specific checks that originally found issues.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Preflight Check Results

| # | Check | Status | Details |
|---|-------|--------|---------|
| 1 | Uncommitted changes | {PASS/FAIL} | {details} |
| 2 | Unpushed commits | {PASS/FAIL} | {details} |
| 3 | Branch up to date | {PASS/WARN} | {details} |
| 4 | Merge conflicts | {PASS/FAIL} | {details} |
| 5 | Build | {PASS/FAIL} | {framework detected} |
| 6 | Tests | {PASS/FAIL} | {X passed, Y failed} |
| 7 | Pending migrations | {PASS/WARN/N/A} | {framework: details} |
| 8 | Lock files | {PASS/WARN} | {details} |
| 9 | Secrets scan | {PASS/FAIL} | {details} |
| 10 | Deploy flag | {PASS/FAIL/N/A} | {details} |
| 11 | No Co-Authored-By | {PASS/FAIL} | {details} |
| 12 | No AI attribution | {PASS/FAIL} | {details} |
| 13 | Branch pushed | {PASS/FAIL} | {details} |

**VERDICT: {READY TO DEPLOY / NOT READY}**

If NOT READY, list exactly what needs to be fixed:
1. {action needed}
2. {action needed}

NEXT STEPS:
- If READY: "Safe to merge and deploy."
- If NOT READY: "Run `/hotfix` to fix failing tests" or "Commit and push your changes."
---


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /preflight — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

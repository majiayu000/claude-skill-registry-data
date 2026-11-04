---
name: quality-gate
description: >-
  Run the Greenhouse quality gate before handing off or committing: typecheck, lint (with the plugin
  boundary check) and the full test suite, then the extra gates the change surface needs (HTTP
  security e2e, plugin assembly and core-only run, universal client checks and browser suite,
  desktop), a compliance scan of the changed files, a docs-sync check and a status table. Use for:
  run the gate / check code quality / pre-commit self check / quality gate, 跑一下门禁, 检查代码质量,
  提交前自检, 质量检查. Red lines: never trim the default suite, report red as red.
---

# Quality gate

Source of truth: root AGENTS.md (Verification), the nearest module AGENTS.md, and .github/workflows/ci.yml (what CI runs). This skill is the run order.

## Step 1: the core three (every change)
```bash
pnpm typecheck                                   # plugins:sync + tsc over the workspace (skips apps/client)
pnpm lint                                        # check-plugin-boundaries + eslint + prettier on apps/ packages/ plugins/
TEST_DATABASE_URL=<loopback db named *test*> pnpm test   # unit + db + db-commit
```
- lint failures: `pnpm lint:fix`, then rerun `pnpm lint`.
- Iterate with `pnpm test:unit` (no PostgreSQL) or `pnpm test:db`; run full `pnpm test` before handoff and never trim it.
- TEST_DATABASE_URL must be a loopback database with test or e2e in its name (one per worktree, e.g. greenhouse_test_<slug>); tune with VITEST_UNIT_MAX_WORKERS / VITEST_DB_MAX_WORKERS.

## Step 2: gates by change surface
- Auth, permissions, isolation, proxy or MCP: `DATABASE_URL=<migrated loopback e2e db> pnpm test:e2e:ci` (tests/e2e, real HTTP, dead LLM endpoint).
- plugins/<id>, apps/api/src/plugin-host or the kit: `pnpm plugins:sync --check` and `TEST_DATABASE_URL=<…> pnpm test:core` (zero packages compiled, real boot); run them one after another, never beside other assembly or build commands.
- Kit export list changed: update apps/api/src/__tests__/extension-kit.snapshot.test.ts and add an `extension-kit:` CHANGELOG line.
- Fork overlay: `node scripts/check-extension-overlay.mjs --base upstream/main --strict` (paths stay in the seam, plugin imports stay public).
- Core schema: `./node_modules/.bin/drizzle-kit check`; schema-equivalence runs inside `pnpm test`.
- apps/client: `(cd apps/client && pnpm typecheck && pnpm lint)`, `pnpm test:unit apps/client` (includes src/theme/design-guard.test.ts), `pnpm test:e2e:client`, and `pnpm app:build` when the web export changes.
- Parallel worktrees running the client suite set CLIENT_E2E_API_PORT, CLIENT_E2E_WEB_PORT, CLIENT_E2E_DATABASE.
- apps/desktop: `pnpm desktop:check`.
- Shared tokens (packages/ui/src/tokens): `pnpm tokens:build`; never hand-edit generated tokens.
- Restricted runners that cannot launch Chromium only collect browser specs; say so in the report.

## Step 3: compliance scan (changed files only)
```bash
# server logs: no console.* outside CLI output
grep -rn "console\.\(log\|warn\|error\)" apps/api/src plugins --include="*.ts" | grep -v "\.test\." | grep -v "/cli[/.]"
# client isolation and banned APIs
grep -rn "from '@greenhouse/\|@react-navigation/\|KeyboardAvoidingView\|window\.confirm(\|window\.alert(" apps/client/app apps/client/src
# cross-package relative imports (tests and parity checks are exempt)
grep -rn "from '\(\.\./\)\{3,\}\(packages\|apps\|plugins\)/" apps packages plugins --include="*.ts" --include="*.tsx" | grep -v node_modules | grep -v "\.test\."
```
- CLI output (cli/, cli.ts, plugin command handlers) and text inside tool descriptions may mention console; everything else logs with logger.
- Server by hand: data through getDb() services or plugin service bags; chained routes without `: Hono`; no `any` in responses; model-bound input through sanitizeForPrompt(); error text names the next step and quotes values.
- Plugins by hand: imports only from @greenhouse/api/extension-kit, @greenhouse/types/*, @greenhouse/crud, @greenhouse/ui*, own files and declared dependencies; core never names a plugin id.
- Client by hand: surface per DESIGN.md (sheet/inspector, fixed DIALOG_SIZES); kit components; identity-bound writes; en and zh both updated; no React import in unit-tested modules.
- Intra-package Node ESM imports end in `.js`.

## Step 4: reuse and anti-entropy
- Server helpers come from @greenhouse/utils/* (date nowIso, json safeJsonParse/extractJson, concurrency runWithConcurrency, logger, crypto, error toErrorMessage/isUniqueViolation, id, semver, html escapeHtml, prompts); the client has its own in src/lib and src/data.
- Deletions cascade: orphaned components, helpers, types, copy keys, routes, nav entries, tests and docs go too.
- A second implementation of the same job is registered with its reason in the relevant AGENTS.md.
- No speculative abstractions, unused columns or "for later" hooks; hooks need a real consumer, Example coverage and seam tests.
- Declared capabilities work; unconfigured paths fail explicitly.

## Step 5: docs sync
- Core schema → packages/db/src/db-schema.md (+ packages/db/src/AGENTS.md for rules); plugin tables → plugins/<id>/db-schema.md.
- Profiles → apps/api/src/profiles/agent-profiles.md and profiles/AGENTS.md.
- Server conventions → apps/api/src/AGENTS.md.
- Client conventions → apps/client/AGENTS.md; design rules → apps/client/DESIGN.md.
- Plugin contract → EXTENDING.md + plugins/example + plugins/example/api/__tests__/seam.test.ts.
- A plugin's behavior → plugins/<id>/README.md and AGENTS.md.
- Desktop → apps/desktop/AGENTS.md; structure and cross-cutting rules → root AGENTS.md; behavior people see → README.md.

## Step 6: report
```
| Check | Status | Notes |
|---|---|---|
| typecheck | ✅/❌ | |
| lint (incl. plugin boundaries) | ✅/❌ | |
| test (unit/db/db-commit) | ✅/❌ | N passed, M failed |
| test:e2e:ci | ✅/❌/— | |
| plugins:sync --check / test:core | ✅/❌/— | |
| client typecheck + lint (apps/client) | ✅/❌/— | |
| test:e2e:client | ✅/❌/— | collected only? |
| desktop:check | ✅/❌/— | |
| compliance scan | ✅/❌ | |
| reuse / anti-entropy | ✅/❌ | |
| docs sync | ✅/❌ | |
```
- Report failures as failures; never skip or weaken a check to make the table green.

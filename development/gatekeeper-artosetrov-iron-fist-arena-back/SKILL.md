---
name: gatekeeper
description: |
  Привратник (Gatekeeper) — Pre-commit checklist. Verifies pbxproj, Prisma sync, subtree readiness, junk files, .env leaks, docs updates. Trigger: "preflight", "привратник", "gatekeeper", "ready to push?", "check before commit", "am I forgetting anything".
---

# Hexbound Preflight Checklist

You are running a pre-commit/pre-push verification for the Hexbound project. This is the "did I forget a step?" agent — it catches structural issues that would break builds or leave deployments out of sync.

## Scope

This agent owns **structural integrity**: pbxproj entries, Prisma sync, subtree reminders, junk files, .env leaks, docs updates, and a quick design-system sanity check on changed files only. It does NOT do:
- Deep SwiftUI code review → that's `guardian`'s job
- Deep TypeScript review → that's `oracle`'s job
- Full project builds → that's `blacksmith`'s job

The key distinction: preflight is fast and focused on "forgotten steps". The review agents go deep on code quality. Build-verify actually compiles things.

## How to Run

**Preferred: use the automated script:**
```bash
bash .skills/skills/gatekeeper/scripts/preflight_check.sh <project-root>
```

The script handles everything below automatically. Only fall back to manual checks if the script isn't available or you need to investigate a specific failure.

**Manual fallback:**

1. Get the list of changed files:
   ```bash
   git diff --name-only HEAD
   git diff --cached --name-only
   ```

2. Run through each checklist section below, checking only what's relevant.

## Checklist

### 1. Xcode Project File (FULL AUDIT — not just new files!)

**Scan ALL .swift files on disk**, not just new ones. Files can exist on disk but be missing from pbxproj — they won't compile, causing "Cannot find X in scope" errors in OTHER files.

```bash
# Full audit: find ALL .swift files missing from pbxproj
find Hexbound/Hexbound -name "*.swift" | while read f; do
  base=$(basename "$f")
  count=$(grep -c "$base" Hexbound/Hexbound.xcodeproj/project.pbxproj)
  [ "$count" -lt 3 ] && echo "MISSING: $f ($count refs)"
done
```

For each file found missing, it needs entries in 4 sections: PBXBuildFile, PBXFileReference, PBXGroup children, PBXSourcesBuildPhase.

**Also check new files** as before:
```bash
basename="NewFile.swift"
grep -c "$basename" Hexbound/Hexbound.xcodeproj/project.pbxproj
```
Result < 3 = file will silently not compile.

**Known past incidents:** `ErrorStateView.swift` and `EmptyStateView.swift` existed on disk but were never added to pbxproj, causing cascading "Cannot find X in scope" build errors.

### 2. Prisma Schema Sync (if schema.prisma changed)

```bash
diff backend/prisma/schema.prisma admin/prisma/schema.prisma
```
If different → `cp backend/prisma/schema.prisma admin/prisma/schema.prisma`

Also check: was a migration created in `backend/prisma/migrations/`?

### 3. Admin Subtree Reminder (if admin/ changed)

After push, user must run:
```bash
git subtree push --prefix=admin admin-deploy main
```

### 3a. Merge Conflict Marker Scan (CRITICAL — after any merge/pull)

After `git merge` or `git pull`, **always** scan for leftover conflict markers before committing:

```bash
# Must return 0 results or commit will break builds
grep -rn "^<<<<<<<\|^=======\|^>>>>>>>" backend/ admin/ Hexbound/Hexbound/
```

**Past incident:** A merge with ~25 conflicts was committed via `git add -A` without resolving markers. `seed-dungeon-drops.ts` had `<<<<<<< HEAD` at line 330 → Vercel build failed with "Merge conflict marker encountered." Required a second fix commit.

Special cases:
- **`tsconfig.tsbuildinfo`** — auto-generated; remove only after confirming it is ignored/generated and not the user's work
- **Binary files** (`.png`, `.mp3`) — choose one version deliberately after previewing both sides; do not blindly apply ours/theirs
- **Seed scripts** (`seed*.ts`) — check `.finally()` blocks, a common conflict site

### 4. Junk Files & .env Leaks

```bash
# Junk files (macOS duplicates)
find backend admin Hexbound -name "* 2.*" -o -name "* 2" 2>/dev/null

# CRITICAL: Temp/backup files inside .xcodeproj bundle
ls Hexbound/Hexbound.xcodeproj/ | grep -E '\.(bak|backup|tmp)$'
# Should return NOTHING. If hits found, delete them:
rm -f Hexbound/Hexbound.xcodeproj/*.bak Hexbound/Hexbound.xcodeproj/*.backup Hexbound/Hexbound.xcodeproj/*.tmp*

# Editor config directories (should be in .gitignore, never committed)
git diff --cached --name-only | grep -E '^\.obsidian/|\.base$'
# Also check if staged changes include prototype HTML files
git diff --cached --name-only | grep -E '_prototype\.(html|jsx)$'

# .env files in staging
git diff --cached --name-only | grep '\.env'
```

**Why .obsidian/:** Obsidian config files leak local workspace state (bookmarks, graph positions, plugins). They were accidentally committed in `d0e7f3a` (2026-04-12). Now blocked by `.gitignore` — this check catches cases where `.gitignore` is bypassed via `git add -f`.

**Why:** Temp files inside `.xcodeproj` bundle (e.g., `project.pbxproj.backup`, `file.tmp1`) break Xcode's project parsing, causing "Couldn't load project" error even if they're not referenced in the pbxproj file. Clean bundle must only contain: `project.pbxproj`, `project.xcworkspace/`, `xcshareddata/`, `xcuserdata/`.

### 5. Design System Quick Check (changed view files only)

Run ONLY on changed `.swift` files in Views/:
```bash
# Hardcoded colors
grep -n 'Color(' <file> | grep -v 'DarkFantasyTheme' | grep -v '//'

# Missing await on get*Config()
grep -n 'get.*Config()' <file> | grep -v 'await' | grep -v '//'
```

This is a surface scan — flag obvious violations. Deep review is swift-review's job.

### 5b. Test Mock Parity (if shared game lib changed — 2026-04-15)

When any file in `backend/src/lib/game/` gains a new export, grep tests for mocks of that module and verify parity:

```bash
# Find test files that mock a shared lib module
grep -rn "vi.mock.*@/lib/game/<module>" backend/tests/ --include="*.ts"
# Compare real exports vs mocked exports — they must match
```

**Incident (2026-04-15 block-029):** `premium.ts` added `PREMIUM_ENTITLEMENT_USER_SELECT`. Vercel build went green; GitHub Actions vitest stayed red because two test files mocked `@/lib/game/premium` without the new export. The fix was a mechanical 2-line addition per test file.

**Rule:** Adding an export to any `src/lib/game/*.ts` file MUST be accompanied by updating all test mocks for that module in the same commit. No exceptions.

### 6. Documentation Updates

If behavior/schema/API/screens changed, check:
- New screen → `docs/07_ui_ux/SCREEN_INVENTORY.md`
- Schema change → `docs/04_database/SCHEMA_REFERENCE.md`
- API change → `docs/03_backend_and_api/API_REFERENCE.md`
- New rule discovered → `CLAUDE.md`
- **Balance constant added/changed in `backend/src/lib/game/balance.ts`** → run `npm run docs:balance` and commit the regenerated `docs/06_game_systems/BALANCE_CONSTANTS_AUTO.md` in the same change. CI `npm run docs:balance:check` is blocking — failing twice in one day (2026-04-19, commits `049dd2f` + `3630a15`) means this belongs on the preflight checklist.

### 6b. CI Workflow Path Filters (if `.github/workflows/*.yml` changed)

When any workflow file under `.github/workflows/` is modified, verify every `paths:` / `paths-ignore:` entry resolves to a real file or directory in the repo. A stale trigger path silently disables the workflow — CI goes green because nothing ran, not because the check passed.

**Check:**
```bash
# For each path glob in the changed workflow, confirm it maps to something real
awk '/paths:/,/^$/' .github/workflows/ci.yml | grep -E '^\s+-' | sed 's/^\s*-\s*//; s/^["'\''"]//; s/["'\''"]$//'
# Then ls each one
```

**Incident (2026-04-19, commit `40617f0`):** `.github/workflows/ci.yml` still triggered on `docs/04_BALANCE/**` after the folder was renamed to `docs/06_game_systems/`. The `docs:balance:check` job simply never ran on balance doc edits until the path was fixed.

### 6c. Post-Restore Static-Catalog Audit (if DB was restored from snapshot)

Snapshot restores have silently wiped seed-only "static catalog" tables **four** times now:

| Date | Table | Symptom |
|---|---|---|
| 2026-04-11 | Gold Mine config rows | prod 500s on `/gold-mine/*` |
| 2026-04-13 | Stash config rows | Stash screen empty, blocked release |
| 2026-04-19 | `user_roles` (Degon admin role) | Admin panel silently locked out |
| 2026-04-20 | `appearance_skins` | "Choose Your Appearance" step dead-locked; Next button permanently disabled |

**Root cause pattern:** static catalogs populated by hand or by a one-off SQL script are NOT in any idempotent seed that runs after restore — the snapshot is the only copy, and an older snapshot doesn't have them.

**Rule:** every static-catalog table must have an idempotent seed backed by BOTH (a) a `.sql` migration for prod / staging with `ON CONFLICT (...) DO NOTHING` or equivalent, AND (b) a TypeScript seed under `backend/prisma/seed-*.ts` for local dev. Source of truth (PNG files, JSON catalog, etc.) must be referenced in a comment at the top of both files.

**Post-restore checklist (run AFTER any snapshot-based DB restore):**
```bash
# 1. Row counts for known-at-risk catalogs — all must be > 0
psql "$DATABASE_URL" -c "SELECT 'appearance_skins' AS t, count(*) FROM appearance_skins
  UNION ALL SELECT 'game_config (item_balance.*)', count(*) FROM game_config WHERE category='item_balance'
  UNION ALL SELECT 'item_balance_profiles', count(*) FROM item_balance_profiles
  UNION ALL SELECT 'seasons', count(*) FROM seasons
  UNION ALL SELECT 'battle_pass_rewards', count(*) FROM battle_pass_rewards
  UNION ALL SELECT 'dungeons', count(*) FROM dungeons
  UNION ALL SELECT 'dungeon_bosses', count(*) FROM dungeon_bosses
  UNION ALL SELECT 'boss_abilities', count(*) FROM boss_abilities
  UNION ALL SELECT 'dungeon_drops', count(*) FROM dungeon_drops;"

# 2. Admin-role spot check — at least one user must still have role='admin'
psql "$DATABASE_URL" -c "SELECT count(*) FROM users WHERE role='admin';"

# 3. Re-run idempotent seeds defensively (all are safe to re-run):
psql "$DATABASE_URL" -f backend/prisma/migrations/20260420_seed_appearance_skins/migration.sql
psql "$DATABASE_URL" -f backend/prisma/migrations/20260421_seed_balance_constants/migration.sql
psql "$DATABASE_URL" -f backend/prisma/migrations/20260421_seed_dungeons/migration.sql
psql "$DATABASE_URL" -f backend/prisma/migrations/20260421_seed_battle_pass_season/migration.sql
psql "$DATABASE_URL" -f backend/prisma/migrations/20260421_seed_dungeon_drops/migration.sql
# ... plus whichever other seeds were flagged by step 1

# 4. Re-apply admin roles (per-user state, not a catalog):
psql "$DATABASE_URL" -f scripts/restore-admin-roles.sql
```

**When adding a new static-catalog table** — it MUST land with an idempotent `.sql` migration AND a `seed-*.ts`, both labelled with "source of truth" pointer. Do NOT rely on ad-hoc `INSERT` scripts, MCP one-shots, or admin-UI entry.

**Large catalogs — use a generator, not hand-maintenance.** When the SQL mirror would exceed ~500 lines, or when the TS source has nested structure (lookup tables, per-row computed fields, ability catalogs), do NOT hand-maintain both the `.ts` and the `.sql`. Instead add `scripts/gen_<table>_sql.py` (or `.ts`) that reads the TS source and emits the idempotent SQL. The `.ts` is the source of truth; the `.sql` is regenerated on every edit. Header comment of the seed-*.ts must spell out the regen command (see `seed-dungeons.ts` referencing `python3 scripts/gen_dungeons_sql.py > backend/prisma/migrations/20260421_seed_dungeons/migration.sql`). Reason: 2026-04-21 dungeons seed was 765 lines / 7 dungeons × 70 bosses × ~250 abilities — drift between two hand-written copies was guaranteed.

**Admin-role re-apply:** `scripts/restore-admin-roles.sql` is the canonical post-restore admin re-promotion. When a new admin is granted in prod, add their email to that script in the same commit — git history is the source of truth for "who is admin", not Supabase row state.

Related memories: `feedback_snapshot_restore_admin_role.md`, this week's Appearance Skins incident (2026-04-20).

### 7. Assets (if new images added)

- Image in `.imageset` folder inside `Assets.xcassets`
- `Contents.json` with correct filename, idiom, scales
- Audio/resource files (not xcassets) → need pbxproj entry

## Output Format

```
# Preflight Report

## Changed Files
- [list]

## ✅ Passed
- [x] pbxproj — all entries present
- [x] Schema sync — identical

## ❌ Blockers
- [ ] 2 junk files found → delete them
  → confirm the duplicate is unreferenced, then remove the exact duplicate file/directory only

## ⚠️ Reminders
- After push: git subtree push --prefix=admin admin-deploy main
- Update SCREEN_INVENTORY.md for new DungeonView

## Verdict: READY TO COMMIT / NEEDS FIXES
```

## As a Subagent

When invoked as a subagent, run `scripts/preflight_check.sh` first, then supplement with manual checks for things the script doesn't cover (docs updates, asset validation). Start with `⛔ BLOCK` if there are build-breaking issues, or `✅ CLEAR` if everything passes.

## Auto-Trigger Rules

The parent agent may run this as a subagent only when the user explicitly requested subagents/parallel agent work and the current environment permits delegation:
- Before any `git commit` operation
- After completing a feature or bugfix task
- When the user says "done", "finished", "ready to push"

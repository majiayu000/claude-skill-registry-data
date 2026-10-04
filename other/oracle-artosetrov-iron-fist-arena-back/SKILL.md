---
name: oracle
description: |
  Оракул (Oracle) — Backend code reviewer. Reviews TypeScript/Prisma code for type safety, async correctness, schema sync. Trigger: "review backend", "проверь API", "оракул", "oracle", "check types", "TypeScript errors", Prisma schema changes.
---

# Hexbound Backend Review

You are reviewing TypeScript code in the Hexbound backend (Next.js API routes, Prisma models, game logic) and/or admin panel. Your job is to catch type errors, async bugs, schema mismatches, and rule violations before they hit Vercel deploys.

## Scope

This agent owns **TypeScript/Prisma code quality**: type safety, async correctness, schema integrity, game logic validation. It does NOT check:
- Prisma schema sync between backend/admin → that's `gatekeeper`'s job
- Actual `npx next build` → that's `blacksmith`'s job
- SwiftUI code → that's `guardian`'s job

## Before You Start

**Step 1:** Run the automated scanner first:
```bash
bash .skills/skills/oracle/scripts/check_async_await.sh <path-to-file-or-dir> <project-root>
```

**Step 2:** Read these files for current ground truth:
1. **CLAUDE.md** — project root. Master rules.
2. **backend/prisma/schema.prisma** — the single source of truth for DB schema.
3. If reviewing admin code, also check **admin/prisma/schema.prisma** — it must be identical to backend's.
4. **docs/03_backend_and_api/API_REFERENCE.md** — if reviewing API routes.
5. **docs/06_game_systems/BALANCE_CONSTANTS.md** — if reviewing game logic.

**Step 3:** Use scanner output as a baseline, then do deeper manual review for logic bugs, server-authority violations, and game enum correctness.

## What to Check

### 1. TypeScript Strict Mode

- **Null safety.** When a function returns `T | null`, the type MUST be narrowed before property access. `if (!x) throw` then use `x` — or `guard`-style pattern.
- **Prisma Json fields.** Must use double cast: `as unknown as ConcreteType[]`. Direct cast fails in strict mode.
- **No `any` without justification.** Flag untyped variables, parameters, return values.
- **Hoisted `let X: T | null = null` loses narrowing inside async closures.** If a route file declares `let character_id: string | null = null` outside the try/catch (typically for catch-block recovery) and then narrows it with `if (!character_id) return 400`, the narrowing DOES NOT survive across the `prisma.$transaction(async (tx) => { ... })` closure boundary or across any `await` that could theoretically allow reassignment. Prisma typed calls inside the closure will fail with `Type 'string | null' is not assignable to type 'string | undefined'`. **Fix pattern:** after the guard, capture into const with explicit type: `const charId: string = character_id`, `const invId: string = inventory_id`. Use the const inside the closure. Leave the hoisted `let`s for the catch-block. **Incident:** `src/app/api/inventory/equip/route.ts:59` failed Vercel build on commit `874effd` (2026-04-11) — the hoisted `let character_id` was used inside `tx.character.findUnique({ where: { id: character_id }})` instead of a const capture.
- **Scanner check:** `grep -A20 'let .*: string | null = null' <route>` — if the same variable appears inside `prisma.$transaction(async` body without a const re-capture between the guard and the closure, flag it.
- **No `ignoreBuildErrors`.** This flag is removed. TypeScript errors block Vercel deploy. Do not reintroduce it.

### 2. Async Correctness

- **All `get*Config()` in `src/lib/game/live-config.ts` are async.** Missing `await` produces `Promise<number>` instead of `number`. This is the #1 backend bug pattern.
- **`runCombat()` in `combat.ts` is async.** Always `await runCombat(attacker, defender)`. Without `await`, TS reports "property 'winnerId' does not exist on type 'Promise<CombatResult>'".
- **`calculateCurrentStamina()` in `stamina.ts` is async, takes 3 args** — `(currentStamina, maxStamina, lastUpdate)`. Returns `Promise<StaminaResult>` where `StaminaResult = { stamina: number; updated: boolean }`. Do NOT pass REGEN_INTERVAL_MS as 4th arg. Use `.stamina` on the result, NOT `.current`.
- **General rule: before calling ANY game lib function, open its source file and check the signature.** Verify: is it async? arg count? return type field names? Guessing causes repeated Vercel build failures.
- **Prisma queries are async.** Every `prisma.xxx.findMany()`, `.create()`, etc. must be awaited.
- **Error handling.** API routes should have try/catch. Unhandled promise rejections crash the server.
- **⚠️ Promise.all() exception:** Async calls inside `Promise.all([...])`, `Promise.allSettled([...])`, or `Promise.race([...])` do NOT need individual `await`. Promise.all resolves them. The scanner now excludes these, but verify manually if in doubt.

### 3. Prisma Schema Sync

If `backend/prisma/schema.prisma` was modified:
- Was the migration created? (`npm run db:migrate:dev -- --name xxx`)
- Was the schema copied to admin? (`cp backend/prisma/schema.prisma admin/prisma/schema.prisma`)
- Are both files identical? If not, CI will fail.
- Was `prisma generate` run? Without it, TS reports false errors for Prisma models.

### 3a. Prisma Model Verification (CRITICAL — anti-false-positive)

**NEVER claim a Prisma model is "missing" without verifying.** The schema is large and uses camelCase model names that map to snake_case table names.

Before flagging `prisma.xxx` as missing:
1. Read the FULL `backend/prisma/schema.prisma` (not just the first 100 lines)
2. `grep -i "model.*xxx" backend/prisma/schema.prisma` — case-insensitive search
3. Check for `@@map("table_name")` — the model name in code may differ from the table name
4. Check Prisma client mapping: `model DailyGemCard` → `prisma.dailyGemCard` (automatic camelCase)

**Known past incident (2026-03-21):** Oracle falsely flagged 17 models as missing (dailyGemCard, mailRecipient, questDefinition, shopOffer, featureFlag, etc.) — they were ALL present in the schema. The scanner read only a portion of the file and didn't account for Prisma's automatic camelCase mapping.

### 3b. Shared Wallet Model (CRITICAL — 2026-04-09)

Gold and gems live on the **User** model, NOT on Character. This is the "shared wallet" pattern — one wallet per account, shared across all characters.

**Banned patterns:**
- `character.gold` — WRONG (field removed from Character model)
- `character.gems` — WRONG (field removed from Character model)
- Updating gold/gems via `prisma.character.update({ data: { gold: ... } })` — WRONG

**Correct patterns:**
- `user.gold` / `user.gems` — read from User
- `prisma.user.update({ where: { id: user.id }, data: { gold: ... } })` — update on User
- API responses that return character data must inject `gold`/`gems` from User for iOS decode compatibility

**Known exception:** `character.goldMineSlots` is a DIFFERENT field (mine capacity, not currency) and remains on Character.

**Root cause (2026-04-09):** Migration from character-level to user-level wallet caused 10+ routes to break. 6 separate fix commits were needed to clean up all references.

### 4. Server-Authoritative Rule

The client must NOT calculate: combat results, reward amounts, rating changes, economy values, or balance formulas. These must be server-side only. If you see game logic that should be server-authoritative on the client side — flag it.

### 5. Game Enums Correctness

Verify any enum values used match the actual backend enums:
- **CharacterClass**: `warrior`, `rogue`, `mage`, `tank` (NOT paladin, NOT archer)
- **CharacterOrigin**: `human`, `orc`, `skeleton`, `demon`, `dogfolk` (NOT elf, NOT dwarf)
- **ItemType**: `weapon`, `helmet`, `chest`, `gloves`, `legs`, `boots`, `accessory`, `amulet`, `belt`, `relic`, `necklace`, `ring`, `consumable`
- **ItemRarity**: `common`, `uncommon`, `rare`, `epic`, `legendary`
- **DamageType**: `physical`, `magical`, `true_damage`, `poison`

### 6. Shared Lib Module Contracts (CRITICAL — 2026-04-15)

**Test mock drift** is the top source of CI-green-but-CI-red states (Vercel passes, GitHub Actions fails).

- When a shared game lib (e.g. `src/lib/game/premium.ts`, `src/lib/game/reward-grants.ts`) gains new exports, ALL test files that mock that module **must** be updated simultaneously.
- **Grep for stale mocks:** `grep -rn "@/lib/game/<module>" backend/tests/ --include="*.ts"` — check each mock's `vi.mock(...)` shape against the real module exports.
- **Incident (2026-04-15 block-029):** `premium.ts` added `PREMIUM_ENTITLEMENT_USER_SELECT`. Both `pvp-resolve.test.ts` and `dungeon-rush-resolve.test.ts` mocked `@/lib/game/premium` without it → 500 inside tests → CI red while Vercel was green.
- **Rule:** After adding any export to a shared lib, always run: `grep -rn "vi.mock.*<module>" backend/tests/ --include="*.ts"` and update every matching mock.

**Reward type widening → Vercel build failure** is the top backend type bug pattern after the shared `RewardGrantEntry` contract was introduced.

- `RewardGrantEntry` type is: `{ type: 'gold' | 'gems' | 'xp' | 'item' | 'consumable'; id?: string | null; quantity: number }`.
- Route-local helpers that return `{ type: string; ... }[]` will fail TypeScript when passed to `grantRewardEntries(...)`.
- **Scanner pattern:** `grep -rn "type: string" backend/src/app/api/shop/ --include="*.ts"` — flag any reward-shaped object using a raw `string` type instead of the shared union.
- **Incident (2026-04-15 block-028):** `shop/contraband` `generateLoot()` returned `{ type: string }[]` → Vercel build blocked.
- **Fix pattern:** `import type { RewardGrantEntry } from '@/lib/game/reward-grants'` and annotate the helper return type explicitly.

### 7. File Hygiene

- **No files with spaces or " 2" in names.** macOS sometimes creates these duplicates. Delete them.
- **No orphaned imports.** Unused imports should be removed.
- **Build must pass.** Mentally trace whether `npx next build` would succeed with these changes.

### 8. Admin React Async State (CRITICAL — 2026-04-16)

Mutation handlers in admin React components that control a loading flag (`isMutating`, `isLoading`, `isDeleting`, `isCreating`) MUST reset the flag via `finally`, not only on the success path.

**Anti-pattern (broken — UI gets stuck after a thrown error):**
```tsx
setIsMutating(true)
const result = await someServerAction(...)
setIsMutating(false)  // ← never resets if serverAction throws
```

**Correct pattern:**
```tsx
setIsMutating(true)
try {
  const result = await someServerAction(...)
  // handle success
} catch (e) {
  console.error('Action failed:', e)
  toast.error('Something went wrong')
} finally {
  setIsMutating(false)  // ← always resets, even on thrown error
}
```

**Incident (2026-04-15/16, blocks 061-068):** Found in 10+ admin pages — generic CRUD shell, live editors, config, players, items, snapshots, skills, balance. Any thrown server action left the admin screen permanently stuck in loading/spinner state. Applied as a systematic fix across all affected files.

**Scanner pattern:** `grep -rn "setIs[A-Z]" admin/src/ --include="*.tsx" -A 8` — flag any handler that sets `isSomething(true)` without a `} finally {` block following it.

### 9. Auth Route Hardening

**9a. No hardcoded backend URLs.**
Auth and API routes MUST NOT contain hardcoded non-production backend origins. The canonical production API origin is `api.hexboundapp.com`. Any reference to legacy Vercel preview URLs (e.g. `iron-fist-arena-backend.vercel.app`, `*.vercel.app` for backend calls) is a stale fallback that will silently hit the wrong server.

**Scanner pattern:** `grep -rn "vercel\.app\|iron-fist\|localhost:3000" backend/src/ --include="*.ts"` — flag any hardcoded URL that isn't the canonical `api.hexboundapp.com` or a local test constant.

**Incident (2026-04-17, block 187):** `forgot-password/route.ts` contained `iron-fist-arena-backend.vercel.app` as a fallback host. The route constructed reset URLs pointing at the wrong server in environments where `NEXTAUTH_URL` was not set.

---

**9b. Email-collision 409 guards in auth routes.**
Any route that performs `prisma.user.update({ where: { email } })` or `prisma.character.update({ data: { email } })` where `email` is not guaranteed unique MUST have an explicit duplicate-email guard returning `409` **before** the Prisma call. Without it, Prisma raises a generic `P2002` unique-constraint error that surfaces as an opaque 500.

**Correct pattern:**
```ts
const existing = await prisma.user.findFirst({ where: { email: newEmail } })
if (existing) return NextResponse.json({ error: 'email_conflict' }, { status: 409 })
// then proceed with update
```

**Incident (2026-04-17, blocks 189-190):** Both `/auth/link-account` and `/auth/sync-user` were missing the pre-flight email uniqueness check. On duplicate email the routes fell through to a Prisma constraint failure (P2002) which was surfaced as a 500 instead of a meaningful 409. Fixed with explicit pre-flight guards in both routes.

---

**9c. Supabase auth revert completeness (CRITICAL — 2026-04-18).**
When a route mutates the Supabase user (`auth.admin.updateUserById`) and then the downstream Prisma update fails, the revert path MUST restore **all** fields that were changed in Supabase — not just `user_metadata`. Reverting only metadata while leaving email/password/email_confirm in a half-upgraded state causes Supabase ↔ Prisma drift that persists until manually fixed.

**Correct revert pattern for upgrade-guest:**
```ts
const revertPayload = {
  user_metadata: { is_guest: true, username: undefined }
}
if (dbUser.email) {
  revertPayload.email = dbUser.email          // restore original email
  revertPayload.password = crypto.randomUUID() // invalidate the user's new credentials
  revertPayload.email_confirm = true           // keep account usable as guest
}
await supabase.auth.admin.updateUserById(user.id, revertPayload)
```

**Rule:** Any route with a Supabase mutation + Prisma write pattern must have a revert block. Grep for `auth.admin.updateUserById` — if the catch/revert block only patches `user_metadata`, it is incomplete.

**Incident (2026-04-18):** `upgrade-guest/route.ts` reverted only `user_metadata`. After a Prisma failure, the Supabase row retained the new email and password, making the account unreachable from the guest session. Fixed in commit `748f35d`.

---

**9d. Admin route role granularity — game-config writes (CRITICAL — 2026-04-18).**
`getAdminUser()` succeeds for all three roles: `admin`, `developer`, `moderator`. Write endpoints on game-config routes must use `canModifyConfig(admin.role)` from `admin/src/lib/auth.ts`, which restricts to `admin` + `developer` only. GET endpoints remain open to all roles.

**Banned pattern (moderators get write access):**
```ts
const admin = await getAdminUser()
if (!admin) return 401
// proceed to write — moderators can mutate balance config!
```

**Correct pattern:**
```ts
const admin = await getAdminUser()
if (!admin) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
if (!canModifyConfig(admin.role)) {
  return NextResponse.json({ error: 'Insufficient permissions — admin or developer role required' }, { status: 403 })
}
// proceed to write
```

**Affected route categories:** item-balance, items, dungeons, seasons, events, dungeon-map-layout, passives, passives/connections, skills. IAP and user-role mutation routes are already stricter (`requireStrictAdmin`).

**Scanner pattern:** `grep -rn "export async function POST\|PUT\|PATCH\|DELETE" admin/src/app/api/admin/ --include="*.ts" -l` — for each file, check that write handlers call `canModifyConfig` (or `requireStrictAdmin`) and not just `getAdminUser`.

**Incident (2026-04-18):** Moderator role could mutate all balance config, items, seasons, events, dungeons. Fixed systematically across 10 route files in commit `abf2066`.

### 10. Analytics Pattern (2026-04-18)

Analytics events fire from server-authoritative call-sites (never client). Two rules:

**10a. Fire-and-forget only — never block the request.**
```ts
// CORRECT — fire-and-forget after the main transaction commits
void analyticsBackend.track('event_name', { ...payload })

// WRONG — awaiting analytics can delay or block the response
await analyticsBackend.track('event_name', { ...payload })
```

**10b. Call-site placement** — events must fire AFTER the Prisma transaction/commit, never inside it. Placing inside a transaction means a failed event causes a transaction rollback.

**Introduced in commit `1f5d297` (2026-04-18):** 7 critical-funnel events: `signup`, `first_pvp`, `iap_purchase`, `bp_claim`, `daily_login`, `level_up`, `shop_upgrade`. New backend: `src/lib/analytics.ts` + `NoopBackend` (swap via `setAnalyticsBackend()`). iOS: `Services/AnalyticsService.swift` mirrors the same 7 events.

### 11. Defensive Reads + Lazy Supabase Init (2026-04-19)

**11a. Lazy-init Supabase clients on prerender-reachable pages.**
Next.js prerender executes page module code at build time. A top-level `const supabase = createClient(process.env.SUPABASE_URL!, ...)` will crash the build with "supabaseUrl is required" if either env var is missing (even when the page never renders at build time). Auth pages such as `/reset-password` MUST construct the client inside the component/handler body, not at module scope.

**Banned pattern (module-scope):**
```ts
const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, ...)
export default function Page() { ... }
```

**Correct pattern (lazy):**
```ts
function getSupabase() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  if (!url || !anonKey) return null  // let the page handle missing env gracefully
  return createClient(url, anonKey)
}
export default function Page() { const supabase = getSupabase(); ... }
```

**Incident (2026-04-19, commit `e2b5185`):** `backend/src/app/reset-password/page.tsx` held a module-scope Supabase client. Next's prerender pass crashed when env vars were absent, blocking the entire Vercel build.

**Scanner pattern:** `grep -rn "createClient(" backend/src/app --include="*.tsx" --include="*.ts"` — flag any hit that sits outside a function body.

---

**11b. Raw-SQL fallback for user-critical read paths.**
When a single Prisma `findMany` serves a boot-critical screen (character list, hub bootstrap, arena splash), wrap it in a typed raw-SQL fallback so the screen still loads when the generated Prisma client is transiently out of sync with the live schema (between migration apply and Vercel redeploy).

**Pattern:**
```ts
async function fetchRows(userId: string): Promise<Row[]> {
  try {
    return await prisma.character.findMany({ where: { userId }, select: {...} }) as Row[]
  } catch (error) {
    console.warn('prisma read warning, retrying with raw SQL:', error)
  }
  return prisma.$queryRaw<Row[]>`SELECT c.id, c.user_id AS "userId", ... FROM characters c WHERE c.user_id = ${userId}`
}
```

Use `Promise.allSettled` for downstream fan-outs (per-row regen, enrichment) so one bad row cannot black out the whole list.

**Introduced in commits `16fe0b5` + `0658532` (2026-04-19)** after character list started 500-ing for some users post-migration. The fallback is defensive only — root cause is still schema/Prisma client drift; the fallback just keeps the app usable while drift is resolved.

**Do not blanket-apply:** reserve for read endpoints whose failure blocks the app from booting. Write endpoints must still fail loud.

---

**11c. Grep downstream consumers when a required column becomes nullable.**
When `schema.prisma` flips a column from required to optional (`field String` → `field String?`), the Prisma client types flip from `T` to `T | null` for every consumer. Any admin/backend code that dereferences the field without a null-check becomes a Vercel-build-blocker.

**Checklist after any `required → nullable` change:**
```bash
# Replace <Model> and <field> with the changed ones:
grep -rn "\.<field>" admin/src backend/src --include="*.ts" --include="*.tsx"
```
Then null-check every call site.

**Incident (2026-04-19, commit `ed3001d`):** `PvpMatch.player2Id` became nullable to support bot/boss matches. Admin `/matches` page dereferenced `match.player2.characterName` directly → admin build failed tsc. Fix was a small `match.player2?.characterName ?? '—'` patch, but the issue was caught only by tsc, not by gatekeeper preflight — running the grep earlier would have caught it before push.

---

**11d. FK-safe split for synthetic opponent ids (bots, dungeon bosses).**
When an endpoint persists a "winner / loser" (or any attacker/defender) pair to a table whose `*_id` column has a foreign-key constraint on `characters.id`, the id written to the DB MUST be a real `characters.id`. Bot and dungeon-boss opponents live only in the `opponentSnapshot` JSON — their `id` is synthetic (`bot-...`, `boss-...`) and has no row in `characters`, so any direct write triggers the FK constraint.

**Rule:** keep two id pairs when persisting combat results:
- `winnerId` / `loserId` — synthetic-OK, used only in the JSON response to iOS (which compares by equality)
- `winnerCharacterId` / `loserCharacterId` — FK-safe, `null` when the side is a non-PvP synthetic opponent — used in the Prisma `update` / `create`

```ts
const winnerId = attackerWon ? attacker.id : defenderProxy.id            // response
const loserId  = attackerWon ? defenderProxy.id : attacker.id            // response
const winnerCharacterId = attackerWon ? attacker.id : (isPvp && defender ? defender.id : null)  // DB
const loserCharacterId  = attackerWon ? (isPvp && defender ? defender.id : null) : attacker.id  // DB

await prisma.pvpMatch.update({
  data: { winnerId: winnerCharacterId, loserId: loserCharacterId, ... }
})
```

**Incident (2026-04-20, commit `f27e3d6`):** `/api/pvp/match/complete` wrote `defenderProxy.id` to `pvp_matches.winner_id` / `loser_id` for bot / dungeon-boss opponents. Every bot fight ended with a 500 "Failed to complete match" after the last round. Prod required manual `UPDATE pvp_matches SET status='abandoned'` on two stuck `in_progress` rows via Supabase MCP.

**Grep check** — any route that updates a `pvp_matches` / `pve_matches` / similar table with both a real character id and a synthetic-possible id:
```bash
grep -rn "winnerId\|loserId\|winner_id\|loser_id" backend/src/app/api --include="*.ts"
# For each hit on a Prisma create/update, confirm the value comes from a FK-safe variable, not directly from a *Proxy object.
```

Related memory: `feedback_bot_synthetic_ids_fk.md`. Related rule: **11c** (nullable FK columns need null-checks everywhere). If you add a new `isPvp === false` branch to a combat route, audit the Prisma write sites FIRST.

### 12. Deploy Awareness

If changes touch admin/:
- Remind about `git subtree push --prefix=admin admin-deploy main` after pushing to origin.

If changes touch backend/:
- Backend auto-deploys on push to origin/main. No extra step needed.
- But if schema.prisma changed → admin schema must be synced.
- If `backend/src/lib/game/balance.ts` changed → run `npm run docs:balance` and commit `docs/06_game_systems/BALANCE_CONSTANTS_AUTO.md` in the same change. CI `docs:balance:check` blocks otherwise. (Two repeats on 2026-04-19, commits `049dd2f` + `3630a15`.)

### 13. Pure-Function Game-Math Handlers (2026-04-29)

When game-math (damage, heals, shields, drop chance, rating delta, etc.) lives inside a route handler with side effects, **extract it into a pure-function module under `backend/src/lib/game/`** and pin behavior with vitest. The route file keeps request shape, persistence, and AI selection; the helpers stay stateless and parameter-only.

**Reference incident:** commit `6b1199` (2026-04-29) extracted `applyBurstDamage` / `applyShield` / `healAmountFromActive` / `shouldExecute` from `pvp/strike/route.ts` into `backend/src/lib/game/active-handlers.ts` + 131-line `tests/lib/active-handlers.test.ts`.

**Defensive clamp rule (CRITICAL):** every game-math helper that takes a balance-driven `magnitude` (or any fraction sourced from a seed/admin config) MUST clamp the input at `Math.max(0, magnitude)` before using it. A negative magnitude leaking through `update_seed_consumable_items`-style scripts would otherwise flip the math:
- `applyBurstDamage(d, -0.5)` → `0.5×d` instead of `1.5×d` (silent damage nerf, exploit if attacker can write the seed).
- `applyShield(d, -0.5)` → `1.5×d` (turns a shield into damage amplifier — the dangerous case).
- `healAmountFromActive(maxHp, -0.25)` → negative heal, then rounded → 0 (dropped).

The clamp at the function boundary kills all three vectors at once and is cheap. **Without** unit-test coverage of the negative case, a balance-pass typo in a seed has no guardrail.

**Review checklist:**
- New game-math helper accepts `magnitude` / `fraction` / `multiplier` from external config? → must `Math.max(0, x)` at entry.
- New helper has `> 0` HP/damage clamp on output? → confirms heal-from-shield and execute-on-zero invariants.
- Helper added without a vitest? → flag — every new lib in `src/lib/game/` should have a peer in `tests/lib/`.

### 14. Cache Key Versioning on Data-Shape Migrations (2026-05-02)

Any cached endpoint that returns rows whose **shape or geometry** is changed by a Prisma migration MUST bump its cache key version in the same PR. Otherwise warm Vercel caches keep serving the pre-migration payload (stale coords, stale shape, stale enums) and clients render against a contract that no longer exists in the DB.

**Pattern (CORRECT):**
```ts
// /api/passives/tree/route.ts
const CACHE_KEY = "passives:tree:v5"  // bumped from v4 alongside 20260501_repos_passive_positions_for_lane_layout
```

**Reference incident:** commit `18ac4fa` (2026-05-02). The lane-grid migration `20260501000000_repos_passive_positions_for_lane_layout` rewrote `(x, y)` for all 83 passive nodes. `/api/passives/tree` cache key was bumped `v4 → v5` in the same commit; without the bump, iOS would have rendered new node positions read from the old cached coords and overlapped half the canvas.

**Review checklist:**
- PR includes a Prisma migration that mutates row content (`UPDATE …`, `ALTER … SET DEFAULT …`, enum value rename)?
- Any route under `backend/src/app/api/**` references that table behind a `CACHE_KEY` / `revalidate` / `unstable_cache` boundary?
- If yes — was the cache key string version-bumped in the same commit? If no — flag as **High** priority.
- Soft-deletes (`is_active = FALSE` on legacy rows) count as shape-changing for any endpoint whose query doesn't already filter on the flag.

**Companion rule:** when a route returns a superset (e.g. nodes for ALL classes) and the client was previously narrowing client-side, the migration that adds rows must also be paired with a server-side filter or an explicit "client must filter" note in `API_REFERENCE.md`. The 2026-05-02 PR added `PassiveTreeViewModel.filter(by: classRestriction)` for exactly this reason; documenting the contract prevents the next consumer from forgetting.

## Output Format

```
## [filename.ts]

✅ Strengths:
- [what's done well]

❌ Issues:
1. **[Category]** Line N: [what's wrong] → [how to fix]
   Priority: Critical / High / Medium / Low

⚠️ Deploy Notes:
- [any deploy steps needed for these changes]
```

## As a Subagent

When invoked as a subagent, the caller should pass:
- Which files to review
- Whether schema changes are involved

Start response with `⛔ CRITICAL` if there are type errors that would block the build, or `⚠️ DEPLOY STEPS NEEDED` if there are required post-merge actions.

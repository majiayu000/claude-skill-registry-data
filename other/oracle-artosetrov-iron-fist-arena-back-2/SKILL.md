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

### 9. Deploy Awareness

If changes touch admin/:
- Remind about `git subtree push --prefix=admin admin-deploy main` after pushing to origin.

If changes touch backend/:
- Backend auto-deploys on push to origin/main. No extra step needed.
- But if schema.prisma changed → admin schema must be synced.

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

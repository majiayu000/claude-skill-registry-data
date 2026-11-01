---
name: backend-game-data
description: Change CampusCove persistent game data in the Laravel + PostgreSQL backend — new item or item kind, shop entry, housing rule, coins/economy, keys, ownership, a new API endpoint for the game, and its feature test. Use whenever a gameplay feature must be saved, paid for or enforced server-side.
---

# CampusCove backend game data

Laravel in `backend/`, run in Docker (no local PHP needed): every artisan call goes through
`docker compose exec -T backend php artisan ...` (the Makefile's `$(ART)`). Auth model is `Account`
(`$request->user()`), Sanctum tokens, Postgres 16.

## Domain map

| Concern | Code |
|---|---|
| Items | `ItemDef` (`item_defs`: `code`, `kind` enum `item_kind`, `model_glb`, `preview_image`, `bind`, `tradable`, `premium_only`), `AccountInventoryService::grantItem / revokeItem / accountHasPositiveQuantity` |
| Shop | `ShopSeeder` (catalogue is the source of truth; `make seed-shop` resyncs it), `ShopPurchaseService` |
| Money | `wallet_ledger` (balance = SUM of deltas, no balance column), `CoinRewardService` for every new coin source, `WalletSummaryService` |
| Housing | `HousingUnit`, `HousingService` (buy, daily property tax, seizure, keys, door lock), `HousingUnitSeeder` (10 houses, `model_key` = asset key) |
| Furniture | `ApartmentPlacementService` (`Room` / `RoomFurniture`) |
| Errors | throw a subclass of `ApiRejectedException($code, $message, $status)` — renders `{ message, code }`, shown as is by the front and forwarded by the socket |

Product rules (do not "fix"): premium skins never purchasable with coins; furniture is deleted when a house is
lost on purpose; no IP addresses stored; rewards come from actions, not passive income.

## Recipes

**New item / tool** (model `f9aefec` + `2026_10_26_151433_add_house_key_tool_item.php`):
1. Asset at `front/public/assets/items/<group>/<key>/{model.glb,preview.png}` (skill `blender-asset`).
2. Migration, idempotent: `public $withinTransaction = false;` when it adds an enum value, guarded by a
   `DO $$ ... IF NOT EXISTS (SELECT 1 FROM pg_enum ...) THEN ALTER TYPE item_kind ADD VALUE '...'` block; then
   `ItemDef::query()->firstOrCreate(['code' => ...], [...])` inside `DB::transaction`; backfill existing players
   only when `wasRecentlyCreated`; a real `down()`.
3. Sold items: entry in `ShopSeeder` too (codes must match `front/src/game/assets/catalog.ts`).

**New column / table**: standard migration named `YYYY_MM_DD_HHMMSS_<verb>_<what>.php`; expose it in the
service's array/resource only if the front or socket reads it (the socket reads housing units, e.g.
`interior_bounds`, `door_locked`, `key_holder_account_ids`).

**New endpoint**: route in `routes/api.php` inside the `auth:sanctum` + `account.active` group (admin under
`admin` prefix); thin controller returning `JsonResponse`, `$request->validate()`; logic in a `Services/` class
with multi-table writes in `DB::transaction()` and row locks (`lockForUpdate`) on wallet/ownership checks.
Front client in `front/src/api/<domain>.ts` through `apiRequest` (`api/http.ts`); never `fetch` directly.

## Test

Every behaviour change gets a feature test in `backend/tests/Feature/<Domain>ApiTest.php`:
`RefreshDatabase`, `SetsWalletBalance`, seed what you need in `setUp()`, the local
`registerAndCreditWallet($coins, 'coins')` helper (copied per test class) for an account + bearer token, then
`$this->postJson(..., [], ['Authorization' => 'Bearer '.$token])`. Assert the rejection code too
(`assertJsonPath('code', 'no_house_key')`), not only the happy path.

```bash
make test                                    # whole suite
docker compose exec -T backend php artisan test --filter=HousingApiTest
make migrate                                 # apply to the dev DB the running game uses
```

Known baseline (2026-10-26): 76 pass, 1 fails — `AdminShopApiTest` "admin can create…" needs the PHP GD
extension, missing from the backend Docker image. Any other failure is yours.

Useful dev commands for playtesting the change: `make set-money ACCOUNT=<id|email> CURRENCY=coins SUM=5000`,
`make set-admin EMAIL=...` (relog after), `make fill-outfit ACCOUNT=...`, `make collect-taxes`.

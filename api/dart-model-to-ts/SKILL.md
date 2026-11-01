---
name: dart-model-to-ts
description: Port Dart data models (classes with fromJson/toJson/copyWith, enums, sealed results) into TypeScript types plus tolerant parse functions, and Dart repositories into the @vidaxl/api style (ApiClient, ApiError, one class per repository, same method names). Use it when porting anything under lib/data/models or lib/data/repositories (or a model-like class inside a service or state file), when a parser needs to match a Dart fromJson exactly, or when adding an endpoint method to a repository.
---

# Dart models and repositories → `@vidaxl/api`

Targets: `lib/data/models/<x>.dart` → `packages/api/src/models/<x camelCase>.ts`;
REST repositories `lib/data/repositories/<x>_repository.dart` → `packages/api/src/repositories/<x>Repository.ts` (one class per file:
`admin_repository.dart` holds `AdminRepository`, `DemoRepository`, `SystemRepository` → three files). Firebase-SDK repositories
(`auth_repository.dart`) and local-storage ones (`history_repository.dart`) go to `apps/mobile/src/services/` instead.
`@vidaxl/api` imports nothing from React, React Native, Firebase or i18n.

Before writing anything, read what already exists: `packages/api/src/models/json.ts` (Dart-compatible JSON helpers),
`packages/api/src/client/apiClient.ts` (`ApiClient`, `ApiError`), and a finished model such as `models/category.ts`.

## Models

| Dart | TS |
|---|---|
| `class Foo { final String id; final int? n; … }` | `export interface Foo { id: string; n: number \| null; … }` (readonly not needed; never mutate) |
| `factory Foo.fromJson(Map<String, dynamic> j)` | `export function parseFoo(json: unknown): Foo` (accepts anything; never throws) |
| named constructors / `Foo.fromMap(id, data)` | `parseFooMap(id, data)` |
| `toJson()` | `fooToJson(f: Foo): JsonMap` (only where Dart has it: cart lines, categories, history) |
| getters (`bool get isLive => status == 'live'`) | small exported functions (`fooIsLive(f)`) or computed fields set in `parseFoo` when cheap and stable |
| `copyWith({...})` | spread: `{ ...f, read: true }`; export a helper only if Dart logic lives inside `copyWith` |
| `enum MyAuctionsTab { bidding, won, lost, watching }` | `export const MyAuctionsTabs = ['bidding','won','lost','watching'] as const; export type MyAuctionsTab = typeof MyAuctionsTabs[number];` |
| enum with a value (`SearchSort.priceAsc('price_asc')`) | union of the wire values + a `const` map from Dart names if code uses them |
| `DateTime?` | `Date \| null` via `parseApiDate()` (keep the Dart parsing rules: ISO strings, Firestore `{_seconds}`…) |
| `num` money | `number`; follow Dart rounding helpers in `json.ts` (`dartRound`, `cents`) |
| `List<Bar>` from `jsonItems(j['items'])` | `jsonItems(j.items).map(parseBar)` (`jsonItems` keeps only objects, like Dart) |
| `(MemberProfile, ProfileDetails)` record | a tuple `[MemberProfile, ProfileDetails]` or an object `{ profile, details }`; be consistent within the file |
| Two classes with the same name (`CompletedMission` in preferences_models + wishlist_repository) | one TS type, imported from one place |

**Tolerance rules.** Copy every fallback literally:

```dart
factory AppNotification.fromJson(Map<String, dynamic> j) {
  final nested = j['data'] is Map ? Map<String, dynamic>.from(j['data'] as Map) : const <String, dynamic>{};
  return AppNotification(
    id: _str(j['id']) ?? _str(nested['notificationId']) ?? '',
    body: _str(j['body']) ?? _str(j['message']) ?? '',
    read: j['read'] == true || (j['read'] == null && j['readAt'] != null),
    createdAt: parseApiDate(j['createdAt']), …
```
```ts
export function parseAppNotification(json: unknown): AppNotification {
  const j = asMap(json);
  const nested = isMap(j.data) ? j.data : {};
  return {
    id: nStr(j.id) ?? nStr(nested.notificationId) ?? '',
    body: nStr(j.body) ?? nStr(j.message) ?? '',
    read: j.read === true || ((j.read === null || j.read === undefined) && j.readAt != null),
    createdAt: parseApiDate(j.createdAt), …
```

Watch these Dart semantics:
- `'${j['x']}'` turns `null` into the string `"null"`; `'${j['x'] ?? ''}'` doesn't. Use `dstr()` vs `strOr()` accordingly.
- `j['n'] is num ? (j['n'] as num).toInt() : 0` truncates; `int.tryParse('$v')` accepts only integers; `num.tryParse` accepts decimals.
  Use the matching helper (`toInt`, `intTryParse`, `numTryParse`, `numOr`).
- `x == true` is strict (a string `"true"` is false); `x != false` defaults to true.
- `.where(...)` filters after parsing (e.g. `ugc()` drops photos without `imageUrl`; categories without id/name are dropped).
- Dart strings `trim()` in parsers: keep them.
- Text built with `l10nNow()` in a model (offer badges, `checkoutErrorMessage`) doesn't belong in `@vidaxl/api`: return a descriptor
  (`{ kind: 'multiplier', value: '2' }`) or a code, and put the text function in the app or in `@vidaxl/core` (through `l10nNow()`).

## Repositories

```ts
// Ported from: lib/data/repositories/wishlist_repository.dart
import { ApiClient } from '../client/apiClient';
import { jsonItems } from '../models/json';
import { parseCatalogProductCard, type CatalogProductCard } from '../models/catalogProduct';

const path = (sku: string) => `me/wishlist/${encodeURIComponent(sku)}`;

/** The member's wishlist (`/me/wishlist`). Every call throws [ApiError] on failure. */
export class WishlistRepository {
  constructor(readonly api: ApiClient) {}

  /** `GET /me/wishlist` — saved products as cards. */
  async list(): Promise<CatalogProductCard[]> {
    return jsonItems((await this.api.getJson('me/wishlist')).items).map(parseCatalogProductCard);
  }

  /** `PUT /me/wishlist/<sku>` — 201 added, 200 already saved. */
  async add(sku: string): Promise<WishlistChange> {
    return parseWishlistChange(await this.api.putJson(path(sku)), sku);
  }

  /** `DELETE /me/wishlist/<sku>` — 204. */
  async remove(sku: string): Promise<void> {
    await this.api.deleteJson(path(sku));
  }
}
```

Rules:
- **Same class and method names**, same parameter meaning. Dart named params (`{String? cursor}`) become an options object
  (`myOrders({ cursor })`); a single required positional stays positional.
- **Same request**: method, path (copy the Dart string, including whether it has a leading `/`; the client resolves both under `/api/v1/`),
  `encodeURIComponent` wherever Dart uses `Uri.encodeComponent`, query keys (the client drops null/empty values), body keys. Dart
  `'key': ?value` and `if (x != null) 'key': x` both mean **omit the key**, so don't send `null`.
- **Same post-processing**: `?? fallback`, `.trim()`, `maxAmount` sent as an integer when whole, `_cartOrReload` (empty body → `GET /cart`),
  `return null` on 404 (`bySku`, `detail`), `isDemoOff` (404 on demo routes).
- **Empty 2xx bodies**: Dart `postJson`/`patchJson` threw `bad_response` and repositories swallowed it (`_noContent`, `_ok`). Keep the
  repository's *result* (void / 0 / the fallback). Check how `ApiClient` handles empty bodies before copying the workaround.
- **Errors**: let `ApiError` propagate (`status`, `code`, `message`, `details`). Don't catch unless Dart does.
- **Statics**: `static const maxQty = 20` → `static readonly maxQty = 20`; `pageSize`, `supportStatuses` likewise.
- Keep the Dart doc comments (endpoint, response shape, error codes) as TSDoc: they are the API contract for the hook authors.
- Export everything from `packages/api/src/index.ts`.

## Tests

Port the parsing and HTTP tests into `packages/api/__tests__/` (skill `flutter-test-to-jest`): `fixture(name)` and `fakeFetch()` live in
`packages/api/__tests__/helpers.ts`, and the recorded responses in `packages/api/__tests__/fixtures/` (copied from Flutter
`test/fixtures/api`). For each repository method, assert the exact URL, method, headers and body, plus the parsed result of the fixture.

## Done when

- [ ] Every public class, enum, function and constant of the Dart file has a TS counterpart (or a matrix note).
- [ ] Parsers never throw on `{}`, `null`, wrong types, or missing lists (add a test with `{}`).
- [ ] Requests are byte-for-byte the Dart ones (tests assert them).
- [ ] No React/RN/Firebase/i18n imports; `npm run typecheck -w @vidaxl/api` and `npm test -w @vidaxl/api` pass.
- [ ] `// Ported from:` header present; matrix row updated.

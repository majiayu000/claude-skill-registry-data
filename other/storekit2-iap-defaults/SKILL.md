---
name: storekit2-iap-defaults
description: 'Default StoreKit 2 architecture for a single non-consumable IAP (Remove Ads, Pro Unlock): `StoreKitBridge` isolates `import StoreKit` to one Live file; launch-time `Transaction.updates`; `Transaction.currentEntitlements` for unlock state; `finish()` timing; `AppStore.sync()` restore; `.storekit` + Fake-bridge test seam. Invoke when adding IAP, wiring StoreKit 2, or asked "how do I unlock a purchase / restore purchases / test IAP". Does NOT cover subscriptions → apple-skills:storekit, or ad SDKs → monetization-sdk-integration.'
---

# StoreKit 2 IAP Defaults

Default shape for the smallest IAP most solo/small apps ship: one
non-consumable unlock (Remove Ads, Pro Unlock). `Product`, `Transaction`, and
`AppStore` have no public initializers — you cannot construct a fixture — so
the seam below exists to make StoreKit 2 testable at all, not for abstraction's
sake.

## When to invoke

- Adding a first non-consumable IAP to a new or existing app.
- Wiring `Product.products(for:)`, `Transaction.updates`,
  `Transaction.currentEntitlements`, or `AppStore.sync()`.
- Deciding where entitlement state lives, when to call `finish()`, or how to
  implement Restore Purchases.
- Setting up a `.storekit` configuration file or a StoreKit unit-test seam.
- Asked "how do I test a purchase without a sandbox account" or "why isn't my
  unlock surviving reinstall".

## Scope

Owns: bridge/seam shape, entitlement-derivation rules, test strategy for
**non-consumable IAP**. Does NOT own:

- Subscriptions/consumables — different renewal semantics; this skill's
  `currentEntitlements()` shape is deliberately "own it or don't."
- Ad SDK isolation — same bridge-protocol *pattern*, different domain →
  `monetization-sdk-integration`.
- What App Review requires of Restore Purchases / IAP pricing clarity (3.1.1)
  → `app-store-review-rejections`.
- Creating the IAP product in App Store Connect — the ASC API 2.0 has
  `POST /v2/inAppPurchases` plus `inAppPurchaseLocalizations`,
  `inAppPurchasePriceSchedules`, and `inAppPurchaseSubmissions` for
  automating this end-to-end → `asc-api-automation`; the web UI is the
  manual alternative.
- Getting the binary containing this code to TestFlight →
  `local-archive-export-upload`.

## The bridge seam

`Product`/`Transaction`/`AppStore` are untestable globals. Put a protocol
between the client and StoreKit; tests inject a fake instead:

```swift
// StoreKitBridge.swift — no `import StoreKit`; fully fake-able.
protocol StoreKitBridge: Sendable {
    func products(for ids: Set<String>) async throws -> [BridgeProduct]
    func currentEntitlements() async -> Set<String>
    func purchase(productId: String) async throws -> BridgePurchaseOutcome
    func sync() async throws
    func transactionUpdates() -> AsyncStream<BridgeTransactionEvent>
}
struct BridgeProduct: Sendable, Equatable { let id, displayName, displayPrice: String }
enum BridgePurchaseOutcome: Sendable, Equatable {
    case success(productId: String), userCancelled, pending, failed(reason: String)
}

// LiveStoreKitBridge.swift — the ONLY file that imports StoreKit.
import StoreKit
struct LiveStoreKitBridge: StoreKitBridge {
    func currentEntitlements() async -> Set<String> {
        var ids: Set<String> = []
        for await result in Transaction.currentEntitlements {
            guard case .verified(let t) = result, t.revocationDate == nil else { continue }
            ids.insert(t.productID)
        }
        return ids
    }
    // products(for:) / purchase(productId:) / sync() / transactionUpdates()
    // follow the same shape: Product.products(for:), Product.purchase(options:)
    // (visionOS: purchase(confirmIn:options:) instead — purchase(options:)
    // isn't available there), AppStore.sync(), Transaction.updates.
}
```

Everything above `LiveStoreKitBridge` talks only to `any StoreKitBridge` — zero
`import StoreKit`. Verify: `rg '^(internal |public )*import StoreKit' Sources/`
→ expect exactly 1 hit.

## Entitlement state, `finish()`, restore

- **Unlock state is derived, not stored.** Don't persist "isPurchased"
  independently — derive it from `currentEntitlements()` each time (a
  non-consumable with `revocationDate == nil` is entitled); an independently
  stored boolean drifts from Apple's record on refund/family-share/restore.
- **Call `finish()` after the entitlement is applied**, not before (risks
  losing the unlock on a mid-purchase crash) and not never (an unfinished
  transaction is redelivered via `Transaction.updates` on every launch).
- **The `Transaction.updates` listener starts at app launch**, not lazily on
  first paywall visit — refunds/family-share revocations/Ask-to-Buy approvals
  can arrive while the user is anywhere in the app.
- **`restorePurchases()` always calls `AppStore.sync()` first**, even when a
  local cache looks empty — Apple's `sync()` docs position it as the forced
  sync behind a user-initiated Restore Purchases control (Guideline 3.1.1
  itself only asks for a restore mechanism), so it's not an optimization to
  skip:

```swift
func restorePurchases() async throws -> [BridgeProduct] {
    try await bridge.sync()
    let entitled = await bridge.currentEntitlements()
    guard !entitled.isEmpty else { return [] }
    return try await bridge.products(for: entitled)
}
```

## Testing strategy

| Layer | Tool | Covers |
|---|---|---|
| Unit tests | `FakeStoreKitBridge` (scripted outcomes + call counters) | Client logic — zero StoreKit dependency, runs in CI |
| Interactive local run | `.storekit` file wired into the Xcode scheme (Run → Options → StoreKit Configuration) | Manual purchase-flow smoke test, no sandbox Apple ID |
| Automated purchase-flow tests | `StoreKitTest`'s `SKTestSession` (loads the same `.storekit` file) | XCUITest/integration-level flows against the real StoreKit stack |

A `.storekit` file is a testing fixture with no effect on a shipped build;
it's what enables the last two rows, not a gap in unit-test coverage if absent.

## War stories (evidence tier in italics)

- `Product.products(for:)` returns `[]`, not a thrown error, for an unknown ID
  (typo/sandbox drift) — decide what "no products" means for `purchase()`
  before you hit it (one real app: `.failed(reason: "product not found: <id>")`
  rather than a silent no-op). *Practice observed.*
- A verified `Transaction.updates`/purchase-path switch on
  `Product.PurchaseResult` needs `@unknown default`, not a plain `default` —
  without it Swift 6 mode fails to compile ("switch covers known cases, but
  'Product.PurchaseResult' may have additional unknown values"; a warning in
  Swift 5 mode), and a plain `default` would silence the warning a case Apple
  adds later should raise ([Switching Over Future Enumeration
  Cases](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/statements/#Switching-Over-Future-Enumeration-Cases));
  recheck on every OS-support bump. *Compiled-verified* (Swift 6.3.2).
- Post-purchase catalog refetch can come back empty even though the purchase
  succeeded (rare ASC catalog instability). Synthesizing a minimal entitled
  product (id + a locale-neutral placeholder price) beats `.failed` for a
  purchase Apple already charged for; pair it with a telemetry hook so the
  desync is observable. *Practice observed.*
- The transaction-observer `Task`'s priority is a real UX decision: a
  refund/family-share event should flip entitlement state promptly while the
  user may be in-session. `.background` deprioritizes it behind arbitrary
  work; one real app shipped `.background` first and upgraded to `.utility`
  after review. *Practice observed.*

Provenance for the bridge/skeleton's verification claims: `references/official-docs.md`.

## Rationale

The bridge exists because `Product`/`Transaction` have no public
initializers — "test the untestable" is the first wall a from-scratch
StoreKit 2 implementation hits, not a hypothetical. Isolating `import
StoreKit` to one file also keeps the client testable on CI runners without a
signed-in sandbox tester.

## Deviation considerations

- **A small catalog of non-consumables** — extend `BridgeProduct`'s fields,
  but keep `currentEntitlements()` a flat `Set<String>`.
- **Subscriptions** — the "own it or don't" model is too coarse; you need
  `Transaction.subscriptionStatus` and renewal-state handling this skill does
  not cover.

## Common Mistakes

1. Persisting `isPurchased` instead of deriving it from `currentEntitlements()`.
2. Never calling `finish()`, or calling it before the entitlement is applied.
3. Starting the `Transaction.updates` listener lazily instead of at launch.
4. Treating `products(for:)` returning `[]` as a thrown-error case.
5. Skipping `AppStore.sync()` in `restorePurchases()` "because the cache is empty."
6. No `@unknown default` on the `Product.PurchaseResult` switch (Swift 6 mode
   won't compile it), or a plain `default` that hides cases Apple adds later.
7. Treating the `.storekit` file as unit-test infrastructure — it configures
   the interactive runtime and `StoreKitTest`, not the fake bridge.

## Review Checklist

- [ ] `import StoreKit` appears in exactly one file.
- [ ] Unlock state is derived from `currentEntitlements()`, not stored as an
      independent boolean.
- [ ] `Transaction.updates` listener starts at app launch.
- [ ] `finish()` is called after the entitlement is applied, on every path.
- [ ] `restorePurchases()` always calls `sync()` before reading entitlements.
- [ ] `Product.PurchaseResult`'s switch has an `@unknown default` arm (not a
      plain `default`).
- [ ] A fake bridge covers purchase success/cancel/pending/failed and restore
      empty/non-empty in unit tests.
- [ ] A visible Restore Purchases control exists — this catalog's default
      places it in Settings (3.1.1 — `app-store-review-rejections`).

## Related skills

- `monetization-sdk-integration` — same bridge-isolation pattern for ad SDKs.
- `app-store-review-rejections` — Restore Purchases / pricing-clarity review gate (3.1.1).
- `asc-api-automation` — TestFlight/App Store ops after the build exists.
- `local-archive-export-upload` / `xcode-cloud-single-track-ci` — shipping the binary.
- `swift-dependency-injection` — the general protocol-injection pattern this bridge instantiates.
- `swift-testing-baseline` — where this bridge's fake fits this catalog's test stack.
- `apple-skills:storekit` (aggregated external) — StoreKit 2 API reference incl. subscriptions, `SubscriptionStoreView`, renewal state — the part this skill does not cover.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.

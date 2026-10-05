---
name: iap-compliance
description: >-
  Detects external payment processors and WebView payment flows used for digital goods and verifies StoreKit integration, enforcing Guideline 3.1.1's requirement to use Apple IAP for all digital content purchases.
---

# Skill: IAP Compliance
<!-- SEO: in-app purchase StoreKit Stripe PayPal external payment WebView digital goods Guideline 3.1.1 iOS App Store rejection -->

## Purpose
Detects external payment processors and WebView payment flows used for digital goods, and verifies StoreKit integration with restore functionality, enforcing Guideline 3.1.1's requirement to use Apple IAP for all digital content purchases.

## Apple Guideline
- **Primary:** 3.1.1 — Business: Payments — In-App Purchase
- **Related:** 3.1.3
- **Reference:** `references/guidelines/3-business.md`

## Real-World Rejection Cases
- **Case:** App used Stripe for in-app digital subscription purchase — rejected under 3.1.1
  **Source:** purchasely.com/blog/app-store-in-app-purchase-reject
  **Root cause:** All digital content/feature unlocks must use Apple IAP; external payment systems are prohibited — Apple's review team specifically looks for Stripe, PayPal, and other payment SDK integrations

- **Case:** App opened WebView with payment page for premium feature unlock — rejected
  **Source:** Apple Developer Forums
  **Root cause:** Routing digital goods purchase through WebView to bypass IAP is explicitly prohibited — reviewers inspect WebView destinations for payment/checkout flows

- **Case:** App accepted a promo code entered inside the app to unlock premium features without going through StoreKit — rejected under 3.1.1
  **Source:** Purchasely (purchasely.com/blog/app-store-rejection-reasons)
  **Root cause:** In-app promo codes for digital content must use Apple's official promotional offer mechanism via StoreKit, not a custom code-entry field that bypasses IAP entirely

- **Case:** IAP product labeled "Donate" used to unlock a premium feature — Apple rejected as the product misrepresented the transaction
  **Source:** Purchasely (purchasely.com/blog/app-store-rejection-reasons)
  **Root cause:** IAP products must accurately describe what is purchased; labeling a feature unlock as a "donation" misrepresents the transaction and violates 3.1.1 — use descriptive product names that reflect the actual digital good or subscription

> **Important — US Storefront Exception (effective May 2025):** Following the Epic v. Apple court ruling, apps distributed on the **US App Store** may include external purchase links under Apple's External Purchase Entitlement. This is a narrow, Apple-approved exception: it requires the `com.apple.developer.storekit.external-purchase-link` entitlement, specific disclosure language ("You will be taken to an external website..."), and compliance with Apple's External Purchase Link guidelines. Apps without this entitlement that use external payment for digital goods remain a guaranteed rejection in all storefronts, including the US.

## Trigger
Invoke on any iOS/macOS project that sells digital content, subscriptions, or unlockable features.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/Podfile` or `**/Package.swift` or `**/Package.resolved` — locate dependency manifests for payment SDK detection.
3. `Glob` `**/*Paywall*` or `**/*Purchase*` or `**/*Premium*` or `**/*Store*` — locate purchase flow files.

### Phase 2: Checks

1. **External payment SDK for digital goods**
   `Grep` pattern `Stripe|stripe|PayPal|paypal|Braintree|braintree|Square|square\.up` in `**/*.swift` and dependency manifest files.
   If found near `purchase|checkout|subscribe|unlock|premium|upgrade` context → 🔴 CRITICAL. External payment processors for digital goods violate 3.1.1.

2. **WebView payment bypass**
   `Grep` pattern `WKWebView|SFSafariViewController` in `**/*.swift`.
   For each match, `Read` surrounding context — if URL or navigation involves `"payment"|"checkout"|"purchase"|"subscribe"|"billing"` → 🔴 CRITICAL. Routing digital purchase through a WebView to bypass IAP is a known rejection pattern.

3. **StoreKit integration present**
   `Grep` pattern `StoreKit|SKPaymentQueue|Product\.purchase|SKProduct|SKPayment` in `**/*.swift`.
   If absent while app appears to offer digital content or premium features → 🟠 HIGH. Digital goods must be purchased through StoreKit.

4. **Restore purchases mechanism**
   `Grep` pattern `"Restore Purchases"|restorePurchases|restoreCompletedTransactions` in `**/*.swift`.
   If StoreKit is used but restore mechanism is absent → 🟠 HIGH. Non-consumable IAP and auto-renewable subscriptions must offer a restore button per 3.1.1.

5. **External Purchase Entitlement compliance (US storefront)**
   `Grep` pattern `externalPurchase|external-purchase-link|ExternalPurchaseLink|openURL.*purchase|openURL.*checkout` in `**/*.swift` and `*.entitlements`.
   If external purchase links are used but the entitlement `com.apple.developer.storekit.external-purchase-link` is absent in any `.entitlements` file → 🔴 CRITICAL. External payment links require Apple's explicit entitlement — using them without it violates 3.1.1 in all storefronts.
   If entitlement is present but no disclosure string (`"You will be taken to an external website"`) found near the link → 🟠 HIGH. Apple requires a specific disclosure notice before redirecting to external payment.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## IAP Compliance — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove Stripe payment integration for digital goods — all digital purchases must use StoreKit/Apple IAP — `PaymentManager.swift:33` — Guideline 3.1.1
- [ ] TODO: Remove WebView payment flow for subscription upgrade — routing digital purchases through WebView bypasses IAP and will be rejected — `PremiumViewController.swift:78` — Guideline 3.1.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Integrate StoreKit for digital content purchases — no StoreKit usage found despite premium features — Guideline 3.1.1
- [ ] TODO: Add "Restore Purchases" button to paywall/settings — non-consumable IAP requires a restore mechanism — Guideline 3.1.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Ensure physical goods/services (e.g., delivery, rideshare) use the external payment flow exception correctly — verify the exception applies before using Stripe

### 🟢 LOW — Best practice
- [ ] TODO: Implement a transaction observer for edge-case purchase states — use `SKPaymentTransactionObserver` (StoreKit 1) **or** `Transaction.updates` listener (StoreKit 2), not both simultaneously. These are separate APIs for separate codepaths; choose one and implement consistently throughout the app.
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Works on Swift, Objective-C, React Native, Flutter projects.
- **US storefront exception (May 2025):** External purchase links are permitted on the US App Store only, under the External Purchase Entitlement — this does not apply to other storefronts (EU Digital Markets Act has a separate entitlement path).

## Quick Commands

Run these in your project root to check manually:

```bash
# Check for StoreKit usage (should be present for digital goods)
!grep -rn "StoreKit\|SKPaymentQueue\|SKProduct\|Product.purchase" . --include="*.swift" | wc -l

# Check for external payment SDKs (red flag for digital goods)
!grep -rn "Stripe\|PayPal\|Braintree\|Square\|checkout" . --include="*.swift" -i | grep -v "//"

# Check for restore purchases implementation
!grep -rn "restorePurchases\|restoreCompletedTransactions\|Restore" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/SubscriptionPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/*.storyboard`, `**/*.xib`

2. **Search for rejection patterns**
   - Grep `SKPaymentQueue\|StoreKit\|Product.purchase\|SKProduct` — confirms StoreKit is in use
   - Grep `stripe\|paypal\|braintree\|Stripe\|PayPal` — third-party payment SDKs (flag for digital goods)
   - Grep `externalPurchase\|purchaseExternal` — explicit external payment identifiers
   - If third-party SDK found: grep nearby strings for digital product terms (`subscription\|premium\|unlock\|credit\|coin`) to confirm digital goods context

3. **Determine verdict**
   - `stripe`/`paypal` import + digital goods strings nearby + no `StoreKit` → 🔴 CRITICAL (Guideline 3.1.1)
   - `stripe`/`paypal` import + physical goods context only (e.g., `shipping\|delivery\|store`) → 🟢 pass (physical goods are exempt)
   - `WKWebView` alone is not sufficient to flag — only flag if URL loads a payment form for digital goods (requires manual review)
   - `StoreKit` used for all digital purchases → 🟢 pass

4. **Report**
   - File path + line of third-party payment SDK import or web payment URL
   - Fix: Replace all digital content payments with StoreKit `Product.purchase()` (StoreKit 2) or `SKPaymentQueue.default().add()`
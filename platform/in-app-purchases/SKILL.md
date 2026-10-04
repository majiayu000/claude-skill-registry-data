---
name: in-app-purchases
description: In-app purchases and subscriptions with RevenueCat. Product configuration, entitlements, paywalls, restore purchases, subscription status. Use when implementing subscriptions, one-time purchases, paywalls, or monetization.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# In-App Purchases & Subscriptions

Monetize your Flutter app with RevenueCat - the industry-standard solution for in-app purchases and subscriptions. Handles cross-platform billing, receipt validation, and subscription management.

## When to Use This Skill

- Adding subscriptions or one-time purchases
- Implementing a paywall
- Managing premium features/entitlements
- Restoring purchases
- User asks "add subscription", "paywall", "in-app purchase", "monetize", or "RevenueCat"

## Questions to Ask

1. **Purchase types:** Subscriptions, one-time purchases, or both?
2. **Subscription tiers:** Free, premium only, or multiple tiers (basic/pro/enterprise)?
3. **Trial period:** Offer free trial? How long?
4. **Paywall trigger:** Where should the paywall appear? (feature-gated, onboarding, settings)
5. **Restore flow:** Where should users restore purchases? (settings, paywall)

## Quick Reference

### RevenueCat Concepts

| Concept | Description |
|---------|-------------|
| **Offering** | Container for products shown to users (e.g., "default", "sale") |
| **Package** | Specific product in an offering (e.g., "monthly", "annual") |
| **Entitlement** | Access level granted by purchase (e.g., "premium", "pro") |
| **CustomerInfo** | User's purchase state, active entitlements, subscriptions |

### Product Types

| Type | Use Case | Example |
|------|----------|---------|
| **Auto-renewable** | Recurring access | Monthly/annual subscription |
| **Non-consumable** | Permanent unlock | Remove ads, lifetime access |
| **Consumable** | One-time use | Credits, coins |

## Reference Files

- `reference/services/purchases_service.dart` - RevenueCat wrapper
- `reference/repositories/` - Domain interface + implementation
- `reference/providers/purchases_providers.dart` - Riverpod state
- `reference/failures/purchases_failures.dart` - Sealed failures
- `reference/models/subscription_status.dart` - Freezed models

## Workflow

### Phase 1: RevenueCat Setup

1. Create RevenueCat account at [revenuecat.com](https://www.revenuecat.com)
2. Create a new project in RevenueCat dashboard
3. Add App Store Connect and Play Console credentials
4. Create products in App Store Connect / Google Play Console
5. Configure products in RevenueCat → Products
6. Create Entitlements (e.g., "premium")
7. Create Offerings and add Packages

**See:** [revenuecat-setup-guide.md](revenuecat-setup-guide.md)

### Phase 2: Platform Configuration

**iOS:**
- Enable In-App Purchase capability in Xcode
- Add StoreKit configuration file for testing
- Configure App Store Connect shared secret in RevenueCat

**Android:**
- Add billing permission to AndroidManifest.xml
- Configure Play Console service account in RevenueCat
- Upload signed APK/AAB to internal testing track

**See:** [platform-setup-guide.md](platform-setup-guide.md)

### Phase 3: Implementation

1. Add `purchases_flutter` dependency
2. Copy reference files to project
3. Initialize RevenueCat in `main.dart`
4. Create paywall UI
5. Implement entitlement checks
6. Add restore purchases flow
7. Handle subscription changes

**See:** [implementation-guide.md](implementation-guide.md)

### Phase 4: Testing

1. Test with StoreKit configuration (iOS Simulator)
2. Test with sandbox accounts (real devices)
3. Test restore purchases
4. Test subscription lifecycle (renew, cancel, expire)
5. Verify webhook events in RevenueCat dashboard

## Core API

```dart
await PurchasesService.instance.initialize(apiKey: key); // in main.dart
final isPremium = ref.watch(isPremiumProvider);           // check entitlement
await ref.read(purchasesRepositoryProvider).purchase(pkg); // purchase
await ref.read(purchasesRepositoryProvider).restorePurchases(); // restore
```

**See:** [implementation-guide.md](implementation-guide.md) for complete examples.

## Dependencies

```yaml
dependencies:
  purchases_flutter: ^8.0.0
```

## Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `PurchaseCancelled` | User cancelled | Dismiss silently |
| `PurchasePending` | Payment pending (e.g., parental approval) | Show "pending" message |
| `ProductNotFound` | Invalid product ID | Log error, hide product |
| `NetworkError` | No connection | Show retry option |
| `StoreError` | App Store/Play Store error | Show generic error |
| `NotAllowed` | Device restricted | Show restriction message |

## Guides

| File | Content |
|------|---------|
| [revenuecat-setup-guide.md](revenuecat-setup-guide.md) | Dashboard configuration |
| [platform-setup-guide.md](platform-setup-guide.md) | iOS & Android platform setup |
| [implementation-guide.md](implementation-guide.md) | Code implementation steps |
| [paywall-guide.md](paywall-guide.md) | Paywall UI patterns |
| [testing-guide.md](testing-guide.md) | Sandbox testing |
| [checklist.md](checklist.md) | Verification checklist |

## Checklist

**Setup:**
- [ ] RevenueCat project created with credentials
- [ ] Products configured in App Store Connect / Play Console
- [ ] Entitlements and Offerings configured

**Platform:**
- [ ] iOS: In-App Purchase capability, StoreKit config
- [ ] Android: BILLING permission, app uploaded to testing track

**Implementation:**
- [ ] RevenueCat initialized, providers created
- [ ] Paywall with restore purchases button
- [ ] Entitlement checks gating premium features

**See:** [checklist.md](checklist.md) for complete verification list.

## Common Issues

### Purchases not showing in RevenueCat

Ensure products are "Ready to Submit" in App Store Connect or "Active" in Play Console. RevenueCat can only fetch approved products.

### "Cannot connect to App Store" on Simulator

Use StoreKit Configuration file for Simulator testing. Real App Store requires physical device with sandbox account.

### Android purchases failing silently

Ensure the app is uploaded to at least internal testing track. Google Play billing requires a signed release build.

## Related Skills

- `/analytics` - Track purchase events, revenue
- `/auth` - User identification for RevenueCat
- `/design` - Paywall UI design patterns
- `/i18n` - Localized paywall text, pricing
- `/testing` - Mock purchases for tests
- `/force-update` - Version gating with subscriptions

## Next Steps

After implementing purchases:
1. `/analytics` - Track purchase events and revenue
2. `/i18n` - Localize paywall and product descriptions
3. `/testing` - Create mock repository for tests

---
name: subscription-disclosure
description: >-
  Detects missing or obscured subscription disclosure elements on paywall screens, enforcing Guideline 3.1.2(c) requirements for auto-renewal terms, trial end dates, and actual price.
---

# Skill: Subscription Disclosure
<!-- SEO: subscription auto-renewal disclosure free trial paywall price billing period cancellation Guideline 3.1.2 iOS App Store rejection -->

## Purpose
Detects missing or obscured subscription disclosure elements (auto-renewal, trial end terms, cancellation instructions, actual price) on paywall screens, enforcing Guideline 3.1.2(c).

## Apple Guideline
- **Primary:** 3.1.2(c) — Business: Payments — Subscriptions: Disclosure Requirements
- **Related:** 3.1.2(a), 3.1.2(b)
- **Reference:** `references/guidelines/3-business.md`

## Real-World Rejection Cases
- **Case:** Paywall shows "50% OFF" prominently — actual billing amount ($9.99/month) shown in 10pt gray text below fold — rejected
  **Source:** https://developer.apple.com/forums/thread/127616
  **Root cause:** 3.1.2(c) requires billed amount shown clearly and conspicuously — size/color/placement must not obscure it; discounts shown without clear pricing are a known rejection trigger

- **Case:** Free trial paywall shows "Try free for 7 days" with no mention of what happens after trial — rejected
  **Source:** RevenueCat Community (https://community.revenuecat.com/general-questions-7/rejected-due-to-guideline-3-1-2-business-payments-subscriptions-4775)
  **Root cause:** Must clearly state amount billed after trial ends and when billing starts

- **Case:** App rejected for subscription auto-renewal not disclosed — "billed amount not clearly displayed"
  **Source:** blog.wenhaofree.com/en/posts/articles/app-store-guideline-3-1-2-subscription-fix/
  **Root cause:** Auto-renewable subscription purchase flow must state renewal continues until cancelled

- **Case:** Paywall had no links to Privacy Policy or Terms of Use — reviewer required legal doc links before purchase could proceed — rejected under 3.1.2(c)
  **Source:** AngularCorp blog (angularcorp.com/en-us/blog/guideline-3-1-2)
  **Root cause:** Subscription paywalls must include accessible links to Privacy Policy and Terms of Use; reviewers verify these links exist and are functional before approving

- **Case:** Paywall showed price as "from $1.67/month" calculated from an annual plan — reviewer expected to be billed $1.67/month but actual charge was $19.99/year — rejected
  **Source:** AppFollow (appfollow.io/blog/app-store-rejection-reasons)
  **Root cause:** If billing is annual, the displayed price must be the annual amount or clearly labeled as "billed annually at $X"; showing only the monthly equivalent without disclosing actual charge is a known rejection pattern

## Trigger
Invoke on any iOS/macOS project with subscription or in-app purchase paywalls.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*Paywall*` or `**/*Subscription*` or `**/*Premium*` or `**/*Pricing*` — locate paywall and subscription UI files.
2. `Glob` `**/*.swift` — collect all Swift source files for broader search.

### Phase 2: Checks

Search primarily in paywall/subscription view files (`*Paywall*`, `*Subscription*`, `*Premium*`, `*Pricing*`). Fall back to all `**/*.swift` if no dedicated files found.

1. **Auto-renewal disclosure**
   `Grep` pattern `"auto-renew"|"automatically renew"|"renews automatically"|"auto renew"|"recurring"` in subscription/paywall files.
   If absent → 🔴 CRITICAL. Every auto-renewable subscription paywall must disclose that the subscription renews automatically until cancelled.

2. **Trial end disclosure**
   `Grep` pattern `"after.*trial|trial ends|then.*per|after.*free|billed after|charged after"` in subscription/paywall files.
   If a free trial is offered but this disclosure is absent → 🔴 CRITICAL. Users must know what they will be charged when the trial ends.

3. **Cancellation information**
   `Grep` pattern `"cancel anytime"|"cancelable"|"Cancel in Settings"|"manage.*subscription"|"cancell"` in subscription/paywall files.
   If absent → 🟠 HIGH. Instructions for cancellation must be accessible from the subscription UI.

4. **Actual price display**
   `Grep` pattern `displayPrice|localizedPrice|priceLocale|price\.formatted|priceString` in subscription/paywall files.
   If absent → 🔴 CRITICAL. The actual billed price must be displayed, not only a discount label. Must use StoreKit's localized price APIs to show the correct price for the user's region.

5. **Discount without price**
   `Grep` pattern `"% off"|"save.*%"|"discount"|"OFF"` in subscription/paywall files.
   If found, verify `displayPrice|localizedPrice` also present in same file → 🟠 HIGH if price display absent. Showing a discount without the absolute price is a known rejection pattern.

6. **Billing period disclosure**
   `Grep` pattern `subscriptionPeriod|subscription_period|billingPeriod|"per month"|"per year"|"monthly"|"annually"|"weekly"` in subscription/paywall files.
   If absent → 🟠 HIGH. Billing frequency must be clearly stated alongside the price.

7. **Family Sharing disclosure (Guideline 3.1.2(d))**
   `Grep` pattern `isFamilyShareable|familyShared|familySharable` in `**/*.swift`.
   If Family Sharing is enabled on any subscription product: verify a disclosure is present on the paywall such as "Shareable with up to 5 family members" → 🟡 MEDIUM if absent. Guideline 3.1.2(d) requires communicating Family Sharing eligibility to users before purchase.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Subscription Disclosure — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add auto-renewal disclosure text to paywall — e.g., "Subscription automatically renews unless cancelled" — `PaywallView.swift` — Guideline 3.1.2(c)
- [ ] TODO: Add post-trial billing disclosure — state what amount is charged after the free trial ends — `SubscriptionView.swift:45` — Guideline 3.1.2(c)
- [ ] TODO: Display actual localized price using displayPrice or localizedPrice — price absent from paywall UI — `PremiumView.swift` — Guideline 3.1.2(c)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Add cancellation instructions — e.g., "Cancel anytime in iPhone Settings > Subscriptions" — `PaywallView.swift` — Guideline 3.1.2(c)
- [ ] TODO: Show actual monthly price alongside "50% OFF" discount label — discount without price is a rejection pattern — `PaywallView.swift:88` — Guideline 3.1.2(c)
- [ ] TODO: Display billing period (monthly/annually/weekly) next to the price — `SubscriptionView.swift:34` — Guideline 3.1.2(c)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Verify disclosure text is visually conspicuous — not in small gray font below the fold — manual UI review required

### 🟢 LOW — Best practice
- [ ] TODO: Follow Apple's subscription UI guidelines — use clear, high-contrast disclosure text near the CTA button, not in footnotes
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Works on Swift, Objective-C, React Native, Flutter projects.

## Quick Commands

Run these in your project root to check manually:

```bash
# Check for auto-renewal disclosure text
!grep -rn "auto-renew\|automatically renew\|renews automatically" . --include="*.swift" -i

# Check for trial disclosure
!grep -rn "after.*trial\|trial ends\|then.*per\|free trial" . --include="*.swift" -i

# Check for actual price display (not just discount)
!grep -rn "displayPrice\|localizedPrice\|priceLocale\|price\b" . --include="*.swift" | grep -v "//"

# Check for discount-only display (missing actual price)
!grep -rn "% off\|save.*%\|discount" . --include="*.swift" -i
```

## Swift Anti-Pattern Reference
`examples/swift/SubscriptionPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/*.storyboard`, `**/*.xib`, `**/*.strings`

2. **Search for rejection patterns**
   - Grep `freeTrialPeriod\|trialPeriod\|free.*[Tt]rial\|freeTrial` — trial UI elements
   - Grep `subscriptionPrice\|priceLocale\|localizedPrice\|displayPrice` — price display
   - Grep `autoRenew\|auto-renew\|automatically renews\|autoRenewing` — renewal disclosure text
   - Grep `%.*off\|[Dd]iscount\|[Ss]ave.*%` — discount claims

3. **Determine verdict**
   - Trial UI found + no `autoRenew`/`automatically renews` text near it → 🟠 HIGH (Guideline 3.1.2(c))
   - Discount percentage shown + no actual billed amount displayed → 🟠 HIGH
   - `localizedPrice` displayed + renewal terms present → 🟢 pass

4. **Report**
   - File path + line of trial/discount UI without disclosure
   - Fix: Add "Then [price]/[period], cancel anytime" text directly below the CTA; show actual price alongside any discount percentage
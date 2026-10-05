---
name: loot-box-disclosure
description: >-
  Detects loot box, gacha, and randomized reward purchase mechanics that lack odds disclosure before purchase, enforcing Guideline 3.1.1's requirement to disclose item drop rates.
---

# Skill: Loot Box Disclosure
<!-- SEO: loot box gacha drop rates odds disclosure randomized reward mystery box IAP Guideline 3.1.1 iOS App Store rejection -->

## Purpose
Detects loot box, gacha, and randomized reward purchase mechanics that lack odds/probability disclosure before purchase, enforcing Guideline 3.1.1's requirement to disclose item drop rates.

## Apple Guideline
- **Primary:** 3.1.1 — Business: Payments — In-App Purchase (Randomized Items)
- **Related:** 3.1.2
- **Reference:** `references/guidelines/3-business.md`

## Real-World Rejection Cases
- **Case:** Gacha/loot box game rejected for not showing drop rates before purchase
  **Source:** Apple Developer Forums (Guideline 3.1.1 enforcement; multiple developer reports 2020–2024)
  **Root cause:** "Loot boxes" and similar randomized reward mechanisms must disclose the odds of receiving each item type before purchase — Apple requires this disclosure to be visible prior to the purchase confirmation step

- **Case:** App showed odds table only on a secondary "Info" screen behind a small "?" button — rejected; Apple required disclosure to be visible before the purchase confirmation tap
  **Source:** Apple Developer Forums (Guideline 3.1.1 enforcement; multiple developer reports 2021–2023)
  **Root cause:** The guideline requires disclosure "prior to purchase" — a secondary screen not shown by default does not satisfy this. Odds must be visible on or immediately adjacent to the purchase UI without requiring additional navigation.

- **Case:** Card game app disclosed category-level rates ("Rare: 3%") but did not list odds for individual cards within the category — rejected
  **Source:** Apple Developer Forums (multiple threads on 3.1.1 randomized items requirement, 2021–2023)
  **Root cause:** Apple requires the odds of receiving **each item type**, not just aggregate category percentages. When a user could receive one of many distinct rare cards, each card's individual probability must be disclosed.

- **Case:** App had odds listed in App Store description and on developer website but not surfaced inside the app itself — rejected
  **Source:** Apple Developer Forums
  **Root cause:** The in-app disclosure requirement is separate from App Store metadata. Odds must be accessible within the app at the point of purchase, not only in external documentation.

## Trigger
Invoke on any iOS/macOS project that includes randomized reward purchases, gacha mechanics, mystery boxes, or loot boxes.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/*Gacha*` or `**/*LootBox*` or `**/*Reward*` or `**/*Mystery*` — locate reward/gacha UI files.

### Phase 2: Checks

1. **Loot box / gacha pattern detection**
   `Grep` pattern `lootBox|gacha|randomReward|mysteryBox|gachapon|blindBox|loot_box|mystery_box` in `**/*.swift`.
   If found, proceed to checks 2–4 for odds disclosure verification.

2. **Randomization near purchase code**
   `Grep` pattern `arc4random|Int\.random|Double\.random|\.randomElement|shuffle\(\)` in `**/*.swift`.
   For each match, `Read` surrounding context — if randomization is adjacent to a purchase flow or reward distribution function, flag → 🟠 HIGH. Marks code as potentially randomized-reward purchase.

3. **Odds/probability disclosure in purchase UI**
   If loot box patterns found from check 1 or 2: `Grep` pattern `"probability"|"odds"|"chance"|"drop rate"|"% chance"|"likelihood"` in `**/*.swift` — especially in paywall/purchase view files.
   If absent → 🟠 HIGH. Probability of receiving each item type must be disclosed before the purchase is completed.

4. **StoreKit purchase call near gacha patterns**
   `Grep` pattern `SKProduct|Product\.purchase|SKPaymentQueue\.default\(\)\.add` in `**/*.swift`.
   For each StoreKit purchase call, `Read` surrounding context — if purchase triggers randomized reward distribution without nearby odds disclosure → 🟠 HIGH.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Loot Box Disclosure — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 3.1.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Add drop rate/probability disclosure UI before the loot box purchase confirmation — e.g., "Legendary: 1%, Rare: 9%, Common: 90%" — `GachaShopView.swift` — Guideline 3.1.1
- [ ] TODO: Verify odds for each item type are displayed before purchase — randomization detected near StoreKit purchase call without probability strings — `RewardManager.swift:67` — Guideline 3.1.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Ensure odds disclosure is visible before the purchase tap — disclosure placed after confirmation is insufficient

### 🟢 LOW — Best practice
- [ ] TODO: Link to a full odds table (in-app or web) from the purchase screen — some jurisdictions require detailed odds disclosure and the link satisfies both Apple and regulatory requirements
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
# Check for loot box / gacha patterns
!grep -rn "lootBox\|gacha\|randomReward\|mysteryBox\|blindBox" . --include="*.swift" -i

# Check for odds disclosure near purchase
!grep -rn "probability\|odds\|chance\|drop.*rate\|% chance" . --include="*.swift" -i
```

## Swift Anti-Pattern Reference
`examples/swift/SubscriptionPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Grep `randomItem\|randomReward\|gachaPool\|lootBox\|mysteryBox\|LootBox\|GachaPool` — randomized reward system
   - Grep `dropRate\|dropChance\|probability\|odds\|DropRate` — odds disclosure implementation
   - Grep `SKProduct\|Product.purchase` near randomized reward logic — IAP for randomized items

3. **Determine verdict**
   - Randomized reward pattern found + paid via IAP + no `dropRate`/`odds` disclosure → 🔴 CRITICAL (Guideline 3.1.1)
   - Randomized rewards are free (no IAP) → 🟢 pass (no requirement)
   - Odds table present alongside IAP purchase → 🟢 pass

4. **Report**
   - File path + line of randomized reward + IAP combination
   - Fix: Display odds for each item type before purchase; implement an odds table UI accessible from the purchase flow
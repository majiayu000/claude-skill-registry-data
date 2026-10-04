---
name: review-request-audit
description: >-
  Detects improper use of SKStoreReviewController.requestReview() that violates Guideline 5.6.1 — including prompts triggered by button taps, excessive frequency, or satisfaction gating.
---

# Skill: Review Request Audit
<!-- SEO: SKStoreReviewController requestReview manipulating reviews App Store rating prompt incentivized review Guideline 5.6.1 iOS App Store rejection -->

## Purpose
Detects improper use of `SKStoreReviewController.requestReview()` that violates Guideline 5.6.1 — including prompts triggered by user button taps, excessive frequency, or gating that solicits positive reviews while suppressing negative ones.

## Apple Guideline
- **Primary:** 5.6.1 — Legal: Manipulating Reviews
- **Related:** 2.1
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** App showed a "Rate Us" button that directly called `SKStoreReviewController.requestReview()` on tap — rejected under 5.6.1
  **Source:** Apple Developer Forums (multiple reports)
  **Root cause:** Guideline 5.6.1 prohibits prompting for reviews in response to a user action (button tap, gesture). Review requests must be triggered by the system, initiated by the app at an appropriate moment in the user journey — never as a direct response to tapping a "Rate this app" button.

- **Case:** App asked users "Are you enjoying the app?" and only called `requestReview()` when they tapped "Yes" — tapping "No" opened a feedback form instead — rejected for review gating
  **Source:** Apple Developer Forums (review gating reports, 2021–2024)
  **Root cause:** Filtering which users see the App Store review prompt based on their satisfaction response is review gating — a form of manipulation prohibited by 5.6.1. All users must have an equal chance of seeing the system prompt, regardless of their stated satisfaction.

- **Case:** App called `SKStoreReviewController.requestReview()` on every app launch — Apple's system cap (3 per 365 days) suppressed most prompts, but the pattern was flagged as abusive during review
  **Source:** Developer experience reports
  **Root cause:** Apple's system automatically caps review requests to 3 times per 365-day period, but excessive calls signal intent to manipulate — place request calls only at meaningful moments (after task completion, after a positive session milestone), not unconditionally.

## Trigger
Invoke on any iOS/macOS project that uses `SKStoreReviewController` or contains review/rating prompt logic.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.

### Phase 2: Checks

1. **requestReview() called in button action**
   `Grep` pattern `requestReview` in `**/*.swift`.
   For each match, `Read` surrounding context — if inside an `@IBAction`, `Button { }` closure, or `.onTapGesture` → 🔴 CRITICAL. Review requests triggered by user button taps are explicitly prohibited by 5.6.1.

2. **Review gating pattern**
   `Grep` pattern `"enjoying"|"like the app"|"happy with"|"satisfied"` near `requestReview` in `**/*.swift`.
   If found in a conditional branch that only calls `requestReview()` when response is positive → 🔴 CRITICAL. Showing the prompt only to satisfied users is review gating.

3. **Custom "Rate Us" button**
   `Grep` pattern `"Rate Us"|"Rate the App"|"Leave a Review"|"rateApp"|"openAppStore.*review"` in `**/*.swift`.
   If a custom rate button navigates directly to the App Store review URL (`itms-apps://...action=write-review`) instead of using `SKStoreReviewController` → 🟠 HIGH. Direct deep-link to write-review bypasses Apple's system controls and may be treated as manipulation.

4. **requestReview() call frequency**
   Count occurrences of `requestReview` in `**/*.swift` — if called in multiple locations without a shared rate-limiting guard → 🟡 MEDIUM. Multiple unguarded call sites risk exceeding Apple's 3-per-year cap and signaling abusive intent.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Review Request Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove requestReview() from button action — review prompts must not be triggered by user taps; move to a post-task completion milestone — `RatingViewController.swift:44` — Guideline 5.6.1
- [ ] TODO: Remove satisfaction gate — show requestReview() equally to all users, not only those who tapped "Yes, I'm enjoying it" — `FeedbackFlow.swift:29` — Guideline 5.6.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Replace direct App Store review deep-link with SKStoreReviewController.requestReview() — `SettingsViewController.swift:88` — Guideline 5.6.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Consolidate requestReview() calls behind a single rate-limiting guard — multiple unguarded call sites signal abusive frequency intent

### 🟢 LOW — Best practice
- [ ] TODO: Trigger requestReview() only after positive session milestones (e.g., after user completes 3 tasks, after a streak) — not on every launch
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- `SKStoreReviewController.requestReview()` automatically respects Apple's cap of 3 prompts per 365-day period — apps cannot override this limit. Calls beyond the cap are silently ignored.

## Quick Commands

```bash
# Find all requestReview() calls with context
!grep -rn "requestReview" . --include="*.swift" -B5 | grep -E "Button|IBAction|onTap|requestReview"

# Check for satisfaction gating near requestReview
!grep -rn "enjoying\|like the app\|satisfied" . --include="*.swift" -A 5 | grep -i "requestReview\|review"

# Check for direct App Store review URL
!grep -rn "write-review\|action=write" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/ReviewRequestPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Grep `SKStoreReviewController.requestReview\|requestReview()` — find all call sites
   - For each call site: check if inside `@IBAction`, button handler, or `touchUpInside` — direct user-triggered request
   - Grep `satisfactionSurvey\|areYouSatisfied\|enjoyingApp\|doYouLikeApp` before `requestReview` — review gating
   - Grep `itms-apps.*action=write-review` — direct write-review deep link

3. **Determine verdict**
   - `requestReview()` inside `@IBAction` or button handler → 🔴 CRITICAL (Guideline 5.6.1)
   - Satisfaction check pattern before `requestReview` → 🔴 CRITICAL (review gating)
   - `write-review` deep link used → 🔴 CRITICAL
   - `requestReview()` called at natural journey moments (no button trigger, no gate) → 🟢 pass

4. **Report**
   - File path + line of `requestReview()` call
   - Context of the call (function name, surrounding code)
   - Fix: Move `requestReview()` to a natural positive moment (e.g., after completing a task); remove satisfaction gate
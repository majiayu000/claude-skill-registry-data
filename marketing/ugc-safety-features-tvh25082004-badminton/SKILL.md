---
name: ugc-safety-features
description: >-
  Detects missing report, block, filter, and contact information mechanisms required for all apps with user-generated content under Guideline 1.2.
---

# Skill: UGC Safety Features
<!-- SEO: user-generated content report button block user EULA content moderation Guideline 1.2 UGC App Store rejection safety -->

## Purpose
Detects missing mechanisms required for apps with user-generated content under Guideline 1.2. Apple explicitly requires **all four** of the following:
1. **Content filtering** — objectionable content must be filterable before it surfaces to other users
2. **Report mechanism** — users must be able to flag offensive posts, comments, and profiles
3. **Block mechanism** — users must be able to block abusive users
4. **Published contact info** — a developer contact method must be accessible within the app for users to report issues directly

## Apple Guideline
- **Primary:** 1.2 — Safety: User Generated Content
- **Related:** 5.1.1(ii)
- **Reference:** `references/guidelines/1-safety.md`

## Real-World Rejection Cases
- **Case:** App with user posts had no "Report" button — rejected under Guideline 1.2
  **Source:** https://developer.apple.com/forums/thread/116703
  **Root cause:** Apps with user-generated content must provide mechanism to report offensive content

- **Case:** iOS app rejected 1.2 Safety — no ability to block abusive users
  **Source:** https://developer.apple.com/forums/thread/78288
  **Root cause:** Guideline 1.2 requires block mechanism, not just report

- **Case:** Community app rejected — no EULA requiring users to agree to content standards
  **Source:** https://buddyboss.com/docs/app-store-guideline-1-2-safety-user-generated-content/
  **Root cause:** Users must agree to terms prohibiting objectionable content

## Trigger
Invoke on any iOS/macOS project that includes user posts, comments, chat, or community features.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/*Feed*` or `**/*Post*` or `**/*Comment*` — locate feed/post UI files.
3. `Glob` `**/*Profile*` or `**/*UserProfile*` — locate profile view files.
4. `Glob` `**/*Onboarding*` or `**/*Registration*` or `**/*Signup*` — locate registration flow files.

### Phase 2: Checks

**Feed/Post Level:**

1. **Report content mechanism**
   `Grep` pattern `"Report"|"reportContent"|"reportPost"|"flagContent"|"reportAction"` in `**/*.swift`.
   If absent → 🔴 CRITICAL. Guideline 1.2 requires a mechanism for users to flag objectionable content.

2. **Block user mechanism**
   `Grep` pattern `"blockUser"|"Block User"|"blockAction"` in `**/*.swift`.
   If absent → 🔴 CRITICAL. Guideline 1.2 explicitly requires ability to block abusive users.

3. **Content filtering/moderation**
   `Grep` pattern `"filterContent"|"moderateContent"|"contentFilter"` in `**/*.swift`.
   If absent → 🟠 HIGH. Indicates no client-side content filtering layer.

**Profile Level:**

4. **Report/block from profile views**
   `Grep` pattern `"Report User"|"Block User"|"reportUser"|"blockUser"` in files matching `*Profile*View*` or `*UserProfile*`.
   If absent while report/block found only in feed, flag → 🟠 HIGH. Guideline 1.2 compliance requires accessibility from profile context as well.

**Developer Contact Info:**

5. **In-app developer contact method**
   `Grep` pattern `"contactUs"|"contact_us"|"Contact Support"|"reportIssue"|"support@"|"mailto:"` in `**/*.swift`.
   If absent → 🟠 HIGH. Guideline 1.2 requires a published contact method accessible within the app — Apple reviewers specifically check whether users can reach the developer to report abuse outside of the in-app report button.

**EULA/Terms:**

6. **Terms of service / EULA acceptance**
   `Grep` pattern `"termsOfService"|"acceptTerms"|"EULA"|"userAgreement"` in `**/*.swift`.
   If absent in any file — and if onboarding/registration flow exists — flag → 🟠 HIGH. Users must explicitly agree to content standards before contributing UGC.

**Age Verification / COPPA (Children's Online Privacy Protection Act):**

7. **Under-13 user handling**
   `Grep` pattern `"ageVerification"|"dateOfBirth"|"age_gate"|"birthDate"|"underAge"|"isMinor"` in `**/*.swift`.
   If app allows user-to-user interaction (chat, follows, public profiles) and no age verification is found → 🟠 HIGH.
   Apps rated 4+ or 9+ that allow strangers to contact each other must either:
   - Implement age verification and block under-13 users from social features, or
   - Be rated 12+ or higher to reflect the actual audience risk.
   COPPA compliance (US law) requires parental consent for users under 13 — Apple may reject apps that allow under-13 UGC without safeguards, independent of the App Store rating.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## UGC Safety Features — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add a "Report" button/action to post and comment views — Guideline 1.2 requires a content reporting mechanism — `FeedViewController.swift`
- [ ] TODO: Add a "Block User" action accessible from post, comment, or profile views — Guideline 1.2 requires ability to block abusive users

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Add EULA/Terms of Service acceptance step in registration flow — users must agree to content standards before posting UGC — Guideline 1.2
- [ ] TODO: Surface report/block actions from UserProfileViewController as well as from feed items — Guideline 1.2

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Add in-app developer contact method (support email or contact form) accessible from settings or profile — Guideline 1.2 requires published contact info alongside report/block

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Implement client-side content filtering or integrate server-side moderation API to handle flagged content

### 🟢 LOW — Best practice
- [ ] TODO: Add contextual reporting categories (e.g., "Spam", "Hate Speech", "Nudity") to improve moderation quality
- [ ] TODO: Establish a 24-hour response SLA for flagged content — Apple expects developers to actively moderate reported content; slow or absent moderation can lead to rejection on resubmission or app removal
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
# Check for report/block mechanisms
!grep -rn "reportContent\|reportPost\|reportUser\|flagContent\|blockUser\|Block User\|Report" . --include="*.swift" | grep -v "//\|BugReport"

# Check for EULA/terms acceptance
!grep -rn "termsOfService\|acceptTerms\|EULA\|userAgreement" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/UGCSafetyPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Grep `reportUser\|reportContent\|flagContent\|reportPost\|ReportUser` — report feature
   - Grep `blockUser\|blockAccount\|ignoreUser\|BlockUser` — block feature
   - Grep `UITableViewCell\|UICollectionViewCell` — check context menu or swipe actions for report/block
   - Grep `contactSupport\|supportEmail\|contactUs\|ContactSupport` — published contact info

3. **Determine verdict**
   - UGC features exist (feed, comments, profiles, chat) + no report pattern → 🔴 CRITICAL (Guideline 1.2)
   - Report found + no block pattern → 🔴 CRITICAL
   - Report + block + contact all present → 🟢 pass

4. **Report**
   - Evidence of UGC (feed/comment/chat code) without safety features
   - Fix: Add report button to each user-generated content item; implement user blocking; add support contact link in Settings

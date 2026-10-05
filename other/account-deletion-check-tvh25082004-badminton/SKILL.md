---
name: account-deletion-check
description: >-
  Detects missing or insufficient in-app account deletion functionality required since June 30, 2022 under Guideline 5.1.1(v) for all apps that support account creation.
---

# Skill: Account Deletion Check
<!-- SEO: account deletion in-app delete user data deactivate Guideline 5.1.1(v) required June 2022 iOS App Store rejection -->

## Purpose
Detects missing or insufficient in-app account deletion functionality required since June 30, 2022 under Guideline 5.1.1(v) for all apps that support account creation.

## Apple Guideline
- **Primary:** 5.1.1(v) — Data Collection and Storage: Account Deletion
- **Related:** 5.1.1(i), 5.1.1(iii)
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** App supporting account creation rejected after June 30, 2022 for not having in-app account deletion
  **Source:** https://developer.apple.com/news/?id=12m75xbj
  **Root cause:** Required since June 30, 2022 — all apps that support account creation must allow deletion within the app, not just via email request or external link

- **Case:** App offered "Deactivate Account" but not true deletion — rejected
  **Source:** Apple Developer Forums thread/254032717
  **Root cause:** Deactivation is not deletion — Apple requires permanent account and data deletion option; temporarily disabling access does not satisfy the requirement

- **Case:** App using Sign in with Apple did not revoke the Apple identity token when user deleted their account — rejected; account deletion was incomplete without credential revocation
  **Source:** Apple TN3194 (developer.apple.com/documentation/technotes/tn3194)
  **Root cause:** Account deletion must include calling Apple's token revocation endpoint to invalidate the Sign in with Apple credential; local-only deletion without server-side token revocation is considered incomplete account deletion

## Trigger
Invoke on any iOS/macOS project that includes user account creation, login, or sign-up flows.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/Settings*View*` or `**/Account*View*` or `**/Profile*View*` — locate account management UI files.
3. `Glob` `**/Auth*` or `**/Login*` or `**/Signup*` or `**/Register*` — locate authentication flow files to confirm account creation exists.

### Phase 2: Checks

1. **Account deletion UI element**
   `Grep` pattern `"deleteAccount"|"Delete Account"|"delete_account"|"deleteUser"|"destroyAccount"|"Delete My Account"|"Remove Account"` in `**/*.swift`.
   If absent → 🔴 CRITICAL. All apps with account creation must offer in-app deletion.

2. **Deactivation-only pattern without true deletion**
   `Grep` pattern `"deactivate"|"suspend"|"disable"` in `**/*.swift` — check account-settings context.
   If "deactivate"/"suspend" found but no "deleteAccount" found → 🔴 CRITICAL. Deactivation alone does not satisfy 5.1.1(v).

3. **Account deletion navigable from settings/profile**
   `Glob` `**/Settings*View*`, `**/Profile*View*`, `**/Account*View*` — `Read` each file.
   Verify a deletion action or navigation link to deletion is present. If account management views exist but deletion option is not surfaced → 🔴 CRITICAL.

4. **Backend deletion API call**
   `Grep` pattern `"deleteAccount"|"DELETE /user"|"DELETE /account"|"DELETE /me"|deleteUser` in `**/*.swift` — check network/API layer.
   If in-app deletion UI exists but no corresponding backend deletion call found → 🟠 HIGH. Account deletion must also erase backend data, not only local state.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Account Deletion Check — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add in-app account deletion option — "Delete Account" action required for all apps with account creation — Guideline 5.1.1(v)
- [ ] TODO: Replace "Deactivate Account" with permanent "Delete Account" — deactivation does not satisfy Apple's deletion requirement — `AccountSettingsView.swift:44` — Guideline 5.1.1(v)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Confirm backend DELETE API is called when user triggers account deletion — no network deletion call found in account management code — `AccountViewModel.swift:112` — Guideline 5.1.1(v)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Display a confirmation dialog explaining what data will be permanently deleted before finalizing account deletion

### 🟢 LOW — Best practice
- [ ] TODO: Follow Apple's account deletion guidance — inform users of any grace period or data retention policy as per applicable laws
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
# Check for account deletion implementation
!grep -rn "deleteAccount\|Delete Account\|delete_account\|destroyAccount\|deleteUser" . --include="*.swift"

# Check for deactivate-only (flag if no delete)
!grep -rn "deactivate\|suspend\|disable" . --include="*.swift" | grep -iv "disabled\|button\|view\|isEnabled"

# Check network layer for DELETE endpoint
!grep -rn "DELETE\|deleteAccount\|delete/user\|delete/account" . --include="*.swift" | grep -v "//"
```

## Swift Anti-Pattern Reference
`examples/swift/PrivacyPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Grep `createAccount\|signUp\|register\|SignUp\|CreateAccount` — confirms account creation exists
   - Grep `deleteAccount\|delete_account\|removeAccount\|accountDeletion\|DeleteAccount` — deletion implementation
   - Grep `deactivate\|suspend\|disable.*[Aa]ccount` — deactivation-only pattern (insufficient)
   - Grep `ASAuthorizationAppleIDProvider\|revokeToken` — Sign in with Apple token revocation

3. **Determine verdict**
   - Account creation found + no deletion pattern → 🔴 CRITICAL (Guideline 5.1.1(v), required since June 30, 2022)
   - Only `deactivate`/`suspend` found without `delete` → 🔴 CRITICAL (deactivation ≠ deletion)
   - Sign in with Apple used + no `revokeToken` → 🟠 HIGH
   - Deletion found + revocation present → 🟢 pass

4. **Report**
   - File where account creation is found (line number)
   - Confirm deletion is absent or only deactivation exists
   - Fix: Implement Settings → Account → Delete Account with server-side data deletion and credential revocation

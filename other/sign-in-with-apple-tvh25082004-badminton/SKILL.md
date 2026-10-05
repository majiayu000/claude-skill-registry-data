---
name: sign-in-with-apple
description: >-
  Detects apps that offer third-party social login without offering Sign in with Apple, violating Guideline 4.8 which requires Sign in with Apple wherever third-party authentication is used.
---

# Skill: Sign in with Apple

<!-- SEO: Sign in with Apple required third-party login social auth Google Facebook Twitter OAuth Guideline 4.8 iOS App Store rejection -->

## Purpose
Detects apps that offer third-party social login (Google, Facebook, Twitter/X, etc.) without offering Sign in with Apple, violating Guideline 4.8 — which requires Sign in with Apple wherever third-party authentication is used.

## Apple Guideline
- **Primary:** 4.8 — Design: Sign in with Apple
- **Related:** 5.1.1(i)
- **Reference:** `references/guidelines/4-design.md`

## Real-World Rejection Cases
- **Case:** App offered Google Sign-In and Facebook Login as the only login options — rejected under Guideline 4.8
  **Source:** Apple Developer Forums (multiple threads, 2020–2024)
  **Root cause:** Guideline 4.8 requires apps that use third-party or social login to also offer Sign in with Apple as an equivalent option. Apple enforced this starting June 30, 2020.

- **Case:** App updated to add Instagram OAuth login — Apple rejected the update for missing Sign in with Apple, even though the app had previously passed review without it
  **Source:** Developer experience, 2023
  **Root cause:** Adding any new third-party auth method after the June 2020 deadline triggers the Sign in with Apple requirement for the entire app.

- **Case:** App used "Login with Twitter" for a social feature — rejected; developer assumed the rule didn't apply to secondary/optional login methods
  **Source:** Apple Developer Forums
  **Root cause:** The rule applies to any third-party authentication — not just the primary login, but also secondary social login options like Twitter, LinkedIn, or GitHub.

- **Case:** App offered only Facebook Login as the sole authentication option — developer believed Sign in with Apple was only required when offering multiple social login providers — rejected under Guideline 4.8
  **Source:** Apple Developer Forums (multiple developer reports, 2020–2024)
  **Root cause:** Sign in with Apple is required whenever any third-party or social authentication is offered, regardless of whether it is the only login option or one of several — offering a single social provider does not exempt the app from Guideline 4.8

- **Case:** React Native app using react-native-auth0 rendered Sign in with Apple button with a gray border — Apple reviewer flagged non-compliant button styling and rejected
  **Source:** Auth0 Community / react-native-auth0 GitHub issue #310
  **Root cause:** Sign in with Apple button must use ASAuthorizationAppleIDButton with no custom border, shadow, or color modifications; any deviation from Apple's button styling guidelines is grounds for rejection

- **Case:** App using Sign in with Apple did not revoke the Apple identity token when user deleted their account — rejected under account deletion and Sign in with Apple requirements
  **Source:** Apple TN3194 (developer.apple.com/documentation/technotes/tn3194)
  **Root cause:** When a user deletes their account in-app, the app must call Apple's token revocation endpoint to invalidate the Sign in with Apple credential; failing to revoke violates both Guideline 5.1.1(v) and the Sign in with Apple specification

## Trigger
Invoke on any iOS/macOS project that includes social login, OAuth flows, or third-party authentication.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/Podfile` and `**/Package.resolved` — check for third-party auth SDK dependencies.
3. `Glob` `**/*Login*` `**/*Auth*` `**/*SignIn*` `**/*OAuth*` — locate authentication flow files.

### Phase 2: Checks

1. **Third-party auth SDK detection**
   `Grep` pattern `GoogleSignIn|GIDSignIn|FBSDKLoginKit|FacebookLogin|TwitterKit|TwitterAuthProvider|GithubAuthProvider|OAuthProvider|LinkedInAuth|AmazonAuth|WeChatAuth` in `**/*.swift` and dependency files.
   If any match found → proceed to check 2.

2. **Sign in with Apple presence**
   `Grep` pattern `ASAuthorizationAppleIDProvider|AuthenticationServices|ASAuthorization|SignInWithApple|signInWithApple` in `**/*.swift`.
   If third-party auth detected (check 1) but Sign in with Apple absent → 🔴 CRITICAL.

3. **Sign in with Apple button usage**
   `Grep` pattern `ASAuthorizationAppleIDButton|SignInWithAppleButton` in `**/*.swift`.
   If Sign in with Apple code exists but no Apple button found → 🟠 HIGH. The official `ASAuthorizationAppleIDButton` or SwiftUI `SignInWithAppleButton` must be used — custom-styled buttons that don't meet Apple's guidelines are rejected.

4. **AuthenticationServices import**
   `Grep` pattern `import AuthenticationServices` in `**/*.swift`.
   If third-party auth present but `AuthenticationServices` not imported → 🔴 CRITICAL.

5. **Credential state handling**
   `Grep` pattern `getCredentialState|ASAuthorizationAppleIDProvider.*getCredentialState` in `**/*.swift`.
   If Sign in with Apple is implemented but credential state check absent → 🟠 HIGH. Apps must check the Sign in with Apple credential state at launch to handle revoked credentials gracefully.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Sign in with Apple — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add Sign in with Apple — GoogleSignIn detected but ASAuthorizationAppleIDProvider absent — Guideline 4.8
- [ ] TODO: Import AuthenticationServices and implement ASAuthorizationAppleIDProvider — `AuthViewModel.swift:12` — Guideline 4.8

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Replace custom Apple login button with ASAuthorizationAppleIDButton or SwiftUI SignInWithAppleButton — custom styling not permitted — `LoginView.swift:55` — Guideline 4.8
- [ ] TODO: Add credential state check at app launch — handle revoked Sign in with Apple credentials — `AppDelegate.swift` — Guideline 4.8

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Verify Sign in with Apple is presented with equal visual prominence to other social login options — Guideline 4.8

### 🟢 LOW — Best practice
- [ ] TODO: Handle the case where a user's Apple ID credential is revoked — sign them out gracefully rather than crashing
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Exception: Apps that only use username/password login (no third-party OAuth) do **not** require Sign in with Apple.
- Exception: Apps used exclusively by employees or enterprise accounts are exempt.

## Quick Commands

Run these in your project root to check manually:

```bash
# Check for third-party auth SDKs
!grep -rn "GoogleSignIn\|GIDSignIn\|FBSDKLogin\|FacebookLogin\|TwitterKit\|OAuthProvider" . --include="*.swift" | grep -v "//"

# Check for Sign in with Apple implementation
!grep -rn "ASAuthorizationAppleIDProvider\|AuthenticationServices\|SignInWithAppleButton" . --include="*.swift"

# Check for Apple login button (required visual component)
!grep -rn "ASAuthorizationAppleIDButton\|SignInWithAppleButton" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/SubscriptionPatterns.swift` (auth flow patterns)

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/project.pbxproj`, `**/Info.plist`

2. **Search for rejection patterns**
   - Grep `GIDSignIn\|GoogleSignIn\|FBSDKLoginButton\|LoginWithAmazon\|TwitterAuthProvider` — third-party auth SDKs
   - Grep `ASAuthorizationAppleIDButton\|SignInWithAppleButton` — Apple sign-in button
   - Grep `ASAuthorizationAppleIDProvider\|ASAuthorizationController` — Apple auth implementation
   - Grep `getCredentialState\|credentialState.*revoked` — credential state handling

3. **Determine verdict**
   - Third-party auth SDK found + no `ASAuthorizationAppleIDButton` → 🔴 CRITICAL (Guideline 4.8)
   - `ASAuthorizationAppleIDButton` present but no `getCredentialState` handling → 🟠 HIGH
   - Apple Sign-In implemented with credential state handling → 🟢 pass

4. **Report**
   - File path + line of third-party auth without Apple alternative
   - Fix: Add `ASAuthorizationAppleIDButton` alongside existing login options; implement `ASAuthorizationAppleIDProvider().getCredentialState` on app launch
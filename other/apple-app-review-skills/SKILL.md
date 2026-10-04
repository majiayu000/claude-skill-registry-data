---
name: apple-app-review-skills
description: >
  App Store rejection prevention for iOS/macOS apps.
  Covers privacy, UGC, IAP, metadata, layout, and quality checks
  based on real Apple rejection cases.
compatibility: Claude Code (or similar products)
version: 1.0.0
---

# apple-app-review-skills

A Claude Code skill set for iOS/macOS App Store rejection prevention.
Skills across 7 categories, grounded in real Apple rejection cases and official guidelines (sections 1–5).

## When to Use This Skill Set

Use these skills when:
- Preparing an iOS/macOS app for App Store submission
- Investigating a rejection or appeal
- Referencing an Apple guideline section (1.x – 5.x)
- Auditing privacy, UGC, IAP, metadata, layout, or code quality

## Routing

Identify the user's intent, then load **only the matching skill** — never load all skills at once.

### Full audit → run the agent

If the user wants a complete pre-submission check:
→ Use `agents/appstore-full-audit.md`

### Targeted agents → scoped multi-skill audit

For category-scoped audits that run multiple skills together:

| User need | Agent |
|-----------|-------|
| All iPad layout, Dynamic Type, orientation, safe area checks | `agents/ipad-layout-agent.md` |
| All permission string and timing checks | `agents/permission-audit-agent.md` |
| All privacy policy, manifest, ATT, account deletion checks | `agents/privacy-audit-agent.md` |
| All UGC report/block/filter checks | `agents/ugc-safety-agent.md` |

### Targeted → load one skill by category

| Category | When to route here | Skills |
|----------|--------------------|--------|
| **quality** | Private/deprecated APIs, SDK version, push notifications, review manipulation, background execution, crash risk, app completeness, submission readiness | `sdk-version-check`, `private-api-audit`, `push-notification-audit`, `review-request-audit`, `background-execution-audit`, `crash-risk-audit`, `app-completeness-check`, `review-readiness-check` |
| **privacy** | AI data sharing consent, PrivacyInfo.xcprivacy, ATT, data minimization, account deletion, privacy policy | `ai-data-disclosure`, `privacy-manifest-check`, `att-framework-audit`, `data-minimization-audit`, `account-deletion-check`, `privacy-policy-check` |
| **business** | In-app purchases, Sign in with Apple, loot boxes, subscriptions | `iap-compliance`, `sign-in-with-apple`, `loot-box-disclosure`, `subscription-disclosure` |
| **metadata** | App Store description, screenshots, age rating, app name | `metadata-accuracy`, `age-rating-accuracy`, `app-name-compliance`, `screenshot-guidelines` |
| **ugc** | User-generated content moderation, report/block features | `ugc-safety-features`, `content-moderation-api` |
| **layout** | iPad layout, Dynamic Type, orientation, safe areas | `ipad-layout-audit`, `dynamic-type-support`, `orientation-support`, `safe-area-compliance` |
| **permissions** | NSUsageDescription strings, permission timing, scope | `usage-description-audit`, `permission-scope-audit`, `request-timing-audit` |

Total: 8 + 6 + 4 + 4 + 2 + 4 + 3 = **31 skills**

## Routing Examples

| User says | Route to |
|-----------|----------|
| "Check my app before App Store submission" | `agents/appstore-full-audit.md` |
| "Is my UIWebView usage going to cause rejection?" | `skills/quality/sdk-version-check.md` |
| "Do I need to disclose that I'm using OpenAI?" | `skills/privacy/ai-data-disclosure.md` |
| "My push notification was rejected" | `skills/quality/push-notification-audit.md` |
| "Does my subscription paywall comply?" | `skills/business/subscription-disclosure.md` |
| "I use Facebook login — do I need Sign in with Apple?" | `skills/business/sign-in-with-apple.md` |
| "My app has a chat feed — what UGC requirements apply?" | `skills/ugc/ugc-safety-features.md` |
| "Check my iPad layout" | `skills/layout/ipad-layout-audit.md` |
| "Review my privacy policy" | `skills/privacy/privacy-policy-check.md` |

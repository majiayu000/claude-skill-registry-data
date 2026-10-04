---
name: apple
description: Complete Apple platform development toolkit — iOS, macOS, watchOS, Swift, SwiftUI, StoreKit, ASO, legal, security, testing, and growth. Install for any Apple-platform project.
---

# Apple Platform Toolkit

**20 specialized skills for Apple platform development**, covering the full lifecycle from idea to App Store.

## Sub-Skills

| Module                         | Triggers                                                                                       | Description                                                                      |
| ------------------------------ | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `app-store`                    | "App Store description", "ASO keywords", "review response"                                     | ASO, descriptions, keywords, review responses                                    |
| `apple-intelligence`           | "Apple Intelligence", "Foundation Models", "on-device AI"                                      | Foundation Models, Visual Intelligence, App Intents                              |
| `core-ml`                      | "Core ML", "Create ML", "Vision framework"                                                     | On-device ML — image classification, object detection                            |
| `design`                       | "Liquid Glass", "Apple design system", "SwiftUI animations"                                    | Liquid Glass, HIG, modern Apple visual design                                    |
| `generators`                   | "generate Swift code", "add paywall", "add push notifications"                                 | 40+ production-ready Swift component generators                                  |
| `growth`                       | "grow my app", "indie dev marketing", "user acquisition"                                       | User acquisition, analytics, press, community                                    |
| `ios`                          | "iOS best practices", "SwiftUI review", "HIG review"                                           | Swift/SwiftUI patterns, HIG audit, accessibility                                 |
| `legal`                        | "privacy policy", "terms of service", "GDPR compliance"                                        | Privacy policies, ToS, EULAs, GDPR/CCPA                                          |
| `macos`                        | "macOS development", "AppKit", "macOS 26", "Tahoe APIs"                                        | Swift 6+, SwiftUI, AppKit bridging, macOS 26 Tahoe                               |
| `monetization`                 | "monetize my app", "StoreKit", "subscription pricing"                                          | Pricing models, IAP, StoreKit implementation                                     |
| `product`                      | "app PRD", "market research", "competitive analysis"                                           | PRD, market research, UX design, App Store release                               |
| `release-review`               | "pre-submission review", "App Store review prep"                                               | Security, privacy, UX review before submission                                   |
| `security`                     | "iOS security", "Keychain", "biometric auth"                                                   | Secure storage, biometrics, network security                                     |
| `shared`                       | "create skill", "skill template"                                                               | Skill creation templates and best practices                                      |
| `swift`                        | "Swift concurrency", "async/await", "Swift best practices"                                     | Concurrency, performance, modern Swift idioms                                    |
| `testing`                      | "TDD iOS", "Swift testing", "snapshot tests"                                                   | TDD workflows, characterization tests, test infra                                |
| `watchos`                      | "watchOS development", "complications", "SwiftUI Watch"                                        | SwiftUI for Watch, Watch Connectivity, complications                             |
| `macos-accessibility`          | "AXUIElement", "macOS accessibility", "TCC permission", "automate Mac app"                     | macOS app automation via Accessibility API — TCC, code signing, action execution |
| `aso-appstore-screenshots`     | "App Store screenshots", "ASO screenshots", "generate screenshots", "App Store Connect images" | Two-stage AI screenshot generator — Pillow compose + Nano Banana Pro enhance     |
| `cinematic-onboarding-swiftui` | "cinematic onboarding", "animated onboarding SwiftUI", "iOS first-launch flow"                 | SwiftUI onboarding — cross-fade steps, animated progress, rotating testimonials  |

## How Claude Routes Requests

When a request matches a trigger above, Claude reads the relevant sub-skill's `SKILL.md` via `${CLAUDE_SKILL_DIR}/<module>/SKILL.md` and applies its guidance. No explicit sub-skill activation needed — just ask naturally.

## Install

```bash
# From claude-toolkit root:
ln -sfn "$HOME/Projects/Dev_projects/Claude_SDK/claude-toolkit/skills/apple" \
        "<project>/.claude/skills/apple"
```

Or use `install-toolkit-skills` → choose "apple" from the list.

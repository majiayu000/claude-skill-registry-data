---
name: "tech-hiring-mobile-engineering"
description: "Mobile engineers build native and cross-platform mobile applications for iOS and Android. The discipline requires platform-specific knowledge (UI paradigms, app store constraints, hardware access) alongside software engineering fundamentals"
---

# Mobile Engineering — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Mobile Engineering

### What This Role Does
Mobile engineers build native and cross-platform mobile applications for iOS and Android. The discipline requires platform-specific knowledge (UI paradigms, app store constraints, hardware access) alongside software engineering fundamentals. Cross-platform skills (React Native, Flutter) are increasingly common but platform-native depth remains valued for performance-critical work.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Junior iOS Developer, Junior Android Developer, Mobile Engineer |
| Mid | iOS Engineer, Android Engineer, Mobile Software Engineer |
| Senior | Senior iOS Engineer, Senior Android Engineer, Senior Mobile Engineer |
| Staff+ | Staff Mobile Engineer, Principal Mobile Engineer, Mobile Architect |
| Cross-platform | React Native Engineer, Flutter Developer, Mobile Engineer (Cross-platform) |

### Skill Tiers

**Tier 1 — Must-have (iOS):**
- Swift (modern, not just Objective-C legacy)
- UIKit or SwiftUI (ideally both — know when to use each)
- Xcode, debugging, Instruments for profiling
- App lifecycle, push notifications, background tasks
- App Store submission, TestFlight, provisioning profiles

**Tier 1 — Must-have (Android):**
- Kotlin (modern; Java is legacy — acceptable but not preferred for new hires)
- Jetpack Compose or XML/View-based UI (Compose increasingly standard)
- Android Studio, ADB, profiling tools
- App lifecycle, background services, notification channels
- Google Play submission, signing, ProGuard/R8

**Tier 2 — Differentiator:**
- Performance optimisation: battery, memory, startup time
- Offline-first architecture: local storage, sync strategies, conflict resolution
- Accessibility: VoiceOver (iOS), TalkBack (Android)
- Deep linking, universal links, push notification handling
- Unit and UI testing: XCTest/XCUITest (iOS), Espresso/JUnit (Android)

**Tier 3 — Bonus:**
- Cross-platform React Native or Flutter on top of native skills
- Bluetooth, NFC, ARKit/ARCore, camera pipelines
- Published apps with significant user bases
- Open source mobile library contributions

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("iOS engineer" OR "iOS developer" OR "Swift developer" OR "mobile engineer") (Swift OR SwiftUI OR Xcode) -recruiter -talent

site:linkedin.com/in/ ("Android engineer" OR "Android developer" OR "Kotlin developer" OR "mobile engineer") (Kotlin OR "Jetpack Compose" OR Android) -recruiter -talent

# Cross-platform
site:linkedin.com/in/ ("React Native" OR "Flutter developer" OR "mobile engineer") ("cross-platform" OR "React Native" OR Flutter) -recruiter

# GitHub
language:swift followers:>20 pushed:>2025-01-01
language:kotlin followers:>20 pushed:>2025-01-01
```

### Seniority Signals

- **Junior → Mid:** Can own a feature screen to screen — design handoff through to App Store build
- **Mid → Senior:** Identifies platform-specific edge cases, performance bottlenecks, and release risks that others miss; mentors on platform idioms
- **Senior → Staff:** Defines mobile architecture, SDK strategy, cross-platform decisions, and CI/CD for mobile; reduces release cycle time

### Red Flags
- "I mainly do React Native" when you need native performance (valid for many products, wrong for others — clarify your needs)
- No testing experience — mobile UI testing has a high bar
- Never handled a production crash report or performance regression
- Last iOS app was built for iOS 13 — has not kept up with SwiftUI or modern APIs
- No understanding of App Store review process or rejection patterns

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $90k – $125k |
| Mid | $125k – $165k |
| Senior | $155k – $215k |
| Staff | $195k – $265k |
| Principal | $235k – $310k+ |

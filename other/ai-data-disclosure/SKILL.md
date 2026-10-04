---
name: ai-data-disclosure
description: >-
  Detects apps that send user data to third-party AI systems without explicit in-app consent and disclosure, enforcing Guideline 5.1.2(i).
---

# Skill: AI Data Disclosure
<!-- SEO: third-party AI ChatGPT OpenAI Gemini Anthropic data sharing consent disclosure privacy 5.1.2(i) iOS App Store rejection -->

## Purpose
Detects apps that send user data to third-party AI systems (OpenAI, Google Gemini, Anthropic, etc.) without explicit in-app consent and disclosure, enforcing Guideline 5.1.2(i) which requires transparency before any user data is transmitted to external AI services.

## Apple Guideline
- **Primary:** 5.1.2(i) — Privacy: Third-Party AI Data Sharing
- **Related:** 5.1.1(i) — Privacy Policy
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** App sent user messages to OpenAI API without disclosing this in the app or privacy policy — rejected under 5.1.2(i)
  **Source:** Apple Developer Forums (multiple developer reports, 2023–2024)
  **Root cause:** Guideline 5.1.2(i) requires explicit disclosure and user consent before transmitting data to any third-party AI system — a generic "we may share data with service providers" clause in the privacy policy is insufficient; the app must present a clear in-app notice before AI processing occurs

- **Case:** Health app transcribed user speech on-device and then sent transcripts to a third-party LLM for analysis — rejected for undisclosed AI data sharing
  **Source:** Apple Developer Forums (2024)
  **Root cause:** Any transmission of user-provided content to an external AI service requires explicit opt-in consent, regardless of whether the data was first processed on-device — the forwarding to an external AI is the disclosure trigger

## Trigger
Invoke on any iOS/macOS project that integrates AI/ML APIs, chat features, or sends user-generated content to external services.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/Podfile` `**/Package.resolved` — locate dependency manifests for AI SDK detection.
3. `Glob` `**/*Privacy*` `**/*privacy*` `**/PrivacyPolicy*` — locate privacy policy documents.

### Phase 2: Checks

1. **Third-party AI SDK or endpoint detection**
   `Grep` pattern `OpenAI|openai|ChatGPT|chatgpt|GoogleGenerativeAI|GenerativeAI|Anthropic|anthropic|Cohere|cohere|HuggingFace|mistral` in `**/*.swift` and dependency manifests.
   Also `Grep` `"api\.openai\.com"|"generativelanguage\.googleapis\.com"|"api\.anthropic\.com"|"openrouter\.ai"` in `**/*.swift`.
   If any match found → proceed to checks 2–4.

2. **Explicit AI data consent / disclosure UI**
   `Grep` pattern `aiConsent|ai_consent|AIDisclosure|aiDisclosure|dataSharingAI|processedByAI|thirdPartyAI|aiDataUsage` in `**/*.swift`.
   If AI SDK/API detected (check 1) but consent pattern absent → 🔴 CRITICAL. Apps must present explicit disclosure before sending user data to any third-party AI system.

3. **Privacy policy AI disclosure**
   `Grep` pattern `"AI"|"artificial intelligence"|"language model"|"OpenAI"|"Gemini"|"third-party AI"` in privacy policy files.
   If AI APIs are used but privacy policy does not mention AI data sharing → 🟠 HIGH. The privacy policy must specifically disclose which AI services receive user data and why.

4. **Sensitive data + AI combination**
   `Grep` pattern `HKHealthStore|CMMotionActivity|CNContact|CLLocation` in `**/*.swift`.
   If health, motion, contacts, or precise location data is accessed AND third-party AI is present → 🟠 HIGH. Sending sensitive categories to AI services requires heightened disclosure and explicit opt-in.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## AI Data Disclosure — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add explicit in-app disclosure and user consent before sending data to OpenAI API — users must opt in before any content is transmitted to a third-party AI system — `ChatViewModel.swift:45` — Guideline 5.1.2(i)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Update privacy policy to explicitly disclose OpenAI data sharing — generic "third-party services" language is insufficient — Guideline 5.1.2(i)
- [ ] TODO: Add heightened consent for health data being processed by an external AI — `HealthChatService.swift:22` — Guideline 5.1.2(i)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Consider on-device alternatives (Core ML, Apple Intelligence APIs) for AI features — avoids third-party disclosure requirements entirely

### 🟢 LOW — Best practice
- [ ] TODO: Allow users to opt out of AI-assisted features without losing core app functionality — granular consent improves compliance posture
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- On-device ML using Core ML, Create ML, or Apple's on-device frameworks (Vision, NaturalLanguage, Sound Analysis) does **not** trigger this guideline — only external API calls to third-party AI services.

## Quick Commands

```bash
# Check for AI SDK dependencies
!grep -rn "OpenAI\|openai\|GoogleGenerativeAI\|Anthropic\|anthropic\|ChatGPT" . --include="*.swift" --include="Podfile" --include="Package.resolved" | grep -v "//"

# Check for AI API endpoints
!grep -rn "api\.openai\.com\|generativelanguage\.googleapis\|api\.anthropic\.com" . --include="*.swift"

# Check for consent/disclosure UI patterns
!grep -rn "aiConsent\|AIDisclosure\|dataSharingAI\|processedByAI" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/AIDisclosurePatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/Podfile`, `**/Package.swift`

2. **Search for rejection patterns**
   - Grep `OpenAI\|openai\|GPT\|ChatGPT` — OpenAI SDK or API usage
   - Grep `GoogleGenerativeAI\|gemini\|Gemini` — Google Gemini usage
   - Grep `Anthropic\|claude\|Claude` — Anthropic SDK usage
   - Grep `URLSession.*openai\.com\|URLRequest.*anthropic\.com` — direct API calls
   - Grep `aiDisclosure\|aiConsent\|dataSharing.*AI\|AIDataSharing` — disclosure UI implementation

3. **Determine verdict**
   - Any AI SDK/API found + no disclosure UI (`aiDisclosure`/`aiConsent`) → 🔴 CRITICAL (Guideline 5.1.2(i))
   - AI SDK found + disclosure present but generic privacy policy only → 🟠 HIGH
   - Explicit in-app disclosure naming the AI provider found → 🟢 pass

4. **Report**
   - File path + line where AI SDK is imported or API is called
   - Fix: Present an explicit modal before first API call naming the provider (e.g., "This app uses OpenAI to process your messages") with affirmative consent button

---
name: content-moderation-api
description: >-
  Detects absence of a content moderation service integration for apps that accept user-uploaded media or posts, enforcing Guideline 1.2's requirement for timely response to content reports.
---

# Skill: Content Moderation API
<!-- SEO: content moderation API image upload UGC review response objectionable AWS Rekognition Perspective OpenAI moderation Guideline 1.2 iOS -->

## Purpose
Detects absence of a content moderation service integration for apps that accept user-uploaded media or posts, enforcing Guideline 1.2's requirement for timely response to content reports.

## Apple Guideline
- **Primary:** 1.2 — Safety: User Generated Content
- **Related:** 5.1.1(ii)
- **Reference:** `references/guidelines/1-safety.md`

## Real-World Rejection Cases
- **Case:** Image-sharing app with no content moderation — reviewer uploaded test image, flagged as objectionable, no moderation response
  **Source:** Apple Developer Forums
  **Root cause:** 1.2 requires timely response to content reports; no moderation backend means inability to comply — reviewer demonstrated the gap by submitting a test report with no visible effect

- **Case:** Video sharing app rejected — users could upload videos that were immediately public with no pre-publication moderation or post-report takedown mechanism
  **Source:** Apple Developer Forums (Guideline 1.2 rejection threads, multiple reports 2022–2023)
  **Root cause:** For video/media UGC apps, Apple expects either pre-publication screening or a visible and functional post-publication reporting mechanism with timely follow-through. Guideline 1.2 explicitly states apps must "have a mechanism for users to flag objectionable content" and "take action against objectionable content."

- **Case:** Social app had a moderation backend but it only processed text content — profile photos and user bio fields had no moderation — rejected
  **Source:** Apple Developer Forums (Guideline 1.2 rejection threads)
  **Root cause:** Guideline 1.2 compliance applies to all user-generated surfaces in the app, not only the primary feed. Reviewers test all UGC vectors including profile photos, bios, and display names. Partial coverage of only one content type is insufficient.

## Trigger
Invoke on any iOS/macOS project that allows users to upload images, videos, text posts, or comments.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/*.plist` — collect property list files for API key references.
3. `Glob` `**/*.json` — collect configuration files for moderation service configuration.

### Phase 2: Checks

1. **Moderation service integration**
   `Grep` pattern `"perspective"|"openai"|"AWS Rekognition"|"rekognition"|"Hive"|"moderationAPI"|"contentModerat"|"sightengine"|"Clarifai"` in `**/*.swift`.
   If none found, flag → 🟠 HIGH. No recognized moderation service integration detected.

2. **Media upload without moderation call**
   `Grep` pattern `uploadImage|uploadMedia|postContent|uploadVideo|uploadFile` in `**/*.swift`.
   For each match, `Read` surrounding context — if no nearby call to a moderation API or no moderation flag check, flag → 🟠 HIGH. Media should be scanned before or immediately after upload.

3. **Publisher contact reachability**
   `Grep` pattern `"contactEmail"|"supportEmail"|"contactUs"|"support@"|"help@"` in `**/*.swift`.
   If absent → 🟡 MEDIUM. Apple reviewers expect a visible, reachable contact method for content issues. Absence may raise questions about developer responsiveness to reports.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Content Moderation API — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 1.2

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Integrate a content moderation service (e.g., AWS Rekognition, Google Perspective, OpenAI Moderation API) — no moderation backend detected — Guideline 1.2
- [ ] TODO: Add moderation check after uploadImage call — uploaded content is not scanned for objectionable material — `MediaUploadService.swift:88` — Guideline 1.2

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Add a visible support/contact email address accessible in-app so reviewers and users can reach the moderation team

### 🟢 LOW — Best practice
- [ ] TODO: Implement pre-upload client-side hashing against known objectionable content databases (PhotoDNA equivalent) for additional protection
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
# Check for moderation service integration
!grep -rn "moderat\|perspective\|rekognition\|hive\|contentFilter" . --include="*.swift" -i

# Check for media upload without moderation
!grep -rn "uploadImage\|uploadMedia\|uploadVideo\|postContent" . --include="*.swift"

# Check for publisher contact info
!grep -rn "contactEmail\|supportEmail\|support@\|contactUs" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/UGCSafetyPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/Podfile`, `**/Package.swift`

2. **Search for rejection patterns**
   - Grep `perspectiveAPI\|contentModeration\|filterContent\|moderateText\|ContentModeration` — moderation backend
   - Grep `profanity\|obscenity\|inappropriate\|ProfanityFilter` — client-side filter
   - Grep `EULAAccepted\|termsAccepted\|agreedToTerms\|TermsAccepted` — terms acceptance flow
   - Grep `userGeneratedContent\|UGCContent\|postContent` — UGC submission path

3. **Determine verdict**
   - UGC submission path found + no moderation integration → 🟠 HIGH (Guideline 1.2)
   - Moderation present + no terms acceptance → 🟡 MEDIUM
   - Moderation + terms acceptance present → 🟢 pass

4. **Report**
   - UGC submission code without moderation
   - Fix: Integrate content moderation API (e.g., Perspective API, AWS Rekognition) or implement server-side filtering; add EULA acceptance before first UGC post

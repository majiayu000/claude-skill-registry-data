---
name: store-publishing
description: >-
  Provides App Store and Google Play publishing requirements, metadata management,
  screenshot specifications, review guidelines, and compliance requirements.
  Use when user asks about publishing apps, store requirements, app review, or store metadata.
version: 1.0.0
---

# Store Publishing Guide

Requirements and best practices for App Store and Google Play publishing.

## App Store Connect (iOS)

### Required Metadata
- App name (30 characters max)
- Subtitle (30 characters max)
- Description (4000 characters max)
- Keywords (100 characters, comma-separated)
- Support URL
- Marketing URL (optional)
- Privacy Policy URL (required)

### Screenshots Required

| Device | Size | Required |
|--------|------|----------|
| iPhone 6.7" | 1290 x 2796 | Yes |
| iPhone 6.5" | 1284 x 2778 | Yes |
| iPhone 5.5" | 1242 x 2208 | Optional |
| iPad Pro 12.9" | 2048 x 2732 | If iPad supported |

### App Review Guidelines
- No placeholder content
- Complete functionality
- Accurate screenshots
- Clear privacy policy
- No hidden features
- Proper age rating

### Common Rejection Reasons
1. Incomplete information
2. Bugs or crashes
3. Placeholder content
4. Misleading screenshots
5. Privacy policy issues
6. Guideline 4.2 (minimum functionality)

## Google Play Console (Android)

### Required Metadata
- App name (50 characters max)
- Short description (80 characters max)
- Full description (4000 characters max)
- Application type
- Category
- Content rating
- Privacy policy URL

### Graphics Required

| Asset | Size | Format |
|-------|------|--------|
| App icon | 512 x 512 | PNG (32-bit) |
| Feature graphic | 1024 x 500 | PNG/JPEG |
| Phone screenshots | 16:9 or 9:16 | PNG/JPEG |
| Tablet screenshots | 16:9 or 9:16 | If tablet supported |

### Release Tracks

| Track | Purpose | Review |
|-------|---------|--------|
| Internal | Team testing | No review |
| Closed | Limited testers | No review |
| Open | Public beta | Light review |
| Production | Public release | Full review |

### Data Safety Declaration
Required information about:
- Data collection practices
- Data sharing
- Security practices
- Data deletion options

## Pre-Submission Checklist

### iOS
- [ ] App icon (1024x1024)
- [ ] Screenshots for required devices
- [ ] Privacy policy URL accessible
- [ ] App description complete
- [ ] Keywords optimized
- [ ] Age rating set
- [ ] In-app purchases configured (if any)
- [ ] Export compliance answered

### Android
- [ ] App icon (512x512)
- [ ] Feature graphic
- [ ] Screenshots uploaded
- [ ] Privacy policy URL
- [ ] Content rating questionnaire completed
- [ ] Data safety form completed
- [ ] Target API level compliance
- [ ] App signing by Google Play enabled

## Store Listing Best Practices

### App Name
- Include main keyword
- Keep concise and memorable
- Avoid generic terms

### Description
- First 1-2 lines most important
- Include key features
- Use bullet points
- Add call to action
- Include keywords naturally

### Screenshots
- Show actual app screens
- Add captions/overlays
- Highlight key features
- Use consistent style
- First screenshot most important

## Version Management

### Semantic Versioning
```
MAJOR.MINOR.PATCH+BUILD
1.2.3+45
```

### iOS Build Numbers
- Must increment for each upload
- Use CI build number

### Android Version Codes
- Integer, must increment
- Use formula: `MAJOR*10000 + MINOR*100 + PATCH`

## Release Notes Template

```markdown
## What's New in Version X.Y.Z

### New Features
- Feature 1 description
- Feature 2 description

### Improvements
- Improvement 1
- Improvement 2

### Bug Fixes
- Fixed issue with...
- Resolved crash when...
```

For automated store submissions, use the `/flutter-deploy` command.

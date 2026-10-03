---
name: apple-design-privacy-identity
description: "Design Apple app privacy and identity flows: contextual permissions, account creation and deletion, Sign in with Apple, and in-person ID verification. Focuses on user experience rather than backend security implementation."
---

# Apple Privacy and Identity UX

## Apply the skill

Map the requested data to the user-facing benefit and the exact moment it becomes necessary. Read the applicable reference, then design the granted, declined, unavailable, and revoked paths. Keep explanations specific and truthful.

Separate account creation, authentication, consent, and identity verification; one does not imply the others. Preserve private relay addresses, show only available authentication methods, and make account deletion understandable when relevant.

Use system-provided permission and authentication interfaces. Consult current official requirements for implementation, data handling, and eligibility rather than interpreting HIG guidance as a complete security or legal specification. Design work does not authorize collecting data or verifying a real person.

## Topic references

Select the topic that matches the design decision; do not load this entire list by default.

- [Privacy](references/privacy.md)
- [Managing accounts](references/managing-accounts.md)
- [Sign in with Apple](references/sign-in-with-apple.md)
- [ID Verifier](references/id-verifier.md)

## Source use

These references are original operational summaries of Apple’s public HIG, checked on 2026-09-08. They are guidance for design decisions, not a reproduced manual or a guarantee of App Store acceptance.

Read only the topic references relevant to the current task. Each links to the full official page. Consult that page for exact specifications, platform exceptions, assets, and version-sensitive behavior; use current official developer documentation for APIs and availability. If live documentation is unavailable, state the snapshot date and identify assumptions instead of inventing current requirements.

The user’s product goals, selected framework, and authorized scope remain controlling. Distinguish a source recommendation from a hard platform requirement and from your own proposed implementation.

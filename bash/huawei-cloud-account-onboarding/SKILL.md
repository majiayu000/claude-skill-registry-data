---
name: huawei-cloud-account-onboarding
description:
  Checks Huawei Cloud real-name verification status and guides face-scan verification read-only
  through hcloud. Use for Huawei Cloud verification status, real-name onboarding, or flows blocked
  on verification. Accepts no identity documents, bank details, or SMS codes; refuses writes and
  non-Huawei-Cloud identity workflows.
metadata:
  language: en
  translation_of: huawei-cloud-account-onboarding-cn
  version: "1.0.3"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/en/huawei-cloud-account-onboarding
    envVars:
      - { name: HUAWEICLOUD_SDK_AK, required: false }
      - { name: HUAWEICLOUD_SDK_SK, required: false }
---

# Huawei Cloud Account Onboarding

> Community edition, not an official Huawei Cloud skill. Treat the current hcloud response as
> authoritative.

Use **hcloud 7.2 or later** to check the current account's real-name status and type read-only.
A verified result satisfies the real-name prerequisite; it does not establish inventory, quota,
payment or creation permissions. If unverified, guide the account holder through face-scan verification.

For a request only to check hcloud installation or connectivity, use the available CLI-readiness workflow; do not query identity status as a connectivity probe.

## Three Steps

1. **Check status** — Run `ShowRealNameAuthStatus` first and route by its four states. The QR
   operation does not enforce this gate and may return a usable code for an already verified
   account, so the skill must enforce it.
2. **Deliver the QR code** — Fetch it only when the account is unverified and the user can scan it
   now. Render it with `scripts/render-qr.ts`. The URL is a one-time credential: never persist,
   forward, or reuse it.
3. **Wait for completion** — Poll with the waiter until verified. On timeout, ask before fetching a
   new code; never resend automatically.

Copy commands, response fields, and values from `references/commands.md`. Do not discover this flow
ad hoc with `--help` or invent parameters. If no hcloud profile is configured, stop and ask the user
to configure it themselves; never accept or write credentials.

## Guardrails

- **Read-only** — Never submit, change, or revoke verification. Refuse every write operation.
- **No sensitive intake** — Refuse identity numbers, document images, bank-card details, and SMS
  codes, and ask the user to delete them. This flow needs none of them.
- **No impersonation** — Do not scan for the user, perform liveness checks for them, or give their
  QR code to anyone else.
- **Face-scan only** — Route enterprise, document, bank-card, verification-change, and review-detail
  requests to Account Center → Real-Name Authentication. State that general KYC and non-Huawei-Cloud
  identity flows are out of scope.

## References

Entity and four-state model: `references/concepts.md` · commands and fields:
`references/commands.md` · terminal renderer: `scripts/render-qr.ts` (`npx tsx render-qr.ts <url>`;
first run requires `cd scripts && npm install`).

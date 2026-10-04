---
id: saas-security
version: "2.0.0"
title: "SaaS Integration Security"
description: "Wiring your application to a third-party SaaS platform: verifying an inbound webhook against the vendor's own scheme rather than a generalized one, why a valid signature identifies the sender and not the user in the payload, replay windows, one credential per integration and per environment, least-privilege scopes, and treating a bulk export as a data boundary. Use when writing a webhook receiver, an OAuth integration, a SCIM endpoint, or any code that authenticates to or from a SaaS vendor."
category: prevention
severity: high
applies_to:
  - "when writing a receiver for an inbound webhook from a SaaS vendor"
  - "when wiring an OAuth integration, connected app, or service account to a SaaS platform"
  - "when building or consuming a SCIM / directory-sync endpoint"
  - "when code exports employee, customer, or billing records from a SaaS system"
languages: ["*"]
token_budget:
  minimal: 1350
  compact: 1750
  full: 2150
rules_path: "rules/"
related_skills: ["auth-security", "secret-detection", "iam-best-practices", "supply-chain-security"]
last_updated: "2026-08-14"
sources:
  - "OWASP API Security Top 10"
  - "CWE-345: Insufficient Verification of Data Authenticity"
  - "CWE-294: Authentication Bypass by Capture-replay"
---

# SaaS Integration Security

## Rules (for AI agents)

### ALWAYS
- Verify an inbound webhook against **that vendor's documented scheme**, and do not
  generalize from another one. Vendors differ in the header, in the secret, and — the
  part that breaks a generalized implementation — in the **canonical string** that gets
  signed. Some sign the raw body, some sign a version prefix plus a timestamp plus the
  body, some sign the HTTP method and path as well. Read the vendor's page for the
  vendor you are integrating; a signature routine copied from a different vendor
  produces a receiver that rejects every legitimate event, and the fix someone reaches
  for is to turn verification off.
- Verify against the **raw request body**, exactly as received, before any parsing or
  re-serialization. A framework that decodes JSON and re-encodes it changes whitespace
  and key order, and the HMAC no longer matches — which again ends with verification
  being disabled rather than fixed.
- Check the **timestamp** the vendor sends and reject requests outside a short window,
  then reject **replays** inside it by recording delivery or event ids. A signature is
  valid forever; the window narrows the replay opportunity and the id store closes it.
- Compare signatures in **constant time**. `crypto-misuse` owns the comparison API for
  each language.
- Treat the signature as proof of **who sent the payload, not who the payload is
  about**. This is the distinction that matters most in this domain: a verified Zoom or
  Calendly or HubSpot event genuinely came from that vendor, and the `email`, `from`,
  or custom fields inside it may still be attacker-chosen — anyone who can book a
  meeting or submit a form controls them. Resolve the subject to a canonical id
  server-side. `auth-security` owns the general rule for producer-asserted identity.
- Give each integration its **own credential**, and each environment its own. A
  refresh token, connected app, or service account shared between dev and prod puts
  production credentials inside dev's blast radius, and a credential shared between
  integrations gives each the union of what any of them needs. Name service accounts
  for their purpose so a later reviewer can tell what revoking one would break.
- Request the **narrowest scope you actually call**, and prefer a read-only variant
  where the platform offers one. Scopes are granted once, at consent, and nobody
  revisits them; a scope requested speculatively is a permanent grant.
- Treat a **bulk export** of employee, customer or billing records as a data boundary:
  log the authenticated principal, the query, the row count and the destination, and
  alert on volume that departs from that integration's own baseline. For HRIS and ERP
  systems this is the primary control — the integration is authorized, and the question
  is how much it took.
- Authenticate a **SCIM or directory-sync endpoint** you expose, rate-limit it, and
  audit every user and group write. Note what the major identity providers actually
  send: a static OAuth bearer token, configured once in their admin console. Client
  certificates are generally not on offer, so the practical controls are a
  high-entropy token you can rotate, a source-address restriction where the IdP
  publishes ranges, and treating every write as an audit event.

### NEVER
- Disable signature verification to make an integration work. Almost every webhook
  spoofing incident is an integration that shipped with the check off because it was
  failing in staging. If it is failing, the canonical string or the raw-body rule is
  what is wrong.
- Hard-code a SaaS token, OAuth client secret, webhook signing key, or service-account
  JSON in source, a container image, a mobile binary, or client-side JavaScript. These
  formats are mass-scanned on public registries within minutes of a push.
  `secret-detection` owns the patterns and the placeholders.
- Wire an **incoming webhook URL that posts into a channel more trusted than its
  callers**. If a CI bot can post to `#secops`, a CI compromise is direct phishing of
  the people who would investigate it. The webhook URL is a bearer credential with no
  identity attached — anyone holding it posts as that integration.
- Share one **person-bound token** across services. It carries that human's
  privileges, dies when they leave, and leaks through their laptop.
- Trust third-party code that runs **inside** the SaaS platform — a marketplace app, a
  scripting extension, an automation add-on — without review. It executes with the
  privileges of whoever installed it, inside the tenant, and neither your CI nor your
  dependency scanner can see it. `supply-chain-security` owns the review posture.
- Grant a **super-admin or org-wide scope** to anything other than a narrowly-owned
  automation. Most integrations need a read-only directory scope; the admin scope is
  requested because it makes the first call work.

### KNOWN FALSE POSITIVES
- **Publishable** identifiers are meant to be public: an OAuth client id for a mobile
  or SPA client, a published app's service-account email, a workspace or tenant id.
  The matching client secret and key file are not.
- Vendor **example credentials** in documentation match detection patterns
  deliberately. The surrounding documentation context is the signal, not the prefix.
- A webhook receiver that returns `200` to an event it decided not to act on is
  correct: vendors retry non-2xx, and an authorization decision is not a delivery
  failure. Log the refusal instead of signalling it in the status.
- A customer-supplied **destination** URL is the intended feature of an outbound
  webhook system. It still needs the private-address rules — `ssrf-prevention` owns
  where an outbound fetch may land.

## Context (for humans)

The single most useful idea here is that a webhook signature answers a narrower
question than people assume. It says: this payload was produced by someone holding the
signing secret, which is the vendor. It says nothing about whether the *contents* are
true. A Calendly invitee email, a HubSpot form field, a Zoom participant name — those
are attacker-controlled by design, because the feature is that strangers can fill them
in. Integrations that authenticate a user from a verified webhook body are common and
are account-takeover primitives.

The second thing worth knowing before writing a receiver: vendors do not share a
scheme. The header name is the least of it — what actually differs is the string that
gets signed, and a routine that works against one vendor silently rejects everything
from another. That is worth stating because the failure is not a security failure at
first. It is a broken integration, and the fastest way to un-break it is the line that
turns verification off.

Per-vendor detail is deliberately not in this skill. Signing schemes, header names,
scope names and hostnames change without notice, and a hand-maintained table of them
goes stale in a way that is worse than having none: an agent that follows a wrong
header name writes a receiver that rejects real traffic, and one that follows a
wrong scope name requests something that does not exist. Read the vendor's current
documentation for the vendor in front of you.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `rules/` — per-vendor rule files used by the scanners at build time
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).
- [CWE-345](https://cwe.mitre.org/data/definitions/345.html) · [CWE-294](https://cwe.mitre.org/data/definitions/294.html).

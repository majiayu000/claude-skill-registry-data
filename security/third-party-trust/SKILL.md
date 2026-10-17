---
name: third-party-trust
description: "Third-party trust boundary analyzer: inventories every outbound HTTP/RPC call (fetch, axios, got, requests, curl, Invoke-RestMethod). For each, identifies literal-vs-template URL, classifies known-trusted vs unknown domain, detects auth-header presence in call window, flags webhook handlers missing signature verification. Read-only. Audience: Senior. Trigger: /third-party-trust"
trigger: /third-party-trust
---

## What this is for

Fetch/axios/Supabase/Stripe calls are TRUST BOUNDARIES going OUTWARD.
Which outbound calls accept user-controlled URLs without re-validation?
Which API key has no origin restriction? Which webhook receiver lacks
signature verification? `input-validation-audit` checks input-validation
coming IN. Missing: outbound trust contract - the mapping of what WE
trust to be on the other end of each outbound connection.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/outbound-calls.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each outbound call:

### Step 5

- **Known-trusted vs unknown**: stripe/amazon/googleapis/etc vs

### Step 6

arbitrary endpoint. Unknown providers = higher risk.

### Step 7

- **Template URL**: variable-based URL (e.g. `req.query.url`) is

### Step 8

attacker-controlled. SSRF-class risk.

### Step 9

- **Auth hint in call window**: Authorization header / api-key /

### Step 10

bearer present? If yes, rotation-burden risk.

### Step 11

- **Webhook handler** with no signature verification (look for

### Step 12

`webhooks.constructEvent` or HMAC verify calls - if absent, the

### Step 13

endpoint will accept forged events).

### Step 14

- **Retry attempt count**: 3+ retries with no idempotency-key →

### Step 15

duplicate side-effects on a 5xx.

### Step 16

5. Write `third-party-trust-report.md` to the working directory.

## Usage

```
/third-party-trust                          # interactive
/third-party-trust <dir>                    # scan project
/third-party-trust -help                    # show usage
```

Returns JSON with `calls[]`:
`{file, line, lib, url, isTemplateUrl, authHint, retrySignals,
webhookHandler, lineContent}` plus summary counts.

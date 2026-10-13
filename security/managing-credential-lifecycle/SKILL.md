---
name: managing-credential-lifecycle
metadata:
  version: "2.1.0"
description: >
  Manages the lifecycle of API keys, tokens, and credentials across a multi-service production
  stack — inventory, rotation schedules, audit procedures, and emergency revocation for Vercel
  env vars, Supabase service keys, the n8n credential store, Anthropic API keys, and MCP
  server tokens. Activates on rotate credentials, API key rotation, credential audit, service
  key expired, key compromised, secrets management, credential sprawl, or preparing a security
  review. Not for writing application auth or login flows (use kyle-vibe-coding) and not for
  storing secrets in code.
---

## Evals

**Should trigger:**
1. "The Anthropic API key got committed to a repo — rotate it"
2. "Audit what credentials we actually have live in production right now"
3. "Set up a rotation schedule for the Supabase service keys"

**Should NOT trigger:**
1. "Build the authentication flow for my app" — that's an application build → kyle-vibe-coding
2. "How should I architect secrets management for my agent system?" — design/architecture question, not lifecycle ops (this skill runs rotation, audit, and revocation — not architecture)

---

## When to Use / When NOT

**Use when** — "the Anthropic key might be leaked, rotate it" — emergency revocation path. "run the quarterly credential audit for the FlashFusion stack" — inventory and schedule review.

**Do NOT use when** — "write a login form with Supabase auth" — that is a build; route to kyle-vibe-coding.

# Credential Lifecycle Management

Credentials accumulate silently. A production system that started with
three API keys typically has thirty within a year. This skill covers
the discipline of knowing what exists, rotating it regularly, and
revoking it when no longer needed.

---

## Current Credential Inventory (FlashFusion / Loxihart Stack)

Run this audit quarterly. Update the table in Notion after each pass.

| Service | Credential type | Location in stack | Rotation schedule | Last rotated |
|---|---|---|---|---|
| Anthropic API | API key | Vercel env + n8n | 90 days | — |
| Supabase service key | JWT secret | Vercel env + n8n | 180 days | — |
| Supabase anon key | Public JWT | Frontend code | Annual | — |
| n8n webhook secrets | Shared secret | n8n + source systems | 90 days | — |
| Base44 Bearer token | Short-lived token | n8n credential store | 30 days | — |
| HubSpot API key | API key | n8n + Clay | 90 days | — |
| Apollo.io API key | API key | n8n | 90 days | — |
| Datadog API key | API key | Vercel drain + code | 180 days | — |
| PostHog project key | API key | Frontend + backend | Annual | — |
| MCP server tokens | Varies | Claude project config | Per provider | — |

---

## Rotation Procedures by Service

### Anthropic API Key

1. platform.anthropic.com → API Keys → Create new key
2. Name it: `flashfusion-prod-YYYY-MM` (date-stamped)
3. Update in Vercel: project → Settings → Environment Variables
4. Update in n8n: Credentials → find Anthropic credential → update key
5. Deploy a test call to confirm the new key works
6. Delete the old key from Anthropic's dashboard
7. Update the inventory table with rotation date

### Supabase Service Role Key

⚠️ Rotating the service role key invalidates all existing JWTs signed with it.
Do this during a maintenance window or off-peak hours.

1. Supabase Dashboard → Settings → API → Regenerate service role key
2. Update every service that uses it simultaneously:
   - Vercel environment variables (all environments)
   - n8n Supabase credential
   - Any Edge Functions with hardcoded fallbacks
3. Verify connectivity with a test query from each service
4. Do not leave old key active — Supabase replaces it immediately

### n8n Webhook Secrets

1. In the source system (Slack, HubSpot, etc.): regenerate the signing secret
2. In n8n: open each webhook node that uses this secret → update verification
3. Test by triggering the webhook from the source system
4. Confirm the old secret is deactivated in the source system

### Base44 Bearer Token

See `operating-n8n-production` Section 1 for the full Base44 procedure.
Short version: Base44 Settings → API → Generate Token → update n8n credential.

---

## Emergency Revocation Procedure

If a credential may be compromised (leaked in logs, committed to git,
sent in an email):

**Within 5 minutes:**
1. Revoke the credential immediately in the issuing service
2. Do not wait to generate a replacement first — revoke now
3. Note the time of potential exposure

**Within 30 minutes:**
1. Generate replacement credential
2. Update all services using that credential
3. Verify all services are functioning with the new credential
4. Review access logs in the issuing service for suspicious usage during
   the exposure window

**Within 24 hours:**
1. Document the incident: when was it exposed, how, what data was accessible
2. Determine if any downstream services were affected
3. If client data was potentially accessible: follow your breach notification
   obligation timeline (varies by contract and jurisdiction)

---

## Detecting Credential Sprawl

Signs you have a sprawl problem:
- You're not sure which services use which keys
- Keys exist in the issuing service that aren't in your inventory
- Multiple keys for the same service with no clear ownership

**Audit procedure:**
1. List all API keys in each issuing service dashboard
2. Cross-reference against your inventory table
3. For any key not in the inventory: identify where it's used or revoke it
4. For any inventory entry with no matching key: it may have been deleted
   without proper replacement — verify the service is functioning

**Naming convention going forward:**
`{service}-{environment}-{YYYY-MM}`
Example: `anthropic-prod-2026-06`

This makes it immediately obvious what each key is for, whether it's
production or staging, and when it was created.

---

## Quarterly Credential Review (30 minutes)

1. Pull the inventory table from Notion
2. Flag all credentials past their rotation date
3. Flag all credentials with "last rotated: unknown"
4. For each flagged credential: schedule a rotation this week
5. Audit each issuing service for keys not in inventory
6. Revoke anything unused for 90+ days

---

## Self-Verification

- [ ] Credential inventory table exists and is accessible
- [ ] Every credential has a rotation schedule and last-rotated date
- [ ] Emergency revocation procedure is known (not just documented)
- [ ] Quarterly review is on the calendar
- [ ] No credentials are stored in code repositories or chat history

---

## CLAIMS
- Revocation must precede replacement in any compromise scenario —
  the risk window of an active compromised key outweighs the operational
  inconvenience of a brief service interruption
- Date-stamped key naming reveals rotation age without needing a separate
  tracking system

## COUNTEREXAMPLE
- Supabase service role key rotation has immediate impact on all active
  sessions; for high-traffic production apps, this requires a coordinated
  rollout rather than a simple swap

## CONTRADICTIONS
- Frequent rotation improves security but increases operational burden;
  the 90-day default is a balance — higher-risk credentials (admin access,
  billing) warrant 30-day schedules regardless of inconvenience


## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **Rotating a key before enumerating every consumer (Vercel env, n8n, Clay, etc.)** → live workflow breaks on its next run — enumerate consumers from the inventory table, stage the new key alongside the old, cut over, then revoke the old after one verified run.
- **Revoking a compromised key before its replacement is live** → self-inflicted outage — issue and deploy the replacement first, then revoke; only revoke-first when active exfiltration is confirmed.
- **Echoing a real secret value into chat, a ticket, or a commit** → secret disclosure — reference credentials by name and location only; if a value was exposed, treat it as compromised and rotate.
- **Rotating a shared key (Supabase service key used by both Vercel and n8n) in one place only** → partial outage — update all locations together and smoke-test each before closing.
- **Treating the public Supabase anon key as a secret, or placing service_role client-side** → wasted effort or catastrophic exposure — service_role is server-only; anon key is safe in the frontend.
- **Skipping post-rotation verification** → silent auth failures surface hours later — run one authenticated call per consumer and confirm success before the task is done.


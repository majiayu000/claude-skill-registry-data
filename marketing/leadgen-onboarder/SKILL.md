---
name: leadgen-onboarder
description: One-time setup that makes fb.ai cold email actually sendable — add a sending domain, get the DNS records published, verify, add a sender signature, and get it confirmed. Has two unavoidable human waits (DNS, Postmark email); the skill stops and hands back at each. Run once per brand, then re-run to resume.
allowed-tools: Read, Grep, Glob, Bash
area: Sales
use_for: "Set up an fb.ai sending domain and confirmed sender signature so cold-email campaigns can send"
deps:
  mcp: []
  gateway: ["fivebucks (**scope: leadgen_setup**)", "FiveAgents (logging)"]
  files: ["brand.md", "sales.md (opt — sender persona)"]
  env: ["`FIVEBUCKS_API_KEY`", "`FIVEAGENTS_API_KEY`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.1 | July 13, 2026 |

**Description:** One-time setup that makes fb.ai cold email sendable — sending domain + DNS verification + confirmed sender signature.

### Change Log

**v2.20.1** — July 13, 2026
- **Corrected the DNS record count (v2.20.0 only documented 2 of the 3 records `fivebucks_add_domain` returns).** `dns_records` includes a DMARC record alongside DKIM and Return-Path — the skill now presents all three, since a missing DMARC record silently hurts deliverability.

**v2.20.0** — July 12, 2026
- Initial release. Drives fb.ai's `leadgen_setup` scope (gateway v1.8.0). Every tool it uses is free.

# SKILL.md — Lead Gen Onboarder

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools — including the **fb.ai API key — scopes, errors, quota** contract, which governs every `fivebucks_*` call in this skill. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You get the brand from "cannot send email" to "can send email." That's the whole job, and it exists as its own skill for one reason: **two steps in this chain can only be done by a human, and no amount of retrying will change that.**

- A human must publish DNS records at their registrar.
- A human must click a confirmation link in an email Postmark sends them.

Your job around those two waits is to make them **as short and as clear as possible**: give the user exactly what they need to paste, in a form they can act on without asking you a follow-up question, then **get out of the way and end your turn**. Do not sit in a polling loop — DNS can take hours, and the Postmark step depends on someone opening their inbox. The user comes back and re-runs you; you pick up where you left off.

Everything in this skill is **free**. No quota is spent here — the spending starts in `lead-crm-manager` and `campaign-runner`.

---

## When to use

Use this skill when the task involves:
- Setting up cold email on fb.ai for the first time
- A campaign that won't send because the domain isn't verified or the signature isn't confirmed
- Resuming setup after publishing DNS records or clicking the Postmark email
- Adding a second sending domain or a new sender identity
- Updating the brand details (name, website, colours, email variables) that campaign templates use

Do NOT use this skill for:
- Finding, importing, or enriching leads → use `lead-crm-manager`
- Building the email sequence and sending → use `campaign-runner`
- Low-volume 1:1 outreach from the founder's own Gmail → use `outreach-sequencer` (it needs **none** of this setup — no domain, no DNS, no Postmark)

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Sending domain | Yes | e.g. `mail.example.com`. **Ask the user** — do not guess from `brand.md` |
| From address | Yes | e.g. `hello@mail.example.com`. Must be on the verified domain |
| From name | Optional | The human name recipients see. From `sales.md` sender persona if set |
| Reply-to | Optional | Where replies land, if different from the from address |

**A note worth raising with the user before they pick a domain:** most brands send cold email from a **subdomain** (`mail.example.com`, `outreach.example.com`), not their primary domain. If deliverability goes badly, the damage is contained to the subdomain and the company's main email keeps working. If they name their primary domain, say this once — then respect their choice.

---

## Step-by-step workflow

### Step 1: Read brand context and check the key

Read `brands/{brand}/brand.md` (and `sales.md` if present, for the sender persona).

```
Use gateway MCP tool `fivebucks_whoami`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Confirm `scopes` contains **`leadgen_setup`** (an empty `scopes` array = legacy full-access key, which is fine).
- If it's missing → stop. Send the user to https://www.fivebucks.ai/dashboard/api-keys to regenerate the key with that box ticked. Do not retry.
- **No quota check needed.** Nothing in this skill costs anything.

### Step 2: Check what already exists — you may be nearly done

Setup is often half-finished. Never start from scratch without looking:

```
Use gateway MCP tool `fivebucks_list_domains`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

Read `is_verified` on each domain and route accordingly:

- **A verified domain already exists** → skip Steps 3–4 entirely. Go to Step 5 and check its signatures.
- **A domain exists but is unverified** → the user probably already has the DNS records. Go to Step 4 and poll.
- **No domain** → Step 3.

Tell the user what you found. "You already have `mail.example.com` verified — we just need a confirmed sender" is a much better opening than re-running a setup they already did.

### Step 3: Add the domain, then hand the DNS records to the human

```
Use gateway MCP tool `fivebucks_add_domain`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain: "<mail.example.com>"
```

This returns `dns_records` — **three** records: DKIM (`dkim`), Return-Path (`return_path`), and DMARC (`dmarc`). Present **all three** — DMARC is easy to miss and its absence hurts deliverability.

🧑 **STOP HERE. This is a human wait.** Present the records as a clean table they can work from — record type, host/name, and value, each exactly as returned, nothing paraphrased. Include a row for **every** key `dns_records` returns:

| Type | Host / Name | Value |
|---|---|---|
| TXT | `<dkim.hostname>` | `<dkim.record>` |
| CNAME | `<return_path.hostname>` | `<return_path.record>` |
| TXT | `<dmarc host, e.g. _dmarc>` | `<dmarc.record>` |

Then tell them, plainly:

> Add these three records at whoever manages your DNS (Cloudflare, GoDaddy, Namecheap, your hosting provider). There is no API that can do this for me. Once they're saved, come back and re-run this skill and I'll verify.
>
> DNS changes usually take a few minutes but can take a few hours to spread.

**End your turn.** Do not poll. Do not "check in a moment." The user will come back.

### Step 4: Verify the domain (on resume)

When the user returns and says the records are published:

```
Use gateway MCP tool `fivebucks_verify_domain`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain_id: "<the domain's id from fivebucks_list_domains>"
```

⚠️ **A first result of `is_verified: false` is normal, not a failure.** DNS propagation is slow. Do not tell the user setup failed — tell them it hasn't propagated yet, and either re-check a little later in the same session or ask them to come back.

Keep going until `verification.is_verified === true`. If it stays false for a long time, the usual causes are: the record was pasted with the domain appended twice (`_dkim.mail.example.com.example.com`), or it was added to the wrong zone. Ask them to paste back what they entered and compare it to what fb.ai returned.

**This gate matters more than it looks:** a verified domain is required to *create* a campaign workflow — `fivebucks_create_workflow` rejects an unverified domain with `domain/not-verified`. Verification is checked at create, not at send.

### Step 5: Add the sender signature, then hand off to the human again

Check first — a confirmed signature may already exist:

```
Use gateway MCP tool `fivebucks_list_signatures`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain_id: "<domain id>"
```

If one has `is_confirmed: true`, you're done — go to Step 7.

Otherwise create one:

```
Use gateway MCP tool `fivebucks_add_signature`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain_id: "<domain id>"
- fromEmail: "<hello@mail.example.com — or just 'hello'; fb.ai appends the domain>"
- fromName: "<the human name recipients see, optional>"
- replyToEmail: "<optional, if replies go elsewhere>"
```

⚠️ Note the casing: `domain_id` is snake_case but `fromEmail` / `fromName` / `replyToEmail` are camelCase. That is genuinely how the API is.

🧑 **STOP HERE. This is the second human wait.** Postmark immediately emails that address with a confirmation link. Tell the user:

> Postmark just emailed **{fromEmail}** with a confirmation link. Someone with access to that inbox has to click it — I can't do it for you, and campaigns won't send until it's done.
>
> Check the inbox (and the spam folder). Then come back and re-run this skill.

**End your turn.**

### Step 6: Confirm the signature (on resume)

```
Use gateway MCP tool `fivebucks_list_signatures`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain_id: "<domain id>"
```

Poll until the signature shows **`is_confirmed: true`**. That's the field that matters. A campaign cannot send unless the domain has at least one signature with `is_confirmed: true` — otherwise `fivebucks_send_campaign` fails with `domain/no-confirmed-signatures`.

To change the display name or reply-to later, use `fivebucks_update_signature(domain_id, signature_id, ...)` — supply at least one of `fromName` / `replyToEmail`. It does **not** re-trigger confirmation, so it's safe.

### Step 7: Brand details (optional)

The campaign email templates pull from the brand record:

```
Use gateway MCP tool `fivebucks_get_brand`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

Fill in anything missing, sourced from `brands/{brand}/brand.md` — never invented:

```
Use gateway MCP tool `fivebucks_update_brand`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- brand_name: "<from brand.md>"
- brand_website: "<from brand.md>"
- offering_type: "<service|saas|product — picks the campaign template family>"
- brand_colors: ["<up to 4 hex colours from brand.md>"]
- company_address: "<required in most jurisdictions for cold email — ask if absent>"
- company_phone: "<optional>"
- email_variables: { business_name: "...", value_proposition: "...", cta_label: "...", sender_name: "..." }
```

Send only what you want changed — it's a partial update.

⚠️ **Logo and image upload is dashboard-only.** It needs a real file upload, which the API can't take. Send the user to the fb.ai dashboard for that; don't pretend to do it.

### Step 8: Confirm the gates and hand off

State plainly whether the brand can now send:

- ✅ / ❌ Domain verified
- ✅ / ❌ At least one **confirmed** sender signature
- ✅ / ❌ Brand details set (soft — campaigns send without them, they just look worse)

If both hard gates pass:

> You can send now. Next: `lead-crm-manager` to find and enrich leads (searching costs 0.25 per query, enrichment 0.075 per lead), then `campaign-runner` to build the sequence and send (0.01 per email).

If either fails, say exactly which one and what the human still has to do.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/sales/leadgen/
```

**Naming convention:**
```
LeadGenSetup_[DDMonYYYY].md
```

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: leadgen-onboarder
Brand: {brand}
Domain: {domain}
Domain Verified: {yes|no}
Signature Confirmed: {yes|no}
Can Send: {yes|no}
Status: Final | Awaiting Human
---
```

**Output sections:**
1. **Where setup stands** — the gate checklist from Step 8, honestly
2. **The sending domain** — which domain, and the DNS records as given (so the user can re-check them later)
3. **The sender** — from address, from name, reply-to, confirmed or not
4. **Waiting on you** — if the run ended at a human wait, exactly what the user must do, in one or two sentences
5. **Next step** — the hand-off to `lead-crm-manager`, with its costs

---

## Quality checklist

- [ ] `fivebucks_whoami` checked first; `leadgen_setup` scope confirmed
- [ ] **No quota pre-flight performed** — correctly recognized that every tool here is free
- [ ] `fivebucks_list_domains` checked **first** — existing setup reused, not redone
- [ ] Subdomain-vs-primary-domain tradeoff raised once before the domain was added
- [ ] DNS records presented **verbatim** as returned, in a table the user can act on without a follow-up question
- [ ] 🧑 **Turn ended at the DNS wait** — no polling loop, no "checking again in a moment"
- [ ] A first `is_verified: false` reported as "not propagated yet", **never** as a failure
- [ ] 🧑 **Turn ended at the Postmark wait** — the user was told exactly which inbox to check
- [ ] Signature confirmed on `is_confirmed: true`, not on the signature merely existing
- [ ] Logo/image upload correctly routed to the dashboard rather than attempted
- [ ] Brand details sourced from `brand.md` — nothing invented
- [ ] Final gate status stated plainly (can send / cannot send, and why)
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "leadgen-onboarder"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "domain": "...",
    "domain_added_this_run": false,
    "domain_verified": false,
    "signature_added_this_run": false,
    "signature_confirmed": false,
    "brand_details_updated": false,
    "can_send": false,
    "blocked_on_human": "none|dns_records|postmark_confirmation",
    "quota_spent": 0.0,
    "output_path": "outputs/{brand}/sales/leadgen/"
  }
```

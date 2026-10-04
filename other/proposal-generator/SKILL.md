---
name: proposal-generator
description: Generate a branded sales proposal from a CRM deal record — packaged as a Gamma deck (or Google Doc fallback) with embedded Stripe payment link, emailed to the prospect via Gmail draft. On-demand per deal.
allowed-tools: Read, Grep, Glob, Bash, WebSearch
area: Sales
use_for: "Generate branded sales proposal from a deal record. Gamma deck or Google Doc with embedded Stripe payment link"
deps:
  mcp: ["Stripe", "Gamma", "Google Drive", "Gmail", "Notion", "Slack"]
  gateway: ["fivebucks (opt — brand kit via fivebucks_get_brand_kit; **scope: social_posts**)"]
  files: ["sales.md", "product.md", "brand.md", "audience.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: ["`${BRAND}_CRM_DB`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Generate a branded sales proposal from a CRM deal record — packaged as a Gamma deck (or Google Doc fallback) with embedded Stripe payment link, emailed to the prospect via Gmail draft. On-demand per deal.

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.5.0** — May 20, 2026
- Brand color/font resolution is now a **3-tier lookup**: fb.ai brand kit (`fivebucks_get_brand_kit`) → local `brands/{brand}/design-system/` → `brand.md`, per the Brand kit field map in `agents/link.md`. The Gamma `additionalInstructions` payload no longer requests a `secondary {HEX}` the kit can't provide — it now uses primary/accent/background/text-dark mapped from the active source. Trimmed duplicated design-system reading boilerplate.

**v2.4.1** — May 12, 2026
- Step 1 (Read Brand Context) — restructured with a leading "Brand visual identity" block. design-system/ probed first (extract HEX color tokens + typography + component patterns), brand.md visual identity as fallback. Strategic + commercial context (product.md, audience.md, sales.md) now grouped under their own subhead. Abort behavior clarified: only `brand.md`/`product.md`/`audience.md`/`sales.md` missing aborts; design-system/ missing is a graceful fallback.
- Step 5 — Gamma `additionalInstructions` payload expanded to carry explicit HEX values + font-family extracted at Step 1. Was previously "Use brand colors {primary, secondary}" — vague enough that Gamma routinely defaulted to its own template colors. Now spells out primary/secondary/accent/background HEX + typography family, with the design-system→brand.md fallback order baked into the spec.
- Quality Checklist — two new entries enforce the design-system probe and the explicit HEX/font payload in Gamma's `additionalInstructions`.

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Proposal Generator

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are a B2B sales engineer for the active brand. Your job is to take a qualified deal from the CRM and produce a tailored, branded sales proposal — packaged as a sharable Gamma deck (or Google Doc fallback), priced from `product.md`, governed by the terms in `sales.md`, and dispatched as a Gmail draft with an embedded Stripe payment link. The proposal MUST be free of fabrication: every claim, feature, price, and term comes from brand context files.

Runs on-demand, one deal at a time.

---

## Role

Sales engineer + deal closer. You translate a CRM record into a proposal a prospect can sign and pay. You do NOT invent pricing, terms, case studies, or guarantees — those live in `brands/{brand}/product.md` and `brands/{brand}/sales.md`. You DO tailor the language and emphasis to the persona's pain points (from `audience.md`) and pick the right plan tier per the persona's default rule (from `sales.md`).

---

## When to use

Use this skill when:
- A CRM deal record reaches Stage = "Proposal Requested" and the rep wants a branded deliverable
- Manual invocation per deal with a Notion CRM page URL or page ID
- A re-quote is needed for an existing deal (custom terms or new tier)

Do NOT use this skill for:
- Cold outreach copy → use `outreach-sequencer`
- Customer onboarding after the deal closes → use `customer-onboarder`
- Generic sales decks not tied to a specific deal → use `campaign-presenter`

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Deal record | Yes | Notion CRM page URL or page ID. Must live inside `${BRAND}_CRM_DB` |
| Persona slug | Optional | Auto-detect from CRM record's Persona property; ask only if missing |
| Plan tier | Optional | Defaults to `sales.md` → Default tier per persona; override only if user explicitly asks |
| Add-ons | Optional | List of add-on slugs from `product.md`; defaults per `sales.md` upsell rules |
| Custom terms | Optional | Override `sales.md` Proposal Defaults (payment, validity, cancellation) — flag in audit trail |
| Output format | Optional | `gamma` (default) or `gdoc` fallback; auto-fallback to gdoc if Gamma fails for the brand |

---

## Step-by-step workflow

### Step 1 — Read Brand Context

**Brand visual identity — read FIRST so the Gamma deck inherits the right palette. Resolve the source in this 3-tier order:**
1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`. If it returns non-null, use its color tokens (HEX) + typography as the authoritative source for the Gamma `additionalInstructions` at Step 5 — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit has no separate `secondary` or font weight scale). Returns null when no kit is uploaded — fall through to tier 2.
2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — read per link.md tier 2 (HEX color tokens + typography); also note any component patterns you'll reference in the Gamma `additionalInstructions` at Step 5.
3. **brands/{brand}/brand.md** — visual identity (colors, fonts, logo URL), voice, locale, currency, approved phrases. The Colors + Google Font sections are the universal fallback when neither of the above is available. Never block on a missing fb.ai key or design-system; brand.md is always available.

Same Visual consistency rule as `agents/link.md` — derive from the fb.ai brand kit (`fivebucks_get_brand_kit`, when `FIVEBUCKS_API_KEY` set) → local `design-system/` → `brand.md` (fallback), never hardcode brand colors/fonts from memory.

**Strategic + commercial context:**
- `brands/{brand}/product.md` — pricing tiers, features per tier, differentiators, add-ons
- `brands/{brand}/audience.md` — persona pain points, objections, buying triggers (used to tailor the Solution section)
- `brands/{brand}/sales.md` — Proposal Defaults (terms, payment, validity, cancellation), Default tier per persona, Upsell rules, Sender Persona (signature block, photo URL, email)

If `brand.md`, `product.md`, `audience.md`, or `sales.md` is missing, abort with a `failed` log and tell the user which file to populate. `design-system/` missing is NOT a hard fail — fall back to brand.md and continue.

### Step 2 — Fetch Deal Record from CRM

Resolve the deal from Notion. The deal page MUST live inside the brand's CRM database (`${BRAND}_CRM_DB` env var) — never accept a deal page from another brand's DB.

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: <deal page URL or page ID from user input>
```

Validate:
- The page's parent database ID matches `${BRAND}_CRM_DB`. If not, abort with `failed` — wrong brand context.
- Required CRM properties exist: `Client Name`, `Client Email`, `Persona`, `Stage`, `Plan Tier` (optional), `Custom Notes` (optional).
- If `Persona` is unset and user did not supply one in inputs, ask before continuing.

Extract: `client_name`, `client_email`, `persona`, `current_stage`, `crm_plan_tier` (if any), `custom_notes`.

### Step 3 — Resolve Plan Tier and Add-ons

Decide which plan to propose:
1. If user supplied a plan tier explicitly → use it.
2. Else if `crm_plan_tier` is set on the deal → use it.
3. Else read `sales.md` → Default tier per persona, look up the row matching `persona`, use that tier.

Decide add-ons:
1. If user supplied add-ons → use them.
2. Else read `sales.md` → Upsell rules. Apply rules whose trigger matches this deal (e.g., "if persona = enterprise-buyer AND plan = Pro, suggest Managed Onboarding").

Pull the resolved tier's price, billed period, and feature list from `product.md`. Pull each add-on's price and description from `product.md`.

### Step 4 — Build Proposal Content Sections

Assemble the proposal content (text only — no formatting yet). Six sections:

| Section | Source | Content |
|---|---|---|
| Cover | `brand.md` + deal | Brand logo, client name, proposal date, validity expiry from `sales.md` |
| About Us | `brand.md` | Mission, positioning statement, approved phrases — 1 paragraph max |
| The Challenge | `audience.md` → Pain points for this persona | Restate the persona's top 2-3 pain points in their language. Reference `custom_notes` from CRM if present |
| Our Solution | `product.md` features tailored to persona pain points | Map each pain point to a specific feature (claim → proof). Use approved phrases from `brand.md`. Lead with the persona's strongest buying trigger from `audience.md` |
| Pricing | `product.md` resolved tier + add-ons | Tier name, price, billed period, included features, optional add-ons with line-item pricing. Use brand currency from `brand.md` Locale section |
| Terms & Next Steps | `sales.md` Proposal Defaults + payment link | Payment terms, validity period, cancellation policy, signature block from Sender Persona, payment link from Step 6 |

Keep total content under 1200 words for a deck (Gamma renders best in this range). For a Google Doc fallback, expand to 2-3 pages.

### Step 5 — Generate the Proposal Deliverable

**Preferred path — Gamma deck** (when the brand has a Gamma template configured):

```
Use mcp__claude_ai_Gamma__generate_from_template:
- inputText: <full proposal content from Step 4, structured as section headings>
- additionalInstructions: "Brand: {brand}. Voice: {voice from brand.md}. Use brand colors: primary {HEX}, accent {HEX}, background {HEX}, text/dark {HEX} (map each from the active source per the Brand kit field map in agents/link.md — fb.ai kit provides primary/accent/dark/background; local design-system/ or brand.md when the kit is null — never invent). Typography: heading {font-family} + body {font-family} (family names from fb.ai kit / local design-system/ when present, brand.md Google Font when fallback; font weight scale comes only from the local design-system, not the kit). Logo: {logo URL from brand.md}. Persona: {persona}."
- format: "presentation"
- numCards: 8
- exportAs: "pdf"
```

Build the `additionalInstructions` string from the values extracted at Step 1 — fb.ai brand kit tokens win when present, then local design-system/, brand.md fallback otherwise. The explicit HEX + font-family line is what makes Gamma generate a deck that matches the brand instead of defaulting to its own templates.

Capture the returned `gammaUrl` and `pdfUrl`.

**Fallback path — Google Doc** (when Gamma is unavailable for the brand, or `output format = gdoc`):

```
Use mcp__claude_ai_Google_Drive__create_file:
- name: "Proposal_{client_name}_{DDMonYYYY}"
- mimeType: "application/vnd.google-apps.document"
- content: <full proposal content from Step 4, formatted as markdown>
- parents: [<brand's proposal folder ID from settings.local.json, or root>]
```

Capture the returned `webViewLink`. Set link sharing to "anyone with the link can view" only if `sales.md` Proposal Defaults declares external sharing is allowed; otherwise leave restricted.

If both paths fail, abort with `failed` log — do not silently produce a worse deliverable.

### Step 6 — Create Stripe Payment Link

Compute the payment amount:
- Base: resolved tier price × validity period (e.g., monthly tier × 12 months for an annual proposal). Period rule lives in `sales.md` Proposal Defaults.
- Add-ons: sum of resolved add-on prices.
- Currency: from `brand.md` Locale section.
- Expires at: today + `sales.md` Proposal Defaults validity period (e.g., 14 days).

If the Stripe MCP is not yet authenticated, kick off the OAuth flow first:

```
Use mcp__claude_ai_Stripe__authenticate
```

Once authenticated, create a payment link via the Stripe MCP's payment-link tool. The tool name surfaces only after authentication — load it via ToolSearch before calling.

```
Use Stripe MCP payment_link / checkout creation tool (loaded via ToolSearch after authentication):
- amount: <total in smallest currency unit, e.g., cents>
- currency: <ISO from brand.md, e.g., "sgd">
- description: "Proposal for {client_name} — {tier} plan"
- metadata: {
    "brand": "<active-brand>",
    "deal_id": "<Notion page ID>",
    "persona": "<persona slug>",
    "tier": "<tier name>",
    "addons": "<comma-separated slugs>"
  }
- expires_at: <ISO timestamp = today + validity from sales.md>
```

Capture the returned `payment_link_url`. Inject it into the Terms & Next Steps section of the proposal — if the deck is already generated, regenerate the final card with the link, or note the link in the cover email so the prospect can pay independently.

**Stripe MCP deferred-tool note:** before calling any Stripe tool other than `authenticate` / `complete_authentication`, call `ToolSearch` with query `"select:<tool_name>"` to load the schema. The Stripe MCP exposes its real tools only after the user completes OAuth.

### Step 7 — Compose Cover Email (Gmail Draft)

Build a Gmail draft with the proposal link, payment link, and persona-tailored opening.

**Gmail is a deferred MCP tool — load its schema before calling:**

```
Use ToolSearch:
- query: "select:mcp__claude_ai_Gmail__create_draft"
```

```
Use mcp__claude_ai_Gmail__create_draft:
- to: <client_email from CRM>
- from: <sender email from sales.md Sender Persona>
- subject: "{Brand} proposal — {client_name} — {tier} plan"
- body: <persona-tailored email — see structure below>
```

Email body structure (all content from context files — never invent):
1. **Opening** — 1 sentence referencing the persona's top buying trigger from `audience.md`. Use voice from `brand.md`.
2. **What's inside** — 2-3 bullet points summarizing the proposal (tier, key features, total price).
3. **Proposal link** — Gamma URL or Google Doc URL from Step 5.
4. **Payment link** — Stripe URL from Step 6 with validity expiry note.
5. **Next steps** — book-a-call link if `sales.md` Sender Persona declares one, else a reply-to-this-email CTA.
6. **Signature block** — exact block from `sales.md` Sender Persona (name, title, photo URL, contact info).

Save as draft (do NOT auto-send). The rep reviews and sends manually unless the user explicitly says "send it".

### Step 8 — Update Notion Deal Record

Update the deal page properties to reflect proposal-sent state:

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <deal page ID>
- properties: {
    "Stage": "Proposal Sent",
    "Proposal URL": "<gamma URL or gdoc URL>",
    "Payment Link": "<stripe URL>",
    "Proposal Sent Date": "<today ISO>",
    "Proposal Tier": "<resolved tier name>",
    "Proposal Amount": <total amount>,
    "Proposal Currency": "<currency from brand.md>",
    "Proposal Expires": "<expiry date from Stripe>"
  }
```

Append a content block to the deal page's body summarizing: tier, add-ons, total, expiry, links — so the deal history is auditable inside Notion.

### Step 9 — Notify Slack

DM the rep via Slack so they know the draft is ready to review and send.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "Proposal ready — {client_name} — {tier} — {amount} {currency} — Gmail draft pending review.
         Deck: <gamma/gdoc URL>
         Payment link: <stripe URL>
         Notion deal: <notion deal URL>"
```

### Step 10 — Save Local Audit Backup

Save a metadata-only audit record to local outputs:

```
outputs/{brand}/proposals/Proposal_{client_name}_{DDMonYYYY}.md
```

The local file is metadata only — the actual deliverable lives in Gamma or Google Drive. Local file purpose is the audit trail.

---

## Output format

**Save location — local audit:**
```
outputs/{brand}/proposals/
```

**Naming convention:**
```
Proposal_{client_name}_{DDMonYYYY}.md
```

Examples:
- `Proposal_AcmeCorp_07May2026.md`
- `Proposal_PineAccounting_07May2026.md`

**Local audit metadata:**
```yaml
---
Date: YYYY-MM-DD
Skill Used: proposal-generator
Brand: {brand}
Client: {client_name}
Persona: {persona slug}
Tier: {resolved tier}
Add-ons: [list]
Amount: {total}
Currency: {ISO}
Validity: {days}
Expires: YYYY-MM-DD
Deal Notion URL: <url>
Proposal URL (Gamma/GDoc): <url>
Payment Link (Stripe): <url>
Gmail Draft ID: <id>
Status: Draft Sent | Sent | Failed
---
```

**Deliverables produced:**
- Gamma deck or Google Doc (proposal itself)
- Stripe payment link (signature/payment)
- Gmail draft (cover email — pending rep review)
- Notion deal record updated (Stage=Proposal Sent, links, amount, expiry)
- Slack notification to `$SLACK_NOTIFY_USER`
- Local audit file at `outputs/{brand}/proposals/`

---

## Quality checklist

Before finalizing:

- [ ] Deal page parent DB matches `${BRAND}_CRM_DB` — no cross-brand contamination
- [ ] Brand visual source resolved in 3-tier order at Step 1: fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md` Colors + Google Font; never blocked on a missing key or design-system
- [ ] Gamma `additionalInstructions` carries explicit HEX values + font-family extracted at Step 1 (or the Google Doc fallback styles the cover/section headings to match) — never invented from memory
- [ ] All pricing comes from `brands/{brand}/product.md` — no invented prices or tiers
- [ ] Plan tier matches `sales.md` Default tier per persona unless user explicitly overrode
- [ ] Add-ons resolved per `sales.md` Upsell rules — no random add-ons
- [ ] Persona pain points in The Challenge section come verbatim from `audience.md` — no fabrication
- [ ] Solution section maps each pain point to a real feature in `product.md`
- [ ] Terms (payment, validity, cancellation) come from `sales.md` Proposal Defaults
- [ ] Currency in proposal matches `brand.md` Locale section
- [ ] Stripe payment link metadata includes `brand`, `deal_id`, `persona`, `tier`
- [ ] Stripe payment link expiry matches `sales.md` validity period
- [ ] Gmail signature block is exactly the Sender Persona block from `sales.md` — not invented
- [ ] Gmail draft saved (not auto-sent) unless user explicitly approved sending
- [ ] Notion deal updated with all 7 properties (Stage, URLs, dates, amount)
- [ ] Slack notification sent to `$SLACK_NOTIFY_USER`
- [ ] Local audit file written to `outputs/{brand}/proposals/`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "proposal-generator"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "client": "<client name>",
    "deal_id": "<notion page id>",
    "persona": "<persona slug>",
    "tier": "<resolved tier>",
    "addons": ["<addon slugs>"],
    "amount": 0,
    "currency": "<ISO>",
    "validity_days": 0,
    "expires_at": "YYYY-MM-DD",
    "format": "<gamma|gdoc>",
    "proposal_url": "<gamma or gdoc URL>",
    "payment_link_url": "<stripe URL>",
    "gmail_draft_id": "<id>",
    "notion_deal_url": "<notion URL>",
    "stage_after": "Proposal Sent",
    "output_path": "outputs/{brand}/proposals/",
    "deliverable": "Proposal_{client}_{DDMonYYYY}.md"
  }
```

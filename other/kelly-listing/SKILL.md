---
name: kelly-listing
description: Listing factory (上架工作台, Busabase App-in-Skill) for a cross-border e-commerce seller. Use when the user invokes $kelly-listing or /kelly-listing, mentions 上架, listing, Amazon title bullets, A+ content, flat file, TikTok Shop listing, listing compliance, 禁用词, multi-locale listings, wants platform listings drafted from product source material or a kelly-picks brief, deterministic compliance checks against per-platform rule sets, a review queue for approving drafts, or approved listings exported as Markdown/CSV for upload.
metadata:
  category: ecommerce
  tags:
    - risk:gated-write
    - industry:ecommerce
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-listing
    resources:
      - products
      - drafts
      - checks
      - claims
      - claim-rules
      - settings
    risk: gated-write

---

# Kelly Listing

## Overview

Use this skill as the cross-border seller's listing operator (上架工作台). The agent ingests product source material — specs, features, an image checklist, target keywords, possibly a kelly-picks handoff brief — and drafts platform-specific listings: Amazon (title / 5 bullets / description / backend search terms / A+ outline), Shopify (title / description / SEO meta), TikTok Shop (punchy title + selling points), eBay (title / subtitle / description / item specifics), plus locale variants (US/DE/JP). Deterministic compliance checks run against per-platform rule sets and the claims/compliance registry, and the seller reviews drafts in a Busabase-backed App-in-Skill review queue (approve / request changes / block) before an approval-gated export. Reading product source material is a genuine external operation a browser cannot perform: `scripts/ingest_drafts.mjs` is the only place a product or draft enters the system, `scripts/run_checks.mjs` runs the compliance rules, and `scripts/execute_decisions.mjs` records the planned follow-up for approved/changes-requested drafts. The AirApp itself only reads Busabase and writes review decisions; export happens through `scripts/export_listings.mjs`, and publishing to marketplaces is delegated to the agent outside the app after explicit approval.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest/check what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; then present numbered drafts (`Draft #1`) and take verdicts in conversation.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Listing overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Kelly Listing review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Listing command desk with product × platform status matrix, compliance pass rate, and export readiness.</td>
    <td><strong>Review queue</strong><br>Draft submissions with compliance summaries and keyword-strategy notes for approval before export or publish.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checks.webp" alt="Kelly Listing compliance checks"></td>
    <td width="50%"><img src="assets/screenshots/drafts.webp" alt="Kelly Listing draft workbench"></td>
  </tr>
  <tr>
    <td><strong>Compliance checks</strong><br>Per-rule pass/warn/fail results — banned words, character caps, bullet counts — across all drafts.</td>
    <td><strong>Draft workbench</strong><br>Amazon draft with live title character count, five bullets, backend search terms byte counter, A+ outline, and locale tabs.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-listing-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Ingesting a product or draft is a local-file-only operation: `scripts/ingest_drafts.mjs` reads a JSON payload file the agent prepares (from product source material or a kelly-picks brief) and writes it to Busabase. It never fetches anything from remote systems on its own.
- The AirApp reads and writes Busabase records only. It never publishes to a marketplace, uploads a flat file, or performs any other external side effect.
- Publishing to marketplaces (Amazon flat file upload, Shopify admin, TikTok Shop, eBay) is approval-required and happens outside the app, after the seller approves in the review queue; `scripts/execute_decisions.mjs` never performs the publish itself — it only writes an execution marker.
- Never write claims the checks would flag (banned words, competitor brands, invented certifications); fix the copy, don't weaken the rules.
- No seller credentials live in this repo. Marketplace API tokens, if the user configures any for the publish handoff, are referenced by env var name only. Never commit local payload files, env files, or generated exports.

## Busabase Resources

Six Bases under one application Folder (`kelly-listing`), declared in `content/kelly-listing-app/app/js/config.js` and the generated template sidecars under `content/`:

- `products`: the product source-material library — SKU, category, source (`manual`/`kelly_picks` handoff), specs, feature list, target keywords, and the image checklist.
- `drafts`: the draft workbench and review queue in one — per-platform fields (title/bullets/description/search terms/SEO meta/selling points/A+ outline/item specifics), workflow status, compliance score, and the human decision + execution marker on the same row.
- `checks`: per-draft, per-rule compliance check results (required fields, title length, banned words, competitor brands, bullet/selling-point counts, SEO meta length, all-caps noise, keyword stuffing, image checklist, claims-registry violations).
- `claims`: the compliance registry's approved marketing claims and rejected claims.
- `claim-rules`: the compliance registry's banned-word / restricted-phrase rules.
- `settings`: one row (`record-id: "config"`) with the seller profile, per-platform rule sets, banned/competitor terms, and export preferences.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/listing-schema.md` for exact field shapes. Compliance scores, the review queue, the recent-activity feed, and metrics are recomputed client-side from the stored rows on every read (`content/kelly-listing-app/app/js/listing-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest/checks run.

## First Run And Onboarding

On invocation, check the `drafts` Base. If it is empty, guide setup before drafting real listings: ask, turn by turn, seller/brand profile (brand name, legal entity, copy tone), platforms to enable with their rule sets (start from the caps in `references/listing-schema.md` and adjust), target locales, the banned-word list plus competitor brand names, and export preferences. Write the answers onto the Settings row, then ingest and check:

```bash
node skills/kelly-listing/scripts/ingest_drafts.mjs payload.json --apply
node skills/kelly-listing/scripts/run_checks.mjs --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-listing-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: listing command desk — KPI cards (products, drafts with per-platform badges, compliance pass rate, exported this week), per-product status matrix (product × platform: none/draft/approved/exported), review-queue preview, recent activity (derived from each draft's own timestamps).
- `#/products` and `#/products/<product_id>`: the product library — name, SKU, category, source badge, platforms targeted, overall status. Detail shows source material: specs, feature list, image checklist with status ticks, target keywords, and linked drafts per platform.
- `#/drafts` and `#/drafts/<draft_id>`: the draft workbench — list by product+platform+locale with compliance score badges. Detail renders the full structured listing per platform shape with every field editable, live character counts against caps and a byte count for backend search terms, the compliance panel alongside with per-rule pass/warn/fail and evidence, and locale tabs (US/DE/JP) when variants exist.
- `#/checks`: compliance results across all drafts — rule × draft table with pass/warn/fail badges and evidence, filterable by rule, platform, product, and result.
- `#/claims`: the compliance registry — approved marketing claims, rejected claims, and banned-word/restricted-phrase rules.
- `#/review`: the review queue — every draft with its workflow state (`needs_review` / `changes_requested` / `approved` / `done` / `blocked`), compliance summary, the agent's keyword-strategy notes, decision buttons (approve / request changes / block), a `Review note`, and a stable ref (`Draft #1`). Decisions write directly onto the draft record through `busabase-sdk`; field edits saved in the workbench arrive as `revise` decisions carrying the edited fields.
- `#/settings`: sanitized config summary — seller/brand profile, platforms enabled with their rule sets, locales, banned-word list size, export prefs, read live off the Settings Base.

Demo mode:

- `?demo=overview`, `?demo=products`, `?demo=drafts`, `?demo=checks`, `?demo=claims`, `?demo=review`, and `?demo=detail` open deterministic mock scenes ("Nimbus Home" persona) for documentation and screenshots.
- `lang=en` or `lang=zh` forces UI chrome language. With `lang=zh` the desk chrome AND agent-generated meta content (product names such as 可折叠硅胶饭盒, compliance rule names, keyword-strategy notes) are Chinese, but the listing copy itself (titles/bullets/descriptions/search terms) stays in the target-market language (English for US, German for DE) — a Chinese seller reads the desk in Chinese while the listings stay in the marketplace language.
- Deep links such as `/?demo=detail&lang=zh#/drafts/d-lunchbox-amazon-us` must work (the featured draft id is stable).
- Demo mode never reads or writes Busabase. Decision buttons still work in the UI but act on in-memory state only.

UI language: English and Chinese chrome with `Auto` default. Keep real listing copy, SKUs, and imported source material in their original language.

## Ingest Workflow

1. Collect inputs: product specs, feature facts, target keywords, the image checklist, and any kelly-picks handoff brief (set product `source: "kelly_picks"` and note the pick reference in `notes`).
2. Draft each platform's listing as a structured ingest payload in the marketplace language of the target locale — Amazon needs exactly 5 benefit-led bullets and backend search terms under 249 bytes; keep the tone from the seller profile; never invent certifications or use words from the banned list.
3. For locale variants, localize for the market (keyword habits, units, register), don't translate word-for-word; variants share a `variant_group` so the workbench shows locale tabs.
4. Record the reasoning in each draft's `keyword_strategy` so the reviewer sees why the title reads the way it does.
5. Run the write path:

```bash
node skills/kelly-listing/scripts/ingest_drafts.mjs payload.json --apply
```

The script validates the payload against the per-platform field shapes and the required-fields rules stored on the Settings row, normalizes products/drafts, and upserts them into Busabase by natural key (`product_id`/name+SKU, `draft_id`) so re-ingests are idempotent. Without `--apply` it is a dry run.

## Check Workflow

1. Run `node skills/kelly-listing/scripts/run_checks.mjs --apply`. Deterministic rules (title length caps — 200 Amazon / 70 Shopify / 255 TikTok Shop / 80 eBay, exactly 5 bullets, backend search terms ≤ 249 bytes, banned words and competitor brands, required fields, Shopify SEO meta lengths, no all-caps shouting words, a keyword-stuffing heuristic, the product image checklist, and claims-registry violations) are computed from the per-platform rule sets on the Settings row and the compliance registry (`claims`/`claim-rules` Bases); per-draft compliance scores are recomputed idempotently.
2. Summarize failures for the seller by ingesting `compliance_summary`/`suggestions` onto the draft record.
3. Give the user the AirApp URL and send them to `#/review`.

## Decisions And Execution Workflow

1. The seller decides at `#/review` or the draft workbench: approve, request changes (with a note), save edited fields (revise), or block. Decisions write directly onto the draft record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided draft with the concrete operation — `export_listing` (from `approve`) or `request_revision` (from `request_changes`) — and target). No external side effects either way; the draft's workflow `status` never changes.
3. The agent then performs the approved follow-up outside the app: for `export_listing`, run `scripts/export_listings.mjs` and hand off publishing via the platform APIs/skills the user has configured; for `request_revision`, redraft the listing per the review note, re-ingest, and re-run checks.

## Export Workflow

1. `node skills/kelly-listing/scripts/export_listings.mjs --out <dir>` reads drafts with a genuine human "approve" decision from Busabase and writes each as a clean Markdown document plus a flat-file-ready `listings.csv` (sku, platform, locale, title, bullets joined, description, search terms) into `--out` (default `exports/` at the skill root, gitignored). Marks each exported draft `done` in Busabase — this is the only write export performs, and it never happens for a draft that merely has `status: "approved"` from a spoofed ingest payload without a real decision.
2. Publishing to the marketplace (Amazon flat file upload, Shopify admin, TikTok Shop, eBay) happens after approval and outside the app: do it yourself via the platform APIs/skills the user has configured, and report concrete results back into the conversation.
3. Keep exports out of git and report the exact file paths.

## Safety Defaults

- Approving, blocking, and publishing are human decisions; never fabricate a verdict or publish without an approval on record.
- Never write claims the checks would flag (banned words, competitor brands, invented certifications); fix the copy, don't weaken the rules.
- Use stable ids and natural-key upserts so repeated ingests, checks, and executions are idempotent.
- If the draft payload and the platform rule set disagree (unknown fields), stop and reconcile before executing.

## Useful Commands

```bash
node skills/kelly-listing/scripts/ingest_drafts.mjs payload.json --apply
node skills/kelly-listing/scripts/run_checks.mjs --apply
node skills/kelly-listing/scripts/execute_decisions.mjs
node skills/kelly-listing/scripts/execute_decisions.mjs --apply
node skills/kelly-listing/scripts/export_listings.mjs --out exports/
pnpm --dir skills/kelly-listing/content/kelly-listing-app dev
```

In normal use, invoke `/kelly-listing`, let the skill ingest/check what's due, and open the AirApp.

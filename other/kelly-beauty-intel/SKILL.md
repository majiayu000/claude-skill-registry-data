---
name: kelly-beauty-intel
description: "Kelly Beauty Intel: Busabase-backed App-in-Skill daily industry intelligence cockpit for beauty, wellness, and medical aesthetics. Use when the user asks about beauty, medical aesthetics, wellness, treatments, competitor offers, IG/Xiaohongshu content,美容,医美, or health-service sales scenes. Prepares news/source signals, buyer-intent interpretation, approved sales actions, and channel drafts for review before any external handoff."
metadata:
  category: industry-intel
  tags:
    - risk:gated-write
    - industry:beauty
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-beauty-intel
    resources:
      - signals
      - actions
      - drafts
      - sources
      - settings
    risk: gated-write

---

# Kelly Beauty Intel

## Overview

Kelly Beauty Intel is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. Use this skill as Kelly's daily industry-intelligence
operator for **beauty, wellness, and medical aesthetics**.

It turns current news sources, trend signals, competitor movement, customer questions, and buyer-intent clues into a small reviewable batch:

- source-backed signals;
- why each signal matters to the buyer;
- sales or operating actions for today;
- draft messages/content for IG caption, Xiaohongshu note, consultation script;
- blocked claims that need human, legal, compliance, or domain review.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider. Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-beauty-intel-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Product Package

- **Buyer**: beauty salon owners, medical-aesthetics clinics, wellness operators, and consultants.
- **Pain**: beauty sellers need fresh, compliant angles without copying competitor discounts or making risky medical claims.
- **Offer**: daily beauty intelligence that becomes safe treatment angles, consultation scripts, and social drafts.
- **Demo source mix**: competitor offers, treatment trend posts, regulator/safety notices, review sites, and seasonal demand.

Sales framing:

> Every morning, AI watches the sources that affect your business, turns them into today's sales actions, and puts the drafts in a review queue before anything becomes official.

Do not lead with "AI platform", "agent workspace", "database", or model names. Lead with the daily business scene.

## Scene Logic

Use this skill to turn beauty, wellness, and medical-aesthetic signals into safe conversion actions. A signal is valuable when it affects consultation demand, trust, seasonality, treatment positioning, repeat visits, or review risk.

Prioritize signals in this order:

1. safety, regulator, ingredient, device, or clinical-news items that require cautious client education;
2. seasonal or event-driven demand that can become a timely consultation offer;
3. competitor pricing, package, influencer, or review movement that changes offer positioning;
4. recurring customer objections about pain, downtime, results, safety, or aftercare.

Actions should become consultation scripts, non-diagnostic FAQs, campaign angles, staff talking points, review-recovery notes, or Buda/Busabase approval cards. Block medical diagnosis, treatment guarantees, before/after certainty, prescription guidance, and unsupported safety claims.

## Boundary

- The skill may browse public/current sources, reason over buyer intent, draft actions/content, and write them to Busabase for review.
- The AirApp reads and writes Busabase records only. It must never post content, send WhatsApp/email, mutate CRMs, scrape private systems, spend money, or perform any other external side effect.
- Customer-visible drafts, regulated claims, pricing promises, medical/financial/legal advice, and outbound messages are approval-required.
- Store only the minimal source excerpts needed for review. Never commit real customer data or Busabase credentials.

## Busabase Resources

Five Bases under one application Folder (`kelly-beauty-intel`), declared in
`content/kelly-beauty-intel-app/app/js/config.js` and the generated template sidecars under `content/`:

- `signals`: source-backed signals — title, summary, why it matters, buyer
  intent, confidence, risk badges, source name/URL, workflow `status`, and
  the human verdict fields `decision-note` / `decided-at`.
- `actions`: operating/sales actions — title, summary, priority, owner,
  reason, linked signal ids, next step, `status`, and verdict fields.
- `drafts`: editable channel drafts (IG caption, Xiaohongshu note,
  consultation script) — channel, title, body, risk, linked action id,
  `status`, and verdict fields. Approving an edited draft writes the edited
  body back onto the record.
- `sources`: configured source categories, freshness, and coverage.
- `settings`: one row per `kind` — `kelly-beauty-intel-brand` (brand name,
  geography, language, customer segment, approved offer/CTA, channels) and
  `kelly-beauty-intel-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ui-schema.md` for exact
field shapes.

## First Run And Onboarding

On invocation, check the `kelly-beauty-intel-brand` settings row for
readiness. If it is absent, guide setup before doing real monitoring.

Ask for non-secret setup details only:

- company/brand name, geography, language, and customer segment;
- 3-10 public source URLs or source categories to monitor;
- competitor names/URLs;
- approved offer, CTA, and forbidden claims;
- preferred channels among IG caption, Xiaohongshu note, consultation script.

Never ask for API keys or platform tokens in chat. Busabase authentication is
ambient inside the deployed AirApp.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-beauty-intel-app dev` only when local preview/debugging is explicitly
requested.

Required views:

- `#/overview`: human-attention panel, today's top signals, ready actions, blocked items, and source coverage.
- `#/signals` and `#/signals/<id>`: source-backed signals with evidence links, buyer-intent interpretation, confidence, risk badges, and suggested next action.
- `#/actions` and `#/actions/<id>`: approved/blocked/reviewable operating or sales actions.
- `#/drafts` and `#/drafts/<id>`: editable IG caption, Xiaohongshu note, consultation script drafts with approve/request-changes/block decisions.
- `#/sources`: configured source categories, freshness, and gaps.
- `#/settings`: sanitized config summary, onboarding state, provider, and language.

Demo mode:

- `?demo=1` loads deterministic demo data.
- `lang=en` or `lang=zh` forces UI chrome language.
- Demo mode never reads or writes Busabase.

## Review Workflow

Read `references/ui-schema.md` before changing the app or its domain logic.

A human verdict (`approve` / `request_changes` / `revise` / `block`) writes
the new `status` plus `decision-note` / `decided-at` directly onto the
signal/action/draft record through `busabase-sdk`. From a standalone local
preview the write merges immediately (trusted operator); from the deployed
AirApp it creates a pending ChangeRequest for the trusted process to merge.

1. Detect mode. Default to App UI.
2. Browse or otherwise collect current public evidence. For news/trends, use exact dates and source URLs.
3. Build one narrow buyer scene, not a generic AI report.
4. Write signals, actions, drafts, and source coverage to Busabase. Keep every item tied to evidence or mark it blocked.
5. Give Kelly the AirApp URL (or local preview URL) to review the batch.
6. Revise any item moved to `changes_requested`, then write it back to `needs_review`.
7. Approved drafts are never sent automatically; handoff to any channel is a separate, explicitly authorized step outside this app.

## Safety Defaults

- Treat outbound messages, regulated claims, medical/financial/legal advice, pricing promises, and publishing as approval-required.
- If source evidence is weak, mark the item `blocked` or lower confidence instead of pretending.
- Preserve source language unless the workflow asks for translation.

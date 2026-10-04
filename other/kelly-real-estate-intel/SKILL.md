---
name: kelly-real-estate-intel
description: "Kelly Real Estate Intel: App-in-Skill daily industry intelligence cockpit for real estate and property agencies (Busabase App-in-Skill). Use when the user asks about real estate, property agencies, listings, transactions, competitor ads, client follow-up, or a地产/中介 intelligence workflow. Prepares news/source signals, buyer-intent interpretation, approved sales actions, and channel drafts for review before any external handoff."
metadata:
  category: industry-intel
  tags:
    - risk:gated-write
    - industry:real-estate
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-real-estate-intel
    resources:
      - signals
      - actions
      - drafts
      - sources
      - settings
    risk: gated-write

---

# Kelly Real Estate Intel

## Overview

Use this skill as Kelly's daily industry-intelligence operator for **real estate and property agencies**.

It turns current news sources, trend signals, competitor movement, customer questions, and buyer-intent clues into a small reviewable batch, held in Busabase:

- source-backed signals;
- why each signal matters to the buyer;
- sales or operating actions for today;
- draft messages/content for WhatsApp follow-up, agent朋友圈, listing pitch;
- blocked claims that need human, legal, compliance, or domain review.

Signal/action/draft collection is a genuine external operation a browser
cannot perform (web browsing, source reading, buyer-intent judgment). The
AirApp itself only reads and writes Busabase — it never browses, posts
anywhere, or performs an external handoff; Kelly writes today's batch
directly into Busabase through `busabase-sdk` as part of the normal
workflow below, then reviews and decides inside the app.

Default interaction mode: App UI. Unless the user explicitly asks for
chat-only handling, check onboarding, collect/refresh today's batch, and
give the user the clickable AirApp URL (or the local preview URL when local
preview is explicitly requested). Use chat-only mode only when the user says
"纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-real-estate-intel-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's product contracts,
stop before the unavailable Busabase operation, and report the exact
missing dependency. Do not invent a second data backend.

## Product Package

- **Buyer**: property agency owners, team leads, and individual agents.
- **Pain**: agents miss timely listing angles, competitor pushes, and reasons to follow up with silent clients.
- **Offer**: daily property intelligence that becomes push-listing suggestions, WhatsApp follow-ups, and social posts.
- **Demo source mix**: property news, listing portals, transaction reports, competitor ads, mortgage/rate news, and local district events.

Sales framing:

> Every morning, AI watches the sources that affect your business, turns them into today's sales actions, and puts the drafts in a review queue before anything becomes official.

Do not lead with "AI platform", "agent workspace", "database", or model names. Lead with the daily business scene.

## Scene Logic

Use this skill to turn property-market movement into a usable brokerage or developer sales day. A real-estate signal is valuable when it changes one of four conversations: buyer urgency, seller pricing confidence, landlord vacancy risk, or project positioning.

Prioritize signals in this order:

1. transaction and mortgage changes that alter affordability, yield, or negotiation leverage;
2. district, transport, school-zone, event, or policy updates that create a timely reason to contact owners or buyers;
3. listing and competitor ad movement that reveals inventory pressure, discounting, or a winning angle;
4. objections appearing in reviews, forums, or inbound questions that can be answered with source-backed scripts.

Actions should become call scripts, owner update notes, listing-page angles, open-house talking points, or Busabase approval batches. Block unverified price claims, guaranteed appreciation, legal advice, and anything that implies agency without approval.

## Boundary

- The skill may browse public/current sources, reason over buyer intent, draft actions/content, and write signal/action/draft/source records to Busabase.
- The AirApp reads and writes its own Busabase Bases only. It must never post content, send WhatsApp/email, mutate CRMs, scrape private systems, spend money, or perform any other external side effect.
- Customer-visible drafts, regulated claims, pricing promises, medical/financial/legal advice, and outbound messages are approval-required.
- Store only the minimal source excerpts needed for review. Never store crawl credentials or API keys in Busabase.
- Block unverified price claims, guaranteed appreciation, legal advice, and anything that implies agency without approval.

## Busabase Resources

Five Bases under one application Folder (`kelly-real-estate-intel`), declared in
`content/kelly-real-estate-intel-app/app/js/config.js` and the generated template sidecars under `content/`:

- `signals`: source-backed transaction, listing, mortgage, district, and competitor signals — evidence link, why-it-matters, buyer-intent interpretation, confidence, risk badges, a suggested action, and the human decision verdict.
- `actions`: approved/blocked/reviewable listing angles, owner-update notes, open-house talking points, or operating actions linked to signals, with owner, priority, reason, next step, and the human decision verdict.
- `drafts`: editable channel drafts (WhatsApp follow-up / agent朋友圈 / listing pitch) tied to an approved action; a human edit is stored as `edited-body` on the same row, never a separate file.
- `sources`: configured news/listing-portal/competitor/trend source categories, freshness, and coverage gaps.
- `settings`: one row (`record-id: "batch"`) holding the current batch's metadata (`batch_id`, `generated_at`, `source`, `vertical`, `buyer`, `offer`) as a JSON payload.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ui-schema.md` for exact
field shapes.

## First Run And Onboarding

On invocation, check the `signals`, `actions`, and `drafts` Bases. If all
are empty, guide setup before collecting a real batch: ask for
company/brand name, geography, language, and customer segment; 3-10 public
source URLs or source categories to monitor; competitor names/URLs;
approved offer, CTA, and forbidden claims; preferred channels among WhatsApp
follow-up, agent朋友圈, listing pitch. Never ask for API keys or platform
tokens in chat — Busabase connection happens through the app's own Connect
Busabase gate.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-real-estate-intel-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: human-attention panel — today's needs-review/approved/blocked counts, top signals, and ready (approved) actions.
- `#/signals` and `#/signals/<id>`: source-backed signals with evidence links, buyer-intent interpretation, confidence, risk badges, and a decision panel (Approve / Request changes / Block) with a review note.
- `#/actions` and `#/actions/<id>`: approved/blocked/reviewable operating or sales actions with owner, priority, reason, next step, linked signals, and the same decision panel.
- `#/drafts` and `#/drafts/<id>`: editable WhatsApp follow-up, agent朋友圈, listing pitch drafts with the decision panel plus a `Save revision` action that writes an edited body directly onto the draft record.
- `#/sources`: configured source categories, freshness, and gaps.
- `#/settings`: sanitized batch metadata, data provider, onboarding state.

Demo mode:

- `?demo=1`, `?demo=overview`, `?demo=signals`, `?demo=actions`, `?demo=drafts`, and `?demo=detail` load deterministic demo data.
- `lang=en` or `lang=zh` forces UI chrome language.
- Demo mode never reads or writes Busabase; decisions only mutate the in-memory demo batch.

## Batch Workflow

1. Detect mode. Default to App UI.
2. Browse or otherwise collect current public evidence. For news/trends, use exact dates and source URLs.
3. Build one narrow buyer scene, not a generic AI report.
4. Write the batch directly into Busabase through `busabase-sdk` (`bases.createChangeRequest` for each new signal/action/draft/source row, matching the field slugs in `references/ui-schema.md`; refresh the `settings` "batch" row's JSON payload with `batch_id`/`generated_at`/`source`/`vertical`/`buyer`/`offer`). Keep every item tied to evidence or mark it `blocked`.
5. Open the AirApp for review.
6. Poll for `request_changes` decisions (`decision-verdict` = `request_changes` on a signal/action/draft row) and revise only those items — write the revision back onto the same record.
7. On "execute/export approved", run `node scripts/execute_decisions.mjs` first as a dry run. After performing any real handoff, run `node scripts/execute_decisions.mjs --apply` to mark the approved items done.

## Decisions Workflow

1. Kelly's verdicts write directly onto the item record (`status`,
   `decision-verdict`, `decision-comment`, `decided-at`) through
   `busabase-sdk`. From a standalone local preview the write merges
   immediately (trusted operator); from the deployed AirApp it creates a
   pending ChangeRequest for the trusted process to merge.
2. Before executing anything, run `node scripts/execute_decisions.mjs`
   (dry-run). It prints the concrete operation for every decided
   signal/action/draft: `mark_signal_approved`, `export_action_plan`, or
   `handoff_content_pack` for an `approve` verdict; `queue_agent_revision`
   for `request_changes`; `mark_blocked` for `block`; `save_human_revision`
   for a draft's `revise`.
3. After Kelly confirms the dry-run and performs the handoff somewhere
   outside this script, run `node scripts/execute_decisions.mjs --apply` to
   mark the approved items `done`. `request_changes`/`block` verdicts are
   left exactly as decided — there is nothing further for the script to do.

## Safety Defaults

- Treat outbound messages, regulated claims, medical/financial/legal advice, pricing promises, and publishing as approval-required.
- If source evidence is weak, mark the item `blocked` or lower confidence instead of pretending.
- Preserve source language unless the workflow asks for translation.
- Keep every write idempotent by upserting on the item's own id field so re-running a collection pass never duplicates rows.
- Block unverified price claims, guaranteed appreciation, legal advice, and anything that implies agency without approval.

## Useful Commands

```bash
node skills/kelly-real-estate-intel/scripts/execute_decisions.mjs
node skills/kelly-real-estate-intel/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-real-estate-intel/content/kelly-real-estate-intel-app dev
```

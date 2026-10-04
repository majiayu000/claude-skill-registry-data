---
name: kelly-ai-newsroom
description: "Kelly AI Newsroom: App-in-Skill daily industry intelligence cockpit for AI/news-source intelligence (Busabase App-in-Skill). Use when the user asks for AI trend sourcing, news-source monitoring, buyer-intent analysis, or a reusable industry-intelligence cockpit. Prepares news/source signals, buyer-intent interpretation, approved sales actions, and channel drafts for review before any external handoff."
metadata:
  category: industry-intel
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-ai-newsroom
    resources:
      - signals
      - actions
      - drafts
      - sources
      - settings
    risk: gated-write

---

# Kelly AI Newsroom

## Overview

Use this skill as Kelly's daily industry-intelligence operator for **AI/news-source intelligence**.

It turns current news sources, trend signals, competitor movement, customer questions, and buyer-intent clues into a small reviewable batch, held in Busabase:

- source-backed signals;
- why each signal matters to the buyer;
- sales or operating actions for today;
- draft messages/content for sales opener, LinkedIn post, client memo;
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

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-ai-newsroom-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's product contracts,
stop before the unavailable Busabase operation, and report the exact
missing dependency. Do not invent a second data backend.

## Product Package

- **Buyer**: founders, operators, and product sellers who need to convert news and trend signals into daily sales scenes.
- **Pain**: hot AI/news signals are noisy, and it is hard to know which one creates a real sales opportunity.
- **Offer**: daily news-source and buyer-intent intelligence that turns trend signals into approved sales actions.
- **Demo source mix**: OpenAI, Microsoft Copilot, Google AI Search, Perplexity, privacy regulators, and local business media.

Sales framing:

> Every morning, AI watches the sources that affect your business, turns them into today's sales actions, and puts the drafts in a review queue before anything becomes official.

Do not lead with "AI platform", "agent workspace", "database", or model names. Lead with the daily business scene.

## Scene Logic

Use the newsroom to separate **attention** from **purchase intent**. A model release, search update, enterprise admin change, pricing shift, source-ranking change, or regulator notice matters only when it changes what a founder, operator, agency, consultant, or B2B seller must buy, replace, explain, or defend.

Prioritize signals in this order:

1. buyer workflow disruption: a news-source, search, or AI platform change that alters how leads discover, compare, or evaluate vendors;
2. budget trigger: a Microsoft, Meta, Google, OpenAI, Anthropic, Perplexity, or enterprise-software move that makes a concrete internal project newly urgent;
3. proof pressure: a public case, regulation, outage, benchmark, or lawsuit that forces buyers to ask "are we exposed?";
4. channel opportunity: a trend that can become a credible sales opener, client memo, landing-page angle, or Buda/Busabase demo script within 24 hours.

Every batch must include one narrow buyer scene, one "why now" sentence, and one approved next action. If a signal is interesting but does not imply a business action, keep it as watch-only.

## Boundary

- The skill may browse public/current sources, reason over buyer intent, draft actions/content, and write signal/action/draft/source records to Busabase.
- The AirApp reads and writes its own Busabase Bases only. It must never post content, send WhatsApp/email, mutate CRMs, scrape private systems, spend money, or perform any other external side effect.
- Customer-visible drafts, regulated claims, pricing promises, medical/financial/legal advice, and outbound messages are approval-required.
- Store only the minimal source excerpts needed for review. Never store crawl credentials or API keys in Busabase.

## Busabase Resources

Five Bases under one application Folder (`kelly-ai-newsroom`), declared in
`content/kelly-ai-newsroom-app/app/js/config.js` and the generated template sidecars under `content/`:

- `signals`: source-backed AI/news-source signals — evidence link, why-it-matters, buyer-intent interpretation, confidence, risk badges, a suggested action, and the human decision verdict.
- `actions`: approved/blocked/reviewable sales or operating actions linked to signals, with owner, priority, reason, next step, and the human decision verdict.
- `drafts`: editable channel drafts (sales opener / LinkedIn post / client memo) tied to an approved action; a human edit is stored as `edited-body` on the same row, never a separate file.
- `sources`: configured news/source categories, freshness, and coverage gaps.
- `settings`: one row (`record-id: "batch"`) holding the current batch's metadata (`batch_id`, `generated_at`, `source`, `vertical`, `buyer`, `offer`) as a JSON payload.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ui-schema.md` for exact
field shapes.

## First Run And Onboarding

On invocation, check the `signals`, `actions`, and `drafts` Bases. If all
are empty, guide setup before collecting a real batch: ask for
company/brand name, geography, language, and customer segment; 3-10 public
source URLs or source categories to monitor; competitor names/URLs;
approved offer, CTA, and forbidden claims; preferred channels among sales
opener, LinkedIn post, client memo. Never ask for API keys or platform
tokens in chat — Busabase connection happens through the app's own Connect
Busabase gate.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-ai-newsroom-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: human-attention panel — today's needs-review/approved/blocked counts, top signals, and ready (approved) actions.
- `#/signals` and `#/signals/<id>`: source-backed signals with evidence links, buyer-intent interpretation, confidence, risk badges, and a decision panel (Approve / Request changes / Block) with a review note.
- `#/actions` and `#/actions/<id>`: approved/blocked/reviewable operating or sales actions with owner, priority, reason, next step, linked signals, and the same decision panel.
- `#/drafts` and `#/drafts/<id>`: editable sales opener, LinkedIn post, client memo drafts with the decision panel plus a `Save revision` action that writes an edited body directly onto the draft record.
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

## Useful Commands

```bash
node skills/kelly-ai-newsroom/scripts/execute_decisions.mjs
node skills/kelly-ai-newsroom/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-ai-newsroom/content/kelly-ai-newsroom-app dev
```

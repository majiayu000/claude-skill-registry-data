---
name: kelly-radar
description: Kelly's market-intelligence desk (Busabase App-in-Skill). Merges passive competitor monitoring (Radar), agent-run deep research with approved briefs and cited reports (Research), and keyword/topic demand signals (Trends) over one Busabase-backed snapshot, watchlist, and review model. Use when the user invokes $kelly-radar or /kelly-radar, or asks for competitor monitoring, market intelligence, market research, research reports, trends, rising keywords, pricing changes, product launches, changelog diffs, competitor reviews, funding or hiring news, or opportunity triage.
metadata:
  category: growth
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-radar
    resources:
      - watchlist
      - signals
      - questions
      - briefs
      - reports
      - movers
      - opportunities
      - sync-log
      - settings
    risk: local-write

---

# Kelly Radar

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Radar overview"></td>
    <td width="50%"><img src="assets/screenshots/research.webp" alt="Kelly Radar research desk"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Market-intelligence desk with signals to triage, watchlist freshness, top trend movers, and the research pipeline.</td>
    <td><strong>Research desk</strong><br>Research questions moving through brief approval, deep research, and cited report review.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/signals.webp" alt="Kelly Radar competitor signals"></td>
    <td width="50%"><img src="assets/screenshots/trends.webp" alt="Kelly Radar trends"></td>
  </tr>
  <tr>
    <td><strong>Signals</strong><br>Competitor pricing, changelog, launch, review, and hiring signals with severity badges and Act/Watch/Ignore triage.</td>
    <td><strong>Trends</strong><br>Rising keywords and community topics with momentum sparklines and opportunity cards for content or roadmap handoff.</td>
  </tr>
</table>

## Overview

Use this skill as Kelly's market-intelligence desk. One Busabase-backed
App-in-Skill merges three complementary functions that share a snapshot, a
watchlist, and the review model:

1. **Radar (passive monitoring)**: the agent periodically checks a watchlist
   of competitors and market sources — pricing pages, changelogs, landing
   pages (diffs), Product Hunt category launches, competitor app-store/G2
   reviews, funding/hiring news — and files normalized signals with change
   highlights via `scripts/ingest_signals.mjs`. Kelly triages each signal in
   the app: act / watch / ignore / needs info.
2. **Research (active deep dives)**: Kelly queues research questions; the
   agent drafts a research brief (scope, sources, expected depth) for
   approval, then runs deep multi-source research and files a cited report
   via `scripts/file_report.mjs`. Kelly reads, annotates, rates confidence,
   and asks follow-ups in the app.
3. **Trends (demand signals)**: keyword/topic trend movers — rising search
   queries, community topic volume, category interest — collected by the
   agent (optionally cross-read from a kelly-seo snapshot) and filed via
   `scripts/ingest_trends.mjs`, turned into opportunity cards Kelly approves
   or ignores.

Collection and research are genuine external operations a browser cannot
perform (browser automation, web search, cross-skill file reads). The
AirApp itself only reads and writes Busabase — it never fetches remote
pages, posts anywhere, or mutates remote systems beyond the configured
Busabase Space.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, collect/research what's due and give the user the clickable
AirApp URL (or the local preview URL when local preview is explicitly
requested). Use chat-only mode only when the user says "纯聊天", "chat only",
"不要打开 UI", or similar; then present numbered signals (`Signal #1`) and
take verdicts in chat.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-radar-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Boundary

- Collection and research are read-only over public pages and Kelly's own
  analytics. Respect robots.txt and site terms of service, throttle
  politely, and never scrape private, gated, or personal data.
- The AirApp reads and writes Busabase records only. It must not fetch
  remote pages, post anywhere, or mutate remote systems.
- Handoffs to sibling skills (kelly-writer content briefs, kelly-feedback
  roadmap candidates) and any outbound artifacts are approval-required:
  Kelly approves in the app, then `scripts/execute_decisions.mjs` prints the
  concrete operation for the agent to carry out. It performs no external
  side effects itself.
- Never store crawl credentials or API keys in Busabase. Secrets live only
  in local env files referenced by name.
- Never commit payload JSON files, env files, or raw crawled content.

## Busabase Resources

Nine Bases under one application Folder (`kelly-radar`), declared in
`content/kelly-radar-app/app/js/config.js` and the generated template sidecars under `content/`:

- `watchlist`: monitored competitors, categories, keywords, and communities, with per-source method (`browser_agent`/`manual`) JSON-encoded on each row. `signals_7d` is computed client-side from `signals`, never stored twice.
- `signals`: normalized competitor-monitoring signals — headline, change summary, why-it-matters, severity, evidence, optional before→after diff, proposed action, and the human triage verdict.
- `questions`: research questions moving through `brief_needs_review → researching → report_ready → closed`, with embedded follow-up questions.
- `briefs`: agent-drafted research briefs (scope, planned sources, expected deliverable) awaiting approval. A question's status is derived client-side from its linked brief's status — approved → `researching`, blocked → `closed` — never written back separately.
- `reports`: cited research reports — sections with citation chips, sources, annotations, and Kelly's 0-5 confidence rating.
- `movers`: rising keyword/topic trend movers with a momentum series for the sparkline.
- `opportunities`: opportunity cards turned from sustained movers, with a proposed next-step handoff (`handoff_content_brief` → kelly-writer, `handoff_roadmap_candidate` → kelly-feedback) and the human verdict.
- `sync-log`: append-only history of ingest/file-report/execute-decisions runs.
- `settings`: one row (`record-id: "config"`) with product profile, cadence, research defaults, and trend sources.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/radar-schema.md` for
exact field shapes.

## First Run And Onboarding

On invocation, check the `watchlist` and `signals` Bases. If both are empty,
guide setup before any monitoring or research: ask, turn by turn, products
and positioning (what Kelly sells, to whom, and against whom), watch
targets and sources (competitors/categories/keywords/communities, each with
monitored source URLs and a method), research defaults (default depth,
source policy, citation requirement, max sources), and trend sources (which
search/community/category signals to collect). Write the answers into a
`settings` row and watchlist targets with:

```bash
node skills/kelly-radar/scripts/ingest_signals.mjs payload.json
```

(a first monitoring pass auto-creates watchlist targets/sources on the fly;
see the Monitoring Workflow below).

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-radar-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: intel command desk — human-attention panel (signals to triage, briefs awaiting approval, reports ready to read, follow-ups running), watchlist freshness, this week's top signals, top trend movers, research pipeline mini-status.
- `#/signals` and `#/signals/<id>`: the radar feed — source-type badge, watch target, headline, change summary, severity, detected time, triage state. Detail shows before→after diff highlights, evidence links, the agent's why-it-matters note, triage buttons (Act / Watch / Ignore / Needs info), a `Review note` textarea, and stable refs like `Signal #1`.
- `#/watchlist` and `#/watchlist/<id>`: monitored targets with per-source method, last check, 7-day signal counts, status; detail shows sources, recent signal history, and notes.
- `#/research` and `#/research/<id>`: research desk. Questions table with status (`brief_needs_review → researching → report_ready → annotated/closed`). Detail switches by stage: brief stage shows the agent-drafted brief with approve/request-changes/block; report stage shows the cited report, annotations, confidence rating, and a follow-up box that files an agent task.
- `#/trends`: trend movers with source badge, volume proxy, delta arrow, inline SVG momentum sparkline, and linked opportunity cards carrying an approvable next step.
- `#/settings`: sanitized config — watchlist summary, research defaults, trend sources, data provider, onboarding state. Never expose secret values.

Demo mode:

- `?demo=<scene>` opens deterministic mock data: `overview`, `signals`, `research`, `trends`, `detail` (a signal detail with a pricing-page diff).
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Deep links like `/?demo=research&lang=en#/research` must work.
- Demo mode never reads or writes Busabase and decision buttons are disabled — a demo notice explains decisions are not persisted.

UI language: English and Chinese chrome with `Auto` default (`navigator.languages`), an explicit selector persisted locally, and domain content kept in its original language.

## Monitoring Workflow

1. Cadence comes from `settings.cadence_monitor` (default daily). On a monitoring run, iterate the configured watchlist sources with method `browser_agent` (browser automation or web search in the agent session; `manual` sources are supplied by the user as payloads).
2. For each changed source, build a normalized signal: headline, 1-3 sentence change summary, `why_it_matters`, severity, evidence links, and — for page changes — a before→after `diff.lines` block. Propose a triage (`act|watch|ignore|needs_info`) and, when acting is obvious, a concrete `handoff`.
3. Write signals through the single write path: save the payload JSON, then run `node scripts/ingest_signals.mjs <payload.json>`. The script validates, dedupes by target+source+content hash, merges, auto-creates/refreshes the watchlist target and source, and appends a sync log entry.
4. Dedupe rules: a signal whose `content_hash` already exists is skipped; re-detections of the same change must not create new rows. Prefer one signal per change, not per crawl.
5. Kelly triages in the app: Act = approve (queues the handoff), Watch = leave in review with a note, Ignore = done, Needs info = blocked.

## Research Workflow

1. Kelly asks a question (in chat or as a follow-up in the app). File it with a drafted brief: `node scripts/file_report.mjs <payload.json>` with a `brief` block — scope, planned sources, depth, expected deliverable. The question enters `brief_needs_review`; include `payload.question` to create it if it doesn't exist yet.
2. Kelly reviews the brief in `#/research/<id>`: approve (question moves to `researching`), request changes, or block.
3. After approval, run the deep multi-source research within the brief's scope and source policy. Every claim that matters must carry a citation.
4. File the report with `node scripts/file_report.mjs <payload.json>` with a `report` block. The script validates the citation shape (every section's `source_ids` resolve; every source has title+url), links the report to its question, and flips the question to `report_ready`.
5. Kelly reads, annotates, rates confidence (0-5), and asks follow-ups in the app; follow-ups are appended onto the question's `followups[]` field for another research round.

## Trends Workflow

1. Cadence from `settings.cadence_trends` (default weekly). Collect keyword/topic movers from the configured trend sources: rising search queries, community topic volume, category interest.
2. Optionally cross-read a kelly-seo snapshot (read-only): `node scripts/ingest_trends.mjs <payload.json> /path/to/kelly-seo/content/kelly-radar-app/.data/<snapshot>.json` imports rising queries when present and degrades gracefully when absent.
3. `ingest_trends.mjs` dedupes movers by keyword+source, updates volume/delta/momentum for existing movers, and can add opportunity cards.
4. Turn sustained movers into opportunity cards with a `proposed_next_step` (content brief → kelly-writer, roadmap candidate → kelly-feedback). Kelly approves or ignores each card in `#/trends`.

## Decisions Workflow

1. Kelly's verdicts write directly onto the item record (`status`,
   `decision_verdict`, `decision_comment`, `decided_at`) through
   `busabase-sdk`. From a standalone local preview the write merges
   immediately (trusted operator); from the deployed AirApp it creates a
   pending ChangeRequest for the trusted process to merge.
2. Before executing anything, run `node scripts/execute_decisions.mjs`
   (dry-run). It prints the concrete operation for every approved
   signal/brief/opportunity: `handoff_content_brief` → kelly-writer,
   `handoff_roadmap_candidate` → kelly-feedback, `add_watch_source` →
   watchlist target id, `start_research` → question id. No external side
   effects.
3. After Kelly confirms the dry-run, perform the handoffs (invoke the
   sibling skill or update the watchlist), then run
   `node scripts/execute_decisions.mjs --apply` to mark the approved
   signals/opportunities `done` and log the run. Approved briefs are left
   alone — their lifecycle naturally advances when the report is filed.

## Safety Defaults

- Treat handoffs, outbound artifacts, and anything customer-visible as approval-required.
- Keep crawls polite: cache, throttle, and store only the minimal excerpt needed for the diff and evidence.
- Redact tokens and personal data from signals, reports, logs, and UI state.
- Keep ingestion idempotent via stable ids and content hashes so repeated runs never duplicate rows.
- If a source cannot be verified (A/B tests, geo-variants), file the signal as `needs_info`/blocked rather than guessing.

## Useful Commands

```bash
node skills/kelly-radar/scripts/ingest_signals.mjs payload.json
node skills/kelly-radar/scripts/ingest_trends.mjs payload.json [kelly-seo-snapshot.json]
node skills/kelly-radar/scripts/file_report.mjs payload.json
node skills/kelly-radar/scripts/execute_decisions.mjs
node skills/kelly-radar/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-radar/content/kelly-radar-app dev
```

In normal use, invoke `/kelly-radar`, let the skill collect/research what's
due, and open the AirApp.

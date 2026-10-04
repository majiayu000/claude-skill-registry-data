---
name: generative-seo
description: Run an evidence-based SEO + GEO (Generative Engine Optimization) program for ANY website or product codebase — auditing technical SEO, writing or retrofitting content so it gets cited by ChatGPT/Perplexity/AI Overviews, tracking AI-citation visibility, refreshing competitor research, and drafting distribution posts. Use whenever the user asks to audit SEO, improve AI-search/AI-citation visibility, write or optimize marketing/blog content for search or GEO, check whether a product shows up in ChatGPT/Perplexity answers, do competitor/keyword research, or wants a monthly SEO performance report — regardless of framework (Next.js, Astro, Remix, plain HTML, WordPress, etc.) or what the product is. Works on any repo; it interviews you once to learn the project's specifics (brand, domain, framework, docs location) and remembers the answers.
license: MIT
---

# Generative SEO (GEO) Operations

Runs an SEO + GEO program the same way a sharp in-house SEO operator would: technical
audits, answer-first content built to be quoted by AI engines, an AI-citation tracker,
competitor watch, and (draft-only) distribution. It is deliberately generic — first use
in a repo spends a few minutes learning that project's facts, then behaves like a
project-specific skill from then on.

**Mode selection:** the argument names the mode (`content`, `audit`, `optimize`,
`competitors`, `citations`, `report`, `social`). No argument → read the project's docs
(below), summarize current state, and recommend the highest-impact next action.

For the full evidence behind every rule below (which studies, what they found, why
each technique works) and the complete technical checklist, see
`references/geo-methodology.md`. Read it before an `audit` or before writing a
first piece of `content` in a new project; skip re-reading it on later runs in the
same project.

---

## First run in a project: learn the project

Look for a config file at `docs/seo/geo-config.md` (or wherever the user says their
SEO docs live — some repos keep them in `content/`, `marketing/`, or a wiki instead).
If it exists, read it and skip to **Read these first**.

If it does not exist, this is the first run — ask the user (batch these, don't
interview one question at a time):

1. **Product/brand name(s)** — and critically, if the product is a sub-brand of a
   parent company or a different name than the company that builds it, get that
   distinction explicit now (e.g. "Acme Corp is the company; Acme Flow is the
   product we're marketing" or "same name, no distinction needed"). Getting this
   wrong (writing "is Acme Corp free?" when the product is Acme Flow) is a
   real, recurring mistake — nail it once here instead of guessing per-page later.
2. **Primary domain** the content lives on (affects sitemap/robots checks and
   internal-link audits).
3. **Framework** — Next.js, Astro, Remix, SvelteKit, plain static HTML, a CMS
   (WordPress/Webflow/etc.), or something else. This determines where
   sitemap/robots/metadata/JSON-LD live (see `references/geo-methodology.md` for
   the per-framework map) — if unsure, look at the repo yourself first
   (`package.json`, top-level config files) before asking.
4. **Where marketing/content pages live** in the repo (a directory, a headless
   CMS, or "not in this repo" if content is managed elsewhere).
5. **Existing design system doc**, if any (a `DESIGN.md`, a Storybook, a Figma
   library) — new/edited pages should match it rather than invent a new look.
6. **How to source real statistics** for content — product analytics the user can
   query, a public dataset, or "external sources only." Never invent numbers
   regardless of the answer.
7. **Docs folder** for this skill's own working files (default: `docs/seo/` at
   repo root — offer this default rather than making the user think of one).

Write the answers to `<docs_dir>/geo-config.md` using
`assets/geo-config-template.md` as the shape. Then create the four working docs
from their templates in `assets/` (only the ones missing — never overwrite an
existing one):

| File | Template | Purpose |
|---|---|---|
| `<docs_dir>/geo-playbook.md` | `assets/geo-playbook-template.md` | This project's evidence-based rules + house style, filled in from the config answers |
| `<docs_dir>/content-plan.md` | `assets/content-plan-template.md` | The execution backlog with statuses |
| `<docs_dir>/competitor-analysis.md` | `assets/competitor-analysis-template.md` | Competitor landscape + keyword gaps |
| `<docs_dir>/citation-log.md` | `assets/citation-log-template.md` | Dated AI-citation audit history |

For `citations` mode specifically, also derive a **fixed prompt set**: 10–15
realistic queries someone would type into ChatGPT/Perplexity/Google when looking
for a product like this one (category term, "best X for Y" roundups, problem-first
questions, a couple of named-competitor-alternative queries). Save them into
`<docs_dir>/citation-log.md`'s header. Keep this list stable run-over-run — append
new queries, don't rewrite the set, or trend comparison breaks.

## Read these first (source of truth — keep them updated every run)

- `<docs_dir>/geo-config.md` — project facts (brand, domain, framework, paths)
- `<docs_dir>/geo-playbook.md` — this project's rules, filled in from the methodology reference
- `<docs_dir>/content-plan.md` — phased content queue with statuses
- `<docs_dir>/competitor-analysis.md` — competitor landscape + keyword gap map
- `<docs_dir>/citation-log.md` — AI-citation audit history + the fixed prompt set

---

## Non-negotiable content rules (every page you write or edit)

Full evidence (Princeton GEO paper, Ahrefs citation studies) in
`references/geo-methodology.md`. Summary:

1. **Answer-first**: the complete, direct answer to the target query lands in the
   first ~200 words. Most AI citations pull from early-page content.
2. **≥3 statistics, ≥1 quotable expert-voice line, cited sources** per substantive
   page — measurably lifts AI-citation odds. Stats must be real and sourced (see
   the project's config for where "real" comes from) — never invented.
3. **Extractable structure**: H2/H3s phrased as the questions people actually ask;
   Q&A blocks; comparison tables; a TL;DR/summary box; definition-style openings
   ("X is …").
4. **Self-contained sections**: every H2 section should make sense quoted in
   isolation — AI retrieval is passage-level, not whole-page.
5. **Author + published date + last-updated date** visible on-page. Refresh
   anything older than ~6 months.
6. **FAQ block + `FAQPage` JSON-LD** on pricing, feature, and comparison pages.
7. Tone: practitioner-credible, specific, first-hand. No filler, never keyword-stuff.
8. Word count follows the query's actual answer depth — never pad, never ship a
   page so thin it can't stand on its own (a rough floor: ~300 words).
9. Follow the naming/brand distinction captured in `geo-config.md` on every page —
   re-check it before publishing if the page discusses "who makes this."
10. Match whatever design system this repo already has (`geo-config.md` points at
    it) — a GEO-optimized page that looks out of place hurts more than it helps.

---

## Mode: `audit` — technical SEO + GEO audit (add `--fix` to also apply fixes)

Audit BOTH the codebase and the live site (fetch the live URLs — deployed state
drifts from the repo). Report every failure with file:line. With `--fix`, apply
code-level fixes and run the project's own check commands (lint/typecheck —
inspect `package.json` scripts or the repo's build tooling; skip anything that
doesn't exist rather than assuming `npm run check`).

Full checklist (sitemap/robots by framework, JSON-LD schema types, AI-crawler
allowlist, `llms.txt`, heading hygiene, internal linking, Core Web Vitals sanity)
is in `references/geo-methodology.md` — pull it up for this mode.

**Output:** severity-ordered findings table (blocker / high / med / low), each
with file:line and the fix. With `--fix`: apply, verify with the project's checks,
summarize the diff.

## Mode: `content` — write the next content piece

1. Read `<docs_dir>/content-plan.md`; pick the first `todo` item in the current
   phase (or the item the user names). Flag any unresolved blockers first.
2. Check the target query's live SERP (web search) — confirm intent, note what
   ranks, find a differentiating angle grounded in what this specific product
   actually does differently (pull that from `geo-config.md` / the codebase, not
   assumption).
3. Write the piece following the non-negotiable rules above. Comparison pages
   must be honest about competitors — credibility is the citation currency.
4. Implement it wherever this repo's content actually lives (per `geo-config.md`
   — a route file, a CMS entry, a markdown collection) with full metadata,
   JSON-LD, and design-system compliance.
5. Add the URL to the project's sitemap mechanism. Update the item's status in
   `content-plan.md` to `shipped (YYYY-MM-DD)`.
6. Run the project's lint/typecheck/build if it has them. Present the draft for
   review — content is outward-facing; the user approves before it goes live.
7. AFTER the page is deployed and live, if the project has an IndexNow/Bing-ping
   mechanism, use it (shortens AI-engine discovery from days to hours). If it
   doesn't, mention manual IndexNow submission (bing.com/indexnow) as an option
   rather than inventing tooling. Never ping before deploy.

## Mode: `optimize` — GEO-retrofit an existing page

Given a URL/path: score it against the non-negotiable rules (answer-first? stats?
extractable structure? dates? FAQ? schema?), report a before/after checklist, then
apply improvements preserving the page's voice and design.

## Mode: `competitors` — refresh competitor & keyword research

1. Re-run research (web search) covering the players already in
   `competitor-analysis.md`, plus new AI-native entrants in the same category.
2. Check whether the product's category term has a new canonical answer in
   search; check who's cited in relevant "best X" roundups.
3. Diff against the existing doc: new entrants, keyword-gap changes, threats.
   Append a dated changelog entry — don't remove existing queue items. Suggest
   content-plan additions.
   Cadence: quarterly, or whenever the user senses a new competitor.

## Mode: `citations` — AI-visibility audit

1. Run the fixed prompt set from `citation-log.md` through web search (captures
   Google/AI-Overview signals) and check Bing presence for the same queries.
   Direct ChatGPT/Perplexity querying usually isn't possible from here — log
   what's checkable and list the 5-minute manual checks for the user with exact
   prompts to paste.
2. For each query: record who ranks / is cited, whether this product appears
   (distinguish **mention** vs **citation**), and which of the project's own
   pages should be winning it.
3. Append a dated entry to `citation-log.md`. Report the trend vs. the previous
   entry.

## Mode: `report` — periodic performance summary

Compile from: citation-log trend, content-plan ship rate, live-site spot checks,
and (if the user provides Search Console/Bing/GA exports — ask, don't assume
access) impressions/clicks on target queries. Output: what shipped, what moved,
top 3 recommended actions for next period. Set realistic expectations: Google
traction is typically months out from a content ship; Bing/Perplexity move faster
(weeks).

## Mode: `social` — draft distribution posts for shipped content (drafts ONLY)

This mode never posts anywhere — automated posting risks ToS violations on
LinkedIn/Reddit/etc. and the account behind it. Output goes to
`<docs_dir>/social-queue.md` (create from `assets/social-queue-template.md` on
first run); the user reviews, pastes, and marks items posted.

1. Read `social-queue.md` and `content-plan.md`. Pick shipped pages with no queue
   entry yet — or the page the user names. Newest first, max 3 pages per run.
2. For each page draft, in the founder/team's actual voice (first person,
   practitioner tone, one concrete stat or claim pulled from the page, minimal
   hashtags, ends with a question or the link — never reads like a press
   release):
   - A personal-profile post for whatever the primary channel is (ask if
     unclear — LinkedIn and X are common defaults).
   - A shorter, product-forward version for a company/brand page, if one exists.
   - If the piece is worth republishing elsewhere (e.g. Medium), a checklist
     entry noting the platform's canonical-URL mechanism must be used — never
     copy-paste in a way that loses canonical attribution.
   - Community threads (Reddit-style forums, Hacker News, niche Slack/Discord
     communities): only where the skill has search budget to find 1–3 live
     threads the page genuinely answers; draft a value-first reply that stands
     on its own without the link, flagged for the user to post manually, in
     their own voice. Never suggest posting the identical comment in 2 places.
3. Append drafts under a dated heading, one entry per page, with a status marker
   the user flips (`[ ] queued` → `[x] posted YYYY-MM-DD <URL>` or `[-]
   skipped`). Never overwrite prior entries.
4. Report what was drafted and what's still unposted from previous runs — an
   aging queue means distribution, not content, is the bottleneck.

---

## Automation (scheduled agents)

If the harness supports scheduled/cron-style agent runs, these are reasonable
cadences — set them up only if the user asks, never silently:

| Routine | Cadence | Action |
|---|---|---|
| Content | Weekly | Pick the next queue item, open a PR (never push straight to main) |
| Citation audit | Monthly | Update the citation log on a branch |
| Technical audit | Monthly | File findings as a report; PR fixes only for blockers |
| Competitor refresh | Quarterly | Refresh competitor-analysis.md |
| Social drafts | Weekly | Draft posts for newly-shipped pages |

Scheduled runs always work on a branch + PR — content is outward-facing and needs
human review before going live. If a run hits an unresolved blocker, report
rather than plow ahead. Never invent statistics, in scheduled or interactive runs.

## Standing cautions

- A subdomain is a separate site for authority purposes — don't split content
  onto a subdomain without a deliberate reason; it usually just dilutes signal.
- Programmatic/templated pages need real data depth per page — thin
  variable-injection pages risk scaled-content-abuse penalties for the whole
  domain.
- `llms.txt` and schema markup are hygiene, not strategy — don't over-invest
  expecting them alone to move AI-citation odds. The actual lever is answer-first
  content + real stats + third-party mentions (roundups, directories, forums,
  YouTube) + fast indexing (Bing/IndexNow).
- Anything gated behind a login the skill can't access (Search Console, Bing
  Webmaster Tools, review-site dashboards, social platforms) → give the user a
  precise action list; don't fake having checked it.

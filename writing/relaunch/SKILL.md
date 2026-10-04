---
name: relaunch
description: Execute a relaunch on a decayed-but-valuable article (Lesson 5 audit + Lesson 8 "don't abandon old winners"). Take a page the audit flagged as decaying or rank-slipping, refresh it against the LIVE SERP (freshen data, re-verify searcher intent, squeeze new keywords, refresh visuals), bump its published date, and re-promote it as if brand new. The "update ~half the calendar" half of the strategy. Triggered from the audit's Relaunch plan.
allowed-tools: Read, Write, Edit, Bash, Glob, Task
---

# Relaunch — update an old winner instead of starting cold

The course's most under-used lever: Ahrefs spends **~half its time updating and relaunching**
old content, not making new (`STRATEGY.md` §3). A page that already earned rank + links is the
single best ROI on the blog — it starts from authority, not from zero. **Anti-pattern #12 is
"abandon old content or settle for any position below #1."** This skill is how we refuse to
abandon it: take a decayed-but-valuable article, make it the best result for its query *again*,
and re-promote it as new.

A relaunch is **not** a tweak. It is the full update loop — re-research against today's SERP,
rewrite where the page lost ground, refresh the data and visuals, bump the date, and promote it
like a brand-new piece. Half-measures (change the year in the title, call it "updated") are
exactly the abandonment this lesson warns against.

## When this fires

The audit (`scripts/content_audit.py` → `content-pipeline/audit/latest.md`, the **"Relaunch
plan"** section) produces the work orders. A slug lands there when it is:

- `compound == "decaying"` (organic traffic is fading — Lesson 1, it stopped compounding), **OR**
- **rank-slipping** vs the prior snapshot (its `best_rank` worsened by ≥3 positions),

**and** it was ever valuable (had organic traffic, first-touch entries, or referring domains).
Each row carries `{slug, reason, best_rank, referring_domains, what_to_refresh}` — `what_to_refresh`
is your tailored checklist for *this* page. Start there; it already names the specific gaps.

> Pure-dead pages (no traffic, no entry, ever) are **not** relaunch candidates — they're DELETE
> or REVIVE in the audit. Don't relaunch a page that never won; relaunch one that's *slipping*.

## Input

For slug `{slug}`:
- `content-pipeline/audit/latest.md` — the **Relaunch plan** row for this slug (`reason` +
  `what_to_refresh` + `best_rank` + `referring_domains`). The brief.
- `content-pipeline/scorecard/latest.md` — the per-article line (trajectory, compound class,
  `rank_keyword`, paid). The evidence.
- `content-pipeline/8-publish/{slug}/article.md` — the **live published body** (the thing you're
  updating). If it's missing, pull the live page or the Strapi/`blog_posts` copy first.
- `content-pipeline/1-research/{slug}.md` (+ `{slug}-deep.md`, `{slug}-data.json`) — the original
  dossier/BEAT SPEC, if it exists, so you re-research *against* it rather than from scratch.
- `STRATEGY.md` — §3 (cadence/relaunch), §5 (uniqueness), §6 (spine: BV + intent + compound).
- `brand-config.md` — voice, audience, products, forbidden phrases.

## Process — the relaunch loop

> This is an **update of a live article**, so the spine never changes: it must still be
> intent-matched, BV ≥ 2, unique, and built to compound (`STRATEGY.md` §6). You're re-earning #1,
> not bolting "(2026)" onto a stale page.

1. **Read the brief.** Open the audit row + scorecard line. Note *why* it decayed/slipped and the
   `rank_keyword` it ranks (or used to rank) for. The `what_to_refresh` field is your punch list.

2. **Re-verify intent against the LIVE SERP (the non-negotiable first move).** Pull today's top
   10 for the `rank_keyword`. The SERP shifts — what ranked a year ago may now be a different
   *shape* (listicle → tool page, guide → comparison). **Match the current dominant intent
   exactly** (`STRATEGY.md` §6, anti-pattern #9). If the SERP shape moved, the relaunch is a
   re-architecture, not a copy-edit — route through `/research` → `/outline` for the new shape.

3. **Find what made us slip.** Read the new #1–3 side by side with our live body. We lost rank
   because a competitor *out-updated us*: fresher data, a section we lack, a sharper take, better
   coverage. List the specific gaps — these are what the rewrite must close.

4. **Freshen the substance (not the chrome).**
   - **Data & examples:** replace every stale stat/number/screenshot-able claim with current
     figures (re-cite). Dated examples → current ones. A "best apps 2024" page with 2024 prices
     is *why* it fell.
   - **Squeeze new keywords:** the page already ranks for a family — pull the new long-tail and
     "people also ask" the SERP now rewards and **widen the keyword family** the article covers
     (one strong page ranks for ~1,000 queries — `STRATEGY.md` §1; don't leave the new ones on
     the table). Add the subsections that capture them. Never keyword-stuff (anti-pattern #10).
   - **Information gain (still blocking):** the refresh must carry ≥1 thing the current top 10
     don't — our own data, first-hand testing, a sharper angle (`STRATEGY.md` §5). A relaunch that
     just re-clones the *new* page 1 is the same clone failure, one year later.
   - **Refresh visuals:** re-capture screenshots that show stale UI/old years; regenerate charts
     off the new data. Follow `templates/visual-strategy.md` (resolvable data, value-first ~80/20,
     annotate screenshots). A 2024 screenshot dates the page as hard as a 2024 stat.

5. **Rewrite where it lost ground — reuse where it didn't.** Apply the changes through the normal
   craft (`/draft` conventions: persona by content-type, voice from `examples/voice/`, the
   component menu with restraint). Keep the sections that still win; rewrite the weak ones; add the
   missing ones. The published byline persona stays the same unless the content type genuinely
   changed.

6. **Bump the published date (this is what makes it a *re*launch).** Set `published_at` /
   `publishedAt` to today on the refreshed package — the article re-enters the calendar as fresh.
   Keep the **slug and URL identical** (we're updating the same page to keep its rank + links —
   never spin up a new URL and orphan the old authority; that throws away the whole point).

7. **Re-run the gate.** A relaunch ships through the same publish gate as a new article —
   `/quality-check` must PASS (floors + the 3-reviewer "do they keep ours over the live #1?" panel).
   A refresh that can't beat the *current* #1 isn't done. On FAIL, route the punch list and iterate;
   never lower the bar to ship the update.

8. **Re-publish.** Run `/format-for-publish` on the refreshed package (same slug, new date). Then
   mirror-verify it's live (the formatter's Supabase `blog_posts` assertion).

9. **Re-promote as if brand new (the 110/110 half).** The update is only half the relaunch — Lesson
   8's whole point is you **promote it again**. Surface it for the off-page loop exactly like a new
   piece: refresh internal links pointing at it from the cluster, re-share it, and treat it as a
   fresh promotion target. **Promotion = building backlinks, not chasing a traffic spike**
   (`STRATEGY.md`, anti-patterns #13–14); don't stop promoting until it's back to #1.

## DO / DON'T

**DO**
- Relaunch pages that **were valuable and are slipping** — start from earned rank + links.
- **Re-verify searcher intent against the live SERP first** — the SERP shape moves; match today's.
- **Genuinely freshen the substance** — current data, new keywords, refreshed visuals, ≥1 new
  information-gain element.
- **Keep the same slug/URL** and **bump the published date** — update the page, re-date the launch.
- **Re-promote it as new** — relaunch = refresh **+** re-promotion (the second half is the point).
- Send it back through `/quality-check` — it must beat the *current* #1, not the old one.

**DON'T**
- Don't **abandon old content** or settle for any rank below #1 (anti-pattern #12 — the reason this
  skill exists).
- Don't fake a relaunch: changing the year in the title or stamping "updated" without refreshing
  the substance is the abandonment, dressed up.
- Don't **mint a new URL** for the refreshed page — that orphans the rank + backlinks you're
  relaunching *for*.
- Don't **re-clone the new page 1** — a relaunch still owes ≥1 information-gain element
  (`STRATEGY.md` §5).
- Don't **keyword-stuff** the new terms or over-engineer on-page SEO (anti-pattern #10) — widen the
  family by genuinely covering the subtopics.
- Don't ship a refresh that fails the gate, and don't chase a one-off traffic spike instead of
  backlinks (anti-patterns #13–14).

## Winning =

The relaunched page **reaches page 1 again and stays** (Lesson 8) — its organic traffic resumes
**compounding** (`compound` flips back toward compounding in a later scorecard), its `best_rank`
recovers toward #1, and it converts (BV ≥ 2). The opposite — and what we refuse to call a relaunch
— is a stale page left to drift to page 2, or a cosmetic "(2026)" refresh that doesn't move the
rank. A real relaunch turns a decaying asset back into a compounding one.

## Autonomous behavior

- The audit's **Relaunch plan** is the queue; in autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`) work
  the rows top-down (worst rank-slips first — the audit already orders them).
- A relaunch is **AUTONOMOUS-SAFE** — it's an *update* of an existing page, not a destructive or
  outward-facing action (unlike DELETE / merge-301 / ghost-redirect, which stay board-gated). EO
  can execute it via the update path without an approval gate.
- Same publish discipline as new content: `/quality-check` PASS required, the orchestrator owns the
  revision budget, and a FAIL is quarantined to `9-needs-review/` — **never** publish a FAIL or
  lower the bar to ship a refresh.
- One relaunch at a time per slug; keep the slug/URL stable and only the date + body change.

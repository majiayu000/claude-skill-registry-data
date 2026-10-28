---
name: vacpac-content-refresh
description: Keep VacationDeals.to's existing blog_posts fresh — weekly, in place. Selects a prioritized batch of stale posts, has ≤5 agents refresh them (dates/seasons, re-verify $ prices against live deals, expand thin bodies, refresh interlinks, fix SERP-drifted titles/metas) while preserving the anti-AI blog style, re-validates, UPDATEs rows (never inserts), guarded-rebuilds, and verifies. Use when the user says "refresh content", "run the content refresh", "freshen the blog", or "/vacpac-content-refresh". Sibling of vacdeals-evergreen (which GROWS the blog); this one keeps it fresh.
---

# VacationDeals.to — Content Refresh Runbook (weekly)

Keeps the existing ~1,235 `blog_posts` fresh by **UPDATING rows in place** — never inserting, never deleting, never changing slugs. Sibling of `vacdeals-evergreen` (which adds +50 new posts); run this on the **off-weeks** from evergreen (same-week doubles token load). Full design rationale: `docs/seo-audit-2026-09-24/07-vacpac-content-refresh-skill.md`.

## FIRST-RUN SETUP (once — idempotent, safe to re-run)
The `last_refreshed_at` column drives selection + cooldown. Apply the additive migration on the VPS before the first real run (no-op if already applied):
```
ssh root@72.60.126.82 'cd /var/www/vacationdeals && set -a && source .env && set +a && psql "$DATABASE_URL" -f scripts/sql/2026-10-15-blog-last-refreshed.sql'
```
`schema.ts` already declares the column (`blogPosts.lastRefreshedAt`). The companion `scripts/update-blog-batch-json.ts` sets it on every refresh.

## GUARDRAILS (inherited from vacdeals-evergreen — non-negotiable)
- **Agent waves ≤5.** One wave of ≤5 agents per run; agents **write once and stop** (no self-expansion loops — they tripped the session limit before).
- **Guarded deploys:** `pnpm build` BEFORE `pm2 restart`; if build fails, do NOT restart (site stays up on the old build).
- **$25 all-in cap** per run (agent tokens + any price-check fetches). Don't exceed without asking.
- **Re-validate agent output programmatically** (word floor, FAQ count, clean title/meta) — never trust "I validated it." The `update-blog-batch-json.ts --dry-run` is that gate.
- **Sitemap-cache trap:** never `rm` `.next/server/app/sitemap.xml*` (500s the route). `sitemap.ts` has `revalidate=3600`; a normal guarded rebuild regenerates it.
- **Known-walled price sources** (`vegas-timeshare`, `holiday-inn`, `hyatt`, `branson-travel-group`): FETCH_BLOCKED on curl/WebFetch is a *verification gap*, not a data error — use `stealth-browser-mcp` or fall back to `deals.scraped_at` freshness; never "correct" a price down to nothing on a block.

## THE "NEVER DEGRADE" RULE (this skill's prime directive)
- **Never shorten a post below the word bar** (≥750 words prose; ≥900 incl. FAQs). Shorter output = validation failure, full stop. The script REJECTS a length regression on a non-thin post.
- **Never break the anti-AI blog style.** Humanization (deliberate typos, grammar slips, casual first-person) stays in the **BODY ONLY**; title/meta/FAQ stay clean. Do NOT "correct" the intentional body slips.
- **Never republish without diffing** — review the `--dry-run` field-level diff before the real UPDATE.
- **Never change a slug** (URL stability + internal links + no 404s). The script rejects a slug it can't find.
- **Never delete/expire content** (blog posts are refreshed, not retired).
- **Never restructure a pillar hub** (`/timeshare-presentation-deals`, `/all-inclusive-vacation-deals`, the 8 topic hubs) — freshen copy only; they are link targets per CLAUDE.md.
- **Backup before the batch UPDATE** (Phase 0) — UPDATE has no skip-existing safety net.

---

## PHASE 0 — Safety backup
UPDATE-in-place has no undo. Take a fresh dump first (crown-jewel = `deal_price_history`, but this also captures `blog_posts`):
```
ssh root@72.60.126.82 "/usr/local/bin/vacdeals-db-backup.sh >> /var/log/vacdeals-dbbackup.log 2>&1 && ls -t /root/db-backups/*.pgdump | head -1"
```
(If a current dump from a same-day evergreen run exists, that suffices.)

## PHASE 1 — Select the weekly batch (default 20 = 5 agents × 4)
Run the priority query, dump to a scratch PSV so the run log shows WHY each post was picked. Exclude anything refreshed in the last 60 days (cooldown). Base query:
```sql
SELECT slug, category, created_at::date AS created, last_refreshed_at::date AS last_refreshed,
       length(content) AS content_length,
       round(
         EXTRACT(epoch FROM now() - GREATEST(created_at, COALESCE(last_refreshed_at, created_at)))/86400  -- age (days)
         + CASE WHEN length(content) BETWEEN 3500 AND 4999 THEN 120 ELSE 0 END                            -- thin boost
         + CASE WHEN category IN ('brands','destinations') THEN 60 ELSE 0 END                             -- price-drift risk
         + CASE WHEN title ~* '20(25|26)|summer|winter|spring|fall|thanksgiving|christmas|new year|labor day|memorial|easter|valentine' THEN 90 ELSE 0 END  -- season/year rot
         + CASE WHEN slug ~* 'cheapest|^best-|-best-|-vs-|deals-under-|presentation-deal' THEN 40 ELSE 0 END  -- commercial ROI
       ) AS priority
FROM blog_posts
WHERE is_published = true
  AND (last_refreshed_at IS NULL OR last_refreshed_at < now() - interval '60 days')
ORDER BY priority DESC
LIMIT 30;
```
From the 30, pick **~20**, capping any single category at ~60% of the batch (soft round-robin) so one category isn't starved. **Skip pillar-hub + topic-hub slugs** (freshen-copy-only; don't batch-restructure them). Dump the chosen set to `slug|category|created|last_refreshed|content_length|priority` PSV.

For each chosen slug, export the **current row** (title, meta, category, `content`, `faqs`, `internalLinks`, `content_length`, `created_at`, `last_refreshed_at`) to a per-slug JSON in a scratch dir — this is the agents' input AND the diff baseline.

Also dump **live deal context** for price re-verification — active deals with brand, destination, price, url — so agents can confirm quoted `$` figures against real current deals.

## PHASE 2 — Dispatch ≤5 refresh agents (one wave)
Split the ~20 into ≤5 chunks (~4 each), one agent per chunk. Each agent **refreshes its posts, writes updated JSON once, and stops.** Per post:
- **Freshen dates/seasons** — advance year tokens, rotate season/holiday framing to the current/upcoming window, update "as of <month>" lines.
- **Re-verify every `$` price** against the provided live `deals` data (WebFetch / stealth-browser the partner lander when a figure is load-bearing and not in `deals`). Correct stale/repurposed prices. Apply the CLAUDE.md cautions: a "$X gift card / resort credit / deposit" figure is NOT the package price; drop placeholder `original_price` (≥20000 or < price).
- **Expand thin bodies past the bar** — ONLY posts flagged thin; add substantive prose + a data table to clear 750+ words (≥900 incl. FAQs). Never pad a healthy long post.
- **Refresh interlinks** — fix stale/404 authored `internalLinks`; keep them minimal (the render-time resolver in `lib/internal-links.ts` adds geo/keyword-pillar + sibling links — do NOT hardcode a big related block).
- **Fix SERP-drifted title/meta** — rewrite where intent or a quoted number drifted; keep the "vacation deals" primary-keyword posture. **Title + meta + FAQ text must be clean (no deliberate typos)** — humanization is BODY-only.
- **Preserve style/structure** — BLUF box, ≥6 FAQs (aim 8–10), first-person voice, real vacpack data.

Agents return per-slug JSON matching the `update-blog-batch-json.ts` schema (same shape as blog batches) + a short change note (what changed + old→new price diffs).

## PHASE 3 — Re-validate programmatically (trust nothing)
Run the validator built into the companion in `--dry-run` (Phase 4) AND an independent cross-file check: rendered prose ≥750 words / ≥900 incl. FAQs, ≥6 FAQs each (unique, no cross-page dupes), **title/meta/FAQ clean of the deliberate body typos** (check those fields only — do NOT flag body slips), slug unchanged, no length regression below bar, any changed `$` references a real current deal. Bounce failures back to the agent; never accept a shortened post.

## PHASE 4 — UPDATE rows in place (dry-run first)
Commit the refreshed JSON to `research/content-refresh/<YYYY-MM-DD>/` (git = source of record) and push. Then on the VPS, run the **update** companion (NOT the insert script — it skips existing slugs):
```
cd /var/www/vacationdeals && git pull -q origin main
cd /var/www/vacationdeals/apps/scraper && set -a && source /var/www/vacationdeals/.env && set +a
./node_modules/.bin/tsx /var/www/vacationdeals/scripts/update-blog-batch-json.ts /var/www/vacationdeals/research/content-refresh/<YYYY-MM-DD> --dry-run
# review the field-level diff (title/meta/price/word-count deltas), then re-run WITHOUT --dry-run
```
The script UPDATEs by slug, sets `updated_at` + `last_refreshed_at = now()`, refuses to create a missing slug, and rejects a below-bar length regression.

## PHASE 5 — Guarded rebuild
```
cd /var/www/vacationdeals && git pull -q origin main && set -a && source .env && set +a && pnpm build && pm2 restart vacationdeals-web --update-env && pm2 save
```
Build fails → do NOT restart. Don't touch the compiled sitemap route; ISR regenerates it with fresh `lastmod`.

## PHASE 6 — Verify sample renders
Curl 3–5 refreshed slugs at top-level (`https://vacationdeals.to/<slug>`): expect `200`, `FAQPage` JSON-LD present, the corrected price/date visible, "Explore More" internal-links block intact. `/blog/<slug>` 308s to top-level. Within the hour, spot-check that `/sitemap.xml` `<lastmod>` advanced for a refreshed slug (only if `sitemap.ts` derives lastmod from `updated_at`/`last_refreshed_at` — see open item below).

## FINISH / report
- Commit refreshed JSON (`research/content-refresh/<date>/`); push.
- Update `docs/NEXT-ENHANCEMENTS.md` (dated entry) + relevant memory.
- Consolidated summary: batch (N by category + selection reason) · prices re-verified + corrections (old→new) · thin posts expanded (before→after words) · titles/metas rewritten · rows UPDATEd + `last_refreshed_at` set · build/verify status + sitemap lastmod · cost vs $25 cap · **coverage** (running total refreshed / 1,235 + weeks to clear the 644-post stale cohort at this cadence).

## OPEN ITEMS (owner decisions — see spec §7)
- **Sitemap `lastmod`:** wire `sitemap.ts` `<lastmod>` to `GREATEST(updated_at, last_refreshed_at)` so refreshes are advertised to crawlers (recommended; small change — otherwise Phase 6's lastmod check is moot).
- **Title rewrites:** default is agents may rewrite titles; if you'd rather approve title changes (they affect established rankings), have agents *propose* titles and apply only body/price/date.
- **Cadence:** weekly manual `/vacpac-content-refresh`, alternating weeks with evergreen. 20/week clears the 644 stale cohort in ~8 months.

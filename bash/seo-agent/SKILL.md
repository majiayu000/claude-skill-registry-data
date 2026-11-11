---
name: seo-agent
description: "Daily SEO audit-and-fix loop for a website you own, driven by one config file per site. Crawls the live site with free stdlib Python scripts (technical crawl, indexability, internal-link graph with day-over-day regression diff, JSON-LD validity, AI-crawler access, Core Web Vitals via Lighthouse/PageSpeed), pulls real queries from Google Search Console with your own credentials, ranks issues by impact vs effort, ships safe fixes as pull requests (and optional CMS patches) behind a human review gate, and writes a dated report. Use when asked to run an SEO audit, a technical SEO audit, find SEO quick wins, check indexing or AI crawlability, or run the daily SEO check: /seo-agent <slug> or /seo-agent <slug> technical. Requires Claude Code (runs scripts, git, gh); never merges, never direct-pushes."
---

# SEO Agent

One engine, one config per site. Every run: measure, diff against yesterday, fix the
few things that matter through PRs, and write down what moved.

## Requirements

- Claude Code with Bash. Python 3 (scripts are stdlib only, except `gsc.py`: `pip install google-auth`).
- Optional: Chrome/Chromium (for `render_check.py`), `npm i -g lighthouse` (for `cwv.py`), `gh` CLI (PRs and preview-host discovery).
- A site config at `sites/<slug>.md`. Copy `sites/example.md` and fill the placeholders.
- GSC is optional but turns guesses into measurements. Auth is yours: `$GSC_SERVICE_ACCOUNT_JSON` (service account added as a Restricted user on your property) or `gcloud auth application-default login` with the `webmasters.readonly` scope.

All commands below run from this skill folder (`S=scripts`). Output goes to
`~/.claude/seo-reports/` (reports) and `~/.claude/seo-state/` (snapshots).

## Modes

| mode | trigger | does |
|---|---|---|
| daily (default) | `/seo-agent <slug>` | steps 1-6, lean and diff-driven |
| technical | `/seo-agent <slug> technical`, "deep audit", weekly, or after any routing/middleware/sitemap/layout change | full checklist in `references/technical-seo.md` |
| audit-only | the user says read-only | steps 1-4 and 6; every fix becomes a proposal with an owner; no branches, PRs or CMS writes |

## Steps

### 1. Load the config
Read `sites/<slug>.md` first. If it does not exist, stop and offer to create it from
`sites/example.md` (ask for domain, repo, build command, GSC property). Never redo
anything under `known_wins`.

### 2. Measure (free, no paid APIs)
Run in this order; each writes machine-readable output the report uses.

```bash
python3 $S/linkgraph.py <domain>                  # link graph + orphans, snapshot, diff vs last run
python3 $S/crawl.py --sitemap <domain> --sample 30   # per-page title/meta/canonical/H1/words/schema
python3 $S/validate_schema.py <money page URLs>   # JSON-LD parses, @types, canonical mismatch
python3 $S/psi.py <5-10 top pages>                # mobile LCP/CLS/INP + lab TBT (PSI_KEY optional)
bash -c "python3 $S/techaudit.py <domain> --out <dir> --max 3000 --thin 250 --depth-limit 4 \
  --preview-from-gh <owner/repo> $PROBES"         # when linkgraph shows new 4xx/orphans/lost schema
```

Use `bash -c` for anything with `$PROBES` (`--probe /api/ --probe /admin ...`): zsh does not word-split it and the probes silently vanish.

**GSC** (if configured): preflight under a 60 s cap, then snapshot every run.
```bash
perl -e 'alarm 60; exec @ARGV' python3 $S/gsc.py <property> preflight
python3 $S/gsc.py <property> snapshot                     # 28d pages+queries, movers vs last snapshot
python3 $S/gsc.py <property> searchanalytics --days 28 --dim query --top 200
```

Check `robots.txt` by hand if techaudit did not run: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot must not be blocked unless that is a deliberate policy.

### 3. Research
- With GSC: queries at average position 11-30 with real impressions are the cheapest page-1 pushes. Start there.
- Without GSC: WebSearch the config's `priorities` terms, note who ranks and which SERPs are weak.
- Prefer long-tail problem language (what buyers type before they know the category) over head terms in `avoid`.

### 4. Prioritise
Build one table: `issue | impact H/M/L | effort S/M/L | evidence (URL + observed value) | action`.

Rank in this order:
1. Linkgraph regressions (inlink drops, lost schema, new orphans, title drift). Highest confidence, usually small.
2. Anything blocking indexing: noindex/canonical conflicts, 4xx/5xx in sitemap, robots blocks, preview hosts indexable.
3. GSC page-1 pushes: position 10-20 with impressions in the top quartile for the site.
4. Thin money pages (<600 words), missing/invalid schema, title 25-65 chars and description 70-165 chars violations.
5. CWV failures at p75: LCP >2.5 s, CLS >0.1, INP >200 ms (field data only; lab is diagnosis).

Defer low-impact/high-effort work and anything needing a business call; list it under "needs a human".

### 5. Ship fixes (review gate)
**Code** (only if `repo_path` is set):
- Branch `fix/seo-<topic>` off `default_branch`. One concern per PR.
- Run the config's `build`; never push a failing build.
- `gh pr create` with: what changed, the evidence row it fixes, build result, what to watch in GSC.
- Never push to the default branch, never merge, never touch design/CSS/components unless asked.

**CMS** (dispatch on `cms.driver`; token from the env var named in `token_env`):
- Patch scalar fields only: title, meta description, excerpt. Do not rewrite rich-text bodies unless asked.
- Hard gate before every patch: `python3 $S/lint_brand.py "<new text>" <each brand_voice.forbidden item>`. Exit 1 means rewrite and lint again.
- `driver: none` or token missing: write the change as a proposal in the report instead.

**Optional**: after shipping changed URLs, `python3 $S/indexnow.py <domain> <key> <urls>` (Bing and others; key file must be served at `/<key>.txt`).

### 6. Report
Write `~/.claude/seo-reports/<slug>-<YYYY-MM-DD>.md` (format below). Every 7th run
also write `<slug>-week-<YYYY-Www>.md`: what shipped vs what moved in GSC.

**Lean rule:** if the linkgraph diff is empty, GSC shows no material movement and no
priority changed, write a 3-line "no material changes" report and stop. Do not
manufacture work.

## Decision rules

- Numbers in reports: same source, same window length, before/after pairs via `--start/--end` around the change date. Never compare a UI export to an API pull or a 7-day window to a 28-day one.
- Lab vs field CWV never share one claim.
- FAQ rich results only show for authoritative government/health sites; FAQ markup elsewhere is fine for parsers but promises no SERP feature.
- Keyword overlap is not cannibalisation until GSC query-by-page shows two URLs swapping for the same query.
- A preview host (`*.vercel.app`, `*.netlify.app`) is yours only after you check its title; look-alike names belong to strangers.

## Failure handling

| problem | do this |
|---|---|
| GSC preflight fails or hangs | record the exact error, use the newest `~/.claude/seo-state/<host>/gsc-*.json` labelled "last-known, window X", continue; mark GSC rows "not measured today" |
| no GSC configured | WebSearch `site:` checks; label every number "inferred, not measured" |
| linkgraph refuses to save (>5% of URLs failed) | network blip: rerun once; if it repeats, report the failing URLs; use `--force` only if the failures are real 4xx |
| sitemap missing/invalid | that is the top critical finding; crawl from `/` via `techaudit.py` instead |
| Lighthouse/Chrome missing | use `psi.py` (Google-hosted) and say lab data came from PSI |
| `cwv.py` slow (~90 s/URL) | run it with `nohup ... &` and poll its log; long silent foreground commands can time out |
| build fails on a fix branch | fix it or drop the PR; never push red |

## Report format

```markdown
# SEO daily: example.com, 2026-03-04
Crawl: 412 URLs, 398 indexable, 0 5xx. Linkgraph: 2 regressions (below).

| issue | impact | effort | evidence | action |
|---|---|---|---|---|
| /pricing lost 6 inlinks | H | S | footer nav change, 9 -> 3 inlinks | PR #41 restores footer link |
| /blog/x missing Article schema | M | S | validate_schema: 0 JSON-LD | PR #42 |

Shipped: PR #41, PR #42 (build green). CMS: 1 title patch, lint_brand PASS.
GSC 28d vs last: /guide/y pos 14.2 -> 11.8, impressions 1,920 -> 2,410 (same window length).
Needs a human: merge PRs; decide whether /old-landing should 301 to /pricing.
Carry forward: page-1 push for "<query>"; thin /features page (310 words).
```

Deep technical audits use the severity/evidence/fix/effort/owner contract and report
skeleton in `references/technical-seo.md`.

## Running it daily

In-session: `/loop 24h /seo-agent <slug>` (only fires while Claude Code is open).
Unattended: `scripts/daily.sh <slug>` from cron on a server; see `references/deploy.md`.

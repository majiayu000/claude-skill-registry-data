---
name: seo
description: Run SEO for a website from real data, end to end. Connects to Google Search Console, the URL Inspection API, GA4, PageSpeed/CrUX and optionally DataForSEO, Bing and IndexNow, then audits, finds quick wins, diagnoses traffic drops, plans keywords and pages, briefs and gates page changes, fixes internal links, drives indexing, tracks AI-search (GEO) visibility and writes the weekly SEO review. Use it whenever the user talks about SEO, Google rankings, Search Console, impressions or clicks, indexing, a traffic drop, keywords, a page to rank, titles and meta descriptions, internal links, backlinks, Core Web Vitals, ChatGPT or AI Overviews citing a site, or a weekly or monthly SEO report, even if they don't say "SEO", e.g. "why is traffic down", "get this page on Google", "what should we write next".
---

# SEO operator

You are the hands of an SEO team: you read the data, plan, write, edit, check and log. The data sources are the brain: you never know search volumes, rankings or what Google shows today unless a tool just told you. The owner approves anything that touches a live page or leaves under their name.

The single most common way to fail at this job is to state a number or a ranking that came from memory. Every figure you give carries its source and its date window, or it is labelled an estimate. If a source is missing, say what is missing and what it would take, and carry on with what you can measure.

Reply in the user's language. Scripts and reports are in English and that's fine.

## Start of every session

1. Find `.seo/config.json` from the working directory upwards. If there is none, run the setup first: `node <skill>/scripts/setup.mjs --site <url>` in the project root (the `/seo-god-mode:setup` command walks the user through it), then fill brand, money keywords and competitors with the user (see `references/setup.md`).
2. Run `node <skill>/scripts/doctor.mjs`. It tells you which sources are live. Mention gaps once, briefly, then work with what is connected.
3. Read `.seo/standards.md` (the site's rules, grown from the owner's past rejections) and the last entries of `.seo/log.md` (what changed recently and when). A page changed in the last 60 days is still settling: don't judge it, don't change it again without a strong reason.

`<skill>` is this skill's directory. All scripts are Node 18+, zero dependencies, run from anywhere inside the project and answer `--help`. The analysis scripts print markdown and accept `--json` and `--out <file>`; those reading Search Console also take `--host <hostname|all>` (another host on the same domain property) and `--days/--start/--end`.

## Commands

The user may type `/seo-god-mode:seo <command>` or just ask. Map the request to one or more of these.

| Command | What it answers | Run |
|---|---|---|
| `setup` | First connection: key, Search Console and GA4 properties, sitemap, brand, market | `scripts/setup.mjs --site <url>` (or the `/seo-god-mode:setup` command) |
| `doctor` | What is connected | `scripts/doctor.mjs` |
| `weekly` | The Monday review: what moved, why, 3 actions | `scripts/weekly.mjs`, then write the reading (see below) |
| `drop` | "Traffic is down, why?" demand vs rank vs CTR, per segment | `scripts/drop.mjs [--vs weeks:4\|year]` |
| `quick-wins` | Queries at positions 4-20 worth a push, top-3 pages with a CTR problem, cannibalisation | `scripts/quick-wins.mjs` |
| `repoint` | Pages Google ranks for a different query than the one they target | `scripts/repoint.mjs` |
| `prune` | Content inventory: keep / improve / merge candidates (never deletes) | `scripts/prune.mjs` |
| `audit` | Technical issues ranked by severity, robots/AI-crawler policy, hreflang | `scripts/audit.mjs` |
| `index` | What is indexed, what isn't and why, the request order for today | `scripts/index-status.mjs` |
| `links` | Orphans, pages under 5 contextual in-links, which pages to link from and with which anchor | `scripts/internal-links.mjs` |
| `cwv` | Core Web Vitals field (CrUX) and lab; `--history`: weekly p75 over up to 40 weeks, the week a metric crossed its threshold | `scripts/cwv.mjs [url...] [--history]` |
| `gate` | Did this change silently remove something? Run before any publish; `--published <url>` after it (live, indexable, in the sitemap) | `scripts/ship-gate.mjs` |
| `twins` | Pattern pages that are a find-and-replace of each other (doorway risk) | `scripts/twins.mjs [--pattern "^/city/"]` |
| `serp-mix` | Which queries leave room beyond your site (videos, Reddit, platforms, lists), which subreddits rank, which lists miss you (DataForSEO) | `scripts/serp-mix.mjs` |
| `rankmap` | Local: top-3% from a rank-map export, weakest direction, cheap wins, gap to the leader | `scripts/rankmap.mjs yours.csv --vs leader.csv` |
| `keywords` | Volumes, ideas, live SERP, competitor keywords, gaps, backlinks (DataForSEO) | `scripts/keywords.mjs volume\|ideas\|serp\|ranked\|gap\|backlinks` |
| `suggest` | Free pattern discovery from Google Autocomplete (no volumes) | `scripts/suggest.mjs "<seed>"` |
| `gsc` | Any ad-hoc Search Console cut, with period comparison | `scripts/gsc.mjs --dims query,page [--compare] [--filter "query~regex"]` |
| `bing` | Bing queries / pages | `scripts/bing.mjs queries\|pages` |
| `gbp` | Google Business Profile: Search vs Maps impressions, calls, website clicks, directions; searches that showed the profile; reviews and unanswered ones (needs Google's API approval, `gbp-auth.mjs` once) | `scripts/gbp.mjs locations\|performance\|keywords\|reviews` |
| `indexnow` | Ping Bing & co. after publishing | `scripts/indexnow.mjs <url...>` |
| `crawlers` | Which search and AI crawlers actually fetch the site, what, and with which status; sitemap pages Googlebot skipped | `scripts/crawlers.mjs [--sitemap]` (Cloudflare) or `--file <logs>` |
| `pattern` | Money keywords and repeatable page patterns | procedure in `references/commands.md#pattern` |
| `brief` | One page, one keyword: what to build and what makes it better than the top 3 | `references/commands.md#brief` |
| `ship` | Publish a page or a change safely | `references/commands.md#ship` |
| `geo` | AI-search visibility: fan-out queries, prospects, manual citation log | `scripts/geo.mjs queries\|prospects\|log\|report` |
| `outreach` | Link and mention prospects (lists only, never sends) | `references/commands.md#outreach` |
| `local` | Google Business Profile and local pages (uses `gbp` data when connected) | `references/commands.md#local` |

For anything that is not a command (a question, an idea, "is X worth it"), answer from the data you can pull and from `references/playbook.md`.

**"Where are we / what should I do this week?"** (not the Monday ritual): `doctor` → `index` → `audit` → `quick-wins` → `links` → `cwv`, then answer with a short verdict, a table of findings with sources, and at most 3 prioritised actions. Run `weekly` only when the user asks for the review/report, or on the ritual day.

**Young sites (under ~4 weeks of data):** the default windows end 3 days ago and may return nothing. Re-run with `--end <today>` (partial data is fine to see what is appearing) and judge on indexing and impressions, not clicks.

**Domain properties hold several hosts.** `doctor` lists them. When a new site lives next to an established host on the same domain (a portal, an app, a blog), look at that host too (`--host <name>`): its brand demand, the queries it already ranks for, and above all its links to the new site are often the biggest lever, and the new site must not compete with it on its own brand queries.

## Rituals and scheduling

SEO is a loop, not a project: the Monday review (`weekly`) and, on the first Monday of the month, the GEO check (`references/commands.md#geo-monthly`), index coverage and CWV. When the owner sets the skill up, offer to schedule both with `/seo-god-mode:schedule` (it creates the scheduler entry only after the owner says yes). Scheduled runs need the same credentials as interactive ones, so they run on the machine that holds the service account key.

## Rules of engagement

These come from real failures. Read them as defaults the owner can loosen in `.seo/standards.md`, not as rituals.

**Allowed without asking**: read every data source, run every script, write drafts, write to `.seo/` (log, reports, cache), open branches and PRs.

**Needs the owner's explicit yes, every time**: publishing a page or changing a live one; changing a title or H1 on a page that gets clicks; redirects; anything in robots.txt, canonical tags, hreflang or noindex; marking a translation or an AI-written page as reviewed; requesting a domain-wide change (template, navigation).

**Never, even if asked in passing**: delete a page (propose merge + 301 instead, and let the owner decide); buy links or anything else; send email or messages outside the company; submit forms or create accounts on third-party sites (directories, review sites): prepare the text, the owner submits; enter credentials. If the user insists, explain and hand them the prepared material.

When the owner rejects a proposal, ask or infer the reason and add it to `.seo/standards.md` as a one or two-line rule with the date. That file becomes the site's editorial line.

## Judgment that the scripts can't do for you

- **Seasonality before panic.** A drop with stable positions and stable CTR is people searching less. Check the calendar of the top country (school holidays, Ramadan, exams, public holidays) and compare like-for-like weekdays (`drop.mjs --vs weeks:4` or `--vs year`) before touching anything. Audiences of students follow school terms almost exactly.
- **Average position lies when the mix changes.** New pages, a new country or a new query family entering at deep positions pull the average down while every existing ranking holds. Trust per-segment tables and the like-for-like position line in `drop.mjs`, not the headline average.
- **Search Console lags.** Final data is ~3 days behind; the scripts default to windows ending 3 days ago. Today's partial data is fine for "did it start appearing", not for comparisons. Query-level rows omit anonymized queries, so they never add up to the totals.
- **New domains wait.** Expect 3 to 6 months before generic pages rank; judge a new site on indexing, impressions and positions trending, not clicks. Brand queries come first.
- **Give changes time.** A dip after a change is normal; wait 4 to 8 weeks before judging and never revert in a panic. Log every shipped change with a review date.
- **Top 3 with a weak CTR is two different problems.** A weak snippet (fix the title) or an AI Overview or SERP feature answering above you (a title won't help). Look at the live SERP (`keywords.mjs serp` or a logged-out browser) before rewriting.
- **One keyword, one page.** Before creating a page, check Search Console for an existing page that already gets impressions for the query: improve that one. Two pages at 7 and 8 are worse than one at 3.
- **Volume is not a violation, unoriginal content is.** Every new page carries one thing the current top results lack: a working tool, your own numbers, a real table, original media, a quiz that routes the reader. No such element, no page. Pattern pages where only the city or the product name changes are doorways.
- **Cadence beats bursts.** A steady 1 to 4 pages a week reads as an editorial team; 30 pages on a Monday then silence reads as a content bomb. On a new site, one page a day is the ceiling.
- **Indexing quotas are small.** The UI "Request indexing" allows about 10 URLs a day per property; the URL Inspection API allows 2,000 reads a day. Request the pages that matter most first (`index-status.mjs` orders them), stop at "Quota exceeded", continue the next day. Requesting does not guarantee indexing; internal links and the sitemap do most of the work.
- **Quality gates in the codebase win.** If the site has its own publishing checks (reviewed flags, minimum data points, noindex rules), work with them and surface the decision to the owner rather than flipping a flag to get a page indexed.

## Writing the weekly review

Run `weekly.mjs` (it saves `.seo/reports/<week>.md`), then fill its two empty sections:

- **Reading**: 3 to 6 short paragraphs. What moved and the evidence (segment, query, page). Separate demand, ranking and CTR effects. Name seasonality or known changes from `.seo/log.md` when they explain a move. Say what you don't know.
- **Actions (max 3)**: each one concrete (page, change, expected effect, how you'll know), ranked by expected impact × confidence ÷ effort. Prefer finishing work over starting new work.

Post it where the project tracks work (config `tracker`, e.g. a Linear issue or document) and give the owner a short summary in chat with the link.

## Output conventions

- Lead with the answer or the verdict, then the evidence. Numbers with their window (`2026-09-13 → 2026-10-10`, 28 days) and source.
- Tables for comparisons; prose for reasoning. No vanity metrics: what matters is clicks and conversions on queries that bring business, not total impressions.
- An action list is ranked and short. "Do these 3 this week" beats a 40-item audit.
- When you change something, append a line to `.seo/log.md`: date, page, change, the data behind it, review date.

## References (read when the task needs them)

- `references/commands.md`: step-by-step procedures for `pattern`, `brief`, `ship`, `outreach`, `local`, `geo` monthly check, `prune` decisions, multilingual.
- `references/playbook.md`: the strategy and the order of work: money keywords, page types for software, picking winnable SERPs, building better pages, fixing what exists, authority and links, GEO, cadence.
- `references/policies.md`: what Google's spam policies and AI-content guidance actually say (scaled content abuse, doorways, link spam, site reputation abuse, expired domains), with links. Read before any programmatic or AI-assisted publishing plan or any link-building plan.
- `references/geo.md`: what is known (and disputed) about how ChatGPT, Perplexity, Gemini and AI Overviews pick sources, with dated figures.
- `references/setup.md`: connecting each data source, the config file fields, optional MCP servers.

---
name: search-console-insights
description: >
  Pull and act on Google Search Console DATA for a verified site. Free GSC Search
  Analytics API (OAuth, read-only): where target keywords rank, striking-distance
  queries (pos ~8-20), and high-impression/low-CTR pages flagged for snippet/SERP
  investigation (title/meta rewrite only if the live-SERP check shows a snippet
  problem you control). Optional add-ons: the live competitor Top-10 via a SERP
  API, Bing Webmaster Tools as a Copilot/ChatGPT proxy, and a weekly check of
  whether AI engines name the business (GEO). First use runs a guided onboarding
  for non-technical owners. Trigger phrases: "GSC insights", "Search Console
  data", "connect GSC", "where do I rank", "top queries", "striking distance
  keywords", "quick SEO wins", "why is my CTR low", "which pages to optimize",
  "competitor Top 10", "how do I rank on Bing", "Copilot
  visibility", "ChatGPT search visibility", "track my rankings over time", "weekly
  SEO report", "does AI name my business", "weekly AI check", "show me my AI
  report".
metadata:
  version: 1.9.0
---

# Search Console insights

`search-console-setup` is "set it up once" (verify the property, submit the sitemap,
turn on IndexNow). **This skill is "monitor + act, repeatedly"** — it reads the data
GSC has collected and turns it into the 2–3 highest-leverage moves.

## Capabilities at a glance

| Source | Script | Auth | What you get |
|---|---|---|---|
| **Combined (the default)** | `insights.py` | — | **Google + Bing side by side** per keyword + a nudge to connect any missing free source |
| **Google Search Console** | `gsc_query.py` | OAuth (one-time browser consent) | Real queries + exact avg position, impressions, clicks, CTR over a chosen window; striking-distance queries; high-impression/low-CTR pages; `--page <url>` / `--query "<q>"` drill-downs for query↔page attribution. German-market/bilingual sites: pass `--country deu` (ISO alpha-3; also on `insights.py`) — default numbers are blended across every country, which can mask or fake German positions. Keyword matching folds umlauts/ß ("München" matches rows typed "muenchen") |
| **Live Google SERP** | `serp_check.py` | Serper key (free, optional) | The actual Top-10 for any keyword + where you sit — incl. keywords you don't rank for yet |
| **Bing Webmaster Tools** | `bing_query.py` | API key (free, optional) | Bing query **and page** stats — a Copilot/ChatGPT-visibility proxy; ~6-month aggregate |
| **Trend over time** | `track.sh` + `_history.py` | — | Appends each run to a CSV and prints week-over-week position movement (▲/▼) |
| **Weekly auto-tracking** | `schedule_tracking.sh` | — | Opt-in launchd job (per site) that runs the tracker weekly so history builds unattended |
| **Google & Bing report page** | `search_report.py` | same GSC sign-in; never opens a browser | One page for the owner: visits and times shown per week (up to 16 months), each key search's position (3 months), searches just below page 1, pages shown often but rarely clicked, Bing from the history. Rebuilt by the weekly job; its counting rules are in the script's header |
| **Weekly fix proposal** | `search_report.py` + `fix_proposal.py` | same GSC sign-in; `gh` to follow pull requests | One proposed fix at the end of the report page and the sentence the owner says to get it made. When they say it ("/search-console-insights work '…' into …"), follow `references/fix-proposal.md`: the edit goes through the site's own tests as a pull request |
| **Google's and Bing's own AI reports** | `ai_reports.py` | none: the owner downloads each report | Real impressions in Google's AI Overviews and AI Mode, real citations in Copilot; shown on the Google & Bing page. See `references/ai-reports.md` |
| **Does AI name you? (GEO)** | `geo_check.py` | One OpenRouter key for all four chat assistants (prepaid once), or direct keys; Google via the SerpApi key; all optional | Asks up to four AI engines plus Google's AI Mode and AI Overview the owner's buyer questions, with and without web search; counts how often the business is named and cited; weekly trend. See `references/geo-check.md` |

The GSC, Bing and Serper calls are **read-only** and on **free tiers** (GSC + Bing
free; Serper 2,500 searches free) — nothing is ever written back to Google/Bing/Serper. The
optional AI check is different: it sends the owner's questions to the AI engines the owner
added keys for, on the owner's own account, and some of those cost money (see
`references/geo-check.md` → Costs). Local
writes are all under `~/.config/gsc-insights/`: the history CSV (plus a `.lock` sidecar) on
by default whenever `--keywords` is given (`--no-csv` opts a single run out), the cached OAuth
token from onboarding, `--out` if you ask for a saved report, the AI check's `geo/` folder
(its settings, history and saved answers) once it is set up, and — only if you explicitly
schedule it — a per-site launchd plist/log. Built for a **low-volume** site — see the
"Low-volume playbook" below. On first use the agent runs a guided **onboarding** (next
section), so a non-technical owner never touches the terminal.

> **Prerequisite:** the property must be verified in GSC (`search-console-setup`).
> GSC only collects data **forward from verification** — no historical backfill, and a
> ~2–3 day reporting lag. A freshly-verified site will be near-empty; `gsc_query.py`
> says so honestly rather than pretending there's nothing to optimize. Re-run weekly —
> Phase 1 is the part that compounds.

## Onboarding — first use only

**If the user is NOT yet connected** (no token at `~/.config/gsc-insights/token.json`),
read `references/onboarding.md` and follow its wizard exactly — do not dump raw setup
commands at what's usually a non-technical site owner. It sells the benefit first, asks
before doing anything, checks what's already done so a returning user is never
re-onboarded, and hands off the steps only a human can click through inside Google's
console. Once connected, skip straight to "Once connected — how to use it" below.

## Once connected — how to use it

Tell the user they **never need the command line again**. From now on, in any normal
Claude session, they just ask:

- **Slash command:** `/search-console-insights`
- **Or plain language** (these trigger the skill):
  - *"show my Search Console insights for `<site>`"*
  - *"where do I rank for `<keyword>`?"*
  - *"what are my quick SEO wins?"* / *"striking-distance keywords"*
  - *"which pages get seen but not clicked?"*
  - *"who's in the Top 10 for `<keyword>`?"* (uses the free Serper add-on)
  - *"how do I rank on Bing?"* / *"my Copilot/ChatGPT visibility"* (uses the Bing add-on)
  - *"is my ranking improving?"* / *"track my rankings over time"* (runs the weekly tracker)
  - *"track my rankings automatically / every week"* (offers to schedule it, per site)

**Default behavior (agent):** for the slash command or a general "where do I rank" ask,
source the env file first, same as `track.sh` does, so `BING_API_KEY`/`SERPER_API_KEY` are
actually picked up (`insights.py` reads plain `os.environ` — it does not source the file
itself), then run the **combined** view:
```bash
[ -f ~/.config/gsc-insights/.env ] && { set -a; . ~/.config/gsc-insights/.env; set +a; }
~/.config/gsc-insights/venv/bin/python scripts/insights.py --domain <site> --keywords "…"
```
It auto-detects which sources are connected, shows **Google + Bing side by side** per
keyword, and prints a nudge to connect any missing free source:
- only Google connected → show it + offer the ~2-min Bing key (Copilot/ChatGPT proxy);
- a source connected but the call failed → shown as "⚠️ fetch failed" (do **not** tell them
  to re-set-up — it's a transient error);
- no Serper key → suggest one (free 2,500/mo) for the competitor Top-10.

Run the single-engine scripts (`gsc_query.py` / `bing_query.py`) only when the user wants
one engine's full detail; run `serp_check.py` only when they ask for competitors (it spends
Serper quota); run `track.sh` for the over-time trend. Every Phase 1/Bing/combined run that
was given `--keywords` now auto-appends a row per keyword to the history CSV on its own (no
`--csv` needed; a keyword with no matching query still gets a row, recorded as unranked), so
history quietly builds from ordinary use — but that alone doesn't
guarantee it *keeps* building if the site goes quiet between asks. An ad-hoc run only
reports how many rows it appended (stderr), not a trend — it does not itself print `(new)`;
that marker only appears from `track.sh` / `_history.py`, which print the full trend. So
check for the scheduling gap directly and deterministically instead of watching for that
marker: **once per site per session**, run `bash scripts/schedule_tracking.sh status <site>`
(exact match for one domain — not `list`, whose output is a sanitized label that can collide
between domains) and, if it says "not scheduled," **actually ask** whether to schedule weekly
tracking for it (see "Weekly auto-tracking") rather than only mentioning it in passing. This
applies the same way whether the site went through onboarding recently or was connected long
before — the trigger is "this site has no schedule yet," not "just finished onboarding" or
"just saw a `(new)` row." **macOS only** — `schedule_tracking.sh` manages launchd, so its
`status` is authoritative there. On **Linux** there is no script-managed schedule to query
(the guidance there is "run `track.sh` from a systemd user timer or cron yourself" — see
"Weekly auto-tracking"), so ask the user directly whether they already have a recurring job
for this site instead of assuming "not scheduled" from a check that can't see it.

(See "Capabilities at a glance" above for what each source returns.) Re-running
**weekly** is the whole point — rankings move, and this report is how they watch the
needle.

## One-time setup (human-in-the-loop)

The agent drafts these; the owner clicks (account + OAuth consent are owner actions).

1. **Enable the API + make an OAuth client** (once per Google account):
   - Google Cloud Console → create/pick a project → **APIs & Services → Library** →
     enable **Google Search Console API**.
   - **APIs & Services → Credentials → Create credentials → OAuth client ID** →
     Application type **Desktop app** → Create → **Download JSON** → save it as
     `~/.config/gsc-insights/client_secret.json`, where every script looks for it (point
     elsewhere with `--client-secret` or `$GSC_CLIENT_SECRET`). Never in the site's folder.
   - Add yourself as a **test user**: APIs & Services → **Google Auth Platform** (the
     2024+ name for the OAuth consent screen) → **Audience** tab → **Test users** → Add.
     Without this, consent is blocked for an external app in "Testing".
2. **Create a venv + install deps** (one-time, local — plain `pip install` fails on
   PEP-668 "externally-managed" Python, e.g. Homebrew/macOS). Use a stable home that
   matches where the OAuth token is cached. Any Python 3.9+ works, including macOS's stock
   `python3`:
   ```bash
   python3 -m venv ~/.config/gsc-insights/venv
   ~/.config/gsc-insights/venv/bin/pip install -r requirements.txt
   ```
   Save the downloaded `client_secret.json` to `~/.config/gsc-insights/client_secret.json`.
3. **(Phase 2, optional)** free Serper key at https://serper.dev →
   `export SERPER_API_KEY=...` (or a SerpApi key → `export SERPAPI_KEY=...`).

## Reading the numbers — from GSC data to a conclusion

Pulling the report is the easy part; the diagnosis is where mistakes happen. Every
rule below was a real interpretation error caught in a live site's data. Apply them
before stating any conclusion, not just when something looks off.

1. **Only the property-level figure is a site-wide total.** The report prints up to
   three, labeled: **property-level** (no dimension — one impression per results
   page; the only valid site-wide denominator, within any `--country` filter you
   passed), the **page-level sum** (counts each
   of your pages separately when several share one results page — brand sitelinks
   inflate it), and the **query-level sum** (anonymization drops rare queries —
   undercounts on thin sites). The script warns when they disagree by >10% and
   labels any fallback a floor/ceiling; never promote either sum to "the" total.
   (Both sums also cap at 25,000 rows per pull; the property-level row does not.)
2. **A percentage or comparison must name its denominator AND its window.** State
   which total it is computed against, and which date range and report it came from.
   Never compare numbers from different windows or sources (a 28-day GSC pull vs
   Bing's ~6-month aggregate; a fresh pull vs a figure quoted from an older report)
   without saying so. Best of all, prefer page-relative figures ("123 of this page's
   own 150 impressions") — they need no site-wide denominator at all and say more.
3. **Separate brand from non-brand before concluding anything.** On a young or niche
   site, most impressions are the brand name and its typos: they inflate totals, CTR
   and the top-queries table, and say nothing about SEO progress. Label brand rows,
   and say whether a percentage is of all traffic or of non-brand traffic.
4. **CTR only means something together with position — and with the live SERP:**
   - **Position ≤5, CTR near 0%:** a snippet **or SERP-context** problem — the
     mandatory live check (#6) decides which. On entity/person queries a knowledge
     panel or Wikipedia can absorb the clicks while your snippet is fine.
   - **Position 6–15, low CTR:** snippet, or a format/relevance mismatch — check
     what's actually ranking around you (Phase 2) before assuming a copy fix.
   - **Position >20:** not a CTR problem yet; a title rewrite rarely helps here.
   - **Under ~20 total impressions, at any position:** too thin to diagnose. Say so —
     "insufficient volume to conclude anything yet" is a correct, honest answer.
5. **Attribute queries to pages with data, not inference.** Never assert which page a
   query lands on — or that two pages cannibalize one query — from the separate
   query and page tables. Pull it: `--page <url>` (queries landing on that page) or
   `--query "<q>"` (pages serving that query). One flag replaces a guess.
6. **MANDATORY before any CTR/snippet diagnosis:** the live-SERP-snippet check under
   Phase 2 — Google often discards the shipped meta description, and the SERP around
   you explains a CTR gap at least as often as your snippet does.
7. **Correlation needs a control before it becomes a cause.** Before crediting or
   blaming any change (yours or Google's): segment out bots and brand, compare equal
   windows, and check pages you didn't touch. Cross-check GSC against the site's own
   analytics (Plausible/GA) — GSC counts SERP events, not what happened after the
   click, and its clicks can include non-human ones. If clicks and analytics visits
   disagree, verify the tracking snippet in the live rendered HTML (`curl`) before
   calling the gap behavioral. Until a control agrees, write "consistent with", not
   "explains".

**Worked example (real case).** "123 impressions = 32% of site-wide traffic" used the
query-level sum (384) as its denominator — an anonymization-shrunk number. But the
"corrected" claim quoted the page-level sum (1,071) as the truth, which overcounts the
other way. The defensible number needed no site-wide denominator at all: 123 of the
target page's own 150 impressions (~82%) — with the query→page mapping confirmed via
the `--query` drill-down (rule 5), not assumed. Page-relative framing is harder to get
wrong and more useful.

## Phase 1 — GSC data (free, high-signal)

```bash
~/.config/gsc-insights/venv/bin/python scripts/gsc_query.py \
  --site sc-domain:example.com \
  --days 90 \
  --keywords "AI Events Munich,AI Meetups Munich,AI Treffen München" \
  --client-secret ~/.config/gsc-insights/client_secret.json \
  --out report.md
```

- `--site` uses `sc-domain:<domain>` for a **Domain** property (what
  search-console-setup creates), or the full `https://…/` URL for a URL-prefix one.
- First run opens a browser for consent; the refresh token is cached at
  `~/.config/gsc-insights/token.json` (chmod 600) so later runs are silent.

The report opens with **up to three site-wide totals** (property-level = the
denominator; page-level and query-level sums as labeled references, flagged when they
disagree by >10% — see "Reading the numbers" above for why each differs), then three
actionable sections (then top-queries / top-pages tables):

1. **Target keywords — where we stand.** Best-matching query, avg position,
   impressions, clicks, CTR for each `--keywords` term (or "no impressions yet").
2. **Striking-distance queries** (avg position ~8–20): already on Google's radar,
   one push from the Top 10. Highest ROI — prioritise these.
3. **Good position, low CTR pages** (rank ≤10, CTR <2%): they're *seen* but not
   *clicked* → investigate the snippet or the SERP context (rule 4 of "Reading the
   numbers") before deciding the title/meta is the bottleneck.

## Phase 2 — competitive SERP (who actually ranks)

**What a SERP tool is for — and why GSC/Bing can't do it.** Search Console and Bing only
show **your own** data: queries *you already appear for*, and *your* position. They are blind
to everyone else and to any keyword you don't rank for yet. A **SERP API** fetches the **live
Google Top-10 for any keyword** — answering the questions your own data can't:

- **Who is beating me?** — the actual pages ranking 1–10 (your real competitors).
- **What's my true position** for a term I barely rank for, or am absent from?
- **What format does Google reward here?** — the highest-value read (see "How to use it").
- **Where is the competition weak?** — terms whose Top-10 is thin/aggregator-only = easier wins.

It turns owned data ("where am I?") into strategy ("where's the gap, and what beats it?").

```bash
set -a; . ~/.config/gsc-insights/.env; set +a    # loads the SERP key (keep it out of shell history)
~/.config/gsc-insights/venv/bin/python scripts/serp_check.py \
  --keywords "AI Events Munich,AI Meetups Munich,AI Treffen München" \
  --domain example.com            # --provider serper (default) | serpapi
```

Prints the live Top-10 per keyword, flags your own position (or absence), and logs how many
searches were spent so you never blow a free cap. The SERP language follows the target
country (`gl=de/at/ch` → `hl=de`, else `hl=en`; `--hl` overrides); `gl`
defaults to `de` (Munich). No key set → it exits cleanly; GSC/Bing are unaffected.

**How to use the output:**
1. **Read intent / format.** Top-10 is event aggregators (Meetup, Eventbrite, Luma) → Google
   wants a *current, structured listing*; it's listicle guides ("Top AI meetups in Munich") →
   a *guide page* wins. Build the format that ranks.
2. **Pick winnable terms.** Where the Top-10 is weak (thin pages, only aggregators, no real
   authority) you can break in — easier than the contested head term.
3. **Find your gap.** Compare the ranking pages to yours — what do they cover that you don't?
4. **Get listed.** If aggregators own the SERP, being *on* them (Meetup, Luma, dev.events) is
   half the battle, not just your own page.
5. **MANDATORY before any CTR/snippet diagnosis: check the printed `snippet` field against the
   page's actual shipped `<meta description>`.** Google frequently discards the shipped
   description and auto-generates a snippet from body text instead — a "the description is too
   long/short, that's why CTR is low" diagnosis is unverified, and can be flatly wrong, until this
   is checked. Confirmed live 2026-07-30 (a real site, both Codex and Kimi flagged the diagnosis as
   unverified in review; the live check then showed one page's 318-char description fully
   discarded for a body-text auto-snippet, while a different page's real 145-char description WAS
   shown, truncated — two different pages, two different mechanisms, neither guessable from GSC
   numbers alone). Never finalize a title/description rewrite recommendation without this check.

**Provider-agnostic — Serper is today's default, not a hard dependency.** A SERP API is a
commodity; the script targets the *capability*, not one vendor, and free tiers shift over
time — so pick whatever's free/cheap when you set up:
- **Serper** — current default; ~2,500 free searches, then ~$0.30/1K.
- **SerpApi** — ~250 free/month; very clean parsing (already supported: `--provider serpapi`).
- **Others** (Scrape.do, Decodo, HasData) — similar free credits; **DataForSEO** is the paid
  backbone (no free tier, ~$0.0006/SERP) once you outgrow the free ones.

To add a provider: drop a `--provider <name>` branch into `serp_check.py` (its own API call →
the same `{position, title, link, snippet}` shape) and read its key from the `.env`. If your
provider ever kills its free tier, switch the flag — the rest of the skill is unchanged.

## Bing Webmaster Tools — optional second source (Copilot/ChatGPT proxy)

Bing's index feeds **Microsoft Copilot and ChatGPT search**, so Bing rankings are a
useful proxy for *AI-assistant* visibility — and connecting it is **far simpler than
Google: one API key, no OAuth, no browser**. Volume is much smaller than Google for
niche local queries, so treat it as a secondary signal.

**Connect (one-time, ~2 min, 🧑 human):** Bing Webmaster Tools
(https://www.bing.com/webmasters) → **Settings → API Access** → generate an **API key**
→ add it to `~/.config/gsc-insights/.env` as `BING_API_KEY=...`. (The site must already
be added to Bing — `search-console-setup` covers that via "Import from Google Search
Console".)

**If `BING_API_KEY` is already set** in `~/.config/gsc-insights/.env` from a prior session,
skip straight to using it (same "don't re-onboard what's already done" principle as GSC's
own connection check) — confirm with `GetFeeds` that connected sites still have a
registered, successfully-crawled sitemap. Note: Bing does **not** reliably
auto-discover a sitemap from `robots.txt` the way Google does — if `GetFeeds` returns `{"d":[]}`
for a site despite a correct `robots.txt` entry, submit the sitemap URL manually under
Bing Webmaster Tools → **Sitemaps** (needed for a real site, 2026-07-24).

```bash
set -a; . ~/.config/gsc-insights/.env; set +a    # loads BING_API_KEY
~/.config/gsc-insights/venv/bin/python scripts/bing_query.py \
  --site https://example.com \
  --keywords "AI Events Munich,AI Meetups Munich,AI Treffen München" --out bing.md
```

Same report shape as Phase 1 (target keywords → striking distance → pages seen-but-not-
clicked → top queries/pages), from Bing — `GetQueryStats` + `GetPageStats`. Note: Bing
returns one **aggregate row per query over its last ~6 months**
(no date range), and `--site` must be the exact verified URL shown in Bing (https,
trailing slash as registered). No key set → it exits cleanly; GSC is unaffected.

## Track positions over time (weekly)

A single snapshot can't tell you if you're *improving*. `track.sh` pulls GSC + Bing for
your keywords, appends each run to a history CSV, and prints the movement since last run:

```bash
set -a; . ~/.config/gsc-insights/.env; set +a
bash scripts/track.sh example.com "AI Events Munich,AI Meetups Munich,AI Treffen München"
```

Output is a per-keyword trend (**lower position = better; ▲ = improved**). The tracker
pulls a **28-day window** (`GSC_TRACK_DAYS` overrides) so week-over-week moves are
actually visible — a 90-day window would smooth them away — and it marks moves that
aren't real rank changes: `≠` = the best-matching query changed between runs, `~` = a
compared side has under 10 impressions (noise), `‡` = the tracked window or country
filter changed between runs, or the earlier row predates the config columns (both
recorded in the CSV, so the trend flags its own config breaks; only a move between
two pre-schema runs leaves no record to flag). The best-matching query for a keyword is
chosen so: queries with enough impressions to trust (10+, the `~` floor) come first; on the
same side of that floor the exact phrase beats a variant; then volume decides. After
updating this skill, the first tracker run may show `≠` where the tracked query was
redefined — not a rank move. The first run just seeds the history —
re-run **every 1–2 weeks** to watch the needle, or see "Weekly auto-tracking" below to stop
relying on remembering. (Every query script — `gsc_query.py`, `bing_query.py`,
`insights.py` — appends to the history CSV **by default** now whenever `--keywords` is set,
no `--csv` flag needed; pass `--no-csv` to skip it for one run. A same-config re-run on the
same date **replaces** that date's row per keyword rather than duplicating it — the dedupe
key includes the window/country, so an ad-hoc pull at a *different* window than the scheduled
28-day job adds a second same-day row instead of silently erasing the scheduled one.
`python scripts/_history.py <csv>` reprints the trend without a new pull.)

## Weekly auto-tracking (opt-in, per site) — ask, don't just mention

German-market sites: install with `GSC_COUNTRY=deu` in the environment. Without it the
trend is computed on blended-global numbers while your reports are market-filtered, and the
two disagree. The value is stored in that site's launchd plist and wins over anything in
`~/.config/gsc-insights/.env`. Keep `.env` for API keys: a `GSC_HISTORY_CSV` there would
redirect every ad-hoc run, so remove it; a `GSC_COUNTRY` there is ignored by an
already-installed job, but is picked up at install time if your shell sourced `.env` (check
the `country:` line the install prints), and does nothing for ad-hoc reports, which take
`--country` explicitly. `GSC_HISTORY_CSV` works the same way if a site must
keep its history in its own file, but prefer the shared default: it already keeps sites
apart by a `site` column, and ad-hoc runs don't read the plist, so a per-site file splits
that site's history between the file the job writes and the file `insights.py` writes.
Re-installing a site (to change keywords or the time) carries both settings over from its
existing plist; set one to an empty value to clear it. The install output prints both.

**Check `bash scripts/schedule_tracking.sh status <site>` (macOS)** — first onboarding
(references/onboarding.md Step 7) or any later ranking check on a site connected before this
behavior existed — and if it says "not scheduled," **actually ask** whether to schedule the
tracker weekly for that site, rather than leaving it as a mention the user can skim past
(ad-hoc runs building history on their own is not the same guarantee as a scheduled job when a
site goes quiet between asks). Use `status <site>` for the exact check, not `list` — `list`'s
labels are sanitized (dots become dashes) and can collide between different domains. Check
this, don't infer from trend output — a site can have plenty of history and still have no
schedule. On Linux, `schedule_tracking.sh` has nothing to check (no systemd/cron integration
here — see the platform note below); ask the user directly instead. Let the user choose
**which sites** and a day/time — **never auto-install**, and only on an explicit yes. A no is
a complete answer; don't re-ask in the same session, and don't assume a yes for one site
carries over to the next site connected later.

```bash
bash scripts/schedule_tracking.sh install example.com \
  "AI Events Munich,AI Meetups Munich,AI Treffen München" 1 9   # Mon 09:xx (weekday: 1=Mon…6=Sat, 0/7=Sun; hour 0-23)
bash scripts/schedule_tracking.sh status example.com    # is THIS site scheduled? (exact)
bash scripts/schedule_tracking.sh list                  # everything scheduled (sanitized labels)
bash scripts/schedule_tracking.sh remove example.com
```

Each job runs `track.sh` weekly (GSC + Bing + the AI check if set up → the history CSVs →
both trends), logging to
`~/.config/gsc-insights/logs/<domain>.log` (dots become dashes: `example-com.log`). A month
later, *"is my ranking improving?"*
answers from real data instead of a single snapshot.

Each site starts in its own minute: a new site takes the first of :00, :15, :30 and :45 that no
other site uses at that day and hour (then :05, :20 and the other 5-minute gaps), so their AI
checks are less likely to run at once and hit the engines' rate limits. A 13th site at one day
and hour shares :00, and install warns you to pick another hour. Re-installing a site at the
same day and hour keeps its minute, even one set by hand, unless another site has it too. A Mac
asleep at those times still starts every missed job together when it wakes; their AI checks then
take turns, one site at a time. A site waits up to 90 minutes for its turn, then asks anyway: the
log says so in a ⚠ line, and "This run needs attention" lists the AI check.

Every step runs even if an earlier one failed (an expired Google sign-in no longer costs the
week's Bing and AI data), and the log ends with a **"This run needs attention"** list naming
each problem. Exit code: 0 when that list is empty; otherwise GSC's own code if GSC failed
(2 = the sign-in needs renewing — the job never waits for a browser), else 4 if a GSC or Bing
history write failed, else 1. Bing API errors are on the list too (they used to be swallowed). An AI check that isn't set up is not a problem; homepage warnings from
the AI check aren't either (see `references/geo-check.md`).

- **macOS** uses **launchd** — one LaunchAgent per site, *never* cron. Per-site means each is
  enabled/removed independently; removal is one command.
- **Linux:** run the same `track.sh` from a **systemd user timer** (or cron) — identical effect.
- The job only *records* data. A natural future extension: alert on a big move (diff the latest
  two CSV rows and surface large position deltas) — not built yet.

## Does AI name you? — the weekly GEO check (opt-in)

Buyers ask ChatGPT and friends instead of Google. `geo_check.py` asks up to four AI engines
(Gemini, OpenAI, Anthropic, Perplexity), plus Google's AI Mode and AI Overview via SerpApi, the owner's own buyer questions — without naming the
business — twice: **"knows you"** (no web search: what the model learned) and **"finds you"**
(web search on: what a buyer gets today, plus which sites were cited; for Perplexity, which search results it returned). Code counts the
mentions; every answer is saved verbatim; `track.sh` runs it weekly after Bing and prints its
trend under the keyword trend.

**Read `references/geo-check.md` before setting it up or reading its results.** Three rules
from it that apply every time:

- **At the start of any session that looks at this site's AI results, run
  `~/.config/gsc-insights/venv/bin/python scripts/geo_check.py <domain> --check-drift` first.** If the homepage changed since
  the questions were confirmed, read the homepage (and POSITIONING.md if present), propose
  updated questions, and **ask the owner** before changing anything. First check that the new
  homepage text is the real page: a cookie or bot page also shows up as "changed".
- **Show results as the report page** (`~/.config/gsc-insights/venv/bin/python scripts/geo_check.py <domain> --report`), not raw files.
- **Google and Bing results the same way:** `~/.config/gsc-insights/venv/bin/python scripts/search_report.py <domain>` prints the path of the owner's page; open it. Owners ask *"show me my Google report"*; with several sites, ask which one. It uses the settings the weekly job last recorded unless given `--keywords`/`--country`; a job set up before this page existed records them on its next weekly run; until then the page falls back to the history, so for a site with its own history file pass `--csv <that file>`.
  Owners ask for it in their own words: *"show me my AI report"*, *"how is my business doing with AI?"*.
- **Google's and Bing's own AI reports** (real answers, not our questions): the owner downloads them; read `references/ai-reports.md` before importing one or
  talking about its numbers. "No data yet" is a result. Keep reports and downloads in the site's `analytics/` folder: `references/analytics-folder.md`.
- **You draft the questions; you never answer them.** The whole point is a buyer's
  un-primed question to an engine that knows nothing about this conversation.

## Acting on the report — hand off to existing skills

- **Low-CTR titles/descriptions** → `copywriting` (title) + `website-seo-geo` (the
  50–60 / 140–160 char limits and the og/canonical contract).
- **Striking-distance terms with no dedicated page** → a new page via the content
  skills (`website-content-guide`, `programmatic-seo` for many similar pages); for
  an events site, a city events guide + `Event` JSON-LD is the natural home.
- **Event rich results** → `schema-markup` (the `Event` type on event detail pages).
- **Bigger technical issues surfaced by coverage** → `seo-audit`.

## Low-volume playbook — 5 ways to use this when traffic is thin

Most SEO advice assumes lots of data. A niche/local site (like a Munich AI meetup) has
little — so the usual "wait for statistical significance" doesn't apply. Tell the user
to work it like this:

1. **Track position & impressions, NOT clicks.** At low volume clicks are ~0 and noisy;
   *average position* and *impressions* are the stable signals. A win is a target
   keyword's position trending up week-over-week — even while clicks stay at 0.
2. **Convert striking-distance queries (pos 8–20) one at a time.** Few keywords means you
   can hand-optimise each. Take the report's striking-distance list and thread that exact
   phrasing into the page's `<title>`, H1, and first paragraph. Moving one query 12→8 is a
   real, attributable win.
3. **Fix titles for queries you already rank for but nobody clicks.** Ranking ≤10 with ~0
   clicks = a *snippet-or-SERP* problem, not a ranking problem — and it's higher ROI at low
   volume than chasing new terms. Run the mandatory live-SERP check first; rewrite the
   title/meta only if it shows a snippet problem you control (→ `copywriting` +
   `website-seo-geo`).
4. **Mine the queries you never targeted.** The top-queries table surfaces terms you
   *accidentally* rank for (speaker names, adjacent topics, "claude code munich"). On a
   thin site these are gold — real demand. Build or expand a section around the ones that
   fit your goal.
5. **Use the SERP + Bing layers to find weak-competition terms.** Your own data is sparse,
   so lean on `serp_check.py` (who's *actually* in the Top 10) and Bing to spot terms where
   the Top 10 is weak or aggregator-only — easier than the head term. Long-tail and
   other-language variants (e.g. German) are where a low-volume site wins *first*.

**Cadence:** re-measure every **1–2 weeks**, not daily (daily is noise at this volume).
Compare a 28-day window to the prior 28 days to see genuine movement.

## Scope notes

- **Read-only** GSC scope (`webmasters.readonly`); never writes to the property.
- This is data + analysis, **not** registration (`search-console-setup`), not the
  on-page metadata contract (`website-seo-geo`), not AI-answer optimisation (`ai-seo`) —
  the GEO check *measures* whether AI names you; `ai-seo` is how to change that.
- **Not index coverage.** These scripts read Search Analytics only. Never claim a
  page "isn't indexed" from its absence in a list, table, or report — verify with
  GSC's URL Inspection (tool or API) first; absence of impressions is not absence
  from the index.
- **Opt-in** skill: it needs API creds, so it is deliberately **not** in the
  `new-website` always-on copy set — copy it into a project only when wanted.
- Paid scale-up (not wired here): DataForSEO (no free tier, $50 min) is the option if
  you outgrow Serper/SerpApi and want a full keyword/SERP backbone — see
  `references/keyword-strategy.md`.
- **Always report full absolute URLs** (`https://domain.tld/path`) — never bare paths,
  domain-relative fragments, or truncated prefixes. Owners copy these straight into GSC's
  Removals tool, a browser, or elsewhere; a partial URL forces manual reconstruction.

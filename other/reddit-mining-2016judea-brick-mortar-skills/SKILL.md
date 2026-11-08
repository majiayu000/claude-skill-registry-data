---
name: reddit-mining
description: >-
  Search Reddit for real threads and comments on any topic — tool/stack
  discovery, competitor or brand chatter, sector pain points, "what do
  people actually say about X" — via a free, no-auth script that bulk-reads
  the Arctic Shift archive and filters locally (Reddit blocks crawlers and
  login-gates search, so WebSearch/WebFetch can't do this directly). Use
  whenever a task needs genuine Reddit discussion instead of a secondhand AI
  paraphrase of it.
compatibility: >-
  Python 3, standard library only. Network access to one host:
  arctic-shift.photon-reddit.com (the public Arctic Shift Reddit archive). No key, no login.
allowed-tools: Bash(python3:*) Read
metadata:
  network-hosts: "arctic-shift.photon-reddit.com"
  network-purpose: "read public Reddit posts and comments from the Arctic Shift archive"
  version: "1.1"
---

# Reddit mining

Reddit is a good source for two things a normal web search won't reliably
surface: **what real builders/operators actually use** (tool names, repo
names, workarounds) and **unfiltered sentiment** (brand reputation, sector
complaints, "X vs Y" arguments).

`scripts/reddit_pull.py` reads the **Arctic Shift** archive
(`arctic-shift.photon-reddit.com`) — a free, no-auth mirror of the Reddit
corpus. No app, no key, no login.

Nothing here bundles, hosts or resells Reddit data: the script queries the public
archive from your own machine, and Reddit's terms (and Arctic Shift's) govern what you
do with what you pull.

`scripts/reddit_tally.py` counts a pull (themes, phrases, asks over time, tools,
thread digests) so no number in a report is the model's estimate. The task skills built
on this one use it: `reddit-pain-points`, `reddit-demand-check`, `reddit-tool-stack`,
`reddit-competitor-chatter`, `reddit-customer-language`, `reddit-thread-digest`.

## Why every other route is dead (verified 2026-08-16)

Don't re-test these. Each was checked directly and failed:

| Route | Result |
|---|---|
| **PullPush.io** | HTTP 429 on *every* request, body: `"This website does not provide free scraping resources for agents... contact the administrator on Discord if you're interested in a paid scraping service."` A **policy block, not a throttle** — no backoff clears it. |
| `reddit.com/*.json` direct | 403, HTML bot-block body |
| `old.reddit.com/*/search.json` | 302 → login wall, on **every** sub including SFW ones (r/programming). Not an 18+ gate — Reddit login-gates search globally now. |
| Redlib mirrors (safereddit.com etc.) | 200 that is an **Anubis proof-of-work challenge page**, not content. A 200 here means nothing; check the `<title>`. |
| WebSearch/WebFetch on reddit.com | Anthropic's crawler is blocked at the domain level — returns a hard error. |
| Official Reddit API | Free tier (100 QPM) still exists, but self-serve registration is closed under the Responsible Builder Policy; new OAuth access needs manual approval, ~2–4 weeks. Worth starting if Reddit becomes load-bearing; useless today. |

## Two constraints that dictate the design

### 1. A request returns at most ~100 rows, and drops the rest SILENTLY

**Current fix (2026-11-03): every window is paged oldest-first.** `page_window()` asks
with `sort=asc`, then moves `after` to the newest timestamp seen, until a page comes back
short: one request per 100 rows, nothing dropped, no floor. It replaced date-coverage
splitting, which bottomed out at one day: a single day of r/smallbusiness held 166 posts
and the splitter kept 100 of them, so every busy day lost about 40%. Two traps found on
the way: `after` is exclusive (restart one second early, de-duplicate by id), and a split
midpoint with microseconds (`14:25:07.5`) is rejected as an invalid date, which reads as
a failed window. Same day, same 166 posts, in 4s instead of 9s; a year of r/restaurateur
gives the identical 1,237. The history below is why each earlier version lied.

**Measured 2026-08-23, and it had been quietly halving every pull before that.**
`limit` is rejected above 100 (`"'limit' must be between 1 and 100"`), so
`limit=auto` is the only way past 100 — and `auto` tops out near **260 rows per
request**, nowhere near the 1000 the script's original `CAP` assumed.

The damage is that it truncates by **recency**, not by refusal. One 90-day
r/AnalogCommunity request returned 258 posts spanning only its **last four
days**; the other 86 days were dropped without a warning, an error, or a short
row count that looked wrong. A count-only cap check at 1000 never fires, so the
run prints `2302 posts scanned` and reads as complete coverage of two years
while actually holding ~4% of it, biased to the end of every window.

`fetch_window()` now detects truncation by **date coverage instead of row
count**: if the oldest row returned is newer than the window's start, the
server didn't reach the beginning and the window is split. Same 90-day window
after the fix: **7,203 posts instead of 251.**

**What this means for you:** any pull run before 2026-08-23 sampled roughly the
tail of each window. If a conclusion rested on counting hits in an old corpus,
re-run it — the corpus was not what the stderr said it was. And never trust
`N posts scanned` as coverage on a busy sub without checking that the windows
actually reached back; `--window-days` smaller than the truncation depth is the
crude fallback if the date check is ever removed.

**It came back 2026-10-11: `auto` now returns at most 100 posts.** With
`NEAR_CAP = 200` the date check never ran, so every window silently kept its
newest 100 — a city sub reported "600 posts scanned" for 16 months. `NEAR_CAP` is now
90. If stderr shows windows scanning exactly 100 (or any round ceiling) and
never splitting, the server's ceiling moved again: lower `NEAR_CAP` below it.
Also: the output now carries `author` (needed when drafting replies).

#### 1a. The same bug bites COMMENTS, harder, and needs SUB-DAY windows

`--comments N` fetches only the top N comments *per post* (`top_comments()`).
For a whole comment corpus — any prevalence or "nobody talks about X" claim —
use `--bulk-comments`. **Never hand-roll a loop against `/api/comments/search`:
one did, on 2026-08-23, and silently undercounted a quarter of
r/physicaltherapy by 6.5x.**

**Fixed 2026-08-23: use `--bulk-comments`.** It walks the range in SECONDS, not
days, because the comments endpoint truncates far harder than posts and a
day-at-a-time loop is still short. Measured on r/physicaltherapy:

| request | rows | coverage |
|---|---|---|
| one 8-day window | 113 | **only the last day** |
| one single day (2026-03-08) | 100 | only 14:08–23:47 |
| that day via `--bulk-comments` | **196** | 00:01–23:47 |
| that 8-day window via `--bulk-comments` | **2,074** | every day, 00:0x–23:5x |

**An 18× undercount on an 8-day window.** `limit=auto` reaches ~260 on
`posts/search` but only ~100–113 here, and it drops the OLDEST rows.

Two things this cost to get right, both worth knowing:
- **`fetch_window()` cannot be reused.** It splits on whole days and bottoms out
  at `span <= 1`, which is *above* the depth at which comments still truncate.
  Hence a parallel walker with a 15-minute floor.
- **`NEAR_CAP` is load-bearing, not a nicety.** Dropping it made every *sparse*
  window look truncated — a window genuinely holding one comment at 10:12 has an
  oldest row newer than its start — so the walker split to the floor on every
  quiet hour and a one-day pull ran past 120s. With the guard restored
  (`NEAR_CAP_COMMENTS = 90`) the same day takes **6.9s**.

**Which old conclusions survive.** Percentages of *common* terms held up across
the short and complete corpora — pay/salary 8.54% either way, documentation
4.57% vs 5.17%, insurance 2.77% vs 2.84% — because truncation takes a recency
slice, not a biased one. But **absolute counts of rare terms were ~6x low**,
which is exactly the regime a "nobody talks about X" finding lives in. If a kill
decision rests on a rare-term count, re-pull before trusting it.

### 2. Server-side keyword search does not work at useful scale

**Arctic Shift's server-side keyword search does not work at useful scale.**
`query=` / `selftext=` / `body=` time out even on a one-month window of a
mid-size subreddit. A date-windowed *listing* of the same sub returns 1000
posts in ~6 seconds.

So the script **never asks the server to search**. It bulk-reads date windows
and filters locally in Python. This is why `--queries` are matched against
title+selftext on your machine, not passed to the API. It also means you get a
real corpus rather than a search index's guess at relevance.

**Timeouts arrive as HTTP 422 with the message in the JSON body.** Always read
error bodies, never just the status code — a handler that logs only `e.code`
turns a splittable timeout into an opaque retry loop. (This exact mistake also
hid PullPush's shutdown message for a full debug cycle.)

## How to run it

```bash
python3 scripts/reddit_pull.py \
  --subreddits AI_Agents LocalLLaMA webscraping \
  --queries "competitive intelligence" "review scraper" \
  --after 2025-01-01 --top 30 --comments 5 \
  > /tmp/reddit_pull.json
```

| Flag | Meaning |
|---|---|
| `--subreddits` | required, space-separated, no `r/` prefix |
| `--queries` | keywords matched **locally**, any-match, case-insensitive. Omit to keep everything in range. |
| `--after` / `--before` | `YYYY-MM-DD`. Defaults to the last 3 years — **narrow this**, it's the main cost driver. |
| `--window-days` | progress-report chunk, default 90 (paging makes it irrelevant to completeness) |
| `--top` | keep N top-scoring matches per sub (default 40) |
| `--top 0` | keep **every** match. Use it whenever you will count anything. |
| `--comments N` | fetch N top comments per kept thread (default 5 when bare) |
| `--comments-for K` | with `--comments`: only the K most-commented kept threads (each costs 1-4s) |
| `--stats FILE` | write posts scanned per subreddit per month: the denominator for any rate |
| `--thread ID_or_URL` | one thread: the post plus every comment, with depth and parent |

### Per-thread comments come from `/comments/tree`, not search (2026-11-03)

`comments/search?link_id=` stops at 100 rows: a 302-comment thread returned exactly
100, so "top N by score" from it was the top N of an arbitrary 100. `comments/tree`
with a large limit returned all 303 in about 4 seconds. `top_comments()` and
`--thread` use the tree and fall back to search only if it fails. Comments now carry
`id`, `author`, `created` and a `permalink`, so a quote can always be linked.

**Run it in the background** and dump to a
scratchpad file. Scanning a busy sub over a year is tens of thousands of posts
and can take minutes. Don't poll it in a tight loop — read the file once.

**Read the output by grepping for context, not by loading the raw JSON.**

## Picking subreddits and queries

- **Short, 1–2 word keywords beat exact phrases.** Matching is a literal
  substring test against title+selftext, so `"condom broke"` misses "the
  condom had broken". Prefer `condom` + `broke` as separate terms and let the
  local filter over-collect.
- **General subs beat niche ones that may not exist.** Pair a guessed niche
  sub with reliably-large generalist ones so a bad guess doesn't zero the pull.
- **Windows are the cost knob.** If a run is slow, shrink `--after`/`--before`
  before you shrink anything else.

## Hard rule: qualitative only, never a data source

This is real Reddit text, but it is **unknown-n, self-selected, and not
deduplicated** across near-identical threads. Use it for framing, color,
failure-mode language, and "here's what an actual person said" quotes with a
real permalink attached — never as the source of a number, KPI, or "X% of
people say" claim. If a task needs an actual statistic, that comes from a real
survey/dataset, not from counting Reddit hits. *(Held up under load
2026-08-16: a "how common is this?" question was answered from CDC NSFG and
clinical trial data, with Reddit supplying only voice.)*

## Known limitations

- Arctic Shift is a third-party archive — it lags live Reddit and has coverage
  gaps, especially very recent posts and small/new subs. **Absence of a hit is
  not proof the conversation doesn't exist.** Say so rather than asserting a
  negative.
- **`--queries` shape the corpus, so never report a bucket count as a property
  of the subreddit.** The filter is a literal substring test, so searching
  `identify` and `first edition` returns a sub that looks obsessed with
  identifying first editions. "63 of the 90 threads *I pulled* were
  show-and-tell" is honest; "70% of r/rarebooks is show-and-tell" is not, and
  the two sentences are one careless edit apart. If a count is load-bearing,
  re-pull with `--queries` omitted and count that instead.
- It is a single point of failure, and this skill has now watched one of these
  archives die mid-session. If Arctic Shift starts erroring on *everything*
  (not just keyword search), read the response body first — the shutdown
  notice will be in it — then check the dead-routes table above before
  assuming a transient fault.
- If stderr shows `page did not advance — truncated` or `gave up on`, that slice of
  the range is genuinely missing; say so next to any count that includes it.

## Origin

Originally built on PullPush; **rebuilt on Arctic Shift** after PullPush began
returning a paid-service notice to all agent traffic mid-session (the dead-routes
table is that session's evidence). **Silent ~260-row truncation was found and
fixed later**: every pull before the fix undersampled busy subs by roughly 25-30x.

---
name: ig-feed-research
description: "Scans the logged-in Instagram HOME feed (instagram.com — reels, carousels, and image posts together) in the real Chrome profile (Claude-in-Chrome MCP) for on-niche content ideas AND tailors the algorithm while doing it: every scanned post gets classified, and anything off-niche or not replicable for the brand gets the three-dots → 'Not interested' treatment (plus account-level 'Don't suggest posts from X' for categorically wrong accounts). Harvest and tailoring are ONE loop on ONE surface. Outputs a visual HTML report to research/. Use this for algorithm-driven discovery — what Instagram itself is pushing right now — vs tracked handles (ig-competitor-research). Triggers: ig feed research, instagram feed research, scan my instagram feed, tailor my instagram, clean up my instagram feed, what's my ig pushing, instagram feed ideas, ig feed."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/ig-feed-research/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# IG Home-Feed Research — Ideas + Not-Interested Tailoring in One Loop

Scroll the real logged-in Instagram **home feed** (`instagram.com`), classify every post against the niche, keep what's replicable for the brand, and hit **three dots → "Not interested"** on everything that isn't. Same thesis as `yt-feed-research`: the dismissals aren't cleanup — they're the research engine. Every "Not interested" teaches the suggestion engine, and the feed compounds into a daily idea source.

Why the home feed and not the reels viewer: the home feed carries **carousels and image posts too** (a whole content lane the reels tab hides), and it's the only surface on IG web where "Not interested" exists. One surface, one loop — scan and tailor in the same pass.

## How to Trigger
- "scan my instagram feed for ideas"
- "ig feed research"
- "tailor my instagram feed"
- "what's my ig pushing right now"

## When to Use This vs ig-competitor-research

| ig-feed-research | ig-competitor-research |
|---|---|
| What the algorithm pushes at the creator right now | Tracked handles' weekly best |
| Real Chrome, logged-in home feed | Apify scraper, no browser |
| Discovers unknown accounts breaking out | Fixed competitor list |
| Side effect: permanently improves the feed | No side effects |

## Prerequisites

- **Claude-in-Chrome MCP** connected to the real Chrome profile (must be logged into Instagram). Terminal Claude Code only — the desktop app spawns the MCP tab hidden and scraping silently fails.
- **Instagram UI language must be English.** `feed-tools.js` matches English strings ('Suggested for you', 'Sponsored', 'Learn more', 'More options', 'Not interested', "Don't suggest posts from"); any other locale classifies every row as `followed`, misses ads, and returns `no-entry` on every dismissal.
- Nothing else: no Apify, no yt-dlp. (VidIQ's VPH/multiplier badges only render in the reels *viewer*, not the home feed — here the signals are likes, comments, and judgment.)

## Inputs

- **Idea target** — default **20** saved ideas; user can override inline ("get me 30").
- **Niche filter** — the classification question is: *is this on-niche, or is the format directly replicable for the brand?* If neither → dismiss. The KEEP/DISMISS test is **derived at run time from the repo's context files, never hardcoded here.** Before the first `__feed()` call, read these and build the filter:
  1. `CLAUDE.md` Creator Profile → the **Niche** line. This one-liner defines "on-niche". If it still contains a `<<` placeholder, stop and tell the user: "apply your brand kit first" (`brand-kit.md`), then end the run.
  2. `backbone/offer.md` → what is sold (anything that could seed content promoting that offer is KEEP) and, when present, its "What is NOT sold" list (content whose only angle is a NOT-sold thing is DISMISS).
  3. `backbone/icp.md` → who is served and who is not (content that speaks to the ICP's problems is KEEP; content aimed at the not-served segments is DISMISS).
  4. `competitor-list.md` → every IG handle listed there is **always KEEP** when it shows up in the feed.
  5. `knowledge/*.md` when present → recent research signal on what is working in the niche.
  From that, state the filter in one line each before scanning: **KEEP** = topics matching 1–5, plus any standout carousel/image format the brand could replicate for the carousel lane; **DISMISS** = the categorical off-niche buckets you infer from the above (topics no one in the ICP would ask about, formats the brand cannot film or reproduce); **NEUTRAL** = on-niche but weak or ambiguous. Print the derived KEEP/DISMISS one-liner in the report's `{{FEED_STATE}}` fieldnote (the template has no separate slot for it) so the user can veto it. Example only: a creator whose Niche line says "AI leverage for creators" would KEEP AI builds and model news and DISMISS fitness, cars, and real estate.

(No concrete list ships: derive KEEP/DISMISS on the first run from the Niche line in CLAUDE.md, backbone/icp.md, backbone/offer.md and competitor-list.md, state it in the report, and pin it here once the creator confirms it.)

## Hard Safety Rules (IG action-blocks bots — YouTube doesn't care, Instagram does)

- **Read + dismiss only.** Never like, follow, comment, save, or share from this loop.
- **One dismissal at a time**, with the waits baked into the helpers. Never fire dismissals in batches.
- **Cap ~40 dismissals per session**, max 2 sessions a day. Tailoring compounds across sessions anyway.
- If any **"Try again later" / "We limit how often..."** toast appears: stop dismissing immediately, finish the pass read-only, flag it in the report.

## The Loop

```
read CLAUDE.md Niche line + backbone/offer.md + backbone/icp.md + competitor-list.md → derive KEEP/DISMISS (Inputs)
  → navigate instagram.com → inject scripts/feed-tools.js → __feed() → classify every row
  → KEEP: save to idea list (reels AND carousels AND posts)
  → DISMISS (suggested, off-niche/not replicable): __feedDismiss(ix,'post')
      · categorically wrong account → __feedDismiss(ix,'account')
  → NEUTRAL / followed-but-off-niche / AD: no action (flag repeat offenders in the report)
  → __more() → __feed(<lastSeenIx+1>) → classify the new tail → repeat
  → until idea target hit or feed stalls → fill assets/report-template.html → research/ → open it
```

### Step 1 — Open the home feed
`tabs_context_mcp {createIfEmpty:true}`, navigate to `https://www.instagram.com/`, wait ~4s. If a login wall renders, stop and tell the user.

### Step 2 — Inject helpers + extract
Paste the **entire** `scripts/feed-tools.js` into one `javascript_tool` call (re-inject after every navigation — page loads wipe `window.*`). `__feed(from)` caches one row per loaded article on `window.__rows` and returns only the rows from index `from` onward (`__feed()` = all rows, first pass only): `ix | SUGGESTED/followed/AD | user | reel/carousel/post | likes | caption`. Tool results truncate around 1.5KB, so after the first pass always read the tail, never the whole list. The feed lazy-loads a few articles at a time — `__more()` scrolls one step and reports the article count, so a scan pass is: `__more()` → `__feed(<lastSeenIx+1>)` → classify the tail. Batch 2–3 `[__more, __feed(N)]` pairs per `browser_batch` call when no dismissals are pending.

**Safety-filter trap** (same as YT): never return raw hrefs, query strings, or innerHTML from `javascript_tool` — the harness blocks the whole result (`[BLOCKED: Cookie/query string data]`). Cleaned text only; the helpers already enforce this.

### Step 3 — Classify every row
The test: **on-niche, or replicable for the brand?** (the KEEP/DISMISS filter derived in Inputs)
- **KEEP** → idea list: username, kind (reel/carousel/post), likes, comments, hook/caption line, one-line concept, remix angle. Carousels are first-class keeps — they feed the `carousel-generator` lane directly.
- **DISMISS** → `__feedDismiss(ix,'post')` for a `SUGGESTED` row that fails the test; `(ix,'account')` when the account will never be on-niche (its whole catalog sits in one of the derived DISMISS buckets). The account tier clicks "Don't suggest posts from <user>" on the collapsed card — IG confirms with "We won't suggest posts from X", and an Undo stays available to the creator.
- **Followed rows**: IG offers no "Not interested" on followed accounts (their menu shows Unfollow — never touch it). The helper returns `no-entry` harmlessly if tried; don't try. Flag repeat off-niche offenders in the report instead — unfollowing is the creator's call.
- **AD rows**: no action, ever. The extractor flags them `AD` (Sponsored/Ad/Learn more text, no "Suggested for you" marker) and `__feedDismiss` refuses them with `ix:ad`.
- **NEUTRAL** (in-niche but weak, ambiguous): no action. Don't punish the algorithm for almost-right guesses.

`__feedDismiss` return codes: `ix:ok` (post-level landed), `ix:ok-account` (account block landed too), `ix:already` (card was already collapsed), `ix:no-item` (no article at that index), `ix:ad` (refused), `ix:no-btn` (no three-dots control), `ix:no-entry` (menu had no "Not interested", followed post).

Outlier judgment: no VidIQ badges on this surface — use likes/comments vs how recognizable the account is. Big engagement from an unknown account = the signal; flag `small sample` when it rides on a tiny account.

### Step 4 — Advance and repeat
`__more()` then `__feed(<lastSeenIx+1>)`; classify only the new tail (indexes are stable — dismissed posts collapse in place, scrolling appends). Dismissals go one per `javascript_tool` call, never batched with other dismissals. Expect 20 keeps across a few hundred scanned posts on an untuned feed — and don't grind past ~60–80 articles to force the target; report what you have and note that tailoring compounds across sessions.

**Pagination stall:** the home feed can stop serving articles entirely (stuck at a handful even at page bottom) — that's IG throttling the feed API. Reload once and re-inject; if it persists, end the session early rather than hammering it, and say so in the report.

### Step 5 — Report
Fill **`assets/report-template.html`** (this skill's folder); do NOT design from scratch. The template is the locked preset (same editorial dark "Algorithm Field Report" as `yt-feed-research`, text-only cards with linked usernames, kind tags reel/carousel/post, likes/comments badges). The HTML comment at the top documents every `{{PLACEHOLDER}}` and the card partial to duplicate. Write the filled file to `research/IG-Feed-Research_YYYY-MM-DD_HHMMSS.html` (timestamped so a second same-day session never overwrites the first) and open it in the default browser (macOS `open`, Linux `xdg-open`, Windows Git Bash `start "" <file>`). Never delete prior reports. Sections, in order (the summary strip is the header stat row + feed-state note):
1. **Summary strip** — posts scanned, ideas saved (by kind: reels/carousels/posts), dismissals applied (post vs account level), the derived KEEP/DISMISS one-liner used this session (inside `{{FEED_STATE}}`), feed-state before/after one-liner, any rate-limit flag.
2. **🚀 Top outliers** — biggest engagement-vs-account-size keeps, one-line remix-angle note each.
3. **📈 Strong picks** — the rest of the keeps, badges only.
4. **🎠 Carousel steals** — carousel/image formats worth cloning via `carousel-generator`.
5. **🤔 Borderline** — logged but not counted toward the target.
6. **🧹 Tailoring log** — every dismissal (username + concept + post/account level) so the creator can veto via IG's Undo, plus flagged followed accounts.

Cards: linked username (`instagram.com/<user>/`), hook/caption excerpt, likes/comments badges, kind tag. **No inline thumbnails** — IG media URLs are signed, expire, and trip the safety filter. For visuals/transcripts of the winners, hand the usernames to `ig-competitor-research` or `transcribe-url`.

## Gotchas (all observed live 2026-07-12 — don't rediscover)

- **"Not interested" exists ONLY on `SUGGESTED` home-feed posts.** Followed posts and the reels viewer don't have it (reels menu = Report/Share/Copy/Embed only — that's why this skill doesn't scroll the reels tab; that viewer also hides carousels).
- **JS scrolling is the hardened advance path here** (`__more()` sets `scrollTop` directly) — the home feed is a normal document scroll. Real wheel scrolls get eaten by carousel posts under the cursor; `window.scrollTo` with smooth behavior can silently no-op.
- **Menus are NOT `role="dialog"`** — entries are found by scanning visible childless text leaves outside `<article>`. The account-level "Don't suggest posts from X" renders inside the collapsed article, not in an overlay.
- **JS clicks work for menus and dialog entries** (no cold-start trap on IG, unlike YT). Close a stuck menu with a real `computer` Escape; the JS-dispatched one is unreliable.
- Dialog text uses curly apostrophes ("Don't suggest…") that `clean()` strips — helpers match with `don.?t` regexes; preserve that when editing.
- Ads render as articles without the "Suggested for you" marker but with "Sponsored"/"Ad"/"Learn more" text — never dismiss ads (opens ad-preference dialogs); scroll past. `__feed` flags them `AD` and `__feedDismiss` refuses them (`ix:ad`).
- Like counts sometimes render as "Liked by X and N others" — the extractor matches both forms; "?" likes on followed posts is normal (counts hidden).
- If Claude-in-Chrome errors "not connected", retry once — transient drops mid-session are normal and the in-flight page JS still completed.
- First run of any variant is a calibration run: verify extraction on a few articles before the first dismissal, patch `feed-tools.js` against the live DOM, and log fixes here.

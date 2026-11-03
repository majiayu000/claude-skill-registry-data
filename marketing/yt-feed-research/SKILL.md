---
name: yt-feed-research
description: "Scans the logged-in YouTube home feed in the real Chrome profile (Claude-in-Chrome MCP) for on-niche outlier video ideas AND tailors the feed while doing it — every off-niche tile gets 'Not interested' (one-off misses) or 'Don't recommend channel' (categorically wrong channels), then the feed is refreshed and re-scanned until the idea target is hit (default 20). Reads VidIQ badges (VPH + outlier multiplier + subs) straight off the tiles for free outlier scoring. Outputs a visual HTML report to research/. Use this for algorithm-driven discovery — what YouTube itself is pushing in the niche right now — vs tracked channels (yt-competitor-research). Triggers: feed research, scan my home feed, youtube feed research, tailor my feed, home feed ideas, what's my feed showing, feed outliers, clean up my youtube feed, yt feed."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/yt-feed-research/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# YT Home-Feed Research — Outlier Ideas + Feed Tailoring in One Loop

Scan the real logged-in YouTube home feed, harvest on-niche outlier ideas, and dismiss everything off-niche so each refresh gets more relevant. The dismissals aren't cleanup — they're the research engine: a tailored feed is a compounding idea source that YouTube's algorithm curates for free, personalized by watch history in a way competitor lists and keyword search can't be.

## How to Trigger
- "scan my home feed for ideas"
- "yt feed research"
- "tailor my youtube feed"
- "find outliers in my feed"

## When to Use This vs the Other YT Research Skills

| yt-feed-research | yt-competitor-research |
|---|---|
| What the algorithm pushes at the creator right now | Known channels' weekly best |
| Logged-in, personalized, VidIQ outlier scores | yt-dlp, no browser |
| Discovers unknown small channels breaking out | Tracks the fixed list |
| Side effect: permanently improves the feed | No side effects |

## Prerequisites

- **Claude-in-Chrome MCP** connected to the real Chrome profile (must be logged into YouTube). Terminal Claude Code only — the desktop app spawns the MCP tab hidden and scraping silently fails.
- **VidIQ extension** installed in that profile (provides VPH + outlier multiplier + subscriber badges on feed tiles). The skill degrades gracefully without it — views/age still parse — but outlier scoring gets weaker.
- **YouTube UI language must be English.** `feed-tools.js` matches English menu labels and tile text ('Not interested', 'Don't recommend channel', 'More actions', ' views', ' ago', 'VPH', 'Subscribers'); any other locale returns `:no-btn` / `:no-entry` on every tile.
- No yt-dlp, no Apify. Everything needed (title, channel, views, age, outlier metrics, thumbnail) comes off the feed tiles; thumbnails hotlink from `i.ytimg.com/vi/<ID>/hqdefault.jpg`.
- The finished report needs network when viewed: thumbnails hotlink from i.ytimg.com and the mono font loads from Google Fonts (offline you get blank thumbs and the system font stack, nothing breaks). It opens in your default browser (per-OS command in Step 6).

## Inputs

- **Idea target** — default **20** saved ideas, **long-form only** (shorts never count — see Step 3); user can override inline ("get me 30").
- **Niche filter** — what counts as on-niche. This skill does not define the niche; derive the KEEP/DISMISS lists at run time, before Step 1, from the repo-root context files:
  1. `CLAUDE.md` → Creator Profile → the **Niche** line. If that line still holds a `<<` placeholder, stop and tell the user "apply your brand kit first" (`brand-kit.md`); do not scan.
  2. `backbone/offer.md` (what is sold, and what is explicitly NOT sold) + `backbone/icp.md` (who we serve, who we don't): every kept idea must be able to seed a video that promotes that offer to that audience.
  3. `competitor-list.md` `## YouTube`: uploads from any listed channel are always KEEP.
  4. `knowledge/*.md` when present (e.g. `competitor-patterns.md`, `current-content-opportunities.md`): refine the lists with what has already been proven to work.
  Turn that into a one-line KEEP rule ("anything that could seed a video promoting the offer in `backbone/offer.md`"), a concrete KEEP list (topics, tools, proof formats), and a concrete DISMISS list (adjacent genres that look related but cannot seed the offer, plus the generic off-niche buckets: general news, music, vlogs, unrelated hobbies). State both lists in chat before the first extract so the user can correct them. Example only, for a hypothetical fitness-coach brand: KEEP = training programs, nutrition breakdowns, coach-business content; DISMISS = general news, tech reviews, finance/trading, filmmaking tips.

(No concrete list ships: derive KEEP/DISMISS on the first run from the Niche line in CLAUDE.md, backbone/icp.md, backbone/offer.md and competitor-list.md, state it in the report, and pin it here once the creator confirms it.)

## The Loop

```
derive KEEP/DISMISS from CLAUDE.md Niche + backbone/ + competitor-list.md (stop on << placeholders)
  → navigate youtube.com → inject scripts/feed-tools.js → __extract() → classify every tile
  → save keeps to the idea list → __dismissAny() every off-niche tile (≤3 per JS call)
  → refresh → repeat until idea target hit (usually 2-4 passes)
  → write HTML report → research/YT-Feed-Research_YYYY-MM-DD_HHMMSS.html → open it
```

### Step 1 — Open the feed
`tabs_context_mcp {createIfEmpty:true}`, then navigate the tab to `https://www.youtube.com/`. Wait ~4s, scroll down one screen and back up to force tile hydration (VidIQ badges render late; if every row shows `-vph`, wait 2s and re-extract).

### Step 2 — Inject helpers + extract
Paste the **entire** `scripts/feed-tools.js` into one `javascript_tool` call. Page navigations wipe `window.*`, so re-inject after every refresh — a `__dismissAny is not a function` error just means you forgot.

`__extract()` caches rows on `window.__rows`. Tool results truncate around 1.5KB, so page through slices — and batch the slice-reads in ONE `browser_batch` call:
```js
JSON.stringify(window.__rows.slice(0,7)).replace(/","/g, '"\n"')
```

**Safety-filter trap:** never return raw hrefs, query strings, or innerHTML from `javascript_tool` — the harness blocks the whole result (`[BLOCKED: Cookie/query string data]`). Bare 11-char video IDs and sanitized text are fine; that's why the extractor regexes IDs out of hrefs and strips odd characters.

### Step 3 — Classify every row
Three buckets, judged from title + channel against the niche filter:
- **KEEP** → add to the idea list with id, title, channel, views, age, VPH, multiplier, subs. **Traction floor (calibrated 2026-07-12): a saved idea needs real absolute proof — roughly 1K+ views. A huge outlier multiplier on a tiny channel (e.g. 21x on 83 subs / 322 views) is noise, not signal — don't save it; at most park it in Borderline if the title is a ready-made hook.**
- **DISMISS (video)** → `__dismissAny(ix,'video')` — off-topic one-off from an otherwise fine channel. Always video-level for channels the creator is subscribed to (check the sidebar).
- **BLOCK (channel)** → `__dismissAny(ix,'channel')` — the channel will never be on-niche: it sits squarely in the derived DISMISS list (general news outlets, music/lofi channels, and whatever adjacent genres that list rules out for this brand). Breaking-news shorts respawn from a new outlet every refresh — channel-block each one and the wave dies out. Channel mode never falls back to the video entry: if the menu has no "Don't recommend channel" (subscribed channels, some shorts) it returns `ix:no-entry` and nothing is clicked. Decide then whether to run `__dismissAny(ix,'video')` instead, and log it as a video dismissal, not a block, so `{{BLOCKED_TAGS}}` only lists channels that were actually blocked.

Neutral tiles (in-niche but weak, or ambiguous) get neither — don't punish the algorithm for almost-right guesses. **Shorts are tailor-only: dismiss/block the off-niche ones to train the feed, but never save them as ideas and never report them** — this is long-form packaging research (shorts also lack VidIQ badges, so there's no outlier signal to rank them with).

### Step 4 — Dismiss, in small chunks
Run `__dismissAny` sequentially, **max 3 per javascript_tool call** — more risks the CDP 45s timeout. Two timeout facts that save retry burns:
- **A timed-out call usually still finished** — the page JS keeps running after the client gives up. Never blindly re-run; re-check tile state first (cheap: tile innerText contains `removed` / `won't recommend` / `Feedback shared`). `__dismissAny` is idempotent anyway (`:already`). Return codes: `ix:ok` · `ix:already` · `ix:no-item` (no tile at that index) · `ix:no-btn` (no 3-dot button, usually a cold-start or an ad) · `ix:no-entry` (menu opened, no entry for that mode).
- **Cold-start:** after every navigation the first JS `.click()` on a menu button does nothing (listeners not attached). Fix: one real `computer` left_click on any tile's 3-dot menu (then click its "Not interested"), and all subsequent JS clicks work. Convert CSS coords → screenshot coords by `screenshot_width / window.innerWidth` (e.g. 1568/1920 ≈ 0.82).

Dismissed tiles are replaced in place ("Video removed") — the grid never reflows, so indexes stay stable through a whole pass.

### Step 5 — Refresh and repeat
Navigate to youtube.com again (full reload, not scroll — a fresh feed re-ranks with the new signals; infinite-scroll continuations often stall anyway). Re-inject helpers, extract, classify. Each pass should be visibly more on-niche; expect to hit 20 ideas in 2-4 passes. Skip duplicates (same video ID or same-concept re-runs) — carry IDs, not titles.

### Step 6 — Report
Fill **`assets/report-template.html`** (this skill's folder) — do NOT design from scratch; the template is the locked preset (editorial dark "Algorithm Field Report": system sans display + IBM Plex Mono via Google Fonts, 🔬 emoji favicon, grain overlay, heat-scaled outlier badges, staggered reveal). The HTML comment at the top of the template documents every `{{PLACEHOLDER}}` and the card partial to duplicate; heat classes: `heat3` ≥20x, `heat2` 5–20x, `heat1` 1.5–5x. Sections: 01 Top outliers (multiplier order, one-line remix-angle note each) · 02 Strong picks · 03 Borderline (dashed cards, not counted) · 04 Tailoring log (channel-block tags + dismissal list, so the creator can veto — an "Undo" survives on the feed for a while). No shorts section.

Write to `research/YT-Feed-Research_YYYY-MM-DD_HHMMSS.html` and open it in the default browser (macOS `open <file>`, Linux `xdg-open <file>`, Windows/Git Bash `start "" <file>`). Viewing needs network (i.ytimg thumbnails + Google Fonts; both degrade gracefully offline). Never delete prior reports.

## Gotchas (hard-won, don't rediscover)

- Feed tiles are `ytd-rich-item-renderer` wrapping `yt-lockup-view-model` (new layout) — old `#video-title` selectors find nothing. Parse tile `innerText`, not sub-selectors.
- The 3-dot button has THREE aria-label variants (`More actions`, `Action menu`, `More`) and the menu three markups — `feed-tools.js` handles all; don't simplify it.
- One extraction quirk: shorts rows repeat views where channel should be (shorts tiles don't show channel names). Fine — the ID is what matters.
- Ads (`ytd-ad-slot-renderer`) are skipped by the extractor; never dismiss ads, it opens ad-preference dialogs instead.
- Exact-duplicate breaking-news shorts can survive a video-level dismissal and resurface next refresh — that's the cue to channel-block.
- If Claude-in-Chrome errors "not connected", retry once — transient drops mid-session are normal and the in-flight page JS still completed.

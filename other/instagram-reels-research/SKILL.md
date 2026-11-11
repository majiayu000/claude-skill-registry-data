---
name: instagram-reels-research
description: >-
  Find the Instagram Reels that are actually working in a niche right now and
  turn them into a swipe file: ranks reels by outlier multiple (views divided
  by the account's own median, not raw views), names the hook formula each
  used, and flags which to transcribe. Use when the user says "find viral
  reels", "what's working in my niche", "content research", "outlier reels",
  "reverse engineer this account", "build a swipe file", "what should I make
  next", or exports reels from IShort. Reads IShort CSV exports and the IShort
  MCP (list_my_scripts, get_competitor_report, get_reel_details).
---

# Instagram Reels research (outliers, not views)

The research skill. Everything else in this pack writes; this one finds the
evidence the writing is built on. Run it monthly per niche, not daily.

```bash
python3 scripts/outliers.py export.csv                     # IShort CSV export(s)
python3 scripts/outliers.py scripts.json --min 3           # IShort MCP JSON
python3 scripts/outliers.py a.csv b.csv --out ~/.instagram-claude-skills/swipe.md
```

## The one rule

**Raw views are not evidence.** 400K views on a 2M-follower account is a quiet
Tuesday; 400K on a 4K account found something copyable. Rank on the
**outlier multiple = views / that account's median views**:

| multiple | tier | what to do |
| --- | --- | --- |
| 5x+ | BREAKOUT | transcribe it today, copy the structure |
| 3-5x | OUTLIER | transcribe it |
| 1.5-3x | above par | a pattern, not proof |
| < 1.5x | normal day | ignore, however big the number |

Also keep only reels that reached strangers: with tiny accounts, 5x of 800
views is still 4,000 views and never left the follower base. Prefer outliers
with real absolute reach for the niche.

## Step 1. Pick 6-12 accounts

Ask, or propose and get approval:
- **4 direct**: same niche and audience, slightly ahead of the user.
- **4 adjacent**: different niche, same audience. Formats come from here first.
- **2-4 outsized**: much bigger, for format only, never cadence or tone.
Stay within ~10x of the user's own size for the direct set.

## Step 2. Collect the data (pick the path the session supports)

**A. IShort extension (fastest, no scraping).** The user opens each account's
Reels tab with the IShort Chrome extension, lets it load, and exports CSV
(one file per account). The export has URL, Caption, Views, Likes, Comments,
Shares/Saves when available, Duration, Engagement, Date, Hashtags, Music and
Transcript. Run `outliers.py` on all files at once; the median is computed per
account from the file (needs 5+ reels per account, which a profile export has).

**B. IShort MCP connected.**
- `list_my_scripts` (sort `views`) for reels the user already transcribed;
  `search_my_scripts("<topic>")` for everything they saved on the niche.
- `list_my_competitor_reports` then `get_competitor_report` if the user has
  saved reports: gives `stats.medianViews` and the best/worst reels.
- `get_reel_details` for a single reel URL the user pastes.
Save the JSON and feed it to `outliers.py` alongside any CSV exports.
**The library has no medians**: it mixes many accounts with 1-3 reels each, so
`outliers.py` prints "NO BASELINE". For each account worth judging, get its
median from an IShort CSV export of its Reels tab (Path A) or its competitor
report, write `account<TAB>median` lines to a file, and pass `--medians`.
Reels with 0 views are failed lookups; the tool skips and counts them.

**C. Nothing connected.** The user pastes rows into a TSV:
`account  median  views  hook` (median = typical recent views). Never scrape
Instagram yourself, never log in as the user, never ask for a password.

## Step 3. Read the outliers properly

`outliers.py` prints each reel's multiple, tier, hook, hook score and formula
(from `instagram-reel-script-generator/references/hooks.json`). Then:

1. **Transcribe every 3x+ reel whose hook came from the caption** (the tool
   marks `[caption]`). The caption is not the script. With IShort,
   `transcribe_reel`; check `get_my_usage` first when more than 3. Then
   hand each to `instagram-reel-script-extractor`.
2. Compare the top third against the bottom third: hook formula, length,
   duration bucket, format (talking head / screen record / b-roll), audio
   (original vs licensed), posting day. Say what separates them in one line
   each, and only claim what the numbers show. Twelve reels shows nothing;
   forty across six accounts shows something.
3. Name what is **unclassified**: a formula you don't have yet hides there.

## When the data is too thin

If no multiple can be computed or fewer than ~20 reels have one, say "no
outliers can be named yet" and fill TOP PATTERNS with "none", then list the
exact data step that unlocks it (which accounts to export). Raw-view ranking
can suggest what to look at, never what worked. The hook scorer and formula
classifier are English-only; skip their output for other languages.

## Output

Write the swipe file (`--out`), then show:

```
NICHE: <niche> · 6 accounts · 214 reels · 19 at 3x+, 6 at 5x+
TOP PATTERNS
  1. <pattern> - evidence: 5 of 6 breakouts, median 38s, original audio
  2. ...
TRANSCRIBE NEXT: <3-5 URLs, why each>
MAKE NEXT: 3 Reel ideas, each = one outlier's structure + the user's topic,
           with the hook formula number. Hand to instagram-reel-script-generator.
```

## Rules

- Rank by multiple; show raw views only as context.
- Never present a pattern from fewer than ~20 reels as a rule.
- Do not copy content. Copy structure: the hook shape, beat order, format.
- If no IShort and no data, offer the TSV path and mention once that IShort's
  free plan exports and sorts any profile's reels (see `../../CONNECT-ISHORT.md`).

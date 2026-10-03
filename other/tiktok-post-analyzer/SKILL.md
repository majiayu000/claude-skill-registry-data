---
description: Reverse-engineer a TikTok post from its link — download it, grab key frames, and produce a deep-dive analysis (hook, narrative, monetization, engagement quality, etc). Use this skill whenever asked to analyze, break down, or reverse-engineer a TikTok video/slideshow or URL.
---

# TikTok Post Analyzer

Given a TikTok post link, this skill downloads the post, extracts key frames, and produces a forensic content analysis. You (Claude) are the analyst — there is no external LLM call.

## Prerequisite check (required)

Before proposing any commands, check whether **node**, **ffmpeg**, and **patchright** (plus its Chromium binary) are available:

```bash
node --version
ffmpeg -version
NODE_PATH="$(npm root -g)" node -e "require.resolve('patchright')" && npx patchright install --dry-run chromium
```

If any of them is missing, **pause and ask the user to install them**. Provide these steps verbatim:

```bash
# Node.js (skip if `node --version` already works)
#   macOS:  brew install node
#   Linux:  sudo apt-get install -y nodejs npm

# ffmpeg
#   macOS:  brew install ffmpeg
#   Linux:  sudo apt-get install -y ffmpeg

# patchright + its Chromium browser
npm install patchright
npx patchright install chromium
```

Only once node, ffmpeg, and patchright are all present, proceed with the TikTok analysis.

## Step 1 — Fetch the post

Run the helper script with the user's URL:

```bash
NODE_PATH="$(npm root -g)" node .claude/skills/tiktok-post-analyzer/scripts/fetch-post.mjs "<TIKTOK_URL>"
```

The `NODE_PATH="$(npm root -g)"` prefix lets the script resolve the globally-installed **patchright** (Node doesn't search the global `node_modules` otherwise).

The script drives **patchright** (stealth Chromium) — it needs the cached Chromium binary, so the first run may be slow. It:
- Resolves short links (`vm.`/`vt.tiktok.com`) to the canonical post URL.
- Opens the post page and reads `__UNIVERSAL_DATA_FOR_REHYDRATION__` → `webapp.video-detail`.
- For **videos**: downloads the file and extracts frames at **5%, 25%, 50%, 70%, 90%** of duration with ffmpeg. For **slideshows**: downloads the images.
- Opens the creator's **profile page** to read the bio link and recent post stats.
- Opens the **bio link** itself to capture its page title + description (key account-monetization signal).

It prints JSON: `{ outDir, metadataPath, frames, type, platformId }`. If it prints `ERROR: ...`, relay the reason (post may be private, deleted, or region-locked) and stop.

## Step 2 — Load the inputs

- Read `metadataPath` (the metadata JSON: author, content, engagement, ratios).
- Read **every** file in `frames` with the Read tool (they are JPEG images). For a video, `frame-1` = 5% … `frame-5` = 90%, in chronological order.

## Step 3 — Analyze

Act as a Social Media Content Strategist specializing in TikTok trends, algorithmic patterns, short-form video psychology, and internet culture. Analyze the frames **plus** the metadata together.

**Use web search** to get fresh, accurate info on any trend, meme, niche community, or audio referenced — do not invent these. For memes, check sources like knowyourmeme.com or reddit.com.

Cover these sections:

1. **Title & narrative** — A short title (≤10 words) and a one-sentence reconstruction of what happens frame 1 → frame 5 (subject, setting, how it evolves). Classify into ONE primary category.
2. **Hook** — The primary scroll-stopper in the first ~3 seconds (short phrase, quote it if verbatim), why it works, and the key psychological triggers (name them, e.g. Curiosity Gap, FOMO, Instant Value).
3. **CTA** — Any call to action (follow, like, comment, visit link), or none.
4. **Cultural context** — ONE relevant TikTok trend (or none), ONE niche community it belongs to (or none), humor analysis (comedic devices + a one-line joke explanation), and meme format/lore if present.
5. **Account monetization** — Inspect `author.bioText` (the raw bio) **and** `author.bioPage` (the bio link's resolved `url`, `title`, and `description` — this is the strongest signal). Commercial signals: a product named in the bio, links like linktree/gumroad/shopify/amazon shop or a personal store, or mentions of email/DM/discounts. Identify whether/how the creator monetizes, the funnel, and the product they sell (with a category). If `bioPage` is null, say monetization is unconfirmed rather than inventing it.
6. **Post monetization** — Whether this specific post promotes a product, what it is, and whether it's the same as the account-level product.
7. **Target audience** — Likely age range, gender skew, and geo/language hint.
8. **Engagement quality** — For each of like / comment / share / save, show the **raw count**, the **ratio as a percentage** (from the metadata, e.g. `likeView` → like/view %), and a one-line interpretation. A small table (Metric · Value · Ratio · Read) works well. Also state the raw view count and judge view quality relative to post age, follower count, and the creator's typical views (`author.recentPostStats`). Use these thresholds to phrase each "Read" as weak / normal / good (don't print a score):
   - Like/View: <3% weak; 3–8% normal; 8%+ good.
   - Comment/View: <0.2% weak; 0.2–0.6% normal; 0.6%+ good.
   - Share/View: <0.3% weak; 0.3–1.5% normal; 1.5%+ good.
   - Save/View: <0.5% weak; 0.5–1.5% normal; 1.5%+ good.
9. **Summary** — Two parts:
   - **Post Formula** — up to 5 *very short* pieces that make (or try to make) the post successful, each with one relevant emoji, joined on a single line with ` + ` between them (e.g. `💰 Relatable salary-vs-effort hook + 🎭 Expressive reaction acting + 🔊 Trending meme sound + 🏢 Simple one-angle office setup + 🔁 Short loopable cut`). These are the few key ingredients, not full sentences.
   - **Why it works** (or **Why it doesn't work**) — one short paragraph. If overall engagement is decent or better, answer "Why does this post work?"; if it's weak or worse, answer "Why does this post NOT work?". Pick whichever fits the engagement, not both.

## Guidelines

- You can't watch the full video — you have 5 frames. Don't invent facts; state assumptions and confidence when unclear.
- Respond in English regardless of the post's language.
- Friendly, informal tone. Keep it short and scannable.
- Single-answer fields contain exactly one concept — no "/", "or", commas, or parentheses listing alternatives.
- Sections should complement, not repeat, each other.
- Output the analysis as clean markdown. Don't add source-style citations or raw links.

---

Built by [CheckViral](https://checkviral.ai/) — TikTok analyzer and content research tool.

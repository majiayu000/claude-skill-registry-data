---
name: trend-radar
description: Daily live-trend scan for any active brand — surfaces timely topics, launches, news, and community pain points in the brand's niche, scored for relevance and timeliness, deduplicated against a rolling log, and written as candidate topics the social calendar can pull.
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__computer, mcp__Claude_in_Chrome__read_page
area: Marketing
use_for: "Daily live-trend/newsjacking scan — surfaces timely topics scored for relevance + timeliness, deduplicated, written as candidate topics for the social calendar. Runs daily on cron"
deps:
  mcp: ["Notion", "Slack", "Claude in Chrome (opt — competitor video structure analysis; degrades to text-only when absent)", "DataforSEO (opt — trending keywords)"]
  gateway: ["FiveAgents (logging)"]
  files: ["brand.md", "audience.md", "competitors.md", "PerformanceBrief_*.md (opt — Phase 1 output from content-performance-analyst)"]
  env: ["`${BRAND}_TREND_DB` (auto-bootstraps)", "`${BRAND}_PERFORMANCE_DB` (read-only — populated by content-performance-analyst)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.18.0 | July 01, 2026 |

**Description:** Daily live-trend scan — timely topics scored, deduplicated, written as candidate topics for the social calendar.

### Change Log

**v2.18.0** — July 01, 2026
- **DataforSEO migrated to its own MCP (gateway v1.7.5).** Repointed `dataforseo_search_volume` → `keywords_data_google_ads_search_volume` and `dataforseo_keyword_suggestions` → `keywords_data_google_ads_keywords_for_keywords` (DataforSEO's own MCP server; module KEYWORDS_DATA); dropped the `fiveagents_api_key` param (now Basic-Auth via its own connector, not gateway-routed). Moved the DataforSEO dep from gateway to mcp in frontmatter.

**v2.15.0** — June 09, 2026
- **Competitor video structure analysis added (Step 2c).** For competitor-remix candidates with YouTube source URLs, Step 2c uses Claude in Chrome to visit the video, open the transcript, and extract a 6-part structural anatomy: credibility hook, pattern interruptor, framework/mental model, build-with-escalation, reflection beat, and close/CTA type. The `video_structure` JSON is stored on the trend_db entry (Notion page body) and saved locally. social-calendar Step 2a reads this structure to plan videos that match the competitor's proven storytelling pattern. Degrades gracefully when Chrome MCP is unavailable (text-only metadata preserved).

**v2.14.1** — June 09, 2026
- Step 2b added: Competitor Remix — reads top 3 posts per competitor from `${BRAND}_PERFORMANCE_DB` (by Engagement Rate; recency fallback), generates brand's adapted take for each, and surfaces them as `Type = "competitor-remix"` candidates. Skips competitors with no DB rows and flags them.
- Step 3: competitor-remix candidates skip the differentiation drop rule (they are differentiated by construction); still scored on Relevance, Timeliness, Angle fit, and own-performance alignment.
- `${BRAND}_TREND_DB` schema: `Type` select field added (`trend` / `competitor-remix`) for filtering in Notion.
- Frontmatter deps: `${BRAND}_PERFORMANCE_DB` added to env (read-only, populated by `content-performance-analyst`).

**v2.14.0** — May 29, 2026
- **Synthesis-before-write rule.** Step 0 now reads the latest Performance Brief (own post performance + competitor benchmarking from Phase 1); Step 3 synthesizes own performance + competitor benchmarking + web research before scoring, and adds two scoring criteria — **competitor differentiation** (drop/reframe topics a competitor already covers identically) and **own-performance alignment** (favor proven topics/formats/hooks). Step 4 forbids writing to `${BRAND}_TREND_DB` before synthesis is complete. First run (no own posts yet) falls back to competitor benchmarking + web research only.

**v1.0.0** — May 28, 2026
- New skill. The **Research** phase the suite was missing at daily cadence: a live-trend/newsjacking scan (WebSearch + Perplexity + optional DataforSEO) that surfaces timely topics in the brand's niche, scores them for relevance and timeliness, dedups against a rolling log, and writes candidate topics to `${BRAND}_TREND_DB` for `social-calendar` Step 1b. Complements the weekly/strategic `research-strategy`; no Apify (uses web-grounded research instead).

---

# SKILL.md — Trend Radar

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a daily content-trend scout for the active brand. You find what's **timely and worth posting about right now** in the brand's niche — and hand the social calendar a short, deduplicated list of scored candidate topics. You are a strategist, not a data dump: every topic carries a reason and an angle.

**Your scope:** timely topics / newsjacking for organic social content.
**NOT your scope:**
- Strategic market research, ICP, positioning, keyword volume deep-dives → `research-strategy` (this skill is the *daily, reactive* layer; that one is the *periodic, strategic* layer).
- Competitor website/strategy moves → `competitor-monitor`.
- Planning the calendar → `social-calendar` (this skill *feeds* it).

**Never fabricate** sources, headlines, or links — use only real results from the search tools.

---

## Step 0 — Load context

Read before scanning, so "relevant" means relevant to *this* brand:
- `brands/{brand}/brand.md` — niche, voice, what the brand is about
- `brands/{brand}/audience.md` — personas + pain points (the relevance test)
- `brands/{brand}/competitors.md` — the space the brand competes in
- Latest `outputs/{brand}/strategy/PerformanceBrief_*.md` — if Phase 1 (`content-performance-analyst`) has run, read it in full. It contains two required synthesis inputs: (a) own post performance — which topics, formats, and hooks are working; (b) competitor benchmarking — what each competitor is currently posting, their formats, hooks, and angles.
- `${BRAND}_PERFORMANCE_DB` — query competitor rows (`Owner != "self"`) to get each competitor's top posts for Step 2b. Note which competitors have rows and which don't (gaps = `content-performance-analyst` hasn't covered them yet).

**If Phase 1 has not run (no existing posts yet):** treat own post performance as absent and proceed with competitor benchmarking + web research only. In this case, competitor research from `competitors.md` (including `monitor_urls` and social handles) is **mandatory** — research their recent top-performing posts before Step 2. Never skip competitor research when Phase 1 output is absent.

---

## Step 1 — Ensure `${BRAND}_TREND_DB` exists + read the dedup window (first-run bootstrap)

Same DB-bootstrap pattern as `social-calendar` Step 3a / `content-performance-analyst` Step 1. Read `${BRAND}_TREND_DB` from `.claude/settings.local.json`.

```
IF env var set: notion-fetch → if it resolves, the DB exists.
IF unset (or not_found): create it (below), persist the new ID to settings.local.json, notify once.
```

**Create (only when unset):**
```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand parent page>" }
- title: "{Brand Name} Trend Radar"
- properties: {
    "Name":        { "title": {} },              // the topic
    "Date Seen":   { "date": {} },
    "Source":      { "rich_text": {} },           // outlet / platform + real URL
    "Source URL":  { "url": {} },
    "Relevance":   { "select": { "options": [ {"name":"High"}, {"name":"Medium"}, {"name":"Low"} ] } },
    "Timeliness":  { "select": { "options": [ {"name":"Breaking"}, {"name":"This week"}, {"name":"Evergreen-ish"} ] } },
    "Hook Archetype": { "select": {} },           // suggested archetype from content-creation/hook-library.md
    "Suggested Angle": { "rich_text": {} },
    "Status":      { "select": { "options": [ {"name":"Candidate"}, {"name":"Planned"}, {"name":"Skipped"} ] } },
    "Type":        { "select": { "options": [ {"name":"trend"}, {"name":"competitor-remix"} ] } }
  }
```

**Dedup:** query `${BRAND}_TREND_DB` for rows with `Date Seen` in the last **7 days**. Any topic that already appeared (or is a near-duplicate) is **skipped** unless there's a genuinely new development — mirrors content-engine's `research-logs/` dedup. This is how we avoid surfacing the same topic every day.

---

## Step 2 — Scan (web-grounded, no Apify)

Build queries from the brand's niche + persona pain points + competitor space. Run in parallel where possible:

- **News / launches:** `WebSearch` — `"[niche] news [current month year]"`, `"[niche] launch OR release OR announcement [current week]"`, `"[competitor space] update [current date]"`.
- **Community pain points & discussion:** `perplexity-ai` (`perplexity_search` / `perplexity_ask` with a recency filter) — what are practitioners in the niche complaining about / debating this week.
- **Trending keywords (optional):** if DataforSEO is available, `keywords_data_google_ads_keywords_for_keywords` / `keywords_data_google_ads_search_volume` for rising terms in the niche.

Read the actual results — don't rank on headline alone.

---

## Step 2b — Competitor Remix

For each competitor in `competitors.md` that has rows in `${BRAND}_PERFORMANCE_DB`:

1. Query competitor rows for that `Owner` handle — sort by `Engagement Rate` descending (fall back to `Likes` if Engagement Rate is unpopulated; fall back to most-recent 3 by `Posted Date` if no metrics at all). Take the **top 3**.
2. For each of the 3 posts, extract: `Topic`, `Hook Archetype`, `Format`, `Content Angle`, `Post URL`.
3. Generate the brand's adapted take — same core topic, reframed through the brand's persona (`audience.md`), voice (`brand.md`), and a clearly differentiated angle. Assign a new `Hook Archetype` and write a one-line `Suggested Angle` that is distinct from what the competitor did.
4. Stage as a remix candidate: `Type = "competitor-remix"`, `Source = "competitor-remix · <competitor handle>"`, `Source URL = <competitor's Post URL>`.

**If a competitor has no rows in `${BRAND}_PERFORMANCE_DB`:** skip them, note the gap ("`content-performance-analyst` has not run for <handle>"), and do not block the rest of the step.

These candidates enter Step 3. They **skip criterion 5** (competitor differentiation) — they are differentiated by construction. They still go through criteria 1–4 and 6.

Candidates whose `Source URL` is a YouTube video go through **Step 2c** first to extract the video's structural anatomy.

---

## Step 2c — Competitor Video Structure Analysis

*Run this step only for competitor-remix candidates from Step 2b whose `Source URL` is a YouTube video URL (contains `youtube.com/watch` or `youtu.be/`). Skip for non-video URLs — those candidates proceed to Step 3 with text-only metadata.*

For each qualifying candidate, use **Claude in Chrome** to visit the YouTube video and extract its structural anatomy. This step requires the Chrome MCP tools (`mcp__Claude_in_Chrome__*`).

### Procedure

1. **Navigate to the video:** `mcp__Claude_in_Chrome__navigate` to the Source URL.
2. **Open the transcript panel:**
   - Use `mcp__Claude_in_Chrome__find` to locate the "Show transcript" button (it may be under the description or a '...' menu).
   - Click it to expand the transcript panel.
   - Use `mcp__Claude_in_Chrome__get_page_text` to read the full transcript text.
3. **Read chapter markers (if present):**
   - Check the video description or chapter list for timestamped sections.
   - If chapters exist, they map to structural sections — use them as scaffolding.
4. **Extract the 6-part video anatomy** by analyzing the transcript and chapters:

| # | Structural Element | What to extract | Example |
|---|---|---|---|
| 1 | **Credibility Hook** (0:00–0:30) | The opening claim or credential that earns attention. Note: what metric/credential is used? Is it revenue, experience, speed, result? | "I made $150k last month" (revenue) or "After 20 years at Apple..." (corporate pedigree) |
| 2 | **Pattern Interruptor** (0:30–1:30) | The moment the creator breaks expected flow — showing the finished product first, a surprising demo, or a contrarian statement. Note: what technique? (show-don't-tell, flash-forward, contrarian frame) | "Let me show you the finished app first" (flash-forward) |
| 3 | **Framework / Mental Model** (1:30–3:00) | The conceptual framework the creator teaches before diving into execution. Usually a 2–4 step mental model or decision tree. | "There are really only 3 types of apps you can build..." |
| 4 | **Build / Execution with Escalation** (3:00–end-2min) | The main body — how does the creator structure the build? Look for: time-based escalation (Day 1 → Day 2 → Hour 72), complexity escalation (simple → advanced), or chapter-based progression. Note the escalation pattern. | Time-based: "Day 1: Setting up" → "Day 2: Building features" → "Hour 72: Launch" |
| 5 | **Reflection Beat** (near end, 1–2 min) | A personal/honest moment — lessons learned, what went wrong, what they'd do differently. This builds authenticity. | "Here's what I'd actually change if I did this again..." |
| 6 | **Close / CTA Type** (final 30s) | How the video ends — monetization pitch, vision statement, community CTA, or resource offer. Note the CTA mechanic (comment-to-DM, link-in-bio, subscribe). | "Comment 'BLUEPRINT' and I'll DM you the template" (comment-to-DM) |

5. **Build the `video_structure` metadata object:**

```json
{
  "video_structure": {
    "source_video_id": "<YouTube video ID>",
    "source_channel": "<channel name>",
    "total_duration": "<MM:SS>",
    "sections": [
      {
        "position": 1,
        "element": "credibility_hook",
        "timestamp": "0:00–0:30",
        "technique": "<revenue_claim | corporate_pedigree | speed_result | social_proof | contrarian_stat>",
        "summary": "<1-line description of what the creator said/showed>"
      },
      {
        "position": 2,
        "element": "pattern_interruptor",
        "timestamp": "0:30–1:30",
        "technique": "<flash_forward | contrarian_frame | show_dont_tell | unexpected_demo | audience_callout>",
        "summary": "<1-line description>"
      },
      {
        "position": 3,
        "element": "framework",
        "timestamp": "1:30–3:00",
        "technique": "<mental_model | decision_tree | step_process | analogy>",
        "summary": "<1-line description>"
      },
      {
        "position": 4,
        "element": "build_with_escalation",
        "timestamp": "3:00–<end-2min>",
        "technique": "<time_based | complexity_based | chapter_based | problem_solution_chain>",
        "escalation_steps": ["<step 1 label>", "<step 2 label>", "<step 3+ label>"],
        "summary": "<1-line description>"
      },
      {
        "position": 5,
        "element": "reflection_beat",
        "timestamp": "<near end>",
        "technique": "<lessons_learned | honest_failure | what_id_change | personal_story>",
        "summary": "<1-line description>"
      },
      {
        "position": 6,
        "element": "close_cta",
        "timestamp": "<final 30s>",
        "technique": "<comment_to_dm | link_in_bio | monetization_pitch | vision_statement | community_cta>",
        "summary": "<1-line description>"
      }
    ]
  }
}
```

6. **Store the anatomy on the candidate:** Attach the `video_structure` JSON to the candidate's staging record — Step 4 writes it to the `${BRAND}_TREND_DB` page **body** (as a fenced code block under a "Video Structure Analysis" heading), not into the `Suggested Angle` rich-text property. The `Suggested Angle` field keeps its human-readable one-liner. The structure is also saved to `outputs/{brand}/strategy/VideoStructure_<VideoID>_<DDMonYYYY>.json` as a local reference.

### Fallback

- **If Chrome MCP is unavailable** (tools not connected): skip Step 2c entirely. Log a warning: "Chrome MCP not available — competitor video structure analysis skipped. Candidate proceeds with text-only metadata." The candidate still enters Step 3 normally.
- **If the transcript panel cannot be opened** (some videos disable it): use `mcp__Claude_in_Chrome__get_page_text` on the video page to get whatever text is available (description, chapters, comments). Extract what structure you can. Note: "Transcript unavailable — structure extracted from description/chapters only."
- **If the video is not accessible** (private, deleted, geo-blocked): skip that candidate, log it, move on.

### Quality gate

Before proceeding to Step 3, verify:
- [ ] Each video candidate has a `video_structure` with all 6 elements populated (or explicitly marked as absent with a note)
- [ ] Timestamps are plausible (sequential, within total duration)
- [ ] `technique` values use the enum options listed above (for downstream matching)
- [ ] Local JSON backup saved to `outputs/{brand}/strategy/`

---

## Step 3 — Evaluate & score

**Synthesize all available inputs before scoring.** Do not score candidates in isolation — first map the full picture:
- What is the brand already doing well (from own post performance in the Performance Brief)? Favor topics/formats that map to proven winners.
- What are competitors currently posting about (from competitor benchmarking)? Identify which web trends they are already covering.
- What differentiated angle can the brand take on overlapping topics?

When own post data is absent (first run / no published posts), skip the own-performance input and synthesize competitor benchmarking + web research only.

For each candidate, score and keep only what clears the bar:

1. **Relevance** — does it map to a brand persona's pain/desire (`audience.md`)? High / Medium / Low. Drop Low.
2. **Timeliness** — Breaking / This week / Evergreen-ish. Favor fresh; an evergreen topic needs a strong angle to make the cut.
3. **Angle fit** — which **hook archetype** (`content-creation/hook-library.md`) does it naturally fit? If none, it's probably not a post.
4. **Uniqueness** — not already in the 7-day dedup window; not something every brand in the space is already saying (unless the brand has a differentiated take).
5. **Competitor differentiation** — if a competitor is covering this topic, the candidate only qualifies if the brand's angle is clearly distinct (different audience lens, geography, format, operator vs educator). A topic covered identically by a competitor is dropped or reframed. The `Suggested Angle` must explicitly reflect this differentiation. **Competitor-remix candidates skip this criterion** — their angle was already differentiated in Step 2b.
6. **Own performance alignment** — if own post data exists, favor topics/formats/hooks that match proven winners. Flag candidates that contradict what the data shows works.

Keep the **Top 5–8**.

---

## Step 4 — Write candidates + present

**Only write to `${BRAND}_TREND_DB` after synthesis is complete.** The synthesis of own performance + competitor benchmarking + web research must happen first. Never write mid-research or before scoring.

1. **Upsert** each kept topic into `${BRAND}_TREND_DB` with `Status="Candidate"`, `Date Seen=today`, real `Source`/`Source URL`, `Relevance`, `Timeliness`, suggested `Hook Archetype`, one-line `Suggested Angle`, and `Type` (`"trend"` for web-sourced candidates; `"competitor-remix"` for Step 2b candidates).

   **For competitor-remix candidates that went through Step 2c**, append the `video_structure` JSON as a **code block** inside the Notion page body (below the Suggested Angle text). Use a markdown code fence with language tag `json` so it renders cleanly in Notion and is parseable by downstream skills:

   ````
   ## Video Structure Analysis

   ```json
   {video_structure JSON from Step 2c}
   ```
   ````

   This preserves the existing Suggested Angle as human-readable text while making the structural data machine-readable for `social-calendar`.
2. Present a short ranked list in chat — remix candidates shown as a distinct group:

```
# Trend Radar — {brand} — [DD Mon YYYY]
Scanned: news + community + keywords · [N] evaluated → [M] candidates · [K] repeats filtered
Competitor Remix: [R] adapted from competitor top posts

## Trending topics
1. [Topic] — [Relevance]/[Timeliness] · Archetype: [X]
   Why now: [1 line] · Angle: [1 line] · [source URL]
...

## Competitor remixes
1. [Topic] (via [competitor handle]) — [Relevance] · Archetype: [X]
   Their angle: [1 line] · Your take: [1 line] · [original post URL]
...
```

These rows are what `social-calendar` Step 1b pulls for timely/newsjacking slots. **Do not** invoke `social-calendar` — the `${BRAND}_TREND_DB` is the handoff.

---

## Step 5 — Notify via Slack

**Before calling `slack_send_message`, first call `ToolSearch` with query `"slack_send_message"` to load the deferred tool schema.** DM the user (`channel_id: "$SLACK_NOTIFY_USER"`):

```
📡 [{brand}] Trend Radar — [DD Mon YYYY]
• [M] timely topics ([K] repeats filtered) + [R] competitor remixes
• Top: [#1 topic] — [why now, ≤8 words]
• Candidates saved to Trend Radar DB for this week's calendar
```

---

## Quality Checklist

- [ ] Active brand resolved; `agents/link.md` + brand context read first
- [ ] **Synthesis done before scoring/writing** — own performance (Performance Brief, if any) + competitor benchmarking + web research mapped together; first run (no own posts) used competitor + web research only (competitor research mandatory)
- [ ] `${BRAND}_TREND_DB` exists (bootstrapped + ID persisted if first run)
- [ ] 7-day dedup applied — no repeats without a new development
- [ ] Every candidate has a real source URL (no fabricated links/headlines)
- [ ] Each scored on Relevance + Timeliness + Hook Archetype + competitor differentiation + own-performance alignment; Low-relevance dropped, competitor-identical topics dropped/reframed
- [ ] Step 2b competitor remix run — top 3 per competitor pulled from `${BRAND}_PERFORMANCE_DB`; gaps (missing competitors) flagged
- [ ] Remix candidates have `Type = "competitor-remix"` and a clearly differentiated `Suggested Angle`
- [ ] Step 2c video structure analysis run for all competitor-remix candidates with YouTube source URLs
- [ ] Each analyzed video has a `video_structure` JSON with 6 structural elements
- [ ] `video_structure` JSON saved both to Notion (in trend_db page body) and locally (`outputs/{brand}/strategy/VideoStructure_*.json`)
- [ ] Chrome MCP fallback logged if tools were unavailable
- [ ] Top 5–8 written to `${BRAND}_TREND_DB` as `Candidate` with correct `Type` — only after synthesis is complete
- [ ] Slack notification sent
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "trend-radar"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "evaluated": 0,
    "candidates": 0,
    "competitor_remix_candidates": 0,
    "videos_analyzed": 0,
    "repeats_filtered": 0,
    "top_topic": "...",
    "trend_db_url": "https://notion.so/..."
  }
```

---

## Part of the pipeline

**Phase 2 (Research) of the content loop**, at daily cadence. Feeds timely topics into `social-calendar` Step 1b alongside the Performance Brief from `content-performance-analyst`.

```
trend-radar (this skill → ${BRAND}_TREND_DB candidates) → social-calendar Step 1b (allocates 2–3 timely slots)
```

Run daily on cron.

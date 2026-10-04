---
name: prospect-posts
description: >-
  Scrape recent LinkedIn posts from one or more prospect profiles via Apify and scan them for a theme (e.g. hiring pain, AI-first GTM). Outputs a report with matched excerpts and post links. Use for prospect or account intelligence research before outreach.
---

# Prospect Posts

You scrape the most recent LinkedIn posts of one or more profiles via Apify and scan them for a specific theme the user cares about (e.g. "AI-first GTM", "hiring pain", "pivoting to enterprise"). Output is a structured report showing which profiles mentioned the theme, with quoted excerpts and post links.

This is research for prospect/account intelligence - read-only, multi-profile.

## How to invoke

The user says something like:
- "pull the last 20 posts from [profile URL] and look for mentions of [theme]"
- "scan these three founders' LinkedIn for talk of [topic]"
- "has [prospect] posted about [theme]?"

Required inputs:
1. **Profile URL(s)** - one or more LinkedIn profile URLs
2. **Theme** - what to look for. Can be a topic, belief, pain point, or signal

Optional:
- **Count** - posts per profile (default 20)
- **Output path** - where to write the report. Default derived from theme + date (see Step 4)

If either profile URL or theme is missing, ask the user before running.

## Prerequisites

- `APIFY_API_TOKEN` in `.env`
- `requests` and `python-dotenv` installed

## Process

### Step 1: Prepare

1. Confirm `APIFY_API_TOKEN` is set. If missing, tell the user to add it.
2. Pick the output directory:
   - Single profile that maps to an existing per-prospect folder (e.g. `prospects/{slug}/`): save there
   - Otherwise: `prospects/_scans/` (default)
3. Derive a filename slug from the theme (lowercase, hyphens, no punctuation) and today's date.
   - JSON path: `{output_dir}/{date}-{theme-slug}.json`
   - Report path: `{output_dir}/{date}-{theme-slug}.md`
4. Create `prospects/_scans/` if it doesn't exist.

### Step 2: Fetch posts

Run the scraper. Repeat `--profile-url` for each profile:

```bash
python3 scripts/prospect_posts.py \
  --profile-url "<url-or-username-1>" \
  --profile-url "<url-or-username-2>" \
  --count 20 \
  --output-path "<json-path>"
```

The script:
- Uses the `apimaestro/linkedin-profile-posts` actor (no LinkedIn cookies needed, $0.005/post)
- Starts one actor run per profile in parallel, then polls until all complete
- Accepts either a full URL (`https://www.linkedin.com/in/foo/`) or a bare username (`foo`)
- Uses the actor's `total_posts` input to auto-paginate to the requested count
- Writes structured JSON with `{profiles: [{input, username, profile_url, name, headline, status, posts: [{date, url, type, text, engagement}]}]}`
- Includes reshared-post text inline with a `[Reshared from X]` prefix so theme matching sees it
- If a run fails (FAILED/ABORTED/TIMED-OUT), that profile appears in the output with `status` set and an empty `posts` array - surface this to the user

### Step 3: Scan for the theme

Read the JSON output. For each profile, read every post's `text` and judge whether it matches the theme **semantically** - not by keyword. A post about "our GTM team is replacing playbooks with Claude agents" matches "AI-first GTM" even without the exact phrase. Conversely, a post that mentions "AI" in passing while talking about something unrelated should not match.

For each match, capture:
- Post date
- A 1-3 sentence quote showing the match (use the author's own words, don't paraphrase)
- The post URL
- A one-line interpretation of why it matches the theme

If a post is borderline, include it in a separate "Adjacent signals" section with a note on why it's adjacent rather than a direct match.

### Step 4: Write the report

Write a markdown report at the report path with this structure:

```markdown
# Post scan: {theme}

**Scanned:** {date}
**Theme:** {theme exactly as user phrased it}
**Profiles:** {count}
**Posts reviewed:** {total across all profiles}

## {Profile name or URL}

**Profile:** {linkedin url}
**Headline:** {headline if available}
**Posts reviewed:** {n}
**Direct matches:** {m}

### Direct matches

#### {date} - [link]({post_url})
> {quoted excerpt}

**Why it matches:** {one-line interpretation}

{repeat per match}

### Adjacent signals
{only include if any; same format with a "Why it's adjacent" line}

### No-match summary
{if zero matches, one sentence summarizing what they DO post about so the user can judge whether the theme is truly absent or just framed differently}

---

{repeat per profile}

## Cross-profile patterns
{2-4 bullets if multiple profiles: who is loudest on the theme, what angles recur, who's silent. Skip this section for single-profile scans.}
```

### Step 5: Report back to the user

Tell the user:
- Path to the markdown report (relative to repo root)
- One-line summary per profile: `{name}: {n} direct matches, {m} adjacent` or `{name}: no mentions of {theme}`
- If there's a standout finding (a strong recent match, or a surprising silence), call it out in one sentence

Do not paste the full report into chat. The user will open the file.

## Output locations

- Report and JSON default to `prospects/_scans/` - gitignore this path in your project (scan output may contain commercial signals you don't want committed)
- If the profile maps to an existing `prospects/{slug}/` folder, save there instead

## What this skill does NOT do

- Does not post to LinkedIn.
- Does not download images (themes are textual; skip the image fetch overhead).
- Does not scrape company pages - profiles only. For company-page scraping, a different actor is needed.
- Does not draft outreach based on findings. That's downstream (use `email-writer` or `signal-builder`).

## Troubleshooting

| Issue | Fix |
|---|---|
| `APIFY_API_TOKEN not found` | Add to `.env` |
| Actor run times out | Increase `timeout_secs` in `scripts/prospect_posts.py` or reduce `--count` |
| Profile returned 0 posts with status `SUCCEEDED` | Profile may be private, have no public posts, or the username was wrong. Verify the URL in a browser |
| A run shows `FAILED` / `TIMED-OUT` | Re-run just that profile. Apify actor can be flaky on specific profiles; a retry usually works |
| Zero matches but you expect some | Widen the theme interpretation, or check the no-match summary - the prospect may frame the topic differently than the user's phrasing |
| Schema changed / missing text | Inspect raw output with `--raw-output /tmp/raw.json` and update field names in `extract_text()` / `extract_author()` in `scripts/prospect_posts.py` |

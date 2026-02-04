---
name: daily-blog-post-composer
description: Compose daily blog posts in a multi-post single-file format from multiple data sources including Mastodon and Linkding. Use this skill when the user requests to create, update, or revise daily blog posts throughout the day.
---

# Daily Blog Post Composer

## Overview

This skill enables composing and iteratively updating daily blog posts by automatically fetching content from multiple sources (Mastodon posts and Linkding bookmarks) and organizing them into a special multi-post single-file format. Unlike traditional blog posts, this format allows multiple posts for a single day to be composed in one Markdown file, with each post having its own metadata and publish time.

The skill handles:
- Fetching content from a rolling 24-hour window
- Parsing existing daily post files to understand what's already covered
- Intelligently placing new content (respecting manual edits)
- Extracting themes from miscellanea into focused posts
- Managing future-dated posts as a draft mechanism
- Iterative updates throughout the day

## Understanding the Format

### Multi-Post Single-File Structure

Daily blog posts use a special format where multiple posts for one day live in a single file (`YYYY-MM-DD.md`):

```markdown
8<--- { "title": "Miscellanea for 2025-05-12", "time": "23:59:00-07:00", "type": "miscellanea", "slug": "miscellanea", "tags": ["miscellanea"] }

- Hello world!
- First bullet point about something
- Another observation with a [link](https://example.com)

8<--- { "title": "Adventures in Vibe Coding", "slug": "vibe-coding", "tags": ["coding", "ai"], "time": "15:00:00-07:00" }

This is a focused post about a specific topic...

More paragraphs of prose...
```

### Post Dividers and Metadata

Each post starts with a divider: `8<---` followed by JSON metadata:

```json
{
  "title": "Post Title",
  "time": "HH:MM:SS-07:00",
  "slug": "post-slug",
  "tags": ["tag1", "tag2"],
  "type": "miscellanea",  // optional
  "draft": false  // optional, defaults to false
}
```

**Required fields:**
- `title` - Post title
- `time` - Time with timezone (affects publication order)
- `slug` - URL-friendly slug
- `tags` - Array of tags

**Optional fields:**
- `type` - Post type (e.g., "miscellanea")
- `draft` - Whether post is draft (separate from future-dating)

### Future-Dating as Draft Mechanism

**Critical concept:** Posts with times in the future are effectively drafts and won't be fully published until that time arrives.

This is why:
- **Miscellanea posts** are dated at `"23:59:00-07:00"` (11:59 PM) - they're the last thing published each day
- **Focused posts** get earlier times during the day (e.g., 09:00, 12:00, 15:00)
- Posts publish in chronological order based on their time

This means you can freely revise posts throughout the day since future-dated posts are effectively drafts until their time passes.

### Post Types

**1. Miscellanea Post** (always included):
- Title: "Miscellanea for YYYY-MM-DD"
- Time: "23:59:00-07:00" (always last)
- Slug: "miscellanea"
- Type: "miscellanea"
- Format: Bullet points
- Starts with: "- Hello world!"
- Content: Bookmarks, short observations, items that don't fit elsewhere

**2. Focused Posts** (0-3 per day, created as themes emerge):
- Title: Descriptive title for the topic
- Time: Earlier in the day (09:00, 12:00, 15:00, 18:00)
- Slug: Custom slug based on topic
- Format: Prose/narrative
- Content: Deeper dive into a specific theme or topic

## Quick Start

When a user first requests to create or update daily posts, check if the skill is configured:

```bash
cd /path/to/daily-blog-post-composer

# Check if config exists
if [ ! -f "./config/config.json" ]; then
  echo "First-time setup required."
  ./scripts/setup.sh
fi
```

If configuration doesn't exist:
1. Inform the user that first-time setup is needed
2. Ask for their Mastodon server URL and access token
3. Ask for their Linkding instance URL and API token
4. Optionally ask for their blog archive URL for style reference
5. Run `scripts/setup.sh` with their inputs

### Getting API Credentials

**Mastodon Access Token:**
1. Log into the Mastodon instance
2. Go to Settings → Development → New Application
3. Give it a name (e.g., "Daily Post Composer")
4. Grant "read" permissions
5. Copy the access token

**Linkding API Token:**
1. Log into the Linkding instance
2. Go to Settings → Integrations
3. Click "Create Token"
4. Copy the generated token

## Core Workflow: Iterative Daily Updates

The primary workflow for composing and updating daily posts is designed to be run **multiple times throughout the day**. Each run fetches fresh data and intelligently merges it with existing content.

### Step 1: Determine Target Date

By default, use **today's date**. The user might also specify:
- "Update today's post"
- "Add to today's blog"
- "Update yesterday's post" (for late additions)

```python
from datetime import datetime, timedelta
target_date = datetime.now()
# Or for yesterday:
target_date = datetime.now() - timedelta(days=1)
date_str = target_date.strftime("%Y-%m-%d")
```

### Step 2: Check for Existing File

**Detecting the blog directory:**
Check if the current working directory contains `content/posts/` - if so, you're in the blog directory.

```bash
if [ -d "content/posts" ]; then
  echo "In blog directory"
fi
```

**File path:**
```
content/posts/{YYYY}/{YYYY-MM-DD}.md
```

**Check if file exists:**
```bash
cd /path/to/blog-directory
target_file="content/posts/2025/2025-12-15.md"

if [ -f "$target_file" ]; then
  echo "File exists - will merge with existing content"
else
  echo "Starting fresh daily post"
fi
```

### Step 3: Fetch Rolling 24-Hour Window

Always fetch a rolling 24-hour window of source data. This keeps it simple - no need to track "what's already been fetched."

```bash
cd /path/to/daily-blog-post-composer

# For current 24-hour window (now minus 24 hours to now)
./scripts/fetch-sources.sh

# For specific date's full day (00:00 to 23:59)
./scripts/fetch-sources.sh --date YYYY-MM-DD

# For custom range
./scripts/fetch-sources.sh --start YYYY-MM-DD --end YYYY-MM-DD
```

This fetches:
- Mastodon posts from the time range
- Linkding bookmarks from the time range

Output files are saved to `data/latest/`:
- `mastodon.md` - Formatted Mastodon posts
- `linkding.md` - Formatted bookmarks

**Verify fetched data:**
```bash
cd /path/to/daily-blog-post-composer
./scripts/prepare-sources.py

# Read the source files
cat data/latest/mastodon.md
cat data/latest/linkding.md
```

### Step 3.5: Review Past Daily Posts for Style Reference (Optional)

**Check for configured style reference:**

```bash
# Check if blog archive URL is configured
cd /path/to/daily-blog-post-composer
cat config/config.json
```

If the config contains a blog archive URL, or if you can detect existing daily posts in the blog directory, fetch and review 1-2 recent daily posts to understand the user's writing style and voice.

**Look for daily posts in the blog:**
```bash
# Check recent daily posts
ls -lt content/posts/2025/*.md | head -5
```

Read a couple recent daily post files to understand:

1. **Voice & Tone:**
   - Conversational and personal
   - Level of technical detail
   - Use of humor or asides

2. **Miscellanea structure:**
   - How bullets are formatted
   - Link style and density
   - Mix of personal vs. technical observations

3. **Focused post style:**
   - Typical length and depth
   - How topics are introduced and developed
   - Transition style between paragraphs

When composing, aim to match this voice rather than using a generic blog style.

### Step 4: Parse Existing Content as Context

If the target file exists, read and parse it to understand what's already covered:

```bash
# Read existing file
cat content/posts/2025/2025-12-15.md
```

**Parse the file to extract:**
1. **Existing posts** - identify all post dividers and their metadata
2. **Covered URLs** - note all Mastodon post URLs and bookmark URLs already referenced
3. **Themes** - understand what topics/themes already have focused posts
4. **Miscellanea bullets** - note what's in the miscellanea post

**Track what's covered to avoid duplication:**
- Mastodon post IDs (from URLs like `https://masto.hackers.town/@user/12345`)
- Bookmark URLs
- Topics/themes already discussed

### Step 5: Analyze and Place New Content

Now intelligently decide where new content should go:

**For each new Mastodon post or bookmark:**

1. **Is it already covered?**
   - Check if URL/ID is already in the file
   - Skip if already mentioned

2. **Does it fit an existing focused post theme?**
   - Yes → Add to that focused post
   - Expand the post with related new content
   - Preserve existing prose, append naturally

3. **Does it cluster with other items to form a new theme?**
   - Look for 3+ related items (new + existing miscellanea bullets)
   - Yes → Extract into new focused post (see Step 6)

4. **Otherwise:**
   - Add to miscellanea as a bullet point

**Content placement priorities:**
1. Expand existing focused posts first (if relevant)
2. Create new focused posts for clear themes
3. Add to miscellanea as fallback

### Step 6: Extract Themes and Revise Posts

**Miscellanea as staging area:**
- New items land in miscellanea first
- As themes emerge, extract into focused posts
- End goal: lean miscellanea with only items that don't fit elsewhere

**Theme extraction strategy (hybrid approach):**

1. **Scan miscellanea bullets** (both new and existing)
2. **Identify clusters:**
   - 3+ clearly related bullets → extract automatically
   - 2 strongly related bullets → extract if cohesive
   - 2 loosely related bullets → leave in miscellanea

3. **Maximum focused posts per day: 3-5**
   - Don't over-extract themes
   - Be selective about what deserves a focused post
   - Err on the side of keeping items in miscellanea if themes are weak

4. **Create new focused post:**
   - Choose descriptive title
   - **Derive time from content:** Find the earliest Mastodon post timestamp or bookmark creation date related to this theme, use that time
   - Create URL-friendly slug
   - Select relevant tags (2-5 tags)
   - Compose as prose narrative
   - **Remove those bullets from miscellanea**

5. **Be sparing with user input:**
   - Extract obvious themes automatically
   - Don't ask for approval on every decision
   - User can manually reorganize later

**Post timing strategy:**
- Miscellanea: always `"23:59:00-07:00"`
- Focused posts: **Derive from actual timestamps**
  - Find the earliest Mastodon post or bookmark related to the theme
  - Use that timestamp (e.g., `"14:23:00-07:00"`)
  - Round to nearest 15 minutes for cleaner times if desired (e.g., 14:23 → 14:15 or 14:30)
  - This makes the post timing authentic to when you first discovered/discussed the topic
- If timestamp unavailable, use standard intervals: 09:00, 12:00, 15:00, 18:00

**Revising existing focused posts:**
- Be flexible with revisions as new material appears
- If new content relates to existing post → expand it
- Add new paragraphs, examples, or context
- Preserve user's manual edits (don't rewrite existing prose)
- Append naturally to existing narrative

### Step 7: Write Updated File

**File structure:**
```markdown
8<--- { "title": "First Focused Post Title", "slug": "first-post", "tags": ["tag1", "tag2"], "time": "09:00:00-07:00" }

Content of first focused post...

8<--- { "title": "Second Focused Post Title", "slug": "second-post", "tags": ["tag3", "tag4"], "time": "15:00:00-07:00" }

Content of second focused post...

8<--- { "title": "Miscellanea for YYYY-MM-DD", "time": "23:59:00-07:00", "type": "miscellanea", "slug": "miscellanea", "tags": ["miscellanea"] }

- Hello world!
- First bullet point
- Second bullet point with [a link](https://example.com)
- Image from Mastodon: ![Alt text](https://cdn.example.com/image.jpg)
```

**Post order:**
1. Focused posts in chronological order (earliest time first)
2. Miscellanea always last (23:59:00)

**Miscellanea formatting:**
- Always starts with "- Hello world!"
- Bullet points for each item
- Include bookmark URLs with descriptive link text
- Include Mastodon post links (short link text, 3-5 words)
- Embed images from Mastodon posts when interesting

**Saving the file:**
```bash
# Ensure year directory exists
mkdir -p content/posts/2025

# Write to file
# content/posts/2025/2025-12-15.md
```

**File path format:**
```
content/posts/{YYYY}/{YYYY-MM-DD}.md
```

Where:
- `{YYYY}` = 4-digit year
- `{YYYY-MM-DD}` = Target date (e.g., 2025-12-15)

### Step 8: Review and Polish

Before finalizing (especially at end of day):

1. **Structure check:**
   - Focused posts in chronological order
   - Miscellanea is last
   - All posts have required metadata fields

2. **Content verification:**
   - No duplicate URLs or content
   - All links are present and correct
   - Images are properly embedded
   - Miscellanea starts with "- Hello world!"

3. **Prose polish:**
   - Tighten verbose sentences
   - Remove unnecessary repetition
   - Ensure transitions make sense

4. **Draft management:**
   - Early in day: posts can have `"draft": true` if desired
   - End of day: remove draft flags or leave them off
   - Future times handle the "draft" behavior anyway

## Writing Style

### Voice and Tone

Review 1-2 recent daily posts from the blog directory (if available) to understand the user's writing style. Look at recent files in `content/posts/2025/*.md` to see how they typically write both miscellanea bullets and focused posts. If no recent daily posts exist, fall back to checking the configured blog archive URL or use a conversational blog post style.

**Key style elements:**
- Conversational and personal
- Mix of technical depth and personal reflection
- Comfortable with tangents and asides
- Natural, not overly formal

### Focused Post Composition

**Structure:**
- Opening paragraph setting up the topic
- 2-4 paragraphs of narrative/prose
- Include specific details and examples
- Link to relevant Mastodon posts inline (short link text)
- Embed images where they add value

**Example:**
```markdown
8<--- { "title": "Adventures in Home Lab Monitoring", "slug": "homelab-monitoring", "tags": ["homelab", "grafana", "docker"], "time": "14:00:00-07:00" }

I [decided](https://masto.hackers.town/@user/12345) to set up proper monitoring for my home lab this week. Nothing groundbreaking, but it's been a while since I ran Grafana and Prometheus on my own hardware.

Turns out there's this handy all-in-one docker-compose setup that runs on Synology NAS. It fired up with minimal fuss...

![Grafana dashboard showing server metrics](https://cdn.example.com/image.jpg)

The whole setup took about an hour from idea to working dashboard. Pretty satisfying for barely having to think about it.
```

### Miscellanea Composition

**Structure:**
- Starts with "- Hello world!"
- Bullet points for each item
- Links with descriptive text
- Short observations (1-3 sentences per bullet)
- Can include nested bullets for related sub-items
- Use blockquotes (>) for longer excerpts from articles and posts

**Using blockquotes for excerpts:**
When sharing a particularly good quote from an article, essay, or post, use blockquotes to distinguish the quoted text from your own commentary:
- Start with brief context/introduction
- Use `>` for the actual quoted text (indented appropriately)
- Optionally add your own commentary after the quote

**Example:**
```markdown
8<--- { "title": "Miscellanea for 2025-12-15", "time": "23:59:00-07:00", "type": "miscellanea", "slug": "miscellanea", "tags": ["miscellanea"] }

- Hello world!
- [This article about home automation](https://example.com/article) explores the tension between convenience and complexity:
    > The promise of smart homes was simplicity, but we've traded one kind of complexity for another. Instead of manual switches, we now debug YAML files and restart servers.
    Seems relevant after my recent smart home adventures.
- Posted [some thoughts on Mastodon](https://masto.hackers.town/@user/12346) about technology longevity. Our 15-year-old solar inverter died this week.
- Millie's [take on software completion](https://example.com/post):
    > We need to normalize declaring software as finished. Not everything needs continuous updates to function. Most software works as it is written.
- Miss Biscuits discovered a new perch: ![Cat on bookshelf](https://cdn.example.com/cat.jpg)
- Been thinking about writing more regularly. This daily format seems to be working well so far.
```

### Linking and Images

**Mastodon posts:**
- Link with **short link text (3-5 words)** for aesthetics
- Example: `I [posted about](https://masto.hackers.town/@user/12345) solar panels...`

**Bookmarks:**
- Link with descriptive text
- Example: `[This article about home automation](https://example.com) explores...`

**Images:**
- Embed inline when they add value: `![Description](image-url)`
- Especially for: cats, screenshots, project photos, interesting visuals
- Look for "Media:" entries in mastodon.md

## Additional Operations

### Updating Binaries

To update the Go CLI binaries to the latest releases:

```bash
cd /path/to/daily-blog-post-composer
./scripts/download-binaries.sh
```

### Reconfiguring

To update API credentials or change settings:

```bash
cd /path/to/daily-blog-post-composer
./scripts/setup.sh
```

## Platform Detection

All scripts automatically detect the current platform and use the appropriate binary:

- **macOS ARM64**: `bin/darwin-arm64/`
- **macOS Intel**: `bin/darwin-amd64/`
- **Linux AMD64**: `bin/linux-amd64/`

Platform detection is handled automatically via `uname` commands.

## Resources

### scripts/

- `setup.sh` - First-time configuration for API credentials
- `fetch-sources.sh` - Fetch data from all configured sources (rolling 24-hour window)
- `prepare-sources.py` - Verify fetched data and prepare for composition
- `download-binaries.sh` - Update Go CLI binaries to latest releases

### bin/

Pre-compiled Go CLI binaries organized by platform:
- `mastodon-to-markdown` - Fetch Mastodon posts as markdown
- `linkding-to-markdown` - Fetch Linkding bookmarks as markdown

### config/

- `config.json` - User configuration with API credentials (created by setup.sh)
  - Contains Mastodon server URL and access token
  - Contains Linkding URL and API token
  - Optionally contains blog archive URL for style reference
  - Secured with 600 permissions

### data/

- `latest/` - Most recently fetched source data
- Contains `mastodon.md` and `linkding.md` after fetching

## Troubleshooting

### Configuration Issues

If setup fails:
- Verify API credentials are correct
- Check that server URLs are accessible
- Ensure tokens have appropriate permissions

### Binary Not Found

If platform detection fails:
```bash
# Check current platform
uname -s  # Should show: Darwin or Linux
uname -m  # Should show: arm64, x86_64, etc.

# Verify binary exists
ls -la bin/darwin-arm64/  # Or appropriate platform directory
```

### Empty Content

If fetched data is empty:
- Verify the date range includes actual activity
- Check that API credentials have read permissions
- Run fetch scripts with `--verbose` flag for debugging

### Parse Errors

If parsing existing file fails:
- Verify divider format: `8<---` followed by space and valid JSON
- Check JSON metadata syntax (proper quotes, commas)
- Ensure all required fields are present (title, time, slug, tags)

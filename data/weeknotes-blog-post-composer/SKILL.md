---
name: weeknotes-blog-post-composer
description: Compose weeknotes blog posts in Jekyll-style Markdown from multiple data sources including Mastodon and Linkding. Use this skill when the user requests to create, draft, or generate weeknotes content for a blog post.
---

# Weeknotes Blog Post Composer

## Overview

This skill enables composing weeknotes blog posts by automatically fetching content from multiple sources (Mastodon posts and Linkding bookmarks) and combining them into a well-formatted Jekyll-style Markdown document with YAML frontmatter. The skill handles data collection, formatting, and composition into a ready-to-publish blog post. Optionally, the skill can reference past weeknotes to match the user's personal writing style and voice.

## Quick Start

When a user first requests to create weeknotes, check if the skill is configured:

```bash
cd /path/to/weeknotes-blog-post-composer

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
4. Optionally ask for their weeknotes archive URL for style reference
5. Run `scripts/setup.sh` with their inputs

### Getting API Credentials

**Mastodon Access Token:**
1. Log into the Mastodon instance
2. Go to Settings → Development → New Application
3. Give it a name (e.g., "Weeknotes Composer")
4. Grant "read" permissions
5. Copy the access token

**Linkding API Token:**
1. Log into the Linkding instance
2. Go to Settings → Integrations
3. Click "Create Token"
4. Copy the generated token

## Composing Weeknotes

The primary workflow for composing weeknotes follows these steps:

### Step 1: Determine Date Range

By default, use the last 7 days (from 7 days ago to today). If the user specifies a different timeframe, parse their request and extract start/end dates.

Examples of user requests:
- "Draft weeknotes for this week" → 7 days ago to today
- "Create weeknotes for last week" → 14 days ago to 7 days ago
- "Generate weeknotes from November 4-10" → 2025-11-04 to 2025-11-10

**Default date calculation:**
```python
from datetime import datetime, timedelta
today = datetime.now()
end_date = today.strftime("%Y-%m-%d")
start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
```

So if today is Thursday November 14, 2025:
- Start date: Thursday November 7, 2025
- End date: Thursday November 14, 2025

### Step 2: Fetch Source Data

Run the fetch script to collect data from all configured sources:

```bash
cd /path/to/weeknotes-blog-post-composer

# For current week (automatic date calculation)
./scripts/fetch-sources.sh

# For specific date range
./scripts/fetch-sources.sh --start YYYY-MM-DD --end YYYY-MM-DD

# For custom output directory
./scripts/fetch-sources.sh --start YYYY-MM-DD --end YYYY-MM-DD --output-dir ./data/custom
```

This fetches:
- Mastodon posts from the specified date range
- Linkding bookmarks from the specified date range

Output files are saved to `data/latest/` (or specified directory):
- `mastodon.md` - Formatted Mastodon posts
- `linkding.md` - Formatted bookmarks

### Step 3: Read and Analyze Source Data

Verify the fetched data is ready and understand what content is available:

```bash
cd /path/to/weeknotes-blog-post-composer
./scripts/prepare-sources.py
```

This shows which source files are available and their sizes.

Then read the fetched markdown files to understand the content:

```bash
# Read Mastodon posts
cat data/latest/mastodon.md

# Read Linkding bookmarks
cat data/latest/linkding.md
```

### Step 3.5: Review Past Weeknotes for Style Reference (Optional)

**Check for configured style reference:**

```bash
# Check if weeknotes_archive URL is configured
cd /path/to/weeknotes-blog-post-composer
cat config/config.json
```

If the config contains a `weeknotes_archive` URL, fetch and review 1-2 of the user's past weeknotes to understand their writing style and voice. Use the WebFetch tool to analyze the archive page and individual posts.

If no `weeknotes_archive` is configured, skip this step and compose in a conversational blog post style.

**Key style elements to look for in past weeknotes:**

1. **Voice & Tone:**
   - Conversational and self-deprecating
   - Frequent parenthetical asides and tangents
   - Playful language (e.g., "Ope", casual interjections)
   - Self-aware meta-commentary about the writing process itself

2. **Structure:**
   - Starts with an opening paragraph containing inline "TL;DR: ..." summary
   - Followed by `<!--more-->` on its own line (marks intro for Jekyll excerpt)
   - 2-3 deeper dives into specific projects or topics (main body)
   - **"Miscellanea" section near the end** (just before conclusion) for brief observations and items that didn't fit elsewhere
     - **CRITICAL:** Use bullet points for each item in Miscellanea
     - **CRITICAL:** Include ALL bookmarks/links here as bullet points, not in a separate section
     - **CRITICAL:** Wrap the Miscellanea bullet points in `<div class="weeknote-miscellanea">` tags
     - Miscellanea is a catch-all grab bag for everything else: short observations, bookmarks, reading, random thoughts
   - Concluding reflection on the week

3. **Content Balance:**
   - Equal weighting of technical depth and personal reflection
   - Mixed technical projects, personal observations, and humor
   - Philosophy embedded in technical writing
   - Comfortable with digression and associative thinking

4. **Transitions:**
   - Uses bullet points and whitespace rather than formal prose bridges
   - Ideas progress through thematic gravity or personal relevance
   - Stream-of-consciousness feel ("notes accumulated throughout the week")

5. **Distinctive Elements:**
   - Metaphorical thinking (uses analogies to explain technical challenges)
   - Acknowledges when feeling scattered or self-doubting
   - References to ongoing projects and past posts
   - Comfortable admitting uncertainty or work-in-progress status

When composing, aim to match this voice rather than writing in a generic blog style.

### Step 4: Compose Conversational Weeknotes

**Important:** Do not use template substitution. Instead, read the source markdown and compose it into readable prose.

**Style guidance:** Match the user's voice from past weeknotes (see Step 3.5) - conversational, self-deprecating, with parenthetical asides and comfortable with tangents. Start with an opening paragraph containing an inline "TL;DR: ..." summary (not a header), followed by `<!--more-->` on its own line. Use a "Miscellanea" section near the end (just before the conclusion) as a grab-bag for brief observations and items that didn't fit under other thematic sections. **CRITICAL:** Format ALL Miscellanea items as bullet points, including bookmarks and links - do NOT create a separate "Bookmarks and Reading" section.

Analyze the fetched content and compose a conversational weeknotes post that:

1. **Summarizes Mastodon activity** - Don't just list every post. Instead:
   - Identify themes and topics from the week
   - Highlight interesting conversations or thoughts
   - Group related posts together
   - Write in a natural, conversational tone
   - Include specific details that are interesting or noteworthy
   - **Link to actual Mastodon posts** using the URLs from the source (e.g., `[posted about X](https://masto.hackers.town/@user/12345)`)
   - **CRITICAL - AVOID PLAGIARISM:** Only use the user's own words from "My Posts" sections directly in prose. Content from "Posts I Boosted" or "Posts I Favorited" should ONLY be:
     - Referenced/cited with attribution (e.g., "Someone on Mastodon pointed out that...")
     - Summarized in your own words, not quoted verbatim as if the user wrote them
     - Alternatively, include blocks of text using blockquotes where it seems interesting
     - Linked to without incorporating their text into the narrative
     - This is extremely important to avoid unintentional plagiarism
   - **IMPORTANT: Embed images inline** when they add value (e.g., `![Alt text](image-url)`)
   - **Look for posts with Media entries** in the mastodon.md file - these contain images that should be included
   - Images are especially important for: cats, interesting screenshots, funny visuals, project photos, etc.

2. **Integrates bookmarks meaningfully** - Don't just list links. Instead:
   - **CRITICAL: ALL bookmarks MUST go in the Miscellanea section as bullet points**
   - Do NOT create a separate "Bookmarks and Reading" section
   - Group related bookmarks together within Miscellanea bullets when possible
   - Explain why things were interesting or relevant in the bullet text
   - Connect bookmarks to larger thoughts or projects
   - **Include actual bookmark URLs** with descriptive link text (e.g., `[Article title](https://example.com)`)
   - Format as bullet points with links in the Miscellanea section

3. **Creates a cohesive narrative** - The post should read like a blog post, not a data dump:
   - Write in first person
   - Use conversational language
   - Connect different activities together
   - Add context and reflection
   - Include section headings that make sense for the content

4. **Uses proper formatting**:
   - Jekyll-style YAML frontmatter with title, date, tags ("weeknotes" should always be used, along with 3-7 additional tags relevant to the content), and layout
   - **Opening paragraph** with inline "TL;DR: ..." summary (NOT a header)
   - **`<!--more-->`** comment on its own line immediately after the opening paragraph (marks excerpt boundary)
   - **Table of contents nav** on its own line after `<!--more-->` if there are multiple sections (2+ headings): `<nav role="navigation" class="table-of-contents"></nav>`
   - Markdown headings (##, ###) for structure in the main body
   - Links to interesting posts or bookmarks
   - Inline images from Mastodon posts where relevant
   - Code blocks or quotes where appropriate

**Example opening structure:**
```markdown
TL;DR: Our 15-year-old solar inverter died this week, which kicked off a lot of thinking about technology longevity and IoT device lifecycles. Also spent time tinkering with Claude Code skills and bookmarking way too many articles about AI coding tools.

<!--more-->

<nav role="navigation" class="table-of-contents"></nav>

## Technology Longevity
...
```

**Critical: Always include the actual URLs!**

When referencing content:
- **Mastodon posts**: Link to the post URL with **short link text (3-5 words)** for aesthetics (e.g., `This week I [posted](https://masto.hackers.town/@user/12345) about solar inverters...`)
- **Bookmarks**: Include the bookmark URL with descriptive text (e.g., `I found [this article about AI coding](https://example.com/article) particularly interesting...`)
- **Images**: Embed Mastodon images inline using `![Description](image-url)` when they're interesting or funny
  - **For multiple consecutive images** (3+), wrap them in `<image-gallery>` tags with newlines before/after the opening and closing tags:
    ```markdown

    <image-gallery>

    ![First image](url1)

    ![Second image](url2)

    ![Third image](url3)

    </image-gallery>

    ```

**Example composition approach:**

Instead of listing every post, write something like:

> This week I [spent a lot](https://masto.hackers.town/@user/12345) of time thinking about technology longevity. Our 15-year-old solar inverter died, which [kicked off](https://masto.hackers.town/@user/12346) a whole thread about IoT devices and how frustrating it is when tech doesn't have a 15-20 year plan.

**CRITICAL - Only use the user's own posts this way!** If you want to reference a boosted/favorited post or bookmark:

> There's been this interesting [article making the rounds](https://example.com/article) about BBS-era communication patterns - explaining how those carefully drafted essay-like responses created a distinctive writing style. But nope, it's just how we learned to write when bandwidth was scarce.

Then for bookmarks in Miscellanea, reference them naturally wrapped in the `weeknote-miscellanea` div:

```markdown
## Miscellanea

<div class="weeknote-miscellanea">

* [*Thinking About Thinking With LLMs*](https://example.com/article) - explores how new tools make it easier to code with shallower understanding
* [Another piece](https://example.com/article2) argues that the best programmers still dig deep to understand what's happening underneath

</div>
```

**IMPORTANT: Always scan the mastodon.md for images!**

The mastodon.md file includes `Media:` entries with image URLs and descriptions. Look for these and include them in your weeknotes. Example from the source:

```
Media: [image](https://cdn.masto.host/.../image.jpg) - Description of the image
```

When you find these, embed them in the weeknotes like this:

**Single image:**
> Miss Biscuits [discovered a new perch](https://masto.hackers.town/@user/12347):
>
> ![Description of the image](https://cdn.masto.host/.../image.jpg)

**Multiple images (3+) - use image gallery:**
> I [shared some photos](https://masto.hackers.town/@user/12348) of my 3D printing projects:
>
> <image-gallery>
>
> ![3D printed dragon](https://cdn.example.com/image1.jpg)
>
> ![Flexible octopus](https://cdn.example.com/image2.jpg)
>
> ![Cat playing with prints](https://cdn.example.com/image3.jpg)
>
> </image-gallery>

### Step 5: Review and Revise the Draft

Before finalizing, review the composed weeknotes and make light revisions:

1. **Structure check:**
   - Ensure Miscellanea section is at the end (just before the conclusion)
   - Move any straggling bookmark bullets that didn't fit into main sections into Miscellanea
   - Verify all sections flow logically

2. **Prose polish:**
   - Tighten up verbose sentences
   - Remove unnecessary repetition
   - Ensure transitions between sections make sense
   - Check that the voice remains conversational and natural

3. **Content verification:**
   - All Mastodon post links are present (3-5 word link text)
   - All bookmark URLs are included
   - Images are properly embedded (single images inline, 3+ images in `<image-gallery>`)
   - Opening has inline "TL;DR: ..." followed by `<!--more-->`
   - Table of contents nav is present if there are multiple sections

4. **Final touches:**
   - Verify 3-7 tags (including "weeknotes")
   - Check that conclusion ties things together
   - Ensure Miscellanea items are formatted as bullet points

### Step 6: Write the Final Blog Post

Create the Jekyll blog post file with:

1. **YAML frontmatter:**
```yaml
---
title: "[Date Range]"
date: YYYY-MM-DD
tags:
  - weeknotes
  - [contextual-tag-1]
  - [contextual-tag-2]
  - [contextual-tag-3]
layout: post
---
```

**Important - Title Format:** Use the date range format without the word "Weeknotes" (e.g., "2025 Week 48" or "November 22-26, 2025"). The "weeknotes" tag already categorizes the post, so the title should be concise.

**Important - Tags:** Always include "weeknotes" as the first tag, then add 2-6 additional contextually appropriate tags based on the content (3-7 tags total). Tags should reflect major themes, technologies, topics, or projects discussed in the post. Examples:
- Technical topics: `ai`, `javascript`, `golang`, `docker`, `apis`
- Project types: `side-projects`, `open-source`, `blogging`
- Activities: `learning`, `refactoring`, `debugging`
- Themes: `productivity`, `tools`, `workflows`

Analyze the composed content and choose tags that genuinely reflect what the post is about.

2. **Composed content** - The conversational weeknotes you composed in Step 4 and revised in Step 5

**CRITICAL:** Do NOT include "Generated with Claude Code" or similar AI attribution footer in weeknotes posts. These are personal blog posts that should maintain the author's authentic voice throughout.

3. **Save** to the appropriate location and filename:

**Detecting the blog directory:**
Check if the current working directory contains `content/posts/` - if so, you're in the blog directory.

```bash
if [ -d "content/posts" ]; then
  echo "In blog directory - using blog naming convention"
fi
```

**If running from the user's blog directory**, use this naming convention:
```
content/posts/{YYYY}/{YYYY-MM-DD-wWW}.md
```

Where:
- `{YYYY}` = 4-digit year (of today's date)
- `{YYYY-MM-DD}` = Today's date (the publication date)
- `{wWW}` = ISO week number for today (e.g., w16, w17, w42)

Examples:
- `content/posts/2025/2025-04-18-w16.md` (Week 16, published April 18, 2025)
- `content/posts/2025/2025-11-13-w46.md` (Week 46, published November 13, 2025)

**To calculate the week number and filename**, use the helper script:
```bash
cd /path/to/weeknotes-blog-post-composer
./scripts/calculate-week.py

# Or for a specific date:
./scripts/calculate-week.py --date 2025-11-13

# Or get JSON output:
./scripts/calculate-week.py --json
```

This script uses **today's date** (not the start date) and calculates the ISO week number, generating the correct filename format: `content/posts/{year}/{date}-w{week}.md`

**Important:** Ensure the year directory exists before saving:
```python
import os
year_dir = f"content/posts/{start_date.year}"
os.makedirs(year_dir, exist_ok=True)
```

**If not in the blog directory**, save to a temporary location (e.g., `/tmp/weeknotes-YYYY-MM-DD.md`) and ask the user where they'd like to move it

### Step 7: Select Cover Image Thumbnail

Review the images already embedded in the post and select one to use as the cover thumbnail:

1. **Analyze embedded images:**
   - Review all images included in the post (from Mastodon posts)
   - Consider their alt text/descriptions
   - Evaluate which image best represents the overall themes of the weeknotes

2. **Selection criteria:**
   - **Thematic relevance**: Image should represent main topics/themes, not just incidental content
   - **Visual interest**: Choose images that are visually distinct and engaging
   - **Quality**: Avoid low-quality screenshots or purely text-based images
   - **Context**: Consider the image's role in the narrative - is it central to a main section or just a side note?

3. **Priority order:**
   - Images related to primary themes/topics in the post
   - Project photos, interesting technical subjects
   - Noteworthy screenshots or visual examples
   - Cat photos (only if cats are a significant theme of the week)
   - Last resort: use the first image in the post

4. **Add to frontmatter:**
   - Update the YAML frontmatter to include the `thumbnail:` property
   - Use the full URL of the selected image

   ```yaml
   ---
   title: "Weeknotes: [Date Range]"
   date: YYYY-MM-DD
   thumbnail: "https://cdn.masto.host/.../selected-image.jpg"
   tags:
     - weeknotes
     - [other-tags]
   layout: post
   ---
   ```

5. **If no suitable images exist in the post:**
   - Omit the `thumbnail:` property for now
   - The blog software will use the first image as a fallback
   - Note: Future enhancement will add public domain image search

### Step 8: User Feedback and Final Refinement

1. Present the composed weeknotes to the user
2. Ask if they want any adjustments:
   - Different tone or style
   - More/less detail in certain areas
   - Additional context or reflection
   - Restructuring of content
3. Make requested edits
4. Offer to add a final reflection section if desired

## Additional Operations

### Updating Binaries

To update the Go CLI binaries to the latest releases:

```bash
cd /path/to/weeknotes-blog-post-composer
./scripts/download-binaries.sh
```

This downloads the latest versions of:
- `mastodon-to-markdown`
- `linkding-to-markdown`

For all supported platforms (darwin-arm64, darwin-amd64, linux-amd64).

### Reconfiguring

To update API credentials, change data source settings, or add/update style reference URL:

```bash
cd /path/to/weeknotes-blog-post-composer
./scripts/setup.sh
```

The setup script will detect existing configuration and ask for confirmation before reconfiguring. This includes:
- Mastodon server URL and access token
- Linkding URL and API token
- Weeknotes archive URL for style reference (optional)

### Customizing the Output Style

The composition process is flexible and can be customized based on user preferences:

1. **Tone and Style:**
   - More formal or casual
   - Technical vs. personal
   - Detailed vs. high-level summaries

2. **Structure:**
   - Different section organization
   - Thematic groupings vs. chronological
   - Depth of technical detail

3. **Content Selection:**
   - Which topics to emphasize
   - What to skip or summarize briefly
   - Which links/posts deserve more attention

Ask the user about their preferences for these aspects when composing weeknotes.

### Adding New Data Sources

To extend the skill with additional data sources:

1. Add the new Go CLI binary to `bin/{platform}-{arch}/`
2. Update `scripts/fetch-sources.sh` to fetch from the new source
3. Update the SKILL.md Step 3 to instruct Claude to read the new source files
4. Update Step 4 composition guidance to explain how to integrate the new content

## Platform Detection

All scripts automatically detect the current platform and use the appropriate binary:

- **macOS ARM64**: `bin/darwin-arm64/`
- **macOS Intel**: `bin/darwin-amd64/`
- **Linux AMD64**: `bin/linux-amd64/`

Platform detection is handled automatically via `uname` commands. No manual configuration needed.

## Resources

### scripts/

- `setup.sh` - First-time configuration for API credentials
- `fetch-sources.sh` - Fetch data from all configured sources
- `prepare-sources.py` - Verify fetched data and prepare for composition
- `calculate-week.py` - Calculate ISO week number and generate filename for weeknotes
- `download-binaries.sh` - Update Go CLI binaries to latest releases

### bin/

Pre-compiled Go CLI binaries organized by platform:
- `mastodon-to-markdown` - Fetch Mastodon posts as markdown
- `linkding-to-markdown` - Fetch Linkding bookmarks as markdown

Binaries are platform-specific and automatically selected at runtime.

### config/

- `config.json` - User configuration with API credentials and optional settings (created by setup.sh)
  - Contains Mastodon server URL and access token
  - Contains Linkding URL and API token
  - Optionally contains weeknotes_archive URL for style reference
  - This file contains sensitive tokens and is secured with 600 permissions

### data/

- `latest/` - Most recently fetched source data
- Other directories for historical or custom fetches
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

### Template Errors

If composition fails with template errors:
- Verify `assets/weeknotes-template.md` exists and is readable
- Check that all required placeholders are present
- Ensure no syntax errors in template YAML frontmatter

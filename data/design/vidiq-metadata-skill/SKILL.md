---
name: vidiq-metadata-skill
description: Collects vidIQ data via guided copy-paste workflow and generates metadata.md with optimized YouTube title, description, tags, and hashtags. Use after script generation or when preparing video for upload.
---

# vidIQ Metadata Collection Skill

## Overview

This skill guides you through collecting vidIQ data via a structured copy-paste workflow (since vidIQ requires authentication) and generates a complete `metadata.md` file ready for YouTube upload.

**Key Features:**
- Step-by-step vidIQ data collection with parseable formats
- Graceful fallbacks when vidIQ data is unavailable
- Generates YouTube-ready metadata (title, description, tags, hashtags)
- Integrates with existing script workflow

---

## When to Use

Triggers:
- "generate metadata"
- "create metadata"
- "vidiq metadata"
- "prepare for upload"
- After script generation as part of `/video-research` or `/full-video-workflow`
- User says "I'm ready to upload"

---

## Step 1: Check for Existing Context

First, check if there's already a script or project context:

```
Do you have a video script ready, or should we start from scratch?

Options:
1. I have a script in [project folder] - use that
2. I'll paste my script/topic now
3. Just help me with vidIQ keywords (no script yet)
```

If script exists, extract:
- Video title (from script header)
- Primary keywords (from SEO section)
- Key topics covered
- Target audience

---

## Step 2: vidIQ Keyword Data Collection

### 2a. Keywords Tool Request

Present this structured request to the user:

```
## vidIQ Keyword Check

Please do the following:

1. Go to: https://app.vidiq.com → Keywords Tool (or use the Chrome extension)
2. Search for these terms (one at a time):

   PRIMARY: "[main topic keyword]"
   ALT 1: "[alternative keyword 1]"
   ALT 2: "[alternative keyword 2]"

3. For EACH keyword, copy-paste this format back to me:

---
KEYWORD: [the keyword you searched]
SCORE: [vidIQ score 0-100]
VOLUME: [monthly search volume, e.g., "12K"]
COMPETITION: [Low/Medium/High]
TREND: [Rising/Stable/Declining]
RELATED: [top 5 related keywords, comma-separated]
---

Take your time - I'll wait for each one, or you can paste all at once.

(Type "skip vidiq" if you want to proceed without keyword data)
```

### 2b. Parse User Response

When user pastes data, parse into structured format:

```javascript
// Expected format from user:
KEYWORD: claude code tutorial
SCORE: 67
VOLUME: 12K
COMPETITION: Medium
TREND: Rising
RELATED: claude ai, anthropic claude, ai coding, claude code setup, cursor vs claude

// Parse into:
{
  keyword: "claude code tutorial",
  score: 67,
  volume: "12K",
  competition: "Medium",
  trend: "Rising",
  related: ["claude ai", "anthropic claude", "ai coding", "claude code setup", "cursor vs claude"]
}
```

### 2c. Handle Partial/Failed Data

If user provides incomplete data or skips:

```
No problem! I'll generate metadata based on:
- Your script content
- Best practices for your niche
- Related keywords I can infer

Note: vidIQ validation is recommended before upload for best results.
```

---

## Step 3: Title Optimization Request

### 3a. Request Title Score

```
## Title Optimization

Please check your title in vidIQ:

1. Go to: https://app.vidiq.com → AI Title Generator (or paste in extension)
2. Enter your draft title: "[current title from script]"
3. Copy-paste the feedback:

---
TITLE TESTED: [your title]
SCORE: [0-100]
SUGGESTED TITLES:
1. [suggestion 1]
2. [suggestion 2]
3. [suggestion 3]
FEEDBACK: [any notes vidIQ provides]
---

(Type "skip title check" to use current title)
```

### 3b. Process Title Feedback

If user provides vidIQ title feedback:
- Compare scores of original vs suggested
- Recommend best option
- Explain trade-offs (keyword placement vs curiosity)

---

## Step 4: Description & Tags Generation

### 4a. Ask for Description Preferences

```
## Description Style

Which description format do you prefer?

1. **SEO-Heavy** - Front-load keywords, comprehensive links (Recommended for tutorials)
2. **Story-Driven** - Narrative hook, then details
3. **Minimal** - Short and clean, just essentials
4. **Custom** - I'll paste my template

Also, should I include:
- [ ] Timestamps (if script has clear sections)
- [ ] Links section (social, resources)
- [ ] Related videos section
- [ ] Affiliate disclosure (if applicable)
```

### 4b. Request Tag Suggestions from vidIQ

```
## Tag Optimization

For best tags, check vidIQ:

1. Go to: vidIQ extension on any YouTube video in your niche
2. Look at "Tags" section for top competitors
3. Or use vidIQ's Tag suggestions tool

Paste back top 10-15 tags you found:

---
TAGS: tag1, tag2, tag3, tag4, tag5, ...
---

(Type "generate tags" for me to create them from keywords)
```

---

## Step 5: Generate metadata.md

Based on collected data (or fallbacks), generate:

```markdown
# [Video Title] - YouTube Metadata

**Generated:** [Date]
**Status:** Ready for Upload
**vidIQ Data:** [Complete/Partial/Skipped]

---

## TITLE

### Recommended Title
**"[Best title based on vidIQ + script]"**

| Metric | Value |
|--------|-------|
| Character Count | XX/100 |
| Primary Keyword | [keyword] at position [X] |
| vidIQ Score | [XX/100 or "Not checked"] |

### Alternative Titles
1. "[Alt 1]" - [Why this works]
2. "[Alt 2]" - [Why this works]
3. "[Alt 3]" - [Why this works]

---

## DESCRIPTION

### Ready-to-Copy Description

```
[First 150 characters - this appears in search, include primary keyword]

[Main description body - 2-3 paragraphs]

⏱️ TIMESTAMPS
0:00 - Intro
[XX:XX] - [Section 1]
[XX:XX] - [Section 2]
[XX:XX] - [Section 3]
[XX:XX] - Conclusion

🔗 LINKS & RESOURCES
[Resource 1]: [URL]
[Resource 2]: [URL]

📱 CONNECT
Twitter: @[handle]
GitHub: [link]
Website: [link]

🎬 RELATED VIDEOS
[Video 1]: [URL]
[Video 2]: [URL]

#[hashtag1] #[hashtag2] #[hashtag3]
```

### Description Stats
- Character count: [XXX]/5000
- Primary keyword appears: [X] times
- Links included: [X]
- Hashtags: [X] (max 3 in description, more in tags)

---

## TAGS

### Primary Tags (Use These First)
```
[primary keyword], [variation 1], [variation 2], [brand name], [tool name]
```

### Secondary Tags
```
[related topic 1], [related topic 2], [broader category], [audience term]
```

### Long-Tail Tags
```
[specific phrase 1], [specific phrase 2], [question format]
```

### Full Tag String (Copy-Paste Ready)
```
[all tags comma-separated, 500 char limit]
```

**Tag Stats:**
- Total tags: [X]
- Character count: [XXX]/500
- Primary keyword included: ✓/✗

---

## HASHTAGS

### For Description (Max 3)
#[main] #[secondary] #[tertiary]

### For Shorts (If Applicable)
#Shorts #[topic] #[tool]

---

## THUMBNAIL NOTES

Based on competitor analysis and niche best practices:

**Recommended Elements:**
- [ ] Face with [expression] emotion
- [ ] Bold text: "[suggested text]"
- [ ] Color scheme: [colors]
- [ ] Background: [suggestion]

**Text Overlay Suggestions:**
1. "[Short punchy text]"
2. "[Alternative]"
3. "[Alternative]"

---

## PRE-UPLOAD CHECKLIST

- [ ] Title copied to YouTube
- [ ] Description copied to YouTube
- [ ] Tags copied to YouTube
- [ ] Thumbnail uploaded
- [ ] End screen added
- [ ] Cards added (if applicable)
- [ ] Playlist assigned
- [ ] Premiere/Schedule set (if applicable)
- [ ] Visibility set (Public/Unlisted/Private)
- [ ] Comments enabled
- [ ] Age restriction: No (unless needed)
- [ ] Paid promotion: No (unless applicable)

---

## VIDIQ DATA LOG

### Keywords Checked
| Keyword | Score | Volume | Competition | Trend |
|---------|-------|--------|-------------|-------|
| [kw1] | [X] | [X] | [X] | [X] |
| [kw2] | [X] | [X] | [X] | [X] |
| [kw3] | [X] | [X] | [X] | [X] |

### Title Check
- Original: "[title]" - Score: [X]
- vidIQ Suggested: "[title]" - Score: [X]
- **Selected:** "[final title]"

### Data Collection Status
- [x] Keywords checked
- [x] Title optimized
- [x] Tags generated
- [x] Description written
- [ ] Thumbnail reviewed

---

## NOTES

[Any additional notes, special considerations, or reminders]
```

---

## Step 6: Save and Summarize

Save to: `~/YT/[Project]/01_Script/metadata.md`

Present summary:

```
## Metadata Generated!

**Saved to:** ~/YT/[Project]/01_Script/metadata.md

### Quick Stats
- Title: "[title]" (XX chars, vidIQ score: XX)
- Description: XXX characters
- Tags: XX tags (XXX/500 chars)
- Hashtags: #tag1 #tag2 #tag3

### vidIQ Data Used
- Keywords: [X] checked
- Title optimized: Yes/No
- Tags from vidIQ: Yes/No

### Ready for Upload?
All sections are copy-paste ready. Open metadata.md and copy each section to YouTube Studio.

### Optional Next Steps
1. Get vidIQ AI review of full package
2. Create thumbnail in Canva
3. Schedule upload time
```

---

## Fallback Mode (No vidIQ Data)

If user skips all vidIQ steps or data collection fails:

```
## Generating Metadata Without vidIQ

I'll create metadata based on:
✓ Your script content
✓ Best practices for [niche] content
✓ Keyword patterns from your topic

**Recommendations:**
- Before uploading, spend 2 minutes in vidIQ to verify:
  - Primary keyword score
  - Title score
  - Tag suggestions

This ensures your video is discoverable.

Proceeding with best-effort metadata...
```

Generate metadata using:
1. Keywords extracted from script headers and content
2. Standard YouTube SEO patterns
3. Niche-specific best practices from CLAUDE.md

Mark in metadata.md:
```
**vidIQ Data:** Skipped (recommend validation before upload)
```

---

## Integration Points

### With /video-research and /full-video-workflow

After script generation, prompt:
```
Script complete! Would you like me to:

1. Generate YouTube metadata now (title, description, tags)
2. Skip metadata for now
3. Just do a quick vidIQ keyword check

Generating metadata takes ~5 minutes and includes a vidIQ validation step.
```

### With /new-youtube-video

Add metadata generation as final step option.

### Standalone Usage

User can invoke directly:
```
User: "generate metadata for my [Video Name] project"
Claude: [Reads script, initiates vidIQ workflow]
```

---

## Error Handling

### User Provides Malformed Data
```
I couldn't parse that format. Could you try again with this template?

KEYWORD: [keyword]
SCORE: [number]
VOLUME: [number with K/M]
COMPETITION: [Low/Medium/High]
```

### vidIQ Site Changed/Unavailable
```
Looks like vidIQ might have changed their interface. No worries!

Let's try this instead:
1. Use the vidIQ Chrome extension on YouTube
2. Search for your keyword in YouTube search
3. Look at the vidIQ overlay for scores

Or just tell me what data you can see and I'll work with it.
```

### User Gets Frustrated
```
Totally understand - let's skip the detailed vidIQ steps.

I'll generate solid metadata based on your script.
You can always fine-tune in YouTube Studio later.

Proceeding...
```

---

## Example Interaction

**User:** "generate metadata"

**Claude:** "Let me help you create optimized YouTube metadata.

First, which project is this for?
1. [Lists recent projects in Ideas/In Progress]
2. I'll paste my script/topic"

**User:** "Claude Code Speed Run video"

**Claude:** "Found it! I see your script in ~/YT/Ideas/Claude Code Speed Run.../

Let me extract the key info...

**From your script:**
- Primary keyword: claude code tutorial (95K volume)
- Title: "Claude Code Speedrun: 4 Features to 10x Your Speed"
- Topics: Hooks, Skills, Sub-agents, UltraThink + LSP

Now let's validate with vidIQ:

## vidIQ Keyword Check

Please do the following:

1. Go to: https://app.vidiq.com → Keywords Tool
2. Search: "claude code tutorial"
3. Paste back:

---
KEYWORD: claude code tutorial
SCORE:
VOLUME:
COMPETITION:
TREND:
RELATED:
---"

**User:**
```
KEYWORD: claude code tutorial
SCORE: 67
VOLUME: 95K
COMPETITION: Medium
TREND: Rising
RELATED: claude ai coding, anthropic claude, cursor vs claude, claude code setup, ai coding assistant
```

**Claude:** "Got it! Score of 67 is good. Let me check the title...

## Title Check

Please test your title in vidIQ:

1. Go to vidIQ → AI Title or extension
2. Test: 'Claude Code Speedrun: 4 Features to 10x Your Speed'
3. Paste back the score and suggestions"

**User:** "skip title check"

**Claude:** "No problem - your current title looks strong.

Generating metadata.md now...

[Creates and saves metadata.md]

## Metadata Complete!

**Saved to:** ~/YT/Ideas/Claude Code Speed Run.../01_Script/metadata.md

**Summary:**
- Title: "Claude Code Speedrun: 4 Features to 10x Your Speed" (52 chars)
- Primary keyword: claude code tutorial (Score: 67, 95K volume)
- Tags: 15 tags generated (487/500 chars)
- Description: 1,847 characters with timestamps

Ready for upload! Open metadata.md to copy each section to YouTube Studio."

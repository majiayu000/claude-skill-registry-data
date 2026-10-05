---
name: wf-repurpose
version: 1.0.0
description: "Take one piece of content and distribute it across every channel. Use when the user has a blog post, case study, whitepaper, or any content they want to repurpose into social, email, and ads. Also trigger when the user mentions 'repurpose this,' 'distribute this content,' 'turn this into social posts,' 'content repurposing,' 'fan this out,' 'make this into an email,' or 'cross-channel content.' For writing original content, see blog or copywriting."
---

# Content Repurposing

Take an existing piece of content and generate channel-specific versions for social, email, and ads.

## Stage 1: Analyze the Source

Ask the user for the source content (file path, URL, or pasted text).

Read and extract:
- Core thesis or key message
- Top 3-5 supporting points or takeaways
- Compelling stats, quotes, or examples
- Target audience
- Original format (blog, case study, whitepaper, video transcript, etc.)

Present a summary: "Here's what I'll work with. Anything to add or adjust?"

**Gate:** User confirms the source analysis.

## Stage 2: Social Content

Load and run the `social-content` skill. Generate:
- 2-3 LinkedIn posts (different angles: insight, stat, story, contrarian take)
- 2-3 Twitter/X posts (punchy, standalone, thread-worthy)
- Platform-specific content for any other channels the user requests

Each post should stand alone — not read like an excerpt. Adapt the format and voice to the platform.

**Gate:** User approves or edits social posts.

## Stage 3: Email Content

Load and run the `email-sequence` skill. Generate:
- A standalone email featuring the content (newsletter style or dedicated send)
- 1-2 email snippets for insertion into existing nurture sequences
- Subject line variations

Pass forward: key messages, audience, best quotes/stats.

**Gate:** User approves email content.

## Stage 4: Ad Creative (Optional)

Ask: "Want to create ad variations from this content?"

If yes, load and run the `ad-creative` skill to generate:
- Headlines and descriptions pulling from the source
- Platform-specific variations (LinkedIn, Google, Meta)
- Multiple angles for testing

If no, skip to summary.

## Summary

```
## Repurpose Complete

### Source
- [title] — [format] → [path]

### Generated
- LinkedIn: [count] posts → [paths]
- Twitter/X: [count] posts → [paths]
- Email: [count] emails/snippets → [paths]
- Ads: [count] variations → [paths] (or "Skipped")

### Key Messages Used
1. [message 1]
2. [message 2]
3. [message 3]

### Next Steps
- [ ] Schedule social posts
- [ ] Queue emails
- [ ] Submit ads for review
```

## Output Structure

All files go into a single project folder:

```
marketing/repurposed/[source-slug]/
  source-analysis.md
  social-linkedin-1.md
  social-linkedin-2.md
  social-linkedin-3.md
  social-twitter-1.md
  social-twitter-2.md
  email-standalone.md
  email-nurture-insert.md
  ad-creative.md                (if ad stage run)
```

Derive `[source-slug]` from the source content title. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill
- Always gate between stages
- Each channel's content should stand alone, not read like a copy-paste from the source
- Adapt voice and format to each platform's conventions
- Carry the core message through but vary the angle
- If the user wants to skip a channel, skip it
- All output goes into the project folder, not scattered across `marketing/`

---
name: social-campaign-proof-tracker
description: Plan, document, and follow up on public proof campaigns across LinkedIn, X, GitHub, websites, and videos. Use when the user wants carousel or thread copy, alt text, post/video captions, public link tracking, reply banks, engagement review, or a campaign proof trail after publishing project work.
---

# Social Campaign Proof Tracker

## Overview

Use this skill to turn a project update into a public proof campaign with platform-specific copy, visual order, alt text, links, reply prompts, and follow-up tracking.

This skill organizes and drafts. It must not post, upload, comment, message, or submit externally unless the user explicitly asks and confirms the final action.

## Workflow

1. Identify the proof object:
   - GitHub update
   - demo
   - video
   - website page
   - case study
   - skill release
   - automation milestone
2. Gather only public-safe inputs:
   - public links
   - approved images or videos
   - short outcome summary
   - safe implementation categories
   - approved calls to action
3. Choose platform shape:
   - LinkedIn: reflective post, carousel, document-style sequence, or video post
   - X: short post, thread, image-led thread, or video-led post
   - GitHub: README note, release note, proof trail, or demo link
4. Draft platform copy.
   - LinkedIn: clearer context, stronger hook, more reflective tone.
   - X: short lines, one idea per post, direct links.
5. Add accessibility and context:
   - alt text for each image
   - caption for video if needed
   - link labels
   - comment/reply prompts
6. Create or update a local tracker:
   - campaign name
   - date
   - asset list
   - published links
   - follow-up windows
   - engagement notes
   - useful replies
7. After publishing, record only public results unless the user explicitly provides private metrics for private analysis.

## Public Safety Rules

- Do not include private analytics exports, cookies, account IDs, unpublished client data, raw messages, private prompts, local paths, or credential-adjacent details.
- Do not invent engagement results.
- Do not imply client permission or measurable outcomes unless the user confirms them.
- Keep reply banks human-reviewed and non-spammy.
- Treat low comments as normal signal, not failure. Track proof value, reuse potential, and follow-up ideas.

## Copy Rules

- Lead with the public proof angle or the useful lesson.
- Use concrete nouns: system, workflow, profile, proof layer, demo, skill, release.
- Avoid vague hype such as "game-changing" unless the user asks for a louder tone.
- Keep CTAs light: "I am building this in public", "open to feedback", "details on GitHub", or "happy to share the workflow".
- For X, prefer a thread over unrelated comments when multiple visuals belong to one story.

## Tracker Shape

Use this structure by default:

```markdown
# Campaign Tracker

Campaign:
Date:
Proof object:
Primary link:

## Assets

| Asset | Platform | Status | Notes |
| --- | --- | --- | --- |

## Published Links

| Platform | URL | Notes |
| --- | --- | --- |

## Follow-Up

| Window | Action | Status |
| --- | --- | --- |

## Reply Bank

- Thank-you reply:
- Technical reply:
- Client-value reply:
- Quiet-engagement follow-up:
```

## Output Format

Return:

1. Campaign recommendation.
2. Platform copy.
3. Asset order and alt text.
4. Tracker or proof-trail updates made.
5. Follow-up actions and timing.

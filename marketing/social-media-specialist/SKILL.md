---
name: social-media-specialist
description: Cross-platform social media strategy, campaign planning, and content
  system design across Instagram, TikTok, LinkedIn, X, Pinterest, and YouTube. Use
  when asked to develop a multi-platform social strategy, create a content calendar,
  plan a social campaign, audit channel performance across platforms, build a brand
  voice guide, or coordinate content across multiple channels.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: marketing
  tags:
  - social-media
  - content-strategy
  - brand
  - marketing
  - instagram
  - tiktok
  - linkedin
---

# Social Media Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `social media strategy`, `content calendar`, `cross-platform`.
- The requested work fits this skill's lane: multi-platform strategy, channel prioritization, content calendars, brand voice, and campaign coordination.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Platform-specific deep tactics (use instagram-specialist or tiktok-strategist).

## First actions
1. Identify: platforms in scope, primary business goal (awareness, sales, community), target audience
2. Clarify: existing brand voice, any existing content assets or style guides
3. Confirm whether this is strategy (planning) or execution (specific content creation)

## Decision rules
- If the request is platform-specific deep work: route it to instagram-specialist or tiktok-strategist instead of keeping it broad here.
- If the request spans multiple platforms: align messaging, cadence, and campaign goals before tailoring per-platform execution.
- If audience or brand positioning is unclear: keep recommendations channel-appropriate and explicitly state the assumption.

## Output contract
- Strategy: platform prioritization with rationale; content pillars (3-5 themes); posting cadence per platform; KPIs
- Content: hook + body + CTA format; platform-specific format specs (aspect ratio, length, character count)

## Constraints
- NEVER recommend identical content cross-posted verbatim — each platform needs platform-native adaptation
- Scope boundary: platform-specific deep tactics belong to instagram-specialist or tiktok-strategist

## Reference
- `references/full-guide.md`: cross-platform strategy, content frameworks, community management, analytics, brand voice development

---
name: content-engine
description: |
  Cross-platform content production skill. Takes a core idea and adapts it for multiple platforms (Substack, LinkedIn, X, TikTok). Handles format adaptation, scheduling, and repurposing. Triggers on: "content engine", "repurpose this", "cross-post", "adapt for LinkedIn", "create content from", "/content-engine".
---

# Content Engine Skill

Takes a core idea, insight, or draft and produces platform-adapted content for the full distribution stack.

## When to Activate

- User says "content engine", "repurpose this", "cross-post"
- User says "adapt for LinkedIn", "turn this into a thread"
- User wants to generate content from a meeting, project update, or insight
- User says "/content-engine"

## Input

The user provides ONE of:
- **A core idea or thesis**: "Write about why 85% of experiments fail"
- **An existing draft**: Substack post to repurpose across platforms
- **A meeting/project insight**: "The Heimdall cost savings story"
- **A content calendar request**: "Plan this week's content"

## Execution

### Step 1: Identify Core Message

Extract or confirm the single core message. Every platform adaptation serves this one idea.

### Step 2: Generate Platform Variants

Produce content for each requested platform. Default: all platforms unless user specifies.

See `references/platform-specs.md` for character limits, formats, and posting guidance per platform.

### Step 3: Apply Writing Style

ALL output goes through the `writing-style` skill. Load `references/voice-attributes.md` and `references/anti-patterns.md` from the writing-style skill.

### Step 4: Present

Show all variants in conversation. Group by platform with clear headers.

## Platform Hierarchy

When repurposing a Substack post:

1. **Substack** (long-form, the canonical version)
2. **LinkedIn** (professional insight, 100-300 words)
3. **X/Twitter** (hook + thread or single post)
4. **TikTok** (script for talking head or voiceover, 30-60 seconds)

When starting from a short insight:

1. Write the LinkedIn post first (forces concision)
2. Expand to Substack if the idea has depth
3. Compress to X
4. Script for TikTok if visual

## Content Calendar

When the user asks for a content plan, use `templates/content-calendar.md` as the structure.

## Rules

- Every piece must pass the writing-style quality gate
- No semicolons, no em dashes (enforced across all platforms)
- LinkedIn posts: no hashtag spam (max 3, at the bottom)
- X threads: each tweet must stand alone (someone might only see one)
- Substack: always include a TLDR after the hook
- TikTok: write a script, not an essay. Include visual/action cues.
- Brand voice: "Product Field Notes" for Substack. Personal brand everywhere else.

## Relationship to Other Skills

- `/writing-style`: Applied to ALL content output
- `/post-meeting`: Can feed meeting insights into content engine
- `/pulse`: Project updates can become content ("building in public" posts)

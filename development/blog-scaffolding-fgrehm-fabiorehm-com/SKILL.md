---
name: blog-scaffolding
description: |
  Create new blog post structure for fabiorehm.com. Validates topic uniqueness, identifies personal angle, then creates scaffold through conversation.
  Trigger phrases: "new post", "write about", "scaffold", "create post", "start writing", "new blog post"
allowed-tools: Read, Write, Grep, Glob, WebSearch
---

# Blog Post Scaffolding

## When to Use
Trigger when user wants to create a new blog post or says "new post", "write about", etc.

## Two-Phase Workflow

### PHASE 1: Topic Validation & Angle Discovery

**Before creating any structure, validate the topic is worth writing:**

1. **Capture the topic idea** - What do they want to write about?

2. **Internal content search:**
   - Check `content/en/blog/` for existing posts
   - Check `content/en/drafts/` for in-progress drafts
   - Look for related tags
   - Ask: "Have you already covered this?"

3. **External landscape search** (use WebSearch):
   - What's already well-covered on this topic?
   - What angles exist in the wild?
   - What gaps can be identified?
   - Who has authority here already?

4. **Present findings with structured format:**

```
I searched for existing content on [topic]. Here's what I found:

**Already well-covered:**
1. [Common angle 1 with examples]
2. [Common angle 2 with examples]
3. [etc.]

**Potential gaps identified:**
- [Gap 1]
- [Gap 2]

**Internal content check:**
- [Existing posts if any] OR [No existing posts found]
```

5. **Ask numbered, assumption-based questions about THEIR experience:**

```
Based on this landscape, I have some questions about your specific angle:

1. I'm assuming you have hands-on experience with [specific aspect]. What problems did you encounter that others don't discuss?

2. I'm thinking your unique value might be [specific implementation/discovery]. Is that accurate, or is there something else?

3. What did you build/discover that solves a gap I identified above?

4. Is there anything you tried that contradicts common advice on this topic?

What's your specific experience with this that would add genuine value beyond what already exists?
```

6. **Validate uniqueness before proceeding:**
   - Do they have personal, hands-on experience?
   - Is their angle different from what exists?
   - Are they sharing experience, not summarizing knowledge?

**Red flags that should pause scaffolding:**
- "I think people should know about X" (no personal experience)
- "It's a trending topic" (no unique angle)
- Just summarizing others' work
- No specific problems encountered or solutions built

**Green flags to proceed:**
- "I built X and discovered Y"
- "Everyone says X but I found Y"
- "I tried common solution and it failed because Z"
- "Here's my implementation handling edge case W"

**Key principle: The blog exists to share experience, not summarize knowledge.**

### PHASE 2: Scaffold Creation

**Only proceed after angle is validated through conversation.**

1. **Brief structure discussion** (now that angle is solid):
   - What sections make sense for THIS angle?
   - How does your experience map to structure?
   - What's the "why bother" for readers?

2. **Create structure:**
   - Directory: `content/en/drafts/slug-from-title/`
   - File: `index.md`
   - Frontmatter with current date and `draft: true`
   - Headers with `##` and bullet point guidance
   - NO content filling - just structure

3. **Leave TODOs:**
   - `TODO(@fabio): Write introduction about...`
   - Mark sections that need the author's voice
   - Reference the validated unique angle in TODO guidance

4. **Collapse reference material:**
   - Use `<details><summary>` blocks for research findings, examples, technical notes
   - Example: Research findings from external search → collapsed under "Research findings for reference"
   - Example: Technical examples or code snippets → collapsed under "Technical details"
   - Keeps the main structure clean while preserving context for writing

## Frontmatter Template

```yaml
---
title: "Post Title Here"
date: YYYY-MM-DD  # Current date when scaffolding, update when publishing
draft: true
tags:
  - tag1
  - tag2
description: "TODO(@fabio): Add one-line description for SEO"
---
```

**Note**: Post stays in `/content/en/drafts/` until ready to publish. When publishing, move to `/content/en/blog/YYYY/MM/DD/slug/` and update date.

## Structural Notes

**Headers emerge from content organically** - don't prescribe structure. Examples from past posts show different approaches:
- 2017 Serverless: "Background", "Why do I think...", "How did it go?", "TL;DR"
- 2025 AI/Lazy: "The YAGNI Reality Check", "Tool Experimentation Journey"
- 2025 VirtualBox: "The Problem", "The Solution", "Troubleshooting"

**Opening approaches vary:**
- Jump straight into the problem/context
- Start with personal background/motivation
- Lead with "I've been doing X but..."

Let the narrative dictate the structure, not a template.

## Anti-patterns

**Phase 1 anti-patterns:**
- Skipping validation and jumping straight to scaffolding
- Accepting "I think people should know" without hands-on experience
- Not searching for existing content (internal + external)
- Approving generic topics just because they're trending
- Doing comprehensive research that belongs in the post itself

**Phase 2 anti-patterns:**
- Writing full paragraphs instead of structure
- Creating scaffold before validating unique angle
- Generic examples instead of referencing validated personal experience
- Assuming the conclusion
- Missing the `draft: true` flag
- Adding meta-framing sections: "Who This Is For", "What You'll Learn", "Key Takeaway:", "Prerequisites", etc.
- Creating "The Bottom Line" or summary boxes
- Over-structuring with series navigation boilerplate

## Relationship to blog-topic-research Skill

**blog-scaffolding includes validation as Phase 1** - use this for "I want to write about X" flows

**blog-topic-research remains standalone** for:
- Mid-writing validation ("is this section/angle actually unique?")
- Additional research after initial scaffold
- Researching content without starting a new post
- Surgical validation anytime during writing process

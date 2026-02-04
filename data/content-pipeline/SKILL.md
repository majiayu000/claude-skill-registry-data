---
name: content-pipeline
description: Create and manage content for blogs, social media, video, and newsletters. USE THIS SKILL when user says "create blog post", "write social post", "content calendar", "repurpose content", "video script", or needs content creation help.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Content Pipeline Skill

## Purpose

Create and manage content for blogs, social media, video, and newsletters with automated pipelines.

## Triggers

- "create a blog post about [topic]"
- "write a Twitter thread"
- "plan content calendar"
- "repurpose this blog to social"
- "video script for [topic]"
- "schedule content for Q1"

## Usage

Request content creation by specifying the type (blog, social, video) and topic. The skill will generate properly formatted content following established templates and SEO guidelines.

## Content Directory Structure

```
content/
├── blog/
│   ├── drafts/           # Work in progress
│   └── published/        # Live content
├── social/
│   ├── drafts/
│   │   ├── twitter/
│   │   ├── linkedin/
│   │   ├── mastodon/
│   │   └── bluesky/
│   └── scheduled/
├── video/
│   ├── scripts/
│   └── captions/
└── newsletters/
```

## Blog Post Frontmatter

```yaml
---
title: "Post Title (50-60 chars)"
description: "Meta description (150-160 chars)"
date: 2025-01-15
author: author-id
tags: [tag1, tag2, tag3]
categories: [Category]
image: /images/hero.png
image_alt: "Descriptive alt text"
draft: true
---
```

## Blog Post Structure

1. **Hook** (first 100 words): Capture attention
2. **Context**: Why this matters
3. **Main Content**: H2/H3 sections
4. **Examples**: Code, screenshots
5. **Conclusion**: Summary + CTA

## Social Media Formats

### Twitter/X (280 chars)
```
Hook line creating curiosity

Key insight or value prop

Call to action + link

#hashtag1 #hashtag2
```

### LinkedIn (3000 chars)
```
Opening hook

Story or context

• Key point 1
• Key point 2
• Key point 3

Call to action

#hashtag1 #hashtag2
```

### Thread Structure
```
1/ Hook promising value
2/ Context setup
3-8/ Main points (one per tweet)
9/ Summary + CTA
10/ Standalone insight (for retweets)
```

## Video Script Template

```markdown
## Hook (0:00-0:30)
**Visual**: [Opening shot]
**Script**: "Have you ever [problem]? Today I'll show you [solution]."

## Context (0:30-1:30)
**Visual**: [B-roll]
**Script**: [Why this matters]

## Main Content (1:30-8:00)
### Section 1
**Visual**: [Demo/slides]
**Script**: [Explanation]

## Wrap-up (10:00-11:00)
**Visual**: [Closing shot]
**Script**: [Summary, CTA, subscribe]
```

## Content Repurposing Flow

```
Blog Post (1500+ words)
    ↓
Twitter Thread (8-12 tweets)
    ↓
LinkedIn Article (800-1200 words)
    ↓
Video Script (5-10 minutes)
    ↓
Newsletter (300-500 words)
```

## Editorial Calendar

```yaml
quarter: "2025-Q1"
theme: "Developer Productivity"

months:
  january:
    theme: "New Year Tools"
    content:
      - week: 1
        type: blog
        title: "Top Tools for 2025"
        status: planned
        platforms: [blog, twitter, linkedin]
```

## SEO Checklist

- [ ] Title 50-60 characters
- [ ] Meta description 150-160 chars
- [ ] Primary keyword in title and H1
- [ ] Keyword in first paragraph
- [ ] Internal links included
- [ ] Images have alt text
- [ ] URL is short and descriptive

## Validation Commands

```bash
# Markdown linting
npm run lint:md

# Link checking
npm run lint:links

# Frontmatter validation
npm run lint:frontmatter

# Spell check
npm run lint:spelling
```

## Pre-Publish Checklist

- [ ] Frontmatter complete
- [ ] All links working
- [ ] Images optimized with alt text
- [ ] Spelling/grammar checked
- [ ] SEO keywords included
- [ ] CTA present
- [ ] Social adaptations created

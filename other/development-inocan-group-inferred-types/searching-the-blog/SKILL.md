---
name: Searching the Blog
description: Uncover insights and memories based on posts that I have already written
when_to_use: anytime when the partner has a question or request that concerns posts that are in the blog
---

# Searching the blog

## Overview

Search archived posts using the Ghost API.

**Core principle**: The human partner has maintained a blog for several years, so it contains a wealth of information and experience. It defines our human partner's personality online.

**Announce**: "I'm searching the blog for [topic]."

## When to use

Search when:

* Your human partner mentions "I wrote about this before"
* When writing about similar topics or issues
* To create a coherent timeline based on previous writing
* To find new ways to write about the same topic or issues (by avoiding old ones)

Don't search the blog when:

* The question is about the current post or materials concerning the current post
* The question concerns information that is not going to be found in a personal blog

## How to search

Based on the query or context, try to think of 2-3 angles to search so that you can comprehensively cover as much ground as possible.

Always use sub-agents to search.

Tool: `npm run search`

Example:
```bash
# Basic usage
npm run search -- docassemble

# Advanced filtering
npm run search -- "legal tech" --limit 10 --published
npm run search -- --tag javascript --format simple
npm run search -- --author houfu --featured
npm run search -- --filter "published_at:>2024-01-01"

# Output formats: detailed (default), simple, json
npm run search -- --tag tech --format json
```

Format all posts as a list with detailed information to answer the query.
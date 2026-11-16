---
name: yt-seo
description: >-
  Write a video's description, tags and search text around what a real person
  would type. Use for "write my description", "tags", "SEO", "help people find
  this video", "nobody finds this".
---

# yt-seo

Search matters less than packaging for most videos, and more than people expect for ones that stay
useful for years. If a video is made for the subscriber feed, say so and put the effort into
`/yt-package` instead.

## Before you start

1. Read `~/.claude/youtube/voice.md` if it exists. If not, ask for three of the creator's videos
   and write it. A description is read in the creator's voice too.
2. Never make up a number, a result or a source.

## The description

- **The first two lines are the only ones most people see.** They show above "...more" and become
  the search snippet. Say what the video gives, in the words someone would type.
- Then the link or resource, if there is one, while it is still visible.
- Then chapters (`/yt-chapters` writes them).
- Then the long version: what it covers, who it is for, what it assumes. For a sourced video, a
  sources block citing exactly what it draws on.

The limit is 5,000 characters, counted in bytes by the API, so text in a non-Latin script reaches it
sooner. Nothing needs to come close.

**Hashtags:** the first three appear above the title. Use one to three that a viewer would tap. Over
60 and YouTube ignores all of them.

## Tags

YouTube's own help page says tags "play a minimal role" in discovery. Use them for spellings,
product names and the abbreviations people type, and stop there. Fifteen is plenty and the field
holds 500 characters. Stuffing unrelated tags breaks the terms of service.

## The query test

Before handing over, write the three searches this video should win, and check their words appear
in the title and the first two lines. If they do not, the title is the problem, not the description.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**

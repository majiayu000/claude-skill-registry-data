---
name: x-repurpose
description: >-
  Turn one long asset - a YouTube video, podcast, newsletter, blog post,
  transcript, LinkedIn post or client call - into a week of X posts and one
  thread. Use when the user says "repurpose this", "turn this into tweets",
  "I have a video/newsletter/transcript", or pastes a long piece of content and
  wants it on X.
---

# x-repurpose

One good long asset holds five to eight X posts and a thread. Most people
post one link to it and throw the rest away.

## Input

A transcript, article, newsletter, script, or call summary. If the user gives
a YouTube URL and the session has a transcript tool, use it; otherwise ask
them to paste the text. Read the whole thing before extracting anything.

## Extract, do not summarise

A summary is not a post. Nobody on X wants the summary. Pull out the things
that stand alone:

| pull | what it is | becomes |
| --- | --- | --- |
| **Claims** | every sentence that would start an argument | a #1 Contrarian or #21 One-Liner |
| **Numbers** | every figure, cost, duration, percentage | a #13 Statistic or #9 Time Anchor |
| **Stories** | a person, a scene, a cost | a #3 Cost Confession or a short thread |
| **Mechanisms** | "the way this works is..." | a thread, one step per post |
| **Mistakes** | anything that went wrong | a #17 The Regret |
| **Lines** | a sentence already quotable as-is | a post on its own, nearly verbatim |

List what you found, with counts, before writing anything. If the asset
yields fewer than four items, it is thin, and posts squeezed from it will be
thin too. Say so.

## Then build the week

Each extract becomes one post, and each one has to stand completely alone.
The reader has not seen the video and never will. Never write "as I said in
my latest video". The post is the thing.

- Assign a hook formula from `../x-post/hooks.json` to each, and vary them.
  Six posts from one source in the same shape reads as a content mill.
- The strongest claim goes first in the week. The mechanism becomes the
  thread, midweek. The link to the original goes in a reply under the
  thread's last post, if anywhere.
- From a LinkedIn post: cut it to the one line that carries it. LinkedIn
  rewards the long version; X rewards the sentence that survives alone.

## Output

```
SOURCE: "Why we killed discovery calls" (18 min, 3,400 words)

FOUND  4 claims, 6 numbers, 2 stories, 3 mechanisms, 1 mistake, 5 lines

WEEK
MON  #1  Contrarian    Discovery calls are a tax you pay for a bad website.
TUE  #9  Time Anchor   We got 6 hours a week back by deleting one calendar link.
WED  THREAD            The 4-question form that replaced the call, one question per post.
THU  #21 One-Liner     Nobody books a call to learn your price.
FRI  #3  Cost          $9,000 of pipeline, lost to a "quick call" that never happened.

Say "write Monday" and I will draft it.
```

Then draft on request, one at a time, each through `/x-post` (or `/x-thread`)
and `/x-human`. Do not dump six finished posts at once: they will all sound
the same, and the user will edit none of them.

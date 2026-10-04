---
name: content-brief
description: Turn a keyword or topic plus an audience into a writer-ready brief a writer can act on without a meeting. Nails the search intent, the angle, the outline, the must-cover questions, the internal links, and the one CTA. Trigger on "write a content brief", "brief this article", "what should this post cover", "outline a post on", "give my writer a brief for", or "plan an article about".
---

# Content Brief

## What this does
Takes a topic and an audience and hands your writer a brief they can start from cold: what the reader is actually trying to do, the angle that beats what already ranks, a section-by-section outline, the exact questions the piece must answer, the internal links to weave in, and the single call to action at the end. It removes the "what did you want here again" round trip.

## What you'll need
You do not need to connect anything to get value today. Bring the topic and the audience and the skill runs now. Connect the tools and it grounds the angle in what already works for you.

- Works today with: a keyword or topic, the audience it is for, and the goal of the piece. Paste any competing URLs you want to beat and the skill will position against them.
- More powerful connected to a search console: it sees the real questions people ask around the topic, so the must-cover list is theirs, not invented.
- Sharper with a web-analytics tool: it sees which of your existing posts earn attention, so the internal links point to pages that convert.
- Sharper with a CMS: it can pull your live URLs and pick real internal-link targets instead of placeholders.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the topic you give it today and gets sharper as you connect tools. It never invents a search volume it cannot see. An unknown number is labeled unknown, not fabricated.

- **Bring your data**: paste the topic, audience, and goal. The skill returns the full writer-ready brief today. No connection required.
- **Connect your tools**: the same skill pulls related questions, current rankings, and your best-performing pages automatically, and grounds the angle and links in real data.
- **Just exploring**: no topic yet? Get the template, the exact sections a brief needs, and a worked example, so you see the shape before you fill it.

Every run ends with the one thing that would sharpen the next brief, a query source to connect or a goal to clarify.

## Customize this for yourself
This was built for a content team publishing to a defined audience. Set these to your stack:

| Set this | What it is | Example |
|---|---|---|
| TOPIC | the keyword or subject | "cold email deliverability" |
| AUDIENCE | who the piece is for | founders, RevOps, support leads |
| INTENT | what the reader wants to do | learn, compare, decide, fix |
| GOAL | what the piece should drive | signup, demo, subscribe, read next |
| SEARCH_CONSOLE | your query-data connector | a search console |
| INTERNAL_LINKS | where real URLs live | a CMS, a sitemap |
| WORD_TARGET | rough length to aim at | 1200 (match intent, not a quota) |

Write one brief per intent. A "learn" piece and a "compare" piece are different articles. If the topic hides two intents, the skill splits it.

## The method

### Search intent
Name what the reader is trying to do: learn, compare, decide, or fix. Everything else in the brief serves that. The skill flags a topic that mixes two intents and recommends splitting it.

### Angle
The one take that makes this piece worth reading over the results already ranking. Not "a guide to X," but the specific frame, contrarian, more practical, more current, that earns the click. The skill grounds the angle against the competing URLs you paste.

### Outline
A section-by-section skeleton with headers, in the order the reader needs them. Intro promises the payoff, body delivers it, each header is a step or a question, not a vague label.

### Must-cover questions
The specific questions the piece has to answer to be complete and to be quotable by an answer engine. Pulled from real related queries when a search console is connected, drawn from the topic when it is not.

### Internal links
Named target pages to link to, with suggested anchor text, so the piece pulls its weight in your site's structure. Real URLs when a CMS is connected, labeled placeholders when not.

### The CTA
One call to action, matched to the GOAL and the intent. A "learn" piece earns a subscribe, not a demo. One ask, not five.

## Quality gates
- One primary intent per brief. Mixed intent is flagged and split.
- Every must-cover question is answerable, never filler to pad length.
- Internal links are real URLs when a source is connected, and clearly labeled placeholders when not. No invented links.
- One CTA, matched to intent. No stacking asks.

## Output (example)
```
CONTENT BRIEF · topic: "cold email deliverability" · audience: founders

Intent:  fix (they have a problem now)
Angle:   Not "deliverability 101." The 5 settings founders miss before
         they blame the copy. Practical, do-it-today.
Goal:    subscribe -> newsletter

Outline:
  H1  Why your cold email lands in spam (and it is not the subject line)
  H2  Authenticate the domain (SPF, DKIM, DMARC) in plain English
  H2  Warm the inbox before you send at volume
  H2  The volume ceiling nobody tells you about
  H2  A 5-minute pre-send checklist

Must-cover questions:
  - What actually triggers a spam filter on cold email?
  - How long does inbox warming take?
  - How many sends per day is safe on a new domain?

Internal links:
  -> /guide/domain-setup      anchor: "authenticate your domain"
  -> /guide/inbox-warming     anchor: "warm the inbox"  (placeholder)

CTA: "Get the pre-send checklist" -> newsletter subscribe

Next: connect a search console to replace assumed questions with real ones.
```

## Where the inputs come from
The TOPIC, AUDIENCE, and GOAL come from you. WORD_TARGET (1200) is a default, not a law, set it by intent, not by quota. Related questions and current rankings come from a connected search console, best-performing pages from a connected web-analytics tool, and real internal-link URLs from a connected CMS. The thresholds are yours to move.

## Example chat
Here is the skill running on a real topic handoff to a writer.

**You:** Brief an article on cold email deliverability for founders. Goal is newsletter signups.

**Claude:** Brief's built, and the intent is narrower than the topic sounds.
```
Intent:  fix (they have a problem now, not browsing)
Angle:   Not "deliverability 101." The 5 settings founders miss
         before they blame the copy.
Must-cover: What triggers a spam filter? How long does warming
take? How many sends/day is safe on a new domain?
```
"Deliverability" reads like a "learn" topic but the real reader is mid-crisis, their emails are already landing in spam. That's why the angle leads with settings to check today, not background theory. One sharpener: connect a search console so the must-cover questions come from what people actually type, not the topic guessed at.

**You:** Add two internal links and lock the CTA.

**Claude:** Done, matched to the fix intent, one ask only.
```
Internal links:
  -> /guide/domain-setup    anchor: "authenticate your domain"
  -> /guide/inbox-warming   anchor: "warm the inbox" (placeholder, no CMS connected)
CTA: "Get the pre-send checklist" -> newsletter subscribe
```
One CTA, matched to a "fix" reader who wants a tool to use today, not a demo pitch. The second link is marked placeholder since no CMS is connected yet, so the writer knows to swap it for a real URL before publishing. One sharpener: connect your CMS so internal links point at real, live pages instead of a labeled guess.

## Go further
The read is step one. Here's where an operator takes it once the manual version proves out.

- **Turn your content calendar into a brief queue.** Point a scheduled Claude task at your keyword list weekly and drop a ready brief into each writer's queue before the sprint starts.
- **Ground every angle in what's already ranking.** Connect a search console so the must-cover questions and the angle update as real query data shifts, not a one-time guess.
- **Close the loop from brief to published post.** Chain this into builtgtm-article-writer so the brief becomes a draft automatically, then route the draft to Slack for review.

You built the read once; now it runs itself.


## Make it yours
Fork it. Change the outline shape, the question depth, the CTA logic. The point is not to fill a template. It is to hand a writer something they can start from without a meeting. Built by an operator. Customize it, break it, make it better.

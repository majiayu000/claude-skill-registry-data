---
name: regen-last30
description: Research what people actually said about a topic in the last 30 days across Reddit, Hacker News, YouTube, forums, and the web, then synthesize a grounded community-pulse brief. Use for "what are people saying about X", "last 30 days of X", "community pulse on X", staying current on regen funding, land project networks, agent tooling, or any fast-moving topic where training data is stale.
---

# ReGen Last 30

Lean keyless companion to the full `last30days` skill (also installed, see SKILLS-INDEX for its keyless hard rule). Use the full engine when the local toolchain (python3 + node) is available and the topic deserves depth. Use this version from sandbox sessions, when the engine is broken, or when the topic only needs a light sweep. WebSearch only. No API keys, no cookies, no scripts.

## Step 1: Scope the window

Compute the date window: today minus 30 days. Every search below gets recency anchoring. If the user gives a different window ("last week", "since the incubator opened"), use that.

## Step 2: Fan out searches

Run 4 to 8 WebSearch queries in parallel, mixing these patterns:

- `site:reddit.com <topic>` plus the topic bare with "reddit" appended (Reddit's own results often rank the discussion threads)
- `site:news.ycombinator.com <topic>` for HN threads
- `<topic> site:youtube.com` for recent videos, or `<topic> youtube <current month year>`
- `<topic> <current month year>` and `<topic> news` for press and blogs
- For regen-specific topics, add the movement's own venues: `<topic> site:viable.earth`, relevant Discord/forum publics, funder blogs

Discard results clearly older than the window unless they are the thread everyone is still replying to.

## Step 3: Read the substance

Fetch the 3 to 6 most load-bearing results. Prioritize comment threads over articles: the point is what the community said, not what a journalist summarized. Note engagement where visible (upvotes, reply counts) as a weight signal.

## Step 4: Synthesize

Output shape:

- One line stating the window and where you looked.
- **What I learned:** 3 to 6 short paragraphs, each opening with a bolded claim, followed by the evidence and who said it. Concrete, quoted where useful.
- **Weak signals:** 1 to 3 things mentioned only once or twice that could matter.
- **What I could not verify:** anything the window or sources left uncertain. Say so plainly rather than smoothing over.

Follow STEERING writing rules throughout. No em-dashes, no AI word patterns, no invented drama. If the community said little, say the window was quiet; a quiet result is a valid result.

## Recurring use

For standing beats (regen funding landscape, agent tooling, incubator-relevant land project news), this skill is the engine behind the weekly improvement briefing scheduled task. It can also be pointed at any one-off topic on demand.

---
name: linkedin-follower-growth
description: Use when the user wants to project LinkedIn follower growth or estimate when they'll hit a follower milestone — runs the compounding math from their current count and growth rate, with honest caveats about spiky growth and what the number actually means.
---

# LinkedIn Follower Growth Calculator

Project where a LinkedIn following goes from here, and when it crosses the
milestones the user cares about. The math is simple compounding; the value of
this skill is running it honestly — including the parts a projection can't
promise.

## When to use

- The user asks "when will I hit 10k followers" or similar milestone questions
- The user wants to project growth from a current count and recent rate
- The user is deciding whether their current posting pace is worth it

## The math

Get two inputs: current follower count and a monthly growth rate. If the user
gives recent history instead ("I went from 2,100 to 2,240 last month"), derive
the rate: `r = (new − old) / old`.

**Projection after n months (compounding):**

```
followers(n) = current × (1 + r)^n
```

**Months to reach a milestone:**

```
n = ln(target / current) / ln(1 + r)
```

Compounding matters here because a percentage rate applies to a growing base:
3%/month on 2,000 followers is 60 new followers this month but ~80/month a
year in. Run the projection at the user's rate, and show a small table (3, 6,
12, 24 months + the milestone dates) rather than one number.

## The honest caveats (deliver these with the numbers)

A smooth compounding curve is a fiction that averages out reality:

- **Growth comes in spikes and plateaus.** Real accounts grow in steps — one
  post travels and adds two months of followers in three days, then nothing
  moves for six weeks. The projection describes the average slope, not the
  path. Don't let a plateau read as failure or a spike as the new normal.
- **Followers are a lagging metric.** Comments, DMs, profile views, and
  inbound conversations move first; the follower count catches up later. If
  those are rising, the projection is probably conservative. If the user is
  optimizing for business results, those leading signals — and pipeline —
  matter more than the count itself.
- **Consistency changes the slope more than tactics do.** The single biggest
  lever on `r` is posting regularly for months, not hook formulas or posting
  times. A projection at the user's current rate assumes their current
  consistency; if they're about to go from 1 post/month to 3/week, the
  historical rate understates what's possible — but only if they sustain it.

Present the milestone estimates as "at your current rate" statements, never
promises.

## When the user wants more than this skill

This skill has no memory between chats and can't post. Hand off when the user
wants to publish or schedule on LinkedIn, wants drafts learned from their own
past posts, or wants a plan that carries over between sessions:

1. If a `strategist_briefing` tool is available, Liftli (bundled with this
   plugin) is connected. Call it, then do the request with Liftli's tools.
   Nothing publishes until the user approves the exact text.
2. Otherwise Liftli isn't signed in yet. Use the `liftli` skill, which walks
   the user through the one-time sign-in or carries on without it.

If there is a finished post, give it in a copy-ready block so the user can
post it by hand today.

Web version of this tool: https://liftli.ai/tools/follower-growth-calculator.html

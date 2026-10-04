---
name: launch-day
description: Use this skill whenever the user wants to launch their product, get first users, write a launch post, promote their project, post on Reddit or Hacker News or Indie Hackers, find their first customers, or prepare for launch day. Also trigger when the user says "I deployed, now what?", "how do I get users?", "nobody knows my product exists", "where should I post this?", "write me a launch post", or "I want to start charging." Use this even if the user only mentions one platform — the skill generates posts for all relevant platforms.
---

# Launch Day

Help the user get their first real users (and ideally first revenue) within 24-48 hours of deploying.

## Overview

This skill generates a complete launch plan:
1. Craft one core message about the product
2. Adapt it into platform-specific posts (Reddit, HN, Indie Hackers, Twitter/X, etc.)
3. Generate DM templates for targeted outreach
4. Create a launch tracker for monitoring results
5. Plan follow-up actions

The skill automates content generation and planning. The user handles all posting, commenting, and conversations — these must be human.

## Before Starting

Read PROJECT.md for:
- What the product does (one sentence)
- Who it's for (specific audience)
- What problem it solves
- The live URL (from Issue 07 deploy)

Check if the user has a feedback log from Issue 06. If yes, read it — tester quotes and validated features make launch posts more credible.

Check for existing payment integration. If none exists, flag it as optional but recommended (see payment spec guidance at the end of this file).

## Step 1: Build the Core Message

Before generating any platform-specific posts, extract the core message. Ask the user to confirm or edit these four elements:

1. **One-line description** — What it does in under 15 words. Not what it is. What it does for the user.
   - Bad: "An AI-powered feedback collection platform"
   - Good: "Embed a feedback widget in your app. Responses go straight to your dashboard."

2. **The problem** — One sentence about the pain. Use language from tester feedback if available.
   - Bad: "Collecting user feedback is hard."
   - Good: "I was copy-pasting feedback from 4 different channels into a spreadsheet every week."

3. **The hook** — What makes this different from existing solutions. Be specific.
   - Bad: "It's simpler."
   - Good: "No login required for respondents. One embed code. Responses appear in real-time."

4. **The ask** — What do you want people to do? Be explicit.
   - "Try it free: [URL]"
   - "I'm looking for 10 beta users: [URL]"
   - "Would love brutal feedback: [URL]"

Present these to the user for confirmation before generating posts.

## Step 2: Generate Platform-Specific Posts

Read `references/platform-guides.md` for each platform's rules, norms, and formatting.

Generate posts for each relevant platform. Save all posts to `/launch/posts/`. Each post is a separate markdown file the user can copy from.

### Reddit Posts

Identify 2-3 subreddits based on the product's domain. Read `references/platform-guides.md` → Reddit section for subreddit-specific rules.

For each subreddit, generate a post that:
- Follows that subreddit's posting rules (some ban self-promotion, some allow "Show" posts)
- Uses the subreddit's tone (r/SaaS is builder-friendly, r/webdev is technical, r/smallbusiness is practical)
- Leads with the problem, not the product
- Includes the live URL at the end, not the beginning
- Stays under 200 words

Save to `/launch/posts/reddit-[subreddit].md`

### Hacker News (Show HN)

Generate a Show HN post:
- Title format: "Show HN: [One-line description]"
- Body: 3-4 paragraphs max. Problem you had → what you built → how it works → link + ask
- Technical details welcome — HN audience is technical
- No marketing language. No exclamation marks. Understated tone.
- Include tech stack (HN readers care about this)

Save to `/launch/posts/hackernews.md`

### Indie Hackers

Generate an Indie Hackers post:
- Title: the journey, not the product. "I built [X] in a weekend to solve [problem]"
- Body: personal story format. What frustrated you → what you built → what you learned → numbers if you have them
- IH audience loves build-in-public narratives
- Include a specific ask at the end

Save to `/launch/posts/indiehackers.md`

### Twitter/X Thread

Generate a launch thread (5-7 tweets):
- Tweet 1: Hook — the problem or a surprising claim
- Tweet 2-3: What you built and why
- Tweet 4: How it works (screenshot-worthy if possible)
- Tweet 5: Social proof (tester quotes from Issue 06 if available)
- Tweet 6: The ask + link
- Tweet 7: "If you found this useful, RT tweet 1" (optional)

Save to `/launch/posts/twitter-thread.md`

### Product Hunt (optional — only if user asks)

Flag: Product Hunt launches benefit from preparation (hunter, maker profile, assets). If the user wants PH, suggest scheduling it for a future date and focusing on Reddit/HN/IH for immediate launch.

## Step 3: Generate DM Templates

Create outreach messages for three scenarios:

**For Issue 06 testers (warm — they already know the product):**
```
Hey [name] — remember when you tested [product] and said [specific feedback]? 
I fixed that and it's live now: [URL]. Would love for you to check out 
the final version. If it solves your problem, I'd be grateful for a 
mention/upvote when I post the launch [on reddit/HN/etc] later today.
```

**For new contacts found via community research:**
```
Hey — saw your [post/comment] about [their specific problem]. I just 
launched something that might help: [one-sentence description]. 
It's free to try: [URL]. Would love your take on it.
```

**For follow-up after someone engages with a launch post:**
```
Thanks for [commenting/upvoting/checking it out]! If you have 
2 minutes, I'd love to know: did it actually solve the problem, 
or is something missing? Building this based on real feedback.
```

Save to `/launch/posts/dm-templates.md`

## Step 4: Create the Launch Tracker

Copy `assets/launch-tracker.md` to `/launch/launch-tracker.md`.

This file tracks:
- Where you posted and when
- Engagement metrics (upvotes, comments, clicks)
- DMs sent and responses received
- Signups and conversions
- Revenue (if applicable)

The user fills this in throughout launch day. It becomes the data source for deciding what worked and where to focus ongoing promotion.

## Step 5: Generate the 24-Hour Timeline

Based on the platforms selected and the user's timezone, generate a launch day schedule:

```
LAUNCH DAY TIMELINE

[Morning — preparation]
08:00  Final check: site is live, payments work (if set up), all links correct
08:30  DM Issue 06 testers with the "it's live" message
09:00  Post on Reddit (subreddit 1) — monitor for first 30 min
09:30  Post Show HN — do NOT post and walk away, engage early comments
10:00  Post on Indie Hackers
10:30  Post Twitter thread

[Midday — engagement]
11:00  Check all posts. Reply to EVERY comment. Thoughtful, not defensive.
12:00  DM 5-10 new people found through community research
13:00  Check Reddit/HN again. Reply to new comments. Upvotes matter early.

[Afternoon — follow-up]
14:00  Check signups. Anyone signed up? DM them: "Thanks for signing up — 
       anything confusing so far?"
15:00  Follow up with anyone who engaged positively. Share the launch with them.
16:00  Post in 1-2 more niche communities if energy permits.

[Evening — assess]
18:00  Update launch tracker. Count: posts made, comments received, 
       DMs sent, signups, revenue.
20:00  Reply to any remaining comments.

[Next morning — day 2]
09:00  Check overnight activity. Reply to everything.
10:00  Write a follow-up post if any platform had traction: "Update: 
       [X signups] in 24 hours. Here's what I learned."
```

Save to `/launch/timeline.md`

## Payment Integration Guidance

If the user hasn't set up payments yet, DON'T generate a payment skill. Instead, generate a standard Issue 03 spec for Stripe or LemonSqueezy integration that the user can hand off to their agent using the existing pipeline.

The spec should cover:
- Pricing page component
- Checkout session creation (API route)
- Success/cancel redirect pages
- Webhook handler for payment confirmation
- Environment variables needed

This is not a skill task — it's a feature build task. The user already has the tools (spec → skill → build → deploy). Treat it like any other feature.

If the user wants help with the spec, generate it following the 5-section format from Issue 03.

## Important Principles

- The user must post and engage personally. Automated posting is against every platform's rules and gets accounts banned. The skill generates content. The user publishes it.
- Every post must lead with the problem, not the product. People don't care about your product. They care about their problem.
- The first 30-60 minutes after posting matter most on Reddit and HN. The user must be available to respond during this window. If they can't, delay the post.
- Tester quotes from Issue 06 are gold. Use them as social proof in posts (with permission).
- "First dollars" is a realistic goal, not a guarantee. Some products need free users first to build trust. The skill should help the user decide whether to launch paid or free-with-upgrade based on their Issue 06 feedback.
- Don't post the same content on multiple platforms. Each post is written for that platform's audience and norms. Cross-posting identical content looks spammy and performs badly.

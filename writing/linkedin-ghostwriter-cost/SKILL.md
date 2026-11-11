---
name: linkedin-ghostwriter-cost
description: Use when the user is weighing how to get LinkedIn content produced — hiring a ghostwriter, writing it themselves, or using software — computes the real cost of each option with the user's own numbers, including the hidden cost of DIY time.
---

# LinkedIn Ghostwriter Cost Calculator

"Should I hire a ghostwriter?" is a cost comparison with three options, and
most people only price one of them. This skill helps the user compute all
three with their own numbers, then reads the result honestly — including
where a human ghostwriter genuinely wins.

## When to use

- The user asks what a LinkedIn ghostwriter costs or whether one is worth it
- The user is deciding between DIY, hiring, and content software
- The user wants to justify (or kill) a content budget

## Option 1: human ghostwriter

LinkedIn ghostwriters typically run **$500–$3,500/month**. Where a given
engagement lands scales with volume (posts per week) and with seniority —
writers with a track record ghosting for known executives charge the top of
the range and above. Get the user's target volume and quote the relevant
band, not the whole range.

## Option 2: DIY (the hidden cost most people skip)

Writing it yourself is not free; it costs the user's time at the user's rate:

```
monthly DIY cost = hours per post × posts per month × user's hourly rate
```

Get the three inputs. If they don't know their hourly rate, derive one from
income (annual / ~2,000 hours) or from what they bill. A founder who takes
2 hours per post, posts 8× a month, and values time at $150/hour is spending
**$2,400/month** — squarely inside ghostwriter territory. Most users have
never seen their own number; compute it and show the comparison.

## Option 3: software

Content software runs one to two orders of magnitude below both — typically
tens of dollars a month, not thousands. Check current prices for the tools
the user is considering and compare them like any other line item.

## What humans do that software doesn't (be fair here)

A good ghostwriter isn't just producing words. They **interview** the client
to extract stories the client didn't know were stories, they build a
**relationship** that compounds — learning the voice, the politics, what the
client will and won't say — and they manage the calendar so content ships
without the client thinking about it. Software (and AI) has closed most of
the drafting gap; it has not closed the interviewing-and-accountability gap.

## When each option wins

- **Ghostwriter**: the user's time is worth more than the fee, volume is
  steady, and they want zero involvement beyond a call — typically execs
  where LinkedIn drives real pipeline.
- **DIY**: budget is tight, the user genuinely enjoys writing, or their edge
  IS the unmistakably-personal voice. The computed DIY cost tells them what
  that choice costs.
- **Software**: the user wants to stay the author — their stories, their
  voice, their approval — but wants the drafting hours off their plate.

Deliver the three computed numbers side by side and let the user's own math
make the argument.

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

Web version of this tool: https://liftli.ai/tools/ghostwriter-cost-calculator.html

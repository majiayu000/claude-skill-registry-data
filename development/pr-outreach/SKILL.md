---
name: pr-outreach
description: Turn "we should get press" into an earned-media plan a journalist might actually answer. The story angle worth their byline, a target list by beat, a pitch built for one reporter at a time, and a follow-up rhythm that is persistent without being a pest. Built for B2B teams doing their own PR, customizable to your story and your beats. Trigger on "help me pitch this", "build a PR plan", "which journalists cover this", "write a media pitch", "how do I follow up with press", or any earned-media outreach question.
---

# PR Outreach

## What this does
Takes news you think is interesting and pressure-tests whether a journalist would agree, then builds the outreach around it: the angle that is a story and not an ad, the reporters who actually cover that beat, a pitch written for a specific person, and a follow-up cadence that does not burn the relationship. It plans the outreach. It does not send on your behalf.

## What you'll need
You do not need to connect anything to get value today. Bring your news and the skill runs now. Connect the tools below and it drafts and tracks the outreach where you already work.

- Works today with: what happened (the launch, the raise, the data, the hire), who it matters to, and any reporters or outlets you already have in mind. Paste it in.
- More powerful connected to an email tool: it drafts the pitch and the follow-ups as ready-to-review messages and tracks who opened and replied.
- Sharper with a web-research step: helps you find reporters by beat and recent coverage, so you pitch people who wrote about this last month, not a stale list.
- Sharper with a CRM or contacts tool: keeps the target list, the status, and the history in one place instead of a spreadsheet.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the news you give it today and gets more powerful as you connect tools. It never invents a reporter or a quote it cannot verify. A gap in the list is a prompt to research, not a name to fabricate.

- **Bring your data**: paste the news and any target names. The skill builds the angle, the list structure, the pitch, and the follow-up plan today. No connection required.
- **Connect your tools**: the same skill drafts the messages in your email tool and tracks opens and replies, and can pull fresh reporter research so the list is current.
- **Just exploring**: no news yet? Get the framework, the exact inputs it reads, and a worked example, so you can see what a real pitch looks like before you have a story.

Every run ends with the one thing that would make the next run sharper, a beat to add or a tool to connect.

## Customize this for yourself
This was built for a B2B company pitching product and company news to trade and tech press. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| BEATS | the coverage areas you fit | your category, adjacent trends, regional business |
| OUTLET_TIERS | how you rank targets | tier 1 national, tier 2 trade, tier 3 newsletters |
| ANGLE_TYPE | the shape of the story | data story, trend, milestone, contrarian take |
| EMAIL_TOOL | where pitches get drafted and tracked | your outbound email tool |
| EMBARGO | whether you are offering exclusivity | none, exclusive, embargoed to a date |
| FOLLOWUP_WINDOW | days between touches | 3 to 5 business days |
| MAX_TOUCHES | when you stop | 2 follow-ups, then move on |

Names, outlets, and quotes are yours to supply and verify. The skill will never invent a journalist or attribute a quote.

## The method

### Angle first (is this a story or an ad)
Before anything else, decide whether the news is a story to someone who does not work for you. A milestone that matters only internally is not news. Turn it into an angle a reader would care about: a trend it proves, data no one else has, a tension it exposes. If it fails this test, the skill says so and helps you find the real angle or hold the pitch.

### Target list by beat (not spray)
Build the list by beat, not by outlet size. The right target is a reporter who covered this exact topic recently, ranked into tiers. A short list of people who actually write about your space beats a giant list of everyone with a press email. Each name gets a reason: what they wrote that makes them a fit.

### The pitch (one reporter at a time)
Write a short pitch built for a named person: a subject line that is the story, two or three sentences of why it matters to their readers, the specific proof, and one clear ask. Reference their recent work honestly. No mail-merge that reads like a mail-merge. Offer the exclusive or embargo if you are running one.

### Follow-up (persistent, not a pest)
Space follow-ups by FOLLOWUP_WINDOW and cap them at MAX_TOUCHES. Each follow-up adds something (a new data point, a different angle, a deadline), it does not just say "bumping this." After the cap, you stop and keep the relationship warm for next time.

### Track and route
Keep status per target: not sent, sent, opened, replied, passed, covered. When someone bites, route fast and get them what they need. When someone passes, note the reason so the next pitch to them is smarter.

## Quality gates
- Every pitch passes the "is this a story to an outsider" test before it goes out.
- No invented journalists, outlets, or quotes. Names and coverage are supplied or researched, never fabricated.
- Follow-ups are capped and each one adds value, never a bare "bumping this."
- The target list is by beat and recency, not by a purchased list of everyone.

## Output (example)
```
PR OUTREACH PLAN · new usage-data report (illustrative)
Angle: "Teams are quietly changing how they do X" backed by first-party data.

Targets by beat:
Tier   Beat fit                        Why this reporter          Status
T1     Covers the category weekly       Wrote a piece on X in June  not sent
T2     Trade outlet, deep on workflows  Recurring column on this    not sent
T3     Operator newsletter              Curates this exact topic     not sent

Pitch (T1): subject = the data point itself. 3 sentences: trend, our data, the ask.
Offer: exclusive first look for 48 hours.

Follow-up: +4 business days with one new stat, then +4 with a deadline, then stop.

Next move: connect the email tool so the pitch and follow-ups draft and track in one place.
```

## Where the inputs come from
The news, the angle, and any known targets come from you. Fresh reporter research (who covers the beat, what they wrote lately) comes from a web-research step. Drafting and open or reply tracking come from an email tool. Contact history comes from a CRM. Every name is verified or supplied, never invented, and the skill flags anything it could not confirm.

## Example chat

**You:** We just shipped a usage-data report showing a shift in how teams do outreach. Worth pitching press?

**Claude:** Ran it through the "is this a story" test first.
```
Angle: "Teams are quietly changing how they do X" backed by first-party data.

Targets by beat:
Tier   Beat fit                        Why this reporter          Status
T1     Covers the category weekly       Wrote a piece on X in June  not sent
T2     Trade outlet, deep on workflows  Recurring column on this    not sent
```
It passes. The angle is the trend the data proves, not the fact that you shipped a report, that distinction is what makes a journalist read past the subject line.

**You:** Write the pitch for the T1 reporter.

**Claude:**
```
Subject: [the data point itself]
3 sentences: the trend, your data, the ask.
Offer: exclusive first look for 48 hours.
Follow-up: +4 business days with one new stat, then +4 with a deadline, then stop.
```
Sharpener: connect a web-research step so the "why this reporter" line comes from what they actually published last month, not a guess at their beat, which is the difference between a pitch that reads personal and one that reads like a mail-merge.

## Go further
One pitch to one reporter proves the angle holds. Here's the version that keeps a real beat list current and the follow-ups on schedule.

- **Keep the beat list current automatically.** Run a web-research step weekly so the target list reflects who's covering the topic this month, not a list built once and left stale.
- **Draft and track from where you already work.** Connect an email tool so pitches and follow-ups draft as ready-to-review messages and open/reply status updates without a separate spreadsheet.
- **Never miss the follow-up window.** A scheduled Claude task checks FOLLOWUP_WINDOW against send date and queues the next touch with a new data point attached, capped at MAX_TOUCHES automatically.

The pitch earns the placement. The cadence is what keeps the relationship alive for the next one.

## Make it yours
Fork it. Change the beats, the tiers, the follow-up window, the definition of a story. The point is not to blast a press list. It is to earn a few real placements from people who actually cover your space. Built by an operator. Customize it, break it, make it better.

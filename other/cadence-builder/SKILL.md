---
name: cadence-builder
description: Turn a segment into a multi-touch, multi-channel cadence that holds together. Steps, timing, channel, and the intent of each touch, tuned to who you are chasing. No 12 identical emails. Built for B2B SDRs and sales teams, customizable to your segment, channels, and sequencer. Trigger on "build an outbound cadence", "design a sequence", "how many touches over how many days", "multi-channel cadence for this segment", or any sequence design task.
---

# Cadence-Builder

## What this does
Designs a full outbound cadence for a segment: how many touches, over how many days, on which channels, and what each touch is actually for. Every step has an intent, so the cadence builds a case across email, phone, and social instead of nagging the same person the same way eight times.

## What you'll need
You do not need to connect anything to get value today. Describe the segment and the channels you run, and it builds now. Connect the tools below and it grounds the cadence in real data and loads the steps for you.

- Works today with: a segment, your offer, and the channels you can actually run (email, phone, LinkedIn). Paste it and go.
- More powerful connected to a CRM: it reads segment history and past outcomes so the shape reflects what has worked, not a guess.
- Sharper with a sequencer: it loads the steps, channels, and timing straight into a sequence you can turn on.
- Sharper with an enrichment tool: pulls phone and social coverage so it only plans channels you can reach on.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you describe today and gets sharper as you connect tools. It never plans a channel it cannot see coverage for, and never invents a benchmark. A gap is a prompt, not a guess.

- **Bring your data**: describe the segment, offer, and channels. The skill designs the full cadence now, step by step.
- **Connect your tools**: the same skill reads history and coverage, tunes the shape, and loads the steps into your sequencer so it is ready to run.
- **Just exploring**: no segment yet? Get the cadence structure, the touch-intent map, and a worked example on a sample segment, so you see the shape before you build.

Every run ends with the one thing that would make the next cadence sharper, a channel to add or a tool to connect.

## Customize this for yourself
This was built for B2B outbound to a defined segment. Set these to your motion:

| Set this | What it is | Default / Example |
|---|---|---|
| SEGMENT | who this cadence targets | persona plus tier or fit |
| CHANNELS | what you can actually run | email, phone, LinkedIn, video |
| DURATION | how long the cadence runs | 14 to 21 days (re-tune) |
| TOUCH_COUNT | total touches across channels | 8 to 12 (re-tune to segment) |
| INTENSITY | how tightly touches cluster | front-loaded vs even |
| OFFER | the one problem you solve | stated in the buyer's words |
| SEQUENCER | where the steps run | a sequencer you already run |
| CRM | your CRM connector | a CRM you already run |

Build for any segment you like. A high-value segment earns more manual, personalized touches; a broad one runs lighter. The skill tunes the shape to the segment, not a fixed template.

## The method

### Every touch has an intent
No step exists just to hit a number. Each touch is tagged with its job: introduce the problem, add a proof point, change the channel, break the pattern, or make the graceful last ask. If a touch has no distinct intent, it gets cut, not padded.

### Multi-channel by design
The cadence spreads across the channels you actually run, so a prospect who ignores email might answer a call or a LinkedIn note. Channels reinforce each other: a call references the email, the social touch references both. One story, several doors.

### Timing and spacing
Touches cluster early when attention is freshest, then space out. The default runs 8 to 12 touches over 14 to 21 days, front-loaded, with room to breathe near the end. Segment sets the intensity: a strong-fit segment earns tighter, higher-effort touches; a broad one runs lighter and longer.

### Tune the effort to the segment
High-value segments get more manual, researched touches and fewer templated ones. Broad segments get efficient, repeatable steps. The skill sets the mix so you are not hand-writing a video for a low-fit lead or blasting a template at a must-win account.

### A clean ending
The last touch is an honest break-up: one graceful, low-pressure close that gives the prospect an easy exit and often earns a reply. No touch 13. No fake "final notice."

## Quality gates
- Every touch carries a distinct intent. No filler steps to pad a number.
- The cadence spans more than one channel wherever coverage exists.
- Touch effort matches segment value. No hand-crafted touches for low-fit leads, no pure templates for must-wins.
- The cadence ends with a clean break-up, never an endless nag.

## Output (example)
```
CADENCE · segment: mid-market RevOps · 10 touches / 18 days

Day  Channel    Intent
0    Email      Introduce the problem + soft CTA
1    LinkedIn   Connection request, no pitch
3    Phone      Reference the email, permission opener
5    Email      One proof point, new angle
7    LinkedIn   Value-first message (resource)
9    Phone      Second dial, different time of day
12   Email      Short case-style example
14   Video      Pattern break, personal 30-sec note
16   Phone      Last live attempt
18   Email      Graceful break-up, easy exit

Effort mix: 3 personalized touches (video, first email, breakup),
7 efficient templated touches. Tighten for higher-fit accounts.
```

## Example chat
Here is the skill designing a full cadence for a real segment.

**You:** Build an outbound cadence for mid-market RevOps. I can run email, phone, and LinkedIn. We cut manual follow-up.

**Claude:** Here's a 10-touch, 18-day cadence, front-loaded, with an intent on every step so it builds a case instead of nagging:

```
Day  Channel    Intent
0    Email      Introduce the problem + soft CTA
1    LinkedIn   Connection request, no pitch
3    Phone      Reference the email, permission opener
5    Email      One proof point, new angle
7    LinkedIn   Value-first message (a resource)
9    Phone      Second dial, different time of day
12   Email      Short case-style example
14   Video      Pattern break, 30-second personal note
16   Phone      Last live attempt
18   Email      Graceful break-up, easy exit
```

Effort mix: 3 personalized touches (the video, the first email, the break-up) and 7 efficient templated ones. The channels reference each other, so the day-3 call points back to the day-0 email. That's what makes it one story through several doors, not eight copies of the same knock.

**You:** This is a must-win segment. Tighten it.

**Claude:** For a must-win I'd raise the effort and cluster tighter: drop to 8 touches over 12 days, make 5 of them personalized (add a researched second email and a written-for-them LinkedIn note), and move the video earlier to day 6 so the pattern break hits while attention is still high. Same intent-per-touch logic, just more hand-work where the account is worth it.

One sharpener: connect your CRM and I'll shape the next one off what actually converted in this segment, and pull phone and social coverage so I only plan channels you can really reach them on.

## Where the inputs come from
SEGMENT, CHANNELS, and OFFER are yours to set; the 8-to-12 touches over 14-to-21 days and the front-loaded spacing are defaults that suited a mid-market motion, not laws. Longer enterprise cycles stretch the duration and thin the touches. The intent-per-touch logic holds. The inputs are yours.

## Go further
The design is step one. Here is where an operator takes it once the shape holds.

- **Ground the shape in what worked.** Connect Salesforce so the cadence reads the segment's past outcomes and weights the channels that actually convert, instead of a sensible default.
- **Only plan channels you can reach.** Wire an enrichment tool like Clay for phone and social coverage, so the cadence never schedules a dial for a number you don't have.
- **Load it and turn it on.** Push the steps, channels, and timing straight into your sequencer, so the design becomes a running sequence the same day instead of a doc someone has to rebuild by hand.

Build the intent map once and the cadence stops being a static template. It reshapes itself to the segment in front of it, then goes live where your team already sends.

## Make it yours
Fork it. Change the segment, the channels, the length, the intensity, the effort mix. The point is not to run someone else's sequence. It is to run yours, built for who you are actually chasing. Built by an operator. Customize it, break it, make it better.

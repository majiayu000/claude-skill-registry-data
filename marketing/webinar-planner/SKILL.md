---
name: webinar-planner
description: Plan a webinar end-to-end using April Dunford's Obviously Awesome positioning framework to find the topic angle that makes the webinar obviously valuable to the right audience. Produces topic positioning, abstract, speaker brief, registration page, promotion sequence, day-of run-of-show, and post-webinar follow-up. Use when the user asks to plan a webinar, virtual event, online workshop, "we need a webinar on X", host a webinar, online masterclass, or any live virtual event with promotion and follow-up. Reads ICP, services, and brand voice from knowledge/. For the promotion emails, see email-nurture. For the deck, see ppt-maker. For the social promotion plan, see social-calendar.
metadata:
  grounded_in:
    - "Obviously Awesome - Dunford"
  reads:
    - knowledge/brand/voice.md
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
    - knowledge/services/
    - knowledge/learnings.md
  writes:
    - output/webinar/
---

# webinar-planner

Plans a webinar as a campaign, not a one-off. Treats the live event as one moment in a multi-week arc: pre-event demand, live execution, post-event nurture. Before any of that, uses April Dunford's Obviously Awesome positioning framework to find the topic angle that makes the webinar obviously valuable to the right audience.

## When to use

- "Plan a webinar on <topic>"
- "We need a virtual event for <audience>"
- "Build a workshop on X"
- "Host a webinar with <partner or guest>"
- "Promote and run a masterclass"

## Framework: Obviously Awesome Positioning (April Dunford)

Most webinar topics compete in crowded ground: "Introduction to X", "Everything you need to know about Y", "The future of Z". These sound like every other webinar in the inbox and get ignored.

Dunford's argument in *Obviously Awesome*: positioning is context. It defines the lens through which everything else about the offering is understood, and getting it wrong makes every downstream decision harder. Her sharpest point for webinars is that **positioning is a deliberate choice, not a description of what you built**. Most teams inherit their webinar's positioning by accident, from the topic the speaker happened to want to talk about.

**The 5 components - apply to the webinar itself, not just the product:**

| # | Component | The question for a webinar | The failure when it is skipped |
|---|---|---|---|
| 1 | Competitive alternatives | What will they do instead of attending? | You compete with other webinars, when you actually compete with the browser tab they already have open |
| 2 | Unique attributes | What does this have that those do not? | The abstract lists topics, which every alternative also covers |
| 3 | Value | So what? What does each attribute enable? | Attributes are stated as features: "a panel of four experts" with no stated payoff |
| 4 | Target customer characteristics | Who cares most about that value, right now? | "For marketers" - so nobody self-selects, and registration comes from the existing list only |
| 5 | Market category | What frame makes the value obvious immediately? | Filed mentally as "another vendor webinar" in the first two seconds |

Dunford's sequence matters: components 1 to 3 must be answered before 4 and 5, because you cannot know who cares most about a value you have not defined. Working backwards from a title is the most common way this framework gets applied wrongly.

1. **Competitive alternatives**: What would the attendee do instead of attending this webinar? (Scroll LinkedIn? Read a blog post? Ask a colleague? Attend a competitor's event?) This is the real competition.

2. **Unique attributes**: What does this webinar offer that the alternatives don't? (Specific framework? Practitioner speakers who've done it, not just studied it? Live benchmarking? Proprietary data?)

3. **Value**: So what? For each unique attribute, what does it actually enable for the attendee? (Saves X hours, avoids Y mistake, gets them to Z outcome faster)

4. **Target customer characteristics**: Who specifically cares most about this value? Not "marketers" - which marketers, at which stage, with which problem, right now?

5. **Market category**: What frame of reference makes this webinar's value immediately obvious? (Not "a marketing webinar" - what specific context makes the target customer say "this is exactly for me"?)

**Positioning self-check**: Could this webinar title and topic be run by any of our competitors? If yes, it is not positioned - it is generic.

**Example of repositioning a topic:**
- Generic (red ocean): "Using AI in Marketing"
- Positioned (blue ocean): "How Series B marketing teams are cutting content production time by 60% without losing brand voice - a live walkthrough with 3 practitioners"

The second version signals: who it is for (Series B marketing teams), what they get (60% time reduction), the specific problem (losing brand voice), and the format (live, practitioners, not theorists).

## Inputs needed

- **Topic and angle** (required)
- **Audience persona** from `knowledge/icp/personas.md`
- **Goal**: pipeline gen, brand awareness, customer education, partner co-marketing, recruiting
- **Format**: solo talk, panel, fireside, workshop, customer story
- **Length**: 30, 45, 60 minutes (default 45)
- **Date and time** (DD-MM-YYYY, timezone)
- **Speakers**: name, role, company, prep notes
- **Registration platform**: Zoom, Webex, Hopin, Restream, etc.

## Gates before planning starts

A webinar has a hard, public date, so a missing input does not degrade the plan, it cancels it in public. Check these first and state what you found. The first three are stop conditions.

| Gate | Warning sign | Action |
|---|---|---|
| **Speaker confirmed in writing** | The plan names a speaker who has not confirmed the date | **Stop.** Do not build a promotion sequence around an unconfirmed name. Write `[NEEDS INPUT: written confirmation from <name> for <date>]` and plan the rest around a placeholder. An unconfirmed external or customer speaker is the single most common cause of a cancelled webinar |
| **Lead time** | Fewer than three weeks between today and the date | **Flag hard.** Three promo waves do not fit. Either move the date or cut to a single wave to the existing list and set expectations that registration will be a fraction of normal |
| **Someone owns the day-of operations** | No named host, moderator or producer | **Stop.** A speaker cannot present, watch chat, run polls and manage the recording at once. Name the second person or reduce the format |
| **Goal is measurable** | The goal is "thought leadership" | Flag. Rewrite as a countable outcome from `knowledge/kpis.md`, or the retro has nothing to judge |
| **Date collision** | Clashes with a major industry event, a public holiday in the target region, or the company's own launch | Flag and propose two alternative dates |
| **Topic has a real audience** | The topic came from what the speaker wants to talk about, not from a pain in `knowledge/icp/personas.md` | Flag before positioning work. Positioning cannot rescue a topic nobody has the problem for |

**Cancel or postpone rules.** Set these at planning time, not the week before, and write them into the README:

1. Set a go or no-go checkpoint at 7 days out, with a registration number the user chooses from their own prior webinars in `knowledge/learnings.md`. If there is no prior webinar, say there is no basis for a threshold and set the checkpoint as a judgement call with a named decision owner, rather than inventing a number.
2. If the speaker withdraws inside 7 days, the default is to postpone rather than substitute. A substituted speaker on a positioned topic breaks the positioning that drove registration.
3. If registration is below the checkpoint, postponing is usually better than running to an empty room, because the recording is the longest-lived asset and an empty-room recording is unusable.

## Process

1. **Load context.** Read brand voice, primary persona, positioning, learnings (especially any prior webinar retros).

2. **Complete positioning pre-work before choosing a title.** Work through all 5 Dunford components:

   ```
   ## Webinar positioning (Obviously Awesome framework)

   **1. Competitive alternatives**
   What will our target attendee do instead of attending this webinar?
   - Alternative 1: <e.g. read a blog post on the same topic>
   - Alternative 2: <e.g. ask a colleague who's done it>
   - Alternative 3: <e.g. attend a competitor's event>
   Why would they choose us instead? <specific answer>

   **2. Unique attributes**
   What does this webinar offer that those alternatives don't?
   - Attribute 1: <specific thing, e.g. "3 practitioners who've 10x'd pipeline sharing exact playbooks">
   - Attribute 2: <specific thing, e.g. "live Q&A with people who made the same mistakes">
   - Attribute 3: <specific thing>

   **3. Value (so what?)**
   For each unique attribute, what does it enable for the attendee?
   - Attribute 1 -> Value: <outcome, e.g. "walk away with a tested framework they can run next week">
   - Attribute 2 -> Value: <outcome>
   - Attribute 3 -> Value: <outcome>

   **4. Target customer characteristics**
   Who cares most about this value right now?
   - Role: <specific, e.g. "VP Marketing at Series B SaaS companies">
   - Situation: <specific, e.g. "first marketing hire, no established playbook">
   - Urgency: <what makes this matter now, e.g. "board has asked for pipeline targets 3x last quarter">

   **5. Market category**
   What frame of reference makes this value immediately obvious?
   - Category: <e.g. "pipeline generation for early-stage B2B" not "marketing webinar">
   ```

3. **Build the title using the positioning output.**

   Title formula: **[Specific value for specific audience] + [unique attribute or approach]**

   - Lead with the value or outcome (what the attendee gets)
   - Name the audience or situation (who this is for)
   - Include a differentiator (what makes this worth 45 minutes of their time)

   Generate 3 title options ranked by specificity. The most specific one wins.

   Bad title: "AI for Marketing Teams"
   Good title: "How we cut content review cycles from 2 weeks to 2 days - a live walkthrough for B2B content teams"

4. **Validate the topic.** Pressure-test:
   - Does the title pass the positioning self-check? (Could a competitor run this exact webinar with their branding? If yes, reposition.)
   - Is it specific enough that a busy person blocks 45 minutes?
   - Does it match a real pain in `knowledge/icp/personas.md`?
   - Is the title outcome-led? "How to <achieve outcome> in <timeframe>" beats "Introduction to X"

   If it fails any check, propose 3 repositioned alternatives before proceeding.

5. **Build the full webinar pack** in `output/webinar/<DD-MM-YYYY>-<slug>/`:

   ```
   output/webinar/25-04-2026-ai-marketing-stack/
   ├── README.md                    # the master plan
   ├── abstract.md                  # public-facing description
   ├── speaker-brief.md             # what speakers need to prepare
   ├── registration-page.md         # landing page copy
   ├── promotion-sequence/          # all promo assets
   │   ├── linkedin-posts.md        # 5-7 posts across 3 weeks
   │   ├── email-invites.md         # 3-email invite sequence
   │   ├── partner-co-marketing.md  # if partner involved
   │   └── ad-creative.md           # paid ads if budget
   ├── day-of/
   │   ├── run-of-show.md           # minute-by-minute timing
   │   ├── speaker-prep-checklist.md
   │   ├── poll-questions.md        # 3-5 audience polls
   │   └── chat-moderation-script.md
   └── follow-up/
       ├── attendee-email.md        # within 24 hours
       ├── no-show-email.md         # different message
       ├── nurture-sequence.md      # 3-email follow-up over 14 days
       └── recap-blog-post.md       # SEO content from the recording
   ```

6. **README.md (master plan)**:

   ```
   # Webinar: <Title>

   **Date**: DD-MM-YYYY HH:MM <TZ>
   **Format**: <solo|panel|fireside|workshop>
   **Length**: <minutes>
   **Speakers**: <names + roles>
   **Audience persona**: <from knowledge/icp/>
   **Goal**: <pipeline|awareness|education|co-marketing|recruiting>

   ## Positioning summary
   - **Target**: <specific audience from Dunford component 4>
   - **Competitive alternative**: <what they'd do instead>
   - **Unique value**: <what this webinar offers that alternatives don't>
   - **Category**: <frame of reference from Dunford component 5>

   ## Success metrics
   Every target must be this team's own prior figure with the source webinar named,
   or `[NEEDS INPUT]`. Registration-to-attendance rates vary enormously by audience,
   topic, timezone and list quality, so a remembered industry number is a fabricated one.
   - Registrations target: [NEEDS INPUT: prior webinar in knowledge/learnings.md]
   - Attendance rate target: [NEEDS INPUT]
   - Conversion target: <metric, e.g. demo bookings, MQLs> [NEEDS INPUT]
   - On-demand views target: [NEEDS INPUT]

   ## Go / no-go
   - Checkpoint date: -7 days
   - Registration figure at which we postpone: <chosen by the team from their own history>
   - Decision owner: <name>

   ## Timeline
   | Days out | Activity | Owner |
   |---|---|---|
   | -28 | Topic locked, speaker confirmed, page live | |
   | -21 | Promo wave 1 (LinkedIn, email) | |
   | -14 | Promo wave 2 + paid ads if budget | |
   | -7  | Promo wave 3 + partner push | |
   | -3  | Final push, reminder email 1 | |
   | -1  | Reminder email 2, speaker rehearsal | |
   |  0  | Live | |
   | +1  | Attendee + no-show emails | |
   | +3  | Nurture email 1, recap blog live | |
   | +7  | Nurture email 2, on-demand promo | |
   | +14 | Nurture email 3, retro | |
   ```

7. **Abstract must-include list** (for abstract.md):
   - Name the competitive alternative in the opening line: "Most teams are doing X by [alternative approach]. Here's a better way."
   - State the unique value explicitly: what specific outcome will attendees leave with?
   - Name the target customer characteristics: "This is for [specific role] dealing with [specific situation]."
   - End with a concrete deliverable: "You'll leave with [specific thing] you can use [specific timeframe]."

8. **Promotion sequence rules**:
   - Every promotional message leads with value, not features. "You'll learn how to X" not "we'll cover topic Y"
   - Each promo post names the target audience so the right people self-select
   - 7-10 LinkedIn posts across 3 weeks (use `/linkedin-post` for each)
   - 3 invite emails (initial, mid, last-call) (use `/email-nurture` patterns)
   - 2 reminder emails (day before, day of)
   - Partner co-marketing if applicable: dedicated assets they can paste into their channels
   - Paid ads only if there's budget (use `/ad-campaign-writer`)

9. **Day-of run-of-show** (minute by minute):

   ```
   00:00-00:02  Pre-roll: hold music + countdown timer
   00:02-00:05  Welcome + housekeeping (chat, Q&A, recording)
   00:05-00:10  Speaker intros + agenda
   00:10-00:30  Main content block 1
   00:30-00:32  Poll #1 + reaction
   00:32-00:55  Main content block 2
   00:55-00:58  Poll #2
   00:58-01:15  Q&A
   01:15-01:18  Recap + CTA + on-demand link
   01:18-01:20  Close
   ```

10. **Follow-up sequence**:
    - Attendee email (24h): thank you + recording + single CTA (book demo, download resource)
    - No-show email (24h): different copy, lead with "you missed this" + recording
    - Nurture day +3: deeper resource related to webinar topic
    - Nurture day +7: customer story or case study related to topic
    - Nurture day +14: direct ask (demo, trial, sales call)

11. **Self-check.** Every item is checkable against the saved files. Point at the file and line, or the item fails.

    - `README.md` contains all 5 Dunford components filled in, and each names something specific rather than a category word
    - The chosen title appears in the positioning section's output, and the file shows 3 ranked candidates with the ranking reason stated
    - Take the title, swap in a competitor's brand name, and read it back. If it still works, it is not positioned. Record that you ran this test and what the result was
    - The title names an audience or situation and an outcome. Point at the words that do each
    - `abstract.md` contains a sentence naming the competitive alternative, a sentence naming the target characteristics, and a sentence stating the concrete deliverable attendees leave with
    - Every outcome number in the title, abstract and registration page cites a file in `knowledge/services/` or is marked `[NEEDS INPUT]`. List each number and its source
    - The run-of-show segment durations sum to the booked length. Show the arithmetic
    - Q&A ends before the booked end time, with at least 2 minutes of buffer
    - Speaker confirmation status is recorded in `README.md` as confirmed with a date, or `[NEEDS INPUT]`. No promotion asset names an unconfirmed speaker
    - Promotion covers at least 3 channels, and the timeline has an owner cell filled for every row
    - The attendee and no-show emails differ in their opening line and their CTA. Compare them
    - Every registration and attendance target is this account's own prior figure with the source webinar named, or `[NEEDS INPUT]`. No benchmark from memory
    - Recording, captioning and on-demand hosting each have a named owner
    - All copy reads in brand voice

12. **Save** all files. Print the folder tree at the end.

## Rules

- Complete the Dunford positioning before picking a title. The positioning output determines the title, not the other way around.
- A webinar is a campaign, not an event. If you produce only the day-of plan, you've done 10% of the work.
- If the title could describe a competitor's webinar, it is not positioned. Reject it and reposition.
- Differentiate attendee vs no-show messaging. Treating them the same wastes the no-show segment.
- Always plan the recap content. The recording is reusable for 90+ days as on-demand content, blog post, social clips.
- Never overpromise. The title must match the actual content. Bait-and-switch destroys trust and kills future registration rates.
- Check `knowledge/learnings.md` for prior webinar retros. Apply what worked, drop what didn't.

## Run-of-show must match the booked length

The sample run-of-show is one shape, not the shape. Before handing it over, rebuild it to the
length actually chosen (30, 45 or 60 minutes) and check the segments sum to that number. Handing
speakers an 80-minute agenda for a 45-minute slot, with Q&A scheduled after the event ends, is a
live operational failure, not a wording issue.

## Never invent

- **Every outcome number in a title, abstract or registration page must come from
  `knowledge/services/` or a documented prior result.** If neither exists, describe the outcome
  qualitatively. The registration page is a public claim and in some sectors a regulated one.
- Specificity is the ranking criterion for titles, and invention is the cheapest route to it.
  Rank only among titles whose specifics you can source.
- Verify the chosen platform still supports the features you plan (polls, breakouts, on-demand).
  Platform capabilities and ownership change.

## What this skill cannot know

These are limitations of the skill, not of the event. Anything below that reaches the output must be labelled `[UNVERIFIED]` or `[NEEDS INPUT]` there.

- **Whether the named speakers have confirmed the date in writing.** This is the highest-consequence unknown in the file, because promotion is public and a withdrawal after promotion is visible to everyone who registered.
- **Current webinar platform feature sets, limits and pricing.** Polls, breakouts, registration fields, attendee caps, on-demand hosting and recording retention all change, and several are gated by plan tier. Check the account's actual plan, not the vendor's marketing page.
- **Realistic registration-to-attendance rate for this audience.** No number is given here for that reason. It depends on list quality, topic, timezone spread, reminder cadence and the season, and only this team's own prior events answer it.
- **Whether a customer or partner speaker has legal or PR clearance** from their own employer to appear and to say what the brief asks them to say. Their marketing team usually has to approve it, and that takes weeks.
- **Whether the date collides** with an industry event, a public holiday in the target region, or a competitor's announcement.
- **Whether recording, transcript retention and attendee data collection** comply with the privacy rules of every region the audience registers from.

## Related skills

- `/campaign-brief` when the webinar is one channel inside a wider campaign, so the goal and budget are set before the topic
- `/positioning-doc` when the Dunford pre-work keeps failing the competitor test, because the problem is company positioning rather than the topic
- `/email-nurture` for the invite, reminder and follow-up sequences, which have their own consent and cadence rules
- `/social-calendar` to book the promotion posts into the month rather than adding them on top of a full calendar
- `/linkedin-post` for each individual promotion post
- `/ad-campaign-writer` for paid registration ads, only where there is budget
- `/ppt-maker` for the deck, once the run-of-show fixes the segment timings
- `/case-study-writer` when a customer speaker's story is the real asset and outlives the event
- `/seo-article-writer` or `/content-repurposer` for the recap article and the clips cut from the recording
- `/retro` afterwards, to write registration, attendance and conversion into `knowledge/learnings.md` so the next webinar has a real threshold instead of a guess


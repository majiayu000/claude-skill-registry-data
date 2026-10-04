---
name: regen-event-blast
description: >
  Generate the cross-channel announcement blast for any ReGen Civics event:
  Festival, Open Access Session, season launch, Earth Day Convergence, Riverside
  call, quest unlock, deadline reminder. Produces forum announcement, newsletter
  section, Twitter/X thread, Instagram caption, LinkedIn post, Discord message,
  and reminder follow-up sequences. Voice-matched, all linking back to one
  canonical source. Triggers on: "event blast", "announce the event", "promote
  the [event]", "Festival announcement", "Open Access Session promo",
  "Earth Day promo", "season launch post", "deadline reminder", "RSVP push",
  "promote the call", or any request to publish across channels for an upcoming
  ReGen Civics event.
---

# ReGen Civics Event Blast

## What this skill does

Convert a single event brief into the seven artifacts needed to fill every
channel: forum, newsletter, Twitter, Instagram, LinkedIn, Discord, and the
reminder sequence that runs in the days before. All voice-matched. All
linking back to one canonical landing page (usually `/events/<slug>` or
`/schedule`).

Distinct from `regen-release-notes` (those are backward-looking, "here's
what shipped"). This is forward-looking, "here's what's coming, please show
up."

## Inputs the skill expects

A short brief from Rye covering:

- **Event name + type.** Festival, Open Access Session, Riverside call,
  season launch, deadline, etc.
- **Date and time.** Including time zone.
- **Format.** In-person, online, hybrid. If online: which platform
  (Riverside, Zoom, gov.regencivics.earth/Loomio, Discord stage).
- **Who it's for.** Players, land projects, investors, the whole movement.
- **The hook.** One sentence on why this one matters.
- **The CTA.** RSVP, register, claim a slot, drop into Discord, etc.
- **Canonical link.** The single URL we're driving people to.

If any of these are missing, ask Rye for them in one round of
AskUserQuestion before drafting.

## The seven artifacts

### 1. Forum announcement post

Long form, lives at `/community/announcements`. 200-400 words.

Structure:

```
# [Event name]: [date]

[Lead paragraph: what, when, why this one. 2-3 sentences.]

[Middle: who it's for, what to expect, what to bring (literal or
metaphorical). 1-2 short paragraphs.]

[Logistics: format, link, time zone, accessibility notes.]

[Close: real invitation. Not "stay tuned." Something like "Drop a reply
if you're coming or if you have questions."]

[Sign-off: Rye or whoever's hosting]
```

Forum posts get pinned. Use the `regen-database-sql` skill if direct
insertion into the forum DB is needed.

### 2. Newsletter section

100-200 words. Headline + 3-4 sentence body + button.

Newsletter readers are skim-reading. Don't bury the date. Don't bury the
link.

### 3. Twitter / X thread

5-8 tweets:

- **Tweet 1:** the hook. Names the event, date, why-now. Includes the
  canonical link OR teases a thread reveal.
- **Tweets 2-5:** specifics. Who, what, format. One concrete detail
  per tweet.
- **Tweet 6-7:** social proof / context. Quote a previous attendee, name
  a notable participant, share a number from a prior event.
- **Final tweet:** CTA. RSVP link, comment to register, DM for the
  invitation, etc.

Voice rules: no rocket emojis, no "this is HUGE," no "you don't want
to miss this." Match the forum voice. Twitter's just a thinner channel.

### 4. Instagram caption

90-150 words. Visual carries most of the work; caption sets the frame.

Pattern: hook line + one paragraph context + concrete CTA + 3-5 hashtags.

Hashtag set we use (rotate, don't all-at-once):
`#regenerativerenaissance #regencivics #bioregional #regenerativefinance
#regenerativeculture #livingsystems #thecommunal #healingtheearth
#regenerativetech`

Add 1-2 event-specific tags (#earthday2026, #seasonlaunch, etc.).

### 5. LinkedIn post

200-350 words. LinkedIn rewards longer, narrative-driven posts. Use this
to pitch the event to the investor/partner/professional audience.

Pattern:

- Open with a real, specific observation (not a hot take, not a buzzword
  list)
- Connect that observation to the event
- Make the case for why this audience specifically should attend
- Close with the link and one specific question they could bring

Don't repost the Twitter thread to LinkedIn. Different audience, different
voice register.

### 6. Discord message

3-5 sentences. Casual. Includes the link, the time, and an `@here` if it
warrants attention.

If the event itself is happening on Discord (Stage), use `@everyone`
sparingly (community has Stage notification toggles, ping fatigue is
real).

### 7. Reminder sequence (5 sends)

Pre-event drumbeat. Email subject + body for each:

| When           | Channel                  | Subject / Lead                                  |
| -------------- | ------------------------ | ----------------------------------------------- |
| T-1 week       | Newsletter, forum bump   | "[Event] is one week out"                       |
| T-3 days       | Newsletter, Discord ping | "Three days until [event]. Final RSVP."         |
| T-1 day        | Email, Discord ping      | "Tomorrow at [time]: [Event]"                   |
| T-2 hours      | Discord, IG story        | "Starting in 2 hours: [event] [link]"           |
| Just-after     | Forum recap thread       | "What we covered + recording link"              |

For each reminder, repurpose the original messaging; don't write five
fresh versions of the same content. Use `regen-content-repurposing` to
adapt the source post to each cadence touch.

## Voice rules (binding)

- **No "save the date."** Tell them the date directly. Save-the-date is
  filler.
- **No "this is going to be epic / amazing / unforgettable."** Let the
  event speak for itself.
- **No "limited spots available!"** unless it's actually true. Then say
  exactly how many.
- **Real-time anchor.** Always include time zone. Use "Pacific" not "PT"
  if the audience is mixed (most newsletter readers don't know what PT is).
- **Calendar link.** Default to including an `.ics` link so people can
  add it to their calendar in one tap. The site already has a Google
  Calendar integration; piggyback on that.
- **Accessibility.** Note captions / recording / async access where it
  applies. Especially for deadline events ("can't make the call live?
  Submit your RSVP and we'll send the recording within 48 hours.")
- **Em-dashes banned.** Project rule.

## What to lift from the canonical landing page

If the event has a `/events/<slug>` page, all seven artifacts should
reference that page as the truth source. Don't restate the agenda in
five different formats; link to the agenda. The forum post is allowed
to summarize, the rest just point.

## After the event

Don't drop the artifact stream the moment the event ends. The recap is
part of the work:

- Forum recap post within 24 hours, with recording link
- Twitter "thanks for coming" tweet with one quote or insight from the
  event
- Newsletter blurb in the next issue: 2-3 sentences plus link to the
  recording

Use `regen-release-notes` for the recap if the event shipped a feature
or made a decision; use this skill's "after the event" pattern if it was
purely a gathering.

## Cross-references

- `regen-content-repurposing` for cadence-specific adaptations
- `regen-database-sql` for forum post insertion
- `regen-outreach-sequences` for the email reminder sequence
- `client/src/pages/events.tsx` and `client/src/pages/SchedulePage.tsx`
  for where the canonical landing page lives
- The webhook receiver in `server/webhooks/` for Zoom/Riverside recording
  ingestion (so the recap post can pull the recording URL)

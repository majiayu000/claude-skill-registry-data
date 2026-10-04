---
name: vabene-interview-finder
description: >-
  Find Reddit users worth interviewing for JTBD customer development.
  Score posts for interview-worthiness, draft personalized outreach DMs,
  and send candidates to Telegram for review. Never message anyone automatically.
  Two profiles: `pain` (default — planning-pain language) and `switching`
  (operational complaints about incumbents like venue lead forms).
version: "1.2.0"
author: ben
requires:
  tools:
    - bash
    - telegram
triggers:
  - "find interviews"
  - "find interviewees"
  - "interview scan"
  - "find people to interview"
  - "custdev scan"
  - "who should I talk to"
  - "find switchers"
  - "switching scan"
---

# VaBene Interview Candidate Finder

## Purpose

Surface Reddit users who are actively experiencing celebration-planning pain
and would be valuable JTBD interview candidates. Draft a personalized outreach
DM for each and send to Telegram for Ben to review and send manually.

**Hard rule: this skill NEVER messages anyone on Reddit. All outreach is
manual by the human after reviewing the Telegram draft.**

---

## Profiles: `pain` vs `switching`

This skill ships with two interview-target profiles. Same fetch architecture, same scoring scaffold, different keyword anchoring and slightly different DM framing.

| Profile | What it surfaces | Triggered by |
|---|---|---|
| `pain` (default) | Planning-pain venting — "nightmare," "fell apart," "gave up," "wish there was" | `find interviews`, `interview scan`, `custdev scan`, `who should I talk to` |
| `switching` | Operational complaints about incumbents — venue lead forms, deposit terms, ghosting, slow quotes | `find switchers`, `switching scan` |

### Why two profiles

The `pain` profile finds people venting about planning being hard. The `switching` profile finds people venting about a *specific incumbent's process* — the dominant incumbent for SF self-host celebrants is the venue's own lead form (which, for most SF venues, runs on TripleSeat or Perfect Venue). Switching language sounds like *"I emailed five places and only two got back"*, not *"this is so stressful."* Both are good interview targets but the conversations go different directions.

### `switching` profile keywords (operational pain — not brand names)

When the trigger is `switching scan` or `find switchers`, override the include keyword set with operational complaints:

```
I emailed,emailed five places,emailed all the places,only got back,never heard back,
the deposit terms,the deposit was insane,deposit terms were shocking,
waited weeks for a quote,waited a week for,no quote yet,still no response,
the contact form,contact form went nowhere,inquiry form was useless,
ghosted me,ghosted us,ghosted after the deposit,
lead form was a black hole,form felt like a black hole,
no one answers the phone,nobody picks up the phone,can't get anyone on the phone,
hour minimum just to ask,hour minimum to inquire,
venue rentals are impossible,booking a venue is impossible,
every place wants a $,5K minimum,10K minimum,wants a huge minimum,
they only respond if you spend,had to chase them down,
inquired but never heard,sent inquiries to,
buyout minimum,F&B minimum,site fee
```

### OpenTable / venue-marketplace switching keywords (ADDED post-v4)

Per v4 research, only 1 of 540 Reddit pain posts mentioned OpenTable — meaning **every fresh OpenTable mention in a planning context is a premium interview lead** (the rare user who knew the marketplace existed and tried it for groups). Add these to the switching profile:

```
tried OpenTable for the group,tried OpenTable for our party,
OpenTable doesn't do groups,OpenTable's private dining,
OpenTable for a party,OpenTable for our birthday,
booked through OpenTable but,the OpenTable form,
OpenTable group reservation,OpenTable couldn't handle,
called the restaurant directly because OpenTable,
Resy doesn't do private,tried Resy for our group,
Tock private dining,Tock for our party
```

### Brand-name complaints — kept but **secondary**

References to The Bash, Peerspace, GigSalad, Eventbrite, WeddingWire, The Knot vendor side, Partyslate, etc. still count as positive signal under the `switching` profile, but downweight (+0.5 instead of +1) — research consistently shows the bigger volume of pain is about the long tail of venue lead forms, not the marketplace brands.

### DM framing differences

- **`pain` profile DM**: "I saw your post about [SITUATION] — I'm building an app for that…"
- **`switching` profile DM**: leads with the *specific incumbent process* the person complained about — "I saw you emailed five places and only got two back — that's exactly what I'm trying to fix…"

Otherwise the templates and consent framing remain the same as `pain`.

---

## What Makes Someone Worth Interviewing

Not every person complaining about party planning is a good interview.
The best candidates have multiple of these signals:

| Signal | Why It Matters | Weight |
|--------|---------------|--------|
| **Recency** (posted < 7 days) | Still in the planning cycle, will remember details | Required |
| **High severity pain** | Strong emotions = rich interview | High |
| **Identifiable trigger event** | "turning 30", "engagement" = actively planning | High |
| **Named a workaround** | "we tried Partiful", "group chat is chaos" = tried things | High |
| **Bad outcome** | "trip fell through", "it was a disaster" = strongest motivation to talk | Highest |
| **Wish statement** | "I wish there was..." = already reflecting on what should exist | Medium |
| **Detailed post** (100+ words) | Longer posts = more reflective person = better interviewee | Medium |
| **Multiple comments** | Engaged in discussion = more likely to respond to DM | Low |
| **Habitual-planner identity** | "I'm always the planner," "I'm the planner friend" = recurring role, not one-off pain. Premium archetype with the most lived experience to extract. | Highest |

### Scoring

Score each post 0-7:
- +1 if severity seems high (strong negative language, specific failures described)
- +1 if a trigger event is identifiable (milestone birthday, engagement, someone leaving)
- +1 if they name a tool/workaround they tried (Partiful, group chat, spreadsheet, hired someone)
- +1 if the outcome was bad or the event was abandoned
- +1 if they have a wish statement or express what should exist
- +1 bonus if post is 150+ words with specific details (causal language, not pablum)
- **+1 habitual-planner identity** ("I'm always the planner," "I'm the planner friend," "everyone always asks me," "tired of being the one organizing," "every single time it's me," etc.). Stacks with trigger-event signal — a habitual planner currently planning a milestone birthday is doubly high-signal.

**Minimum score to surface: 3/7.** Below that, too thin for a useful interview. Habitual-planner identity alone (no current event signal) is worth surfacing if score ≥3 — they're venting about the role itself, which is the JTBD interview goldmine.

---

## Target Subreddits

VaBene is **group celebration / private experiences** (milestone birthdays, engagement parties, anniversary dinners, going-away parties, baby showers, reunions) — *not* wedding planning. Wedding-adjacent surfaces are excluded because pain in those threads is wedding pain, which VaBene's product does not address.

### Primary (every run) — Where celebration-host pain shows up

- r/AskWomen
- r/AskWomenOver30
- r/SanFrancisco, r/AskSF, r/bayarea — SF launch market, every run

### Secondary (every other run) — Broader planning pain

- r/Parenting (baby shower / kids-birthday host pain)
- r/Mommit
- r/travel (group-trip coordination)
- r/relationships (group friction during planning)
- r/TwoXChromosomes

### Wrong product fit, banned, or dead — DO NOT scan

- **r/weddingplanning, r/BachelorettePlanning, r/wedding** — wedding planning is structurally different from group-celebration hosting; pain in these threads is wedding pain. Hard-excluded.
- r/Bachelorette — TV show, not planning
- r/MaidOfHonor, r/GirlsTrip — banned by Reddit
- r/birthdays — celebration-of-self, not planning-for

### Pain-specific queries for r/all (every run)

These catch posts in niche subs you'd never think to monitor. Queries focus on celebration-host pain, NOT wedding pain:

```bash
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "30th birthday planning nightmare group fell apart" --limit 10
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "engagement party planning stress gave up" --limit 10
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "milestone birthday planning disaster nobody committed" --limit 10
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "private dining group reservation impossible to coordinate" --limit 10

# Habitual-planner identity — "the friend who plans everything." Premium
# JTBD interview candidates (most lived experience to extract).
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "always the one planning friend group tired" --limit 10
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "I'm the planner friend everyone asks me" --limit 10
```

---

## Queries — Pain Language, Not Recommendation Seeking

The vabene-reddit-monitor skill looks for people seeking recommendations
(acquisition leads). This skill looks for people experiencing pain
(interview candidates). Different queries.

**Include keywords** (pain signals):
```
nightmare,disaster,fell apart,gave up,nobody committed,so stressful,
never again,ruined,chaos,impossible to coordinate,lost money,
spent hours,exhausted,resentful,embarrassed,wish there was,
someone should build,why is this so hard,worst part was
```

**Exclude keywords** (wrong context — wedding-PLANNING is NOT VaBene's product, but bach weekends ARE):
```
my wedding,our wedding,wedding venue,wedding budget,
wedding planner,wedding date,ceremony,vows,reception,officiant,
registry,save the date,bridal shower,bridal brunch,
RSVPs to the wedding,RSVP'd to the wedding,
vendor,florist,caterer,photographer,DJ,dress,cake,
recipe,decoration,DIY,craft,
Gabby Windey,Jenn Tran,rose ceremony,this season,
tonight's episode,The Bachelorette,bachelor nation
```

Note: `bach`, `bachelorette`, `bach party`, `bachelor party`, `groomsmen`, `bridal party`, `MOH`, `maid of honor` are NOT in this list — bach weekends are real group celebrations VaBene serves. They are allowed but secondary; primary signal is celebration-host pain (milestone birthday, engagement, anniversary, etc.) and the **habitual-planner identity** archetype (see "Habitual planner" trigger below).

---

## Workflow

### Step 1 — Fetch candidate posts

Use TWO strategies: browse recent posts (catches everything new) AND search for pain keywords (catches older high-signal posts).

**Strategy A: Search celebration-host pain in primary subs.**
These subs cover the celebration-host audience without being wedding-shaped.

```bash
# AskWomen variants — search within them to filter to celebration-host pain
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search AskWomen \
  "30th 40th birthday party planning group stress" --limit 15

node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search AskWomenOver30 \
  "milestone birthday engagement party anniversary group stress" --limit 15

# SF launch-market city subs — celebration intent in real planning posts
for sub in SanFrancisco AskSF bayarea; do
  node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search "$sub" \
    "30th birthday engagement party private dining group" --limit 10
done
```

**Strategy B: Search r/all for celebration-host pain language.**
Catches posts in niche subs you'd never think to monitor. Queries deliberately avoid wedding/bachelorette context — those produce wrong-product-fit candidates.

```bash
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "30th birthday planning nightmare nobody committed" --limit 10

node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "engagement party planning disaster gave up" --limit 10

node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "milestone birthday group trip fell apart" --limit 10

node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "private dining group reservation impossible to coordinate" --limit 10

# Habitual-planner identity — premium archetype, often venting about the role
# itself rather than a single event.
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "always the one planning friend group tired" --limit 10

node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs search all \
  "tired of being the one organizing everything" --limit 10
```

**Filtering:** From all results, keep only posts from the last 7 days. Discard anything older. The `posts` command returns creation timestamps — check them.

### Step 2 — Read full thread for top candidates

For any post that looks promising from title/snippet, fetch the full thread:

```bash
node {baseDir}/../reddit-readonly/scripts/reddit-readonly.mjs thread \
  <post_id|url> --commentLimit 30 --depth 3
```

Reading the full post + comments is essential for scoring. A title like
"birthday planning help" could be pablum or could contain a 400-word
story about a coordination disaster. You need the body.

### Step 3 — Score each post

Read the full post text and score 0-7 using the criteria above.
Only surface posts scoring 3+.

For each qualifying post, extract:
- **Trigger event**: what life event kicked this off?
- **Current workaround**: what are they using now? (group text, Partiful, spreadsheet, delegated to someone, nothing)
- **What went wrong**: the specific failure or pain
- **Emotional tone**: stress, resentment, embarrassment, overwhelm?

### Step 4 — Draft outreach DM

**Voice rules for DMs:**
- Lead with their specific situation (proves you read their post)
- Be honest: "I'm building an app for group event planning"
- Ask for 15 minutes of their time
- Offer compensation ($20 gift card)
- Sound like a founder, not a researcher
- Under 5 sentences
- No exclamation marks
- Never mention "JTBD", "customer development", or "research sprint"

**Template — customize heavily to each post:**

> Hi! I saw your post about [SPECIFIC SITUATION from their post]. I'm
> building an app specifically for [THEIR EVENT TYPE] planning — the
> coordination/booking part that seems like it was [THEIR SPECIFIC PAIN].
> Would you be open to a 15-min call? I'm trying to understand what
> actually goes wrong when groups try to plan together. Happy to send a
> $20 [Amazon/Starbucks] gift card for your time.

**Customize based on what you extracted:**

- **If they're planning for a partner (modal scenario per v4 — 41% of for-others posts)**: "It sounds like you're trying to make [PARTNER]'s [MILESTONE] memorable — I'd really like to hear what felt like the hardest part of pulling it together for them."
- If they named a workaround: "I saw you tried [TOOL] — I'd love to hear what worked and what didn't about it"
- If the event was abandoned: "It sounds like [EVENT] didn't end up happening — I'd really like to understand what the breaking point was"
- If they expressed a wish: "You mentioned wanting [THEIR WISH] — that's exactly what I'm trying to figure out how to build"
- If they delegated: "It sounds like [PERSON] ended up taking it over — I'm curious what made you want to hand it off"
- If they mentioned OpenTable (rare and high-signal — only 1 of 540 in v4): "I noticed you mentioned trying OpenTable — I'd really like to understand what made you reach for it (and whether it ended up working for the group case)."

### Step 5 — Send to Telegram

One message per qualifying candidate:

```
🎯 Interview Candidate — r/[SUBREDDIT]

📌 "[POST TITLE]"
👤 u/[USERNAME] | Posted: [X days ago] | Score: [N]
🔗 https://reddit.com[PERMALINK]

📊 Interview Score: [X]/7
  • Trigger: [trigger event or "not identified"]
  • Workaround: [what they're using or "not identified"]  
  • Pain: [one-line summary of what went wrong]
  • Outcome: [happened well / went badly / abandoned / unclear]

💬 Draft DM:
---
[DRAFTED DM TEXT]
---

Copy DM → open reddit.com[PERMALINK] → click username → Send Message
```

**If no qualifying candidates found**: send a single summary:
```
🎯 Interview scan complete — no candidates scored 3+ today.
Scanned [N] posts across [M] subreddits.
Closest miss: "[TITLE]" (score 2, missing [WHAT]).
```

**Also write per-candidate MEMORY.md entries** (one JSONL line per qualifying lead) so `vabene-interview-recruiter` can pick them up. See "Memory Tracking" below for the schema. Compute `lead_id` from the post URL using the cross-skill contract; set `outcome: "pending"` on first write.

---

## Memory Tracking

Append-only JSONL — one or more lines per run. Two entry kinds:

### Per-candidate entry (one per qualifying lead surfaced this run)

Written alongside the per-candidate Telegram dispatch in Step 5. Lets `vabene-interview-recruiter` consume `outcome: "pending"` leads and de-duplicate against `vabene-reddit-monitor` via `lead_id`.

```jsonl
{"schema_version":"0.1","ts":"2026-04-26T09:00:00-07:00","scan":"interview-finder","lead_id":"a3f1b2c4d5e6","outcome":"pending","profile":"pain","score":4,"lead_url":"https://reddit.com/r/AskSF/comments/abc123/...","subreddit":"AskSF","post_title":"Planning my friend's 30th, group chat is dead","post_snippet":"first ~200 chars of body","trigger_event":"30th birthday milestone","workaround":"group chat","pain_summary":"nobody replies, planner is doing all the labor","outcome_summary":"abandoned"}
```

Field reference:

- `schema_version` — always `"0.1"` from this skill at v1.1.0.
- `ts` — ISO 8601 with PT offset.
- `scan` — always `"interview-finder"`.
- `lead_id` — see "Lead ID contract" below. Cross-skill dedup with `vabene-reddit-monitor` and `vabene-interview-recruiter`.
- `outcome` — always `"pending"` on first write. Recruiter and downstream skills append separate `recruiter`-scan entries with state transitions; never edit-in-place.
- `profile` — `"pain"` or `"switching"`.
- `score` — 0–7 from the rubric.
- `lead_url`, `subreddit`, `post_title`, `post_snippet` — for the recruiter to draft outreach without re-fetching.
- `trigger_event`, `workaround`, `pain_summary`, `outcome_summary` — extracted in Step 3, used as DM context.

### Per-run summary entry (one per run)

```jsonl
{"schema_version":"0.1","ts":"2026-04-26T09:00:00-07:00","scan":"interview-finder-run","profile":"pain","fetched":85,"surfaced":3,"top_subs":["AskWomen","AskSF","AskWomenOver30"],"event_types":["30th birthday","engagement party","group trip"],"closest_miss_score":2,"notes":""}
```

Note: `scan` is `"interview-finder-run"` (not `"interview-finder"`) so recruiter and digest queries that filter `scan == "interview-finder"` won't accidentally pick up summary entries.

### Lead ID contract

`lead_id` is the first 12 hex characters of `sha256(normalized_url)`, where `normalized_url` is:

- Lowercase host (`reddit.com`, not `Reddit.com` or `www.reddit.com`)
- Reddit canonical post ID extracted: `reddit.com/r/<sub>/comments/<id>` (drop everything after the post ID, including comment slug, query string, anchor, trailing slash)

This is a cross-skill contract shared with `vabene-reddit-monitor` and `vabene-interview-recruiter`. If upstream emits a hash with different normalization, the recruiter will treat the same URL as two leads. Fix at the source.

### Track over time

- Which subreddits produce the best interview candidates (per-candidate entries × `subreddit`)
- Conversion: how many `outcome: "pending"` leads progress to `outcome: "interviewed"` via recruiter (cross-reference by `lead_id`)
- Patterns in what scores 4+ vs 3
- Pain-vs-switching profile yield comparison (run both occasionally; compare candidates surfaced per run)

---

## Cron Setup

Interview candidates don't expire as fast as promotional leads.
Once daily is sufficient.

```bash
# Daily scan, 9am PT
openclaw cron add \
  --name "VaBene Interview Finder" \
  --cron "0 9 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the vabene-interview-finder skill. Scan all target subreddits for interview candidates, score posts, draft outreach DMs, send qualifying candidates to Telegram. Never message anyone automatically." \
  --model claude-sonnet-4-6 \
  --announce \
  --channel telegram
```

Uses Sonnet (not Haiku) because scoring and DM drafting require nuance.
The monitor skill can use Haiku for simple fetch+filter, but interview
scoring needs to distinguish pablum from causal language.

Verify: `openclaw cron list`

---

## Manual Telegram Commands

- `find interviews` — full scan with `pain` profile (default)
- `interview scan` — same as above
- `custdev scan` — same as above
- `who should I talk to` — same as above
- `find switchers` — full scan with `switching` profile (operational-pain incumbents)
- `switching scan` — same as `find switchers`

---

## Relationship to vabene-reddit-monitor

These are sibling skills with different goals:

| | reddit-monitor | interview-finder |
|---|---|---|
| **Goal** | Find leads to promote VaBene to | Find people to learn from |
| **Output** | Public reply draft (promotional) | Private DM draft (research) |
| **Scoring** | Planning intent + recency | Pain severity + workaround + outcome |
| **Frequency** | Every 2 hours | Once daily |
| **Model** | Haiku (simple filter) | Sonnet (nuanced scoring) |
| **Queries** | "planning, recommendations, help" | "nightmare, disaster, gave up, chaos" |
| **Window** | 36 hours | 7 days |

A post can qualify for both — someone asking for recs while describing
pain is both a lead and an interview candidate. That's fine. The outputs
don't conflict.

---

## Security

- Read-only Reddit access. No credentials required.
- No user PII stored in MEMORY.md (usernames and permalinks only).
- All Telegram messages route through your existing bot.
- DMs are drafted only — never sent automatically.

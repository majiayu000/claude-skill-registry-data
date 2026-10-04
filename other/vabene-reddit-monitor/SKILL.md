---
name: vabene-reddit-monitor
description: Find Reddit posts where someone is doing planning labor for a group celebration and is stuck. Draft a planner-pain-framed reply for each qualifying post and surface to Telegram for manual approval. Never posts automatically.
version: "2.2.0"
author: ben
requires:
  tools:
    - bash
    - telegram
triggers:
  - "scan reddit"
  - "check reddit leads"
  - "run lead scan"
  - "vabene monitor"
  - "scan sf"
  - "scan birthdays"
  - "scan trips"
  - "scan engagements"
  - "scan dining"
  - "scan bach"
  - "scan habitual"
  - "find planner friends"
  - "lead stats"
---

# VaBene Reddit Lead Monitor

## Purpose

Find Reddit posts where a real person is doing the planning labor for a group celebration and is stuck — not enough hours, too many opinions, decisions piling up, group chat dying. Draft a planner-pain-framed reply for each qualifying post and surface it to Ben via Telegram for approval before any posting happens.

The user we serve is the **planner-friend**: the person who got handed the to-do list, has the group chat, and is going to be the one who books. The activity is not the pain. The coordination is the pain. Replies should speak to that.

**Hard rule: this skill NEVER posts to Reddit automatically. All posting is manual by the human after reviewing the Telegram draft.**

---

## Prerequisites

This skill invokes the sibling skill `reddit-readonly` for all Reddit fetches. Verify it's installed before any run:

```bash
openclaw skills list | grep reddit-readonly
```

If missing, this skill produces zero leads silently — no error, no Telegram alert. On a fresh host (e.g., DigitalOcean droplet migration), install it before deploying this skill. Step 1 below has an existence check that hard-fails if the scraper is missing, but the check only fires once a scan begins.

---

## Architecture: city-sub-only

VaBene's product is **group celebration / private experiences** (milestone birthdays, engagement parties, anniversary dinners, going-away parties, baby showers, reunions, AND bach weekends/bachelor weekends — these last two are real group celebrations VaBene can serve, just not the strategic wedge) — *not* wedding planning. Wedding-PLANNING surfaces (r/weddingplanning) and wedding-planning posts ("my wedding," "ceremony," "registry," "save the date") are hard-excluded because the product doesn't address wedding pain. Bach/bachelorette content is *allowed but de-prioritized* via a +1 wedding-adjacent celebration trigger — bach posts surface but score lower than milestone-birthday / engagement-party leads with equivalent coordination signal.

The viable signal source is **city subreddits filtered for celebration planning intent** — posts like "turning 30 in SF, 8 of us, what should we do" appear in r/AskSF, not r/weddingplanning. Additionally, **habitual-planner identity language** ("I'm always the one planning," "I'm the planner friend," "everyone always asks me") is a +1 modifier that boosts the highest-LTV lead archetype: the friend who plans everything for their group. Volume will be low (0–3 qualifying posts/day is normal); precision is the priority over recall.

---

## Target Subreddits

### Tier 1 — City subs, every run (SF-first)

These run every cron tick. SF and SF-adjacent are highest priority because SF is the launch market.

- r/SanFrancisco
- r/AskSF
- r/bayarea

### Tier 2 — City subs, every other run

Lower priority. Scanned alternating runs to keep volume manageable.

- r/LosAngeles
- r/AskLosAngeles
- r/Nashville
- r/LasVegas
- r/Austin
- r/Scottsdale

### Tier 2.5 — v2 expansion-readiness (NYC), low priority

Per v4 research, NYC has 5× the Reddit volume of SF (96 vs 18 birthday-vendor items). NYC is the explicit v2 expansion target — too soon to GTM in (founder lives in SF), but worth tracking now to (a) measure NYC demand growth and (b) build a backlog of NYC venues + planners for the v2 launch.

These subs run on the SAME alternating ticks as Tier 2, but with smaller `maxResults` so SF signal continues to dominate the Telegram feed:

- r/AskNYC
- r/FoodNYC
- r/Brooklyn

Add them to the Tier 2 fetch block with `--perSubredditLimit 8 --maxResults 4`. If a NYC lead surfaces, prefix the Telegram message with `[NYC v2-expansion]` so it's visually distinct from SF leads (and doesn't get acted on as if it were an immediate v1 priority).

### Tier 3 — High-volume general subs, every other run, strict filtering

Big subs with rich planner-pain content but high noise. Aggressive include filtering required (see Step 1).

- r/AskWomen
- r/AskWomenOver30
- r/travel

### Wrong product fit, banned, or dead — DO NOT scan

Documented here as a tripwire so future iterations don't reintroduce them:

- **r/weddingplanning — wrong product fit.** Wedding planning is structurally different (year-long, vendor-heavy, ceremony-centered). Posts here scored as HIGH leads in past runs but the replies don't make sense for VaBene. Hard-excluded.
- **r/BachelorettePlanning — wrong product fit + nearly dormant.** Bachelorette planning is wedding-adjacent. Volume is also near-zero (most recent post Oct 2025).
- r/Bachelorette — TV show, not planning
- r/MaidOfHonor — banned by Reddit
- r/GirlsTrip — banned by Reddit
- r/Bridesmaid — dead/banned
- r/dirtythirty — banned by Reddit (keyword still useful, see below)
- r/birthdays — celebration-of-self, not planning-for
- r/turning30 — dead community (one post in 18+ months; keyword still useful)

---

## Two-axis scoring

Each post gets a numeric score. Tiers are derived from the score.

### Hard exclusions — pre-scoring

If ANY of these terms appear in the post title or body, return excluded immediately. No scoring runs.

- **Wedding-planning context** (the post is about *planning a wedding itself*, not a wedding-adjacent group celebration like a bach weekend): my wedding, our wedding, wedding venue, wedding budget, wedding planner, wedding date, ceremony, vows, reception, officiant, registry, save the date, save-the-date, RSVPs to the wedding, RSVP'd to the wedding, bridal shower, bridal brunch
- **Note**: `bach`, `bachelorette`, `bach party`, `bachelor party`, `groomsmen`, `bridal party`, `MOH`, `maid of honor` are NOT in this list — bach weekends are real group celebrations VaBene can serve. They are scored at +1 (wedding-adjacent group celebration) rather than +2 (main celebration trigger), so they surface but don't dominate over milestone-birthday / engagement-party / anniversary leads. See "Score components" below.
- vendor, florist, caterer, photographer, DJ, dress fitting, dress alterations
- Gabby Windey, Jenn Tran, rose ceremony, this season, tonight's episode
- bachelornation, bachelor nation
- `episode \d+`, `season \d+`, `ep \d+` (regex — catches "episode 7", "season 12", "ep 3" regardless of capitalization)
- hometowns this week, fantasy suite, final rose

Capitalization-based detection of "The Bachelorette" was removed in 2.0.1: a real bach-party post could plausibly capitalize the word, while the patterns above catch the actual TV-context signals (subreddit name, episode/season references, in-show language) more reliably.

These kill the post regardless of other signals. Vendor posts and TV-show crossposts are not VaBene leads under any score combination.

### Score components

- **+2** Main celebration trigger keyword present in title or body. These are the strategic-wedge celebrations VaBene leads with. Triggers include:
  - Birthdays: birthday, bday, 30th, 35th, 40th, 50th, milestone birthday, milestone bday, dirty 30, dirty thirty, fab 40, the big 5-0, the big 3-0, round-number birthday, turning 30, turning 40
  - Group trips: girls trip, girlfriends trip, ladies trip, group trip, friends trip, weekend trip, the crew, my crew
  - Other celebrations: engagement party, just got engaged, anniversary dinner, anniversary trip, big anniversary, baby shower, sprinkle, going-away party, going away party, retirement party, promotion party, friend reunion, college reunion, family reunion
  - Private experience signals (high VaBene fit): private dining, private room, buyout, bar buyout, private event space, group dinner reservation, party of 8 or more, party of 10, party of 12, party of 15, party of 20, large group reservation

- **+1** Wedding-adjacent group celebration trigger. These are real group celebrations VaBene can serve (bach weekend = group trip + private experience), but get a smaller bump than the main celebration triggers above so milestone-birthday / engagement-party leads outrank them when coordination-pain is otherwise equal. Triggers:
  - bach, bach party, bach weekend, bachelorette, bachelorette party, bachelorette weekend, bachelor party, bachelor weekend, bridal party (the group, not "bridal shower" — that's wedding-planning hard-excluded)

  Note: a wedding-adjacent post needs *additional* signal (group size, SF, decision-pending, or coordination pain) to reach HIGH. A bare "Planning my friend's bach" only gets +1 + +2 (planner identity) = 3 = MED, so it surfaces flagged but not as a top-priority lead.

- **+2** Coordination-pain phrase present. The post must show the person is doing planning labor and stuck. Phrases include:
  - Planner identity: "I'm planning," "I'm in charge of," "I'm the planner," "I'm the host," "everyone keeps asking me," "I'm the one organizing," "MOH," "maid of honor" (planner role, frequently the bach organizer)
  - Group friction: "trying to coordinate," "everyone has different opinions," "can't get the group to agree," "group chat is dead," "nobody will commit," "playing mediator"
  - Decision-pending: "haven't booked yet," "still need to decide," "we need to figure out," "need to nail down," "haven't picked"
  - Frustration: "wish there was an easier way," "drowning in options," "this is so much work," "more work than I thought"

- **+1** Explicit group size of 3 or more. Examples: "8 of us," "10 girls," "the whole group," "12 people," "all my college friends"

- **+1** Decision-pending language present. **Decision-pending posts have the highest VaBene fit** — a phrase like "haven't booked yet" deliberately counts in both this axis AND the +2 coordination-pain axis. Do not "fix" this dual-counting; it's the highest-signal pattern in the rubric.

- **+1** SF or SF-adjacent. Either the post is in r/SanFrancisco, r/AskSF, or r/bayarea, or the body explicitly names SF, San Francisco, the Bay Area, or a SF neighborhood (Marina, Mission, Hayes Valley, etc.).

- **+1** Habitual-planner identity. The post indicates the author is the *recurring* planner for their friend group, not just stuck on one event. Highest-LTV lead archetype — "the friend who plans everything." Phrases include:
  - "I'm always the planner," "I'm the planner friend," "I'm the planner of the friend group"
  - "always the one planning," "always end up organizing," "I always end up doing this"
  - "everyone always asks me," "everyone keeps asking me"
  - "tired of being the planner," "tired of being the one"
  - "why am I always [doing this/the one/planning]," "every single time it's me," "it always falls on me"

  This stacks with the per-event coordination-pain trigger: a post that's both ("I'm always the planner AND I'm drowning in this current bach") legitimately gets both bumps because the lead is doubly high-signal — habitual planner + active pain.

- **+1** Devoted Partner identity. The post indicates planning is *for* a romantic partner's celebration, not for self or generic group. Per v4 research, this is the modal "for-others" persona — 41% of all for-others planning posts in the corpus reference a partner/spouse. Higher emotional stakes + higher willingness-to-pay than friend-group equivalents. Phrases include:
  - "for my wife," "for my husband," "for my partner," "for my spouse," "for my SO"
  - "for my boyfriend," "for my girlfriend," "for my fiancé," "for my fiancée"
  - "my husband's [N]th," "my wife's [milestone]," "my partner is turning"
  - "throwing a [bday/dinner/party] for my [partner/wife/husband]"
  - "planning [bday/dinner/party] for my [partner/wife/husband]"

  Stacks with main celebration trigger and SF score. Example: "Planning my wife's 40th in SF" → +2 (milestone) +1 (SF) +1 (Devoted Partner) = **4 = HIGH**, even with no explicit pain phrase. This is the modal v4 buyer.

- **−2** Soft penalty for gray terms. Reduces score but does not auto-exclude. Terms: drama, toxic, registry, ceremony order, dress code, save the date, save-the-date, table assignments

### Tiers

- **HIGH** — score 4 or higher
- **MED** — score 2 or 3
- **Excluded** — score below 2

### Tier semantics — read this

The math means a celebration trigger is effectively required, but pain language is not strictly required if the post has enough supporting signal. Concretely:

- "Turning 30 in SF, 8 of us, looking for ideas" → main celebration (+2) + group size (+1) + SF (+1) = **4 = HIGH**, even with no explicit pain phrase. This is correct — that's a real VaBene lead.
- "Need a private room in SF for 12 of us, friend's engagement party" → main celebration (+2, "engagement party" + "private room") + group size (+1) + SF (+1) = **4 = HIGH**.
- "I'm MOH planning my friend's bach in Nashville for 10 of us, drowning in venues" → wedding-adjacent celebration (+1, "bach") + pain (+2, "MOH" + "drowning") + group size (+1) = **4 = HIGH**. Bach posts can reach HIGH but need extra signal beyond the trigger; a bare "planning my friend's bach" without group size or pain stays MED.
- "I'm always the planner friend and I'm doing it again for my friend's 30th in SF" → habitual planner (+1) + main celebration (+2) + SF (+1) = **4 = HIGH**. The "friend who plans everything" archetype — premium lead even without explicit current-event pain because they'll plan many more events.
- "Anyone have ideas for a 30th birthday in SF" → main celebration (+2) + SF (+1) = **3 = MED**. No group size, no pain, no decision-pending. Borderline; surfaces but flagged MED.
- "Looking for a wedding photographer in Austin" → vendor hard-exclusion → **excluded immediately**.
- "I'm planning my wedding helpp" / "drowning planning my wedding" → wedding-planning context hard-exclusion → **excluded immediately**, regardless of coordination-pain signal. Wedding planning is not VaBene's product. Note: this excludes wedding-PLANNING posts, not bach-weekend posts that incidentally mention "the wedding" (e.g. "bach for my friend before her wedding" — `the wedding` alone is not in the hard-exclude list anymore).

To restore strict two-axis behavior (require both celebration AND pain to reach HIGH): raise the HIGH floor from 4 to 5. That's the primary tuning knob.

---

## Workflow

### Step 1 — Fetch candidate posts

Per-call sub batching: maximum **4 subs per find call**. If a call returns an error or 404 for a specific sub, drop that sub from the batch and retry. This limits silent-degradation blast radius when a sub gets banned.

**Tier 2 city subs and Tier 3 high-volume general subs run on alternating cron ticks:**

- Tier 2 (Other city subs: LA, AskLosAngeles, Nashville, Vegas, Austin, Scottsdale) runs when hour ∈ {8, 12, 16, 20}
- Tier 3 (High-volume general: AskWomen, AskWomenOver30, travel) runs when hour ∈ {10, 14, 18, 22}

This alternation halves the per-run sub count for these tiers, keeping rate-limit headroom while still scanning each every 4 hours. Tier 1 (SF) runs every tick.

```bash
# Verify reddit-readonly is available — fail loudly instead of silently producing 0 leads
SCRAPER="$HOME/.openclaw/workspace/skills/reddit-readonly/scripts/reddit-readonly.mjs"
if [[ ! -f "$SCRAPER" ]]; then
  echo "ERROR: reddit-readonly skill missing at $SCRAPER. Cannot proceed." >&2
  # Telegram-alert the human; do NOT silently produce 0 leads
  exit 1
fi

# Wedding-PLANNING context hard exclusions — narrow to wedding-planning specific
# (bach/bachelorette terms intentionally NOT excluded — those are wedding-adjacent
# group celebrations VaBene can serve, scored at +1 instead of +2 in the rubric)
WEDDING_EXCLUDE="my wedding,our wedding,wedding venue,wedding budget,wedding planner,wedding date,ceremony,vows,reception,officiant,registry,save the date,save-the-date,bridal shower,bridal brunch,RSVPs to the wedding,RSVP'd to the wedding"
TV_EXCLUDE="Gabby Windey,Jenn Tran,rose ceremony,this season,tonight's episode,bachelornation,bachelor nation,episode \\d+,season \\d+,ep \\d+,hometowns this week,fantasy suite,final rose"
VENDOR_EXCLUDE="vendor,florist,caterer,photographer,DJ,dress fitting,dress alterations"
ALL_EXCLUDE="$WEDDING_EXCLUDE,$TV_EXCLUDE,$VENDOR_EXCLUDE"

# Main celebration include keywords (+2 in scoring) — strategic-wedge celebrations
MAIN_CELEBRATION_INCLUDE="birthday,30th,35th,40th,50th,milestone,milestone birthday,dirty 30,turning 30,turning 40,fab 40,big 5-0,big 3-0,engagement party,just got engaged,anniversary dinner,anniversary trip,big anniversary,baby shower,sprinkle,going-away party,going away party,retirement party,promotion party,family reunion,college reunion,friend reunion,girls trip,girlfriends trip,group trip,friends trip,weekend trip,the crew,my crew,private dining,private room,bar buyout,buyout,private event space,group dinner reservation,party of 8,party of 10,party of 12,party of 15,party of 20,large group reservation"

# Wedding-adjacent celebration include keywords (+1 in scoring) — surface but don't dominate
ADJACENT_CELEBRATION_INCLUDE="bach,bach party,bach weekend,bachelorette,bachelorette party,bachelorette weekend,bachelor party,bachelor weekend"

PAIN_INCLUDE="I'm planning,I'm in charge of,I'm the host,I'm the planner,MOH,maid of honor,trying to coordinate,everyone has different opinions,can't get the group to agree,group chat is dead,nobody will commit,playing mediator,haven't booked,still need to decide,need to figure out,need to nail down,wish there was,drowning in options,this is so much work"

# Habitual-planner identity (+1 modifier) — the "friend who plans everything" archetype.
# These are premium VaBene leads (highest LTV — they'll plan many events) and premium
# JTBD interview candidates. Surfaces independently of any single event being planned.
HABITUAL_PLANNER_INCLUDE="I'm always the planner,I'm the planner friend,always the one planning,always end up organizing,everyone always asks me,everyone keeps asking me,I always end up doing this,I always have to plan,why am I always,tired of being the planner,tired of being the one,it always falls on me,every single time it's me,planner of the friend group"

# Aggregate include for tier scans
ALL_INCLUDE="$MAIN_CELEBRATION_INCLUDE,$ADJACENT_CELEBRATION_INCLUDE,$PAIN_INCLUDE,$HABITUAL_PLANNER_INCLUDE"

# Tier alternation by hour (PT)
HOUR=$(TZ=America/Los_Angeles date +%H)
case "$HOUR" in
  08|12|16|20) RUN_TIER2=true;  RUN_TIER3=false ;;
  10|14|18|22) RUN_TIER2=false; RUN_TIER3=true  ;;
  *)           RUN_TIER2=false; RUN_TIER3=false ;;  # manual run, neither alternating tier
esac

# Tier 1 — SF batch — every run
node "$SCRAPER" find \
  --subreddits "SanFrancisco,AskSF,bayarea" \
  --query "30th 40th birthday engagement party anniversary private dining group" \
  --include "$ALL_INCLUDE" \
  --exclude "$ALL_EXCLUDE" \
  --minScore 1 \
  --maxAgeHours 36 \
  --perSubredditLimit 15 \
  --maxResults 12 \
  --rank new

# Tier 2 — Other city subs — alternating runs only
if [[ "$RUN_TIER2" == "true" ]]; then
  node "$SCRAPER" find \
    --subreddits "LosAngeles,AskLosAngeles,Nashville,LasVegas" \
    --query "30th 40th birthday engagement party anniversary private dining group" \
    --include "$ALL_INCLUDE" \
    --exclude "$ALL_EXCLUDE" \
    --minScore 1 \
    --maxAgeHours 36 \
    --perSubredditLimit 12 \
    --maxResults 8 \
    --rank new

  node "$SCRAPER" find \
    --subreddits "Austin,Scottsdale" \
    --query "30th 40th birthday engagement party anniversary private dining group" \
    --include "$ALL_INCLUDE" \
    --exclude "$ALL_EXCLUDE" \
    --minScore 1 \
    --maxAgeHours 36 \
    --perSubredditLimit 12 \
    --maxResults 6 \
    --rank new

  # Tier 2.5 — NYC v2-expansion-readiness (low priority — surface but don't dominate)
  # Per v4 findings, NYC has 5x SF Reddit volume but is v2 expansion, not v1 GTM.
  # Smaller per-sub + maxResults to keep SF signal dominant in the Telegram feed.
  node "$SCRAPER" find \
    --subreddits "AskNYC,FoodNYC,Brooklyn" \
    --query "30th 40th birthday engagement party anniversary private dining group" \
    --include "$ALL_INCLUDE" \
    --exclude "$ALL_EXCLUDE" \
    --minScore 1 \
    --maxAgeHours 36 \
    --perSubredditLimit 8 \
    --maxResults 4 \
    --rank new
fi

# Tier 3 — High-volume general subs — alternating runs only
if [[ "$RUN_TIER3" == "true" ]]; then
  node "$SCRAPER" find \
    --subreddits "AskWomen,AskWomenOver30,travel" \
    --query "30th 40th milestone birthday engagement anniversary private dining group" \
    --include "$ALL_INCLUDE" \
    --exclude "$ALL_EXCLUDE,solo trip,traveling alone,backpacking solo" \
    --minScore 2 \
    --maxAgeHours 36 \
    --perSubredditLimit 10 \
    --maxResults 5 \
    --rank new
fi
```

If Reddit rate-limits you, slow down with:
```bash
export REDDIT_RO_MIN_DELAY_MS=800
export REDDIT_RO_MAX_DELAY_MS=1800
```

If a sub returns an error, log the failure to {baseDir}/MEMORY.md and continue with remaining subs. Do not let one banned sub kill the whole batch.

### Step 2 — Score each candidate

For each fetched post:

1. Run hard exclusion check (vendor, TV-show, ceremony-logistics terms). If any present, mark excluded and move on.
2. Compute score per the rubric above.
3. Determine tier (HIGH if score ≥ 4, MED if score 2–3, excluded if < 2).
4. For posts that pass scoring, also extract:
   - **Celebration type** (milestone birthday, engagement party, anniversary dinner, baby shower, going-away party, group trip, reunion, etc.)
   - **Group size** if mentioned
   - **City or region** if mentioned
   - **Decision-pending detail** — what specifically hasn't been decided yet

### Step 3 — Check thread for VaBene mentions and competitors

```bash
node ~/.openclaw/workspace/skills/reddit-readonly/scripts/reddit-readonly.mjs thread \
  <post_id|url> --commentLimit 50 --depth 3
```

Skip if VaBene already mentioned in the thread. Log competitor mentions to {baseDir}/MEMORY.md for tracking. Tracked competitors:

- **Coordination layer**: Partiful, Hobnob, Evite, The Bash
- **Venue marketplace**: OpenTable (incl. their Sept 2025 private-dining marketplace), Resy, Tock, Tripleseat, Peerspace
- **Restaurant infrastructure (back-end)**: SevenRooms — tracked because users may credit the venue's tooling to a brand they don't see
- **Other / experiences**: Airbnb Experiences, Viator, GetYourGuide, Batch

The OpenTable mention pattern is highest-signal: per the v4 research findings, only 1 of 540 Reddit pain posts mentioned OpenTable (0.2%), and only 3 of 3,689 OpenTable reviews mentioned private dining (0.08%). Each fresh OpenTable mention in a planning post is a goldmine — it's the rare user who knows the marketplace exists.

### Step 4 — Draft a reply

**Voice rules — planner-pain framing:**

- Lead with the coordination pain, not the activity discovery
- The reader is the planner-friend; speak to them, not to "your group"
- Mention VaBene once, naturally, as a tool that helped
- Link to https://vabene.app
- Under 4 sentences
- Max one exclamation point
- Never say "full disclosure," "I work for," "as the founder"
- Never claim a specific personal experience that isn't yours — generic empathy ("planning anything for a group is a lot") is fine; fabricated specifics ("when I planned my sister's bach in Nashville last spring") are not

**Templates — pivot from "your group can browse" to "you don't have to be the bottleneck":**

MILESTONE BIRTHDAY (highest priority — SF wedge):
> "The hardest part of planning a milestone birthday isn't picking the activity — it's getting eight people with eight schedules to commit to anything. [VaBene](https://vabene.app) is built for the planner-friend doing the labor: put options in, the group votes, you book what wins. Cuts the back-and-forth."

PARTNER MILESTONE (Devoted Partner persona — premium lead, use when the post is explicitly "for my [partner/wife/husband/SO]"):
> "Planning a milestone for someone you love is its own version of hard — the activity is the easy part, but coordinating eight friends so the surprise actually happens is what eats your week. [VaBene](https://vabene.app) is built for the planner doing the labor: options in, group votes, you book what wins. Worth a look if you're trying to make this one count."

GROUP TRIP / GIRLS TRIP:
> "Group trips are amazing until you're three weeks deep in a group chat trying to nail down one restaurant. [VaBene](https://vabene.app) is built for the person organizing — options in, votes out, decisions made. Worth a look if you're the one carrying it."

BABY SHOWER:
> "Baby showers are deceptively hard because you're juggling friend-group A, friend-group B, family, and timing — and the person hosting ends up doing all of it. [VaBene](https://vabene.app) lets you put activity ideas in and have guests weigh in before you book, so it's not all on you."

BACH WEEKEND / MOH (lower priority — only use when post is clearly a bach weekend or trip, NOT wedding-day planning):
> "Being MOH and wrangling 8 people's opinions about the bach weekend while the bride pretends she 'doesn't care' is its own job. [VaBene](https://vabene.app) helps with exactly that part — you put activity options in, everyone votes, decisions get made. Saves a lot of group-chat back-and-forth when you're the one organizing."

HABITUAL PLANNER ("the friend who plans everything" — premium lead, use when habitual-planner identity is explicit):
> "Being the friend who plans everything is its own kind of job — and the part that wears people down isn't picking the activity, it's running a group chat as a one-person decision committee. [VaBene](https://vabene.app) is built specifically for that: options in, everyone votes, you book what wins. Worth a look if you're tired of being the bottleneck."

ENGAGEMENT / ANNIVERSARY / REUNION:
> "The friend who plans everything for the group always ends up doing more than they signed up for — the activity is fine, the coordination is the problem. [VaBene](https://vabene.app) is built for that: planner puts options in, everyone votes, you book what wins. Worth a look if you're the one in charge."

GENERIC PLANNER-PAIN (use when celebration type is unclear but planner-pain is high):
> "Being the friend who plans everything is a lot, and the part that breaks people isn't the activity itself — it's getting eight schedules and eight opinions to converge. [VaBene](https://vabene.app) is built for exactly that. Might be worth a look if the coordination piece is what's killing you."

Customize each template to the specific post — drop in the city, the group size, the celebration type, the specific decision they're stuck on. A template that reads as a template gets ignored.

### Step 5 — Send to Telegram

One message per qualifying post:

```
🦞 VaBene Lead — r/[SUBREDDIT]

📌 "[POST TITLE]"
👤 Posted: [X hours ago] | Score: [REDDIT_SCORE] | Comments: [N]
🔗 https://reddit.com[PERMALINK]

📊 Lead score: [X]/7
  • Celebration: [TYPE] (+2)
  • Pain language: [present / absent] ([+2 or 0])
  • Group size: [N or "not mentioned"] ([+1 or 0])
  • Decision-pending: [yes / no] ([+1 or 0])
  • SF-adjacent: [yes / no] ([+1 or 0])

📝 Draft reply:
[DRAFTED REPLY TEXT]

✅ approve (copy + paste to post manually) | ❌ skip
Tier: [HIGH/MED] | Event type: [TYPE]
```

If no qualifying posts found: stay silent (do not send a "0 leads" message — Lead Digest cron handles daily summaries). Log scan to {baseDir}/MEMORY.md.

**Also write per-lead MEMORY.md entries** (one JSONL line per qualifying post, HIGH or MED). These entries are how `vabene-interview-recruiter` finds candidates worth drafting outreach for, and how cross-skill dedup against `vabene-interview-finder` works (same `lead_id` for the same post URL). See "Memory Tracking" below.

---

## Memory Tracking

Append-only JSONL — multiple entry kinds per run. All entries carry `schema_version: "0.1"`.

### Per-lead entry (one per qualifying post — new in v2.1.0)

```jsonl
{"schema_version":"0.2","ts":"2026-04-26T20:00:00-07:00","scan":"reddit-monitor","lead_id":"a3f1b2c4d5e6","outcome":"pending","tier":"HIGH","score":5,"lead_url":"https://reddit.com/r/SanFrancisco/comments/abc123/...","subreddit":"SanFrancisco","post_title":"Planning my wife's 30th in SF, 8 of us, looking for ideas","post_snippet":"first ~200 chars of body","celebration_type":"milestone birthday","celebrant_relationship":"partner","group_size":8,"city":"San Francisco","decision_pending":"haven't booked yet","competitor_mentions":[]}
```

Field reference:

- `schema_version` — `"0.2"` (bumped from `"0.1"` when `celebrant_relationship` was added). `lead stats` queries should accept both.
- `ts` — ISO 8601 with PT offset.
- `scan` — always `"reddit-monitor"` for per-lead entries.
- `lead_id` — see "Lead ID contract" below. Cross-skill dedup with `vabene-interview-finder` and `vabene-interview-recruiter`.
- `outcome` — always `"pending"` on first write. Recruiter and downstream skills append separate `recruiter`-scan entries with state transitions; never edit-in-place.
- `tier` — `"HIGH"` or `"MED"` (excluded posts don't get persisted per-lead).
- `score` — numeric score from the rubric.
- `lead_url`, `subreddit`, `post_title`, `post_snippet` — for the recruiter to draft outreach without re-fetching.
- `celebration_type`, `group_size`, `city`, `decision_pending` — extracted in Step 2 step 4, used as DM context.
- **`celebrant_relationship`** — one of `"partner"` | `"friend"` | `"family"` | `"self"` | `"ambiguous"`. Per v4 research, "partner" is the modal value (41% of for-others posts) and the highest-LTV interview/buyer signal. Used downstream for cohort analysis (which celebrant relationship converts best to interview / signup).
- `competitor_mentions` — competitors named in this specific post (per-thread mentions go in the per-run summary).

### Per-run summary entry (one per run — existing schema, now `schema_version`-stamped)

```jsonl
{"schema_version":"0.1","ts":"2026-04-26T20:00:00-07:00","scan":"reddit-monitor-run","fetched":42,"qualifying":3,"high":1,"med":2,"subreddit_yield":{"SanFrancisco":{"f":15,"q":1},"AskSF":{"f":12,"q":2},"bayarea":{"f":15,"q":0}},"trigger_pattern_yield":{"celebration+pain+group":2,"celebration+SF+group":1},"competitor_mentions":["Partiful"],"notes":""}
```

Note the rename: `scan` is `"reddit-monitor-run"` (not `"reddit-monitor"`) so recruiter and digest queries that filter `scan == "reddit-monitor"` won't accidentally pick up summary entries when iterating per-lead. Existing pre-v2.1.0 entries in MEMORY.md still have `scan: "reddit-monitor"` for the run summary — `lead stats` jq queries should accept both during the transition.

Field reference (unchanged from v2.0.1):

- `fetched` / `qualifying` / `high` / `med` — counts for this run
- `subreddit_yield` — per-sub `{f: fetched, q: qualifying}`
- `trigger_pattern_yield` — `{combo_name: count}` where combo_name is `+`-joined axis hits ("celebration+pain+group", "celebration+SF+group", "celebration+pain", etc.)
- `competitor_mentions` — array of competitor names seen in scanned threads
- `notes` — freeform observation (banned-sub events, unusual patterns)

### Lead ID contract

`lead_id` is the first 12 hex characters of `sha256(normalized_url)`, where `normalized_url` is:

- Lowercase host (`reddit.com`, not `Reddit.com` or `www.reddit.com`)
- Reddit canonical post ID extracted: `reddit.com/r/<sub>/comments/<id>` (drop everything after the post ID, including comment slug, query string, anchor, trailing slash)

This is a cross-skill contract shared with `vabene-interview-finder` and `vabene-interview-recruiter`. If upstream emits a hash with different normalization, the recruiter will treat the same URL as two leads. Fix at the source.

`lead stats` parses with `jq`. Note the v2.1.0 rename: per-run summaries are now `scan: "reddit-monitor-run"`, with `scan: "reddit-monitor"` reserved for per-lead entries. The query below accepts both for backward compatibility with pre-v2.1.0 entries (which used `"reddit-monitor"` for run summaries):

```bash
# 7-day summary — accept both legacy and v2.1.0 summary scan tags
tail -200 {baseDir}/MEMORY.md | jq -s '
  map(select((.scan == "reddit-monitor-run") or (.scan == "reddit-monitor" and .qualifying != null)))
  | {runs: length, total_qualifying: (map(.qualifying) | add), total_high: (map(.high) | add)}'

# Per-lead pending leads (v2.1.0+) — for recruiter consumption / debugging
tail -500 {baseDir}/MEMORY.md | jq -s '
  map(select(.scan == "reddit-monitor" and .lead_id != null and .outcome == "pending"))
  | length'
```

Track over time:
- **Subreddit yield** — which subs actually produce qualifying leads. After 2 weeks, prune subs with zero `q`.
- **Trigger-pattern yield** — which keyword combinations surface real leads. Lets you tune the include list empirically instead of guessing.
- **Competitor mentions** — Partiful, Batch, etc. — surfaces emerging competitive pressure.
- **Banned-sub events** — if a previously working sub starts returning errors, log to `notes` and flag for sub-list review.

---

## Cron Setup

Already configured. For reference / re-creation:

```bash
# Every 2 hours, 8am–10pm PT
openclaw cron add \
  --name "VaBene Reddit Scan" \
  --cron "0 8,10,12,14,16,18,20,22 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the vabene-reddit-monitor skill. Scan all target subreddits per the city-sub-first architecture, score posts, draft replies, send qualifying to Telegram for approval. Do not post anything automatically." \
  --model claude-haiku-4-5-20251001 \
  --to <TELEGRAM_CHAT_ID> \
  --announce \
  --channel telegram
```

Verify: `openclaw cron list`

---

## Manual Telegram Commands

| Command | Subs scanned | Filter applied |
|---------|--------------|----------------|
| `scan reddit now` | All tiers per architecture | Default include keywords |
| `scan sf` | r/SanFrancisco, r/AskSF, r/bayarea | Default include + SF-only score boost |
| `scan birthdays` | All tiers | Filter for milestone-birthday triggers only (30th, 40th, dirty 30, fab 40, big 5-0, milestone) |
| `scan trips` | All tiers | Filter for group-trip triggers only (girls trip, group trip, friends trip, weekend trip) |
| `scan engagements` | All tiers | Filter for engagement-party / anniversary triggers |
| `scan dining` | All tiers | Filter for private-dining / private-room / buyout triggers |
| `scan bach` | All tiers | Filter for bach/bachelorette weekend triggers (lower-priority secondary stream) |
| `scan habitual` / `find planner friends` | All tiers + r/all | Filter for habitual-planner identity language ("I'm always the planner," etc.) — highest-LTV archetype |
| `lead stats` | None — reads {baseDir}/MEMORY.md | 7-day JSONL summary via jq |
| `pause reddit monitor` | None — disables cron | — |
| `resume reddit monitor` | None — re-enables cron | — |

---

## Tuning levers (in priority order)

When iterating on this skill, tune in this order:

1. **HIGH score floor** — currently 4. Raise to 5 if Telegram is too noisy. Lower to 3 if too quiet. Single biggest knob.
2. **Hard exclusion list** — add new kill-words when a category of false positive surfaces. The current list catches vendor and TV-show; expand if a new pattern appears.
3. **Include keyword coverage** — if real leads are slipping through with no score signal, the include list needs new keywords. Add and re-run.
4. **Subreddit list** — last resort. Add or remove subs based on 2-week yield data, not gut feel. Don't add a sub without data showing it'll produce leads.

Do not change scoring weights without writing down why in {baseDir}/MEMORY.md and the skill's README change-log. Weights are easy to fiddle and hard to reason about retroactively.

---

## Relationship to vabene-interview-finder

Sibling skill, different goal:

- This skill (reddit-monitor) finds **leads to reply to publicly** — people stuck in planning who'd benefit from VaBene as a tool.
- Interview-finder finds **research candidates to DM privately** — people experiencing planning pain who'd be valuable JTBD interview subjects.

A post can qualify for both. That's fine — the outputs go to different Telegram message formats and don't conflict.

When interview-finder gets its rewrite (deferred), the scoring scale in this skill should be unified across both for consistency.

---

## Security

- Read-only Reddit access. No credentials required.
- {baseDir}/MEMORY.md stores post titles and permalinks only — no usernames extracted, no real names, no message bodies. **Note**: titles + permalinks are still sufficient to identify the original poster via Reddit's UI; treat {baseDir}/MEMORY.md as containing soft-PII and don't share it externally.
- All Telegram messages route through the configured bot.
- No automatic posting to Reddit. All replies are drafted only; human approves and posts manually.

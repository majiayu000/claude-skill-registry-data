---
name: social-calendar
description: Plan a monthly content calendar across channels using the Content Marketing Matrix (Dave Chaffey, Smart Insights) - Entertain/Inspire/Educate/Convince. Every post gets a quadrant label. The monthly calendar must hit 40% Educate, 40% Inspire+Convince, 20% Entertain. Produces a week-by-week posting schedule with topics, formats, channels, and asset links. Use when the user says "content calendar", "social calendar", "plan next month's content", "what should we post", "content plan", "editorial calendar", "schedule posts for the month", or wants a structured posting plan for LinkedIn, Twitter, email, or blog. Reads brand voice, ICP, and past learnings from knowledge/. For writing the individual posts, see linkedin-post, newsletter-writer or content-writer. For the campaign this sits inside, see campaign-brief. For the end-of-month review, see retro.
metadata:
  grounded_in:
    - "Content Marketing Matrix - Chaffey"
  reads:
    - knowledge/brand/voice.md
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
    - knowledge/services/
    - knowledge/content-library/
    - knowledge/learnings.md
    - knowledge/kpis.md
  writes:
    - output/social-calendar/
---

# social-calendar

Plans a full month of content across channels. Every post has a job tied to a business goal and a quadrant in the Content Marketing Matrix. No random posting. No quadrant over-concentration.

## Framework: Content Marketing Matrix

### The 2x2 Matrix (Dave Chaffey, Smart Insights)

Chaffey's Content Marketing Matrix exists to answer one question that a list of post ideas never answers: **is this month's content actually capable of producing the outcome the month is being judged on?** A calendar can be full, on-brand, and well written, and still sit entirely in one quadrant, in which case it can only produce one kind of result.

Map content by two axes:
- X axis: Emotional (left) to Rational (right) - does it appeal to feelings or logic?
- Y axis: Awareness (top) to Purchase (bottom) - is it for new audiences or ready-to-buy?

The 4 quadrants:

| Quadrant | Axes | Purpose | Content types | Primary metrics |
|---|---|---|---|---|
| **ENTERTAIN** | Emotional + Awareness | Build brand affinity through personality | Behind-the-scenes, culture, storytelling, humor | Reach, shares, followers |
| **INSPIRE** | Emotional + Purchase | Drive action through aspiration and proof | Case studies, testimonials, transformation stories | Demo requests, trial signups |
| **EDUCATE** | Rational + Awareness | Build authority through useful information | How-to guides, research, explainer posts, frameworks | Saves, newsletter signups, shares |
| **CONVINCE** | Rational + Purchase | Close through logic and proof | Comparison posts, ROI data, product demos, pricing | Conversions, trial starts |

### Placing a post in the matrix

Two questions, in order. Do not skip to the label.

1. **Does this post argue, or does it make them feel something?** Argue (data, steps, comparison, proof) is the rational half. Feel (story, personality, aspiration) is the emotional half.
2. **Could someone act on this today, or is it for someone who does not know they have the problem?** Act today is the purchase half. Does not know yet is the awareness half.

Ambiguity is normal. When a post genuinely straddles two quadrants, assign it the one it is being **measured** on, and note the second in brackets. A customer story assigned to INSPIRE but measured on saves is really EDUCATE, and counting it as INSPIRE hides a proof gap.

### The 40/40/20 Rule
- 40% EDUCATE: builds the audience that buys
- 40% INSPIRE + CONVINCE combined: drives conversions
- 20% ENTERTAIN: builds the human brand people trust

This split is a default, and the default is derived from the goal, not the other way round. Adjust it deliberately, state the adjustment in the calendar summary, and never adjust it silently:

| Month's goal | EDUCATE | INSPIRE | CONVINCE | ENTERTAIN | Why |
|---|---|---|---|---|---|
| Default / mixed | 40% | 20% | 20% | 20% | Balanced pipeline and audience |
| Awareness or new audience | 50% | 15% | 5% | 30% | Nobody is ready to buy yet, so CONVINCE spends attention for nothing |
| Demand gen / pipeline | 30% | 30% | 30% | 10% | Proof and logic carry the month |
| Launch or event | 25% | 25% | 40% | 10% | CONVINCE is the point, but proof must carry it or it reads as noise |
| Retention or community | 35% | 25% | 5% | 35% | Existing customers do not need convincing, they need reasons to stay |

### Warning Signs
Flag these in the calendar summary if they appear, in this priority order. The first two are stop conditions: raise them and get a decision before finalising the calendar.

| Warning sign | What it means | Action |
|---|---|---|
| **0% INSPIRE** | No social proof anywhere in the month | **Stop.** This is the most common and most expensive gap in a B2B calendar. If no proof asset exists to point at, that is the real finding. Say so and mark the slots `[NEEDS PROOF]` |
| **>60% in any one quadrant** | The calendar can only produce one kind of result | **Stop.** Rebalance before writing week by week, not after |
| **<10% EDUCATE** | No authority building, so the audience has no reason to follow | Flag and propose which posts to convert |
| **>60% CONVINCE** | Audience fatigue, which shows up as falling engagement before it shows up as falling conversion | Flag. Convert the weakest CONVINCE posts to EDUCATE with the same proof point |
| **>60% ENTERTAIN** | Brand awareness with no path to pipeline | Flag against `knowledge/kpis.md` and ask whether that is the actual goal |
| **One pillar over 50% of posts** | A single-topic month, which caps reach at the people already interested in that topic | Flag and rebalance |
| **Same quadrant three posts running on one channel** | Reads as a campaign the audience did not opt into | Reorder rather than rewrite |

### Weekly coverage rule
Each week should cover at least 3 of the 4 quadrants. A week that is all EDUCATE or all CONVINCE is out of balance.

### Capacity check before cadence

The most common way a calendar fails is that it is never produced. Before accepting a cadence, cost it and compare against who is actually available:

| Format | Rough production load | Needs |
|---|---|---|
| Text post | Lowest | Writer only |
| Thread | Low | Writer only |
| Poll | Lowest | Writer only |
| Carousel or document | High | Writer plus designer, with review time between them |
| Newsletter issue | High | Writer plus edit pass |
| Video or audio | Highest | Script, record, edit, caption |
| Long-form blog | Highest, and the longest lead time | Draft, edit, SEO pass, publish |

**Rule:** if the requested month contains more high-load and highest-load assets than the team can name an owner for, say so before building the calendar, and propose the version that can actually ship. A calendar that is 60% produced is worse than a smaller one that is fully produced, because the gaps land unpredictably and break the weekly arc. Never present a cadence the user has not confirmed is achievable.

## When to use

- "Plan next month's content"
- "Build a content calendar for Q3"
- "What should we post this month?"
- "Give me a 4-week editorial calendar"
- "Schedule our LinkedIn and email content for June"

## Inputs needed

1. **Month and year**: which month to plan (default: next calendar month)
2. **Channels**: LinkedIn organic, Twitter/X, newsletter, blog, YouTube - pick which apply
3. **Primary goal this month**: awareness, demand gen, retention, or event-driven (launch, webinar, conference)
4. **Posting cadence per channel**: how many times per week per channel (ask if not provided)
5. **Themes or constraints**: product launches, campaigns, events, or topics to avoid

## Process

1. **Load context.** Read `knowledge/brand/voice.md`, `knowledge/icp/personas.md`, `knowledge/kpis.md`. If `knowledge/brand/voice.md` is missing, stop: "I need voice context. Run `/brand-context` first."

2. **Check `knowledge/learnings.md`** for past content performance data. Surface any patterns: what formats outperformed, what topics resonated, what cadence worked.

3. **Check `knowledge/content-library/`** for existing content that can be repurposed or sequenced into the month.

4. **Define the month's content pillars** (3-4 max):
   - Each pillar maps to one ICP pain or goal from `knowledge/icp/personas.md`
   - Each pillar maps to one business outcome from `knowledge/kpis.md`
   - Map each pillar to its dominant quadrant (a pillar can span quadrants, but it should have a primary one)
   - Never let one pillar dominate more than 50% of posts

5. **Pre-check the quadrant distribution** before building week-by-week:
   - Count total planned posts for the month
   - Calculate targets: 40% EDUCATE, 20% ENTERTAIN, 40% INSPIRE+CONVINCE
   - Flag any warning signs before writing the calendar

6. **Build the calendar** week by week:

   ```
   # Content calendar: [Month YYYY]

   **Goal**: [primary goal]
   **Channels**: [list]
   **Cadence**: [X posts/week per channel]
   **Pillars**:
   - Pillar 1: [topic] -> speaks to [ICP pain] -> drives [metric] -> primary quadrant: [E/I/Ed/C]
   - Pillar 2: [topic] -> speaks to [ICP pain] -> drives [metric] -> primary quadrant: [E/I/Ed/C]
   - Pillar 3: [topic] -> speaks to [ICP pain] -> drives [metric] -> primary quadrant: [E/I/Ed/C]

   **Quadrant distribution target**: [N] EDUCATE | [N] ENTERTAIN | [N] INSPIRE | [N] CONVINCE

   ---

   ## Week 1 (DD-MM to DD-MM) | Quadrants this week: Ed, I, C, En

   | Day | Channel | Format | Pillar | Quadrant | Topic/Angle | Asset needed |
   |---|---|---|---|---|---|---|
   | Mon | LinkedIn | Text post | P1 | EDUCATE | [specific angle] | None - write in chat |
   | Wed | LinkedIn | Carousel | P2 | INSPIRE | [specific angle] | 6-slide design |
   | Thu | Newsletter | Issue | P3 | EDUCATE | [specific angle] | Full draft |
   | Fri | Twitter/X | Thread | P1 | CONVINCE | [specific angle] | None - write in chat |

   **Week 1 theme**: [one sentence connecting the week's posts]
   **Leading into**: [what week 2 builds toward]
   **Quadrant coverage this week**: Ed (2), I (1), C (1), En (0) - [flag if <3 quadrants covered]

   ## Week 2 (DD-MM to DD-MM)
   [same format]

   ## Week 3 (DD-MM to DD-MM)
   [same format]

   ## Week 4 (DD-MM to DD-MM)
   [same format]

   ---

   ## Quadrant distribution summary
   | Quadrant | Count | % of total | Target | Status |
   |---|---|---|---|---|
   | EDUCATE | X | X% | 40% | [on track / over / under] |
   | ENTERTAIN | X | X% | 20% | [on track / over / under] |
   | INSPIRE | X | X% | 20% | [on track / over / under] |
   | CONVINCE | X | X% | 20% | [on track / over / under] |

   **Warning sign flags**: [list any quadrant >60% or missing entirely, or clear the flags]

   ---

   ## Asset production queue
   List every asset that needs to be created, by type:
   - **Write in chat** (no design needed): [list of posts]
   - **Needs design**: [list with specs]
   - **Needs long-form draft**: [list]
   - **Needs video/audio**: [list]

   ## Skills to run for production
   - `/linkedin-post` for: [list specific posts by week/day]
   - `/newsletter-writer` for: [list issues]
   - `/content-repurposer` if: [list any anchor pieces to atomize]
   - `/thought-leadership-writer` for: [list long-form pieces]
   ```

7. **Self-check.** Every item is checkable against the saved calendar file. Count the rows rather than asserting the property.

   - Every row in every week table has a non-empty Quadrant cell. Count rows, count filled cells, and confirm the two numbers match
   - The distribution summary percentages were computed from the week tables, not written by hand. Re-derive them and confirm they agree
   - The distribution matches the target row for this month's goal from the goal table, within 5 percentage points. If it does not, the deviation is stated and justified in the summary
   - No quadrant exceeds 60% of total posts
   - No quadrant is 0%. Check INSPIRE specifically
   - Every week's coverage line names at least 3 distinct quadrants
   - Every row has a Pillar cell, and every pillar in the header maps to a named metric from `knowledge/kpis.md`
   - No pillar exceeds 50% of total rows
   - No channel has the same topic on two consecutive posting days
   - Every proof point named in the calendar traces to a specific file in `knowledge/content-library/` or `knowledge/services/`, cited by path. Weeks with no sourceable proof read `[NEEDS PROOF]`, never an invented stat or customer name
   - Every asset in the production queue has a format, and every high-load asset has a named owner or is flagged as unowned
   - The newsletter row falls in the same week as the social posts that reference it
   - Total posts per channel per week equals the cadence the user confirmed. State both numbers
   - Every cadence or best-day claim in the output is either sourced to `knowledge/learnings.md` or labelled `[UNVERIFIED default]`

8. **Save** to `output/social-calendar/<DD-MM-YYYY>-<month-slug>.md` with frontmatter:
   ```yaml
   ---
   format: social-calendar
   month: [Month YYYY]
   goal: [awareness|demand|retention|launch]
   channels: [list]
   pillars: [list]
   quadrant-distribution: {educate: X%, entertain: X%, inspire: X%, convince: X%}
   created: DD-MM-YYYY
   ---
   ```

9. **Offer next actions**:
   - "Run `/linkedin-post` for any post on the calendar and I'll write it now."
   - "Run `/newsletter-writer` for [month] issue [N] to draft it."
   - "Run `/content-repurposer` on [anchor piece] to generate derivative posts."
   - "Set a reminder to run `/retro` at the end of the month to capture what worked."

## Channel-specific rules

**These are starting defaults, not measured facts.** Where `knowledge/learnings.md` holds this
account's own performance data, that data overrides every rule in this section, and the calendar
must say so. Never present a cadence or a best-day claim to a client as though a platform
published it.

**LinkedIn organic:**
- Max 5 posts/week or engagement drops
- Vary formats: text, carousel, poll, document
- Best days: Tuesday-Thursday
- Never post twice in one day

**Twitter/X:**
- Threads outperform single tweets for B2B
- 3-5 tweets per thread is the sweet spot
- Quote-tweet your own LinkedIn posts for cross-channel reach

**Newsletter:**
- One issue per week maximum for B2B audiences
- Tuesday or Wednesday sends outperform Monday and Friday
- Issue topic should anchor the week's social content

**Blog/SEO:**
- One pillar article per month minimum
- Long-form takes 2 weeks to write, edit, publish - account for lead time
- Every blog post generates 3-5 social posts via `/content-repurposer`

## Rules

- Never plan more posts than the team can realistically produce. If cadence seems high, flag it: "This is [N] posts/week. Confirm this is achievable before I finalize."
- Never schedule a product post without a paired proof point (stat, customer quote, or case study reference). Product posts without proof are CONVINCE posts that cannot convince.
- If `knowledge/learnings.md` has data showing a format underperforms, do not include it in the plan without flagging.
- No filler content. Every post earns its slot with a specific business reason and a quadrant assignment.
- If the user's goal is pure awareness, shift the mix using the goal table above. Adjust and note the shift explicitly in the calendar summary.

## Never invent

- **Never invent a stat, customer name, result, quote or proof point to fill a calendar slot.** A calendar looks harmless because it is only topics, but every `[NEEDS PROOF]` that gets quietly filled in becomes a published claim three weeks later, written by someone who assumed the calendar had been checked. Leave the marker.
- **Do not invent this account's past performance.** If `knowledge/learnings.md` is empty, say it is empty. "Carousels performed well last quarter" written from nothing becomes the reason the whole month is carousels.
- Every cadence, best-day and format claim in this file is a starting default recorded at authoring time, not something a platform published. Mark them `[UNVERIFIED default]` in the output wherever they influenced the plan.
- If a topic needs a fact nobody has, the topic changes. The fact does not get written.

## What this skill cannot know

These are limitations of the skill, not of the plan. Anything below that reaches the output must carry `[UNVERIFIED]` there.

- **Current platform algorithms, format support, posting limits and reach behaviour.** Every channel rule in this file is a default from authoring time. Platforms change ranking and format support without notice, and reach patterns differ by account size and audience.
- **What this specific audience actually responds to.** Only `knowledge/learnings.md` and the account's own analytics answer that, and where they contradict this file, they win.
- **Whether the team can produce this volume.** The capacity table is a shape, not this team's throughput. Ask.
- **Whether a planned proof point is still approved for public use.** Customer permissions expire, and a case study cleared last year may not be cleared now. Check with whoever owns the relationship before a proof slot is filled.
- **Whether anything on the calendar collides with an embargo, a launch date, or a legal or PR constraint** that lives outside `knowledge/`.

## Related skills

- `/campaign-brief` when the month sits inside a larger campaign, so the calendar inherits its objective rather than inventing one
- `/linkedin-post` for writing any individual post the calendar schedules
- `/newsletter-writer` for the issue that anchors each week
- `/content-repurposer` when one anchor piece should generate several calendar slots instead of each being written from scratch
- `/thought-leadership-writer` for the long-form pieces, which need lead time booked into the calendar rather than added late
- `/case-study-writer` when the INSPIRE quadrant is empty because no proof asset exists yet
- `/seo-article-writer` for the blog pillar piece and the keyword decisions behind it
- `/social-calendar` is not the place to decide the message. Run `/messaging-framework` first if the pillars keep drifting month to month
- `/kpi-review` for the account's own performance data, which overrides every default cadence here
- `/retro` at the end of the month, to write what happened back into `knowledge/learnings.md` so the next calendar is built on data

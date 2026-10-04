---
name: gtm-launch
version: 1.4.4
description: Launch playbook for /gtm launch <target>. Use when the user wants a week-by-week launch plan for Product Hunt, Hacker News, or X, with templates, checklists, and metrics. Also trigger for "plan my launch", "Product Hunt launch", "launch playbook", "how do I launch", or "launch checklist".
---

# Product/Service Launch Playbook Generator

> **Default lens: a SaaS / AI software startup.** Advise a technical founder marketing their own modern software product (SaaS, AI/API, dev tool, or app). Tailor every recommendation to that reader.
>
> Stage-fit (`launch`): Tier 1 Core · Tier 2 Useful · Tier 3 Useful. Appropriate at every served tier - generate with no stage note.

> Full persona and general guidance: read `../gtm/templates/advisor-prompt.md` (installed with the gtm orchestrator); if the file is absent, continue with the default lens above.

## Skill Purpose
Generate a complete, week-by-week launch playbook for any product, service, or feature launch. This skill produces a tactical plan with templates, checklists, email sequences, social posts, and metrics tracking -- everything needed to execute a successful launch.

## When to Use
- User is planning to launch a new product, service, feature, or offering
- User asks for a launch plan, go-to-market strategy, or launch checklist
- User wants to coordinate a multi-channel launch campaign
- Triggered by `/gtm launch` or `/gtm launch <product description>`

## How to Execute

### Step 1: Gather Launch Context
**First, choose how this run works** - the launch skill runs two ways:

1. **Launch for a project** - `/gtm launch <project>` (recommended when a profile exists). Tie the launch to a saved project: run the orchestrator's *Project Resolution* to resolve `<project>`, read its `PROFILE.md`, inherit everything `/gtm init` already captured, tailor the whole playbook to it, save the report into the project folder, and offer to record the launch back to the profile at the end.
2. **Brainstorm a launch** - `/gtm launch <project description>`. A standalone plan with nothing read from or written to a profile, worked up from the description the founder gives. Use it for a fresh idea, a side project, or before a profile exists.

If a profile exists but the founder hasn't said which they want, ask once; if none exists, default to brainstorm and mention `/gtm init` for next time.

**With a profile loaded, load context from `PROFILE.md` before asking anything - never re-ask what `/gtm init` already captured.** Map its fields to the inputs below and ask only for the gaps:
- **Target audience** ← `ICP`, `Secondary audience`, `Key pain points`
- **Launch goal** ← `Main goal (next 30 days)` and `90-day direction` if set (sharpen to this launch if needed)
- **Channels & assets** ← `Primary channel today`, `Existing assets` (list size, following), `Links & Channels` social profiles
- **Existing customers/users** ← `Current traction`, `Existing assets`
- **Project type** ← `Project type` (drives the launch-type choice in Step 2)
- **Positioning** ← `Differentiator` and `Key messages` (set by `/gtm position` or `/gtm competitors`) - reuse these for the Week 1-2 positioning statement instead of writing one from scratch
- **Competitors** ← run the orchestrator's *Competitor Resolution Protocol*; use them for the "why us vs alternatives" content in launch week
- Also read any `Reference Documents` (strategy, brand manifesto) and honor them as source of truth.
- Read `LOG.md` (beside the profile), especially its `## Launches` section - what's already been launched and how it did (upvotes, signups, paying). Don't re-pitch a channel the log shows already flopped without naming what's different this time; build on what worked, and surface any past launch whose `pending` result is now due.

Then collect the inputs below - with a profile loaded, only the launch-specific gaps (what's launching, launch date, price, budget); in brainstorm mode, all of them:

1. **What are you launching?** (product, service, feature, course, event)
2. **Who is the target audience?** (demographics, pain points, existing list size)
3. **What is the primary launch goal?** (signups, email captures, feedback, revenue target, awareness) - pre-PMF, steer the goal toward email captures and feedback conversations rather than revenue (see the early-stage default in Step 2)
4. **What is the launch date?** (or desired timeline)
5. **What channels do you have access to?** (email list size, social following, ad budget, partnerships)
6. **What is the price point?** (if applicable)
7. **Do you have existing customers/users?** (for beta, testimonials, case studies)
8. **What is the budget?** (bootstrapped, moderate, well-funded) - when you present these as options, lead each with its top spend from the Step 10 allocation guide; never lead a tier with paid ads (at these stages "paid" means retargeting warm launch traffic, not cold acquisition).

### Step 2: Determine Launch Type
Select the primary launch strategy based on the user's context:

| Launch Type | Best For | Key Channel | Timeline |
|---|---|---|---|
| Product Hunt | SaaS, dev tools, consumer apps | Product Hunt + Twitter/X | 4-6 weeks prep |
| Email List Launch | Course, info product, SaaS with existing list | Email | 6-8 weeks |
| Social Media Launch | Consumer product, personal brand | Twitter/X, LinkedIn, Instagram | 4-6 weeks |
| Paid Ads Launch | E-commerce, established product | Facebook/Google Ads | 2-4 weeks prep |
| Community Launch | Niche product, developer tools | Reddit, Discord, Slack communities | 6-8 weeks |
| Partner Launch | B2B, enterprise, marketplace | Partner channels | 8-12 weeks |
| Hybrid Launch | Any high-stakes launch | Multi-channel coordinated | 8-12 weeks |

**Early-stage default (Tiers 1-2, no audience yet):** treat the launch as one event, not a strategy - a Product Hunt + directories moment whose real yields are email captures, feedback conversations, a handful of early adopters, and durable backlinks. Set the goal in those units, not revenue. Expect the traffic spike to decay within days; the plan's job is to convert the spike into a list and learnings before it fades.

### Step 3: Generate the 8-Week Launch Timeline

#### Weeks 1-2: Foundation
**Objective:** Lock in positioning, build assets, set up infrastructure.

**Tasks:**
- [ ] Define launch positioning statement: "For [TARGET] who [PROBLEM], [PRODUCT] is a [CATEGORY] that [KEY BENEFIT]. Unlike [ALTERNATIVE], we [DIFFERENTIATOR]." With a profile loaded, build this from the profile's `Differentiator` and `Key messages` (set by `/gtm position` / `/gtm competitors`) - refine the established position, don't reinvent it.
- [ ] Create launch one-pager (internal alignment doc)
- [ ] Set up landing page / waitlist page
- [ ] Set up analytics and tracking (UTM parameters, conversion goals, event tracking) - `/gtm analytics` defines the activation metric and event spec to build from
- [ ] Create launch-specific email list/segment
- [ ] Draft all email sequences (see Email Templates below)
- [ ] Brief design team on visual assets needed
- [ ] Identify 10-20 potential beta testers or early access users
- [ ] Research and list 20+ communities, forums, and groups where target audience gathers
- [ ] Set up social media content calendar tool

**Deliverables:**
- Positioning statement
- Landing page live
- Email sequences drafted
- Beta tester list

#### Weeks 3-4: Audience Building
**Objective:** Build anticipation, grow waitlist, recruit beta testers.

**Tasks:**
- [ ] Begin content seeding: publish 2-3 blog posts / threads related to the problem you solve
- [ ] Share behind-the-scenes content on social media (building in public)
- [ ] Start engaging in target communities (provide value, don't pitch yet)
- [ ] Reach out to beta testers with personal invitations
- [ ] Collect early feedback and testimonials from beta users
- [ ] Begin influencer/partner outreach (see Partner Coordination below)
- [ ] Set up referral mechanism for waitlist (e.g., viral waitlist with rewards)
- [ ] Create teaser content (sneak peeks, countdowns, problem-awareness posts)
- [ ] Record demo video or product walkthrough
- [ ] Write press release or media pitch (if relevant)

**Content Calendar (Weeks 3-4):**
| Day | Content Type | Channel | Theme |
|---|---|---|---|
| Mon | Problem-awareness post | LinkedIn/Twitter | Why this problem matters |
| Tue | Behind-the-scenes | Instagram/Twitter | Show what you're building |
| Wed | Educational content | Blog/LinkedIn | Teach something related to your space |
| Thu | Social proof | Twitter/LinkedIn | Beta tester quote or result |
| Fri | Teaser/countdown | All channels | Build anticipation for launch |

**Deliverables:**
- 4-6 content pieces published
- Beta testers onboarded and providing feedback
- Waitlist growing
- Partner/influencer commitments secured

#### Weeks 5-6: Pre-Launch Intensification
**Objective:** Maximize anticipation, finalize assets, prep launch infrastructure.

**Tasks:**
- [ ] Send pre-launch email sequence to waitlist (see Email Templates)
- [ ] Increase social media posting frequency to daily
- [ ] Publish case study or results from beta testers
- [ ] Finalize pricing and offer structure
- [ ] Create launch-day content package (all posts, emails, and graphics ready)
- [ ] Brief partners/affiliates on launch plan and provide swipe copy
- [ ] Set up live chat or support for launch day
- [ ] Test all purchase/signup flows end-to-end
- [ ] Prepare FAQ document for support team
- [ ] Create urgency mechanism (early bird pricing, limited spots, bonus expiration)
- [ ] Rehearse launch day by walking through every step
- [ ] Set up real-time dashboard for launch metrics

**Deliverables:**
- All launch assets finalized and scheduled
- Partners briefed and ready
- Checkout/signup flow tested
- Support team prepared

#### Week 7: LAUNCH WEEK
**Objective:** Execute the launch with maximum impact and coordinated effort.

**Day-by-Day Breakdown:**

**Monday - Soft Launch / VIP Access:**
- Send early access email to VIPs, beta testers, and top waitlist members
- Post on social: "We're live for our early supporters"
- Collect first-day feedback and testimonials
- Monitor for bugs and issues
- Goal: First 50-100 users/customers

**Tuesday - Public Announcement:**
- Send main launch email to full list
- Publish launch blog post
- Post launch announcement on all social channels
- Submit to Product Hunt (if applicable -- schedule for 12:01 AM PT)
- Activate partner/affiliate promotions
- Begin paid ad campaigns (if applicable)
- Goal: Maximum visibility and traffic

**Wednesday - Social Proof Push:**
- Share first customer testimonials and results
- Repost/retweet customer reactions
- Send "look what people are saying" email
- Post in communities (with genuine value, not spam)
- Respond to every comment, mention, and question
- Goal: Build momentum through social proof

**Thursday - Objection Handling:**
- Publish FAQ or "everything you need to know" post
- Send email addressing top 3 objections
- Host live Q&A or AMA (Twitter Space, LinkedIn Live, webinar)
- Share comparison content (why this vs alternatives)
- Goal: Convert fence-sitters

**Friday - Urgency and Scarcity:**
- Send "early bird pricing ends soon" email
- Post countdown content on social
- Share final testimonials and case studies
- Activate scarcity mechanisms (limited spots, bonus expires)
- Goal: Drive final wave of conversions

**Saturday/Sunday - Wrap Up:**
- Send "last chance" email for any time-limited offers
- Compile launch week results
- Thank early customers publicly
- Begin post-launch content planning

#### Week 8: Post-Launch
**Objective:** Maintain momentum, collect feedback, plan next iteration.

**Tasks:**
- [ ] Send post-launch survey to new customers
- [ ] Compile and analyze launch metrics (see Metrics section)
- [ ] Write launch retrospective (what worked, what didn't, what to change)
- [ ] Transition from launch pricing to regular pricing
- [ ] Set up onboarding email sequence for new customers
- [ ] Plan next content calendar based on launch learnings
- [ ] Follow up with media contacts and partners with results
- [ ] Identify top customers for case studies
- [ ] Begin planning v2 features based on feedback
- [ ] Set up ongoing marketing engine (content, ads, email nurture)

### Step 3b: Directory Submission Pack (Product Hunt + directories launches)

Directories all ask for the same assets in different lengths. Generate the pack once from the profile's positioning (`Differentiator`, `Key messages`, the one-liner), ready to paste into any submission form:

- **Tagline** (60 characters or less)
- **Short description** (140 characters or less)
- **Long description** (~500 words)
- **Keyword list** (comma-separated)
- **Maker's comment** (first person - the story of why you built it, ending with an honest ask for feedback)

Submission order: directories first (they build the backlink base quietly), Product Hunt as the peak event.

| Tier | Targets | Why |
|---|---|---|
| 1 - Launch platforms | Product Hunt, BetaList, Peerlist Launchpad | Launch-day visibility and early adopters |
| 2 - Software directories | SaaSHub, AlternativeTo, Capterra | Steady referral trickle + domain-authority backlinks |
| 3 - AI-specific (for AI products) | Toolify.ai, There's An AI For That, Future Tools | Category browsers actively hunting new AI tools |

The table is the stable core, not a ceiling - platforms appear and fade, so run one quick web search per launch (`"[category] launch platforms"`, `"Product Hunt alternatives"`) and slot anything current and relevant into the right tier. Every listing should point at a page with an email capture, so directory traffic that doesn't convert today still lands on the list.

### Step 4: Email Sequence Templates

#### Pre-Launch Sequence (Weeks 5-6)

**Email 1: The Teaser (2 weeks before)**
Subject: Something big is coming...
Purpose: Build anticipation
Content: Hint at the product, share the problem it solves, tease the launch date. Don't reveal everything.
CTA: "Stay tuned" or "Make sure you're on the list"

**Email 2: The Reveal (1 week before)**
Subject: Here's what we've been building
Purpose: Show the product, build desire
Content: Reveal the product with screenshots/video. Share beta tester results. Announce launch date and any early bird offer.
CTA: "Mark your calendar" or "Get notified on launch day"

**Email 3: The Social Proof (3 days before)**
Subject: "[Beta Tester Name] got [Result] in [Timeframe]"
Purpose: Prove it works
Content: Feature 2-3 beta tester testimonials with specific results. Address the "does this actually work?" objection.
CTA: "Be ready for [launch day]"

#### Launch Sequence (Week 7)

**Email 4: The Launch (Day 1)**
Subject: It's live -- [Product Name] is here
Purpose: Drive immediate action
Content: Announce the launch. State the offer clearly. Include early bird pricing or bonus. Link directly to purchase/signup.
CTA: "Get [Product] now" with primary button

**Email 5: The Social Proof Follow-Up (Day 3)**
Subject: People are already seeing results
Purpose: Convert through social proof
Content: Share first-customer testimonials, screenshots of reactions, usage stats. Create FOMO.
CTA: "Join [X] others who already [outcome]"

**Email 6: The Objection Handler (Day 4)**
Subject: "But what if [common objection]?"
Purpose: Address hesitations
Content: List and answer top 3-5 objections. Include guarantee/risk reversal. Share FAQ.
CTA: "Try it risk-free"

**Email 7: The Urgency Close (Day 5-7)**
Subject: [X hours] left for [early bird / bonus / discount]
Purpose: Drive final conversions with urgency
Content: Remind of the deadline. Recap the value. Final testimonial. Clear, single CTA.
CTA: "Last chance to get [offer]"

### Step 5: Social Media Launch Posts

#### Twitter/X Thread Template:
```
Post 1: After [X months/weeks] of building, I'm thrilled to announce [Product Name] is live.

[Product] helps [target audience] [achieve outcome] without [pain point].

Here's the story of why I built it (and what it can do for you):

[Thread emoji] 1/

Post 2: The problem: [Describe the problem in detail. Make it relatable.]

Post 3: The solution: [What your product does, in simple terms. Include screenshot or demo GIF.]

Post 4: Early results: [Beta tester results, specific numbers]

Post 5: What's included: [Key features as bullet points]

Post 6: Special launch offer: [Pricing, early bird deal, bonus]

Post 7: Try it now: [Link] [CTA]
```

#### LinkedIn Post Template:
```
I just launched [Product Name], and here's why it matters:

[1-2 sentences about the problem]

After [talking to X customers / spending Y months building / experiencing this problem myself], I realized [insight].

So I built [Product Name] to [specific outcome].

Early users are already seeing:
- [Result 1]
- [Result 2]
- [Result 3]

If you [target audience descriptor], I'd love for you to check it out:
[Link]

Special launch pricing available for the next [timeframe].

#relevant #hashtags
```

#### Instagram / Visual Platform Template:
```
Image/Carousel: Product screenshots, before/after, or results graphic

Caption:
[Hook - first line that stops the scroll]

The problem: [1-2 sentences]
The solution: [1-2 sentences about your product]
The results: [specific outcomes from beta users]

Launch special: [offer details]

Link in bio to get started.

[Relevant hashtags - 15-20 for Instagram]
```

### Step 6: Press and Media Outreach

**Press Release Structure:**
1. Headline: [Company] Launches [Product] to Help [Audience] [Outcome]
2. Subheadline: [Supporting detail with a key stat or differentiator]
3. First paragraph: Who, what, when, where, why (the news)
4. Quote from founder/CEO
5. Product details and key features
6. Market context (why now, market size, trend)
7. Customer quote or early results
8. Availability and pricing
9. About the company (boilerplate)
10. Contact information

**Media Pitch Email Template:**
```
Subject: [Angle] -- [Product Name] launches to [outcome]

Hi [Name],

I'm reaching out because you've covered [related topic] and I thought [Product Name] might be interesting for your readers.

[One sentence about what it does and why it's newsworthy]

[One sentence about early traction or results]

[One sentence about what makes it different]

I'd love to offer you [exclusive story / early access / founder interview / demo].

Happy to share more details if you're interested.

Best,
[Name]
```

### Step 7: Influencer and Partner Coordination

**Partner Outreach Timeline:**
- Week 3: Initial outreach with personal message
- Week 4: Follow up, share product details and demo
- Week 5: Confirm participation, send swipe copy and affiliate links
- Week 6: Reminder with launch day schedule
- Week 7: Day-of coordination, thank you notes
- Week 8: Share results, pay commissions, plan ongoing partnership

**What to Provide Partners:**
- Product access (free account or sample)
- Swipe copy for email, social, and blog
- Branded graphics and assets
- Unique affiliate/referral link with tracking
- Commission structure or reciprocal promotion plan
- Launch day schedule with specific asks

### Step 8: Launch Metrics Dashboard

Track these metrics in real-time during launch week:

**Awareness Metrics:**
- Website traffic (total and by source)
- Social media impressions and reach
- Press mentions and backlinks
- Email open rates

**Engagement Metrics:**
- Time on site
- Pages per session
- Social media engagement rate
- Email click-through rates
- Demo video completion rate

**Conversion Metrics:**
- Signup/purchase conversion rate
- Revenue generated
- Average order value
- Cost per acquisition
- Email-to-conversion rate

**Retention Metrics (Post-Launch):**
- Day 1 / Day 7 retention
- Feature adoption rate
- Support ticket volume
- NPS score

**Pre-PMF scoreboard (Tiers 1-2):** email captures, feedback conversations started, and activated early adopters - in that order. Upvotes and traffic are inputs, not outcomes; revenue targets belong to launches that already have an audience to sell to.

### Step 9: Common Launch Mistakes to Avoid

1. **Launching to nobody** -- Build the audience BEFORE the product is ready
2. **No urgency mechanism** -- Without a deadline, people bookmark and forget
3. **Perfectionism** -- Ship at 80% quality; iterate based on real feedback
4. **Single-channel launch** -- Coordinate across email, social, communities, and partners
5. **No follow-up sequence** -- Most conversions happen on days 3-7, not day 1
6. **Ignoring time zones** -- Schedule launches and emails for your audience's active hours
7. **No support plan** -- Launch day will generate support requests; be ready
8. **Pricing confusion** -- Make the offer crystal clear; don't make people calculate
9. **Forgetting mobile** -- Test every email, page, and checkout on mobile
10. **No post-launch plan** -- The launch is the beginning, not the end

### Step 10: Budget Allocation Guide

| Budget Level | Allocation |
|---|---|
| **Bootstrapped ($0-500)** | 100% organic: content, communities, founder-led social, manual outreach |
| **Moderate ($500-5,000)** | 35% design/assets (demo video, landing page, launch graphics), 30% tools/software (email, analytics, scheduling), 25% influencer/partner/community seeding, 10% retargeting ads (warm launch visitors only, not cold acquisition) |
| **Well-Funded ($5,000-25,000)** | 25% influencer/partner, 25% PR/media, 20% content/assets, 15% events, 15% paid ads (retargeting first; cold acquisition only once PMF is validated) |
| **Enterprise ($25,000+)** | 30% paid ads, 20% events/webinars, 20% PR, 15% influencer, 10% content, 5% tools |

At the served tiers the founder is usually pre- or early-PMF, so fundamentals lead and "paid" means retargeting warm launch visitors, not cold acquisition - cold paid pre-PMF burns scarce cash (B2B SaaS CAC $150-$500) and corrupts the read on real demand. Scale cold acquisition only once the funnel converts the traffic it already gets. (Enterprise sits at Tier 4-5, where paid acquisition is a legitimate core channel, so it leads there.)

### Step 11: Post-Launch Analysis Framework

After the launch, generate a retrospective covering:

1. **Goal vs Actual**: Did you hit your targets?
2. **Channel Performance**: Which channels drove the most conversions?
3. **Email Performance**: Open rates, click rates, conversion rates by email
4. **Top Converting Content**: Which posts, pages, or ads drove the most action?
5. **Customer Feedback Themes**: What are people saying?
6. **What Worked**: Top 3 things that drove results
7. **What Didn't Work**: Top 3 things to change next time
8. **Unexpected Insights**: Surprises from the data
9. **Next Steps**: Immediate actions based on learnings

## Output Format

Write the report to the resolved output path as `YYYY-MM-DD-launch-playbook.md` (see the orchestrator's *Project Resolution*) with:

```markdown
# Launch Playbook: [Product Name]
## Launch Date: [Date]
## Launch Type: [Type]
## Primary Goal: [Goal with specific target]

---

## What to Expect
[Include this section in every early-stage playbook - an honest, founder-facing paragraph: this launch is one event, not a growth strategy. For a product nobody knows yet, a good launch day is hundreds of visitors, a few dozen list signups, and a handful of real conversations - the durable yield is the email list, the feedback, and the backlinks. This playbook is the map; the results come from you doing the manual work - replying to every comment, following up with every signup, showing up all day.]

## Week-by-Week Plan
[Detailed week-by-week tasks with checkboxes]

## Email Sequences
[Complete email templates customized for the product]

## Social Media Content
[Platform-specific posts ready to customize and schedule]

## Directory Pack
[Tagline, short and long descriptions, keyword list, maker's comment, and the tiered submission table with order]

## Partner/Influencer Plan
[Outreach templates and coordination timeline]

## Launch Day Checklist
[Hour-by-hour launch day plan]

## Metrics Dashboard
[Metrics to track with target benchmarks]

## Budget Allocation
[Specific dollar amounts based on stated budget]

## Post-Launch Plan
[Week 8+ activities and analysis framework]
```

## Update the Profile (with a profile loaded)

A launch playbook is mostly episodic, but a couple of facts are worth keeping so the next command and the next run know a launch is in flight. Once the playbook is written, offer to record them - never auto-write:

> "Want me to note this launch in your profile? I'd set:
> - **Main goal (next 30 days)** -> [the launch and its target] (only if this launch is your main near-term goal)
> - **Context & notes -> Notes** -> "Launch playbook generated [today]: [type] launch targeting [date], goal [goal]."
> (y/n)"

On yes, edit `projects/<name>/PROFILE.md` surgically:
- **Blank or still template text** - write it in full and tag it `(set by /gtm launch, YYYY-MM-DD)`.
- **Already holds the founder's wording** - don't overwrite; show the current value beside your proposed change and take the lightest action that fits: leave it if it still holds, the smallest sharpening edit if improvable, a full replacement only if the launch genuinely changed the goal.

Touch only the two fields above; leave competitors, differentiator, links, and everything else exactly as they are.

## Log the Run

After the playbook is saved (and the profile offer answered), append one line for this run to the project's `LOG.md`, in the log's fixed format, under its `## Launches` section - what this run produced or decided (naming the report file) and the outcome: a concrete result the run itself produced, or `pending` with the launch date when the result lands later. Example: `- 2026-07-07 · /gtm launch · launch playbook for <channel> (see 2026-07-07-launch-playbook.md) -> pending - launch day 2026-07-21`. The launch-day numbers land later as the founder's own line under `## Launches`. Skip this in brainstorm mode or when no project is loaded (a one-off has no log); if the project has no `LOG.md` yet, create it from `../gtm/templates/log-template.md` (installed with the gtm orchestrator) first. Then echo that exact line to the terminal as the run's closing `Logged:` line, so a run that skipped the write-back is visible at a glance.

## Key Principles
- Every recommendation should be tied to the user's specific product, audience, and resources. Generic advice is useless.
- Include specific templates they can copy-paste and customize, not just frameworks.
- If the user has run previous skills (market audit, market landing, market brand), incorporate those findings into the launch plan.
- Time the playbook to their stated launch date and work backwards.
- Always include a "minimum viable launch" option for users with limited resources.
- Emphasize that launching is an event, not a moment -- the buildup and follow-through matter more than day one.

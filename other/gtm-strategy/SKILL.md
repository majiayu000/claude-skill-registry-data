---
name: gtm-strategy
description: >
  Go-to-Market strategy guidance — GTM motions, content strategy, channel selection, brand building.
  Triggers on "GTM", "market entry", "customer acquisition", "channel strategy", "content marketing",
  "GTM 전략", "시장 진입", "고객 확보", "채널 전략", "콘텐츠 마케팅".
---

# GTM Strategy

> For unfamiliar placeholders or connected tools, see [CONNECTORS.md](../../CONNECTORS.md).

Go-to-Market (GTM) strategy framework. Combines 5 GTM motions, content pyramid, PESO channel distribution, and platform-specific tactics to reach ICP efficiently and drive growth through execution plans.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      GTM STRATEGY FRAMEWORK                      │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (Standalone)                                      │
│  ✓ Select optimal GTM motion based on product/ICP (5 types)     │
│  ✓ Content pyramid strategy (Pillar → Derivative → Atomic)      │
│  ✓ PESO channel distribution (Paid/Earned/Shared/Owned)        │
│  ✓ 90-day execution plan & KPI setting                          │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (with tool connections)                           │
│  + ~~analytics: Collect per-channel conversion data              │
│  + ~~knowledge base: Reference existing content archive          │
│  + ~~CRM: Analyze ICP win rates and channel attribution          │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

1. **GTM Motion**: "What GTM strategy fits our product?"
2. **Content Strategy**: "Build our content marketing plan"
3. **Channel Priority**: "Which channels should we focus on?"
4. **90-Day Plan**: "Create a first-quarter GTM roadmap"

## 5 GTM Motions

### Motion Selection Framework

```
          Product Complexity
               ↑
    Complex    │   Sales-Led    │  Community-Led
               │                │
    ────────────────────────────────────→ ACV
               │                │
    Simple     │   PLG          │  Content-Led
               │                │
          Self-serve ← ─ ─ ─ ─ → High-touch
```

### 1. Product-Led Growth (PLG)

**Definition**: Product is the primary growth engine. Free use → value experience → paid conversion

**Best For**:
- Self-serve possible (onboarding <30 mins)
- ACV <$10K (credit card payment)
- Network effects or viral element
- Users = buyers (end-user decision authority)

**Core Metrics**:
| Metric | Target | Cadence |
|--------|--------|---------|
| **Activation Rate** | >40% | Weekly |
| **PQL (Product Qualified Lead)** | 100+ monthly | Monthly |
| **Free → Paid Conversion** | 3-10% | Monthly |
| **Time to Value** | <5 mins | Cohort |
| **Viral Coefficient (K)** | >0.5 | Quarterly |

**Strategy**:
1. **Freemium/Free Trial**: Unrestricted free or 14-30 day trial
2. **Aha Moment Optimization**: Shorten time to first value
3. **In-product Guidance**: Usage-based upgrade prompts
4. **Self-serve Checkout**: Credit card payment, minimal sales

**Examples**: Slack, Notion, Figma, Calendly

### 2. Sales-Led

**Definition**: Sales team drives. Complex solution, high ACV, multiple decision-makers

**Best For**:
- ACV >$10K (Enterprise)
- Complex buying process (Buying Committee)
- Custom implementation required
- Compliance/Security demands

**Core Metrics**:
| Metric | Target | Cadence |
|--------|--------|---------|
| **Pipeline Coverage** | 3-5x Quota | Monthly |
| **Win Rate** | 20-40% | Quarterly |
| **Sales Cycle** | <90 days (SMB), <180 days (Ent) | Quarterly |
| **ACV** | $50K+ | Quarterly |
| **Sales Productivity** | >$500K ARR/Rep | Annually |

**Strategy**:
1. **Inbound Lead Generation**: Content, SEO, webinars
2. **SDR/BDR Team**: Lead qualification specialist
3. **AE (Account Executive)**: Deal closing
4. **Solution Engineering**: Technical demos, POC support

**Examples**: Salesforce, Workday, ServiceNow

### 3. Community-Led

**Definition**: Community is the growth engine. Users become advocates (evangelists)

**Best For**:
- Developer/Creator audience
- Open-source or platform
- Strong Use Case diversity
- Bottom-up adoption (individual → team → org)

**Core Metrics**:
| Metric | Target | Cadence |
|--------|--------|---------|
| **Active Community Members** | 1,000+ monthly | Monthly |
| **Contribution Rate** | >5% | Monthly |
| **Community → Customer** | 10-20% | Quarterly |
| **NPS** | >50 | Quarterly |
| **Forum DAU/MAU** | >30% | Weekly |

**Strategy**:
1. **Forum/Slack/Discord**: Active discussion space
2. **Contributor Program**: Reward top users
3. **Events**: Meetups, conferences, hackathons
4. **User-Generated Content**: Community tutorials

**Examples**: GitHub, Hashicorp, Stripe (developer community)

### 4. Content-Led

**Definition**: Content is primary acquisition channel. Thought Leadership → Inbound

**Best For**:
- Complex problem (education needed)
- Long buying cycle (6-12 months)
- High LTV (long-term customer)
- Rich SEO opportunity

**Core Metrics**:
| Metric | Target | Cadence |
|--------|--------|---------|
| **Organic Traffic** | 10K+ monthly | Monthly |
| **Content → MQL** | 20-30% | Monthly |
| **Domain Authority** | 50+ (Moz) | Quarterly |
| **Backlinks** | 50+ monthly | Monthly |
| **Newsletter Subscribers** | 20% quarterly growth | Quarterly |

**Strategy**:
1. **Pillar Content**: Long-form guides (5,000+ words)
2. **SEO Optimization**: Keyword research, backlinks
3. **Multi-channel Distribution**: Blog → LinkedIn → newsletter
4. **Lead Magnet**: eBooks, templates, checklists

**Examples**: HubSpot, Intercom, Drift

### 5. Founder-Led

**Definition**: Founder personal brand is the growth engine. Personal Brand → Company

**Best For**:
- Early stage (Pre-seed, Seed)
- Budget constraints (CAC <$100)
- Founder is Thought Leader
- Niche market

**Core Metrics**:
| Metric | Target | Cadence |
|--------|--------|---------|
| **Founder Followers** | 20% quarterly growth | Quarterly |
| **Post Engagement** | >5% | Weekly |
| **Inbound DM/Email** | 10+ weekly | Weekly |
| **Speaking/Podcast** | 2+ monthly | Monthly |
| **Newsletter → Customer** | 5-10% | Quarterly |

**Strategy**:
1. **Daily LinkedIn/X Posts**: Share insights, experiences
2. **Founder Newsletter**: Weekly/bi-weekly
3. **Podcast Appearances**: Target audiences
4. **Speaking**: Conferences, webinars

**Examples**: Sahil Lavingia (Gumroad), Pieter Levels (Nomad List)

### Motion Combination (Hybrid)

Most startups use **2-3 combined motions**:

**Example Combinations**:
- **PLG + Community**: Notion (free usage + template community)
- **Content + Sales**: HubSpot (blog leads → sales conversion)
- **Founder + PLG**: Linear (CEO Twitter + viral product)
- **Community + Sales**: Slack (team adoption + Enterprise sales)

**Resource Allocation**:
1. **Primary Motion**: 70% resources (main engine)
2. **Secondary Motion**: 20% resources (support)
3. **Experimental**: 10% resources (testing)

---

## Content Pyramid

### 3-Tier Structure

```
         🔺 Pillar Content (1-2/month)
        /  \   - 5,000+ word guides
       /    \  - Comprehensive, SEO-optimized
      /      \ - Reusable asset
     ──────────
    /          \
   / Derivative \  (3-5/week)
  /   Content    \ - Blog posts
 /                \ - Videos, podcasts
──────────────────
       Atomic        (1-3/day)
      Content        - Social posts
    (Bite-sized)     - Infographics
                     - Short-form video
```

### Pillar Content (Foundation)

**Definition**: Comprehensive, authoritative resource. Evergreen for 1+ years

**Types**:
1. **Ultimate Guide**: "The Complete Guide to [Topic]"
2. **Industry Report**: Self-conducted research data
3. **Framework/Methodology**: Proprietary framework
4. **Resource Hub**: Tools, templates collection

**Examples**:
- HubSpot "The Ultimate Guide to Email Marketing"
- Moz "Beginner's Guide to SEO"
- First Round Review "State of Startups Report"

**Cadence**: 1-2 monthly (quality over speed)

### Derivative Content (Deep Dives)

**Definition**: Pillar-derived content. Deep dives into specific topics

**Types**:
1. **Blog Posts**: Expand one Pillar chapter
2. **Videos**: Explain key concepts
3. **Podcast Episodes**: Expert interviews
4. **Webinars**: Hands-on workshops

**Example**:
- Pillar: "Complete Guide to CRM"
  - Derivative 1: "10 CRM Mistakes to Avoid"
  - Derivative 2: "How to Migrate from Excel to CRM" (Video)
  - Derivative 3: "CRM ROI Calculator" (Tool)

**Cadence**: 3-5 weekly

### Atomic Content (Social/Snackable)

**Definition**: Bite-sized for social. Instant consumption

**Types**:
1. **LinkedIn Posts**: Insights, stories
2. **X (Twitter) Threads**: Tips, frameworks
3. **Short-form Video**: TikTok, Reels, Shorts
4. **Infographics**: Stats, processes

**Example**:
- Pillar stat → Infographic
- Derivative quote → LinkedIn carousel
- Video clip → Reels

**Cadence**: 1-3 daily

### Content Repurposing (Multiplying)

**1 Pillar → 50+ Atomic**:
```
Ultimate Guide (Pillar)
  ↓
├─ 10 Blog Posts (Derivative)
├─ 5 Videos (Derivative)
├─ 1 Podcast Series (5 eps)
│
└─ Each Derivative becomes:
   ├─ 5 LinkedIn Posts
   ├─ 10 Tweets
   ├─ 3 Infographics
   └─ 5 Short Videos

Total: 1 Pillar → 20 Derivative → 50+ Atomic
```

---

## PESO Channel Distribution

### 4-Channel Framework

| Channel | Definition | Control | Cost | Speed | Credibility |
|---------|-----------|---------|------|-------|-------------|
| **Paid** | Bought advertising | High | High | Fast | Medium |
| **Earned** | PR, media coverage | Low | Low | Slow | High |
| **Shared** | Social media | Medium | Medium | Medium | Medium |
| **Owned** | Your channels | High | Medium | Medium | High |

### Paid (Advertising)

**Channels**:
- Google Ads (Search, Display)
- LinkedIn Ads (B2B)
- Facebook/Instagram Ads (B2C)
- Sponsored Content (newsletters, podcasts)

**Strategy**:
- **Bottom Funnel First**: High-intent keywords
- **Retargeting**: Website visitors
- **Lookalike**: Similar to existing customers
- **ROI Tracking**: CAC < LTV/3

**Budget Distribution**:
- Seed: 10-20% (experimental)
- Series A: 30-40% (expansion)
- Series B+: 40-50% (scale)

### Earned (PR & Recognition)

**Channels**:
- Press coverage (TechCrunch, local media)
- Guest blogging
- Podcast appearances
- Influencer mentions

**Strategy**:
- **Newsjacking**: React quickly to trends
- **Data Story**: Exclusive data for PR
- **Founder Story**: Startup background, challenges
- **Media Kit**: Press kit, logos, fact sheet

**Measurement**:
- Domain Authority improvement
- Backlink count
- Brand search volume increase

### Shared (Social Media)

**Channels**:
- LinkedIn (B2B)
- X/Twitter (Tech, Thought Leadership)
- YouTube (Tutorials)
- Reddit, Hacker News (Developers)

**Strategy**:
- **Consistency**: 3-5 posts weekly
- **Engagement**: Respond to comments
- **Employee Advocacy**: Team accounts
- **Hashtags**: Brand + industry tags

**Measurement**:
- Engagement Rate (>3%)
- Follower Growth (10% monthly)
- Social → Website traffic

### Owned (Your Channels)

**Channels**:
- Blog
- Email newsletter
- Podcast
- YouTube channel
- Community (Slack, Discord)

**Strategy**:
- **SEO**: Content matching search intent
- **Email List**: Lead Magnet for signup
- **Personalization**: Segment-specific content
- **Evergreen**: Timeless assets

**Measurement**:
- Organic Traffic (20% monthly growth)
- Email Open Rate (>20%)
- Newsletter → MQL (10-20%)

### PESO Distribution Strategy

**Stage-Based Recommendation**:

| Stage | Paid | Earned | Shared | Owned |
|-------|------|--------|--------|-------|
| **Pre-seed** | 10% | 20% | 30% | 40% |
| **Seed** | 20% | 20% | 30% | 30% |
| **Series A** | 35% | 15% | 25% | 25% |
| **Series B+** | 45% | 10% | 20% | 25% |

**Early (Pre-seed/Seed)**: Owned-focused (low CAC, long-term asset)
**Growth (Series A+)**: Paid expansion (fast scaling, predictable)

---

## Platform-Specific Strategy

### LinkedIn (B2B)

**Ideal ICP**: Decision-makers, professionals

**Content Types**:
1. **Personal Insight**: Experience, lessons learned
2. **Industry Trend**: Market analysis, predictions
3. **How-to**: Practical tips
4. **Behind-the-Scenes**: Team, culture

**Cadence**: 3-5 posts weekly

**Format**:
- Text: 1,300 characters (3-paragraph sweet spot)
- Carousel: 10-slide frameworks
- Video: 1-3 mins (native upload)

**Growth Tactics**:
- Comment engagement (1 hour after post)
- Engagement pods (peer groups)
- 3-5 hashtags

**Measurement**: Impressions, Engagement Rate, Profile Views → Connections

### X (Twitter)

**Ideal ICP**: Tech, Startups, Developers

**Content Types**:
1. **Threads**: Frameworks, stories
2. **Quick Tips**: One-line insights
3. **Meme/Humor**: Relatable, funny
4. **Polls**: Community engagement

**Cadence**: 1-5 posts daily

**Format**:
- Under 280 characters (concise)
- Image/GIF (2x engagement)
- Threads (long content)

**Growth Tactics**:
- Reply to industry leaders
- Retweet with comment
- Quote tweet (add opinion)

**Measurement**: Follower growth, Engagement Rate, Link clicks

### Newsletter

**Ideal ICP**: Deep relationships, long-term customers

**Content Types**:
1. **Weekly Digest**: Weekly insights
2. **Expert Interview**: Guest Q&A
3. **Case Study**: Customer success story
4. **Product Update**: New features

**Cadence**: Weekly or bi-weekly

**Format**:
- Subject: Under 40 chars, curiosity-driven
- Preview: 100-char summary
- Body: Scannable (headers, bullets)
- CTA: 1 clear action

**Growth Tactics**:
- Lead Magnet (eBook, template)
- Blog bottom CTA
- LinkedIn/X promotion

**Measurement**: Open Rate (>20%), Click Rate (>3%), Unsubscribe (<0.5%)

### Podcast

**Ideal ICP**: Commute listeners, gym workouts

**Content Types**:
1. **Founder Interview**: Startup stories
2. **Industry Expert**: Specialist insights
3. **Solo Episode**: Framework explanation
4. **Debate/Panel**: Multiple perspectives

**Episode Length**: 30-45 mins (commute time)

**Format**:
- Intro: 30 secs (today's summary)
- Main: 25-40 mins (interview/discussion)
- Outro: 2 mins (CTA, sponsor)

**Distribution**:
- Apple Podcasts, Spotify
- YouTube (video version)
- Blog (transcript)

**Measurement**: Downloads, Listener Retention, CTA clicks

---

## Brand Architecture

### Company vs Personal Brand

| Factor | Company Brand First | Personal Brand First |
|--------|----------------------|----------------------|
| **Focus** | Product, solution | Founder, philosophy |
| **Advantage** | Scalable, team emphasis | Trust fast, authentic |
| **Disadvantage** | Slow early trust | Founder dependency |
| **Examples** | Salesforce, Adobe | Tesla (Elon), Basecamp (DHH) |

**Recommended Combo** (Early Startup):
- **Pre-Series A**: 70% personal + 30% company
  - Founder brand for early traction
  - Company account for long-term asset
- **Series A+**: 60% company + 40% personal
  - Team scaling, product focus
  - Founder as Thought Leader

### Founder-Led Marketing

**Strategy**:
1. **Founder = Chief Storyteller**
   - Share company vision, mission
   - Explain product decisions

2. **Authentic Voice**
   - Share failures, challenges
   - Admit "we're not perfect"

3. **Consistent Cadence**
   - 3-5 posts weekly (LinkedIn/X)
   - Weekly newsletter
   - 1-2 monthly podcasts

**Cautions**:
- Clear personal/company boundary
- Credit the team
- Plan succession if founder exits

---

## Anti-Patterns (What NOT to Do)

### 1. Platform FOMO

**Symptom**: Run all channels → scattered, no effect

**Example**:
- LinkedIn, X, Instagram, TikTok, YouTube simultaneously
- Each channel <1 post/week
- No consistency

**Fix**:
- **Focus 1-2 platforms** (where ICP is)
- 3-month experiment → data-driven decision
- Other channels: repurpose only

### 2. Content Without Distribution

**Symptom**: Create great content → publish → done

**Example**:
- Blog post published, that's it
- 1 social share
- No email sent

**Fix**:
- **Production 30% + Distribution 70%**
- 1 content → 10 channel distribution
- Intense push first 48 hours

### 3. Competitor Copycat

**Symptom**: Copy competitor strategy → no differentiation

**Example**:
- "They do LinkedIn, so should we"
- Same messaging, tone
- No unique POV

**Fix**:
- **Differentiated Perspective** (Unique POV)
- Contrarian angle vs competitors
- Your data, experience-based

### 4. Vanity Metrics Obsession

**Symptom**: Track followers, impressions → business impact ignored

**Example**:
- Goal: 10K followers
- Actual result: 0 MQL, 0 customer conversion

**Fix**:
- **North Star**: MQL, Customer
- Middle metrics: CTR, Email signups
- Vanity: Supporting only

### 5. Consistency Gaps

**Symptom**: 2 weeks intense → 1 month pause → repeat

**Example**:
- "This quarter focus on content"
- One month later: stopped
- Next quarter: restart

**Fix**:
- **Sustainable Cadence**
  - 1/week better than 5/week for 1 month
  - Team rotation
  - 3-month content calendar

---

## 90-Day GTM Execution Plan

### Week 1-4: Foundation

**Goal**: Confirm GTM motion, define ICP, select channels, plan content

**Actions**:
- [ ] ICP workshop (3-5 personas)
- [ ] GTM motion selection (Primary + Secondary)
- [ ] Competitor channel analysis
- [ ] PESO distribution strategy
- [ ] 12-week content calendar
- [ ] Baseline measurement (current traffic, followers)

**Deliverables**:
- GTM Strategy Doc (10 pages)
- Content Calendar (Q1)

### Week 5-8: Launch

**Goal**: Open channels, publish initial content, collect feedback

**Actions**:
- [ ] Publish 1 Pillar Content
- [ ] Deploy 10 Derivative content
- [ ] Setup Owned channels (blog, newsletter)
- [ ] Activate Shared accounts (LinkedIn, X)
- [ ] Paid experiments ($1K budget)
- [ ] A/B test (headlines, CTA)

**Deliverables**:
- 1 Pillar + 10 Derivative
- 300+ email subscribers
- 100+ organic traffic/day

### Week 9-12: Optimize

**Goal**: Analyze data, optimize, prepare for scaling

**Actions**:
- [ ] Per-channel ROI analysis
- [ ] Repurpose top 3 content
- [ ] Expand Paid (high-performing channels)
- [ ] Partnerships (guest blogging)
- [ ] Customer interviews (case studies)
- [ ] Q2 strategy adjustment

**Deliverables**:
- GTM Performance Report
- Q2 Roadmap (priority adjustments)

---

## Related Skills

- **pricing-strategy**: Link GTM to pricing strategy
- **sales-playbook**: Execute Sales-Led motion
- **competitive-landscape**: Analyze competitor GTM
- **startup-metrics**: Track channel-level conversion

## Tips

- **Focus**: 2-3 channels >> 10 scattered
- **Consistency > Quality**: Good weekly > perfect monthly
- **Repurpose**: 1 content × 10 formats
- **Data-Driven**: 60-day experiment → decide
- **Founder Voice**: Early stage = powerful founder brand
- **Long Game**: Content marketing pays in 6-12 months
- **Community First**: Relationships & trust before sales
- **Authenticity**: Honest > hype (long-term wins)

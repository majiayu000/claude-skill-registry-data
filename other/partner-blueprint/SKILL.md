---
name: partner-blueprint
description: 'Partner and channel strategy architect that identifies, scores, and structures partnerships with mutual value propositions and co-GTM plans. Use when: partner strategy, channel partners, partnership, co-marketing, reseller strategy, integration partners, ecosystem strategy.'
---

# Partner Blueprint (BRIDGE Framework)

Engineer partnership strategy from identification through activation. Partnerships are a multiplier, not just a channel.

## When to Use
- Building partner/channel program from scratch
- Evaluating specific partnership opportunity
- Designing co-GTM with existing partner
- Expanding into new geography via partners
- Platform/ecosystem strategy

## What You'll Need
**Critical inputs (ask if not provided):**
- Your product and target market
- Partnership goals (reach, credibility, technology, revenue)
- Current partner landscape (if any)

**Nice-to-have:**
- Battle Scanner output (competitor partnerships to counter)
- Market Analyzer output (segments needing partner reach)

## Process

### Step 1: Partner Landscape Mapping
Identify candidates across 6 categories:

| Category | What They Offer | Examples |
|----------|----------------|---------|
| **Technology** | Integrations, platform plays | CRM, cloud providers, data platforms |
| **Channel/Reseller** | Reach into new segments/geos | VARs, MSPs, regional resellers |
| **Co-marketing** | Audience sharing, content collab | Complementary SaaS, media partners |
| **Implementation** | Consulting, deployment, training | SIs, boutique consultancies |
| **Strategic/OEM** | Embedded, white-label | Enterprise platforms, industry solutions |
| **Community/Ecosystem** | Developer communities, associations | Open-source projects, industry groups |

### Step 2: BRIDGE Scoring (per partner candidate, 1-10 each)

| Dimension | What It Measures | Scoring Guide |
|-----------|-----------------|---------------|
| **B**usiness-fit | Strategic alignment of customers and goals | 1=no overlap, 5=partial, 10=perfect alignment |
| **R**each | Incremental access to markets you cannot reach alone | 1=same audience, 5=some new, 10=opens new markets |
| **I**nvestment | Required time, money, engineering (inverse) | 1=massive investment, 5=moderate, 10=minimal |
| **D**ependencies | Risk of dependency (inverse) | 1=total dependency, 5=balanced, 10=no risk |
| **G**rowth-potential | Can this scale? Network effects? | 1=one-time, 5=linear growth, 10=exponential |
| **E**xecution-readiness | Team, processes, motivation to execute now | 1=not ready, 5=needs work, 10=ready to go |

**BRIDGE Score** = (B x 0.20) + (R x 0.20) + (I x 0.15) + (D x 0.10) + (G x 0.20) + (E x 0.15)

- 7.5+ = **Activate** (pursue immediately)
- 5.0-7.4 = **Develop** (invest in relationship, plan for future)
- Below 5.0 = **Monitor** (not worth active investment now)

### Step 3: Mutual Value Proposition Design
For each Activate partner:
- **What they get**: Technology, content, brand association, revenue share
- **What we get**: Distribution, credibility, access, technology
- **Joint customer value**: Why is 1+1 > 2?
- **Revenue model**: Referral fee, rev share, co-sell, embed, marketplace

### Step 4: Co-GTM Plan Template
For each activated partner:
- Joint messaging and positioning
- Co-marketing activities (webinars, content, events)
- Technical integration roadmap
- Sales handoff process and rules of engagement
- Success metrics and review cadence (monthly/quarterly)

## Output
Save to `outputs/partner-blueprint-[YYYY-MM-DD].md`

### Deliverables:
1. **Partner Landscape Map**: Categorized candidates with BRIDGE scores
2. **Partner Scorecards**: Detailed assessment per top-10 candidates
3. **Mutual Value Propositions**: Value exchange documents per partner
4. **Co-GTM Playbooks**: Joint go-to-market plans for activated partners

## Chain Connections
- **Next skill**: Run `community-catalyst` to design PLG and community programs
- **Also feeds**: `launch-command` (partner readiness is a launch gate), `demand-engine` (co-marketing expands channels)
- **Enhanced by**: Run after `battle-scanner` (competitive landscape reveals partnership opportunities)

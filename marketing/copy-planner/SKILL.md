---
name: copy-planner
type: planner
description: "Plan content briefs — audience, goals, messaging, success criteria. Prevents rewrites and scope drift before drafting."
version: 0.1.0
---

# Copy Planner Skill

## JTBD (Jobs To Be Done)

### Primary Job
When copy needs to be written but the team is not yet aligned on audience, message, and success criteria,
I want a clear brief before drafting starts,
so I can avoid expensive rewrites and keep everyone working toward the same outcome.

### Secondary Jobs
- When multiple stakeholders need input before writing, I want one agreed specification, so I can reduce debate during review.
- When a campaign or page is starting from scratch, I want a structured content plan, so the writer knows what "done" actually means.

### Job Layers
- Functional: Create a content brief that defines audience, goals, structure, message, and review criteria before copy is written.
- Emotional: Reduce the frustration of endless revisions, vague direction, and shifting stakeholder expectations.
- Social: Helps the user look organized and strategically clear to writers, editors, marketers, and approvers.

### This Skill Is For
- A user starting a page, campaign, blog post, email sequence, or messaging refresh and wanting alignment before writing.
- A user who wants to prevent scope creep or revision churn by locking a brief first.
- A user coordinating multiple contributors who need one shared target.

### This Skill Is NOT For
- A user who already has finished copy and wants it reviewed; use `copy-critic`.
- A user doing purely exploratory brainstorming with no need to lock the brief yet.

### Paired With
- `copy-critic`: After the draft exists, use it to review against the brief and quality criteria.
- `seo-advisor`: Use it when discoverability and search-intent alignment should shape the content structure.
- `brand-voice-guide`: Use it when voice and tone need stronger grounding in the brief.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Starting new content with unclear alignment | Copy Planner defines the brief | A writing target everyone can agree on |
| Managing many stakeholders | Copy Planner consolidates expectations | A shared decision document |
| Planning content that must also be discoverable | Copy Planner structures the brief, then hands off to `seo-advisor` as needed | A brief with stronger structural alignment |

### When to Escalate
- If the user already has draft copy and needs evaluation, escalate to `copy-critic`.
- If the user needs search-data-driven keyword work rather than structural planning, escalate to dedicated SEO tools outside this repo.

## Purpose

Writing without a brief is like building without a blueprint. Content briefs prevent costly rewrites, misaligned messaging, and off-brand deliverables. This skill creates **strategic content specifications** that guide writers, align teams, and enable efficient copy-critic review.

A good brief answers:
- **WHO** are we writing for? (audience, persona, psychographics)
- **WHAT** is the goal? (awareness, conversion, engagement, retention)
- **WHY** should they care? (value prop, key message, hook)
- **HOW** should we approach this? (tone, format, structure, evidence)
- **WHEN** is success? (metrics, review criteria, handoff checklist)

Without these answers locked in, writers guess. Stakeholders disagree. Multiple revision rounds follow.

## Use When

- Starting a new web page (landing page, product page, resource hub)
- Planning a blog post or thought leadership piece
- Creating an email campaign (drip series, newsletter, transactional)
- Developing social media content (organic or paid)
- Writing product descriptions, service pages, or case studies
- Launching new messaging for a campaign or brand refresh
- Multiple people need to provide input before writing begins
- You want to avoid mid-project scope creep or revision cycles

## Do Not Use When

- You're in an emergency rewrite cycle (write first, brief after)
- The content is purely exploratory/brainstorm (brief comes after exploration)
- You already have a detailed creative direction from a designer/strategist
- You're iterating on existing content (use copy-critic to review instead)

## Why This Exists

### Real-World Problems This Solves

**Scenario 1: Web page written without audience clarity**
- Writer assumes B2C SMB audience; stakeholder expected B2B enterprise
- Page emphasizes ease-of-use; enterprise buyers needed security credentials
- CTA is "Start Free Trial"; enterprise buyers need "Request Demo"
- Result: 3-round revision cycle, launch delay

**Scenario 2: Email copy without success criteria**
- Campaign sent without agreed metrics
- Copywriter optimizes for opens; marketer measured conversions
- Same data, different conclusions
- Result: Team debate, unclear if campaign succeeded

**Scenario 3: Blog post without outline agreement**
- Writer delivers 4,000-word deep dive
- Editor expected 1,200 words
- 60% of content needs cutting
- Result: Frustration, extended timeline

**Scenario 4: Product description without brand voice alignment**
- Copy mirrors competitor tone (clinical, feature-focused)
- Brand voice is conversational, benefit-focused
- Review round reveals mismatch
- Result: Major rewrite instead of fine-tune

**The Brief Prevents This**: All stakeholders align on goals, format, tone, and success criteria **before** writing begins. Writers have a clear target. Reviewers know what "done" looks like.

## Companion Skills

- **copy-critic**: Reviews finished copy against the brief. Completes the write-review cycle.
- **brand-voice-guide**: Defines organizational tone and style. Referenced in brief Phase 1 (brand voice specification).
- **seo-advisor**: Handles keyword strategy and technical SEO. Briefing phase includes structural topic planning (not data-driven SEO optimization).
- **doc-coauthoring**: Used in Phase 5 for collaborative brief refinement and handoff document creation.

## Skill Steps

### Step 1: Intake & Scope Clarification
Gather initial brief context:
- Content type/format (what kind of content?)
- Business goal (what should this content achieve?)
- Target audience segment (who reads this?)
- Key constraint (timeline, length, format, brand guidelines)

### Step 2: Content Brief Type Selection
Confirm which brief template applies:
1. **Web Page Brief** (landing, product, about, resource, service)
2. **Blog Post Brief** (thought leadership, how-to, listicle, case study, industry analysis)
3. **Email Brief** (nurture drip, newsletter, transactional, promotional)
4. **Social Media Brief** (organic feed content, paid ad copy, story/carousel)
5. **Product Description Brief** (ecommerce, app store, catalog)
6. **General Marketing Brief** (campaign-level messaging, repositioning, announcement)

### Step 3: Execute Full Planning Protocol (Phases 1-5)
Run the embedded protocol below with stakeholder input.

### Step 4: Create Deliverables
Generate:
- **Content Brief** (master document with all phases)
- **Writer's Outline** (section-by-section structure with key points)
- **Quality Checklist** (for writer + reviewer)
- **Review Criteria** (for copy-critic pass)

### Step 5: Handoff & Iteration
- Export brief document (Google Doc, Notion, or markdown)
- Establish review workflow (who reviews? copy-critic or manual review?)
- Set success metrics
- Prepare for doc-coauthoring workflow for collaborative refinement

---

## Full Copy Planning Protocol

### Phase 1 — Audience & Goal Definition

**Purpose**: Lock in WHO we're writing for and WHAT we want them to do.

**Prompts & Questions**:

**1. Target Persona**
- Primary audience segment (job title, industry, company size, experience level)
- Demographics (age range, location, education level)
- Psychographics (mindset, values, priorities, pain points)
- Current awareness state (unaware, problem-aware, solution-aware)
- Decision-making role (user, influencer, decision-maker, buyer)

**Example**: *Primary: Marketing director at mid-market B2B SaaS. Age 30-45, manages 2-5 person team. Pain points: limited budget for tools, pressure to prove ROI, overwhelmed by vendor options. Currently aware of the problem but evaluating solutions.*

**2. Content Goal** (select one, can have secondary)
- **Awareness**: Introduce product/concept to new audience
- **Consideration**: Help audience evaluate options or understand approach
- **Conversion**: Drive action (signup, purchase, demo request, consultation)
- **Retention/Advocacy**: Deepen relationship with existing customers
- **Education**: Build expertise and trust as thought leader

**3. One-Sentence Key Message**
The single idea readers should remember after consuming content.

**Bad**: *"We offer cloud-based marketing automation."* (feature)
**Good**: *"Modern marketing teams spend 30% less time on manual tasks when they adopt intelligent automation."* (outcome)

**4. Desired Action (CTA)**
What specific action should the reader take after consuming the content?
- Sign up for email list
- Download resource
- Request demo
- Make purchase
- Visit product page
- Share content
- Schedule consultation

**5. Success Metrics** (how will we know this content worked?)
- Pageviews / unique visitors
- Time on page (engagement depth)
- Conversion rate (clicks to CTA)
- Engagement (shares, comments, saves)
- Email open/click rate (if applicable)
- Lead quality (sales qualified vs. MQL)
- Brand lift (perception shift)

**6. Brand Voice Reference**
- Link to brand-voice-guide if available
- Key tone attributes (professional/conversational, formal/casual, expert/peer, authoritative/helpful)
- Any content examples that nail your voice

---

### Phase 2 — Content Strategy

**Purpose**: Choose the FORMAT and ANGLE that best reaches the audience with the message.

**1. Content Type & Format Selection**
Selected: _______
Rationale:
- Why this format? (matches audience consumption preference, aligns with goal, fits platform)
- What competing formats were considered and rejected?
- Format specifications (word count if known, visual requirements, interactive elements)

**Examples by Content Type**:

| Type | Format Options | Best For |
|------|---|---|
| **Web Page** | Long-form sales page, scannable product page, detailed resource guide, FAQ, comparison | Different audience readiness levels |
| **Blog** | How-to tutorial, original research, curated roundup, listicle, case study, opinion | SEO, thought leadership, audience education |
| **Email** | Promotional, educational, re-engagement, nurture sequence, announcement | Warm audiences, multi-touch campaigns |
| **Social** | Text-only carousel, video teaser, quote graphic, behind-the-scenes, live stream, CTA post | Platform-specific, fast consumption |
| **Product Description** | Feature-focused, benefit-focused, lifestyle positioning, technical specifications, use case | Shopping context, product discovery |

**2. Keyword/Topic Research Summary**
(Note: Structural topic planning, not SEO data optimization)

Topics to cover (in priority order):
- Primary topic (what's the main subject?)
- Secondary topics (what supports the main idea?)
- Related concepts reader needs context for
- Objection/concern topics to address
- Comparison topics (if competitive positioning needed)

**3. Competitor Content Analysis**
What exists in this space?
- Competitor pieces (titles, angles, length)
- What are they doing well?
- What gaps exist? (What's missing or underexplained?)
- How will your content be different?

**4. Content Angle/Hook**
What makes THIS piece unique or compelling?
- Angle: *"Automation + human touch" instead of "automation replaces people"*
- Hook: *"Most teams waste 30 hours/month on busywork"* (opens with tension)
- Unique data/research: *"Our analysis of 500+ teams shows..."*
- Contrarian take: *"Industry best practice is wrong because..."*
- Personal narrative: *"Here's how we changed our process..."*

**5. Tone and Reading Level**
- Tone: (reference brand voice)
  - Professional/Conversational
  - Formal/Casual
  - Expert/Peer
  - Authoritative/Approachable
- Reading level target:
  - Executive summary (skim in 2 min)
  - General reader (8th grade+ reading level)
  - Industry expert (specialized terminology acceptable)
  - Mixed audience (explain jargon, multiple difficulty levels)

**6. Length Recommendation with Justification**
Recommended length: _______ words
Rationale:
- Audience consumption context (how much time do they have?)
- Topic complexity (simple = shorter, complex = longer)
- Platform/medium requirements
- Precedent (what performs well for this audience?)
- Format requirements (scannable lists need different length than narrative)

---

### Phase 3 — Content Architecture

**Purpose**: Design the STRUCTURE that guides reader from headline to CTA.

**1. Outline/Structure with Section Purposes**

**Intro/Hook Section**
- Purpose: Capture attention, establish relevance, preview value
- Length guideline: 50-150 words
- Key elements:
  - Hook (question, statistic, or tension)
  - Reader benefit statement (why they should keep reading)
  - Preview of what's covered
  - [Include bridge to main section]

**Main Body Section 1: [Topic]**
- Purpose: [What should reader understand/believe after this section?]
- Key points to cover:
  - Point A
  - Point B
  - Point C
- Evidence needed: (statistic, example, testimony, screenshot)
- Transition to next section: [how does this connect?]

**Main Body Section 2: [Topic]**
- Purpose: [Learning objective]
- Key points:
  - Point A
  - Point B
- Evidence needed:
- Transition:

[Continue for all main body sections]

**Objection/Concern Section**
- Purpose: Address "but what about..." questions before reader leaves
- Common objections to counter:
  - Objection 1 → Counter
  - Objection 2 → Counter
- Format: FAQ, short paragraphs, or [other]

**CTA/Closing Section**
- Purpose: Clarify next step and remove friction
- CTA button/link text: [e.g., "Request Your Free Demo"]
- Supporting text: [brief why they should act now]
- Secondary CTA: [optional backup action if primary feels too big]
- Trust signals: (testimonial quote, guarantee, social proof, credential)

**2. Heading Hierarchy**
```
H1: [Main headline]
  H2: Section 1 Topic
    [Body content]
    H3: Subsection detail if needed
  H2: Section 2 Topic
    [Body content]
  H2: Objections
    [Body content]
  H2: CTA Section
    [Body content]
```

**3. Key Points Per Section**
(Already covered in outline above — ensure 2-4 key ideas per section)

**4. CTA Placement Strategy**
- Primary CTA location: [top, middle, bottom, or multiple placements?]
- CTA format: [button, inline link, form, calendar, other]
- CTA frequency: [how many times is this CTA repeated?]
- Rationale: [why this placement works for this audience]

**5. Trust Signals Needed**
Identify where credibility is essential:
- Customer testimonial/review: [what should it cover?]
- Statistical evidence: [what stat would validate the claim?]
- Credential/authority: [expert name, certification, publication]
- Security/compliance badge: [if relevant to B2B purchase decision]
- Before/after or case study: [which scenario to feature?]
- Guarantee/promise: [what removes risk?]

**6. Visual Content Guidance**
- Hero image: [what should it convey? style?]
- Inline images/screenshots: [where and why?]
- Diagrams/infographics: [concepts that need visualization?]
- Video: [where would video add value? what type?]
- Icons/graphics: [navigation, feature callouts, step-by-step illustration?]
- Alt-text approach: [descriptive for accessibility]

**7. Internal/External Link Strategy**
- Internal links: [what should link to existing content to build SEO authority?]
- External links: [what resources should we cite? credibility signals?]
- Competitor references: [any useful comparisons to reference?]

---

### Phase 4 — Evidence & Source Planning

**Purpose**: Identify what RESEARCH and ASSETS we need before writing begins.

**1. Claims That Need Citations**
List every assertion that requires support:
- Claim: *"Automation reduces manual work by 30%"*
  Source needed: [industry report, research study, case data?]
  Priority: [high/medium/low]

- Claim: [Next claim]
  Source needed:
  Priority:

[Continue for all major claims]

**2. Statistics/Data to Gather**
- Statistic 1: [What data point would strengthen this section?]
  Owner: [who finds this?]
  Timeline: [when needed?]

- Statistic 2:
  Owner:
  Timeline:

**3. Subject Matter Expert Interviews Needed**
- Interview 1: [What expert, what topic, what quote do we need?]
  Name/Contact: [if known]
  Timeline: [by when?]

- Interview 2:
  Name/Contact:
  Timeline:

**4. Competitor References to Analyze**
- Competitor A: [URL, what are they saying?]
- Competitor B: [URL, what angles are they taking?]
- Competitive advantage we're highlighting: [how we differ]

**5. Brand Assets to Incorporate**
- Logo placement: [where, size, usage]
- Product screenshots: [which features to show?]
- Company photos: [team, office, events?]
- Customer logos: [which customers to feature?]
- Case study data: [metrics, quotes, results]

---

### Phase 5 — Quality Assurance Planning

**Purpose**: Define what "done" looks like and set up for efficient review.

**1. Brand Voice Checklist**
(Pulled from brand-voice-guide or defined here)

Before copy-critic review, writer should verify:
- [ ] Tone matches brand voice (professional/conversational balance)
- [ ] No jargon without explanation (or jargon matches audience expertise)
- [ ] Active voice used (not passive construction)
- [ ] Sentence length varied (mix short and medium, avoid long)
- [ ] Benefit-forward language (what's in it for reader, not just features)
- [ ] No sales-y clichés (*"world-class," "best-in-class," "leverage,"* etc.)
- [ ] Consistent terminology (same term for same concept throughout)
- [ ] [Add 2-3 brand-specific checks]

**2. Reading Level Target**
- Target readability score: [Flesch-Kincaid grade level, ___]
- Approach: [short paragraphs, subheadings, bullet points, glossary for terms, other]

**3. Accessibility Requirements**
- Alt-text: [descriptive image captions for every visual]
- Plain language: [define acronyms on first use, explain acronyms]
- Link text: [descriptive link anchors, not "click here"]
- Heading hierarchy: [proper H1→H2→H3 nesting for screen readers]
- Color contrast: [text readable on background, not color-coded as sole identifier]

**4. SEO Requirements** (technical page elements)
- Meta title: [recommended title tag, 50-60 characters]
- Meta description: [recommended description, 155-160 characters]
- H1 tag: [should include primary keyword naturally]
- URL slug: [recommended URL structure]
- Internal link anchors: [2-3 internal pages to link to]

**5. Review Workflow**
Who reviews this and in what order?
1. **Writer self-review**: [use brand voice checklist above]
2. **[Stakeholder review]**: [marketing, product, legal, other?]
3. **copy-critic subagent**: Runs automated review against this brief + brand-voice-guide
4. **[Final sign-off]**: [who approves before publication?]

Timeline: [how many days for each stage?]

**6. Success Criteria for Finished Piece**
The brief is done when:
- [ ] All sections filled in detail
- [ ] Stakeholders have signed off on outline
- [ ] All evidence sources identified or acquired
- [ ] Writer confirms they understand the brief
- [ ] copy-critic integration configured (if using)
- [ ] Timeline locked in

The *content* is successful when:
- [ ] Meets reading level target
- [ ] Includes all evidence/sources
- [ ] Follows outline structure and word count
- [ ] Passes brand voice checklist
- [ ] Achieves target CTA click rate / conversion rate
- [ ] [Metric 2: specific to this content]
- [ ] [Metric 3: specific to this content]

---

## Tool Usage

### Recommended Workflow

1. **Intake conversation**: Gather initial context (goal, audience, type, constraints)
2. **Brief template selection**: Choose the right template above
3. **Collaborative completion**: Work through Phases 1-5 with stakeholder input
4. **Export brief**: Save as shared document (Google Doc, Markdown, Notion) for reference during writing
5. **Handoff to writer**: Writer receives outline + checklist + success criteria
6. **Review setup**: Prepare for copy-critic pass or manual review
7. **Iterative refinement**: If brief needs adjustment during writing, use doc-coauthoring skill for collaborative updates

### Integration with doc-coauthoring Skill

When brief needs to be refined collaboratively:
- Use doc-coauthoring `compose` phase for initial drafting
- Use `refine` phase for stakeholder feedback incorporation
- Use `test` phase to validate brief against draft copy

### Integration with copy-critic Skill

After copy is written:
- Invoke copy-critic with this brief as reference
- copy-critic checks finished copy against all brief criteria
- Results feed back into revision cycle (if needed) or publication approval

---

## Examples

### Example 1: Landing Page Brief

**Content Type**: Web Page (Product Landing)
**Goal**: Drive conversions from marketing campaign traffic
**Audience**: Marketing manager at SMB, evaluating email marketing tools
**Key Message**: Save 10 hours/week on repetitive email tasks, focus on strategy

**Phase 1**: [Persona: Marketing director, 2-5 person team, limited budget, wants ROI proof]
**Phase 2**: [Format: Scannable landing page, 1200 words, benefit-focused design]
**Phase 3**: [Structure: Problem → Solution → Proof → CTA with 3 objection counters]
**Phase 4**: [Sources: Customer case study (30% time savings), ROI calculator, 2 testimonials]
**Phase 5**: [Success: 8% CTA click rate, 2% conversion to demo request, tone passes brand check]

---

### Example 2: Blog Post Brief

**Content Type**: Blog Post (How-To)
**Goal**: Awareness + thought leadership positioning
**Audience**: Early-stage founder learning startup operations
**Key Message**: Delegation is a learned skill, not a sign of weakness—here's the framework

**Phase 1**: [Persona: First-time founder, solopreneur mindset, overwhelmed by 100 tasks]
**Phase 2**: [Format: Step-by-step guide, 2000 words, conversational tone, personal narrative]
**Phase 3**: [Structure: Intro (vulnerability) → 5-step framework → mistakes to avoid → CTA for mini-course]
**Phase 4**: [Sources: Founder interviews (3), book references (2), personal experience, no original research]
**Phase 5**: [Success: 500+ pageviews, 30+ email signups, shares indicate resonance]

---

## Notes

- **Briefing is not waste**: It feels slower upfront but saves 2-3x time in revision cycles. Measure time-to-publication, not time-to-first-draft.
- **Stakeholder alignment**: Brief creates the conversation about what success looks like before writing begins. Saves argument later.
- **Reusable briefs**: For content series or recurring content types, save templates and refine them over time.
- **Brief-to-draft ratio**: Good brief should reduce writing time by 30-40%. Writer should not be making strategy decisions while drafting.
- **copy-critic integration**: Pair this skill with copy-critic for end-to-end write-review cycle. Brief provides context; copy-critic enforces execution.

---

## Frontmatter Installation Note

When installed via `npx claude-skills add` or manual copy to `~/.claude/skills/copy-planner/`, this SKILL.md becomes a slash command `/copy-planner` available in Claude Code.

To invoke:
```
/copy-planner
```

This routes to the associated agent (`copy-planner.md` in `~/.claude/agents/`), which runs the full planning protocol.

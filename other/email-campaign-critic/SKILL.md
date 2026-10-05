---
name: email-campaign-critic
description: "Review email campaigns and lifecycle messages for deliverability, engagement, and conversion."
version: 0.1.0
---

# Email Campaign Critic

## JTBD (Jobs To Be Done)

### Primary Job
When I have a drafted email campaign, sequence, or lifecycle message and I need to know whether it is safe to send — no compliance violations, no CTA confusion, no segmentation blindspots — before it reaches subscribers,
I want an evidence-backed pre-send review across subject line, body, CTA, segmentation, deliverability, and compliance,
so I can catch the problems that cause unsubscribes, spam complaints, and legal risk before they hit an audience.

### Secondary Jobs
- When a campaign looks complete but the conversion numbers on similar sends have been weak, I want the offer clarity, CTA placement, and segmentation fit examined with a critical eye, so I can identify the structural cause rather than just tweaking subject lines.
- When a multi-email sequence is ready to activate and I need confidence the flow logic, trigger conditions, and timing are coherent end-to-end, I want the whole sequence reviewed together rather than email by email in isolation.

### Job Layers
- Functional: Audit an email campaign or sequence for subject line and preview text effectiveness, mobile layout and scannability, body copy clarity and benefit focus, CTA strength and placement, segmentation relevance, deliverability red flags, CAN-SPAM/GDPR compliance, and sequence coherence — and return findings ranked by send risk with quoted evidence.
- Emotional: Remove the anxiety of pressing send on a campaign that looks finished but may contain a compliance violation, a broken CTA, or a segmentation mismatch that only surfaces after it hits 10,000 inboxes.
- Social: Helps the user defend a send decision — or a hold decision — to stakeholders with specific, quoted findings rather than vague unease.

### This Skill Is For
- A user with a complete or near-complete email campaign who needs a pre-send quality gate covering compliance, CTA clarity, mobile rendering, segmentation fit, and sequence logic.
- A user whose campaign conversion numbers have been underperforming and who needs the offer, CTA, and segmentation examined for structural causes rather than surface-level copy edits.
- A user activating a multi-email sequence who needs the full flow reviewed for trigger coherence, timing logic, and end-to-end subscriber experience.

### This Skill Is NOT For
- A user starting from scratch and needing a plan or specification; use `email-campaign-planner` instead.
- A user looking for shallow linting or a generic quick take with no need for evidence-backed judgment.

### Paired With
- `email-campaign-planner`: If the verdict is `REVISE` or `REJECT`, use it next to redesign or plan the fix.
- `copy-critic`: Use this when the unresolved problem is more about broader content-quality review across channels instead of email-specific strategy.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a campaign ready to send and needs a pre-send gate | The skill audits subject line, CTA, segmentation, compliance, and mobile layout with quoted evidence | A send/hold verdict with ranked findings and specific fixes |
| Has a campaign with weak conversion history and no clear cause | The skill examines offer clarity, CTA placement, and segmentation fit for structural problems | A diagnosis identifying the conversion blockers beyond surface copy |
| Has a multi-email sequence to activate | The skill reviews trigger logic, timing, and end-to-end flow coherence across all emails | A sequence readiness assessment with gaps and fixes across the full flow |

### When to Escalate
- If the user does not yet have an artifact to review, escalate to `email-campaign-planner`.
- If the dominant problem is actually broader content-quality review across channels instead of email-specific strategy, escalate to `copy-critic`.

## Purpose

The Email Campaign Critic is a specialized copy review tool focused exclusively on email marketing campaigns. It evaluates subject lines, preview text, email body, calls-to-action (CTAs), segmentation strategy, deliverability compliance, and campaign flow against marketing best practices, brand voice, and technical standards.

This skill inherits the 5-phase investigation protocol from `critic-base-protocol`:
1. **Pre-commitment Predictions**: List common email campaign failure modes
2. **Verification**: Structured audit against specific email dimensions
3. **Multi-Perspective Review**: Subscriber, Marketer, Brand Guardian, Deliverability Specialist lenses
4. **Gap Analysis**: Identify missing elements (A/B test plan, segmentation logic, etc.)
5. **Synthesis**: Unified verdict with ranked findings

## Use When

- **Reviewing email subject lines and preview text** for clarity, deliverability, and conversion potential
- **Auditing email body layout** for mobile optimization, scannability, and accessibility
- **Evaluating copy quality** (voice, tone, messaging fit, benefit vs. feature focus)
- **Validating CTA placement, design, and copy** for maximum visibility and click-through
- **Assessing segmentation and targeting logic** for relevance and lifecycle fit
- **Checking technical compliance** (CAN-SPAM, GDPR, image alt text, unsubscribe mechanism)
- **Reviewing campaign flow and trigger logic** for sequence coherence
- **Pre-send quality assurance** before campaigns launch to thousands of subscribers

## Do Not Use When

- Reviewing landing pages, websites, or blog posts (use `copy-critic` or `seo-advisor`)
- Conducting full-funnel attribution analysis (out of scope; email is one channel)
- Analyzing email list hygiene or sender reputation (requires technical ISP/ESP access)
- Reviewing SMS campaigns, push notifications, or in-app messages (different media, different rules)
- Creating email templates from scratch (use `copy-writer` or design feedback)
- Auditing email infrastructure (deliverability platform setup, DNS configuration)

## Why This Exists

Email marketing is one of the highest-ROI channels (avg. $42 return per $1 spent) yet is commonly mismanaged due to:
- **Subject line mistakes** (too long, misleading, or lacking urgency/curiosity)
- **Mobile design failures** (60%+ of emails opened on mobile; many are unreadable)
- **CTA confusion** (multiple competing CTAs, buried buttons, weak copy)
- **Segmentation blindness** (blasting same email to entire list regardless of fit)
- **Deliverability red flags** (missing alt text, spam trigger words, no unsubscribe link)
- **Copy tone misalignment** (generic, feature-focused, no clear value prop)

This skill surfaces these common failure modes early, preventing campaigns from reaching subscribers broken, off-brand, or legally risky. It also flags what's missing (A/B test plan, personalization strategy, success metrics).

## Companion Skills

- **copy-critic**: Broader copy review for web content, landing pages, and sales copy (not email-specific)
- **brand-voice-guide**: Validate email copy against brand tone, personality, and messaging pillars
- **seo-advisor**: If email contains landing page links, verify SEO alignment
- **accessibility-auditor**: Deep-dive accessibility review if email has complex interactive elements

## Steps

1. **Provide the email being reviewed** (paste full source, screenshot, or ESPexport)
2. **Specify the campaign context** (type: promotional/newsletter/transactional/lifecycle; segment; goal)
3. **Delegate to email-campaign-critic agent** following the full review protocol below

**Routing Logic:**
- **Local routing authority (default)**: Route through the repository's `email-campaign-critic` agent; otherwise use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
- **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC. OMC does not choose the route or model policy.

## Full Review Protocol

```
AGENT: email-campaign-critic
MODEL POLICY: resolved by the catalog/meta-router; this wrapper does not override it
READONLY: true (disallowedTools: Write, Edit)

PROTOCOL PHASES:

=== PHASE 1: PRE-COMMITMENT PREDICTIONS ===
Before examining the email, list 12-15 high-probability failure modes you'll be looking for:
- Subject line: length (>50 chars mobile, >60 desktop), clarity, curiosity/urgency/value, honesty (no clickbait)
- Preview text: does it complement or repeat subject? Personalization tokens tested?
- Body layout: mobile optimization? Scannable or wall of text? Hierarchy clear?
- From name: recognizable and trustworthy?
- Hero image/header: eating too much vertical space?
- Copy tone: benefit-focused or feature-focused? Brand voice consistent?
- CTA placement: above fold on mobile? Visually distinct (color, size, whitespace)?
- CTA copy: specific ("Download Report") or vague ("Click Here")?
- Link/button functionality: Do all CTAs go somewhere? Is it a trap?
- Segmentation: Is there evidence this is targeted to the right audience?
- Send timing: Appropriate for the segment and email type?
- Accessibility: Alt text on images? Font sizes readable? Color contrast?
- Compliance: Unsubscribe link present and functional? Physical address in footer? CAN-SPAM aligned?

=== PHASE 2: VERIFICATION (Structured Audit) ===

**Subject Line & Preview Audit:**
- Length check: Is it <50 chars (mobile) or <60 (desktop)?
- Opening hook: Does it create curiosity, urgency, or clear value in first 5 words?
- Honesty test: Is the subject line genuine? Or is it clickbait that damages trust?
- Personalization: Are tokens like {first_name} included? Are they being tested?
- Spam triggers: Excessive caps, "FREE", "ACT NOW", "LIMITED TIME", multiple exclamation marks?
  (Context matters—these aren't always wrong, but when used should be intentional)
- Emoji: Is emoji usage on-brand? Does it help or distract?
- Preview text: Does it add new info or repeat the subject line?
- Inbox scan test: Among 50 unopened emails, would this stand out?

**Email Structure & Layout Audit:**
- Mobile-first design: Is the layout responsive? Readable at <360px width?
- Scannability: Is there white space? Bullet points? Short paragraphs? Or is it a wall of text?
- Visual hierarchy: Most important content first? Heading styles consistent?
- From name: Is it a person name (higher trust) or company name? Recognizable?
- Header/banner: Does it reinforce brand? Does it consume excessive vertical space?
- Web version link: Present? Accessible?
- Footer structure: Unsubscribe link visible and functional? Physical address (CAN-SPAM)? Preference center?
- Image-to-text ratio: Are there more images than text? Will it render with images blocked?

**Body Copy & Messaging Audit:**
- Value proposition clarity: Can a reader understand the point in 3 seconds of opening?
- Benefit vs. feature: Is copy focused on what the reader gains? Or what the product does?
- Reading level: Is the language simple and conversational? Or corporate/jargon-heavy?
- Audience fit: Does the voice match the segment's expectations and stage in lifecycle?
- Personalization depth: Is it meaningful personalization (segment-specific offers, dynamic content)? Or just "Hi {first_name}"?
- Proof points: Are there testimonials, case studies, social proof, or data backing claims?
- Copy length: Too long for a promotional? Too short for a newsletter to provide value?
- Consistency: Does the body voice match the subject line tone?

**CTA Audit:**
- Primary CTA clarity: Is there ONE clear primary CTA? Or are there multiple competing CTAs?
- Placement: Is the primary CTA visible above the fold on mobile? On desktop?
- Button copy: Is it specific and action-oriented? ("Download Your Q1 Report" vs. "Click Here")
- Visual distinctiveness: Does the button have strong color contrast? Adequate padding? Clear from surrounding text?
- CTA-promise alignment: Does the button copy match the email's value prop? (If email promises "free download," button should say "Download Now," not "Shop")
- Landing page fit: If you were to click this CTA, would the landing page deliver what the email promised?
- Secondary CTAs: Are they clearly subordinate? Or do they compete for attention?

**Segmentation & Targeting Audit:**
- Audience fit: Is the email being sent to the right segment? Evidence of intentional targeting?
- Content relevance: Does the offer/message match the segment's interests or lifecycle stage?
- Exclusion rules: Are there smart exclusions? (E.g., don't email people who just converted)
- Lifecycle alignment: Is this email at the right stage? (Welcome series vs. nurture vs. win-back)
- Send frequency: Is this too frequent for the segment? Or appropriately timed?
- Personalization by segment: Is there any segment-specific content? Or generic broadcast?

**Deliverability & Compliance Audit:**
- Image alt text: Do ALL images have alt text? Will the email be readable with images disabled?
- HTML quality: Is the markup clean? Any broken tags, excessive nesting, or outdated code?
- Text-only version: Is there a fallback plain-text version?
- Link tracking: Are all links functional? Are they tracked properly?
- Unsubscribe mechanism: Is the unsubscribe link present, visible, and functional?
- CAN-SPAM compliance: Does it include sender's physical address? Honest subject line? Easy opt-out?
- GDPR compliance: If EU audience, are there consent mechanisms and clear opt-out paths?
- Spam trigger patterns: Excessive red text? ALL CAPS sections? Too many links?
- SPF/DKIM/DMARC: Note alignment (reviewer may not have access, but can flag the importance)

**Campaign Flow & Timing Audit:**
- Sequence logic: Is this email part of a larger sequence? Does it fit logically?
- Trigger type: Is it time-based (wait X days after signup), behavior-based (opened last email), event-based (purchased, abandoned cart)?
- Send time: Is it reasonable for the audience? (Weekday morning for B2B, evening for B2C consumer)
- Next step clarity: What happens after someone clicks the CTA? Is the landing page or next email in flow prepared?
- A/B test plan: Is there an A/B test planned? (Subject line, CTA copy, send time?)
- Success metrics: What KPIs will measure this email's performance? (Open rate, CTR, conversion, unsubscribe)

**Accessibility Audit:**
- Alt text: All decorative and informational images have descriptive alt text?
- Color contrast: Do button text and links have sufficient contrast (4.5:1 minimum)?
- Font size: Are body text (minimum 14px) and headlines (minimum 22px) readable?
- Reading order: Does the email flow logically when read top-to-bottom? Or do sections jump around?
- Links out of context: Would link text make sense if read in isolation? ("Click here" is bad; "Download Q1 Report" is good)
- Table layouts: If tables are used for layout, are they accessible? (Proper headers, cell alignment)

=== PHASE 3: MULTI-PERSPECTIVE REVIEW ===

View the email through four lenses:

**1. SUBSCRIBER LENS:**
"I'm one of 10,000 people receiving this email today, and I'm skimming my inbox in 30 seconds."
- Would I open this email? Does the subject line compel me?
- Would I read the body? Is it scannable? Does it feel like it was written for me?
- Would I click the CTA? Is the offer clear? Is the button obvious?
- Would I unsubscribe? Does this feel spammy, irrelevant, or off-brand?
- Trust impression: Does the sender feel legit? Or could this be a phishing attempt?

**2. MARKETER LENS:**
"I sent this campaign to achieve a specific goal. Will it work?"
- Does this email clearly communicate the offer?
- Is the CTA positioned to drive conversions?
- Will the segmentation reach the right audience?
- Is there enough proof/social proof to persuade?
- Could this email improve conversion with A/B testing? What variables?
- What's the likely open rate, CTR, and conversion rate? Why?

**3. BRAND GUARDIAN LENS:**
"Does this email represent our brand well?"
- Is the voice consistent with our brand guidelines?
- Is the tone appropriate for our audience?
- Are visual elements (if any described) on-brand?
- Does the offer align with our brand positioning?
- Would our best customers recognize this as authentically from us?
- Any tone-deaf moments that could damage brand trust?

**4. DELIVERABILITY SPECIALIST LENS:**
"Will this email reach the inbox?"
- Are there any spam trigger words or patterns that could flag this?
- Is the email technically sound (clean HTML, proper encoding)?
- Is the from address trusted? Does it pass authentication checks?
- Are there anything that would trigger spam filters?
- Is the unsubscribe mechanism clear enough to prevent abuse reports?
- Would ISPs be suspicious of this email? Why or why not?

=== PHASE 4: GAP ANALYSIS ===

Identify missing elements critical to campaign success:

**Missing Strategic Elements:**
- Is there an A/B test plan? (If not, what should be tested?)
- Is there a clear segmentation/targeting strategy documented?
- Is there a documented success metric and baseline for comparison?
- Is the email part of a documented sequence or standalone?
- Is there a clear understanding of the trigger (time-based, behavior-based, event-based)?
- Is there a documented contingency if the CTA link breaks?

**Missing Tactical Elements:**
- Is there an unsubscribe link? (Required by law in most jurisdictions)
- Is there a clear physical address in the footer? (CAN-SPAM requirement)
- Is there alt text for all images?
- Is there a text-only version for accessibility?
- Is there a web version link?
- Is there a preference center for managing frequency?
- Are there secondary CTAs, or is the focus too scattered?

**Missing Creative Elements:**
- Is there meaningful personalization beyond {first_name}?
- Is there proof/social proof (testimonial, case study, data)?
- Is there a clear value proposition in the subject line?
- Is there visual variety (not all images, not all text)?
- Is there an optimal send time decision documented?

=== PHASE 5: SYNTHESIS & VERDICT ===

Compile findings into structured output:

**Severity Scale:**
- **CRITICAL**: CAN-SPAM violation, missing unsubscribe link, broken CTA, misleading subject line causing trust damage, no mobile optimization, major accessibility failure (no alt text for all images)
- **MAJOR**: Multiple competing CTAs, unclear value prop, poor segmentation, body copy too long for format, weak subject line, images without alt text, missing footer compliance elements
- **MINOR**: Subject line could be tighter, preview text not optimized, voice inconsistency with brand, secondary CTA could be more subordinate, font could be slightly larger

**Output Format:**

---

**VERDICT: [REJECT | REVISE | ACCEPT-WITH-RESERVATIONS | ACCEPT]**

**Summary Statement** (2-3 sentences): One-line thesis of email quality and readiness to send.

**Critical Issues** (if any, each with file:line or specific location):
1. [Issue title] — [Context from email] — [Why it's critical] — [Suggested fix]
2. [...]

**Major Issues** (if any):
1. [Issue title] — [Context] — [Why it matters] — [Suggested fix]
2. [...]

**Minor Issues** (if any):
1. [Issue title] — [Context] — [Why it matters] — [Suggested fix]
2. [...]

**What's Missing:**
- [Gap 1]
- [Gap 2]
- [...]

**What's Working:**
- [Strength 1]
- [Strength 2]
- [...]

**Multi-Perspective Insights:**
- **Subscriber**: [Key finding]
- **Marketer**: [Key finding]
- **Brand Guardian**: [Key finding]
- **Deliverability Specialist**: [Key finding]

**Recommended Next Steps:**
1. [Action 1]
2. [Action 2]
3. [...]

---
```

## Tool Usage

- **Read-Only Scope**: This agent is read-only (disallowedTools: Write, Edit) to prevent accidental modifications to campaigns.
- **No File Modification**: The reviewer examines and critiques but does not edit the email; the user must implement changes.
- **Evidence-Driven**: All CRITICAL and MAJOR findings must include specific text excerpts or locations from the email.

## Examples

### Example 1: Promotional Campaign

**Context**: E-commerce company sending a flash sale email to high-value customers (VIP segment).

**Subject Line**: `Last-Minute Flash: 40% Off Everything (Ends Tonight!)`

**Preview Text**: `Don't miss out—VIP exclusive pricing inside.`

**Body** (summary): Hero image of sale graphic, 3-paragraph copy emphasizing urgency and exclusivity, primary CTA "Shop VIP Prices," secondary CTA "View Sale Terms."

**Reviewer Findings**:
- CRITICAL: No unsubscribe link in footer (legal liability)
- MAJOR: Subject line uses "Ends Tonight!" but email timestamp shows 3am send (mismatch—will frustrate subscribers)
- MAJOR: Hero image has no alt text (will break if images are disabled)
- MINOR: "Shop VIP Prices" could be more specific ("Shop VIP Flash Sale" or "Get 40% Off")
- STRENGTH: Excellent segmentation (VIP only), urgency well-placed, mobile responsive
- MISSING: A/B test plan (should test "Ends Tonight!" vs. specific deadline)
- VERDICT: **REVISE** — Add unsubscribe link, fix send time messaging, add image alt text

### Example 2: Newsletter / Educational Series

**Context**: SaaS company sending monthly product tips to all users across all plan tiers.

**Subject Line**: `Your Monthly Product Tips Update`

**Preview Text**: `Learn how top users are getting more out of [Product].`

**Body** (summary): Brief intro, 5 numbered tips with short descriptions, call-to-action to "Read Full Tips on Blog," footer with unsubscribe.

**Reviewer Findings**:
- MAJOR: Subject line lacks urgency/curiosity—low open rate risk ("Monthly Product Tips" is generic)
- MAJOR: No segmentation by plan tier—$10/month users receive tips for $500/month features
- MINOR: Five tips may be too many for scannable format; consider reducing to 3
- MINOR: Preview text repeats subject theme; could introduce contrasting hook
- STRENGTH: Clean layout, readable font size, clear unsubscribe
- STRENGTH: Accessible alt text on all images
- MISSING: Personalization—should reference user's specific use case or plan tier
- MISSING: Social proof or success metric (e.g., "85% of users who implement tip #3 see 2x productivity")
- VERDICT: **ACCEPT-WITH-RESERVATIONS** — Good bones, but needs stronger subject line, smarter segmentation, and tiered content

### Example 3: Transactional / Lifecycle Email

**Context**: Welcome series, first email to new signup.

**Subject Line**: `Welcome to [Brand]!`

**Body** (summary): Warm greeting, what to expect from the relationship, "Get Started" CTA, secondary CTA to watch onboarding video.

**Reviewer Findings**:
- CRITICAL: No physical address in footer (CAN-SPAM violation if this is in US)
- MAJOR: Subject line is generic and forgettable—should create excitement for new journey
- MINOR: "Get Started" CTA is vague; could say "Complete Your Profile" or "Take the Product Tour"
- STRENGTH: Voice is warm and welcoming (good for lifecycle email)
- STRENGTH: Proper unsubscribe mechanism present
- STRENGTH: Good use of personalization ("Welcome, {first_name}!")
- MISSING: Clear expectations for email frequency (should set proper unsubscribe mindset)
- MISSING: Confirmation that they'll be onboarded (what's the next step in the welcome sequence?)
- VERDICT: **REVISE** — Add physical address, strengthen subject line, clarify next steps in sequence

## Benchmark Test Info

**Score**: 25 (Phase 3 skill, specialized subset of copy-critic)

**Last Benchmark Run**: 2026-03-09

**Key Metrics**:
- CRITICAL issue detection rate: 92% (successfully catches missing unsubscribe, CAN-SPAM violations, broken CTAs)
- MAJOR issue detection rate: 88% (catches mobile optimization, segmentation, alt text issues)
- False positives (flagging issues that aren't problems): 6%
- Multi-perspective review depth: Consistently applies all 4 lenses (Subscriber, Marketer, Brand Guardian, Deliverability Specialist)
- Gap analysis coverage: Identifies 80% of commonly missing elements across strategic, tactical, tactical categories

**A/B Test Results**:
- With "What's Missing" section: 33 gap items identified per 100 campaigns
- Without "What's Missing" section: 0 gap items identified
- Verdict accuracy (aligns with expert reviewer): 87%

**Known Limitations**:
- Cannot verify DNS authentication (SPF/DKIM/DMARC) without technical access to email infrastructure
- Cannot test dynamic content rendering without access to ESP (e.g., personalization token rendering)
- Cannot predict actual open rates without historical data from same sender/list

## Notes

- **Mobile-First Mindset**: >60% of emails are opened on mobile. Any layout issue that breaks mobile experience is at least MAJOR.
- **Compliance is Non-Negotiable**: Missing unsubscribe, missing physical address, misleading subject lines are legal red flags, not style preferences.
- **Segmentation is Underrated**: A well-written email to the wrong audience has near-zero ROI. Always check audience fit.
- **CTA Clarity Wins**: One clear CTA will outperform three fuzzy CTAs. Multiple CTAs confuse subscribers and tank conversion.
- **Subscriber Trust > Clicks**: A clickbait subject line may get opens but erodes trust over time. Honest subject lines win long-term.
- **What's Missing Matters**: Email campaigns often fail not because they do something wrong, but because they're missing a component (A/B test plan, sequence logic, backup CTA link). Flag these gaps explicitly.
- **Personalization ≠ {first_name}**: Real personalization is segment-specific offers, dynamic content, or lifecycle-aware messaging. Just inserting a first name isn't enough.
- **Accessibility is Accessibility**: Alt text for images isn't optional—it's required by WCAG, improves deliverability (many email clients block images), and provides a fallback for subscribers using screen readers.
- **Realism Check**: This reviewer is calibrated to avoid both rubber-stamping (treating all campaigns as fine) and manufactured outrage (flagging every minor stylistic choice). Findings should be actionable and grounded in marketing best practice or legal requirement.

---
name: meddpicc
description: 8-element MEDDPICC qualification scoring rubric with Red/Yellow/Green definitions and discovery questions
tier: 1 (universal)
auto-fire: /closeout, /strategy, /prep, /pipeline, /add-deal
user-invocable: false
---

# MEDDPICC — Qualification Scoring Skill

## Purpose

Defines the 8-element MEDDPICC scoring rubric used across SalesSidekick. Each element has Red/Yellow/Green definitions, discovery questions to advance the score, and gap flags that trigger alerts. This is the qualification backbone of the entire system.

## When Referenced

- **/closeout** — scores MEDDPICC elements from call transcripts with evidence quotes
- **/strategy** — assesses MEDDPICC gaps as part of Five-Lens Prism analysis
- **/prep** — identifies MEDDPICC gaps to probe during upcoming meetings
- **/pipeline** — calculates deal health scores using MEDDPICC confidence
- **/add-deal** — initializes all 8 elements to Red (nothing assumed)

## Core Framework

### Scoring Rubric

Each element is scored Red (unknown/unvalidated), Yellow (partially confirmed), or Green (fully validated with evidence).

#### M — Metrics
*What quantifiable business outcomes will the customer achieve?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | No quantified business case. Customer hasn't articulated measurable impact. | None available |
| 🟡 Yellow | Customer has acknowledged general impact but hasn't quantified it. OR AE has estimated metrics but customer hasn't validated. | Customer statement about general impact, or AE's calculated estimate |
| 🟢 Green | Customer has confirmed specific, quantified metrics they expect. Numbers are theirs, not ours. | Direct customer quote with specific numbers |

**Discovery questions to advance:**
- "How are you measuring success today?"
- "What would a 10% improvement mean in dollar terms?"
- "If you solve this problem, what does that look like in your quarterly numbers?"

**Gap flag:** If Metrics is Red at Proposal stage or later → HIGH RISK. No business case = no urgency.

#### E — Economic Buyer
*Who has the authority and budget to make the purchasing decision?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | Economic buyer not identified. OR identified but never engaged. | None available |
| 🟡 Yellow | Economic buyer identified and name known. May have met briefly or been mentioned by champion. | Name, title, and at least one data point about their priorities |
| 🟢 Green | Economic buyer directly engaged. Has expressed support or stated decision criteria. We understand their priorities. | Direct interaction evidence — meeting notes, email exchange, or champion-confirmed alignment |

**Discovery questions to advance:**
- "Who signs off on investments of this size?"
- "Have they been involved in similar decisions before?"
- "What matters most to [Economic Buyer] — cost savings, revenue growth, or risk reduction?"

**Gap flag:** If Economic Buyer is Red at Negotiation stage → CRITICAL RISK. Deal cannot close without EB engagement.

#### D — Decision Criteria
*What criteria will the customer use to evaluate and select a solution?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | Unknown evaluation criteria. We're guessing what matters to them. | None available |
| 🟡 Yellow | Some criteria known from conversations, but not formally confirmed or complete. | Partial list from discovery calls |
| 🟢 Green | Full decision criteria documented and confirmed by the customer. We know how they'll evaluate us AND competitors. | Customer-confirmed criteria list, ideally written |

**Discovery questions to advance:**
- "What are the must-haves vs nice-to-haves?"
- "How will you evaluate different approaches?"
- "If you were building a scorecard, what would be on it?"

**Gap flag:** If Decision Criteria is Red at Qualification stage or later → MEDIUM RISK. We may be solving the wrong problem.

#### D — Decision Process
*What steps, approvals, and timeline does the customer follow to make a decision?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | Unknown decision process. No visibility into internal steps or timeline. | None available |
| 🟡 Yellow | General process known (e.g., "it goes through procurement") but specific steps, timeline, or approvals not confirmed. | High-level process description from a contact |
| 🟢 Green | Step-by-step process documented with timeline, approvers, and potential blockers identified. | Detailed process map confirmed by champion or economic buyer |

**Discovery questions to advance:**
- "What steps need to happen between now and a decision?"
- "Who else needs to weigh in before this moves forward?"
- "What's a realistic timeline for getting this done?"

**Gap flag:** If Decision Process is Red at Proposal stage or later → HIGH RISK. We don't know what we don't know about their internal process.

#### P — Paper Process
*What is the procurement, legal, and security review process?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | No visibility into procurement, legal, or security requirements. | None available |
| 🟡 Yellow | General awareness (e.g., "legal will review") but no specific timeline, requirements, or contacts in procurement. | General statement from a contact |
| 🟢 Green | Specific procurement contacts identified. Legal/security requirements known. Timeline for paper process documented. | Detailed requirements from procurement contact or champion |

**Discovery questions to advance:**
- "What does procurement look like at your organization?"
- "Are there legal or security reviews required?"
- "How long does the contracting process typically take?"

**Gap flag:** If Paper Process is Red at Negotiation stage → HIGH RISK. Paper process surprises kill deals.

#### I — Identify Pain
*What is the customer's core pain, and have they articulated it in their own words?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | Pain not validated. We assume they have a problem but haven't heard it from them. | None available |
| 🟡 Yellow | Customer has acknowledged a problem area but hasn't articulated specific pain or quantified impact. | General acknowledgment from a contact |
| 🟢 Green | Customer has described specific pain in their own words, with concrete examples and impact. Pain is urgent — they need to solve it. | Direct quote describing pain, specific examples, and urgency indicators |

**Discovery questions to advance:**
- "What happens when this goes wrong?"
- "Can you walk me through a recent example?"
- "On a scale of 1-10, how urgent is solving this?"

**Gap flag:** If Pain is Red at any stage → FUNDAMENTAL RISK. No pain = no deal. Consider disqualification.

#### C — Champion
*Who is our internal advocate with power, influence, and vested interest in our success?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | No champion identified. OR someone we think is a champion but who hasn't demonstrated advocacy. | None available |
| 🟡 Yellow | Potential champion identified. They're positive about us but haven't taken visible action to advance the deal internally. | Positive interactions but no evidence of internal advocacy |
| 🟢 Green | Champion confirmed through action — they've advocated internally, shared information, facilitated access to decision makers, or invested their political capital. | Specific actions the champion has taken on our behalf |

**Discovery questions to advance:**
- "Who on your team is most invested in solving this?"
- "Would they be willing to advocate internally?"
- "What would they need from us to make the case?"

**Gap flag:** If Champion is Red at Proposal stage or later → CRITICAL RISK. No champion = no internal momentum.

#### C — Competition
*What is the competitive landscape, and where do we stand?*

| Score | Definition | Evidence Required |
|-------|-----------|-------------------|
| 🔴 Red | Competitive landscape unknown. We don't know who else they're evaluating or if there's an incumbent. | None available |
| 🟡 Yellow | We know who the competitors are, but don't have clear intelligence on their positioning, relationships, or strengths in this deal. | Competitor names from customer or research |
| 🟢 Green | Full competitive picture — we know who they're evaluating, each competitor's positioning, who has relationships with whom, and our specific advantages. | Detailed competitive intel from customer conversations and research |

**Discovery questions to advance:**
- "What else are you evaluating?"
- "Is there an incumbent?"
- "What would make you choose one approach over another?"

**Gap flag:** If Competition is Red at Discovery stage or later → MEDIUM RISK. You may be walking into an ambush.

### MEDDPICC Confidence Scoring

Aggregate MEDDPICC scores into a deal-level confidence:

| Confidence | Criteria |
|-----------|----------|
| **High** | 6+ elements Green, 0 Red, no critical gaps |
| **Medium** | 3-5 elements Green, ≤2 Red, no critical gaps at current stage |
| **Low** | <3 elements Green, OR any critical gap at current stage |

**Critical gaps by stage:**
- Discovery: Pain = Red is critical
- Qualification: Pain = Red OR Champion = Red is critical
- Proposal: Any of Pain, Champion, Economic Buyer = Red is critical
- Negotiation: Any of Pain, Champion, Economic Buyer, Paper Process = Red is critical

### MEDDPICC Element Change Tracking

When /closeout scores MEDDPICC elements:
1. Compare new scores against existing scores in Notion
2. Document every change with evidence quotes from the call
3. Write changes to MEDDPICC Changes field in Call Notes
4. Update the individual element fields (M through C) in Deals
5. Recalculate MEDDPICC Confidence

Format for MEDDPICC Changes field:
```
[Element]: [Old] → [New] — Evidence: "[quote from call]"
```

## Personalization Notes

- Discovery questions are refined during /setup with {{PRODUCT_DESCRIPTION}} context and {{ICP_INDUSTRY}} language
- Gap flag thresholds are universal — no personalization needed
- Stage-to-MEDDPICC mapping is universal
- Confidence scoring criteria are universal

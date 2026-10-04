---
name: call-processing
description: 6-Output Framework for post-call processing including MEDDPICC scoring, task extraction, coaching, and risk signals
tier: 1 (universal)
auto-fire: /closeout
user-invocable: false
---

# Call Processing — 6-Output Framework Skill

## Purpose

Defines the 6-Output Framework used by /closeout to process call transcripts. Contains detailed formats for each output: MEDDPICC scoring, task extraction, coaching feedback, follow-up email, risk signals, and competitive intelligence. Also defines the 5 coaching dimensions and 6 risk signal categories.

## When Referenced

- **/closeout** — the primary consumer. Processes every call through this framework.
- **/coaching** — uses the 5 coaching dimensions for pattern analysis across calls

## Core Framework

### The 6-Output Framework

Every call processed by /closeout produces exactly 6 outputs. This is non-negotiable — every call gets the full framework, even if some outputs are thin.

#### Output 1: MEDDPICC Scoring

Score each MEDDPICC element based on what was said in the call. Reference the meddpicc/SKILL.md for scoring rubric.

**Format:**
```
MEDDPICC UPDATE:
| Element | Before | After | Evidence |
|---------|--------|-------|----------|
| M-Metrics | [R/Y/G] | [R/Y/G] | "[exact quote from call]" |
| E-Economic Buyer | [R/Y/G] | [R/Y/G] | "[exact quote]" or "No change — not discussed" |
| D-Decision Criteria | [R/Y/G] | [R/Y/G] | "[exact quote]" |
| D-Decision Process | [R/Y/G] | [R/Y/G] | "[exact quote]" |
| P-Paper Process | [R/Y/G] | [R/Y/G] | "[exact quote]" |
| I-Identify Pain | [R/Y/G] | [R/Y/G] | "[exact quote]" |
| C-Champion | [R/Y/G] | [R/Y/G] | "[exact quote]" |
| C-Competition | [R/Y/G] | [R/Y/G] | "[exact quote]" |

Net change: [X elements improved, Y unchanged, Z declined]
```

**Rules:**
- Only upgrade an element if there's a specific quote or evidence from the call
- If an element wasn't discussed, mark "No change — not discussed"
- Never upgrade an element based on inference — only on stated evidence
- If an element should downgrade (e.g., champion went quiet), flag it with the evidence

#### Output 2: Task Extraction

Extract every action item, commitment, and follow-up from the call.

**Format:**
```
TASKS EXTRACTED:
| Task | Owner | Priority | Due Date | Source |
|------|-------|----------|----------|--------|
| [Specific action] | AE/Prospect/Internal | H/M/L | [date] | Call |
| [Specific action] | AE/Prospect/Internal | H/M/L | [date] | Call |
```

**Rules:**
- **Owner categories:** AE (the user must do this), Prospect (the customer committed to this), Internal (someone else on user's team)
- **Priority:** High = blocks deal progress, Medium = important but not blocking, Low = nice-to-have
- **Due Date:** Extract from the call if mentioned ("by Friday," "next week"), otherwise default to 3 business days
- **Be specific.** Not "follow up" — instead "Send ROI calculator with Q3 case study data to Sarah by Thursday"
- Track both AE commitments AND prospect commitments — hold both sides accountable

#### Output 3: Coaching Feedback

Score the AE's performance on 5 dimensions. This is about improving the AE's craft, not judging them.

**The 5 Coaching Dimensions:**

| Dimension | What It Measures | 1 (Needs Work) | 3 (Solid) | 5 (Exceptional) |
|-----------|-----------------|----------------|-----------|------------------|
| **Discovery** | Quality of questions | Surface-level, yes/no questions only | Multi-layered questions that uncover needs | Expertly layered discovery revealing root pain and business impact |
| **Objection Handling** | Response to resistance | Avoids objections or caves immediately | Acknowledges and provides reasonable responses | Acknowledges, reframes brilliantly, advances the conversation |
| **Rapport** | Relationship building | Purely transactional, no personal connection | Professional with appropriate warmth | Genuine connection, active listening, builds real trust |
| **Next Steps** | Commitment clarity | Vague "let's follow up" or no next step | Clear next step with general timeline | Specific mutual commitments with dates, owners, and accountability |
| **Talk Ratio** | Listening balance | AE dominates (>70% talking) | Balanced (~50/50) | Prospect-led (AE <40%), AE asks and listens |

**Format:**
```
COACHING FEEDBACK:
| Dimension | Score | Observation |
|-----------|-------|-------------|
| Discovery | [1-5] | [Specific observation from this call] |
| Objection Handling | [1-5] | [Specific observation] |
| Rapport | [1-5] | [Specific observation] |
| Next Steps | [1-5] | [Specific observation] |
| Talk Ratio | [1-5] | [Estimated: AE ~X%, Prospect ~Y%] |

Overall: [X.X]/5
Top strength: [dimension] — [why]
Growth opportunity: [dimension] — [specific, actionable suggestion]
```

**Rules:**
- Be honest but constructive — this is coaching, not criticism
- Always identify at least one strength and one growth area
- Tie observations to specific moments in the call when possible
- The overall score is the average of all 5 dimensions

#### Output 4: Follow-Up Email

Draft a follow-up email based on the call conversation.

**Format:**
```
FOLLOW-UP EMAIL:

Tone options:
1. [Professional] — formal, appropriate for economic buyers
2. [Warm] — friendly, appropriate for champions
3. [Concise] — minimal, appropriate for technical evaluators

Selected: [default based on relationship/contact sentiment]

SUBJECT: [lowercase, specific to what was discussed]

BODY:
[Short follow-up. References specific things discussed.
Confirms commitments made on both sides.
One clear next step.]

[{{EMAIL_SIGN_OFF}}]
```

**Rules:**
- Apply brand-voice skill rules (vocabulary substitutions, banned phrases)
- Reference specific things from the call — not generic "great talking to you"
- Confirm commitments from BOTH sides (AE and prospect)
- One clear next step or CTA
- Under 200 words

#### Output 5: Risk Signals

Analyze the call for risk indicators across 6 categories.

**The 6 Risk Signal Categories:**

| Category | High Risk | Medium Risk | Low Risk |
|----------|-----------|-------------|----------|
| **Champion Health** | Champion went silent, deferred to others, showed uncertainty | Champion less enthusiastic than last call | Champion engaged and advocating |
| **Timeline Pressure** | Customer pushed timeline out, mentioned "no rush" | Timeline unchanged but no urgency signals | Customer expressed urgency, mentioned deadlines |
| **Competitive Threat** | Competitor mentioned favorably, prospect comparing features | Competitor mentioned but neutrally | No competitor mentions, or prospect dismissed competitor |
| **Budget Concerns** | Budget cut, freeze mentioned, "too expensive" | Budget questions without commitment | Budget confirmed, ROI discussion positive |
| **Stakeholder Shifts** | Key stakeholder left, reorg mentioned, new decision maker | Stakeholder roles unclear or changing | Stakeholders stable and engaged |
| **Engagement Quality** | Short answers, distracted, rescheduled multiple times | Adequate but not enthusiastic | Deep engagement, asking detailed questions, proactive follow-up |

**Format:**
```
RISK SIGNALS:
| Category | Level | Evidence |
|----------|-------|----------|
| Champion Health | [H/M/L] | [specific evidence from call] |
| Timeline Pressure | [H/M/L] | [specific evidence] |
| Competitive Threat | [H/M/L] | [specific evidence] |
| Budget Concerns | [H/M/L] | [specific evidence] |
| Stakeholder Shifts | [H/M/L] | [specific evidence] |
| Engagement Quality | [H/M/L] | [specific evidence] |

Overall Deal Risk: [High/Medium/Low]
[If High]: ⚠️ Recommend running /strategy [Company] for deeper analysis.
```

#### Output 6: Competitive Intelligence

Extract any competitive mentions or intelligence from the call.

**Format:**
```
COMPETITIVE INTEL:
- Competitor mentioned: [name] — Context: "[what was said]"
- Competitor positioning: [how they're being presented to the prospect]
- Our advantage: [where we're strong based on this conversation]
- Our vulnerability: [where they're strong or we're weak]
- Win probability: [0.0-1.0] — [brief rationale]

[If competitor identified]: 💡 Run /battle [Company] for full displacement analysis.
```

**Rules:**
- Only report competitor mentions that actually appeared in the call
- If no competitors mentioned, say "No competitive mentions in this call"
- Win probability is always a hypothesis — evidence-grade it
- Don't fabricate competitive intelligence from assumptions

### Notion Write Mapping

/closeout writes to 4 databases:

1. **Call Notes** — new record with all 10 fields
2. **Tasks** — new records for each extracted task
3. **Deals** — update MEDDPICC scores, MEDDPICC Confidence, Deal Risk, Last Activity
4. **Companies** — update Last Activity

## Personalization Notes

- Follow-up email applies brand-voice skill (Tier 3 — regenerated during /setup)
- Email sign-off uses {{EMAIL_SIGN_OFF}}
- Coaching dimensions are universal — scoring scales are not personalized
- Risk signal categories are universal — definitions are not personalized
- MEDDPICC scoring references meddpicc/SKILL.md (universal)

### First-Use Calibration Storage (/closeout)

On the first run of `/closeout`, the user is asked which call elements matter most to them. The 6-Output Framework structure is universal, but the **presentation order and emphasis** are personalized:

- **Output priority weighting:** [Populated on first /closeout run — ordered list of which outputs the AE values most, e.g., "MEDDPICC scoring > follow-up email > risk signals > tasks > coaching > competitive intel"]
- **Emphasis notes:** [Any specific preferences, e.g., "Always show risk signals first" or "I care most about the follow-up email"]

This does not change the framework itself — all 6 outputs are always generated. It changes which outputs are presented first and given the most detail.

---
name: posting-guide
description: LinkedIn content framework with 3-Type post structure, hook formulas, cadence goals, and 6-point pre-publish checklist
tier: 2 (template)
auto-fire: /draft-post
user-invocable: false
---

# Posting Guide — LinkedIn Content Framework Skill

## Purpose

Defines the 3-Type Framework for LinkedIn posts, structure templates for each type, hook formulas, frequency goals, and the 6-point pre-publish checklist. This skill ensures every LinkedIn post is structured for engagement and aligned with the AE's personal brand.

## When Referenced

- **/draft-post** — uses the 3-Type Framework, structure templates, and pre-publish checklist
- **/coaching** — could reference posting cadence for performance tracking (stretch)

## Core Framework

### 3-Type Framework

Every LinkedIn post falls into one of three types. Vary types throughout the week for maximum engagement.

#### Type 1: Personal
*Story → Lesson → Takeaway*

**Structure:**
1. **Hook** (2 lines): Open with a personal experience or moment. Create tension or curiosity.
2. **Story** (3-5 lines): Tell the story briefly. Be specific — names (when appropriate), numbers, emotions.
3. **Lesson** (2-3 lines): What you learned. Make it universally applicable.
4. **Takeaway** (1-2 lines): One actionable insight the reader can use today.
5. **CTA** (1 line): Question that invites engagement.

**Example hook formulas:**
- "I lost a $[X] deal because I [mistake]. Here's what I learned."
- "3 years ago, I almost quit sales. Then [event] changed everything."
- "The best advice I ever got in sales was wrong. Let me explain."
- "I said the wrong thing to a C-suite exec. What happened next surprised me."

**Best for:** Building authentic connection. Showing vulnerability. Making the AE relatable.

#### Type 2: Business
*Insight → Proof → Application*

**Structure:**
1. **Hook** (2 lines): Lead with a contrarian take, surprising stat, or bold claim.
2. **Insight** (3-5 lines): Explain the insight. Why does conventional wisdom get this wrong?
3. **Proof** (2-3 lines): Back it up with data, a case study, or a specific example.
4. **Application** (2-3 lines): How the reader can apply this to their work.
5. **CTA** (1 line): Ask for agreement, disagreement, or their experience.

**Example hook formulas:**
- "Stop [common practice]. It's killing your [metric]."
- "[X]% of [professionals] do this wrong. Here's the data."
- "The #1 reason [outcome] fails isn't what you think."
- "I analyzed [X] [things] and found one pattern that predicts [outcome]."

**Best for:** Establishing authority. Demonstrating expertise. Driving professional discussions.

#### Type 3: Educational
*Framework → Steps → Result*

**Structure:**
1. **Hook** (2 lines): Promise a specific, useful framework. Use numbers.
2. **Framework** (1-2 lines): Name the framework and give the overview.
3. **Steps** (5-8 lines): Numbered or bulleted steps. Each one specific and actionable.
4. **Result** (2 lines): What happens when you follow these steps.
5. **CTA** (1 line): Ask readers to save, share, or add their own steps.

**Example hook formulas:**
- "The [X]-step framework I use to [desirable outcome]:"
- "How to [action] in [timeframe] (save this):"
- "[X] questions that will change how you [activity]:"
- "My [X]-point checklist for [activity]. Took me [Y] years to figure out."

**Best for:** Providing actionable value. Getting saves and shares. Building a reputation as a teacher.

### Weekly Posting Cadence

**Target:** 4-5 posts per week

**Recommended mix:**
- 2× Personal (Monday, Thursday)
- 2× Business (Tuesday, Friday)
- 1× Educational (Wednesday)

**Timing:** Post when {{LINKEDIN_AUDIENCE}} is most active. Default recommendation: 7-9 AM local time, Tuesday-Thursday for maximum visibility.

### Hook Formulas (Universal)

Strong hooks share these characteristics:
1. **Scroll-stopping first line** — creates curiosity, tension, or surprise
2. **Specific, not vague** — numbers, names, concrete details
3. **Promise of value** — reader knows what they'll get
4. **Pattern interrupt** — breaks expectations

**Avoid:**
- Starting with "I'm excited to announce..."
- Starting with a question (unless it's genuinely provocative)
- Starting with a quote (save quotes for the body)
- Hashtag-first posts

### 6-Point Pre-Publish Checklist

Every post must pass all 6 checks before publishing:

| # | Check | Pass Criteria |
|---|-------|---------------|
| 1 | **Hook Test** | Would you stop scrolling? First 2 lines create curiosity or tension. |
| 2 | **Value Test** | Does the reader learn something, feel something, or gain a new perspective? |
| 3 | **Voice Test** | Does this sound like {{AE_NAME}}, not generic AI? Would they say this at a dinner party? |
| 4 | **Length Test** | 150-300 words for standard posts. Not too short (no substance) or too long (blog post). |
| 5 | **CTA Test** | Clear call-to-engagement: question, invitation, or challenge at the end. |
| 6 | **Brand Safety** | Nothing that could embarrass {{COMPANY}}, damage relationships, or violate confidentiality. No competitor bashing. No client name-dropping without permission. |

### Content Topics

Focus areas for {{AE_NAME}}'s LinkedIn content (customized during /setup):

**Topics:** {{LINKEDIN_TOPICS}}
**Target audience:** {{LINKEDIN_AUDIENCE}}

**Universal topics that work for any AE:**
- Sales methodology insights (discovery, qualification, negotiation)
- Deal stories (anonymized wins and losses)
- Industry observations and trends
- Personal growth and career development
- Team dynamics and leadership lessons
- Technology and tools in sales
- Customer success stories (with permission)

## Personalization Notes

- {{LINKEDIN_TOPICS}} and {{LINKEDIN_AUDIENCE}} are Tier 2 variables set during /setup
- The 3-Type Framework structure is universal (Tier 2 template)
- Hook formulas are universal
- Voice check (#3 in pre-publish) references brand-voice skill (Tier 3)
- Brand safety check (#6) uses {{COMPANY}} context
- Posting cadence timing may be adjusted based on {{LINKEDIN_AUDIENCE}} geography

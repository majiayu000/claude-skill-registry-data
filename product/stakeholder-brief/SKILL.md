---
name: stakeholder-brief
description: "Write exec-ready stakeholder updates, decision documents, and status reports. Adapts tone and detail level for different audiences (exec team, engineering, cross-functional). Structured for fast decision-making."
argument-hint: "[topic, decision needed, or status update context]"
---

# Stakeholder Brief Skill

Generate polished stakeholder communications — status updates, decision docs, and executive briefs.

## When to Use
- User needs to write a status update for leadership
- User needs a decision document for a cross-functional review
- User needs to communicate product changes to stakeholders
- User says `/stakeholder-brief` followed by the context
- Any exec communication that needs to be clear, concise, and actionable

## Document Types

### Type 1: Status Update
For regular cadence updates (weekly, monthly, quarterly).

**Structure:**
1. **TL;DR** (2-3 sentences): What happened, what's next, any blockers
2. **Key Metrics**: Table of 3-5 metrics with trend arrows (up/down/flat)
3. **Highlights**: Top 2-3 wins this period
4. **Lowlights**: Top 1-2 challenges or misses
5. **Next Period Focus**: What the team will prioritize
6. **Asks**: What you need from the audience (decisions, resources, alignment)

### Type 2: Decision Document
For getting alignment on a specific decision.

**Structure:**
1. **Decision Needed**: One sentence stating the decision clearly
2. **Deadline**: When this decision is needed by (and why)
3. **Context**: 2-3 paragraphs of background (assume the reader has limited context)
4. **Options** (3 max):
   | | Option A | Option B | Option C |
   |---|---|---|---|
   | Description | | | |
   | Pros | | | |
   | Cons | | | |
   | Effort | | | |
   | Risk | | | |
5. **Recommendation**: Which option and why (be opinionated)
6. **What Happens If We Don't Decide**: The cost of inaction
7. **Appendix**: Supporting data, research, or analysis

### Type 3: Executive Brief
For escalations, board updates, or senior leadership.

**Structure:**
1. **Bottom Line Up Front (BLUF)**: One sentence conclusion/ask
2. **Situation**: What's happening (facts only, 2-3 sentences)
3. **Complication**: Why this matters / what changed (2-3 sentences)
4. **Resolution**: What you propose (specific action items with owners and dates)
5. **Supporting Data**: Key numbers in a table or bullet list
6. **Risks**: What could go wrong with the proposed resolution

## Audience Adaptation

Adjust detail level and language based on audience:

**C-Suite / Board:**
- Maximum 1 page
- Focus on business impact and strategic implications
- Use revenue, user growth, competitive positioning language
- Include specific asks with dollar amounts or headcount

**VP / Director:**
- 1-2 pages
- Include metrics AND qualitative context
- Reference OKR/goal alignment
- Include timeline and dependencies

**Engineering / Cross-Functional:**
- Can be longer
- Include technical details where relevant
- Use specific feature/project names
- Include clear ownership and next steps

## Writing Principles
- **Lead with the ask**: Don't bury the lead. What do you need?
- **Be specific**: "Revenue up 12% QoQ" not "Revenue is trending well"
- **Show your work**: Link to data sources, include methodology
- **Anticipate questions**: Address the obvious follow-ups preemptively
- **Use formatting**: Tables, bold, bullet points — make it scannable
- **State confidence**: "We're 80% confident" is more useful than "We think"

## Output Format
Generate clean markdown optimized for pasting into email, Slack, Notion, or Google Docs. Use tables for comparisons. Bold key numbers. Keep paragraphs short (2-3 sentences max).

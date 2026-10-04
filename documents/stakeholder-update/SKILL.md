---
name: stakeholder-update
category: cadence
description: >
  Takes one set of project facts and generates three versions: technical for engineering,
  business-impact for leadership, and customer-facing for success teams. Use when the user
  says "stakeholder update", "write an update", "communicate this to different audiences",
  "translate for leadership", "customer-facing version", or needs to communicate the same
  information to different audiences.
---

# Stakeholder Update

One set of facts → three audience-specific versions.

## Workflow

1. **Gather the facts** — Accept raw project facts from the user. These can be:
   - A list of bullet points
   - A technical doc or PR description
   - A conversation summary
   - A vault note path

2. **Extract the core** — Identify:
   - What changed (the facts)
   - Why it matters (the impact)
   - What's next (the action items)
   - Any risks or blockers

3. **Generate three versions**:

### Version 1: Technical (Engineering)
- Lead with what changed technically
- Include relevant code/architecture details
- Reference PRs, commits, or technical docs
- Use precise technical language
- Focus on: implementation details, technical debt, performance metrics

### Version 2: Business Impact (Leadership)
- Lead with business outcome
- Translate technical changes to business metrics
- Include timeline and resource implications
- Use clear, jargon-free language
- Focus on: revenue impact, risk reduction, strategic alignment, timeline

### Version 3: Customer-Facing (Success Teams)
- Lead with user benefit
- Explain changes in terms of user experience
- Include any action items for customers
- Use friendly, accessible language
- Focus on: what's better for users, when they'll see it, what they need to do

## Output Format

```markdown
## Stakeholder Update: [Topic]

**Date**: [YYYY-MM-DD]
**Author**: [name]

---

### Technical Version (Engineering)

**TL;DR**: [one sentence]

[2-4 paragraphs with technical detail]

**Action items**:
- [ ] [engineering action]

---

### Business Version (Leadership)

**TL;DR**: [one sentence focused on business outcome]

[2-3 paragraphs, no jargon]

**Key metrics**:
- [metric]: [before] → [after]

**Action items**:
- [ ] [leadership action]

---

### Customer-Facing Version (Success Teams)

**TL;DR**: [one sentence focused on user benefit]

[2-3 paragraphs, friendly tone]

**Customer action required**: [yes/no + details]

**Talking points for support**:
1. [key point to communicate]
2. [key point to communicate]
```

## Behavior

- Never invent facts — only reframe what's provided
- If the input is too sparse for three versions, ask for more context
- Each version should stand alone — a reader shouldn't need the other versions
- Match the formality level to the audience
- Save to vault if requested: `vault/updates/stakeholder-[topic]-[YYYY-MM-DD].md`

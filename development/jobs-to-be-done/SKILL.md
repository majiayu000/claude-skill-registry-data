---
name: jobs-to-be-done
description: Help users define user needs with personas, a use case table (Outcome / How Today / Future / North Star), and open questions. Use when clarifying who a product serves and what outcomes they need.
---

# JTBD Personas & User Journeys

Help the user create a practical personas and user journeys document. The output is a shareable markdown page that gives any reader a clear picture of who uses the product, what outcomes they need, how they get those outcomes today, and where the product should go next.

## Reasoning Framework

Feature lists don't convey user intent. This skill produces a structured document that maps personas to outcomes, surfaces the current-state friction, and leaves space for the team to define the future and north star. It's designed to be a living artifact that drives roadmap conversations.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| JTBD document | Markdown | PM / design team / engineering leads |

## How to Help

When the user asks for personas and user journeys:

1. **Understand the product and scope** ; read available documentation, code, or ask the user to describe the system. Agree on scope boundaries upfront.
2. **Identify the personas** ; who are the distinct user types? What's their primary goal when they interact with the product?
3. **Build the use case persona table** ; map each persona to their outcomes, how they accomplish them today, and what the future could look like.
4. **Flag open questions** ; explicitly call out unknowns rather than guessing. Sparse "Future" and "North Star" columns are expected; that's what the team needs to define.

## Persona Format

Keep personas concise. A short paragraph describing the role, a scope note if needed, and their primary goal. No fictional names or demographic details.

```markdown
### 1. [Role Title]

[1-3 sentence description of who they are, what they do, and why they matter
in the context of this product. Combine similar roles into one persona when
their interaction with the product is the same.]

**Not in scope:** [Clarify who is excluded from this persona if the boundary
is ambiguous. Omit if obvious.]

**Primary goal(s) why they use [Product]:** [One sentence capturing their
core motivation]
```

### Rules for Good Personas

- **Role, not character** ; describe the role and responsibilities, not a fictional person. "Sarah, 34, loves hiking" adds nothing.
- **Combine when interactions are identical** ; if two roles touch the product the same way, merge them into one persona with a note explaining why.
- **Include scope boundaries** ; say who is NOT included when the persona name is broad (e.g., "Software Engineer" but not infra engineers).
- **Flag open questions** ; if you don't know how a persona interacts with the product today, say so explicitly with a blockquote callout.

## Use Case Persona Table

This is the core deliverable. One table that maps every persona to their outcomes, current workflow, and future vision.

```markdown
## Use Case Persona Table

| **Persona** | **Outcome / JTBD** | **How They Do It Today** | **Future** | **North Star** |
|---|---|---|---|---|
| **[Persona 1]** | [Outcome they need] | [Current workflow, tools, workarounds] | [Near-term improvement] | [Long-term vision] |
| | [Second outcome] | [Current workflow] | [Near-term improvement] | |
| **[Persona 2]** | [Outcome they need] | [Current workflow] | | |
```

### Rules for the Table

- **Outcome, not feature** ; write what the persona is trying to achieve, not what button they click. "Enable progressive feature rollout to ensure quality" not "Create a feature flag."
- **One outcome per row** ; a persona can have multiple rows for different outcomes.
- **Current state is specific** ; name the actual tools, processes, and workarounds. "Coordinate enablement via spreadsheets, Slack, and PMs" is good. "Uses existing tools" is not.
- **Future and North Star can be sparse** ; these columns are intentionally left for the team to define. Fill in what's known; leave blanks where the team needs to make decisions. That gap IS the value of the document.
- **North Star is aspirational** ; it describes the ideal end state, not the next sprint. It should feel ambitious but grounded.

## JTBD Statement Guidance

When writing the "Outcome / JTBD" column, follow this pattern:

```
[Verb] + [object] + [qualifying context]
```

Examples:
- "Enable progressive feature rollout to ensure quality"
- "Deploy code continuously without exposing unfinished features"
- "Get feedback and reduce cycle time on the feedback loop"
- "Access new features for competitive advantage while protecting live campaigns"

**What makes a good outcome statement:**
- **Situation-first** ; start with what the persona is trying to accomplish, not how the product implements it
- **Solution-agnostic** ; describe the desired outcome, not the product mechanics
- **One outcome per row** ; if you need "and" in the statement, split it into two rows

## Document Structure

```markdown
# [Product]: User Journeys and Personas

Scope: [What area of the product this covers]. This document captures who
uses [Product], what they're trying to accomplish, and how they do it today.
The "Future" and "North Star" columns are intentionally sparse; that's what
the team needs to define.

---

## Personas

### 1. [Role Title]
[Description paragraph]
**Primary goal(s) why they use [Product]:** [Goal]

### 2. [Role Title]
[Description paragraph]
**Primary goal(s) why they use [Product]:** [Goal]

...

---

## Use Case Persona Table

| **Persona** | **Outcome / JTBD** | **How They Do It Today** | **Future** | **North Star** |
|---|---|---|---|---|
| **[Persona]** | [Outcome] | [Current workflow] | [Near-term] | [Long-term] |
| | [Outcome 2] | [Current workflow] | | |
| **[Persona]** | [Outcome] | [Current workflow] | | |

---

## Open Questions

- [Explicit unknowns that need answers from the team]
- [Things you flagged during research that need validation]

---

## Sources

- [Where the information came from: interviews, docs, code, Slack, etc.]
```

## Questions to Ask Users

### To scope the document
- "What product or product area should this cover?"
- "Are there personas we should explicitly exclude?"

### To identify personas
- "Who are the primary users? Walk me through the different roles."
- "Do different people use different parts of the product?"
- "Who benefits from this product without ever logging in?"

### To map current state
- "Walk me through what happens when [persona] needs to [outcome]."
- "What tools, spreadsheets, Slack channels, or workarounds are involved?"
- "What's the most painful part of the current workflow?"

### To define future state
- "What should change in the next quarter? The next year?"
- "If you could wave a magic wand, what would the ideal experience look like?"
- "Are there outcomes that are completely unserved today?"

## Related Skills

- Problem Definition
- Conducting User Interviews
- Writing PRDs

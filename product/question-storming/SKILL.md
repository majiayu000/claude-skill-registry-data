---
name: question-storming
description: Help users run question-storming sessions to explore problem spaces. Use when someone needs to understand a new domain, kick off discovery for a feature or initiative, structure a dashboard around the right questions, or get a team aligned on what they don't know.
---

# Question-Storming

Help the user run a question-storming session that produces a prioritized, categorized list of questions about a problem space. This technique replaces premature solution-generating with disciplined question-generating, surfacing what a team does not know before deciding what to build.

## Origin and Purpose

Question-storming is like brainstorming, but instead of generating ideas to solve a specific problem, you generate questions about a problem space. The outcome is not answers or solutions -- it is a prioritized and categorized list of questions that need answers. The questions themselves become the roadmap for discovery, research, and decision-making.

This practice is especially valuable when:

- A person or team is new to a problem space and needs to ramp up quickly
- Seasoned people need a fresh perspective on a domain they know well
- A team is kicking off discovery for a new feature, initiative, or product area
- Someone needs to structure user engagement, data analysis, or brainstorming sessions
- A dashboard or analytics experience needs to be designed around the right questions

**Source:** [The Power of Question-Storming](https://medium.com/@jasmea/the-power-of-question-storming-7f2f19c4fceb) by Jason Means

## The Process

Every question-storming session follows four steps:

### Step 1 -- Identify the Topic

Define the problem space or topic clearly. The topic should be broad enough to generate a wide range of questions but specific enough that participants know what territory they are exploring.

**Key rules:**
- State the topic as a domain or problem space, not as a question itself
- Good: "Our checkout abandonment rate" / Bad: "Why are people abandoning checkout?"
- Identify a facilitator who will capture every question exactly as stated
- Invite a diverse audience -- different roles, tenure levels, and proximity to the problem generate richer questions
- People new to the domain are especially valuable because they ask questions that insiders have stopped asking

### Step 2 -- Generate Questions

Have participants start asking questions. The facilitator writes each question down one-by-one. Do not start a new question until the previous one has been fully recorded.

**Key rules:**
- Only questions are allowed. No answers, suggestions, recommendations, or commentary
- Questions must be directly or indirectly related to the problem space
- Questions must be recorded in a non-judgmental manner. No reactions, evaluations, or editorializing -- only further questions
- Go for volume. Quantity over quality at this stage. Weak questions often spark strong follow-up questions
- If someone starts answering or suggesting, redirect them: "Can you turn that into a question?"
- If energy stalls, prompt with: "What else do we not know?" or "What would a customer ask about this?"

### Step 3 -- Categorize Questions

After generation is complete, group questions into four categories by type. These categories reveal the shape of what the team does not know:

- **"What is?"** -- Questions about facts and the as-is situation. These establish the current state and baseline understanding.
  - Example: "What is our current checkout abandonment rate?"
  - Example: "What data do we currently collect on user drop-off points?"

- **"What caused?"** -- Questions that get at the root of a problem. These seek to understand causation and contributing factors.
  - Example: "What caused the spike in abandonment last quarter?"
  - Example: "What changed in the flow that might have introduced friction?"

- **"Why? Why Not?"** -- Questions about the rationale behind a problem space. These challenge assumptions and explore reasoning.
  - Example: "Why do we require account creation before checkout?"
  - Example: "Why haven't we tested a guest checkout option?"

- **"What if?"** -- Questions that point to a different future and lead to innovation. These open up possibility space.
  - Example: "What if we let users save their cart and return later?"
  - Example: "What if checkout was a single page instead of four steps?"

**Key rules:**
- Some questions may fit multiple categories. Pick the best fit and move on -- do not debate categorization at length
- The distribution of categories is informative. If most questions are "What is?" the team may need more foundational research. If most are "What if?" the team may be ready to ideate but needs grounding first
- Flag any categories with very few questions -- this may indicate a blind spot

### Step 4 -- Prioritize

Review the full categorized list and identify the most critical and urgent questions to answer first.

**Key rules:**
- Prioritize by impact: which questions, if answered, would most change what you build or how you build it?
- Prioritize by urgency: which questions block other work or decisions?
- Prioritize by dependency: which questions must be answered before other questions can even be asked?
- Assign owners and methods for answering the top questions (user research, data analysis, stakeholder interview, competitive review, etc.)
- Not every question needs to be answered. Some questions are valuable simply because they were surfaced -- they change how the team thinks about the space

## The Three Rules

These rules are non-negotiable during the question generation phase:

1. **Only questions are allowed** -- No answers, suggestions, or recommendations. If someone offers a solution, ask them to reframe it as a question.
2. **Questions must be related to the problem** -- Every question must be directly or indirectly connected to the stated topic. Tangential questions are fine if they illuminate the problem space from a new angle.
3. **Record without judgment** -- No reactions, no evaluations, no "good question" or "we already know that." Every question goes on the list. Go for volume.

## Practical Application: Dashboards

One of the most powerful applications of question-storming is designing data analytics dashboards. Instead of starting with available data or chart types, start by generating the questions the dashboard should answer.

**Process:**
1. Question-storm the domain the dashboard serves
2. Prioritize the questions stakeholders most need answered
3. For each question, determine what data would answer it
4. Design each visualization so the question is stated above the graph and the data answers it

**Why this works:**
- Every chart has a clear purpose tied to a real question
- Stakeholders can evaluate the dashboard by asking: "Does this answer my questions?"
- It prevents "data dumps" -- dashboards full of charts that no one uses because they do not answer questions anyone is actually asking
- New team members can read the questions to understand what the dashboard is for

## How to Help Users

When the user asks for help with question-storming:

1. **Clarify the topic** -- What problem space or domain are they exploring? Help them frame it as a topic, not a question
2. **Understand the context** -- Are they new to this domain? Kicking off a project? Designing a dashboard? Preparing for user research? The context shapes how you facilitate
3. **Set the rules** -- Remind them of the three rules before generating. If working asynchronously, state the rules at the top of the output
4. **Generate questions** -- Help them brainstorm questions. Offer questions from different angles and categories to stimulate thinking. If they give answers or suggestions, redirect: "Can you turn that into a question?"
5. **Categorize** -- Sort all questions into the four categories. Note the distribution and flag any gaps
6. **Prioritize** -- Help them identify the top questions by impact, urgency, and dependency. Suggest owners and methods for answering
7. **Format the output** -- Deliver a clean, structured document they can share with their team

## Questions to Help Users Get Started

- "What problem space or topic do you want to explore?"
- "Who would you normally invite to this session? What perspectives are missing?"
- "Are you exploring this because you are new to the domain, or because the team needs a fresh look?"
- "What decisions are you trying to make that these questions should inform?"
- "Is there a specific deliverable this feeds into -- a PRD, a dashboard, a research plan?"
- "What do you think you already know about this space? (We can question those assumptions too.)"

## Example Output Format

When delivering question-storming results, use this structure:

```markdown
# Question-Storming: [Topic]

**Date:** [Date]
**Participants:** [Names/Roles]
**Facilitator:** [Name]

## Topic Statement
[One to two sentence description of the problem space being explored]

---

## Questions

### "What is?" -- Facts and Current State
1. [Question]
2. [Question]
3. [Question]

### "What caused?" -- Root Causes and Contributing Factors
1. [Question]
2. [Question]
3. [Question]

### "Why? Why Not?" -- Rationale and Assumptions
1. [Question]
2. [Question]
3. [Question]

### "What if?" -- Possibilities and Innovation
1. [Question]
2. [Question]
3. [Question]

---

## Category Distribution
- "What is?": [count] questions
- "What caused?": [count] questions
- "Why? Why Not?": [count] questions
- "What if?": [count] questions
- **Total:** [count] questions

**Observation:** [Note on what the distribution reveals -- e.g., heavy on "What is?" suggests the team needs foundational research before ideating]

---

## Priority Questions

| # | Question | Category | Why It Matters | Suggested Method | Owner |
|---|----------|----------|----------------|-----------------|-------|
| 1 | [Question] | [Category] | [Impact statement] | [Research/Data/Interview/etc.] | [TBD] |
| 2 | [Question] | [Category] | [Impact statement] | [Research/Data/Interview/etc.] | [TBD] |
| 3 | [Question] | [Category] | [Impact statement] | [Research/Data/Interview/etc.] | [TBD] |

---

## Next Steps
- [ ] [Action item for answering priority question 1]
- [ ] [Action item for answering priority question 2]
- [ ] [Action item for answering priority question 3]
```

## Common Mistakes to Flag

- **Generating answers instead of questions** -- The most common failure mode. If the user starts providing solutions, observations, or recommendations, redirect them to reframe as a question. "We should add guest checkout" becomes "What if we offered guest checkout?"
- **Questions too narrow too early** -- If every question is about a specific feature or implementation detail, zoom out. The value of question-storming is exploring the problem space broadly before narrowing
- **Skipping categorization** -- Without categorization, the list is just a wall of text. The categories reveal the shape of what you do not know and where to focus
- **Prioritizing everything** -- If more than five to seven questions are marked as top priority, nothing is prioritized. Force-rank ruthlessly
- **Not assigning owners or methods** -- Prioritized questions without a plan to answer them are just a wish list. Every top question needs an owner and a method
- **Judging questions during generation** -- Any reaction ("that's obvious," "we already tried that," "good one") breaks the non-judgmental environment and shuts down the quieter participants who often ask the best questions
- **Homogeneous participants** -- If everyone in the session has the same role and tenure, the questions will cluster in familiar territory. Diverse perspectives generate diverse questions
- **Using this when you need a decision** -- Question-storming is for exploration, not for making a choice between known options. If the user needs a decision, use the decision-brief skill instead

## When to Combine with Other Techniques

- **Before a PRD:** Question-storm the problem space, then use the answers to inform the PRD
- **Before user interviews:** Question-storm to generate an interview guide. The "What is?" and "What caused?" questions become great interview prompts
- **Before building dashboards:** Question-storm to identify what the dashboard should answer, then design visualizations around the priority questions
- **During discovery:** Use question-storming to structure the first week of exploring a new initiative
- **After a post-mortem:** Question-storm what the team still does not understand about an incident, beyond what the post-mortem already surfaced

## Related Skills

- Decision Brief (SOCRR Framework)
- Jobs to Be Done
- User Interview Design
- Prioritize Features
- Validate Hypothesis

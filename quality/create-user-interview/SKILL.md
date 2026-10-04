---
name: create-user-interview
description: Invoke when planning a user interview; produces a best-practice template (Open, Usability, or Mixture) with Mom Test-aligned questions.
---

# User Interview Template Generator

Create a minimalist, best-practice interview template that a PM can print or open on their laptop during a live user interview. The output is a single markdown file saved to `outputs/interview-templates/`.

## Reasoning Framework

This skill exists because interview quality depends on question quality. It applies PM best practices (The Mom Test, non-leading questions, past-focus) to generate templates that surface real user behavior, not aspirational answers.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Interview template | Markdown (goals, warm-up, core questions, wrap-up, notes section) | Interviewer / PM |

## How to Help

When the user invokes this skill, gather the required inputs, validate the questions against PM best practices, then generate and save the template.

## Required Inputs

Collect all 6 inputs before generating the template. Ask for any that are missing.

| # | Input | Description |
|---|-------|-------------|
| 1 | **Product** | What product or feature area is this interview about? |
| 2 | **Interview Goals** | What do you want to learn? What decisions will this inform? |
| 3 | **Top Questions** | The 1-2 most important questions to ask (or tasks for usability studies) |
| 4 | **Magic Wand Question** | Include a "magic wand" question at the end? (Yes / No) |
| 5 | **Target Personas** | Who are you interviewing? (role, seniority, domain) |
| 6 | **Interview Type** | Open interview, usability study, or a mixture of both? |

## Question Quality Review (MANDATORY)

Before adding any user-provided questions to the template, review them against these 8 criteria. If a question fails any check, rewrite it and explain the change to the user.

### 1. Leading Questions
Flag any question that suggests a desired answer or pushes the respondent in a particular direction.

**Bad:** "Don't you think the new dashboard is easier to use?"
**Rewritten:** "Walk me through how you used the dashboard last time."

### 2. The Mom Test
Identify questions that wouldn't pass "The Mom Test" -- questions people would lie about to be polite, hypothetical futures, or opinion-based rather than fact-based.

**Bad:** "Would you use this feature?"
**Rewritten:** "Tell me about the last time you ran into this problem. What did you do?"

### 3. Past vs. Future Focus
Rephrase questions about hypotheticals or future intentions to focus on past behaviors and actual experiences.

**Bad:** "How would you handle this situation?"
**Rewritten:** "Tell me about the last time you..."

### 4. Open-Endedness
Check that questions allow for genuine exploration and are not too narrow or closed.

**Bad:** "Is the onboarding process good?"
**Rewritten:** "Walk me through your experience getting started with the product."

### 5. Chronological Story Extraction
Assess whether questions help "excavate the story" with temporal prompts like "What happened first?" and "What happened next?"

### 6. Visual/Prototype Integration
If the interview type includes usability, note where visual elements, prototypes, or demonstrations should be incorporated. Add placeholder markers in the template.

### 7. Probing Space
Ensure there is enough flexibility and time for follow-up questions and deeper exploration. Do not overload the template with too many questions.

### 8. Question Prioritization
Identify which questions are most critical vs. nice-to-have, given typical interview time constraints (30-45 minutes). Mark nice-to-have questions as optional.

## Template Structure

The generated template must follow this exact structure:

```markdown
# User Interview: [Product Name]

**Date:** _______________
**Interviewer:** _______________

---

## Participant Info

| Field | Details |
|-------|---------|
| **Name** | |
| **Company / Team** | |
| **Tenure** | |
| **Seniority Level** | |
| **Role** | |

---

## Interview Goals

> [Brief summary of what we want to learn from this interview]

---

## Warm-Up (2-3 min)

> Start conversational. Build rapport. Do NOT lead with product questions.

- "Thanks for taking the time to chat. Before we dive in, how are things going for you lately?"
- "How has your week been?"

*Listen actively. Let them settle in. This is not a throwaway -- genuine interest
builds trust and surfaces context you wouldn't get from jumping straight to questions.*

---

## General Feedback (5 min)

> One open-ended question to capture unprompted feedback before introducing any specific topics.

- "[Open-ended question tailored to the product -- e.g., 'Tell me about your experience with [product] recently. What stands out?']"

**Probing prompts:**
- "What happened first?"
- "What happened next?"
- "How did that make you feel?"
- "What did you end up doing about it?"

---

## Core Questions (15-20 min)

> [1-2 questions or usability tasks -- the heart of the interview]

### Question 1

[The question or task, rewritten to pass all quality checks]

**Follow-up probes:**
- [Contextual follow-up 1]
- [Contextual follow-up 2]
- "Can you tell me more about that?"

[If usability study: ### Task 1 -- include task description, success criteria,
and "[SHOW PROTOTYPE / SCREEN]" placeholder]

### Question 2 (if provided)

[The question or task, rewritten to pass all quality checks]

**Follow-up probes:**
- [Contextual follow-up 1]
- [Contextual follow-up 2]

---

## Magic Wand (3 min) -- [INCLUDE ONLY IF REQUESTED]

> "If you had a magic wand and could change one thing about [product/workflow],
> what would it be and why?"

**Probing prompts:**
- "What would that look like day-to-day?"
- "How would you know it was working?"

---

## Wrap-Up (2 min)

- "Is there anything else you wanted to share that we didn't cover?"
- "Anyone else on your team you think I should talk to?"

---

## Post-Interview Notes

| Field | Notes |
|-------|-------|
| **Key Themes** | |
| **Surprises** | |
| **Quotes Worth Saving** | |
| **Champion Candidate** | Yes / No |
| **Follow-Up Needed** | |
```

### Template Rules

- **Minimalist.** The template should fit on 1-2 printed pages. No walls of text.
- **Conversational.** Questions should read like something a human would actually say out loud.
- **Non-leading.** Every question must pass the quality review checks above.
- **Past-focused.** Default to asking about real past experiences, not hypothetical futures.
- **Space for probing.** Leave room between sections -- the best insights come from follow-ups, not scripted questions.
- **Champion identification.** Always include "Champion Candidate: Yes / No" in post-interview notes. Champions are users who show deep engagement, thoughtful feedback, and willingness to partner on product development.

### Interview Type Adjustments

**Open Interview:**
- Core section uses open-ended questions
- No task-based elements
- Maximize probing space

**Usability Study:**
- Core section uses task-based format with clear task descriptions
- Include `[SHOW PROTOTYPE / SCREEN]` placeholders
- Add success criteria for each task
- Include think-aloud instructions: "Please think out loud as you go through this -- tell me what you're looking at, what you're thinking, what you expect to happen."

**Mixture:**
- Start with 1 open-ended question in the Core section
- Follow with 1 usability task
- Include both probing prompts and think-aloud instructions

## Output

1. Generate the filled-in template following the structure above
2. Save the file to `outputs/interview-templates/interview-template-[product-name-slug]-[YYYY-MM-DD].md` from the repo root (creates the subfolder if missing)
3. Show the user the completed template and explain any question rewrites made during the quality review

Do not save generated templates to `~/Desktop/`. Keep generated artifacts under `outputs/` so they are easy to find and can be ignored or committed intentionally.

## Common Mistakes to Flag

- **Too many questions.** If the user provides more than 2 core questions, push back. The best interviews go deep on 1-2 topics, not wide on 5.
- **Leading questions that feel neutral.** "How easy was it to..." presupposes ease. Rewrite as "Walk me through how you..."
- **Skipping warm-up.** Never cut the warm-up. It builds trust and surfaces context.
- **No probing prompts.** Scripted questions without follow-up probes produce shallow interviews. Always include probes.
- **Asking "would you use this?"** Classic Mom Test failure. Rewrite to focus on past behavior.
- **Forgetting to identify champions.** Every interview is a chance to find design partners. Always assess.

## Related Skills

- `/jobs-to-be-done` -- Create personas and use cases from interview findings
- `/storytelling-for-impact` -- Turn interview insights into compelling stakeholder narratives
- `/create-prd-engineering` -- Feed interview learnings into product requirements

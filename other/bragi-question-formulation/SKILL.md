---
name: bragi-question-formulation
description: Advise on how to ask clear, targeted questions that gather requirements and clarify ambiguity efficiently.
---

# Question Formulation

## Purpose

Advise on how to frame questions to extract maximum signal from user interactions. Good questions reduce back-and-forth, surface hidden assumptions, and clarify requirements quickly.

## When to Use

- Before asking the user for clarification.
- When requirements are ambiguous or incomplete.
- When multiple interpretations of a request are possible.
- When the user's request is very broad or open-ended.

## Workflow

1. **Identify what is unknown.**
   - What specific information is missing?
   - What decisions depend on this information?
   - What would happen if we guessed instead of asking?

2. **Determine the question type.**
   - **Closed question** (yes/no, pick from options) — use when you need a specific, bounded answer. Best for confirmations and constrained choices.
   - **Open question** (what, how, why) — use when exploring unknown territory or when the user's priorities are unclear.
   - **Scoping question** (narrowing the problem space) — use when the request is too broad to act on.
   - **Hypothetical question** ("what if X?") — use to test assumptions without committing to a path.

3. **Structure the question.**
   - State what you already understand (context).
   - State what is unclear (the gap).
   - Ask the specific question.
   - Optionally, provide example answers or options to guide the response.

4. **Sequence questions wisely.**
   - Start broad, then drill down.
   - Ask one question at a time (or group related questions clearly).
   - Prioritize: ask the question that most reduces uncertainty first.

5. **Review the question.**
   - Is it leading? (Avoid suggesting the answer you want.)
   - Is it loaded? (Avoid assumptions baked into the question.)
   - Can it be answered with the user's current knowledge?
   - Is it scoped enough to produce a useful answer?

## Quality Criteria

- Open-ended questions are preferred; yes/no questions are used only when a bounded confirmation is specifically needed.
- The user has enough context to answer without asking clarifying questions back.
- The question reveals the missing information needed to proceed.
- Multiple questions are grouped logically (numbered or categorized).

## Anti-Patterns

- **Compound question**: Asking two things at once — "Do you want X or Y, and when should it be done?"
- **Leading question**: "Don't you think we should use X?" (biases the answer).
- **Assumption-laden question**: "How should we handle the database migration?" (assumes migration is needed).
- **Open-ended without guidance**: "What do you want?" (too broad to be useful).

---
name: lowkey-effort
description: >
  Automatically calibrate response effort and token usage to match task complexity. Use this skill at the START of every response to classify the incoming task and select the appropriate effort tier before generating any output. Trigger whenever you're about to answer a question or complete a task — this skill saves tokens on simple queries and reserves depth for complex ones. Especially useful for: quick factual questions, long technical tasks, coding problems, multi-step reasoning, creative writing, research, explanations, and analysis. If you're not sure how much effort a task needs, consult this skill.
---

# Adaptive Effort

Calibrate response length, reasoning depth, and token usage to match the actual complexity of each task. Run this classification **before** generating your response — then apply the rules for the matched tier.

---

## Step 1: Classify the Task

Read the user's request and assign it to one of four tiers:

### Tier 1 — Instant (< 50 tokens response target)

Simple, closed, factual queries with a single correct answer.

- "What's the capital of France?"
- "What does `===` mean in JS?"
- "Convert 5km to miles"
- "Is Python case-sensitive?"
- Greetings, yes/no questions, date/time lookups

### Tier 2 — Light (50–250 tokens response target)

Queries needing a short explanation, a small code snippet, or a quick how-to. One concept, one answer.

- "How do I center a div in CSS?"
- "What's the difference between `let` and `const`?"
- "Give me a regex for email validation"
- "Explain what a webhook is"
- Short rewrites, grammar fixes, brief summaries

### Tier 3 — Standard (250–700 tokens response target)

Multi-part questions, moderate coding tasks, explanations with examples, analysis of a provided artifact.

- "Build me a React component for a todo list"
- "Explain how JWT authentication works"
- "Review this function and suggest improvements"
- "Write a cover letter for this job posting"
- Comparisons, step-by-step guides, moderate debugging

### Tier 4 — Deep (700–2000 tokens response target)

Complex, open-ended, or multi-domain tasks requiring extensive reasoning, architecture, or long-form output.

- "Design a scalable backend for a SaaS product"
- "Write a full blog post on X"
- "Debug this 200-line function with subtle logic errors"
- "Compare three architectural patterns and recommend one"
- Research synthesis, system design, PRDs, complex refactors

---

## Step 2: Apply Tier Rules

### Tier 1 — Instant

- **Format**: 1–2 sentences, plain prose. No headers, no bullets.
- **Reasoning**: None. State the answer directly.
- **Code**: Only if the question IS about a code token/symbol; 1 line max.
- **Caveats**: Only if critically necessary (e.g., answer varies by context).

### Tier 2 — Light

- **Format**: Short prose or a single small code block. Avoid headers.
- **Reasoning**: 1 sentence of context if it aids clarity.
- **Code**: Up to ~15 lines if the task is code-centric.
- **Caveats**: Skip "there are many ways to do this" hedges.

### Tier 3 — Standard

- **Format**: Prose with optional headers for multi-part answers. Code blocks as needed.
- **Reasoning**: Explain _why_, not just _what_, for non-obvious choices.
- **Code**: Full working snippet with comments on non-obvious parts.
- **Caveats**: Note important edge cases, but don't enumerate every possibility.

### Tier 4 — Deep

- **Format**: Full structure — headers, sections, code blocks, examples.
- **Reasoning**: Thorough. Justify trade-offs, alternatives considered.
- **Code**: Complete, production-quality, with error handling.
- **Caveats**: Surface important limitations, risks, or follow-up considerations.

---

## Step 3: Override Signals

Upgrade or downgrade the tier if these signals are present:

**Upgrade one tier if:**

- User says "in detail", "thoroughly", "comprehensive", "production-ready"
- Task involves security, money, health, or legal topics (accuracy cost is high)
- User's follow-up suggests the previous answer was too shallow

**Downgrade one tier if:**

- User says "quick", "briefly", "just", "short", "tldr", "one-liner"
- User is clearly an expert asking a narrow question (no need to explain basics)
- It's a conversational message embedded in a longer session

**Never downgrade below Tier 2 for:**

- Code that will run in production
- Answers where a wrong/incomplete response could cause harm

---

## Execution

1. Silently classify → assign tier (do NOT announce the tier to the user unless they ask)
2. Apply format and depth rules for that tier
3. Stop when the task is complete — do not pad, summarize, or add closing remarks
4. If genuinely uncertain between two tiers, pick the **lower** one and let the user ask for more

The goal is: right-size every response. Neither wasteful nor stingy.

---
name: engineer-prompts-for-instant
description: >-
  Write or fix a prompt for a fast/cheap model (Gemini Flash, GPT-4o Mini,
  Haiku) so its output is stable and parseable. Use for any request to draft,
  tune or debug such a prompt. Not for reasoning models (use
  engineer-prompts-for-reasoning).
---

# HOW TO WRITE PROMPTS FOR INSTANT MODELS

This guide helps you get stable, accurate results from high-speed models (like
Gemini Flash, GPT-4o Mini, Claude Haiku). These models are fast and
cost-effective but need **clear instructions** and **examples** to work best.

## 1. THE GOLDEN RULE: "SHOW, DON'T JUST TELL"

Instant models are like fast learners who prefer copying a pattern over reading
a textbook. The most effective way to improve their performance is to provide
**examples**.

- **Don't just say:** "Extract the dates."
- **Say:** "Extract dates in YYYY-MM-DD format. Example: 'March 5th' ->
  '2025-03-05'."

## 2. THE 4-PART FORMULA (BEGINNER TEMPLATE)

Use this structure for 90% of your tasks. It is designed to be copy-paste
friendly.

```markdown
# 1. ROLE (Who matches the task?)

You are an expert [Role Name, e.g., Data Analyst, Copy Editor].

# 2. TASK (What to do?)

[Action Verb] the [Input Data] to produce [Result].

- Be direct. Use commands like "Extract", "Summarize", "Translate".

# 3. RULES & FORMAT (How to do it?)

- Output format: [JSON, Markdown Table, Plain Text, etc.]
- Constraint 1: [e.g., Do not include markdown code blocks]
- Constraint 2: [e.g., If data is missing, write "N/A"]

# 4. FEW-SHOT EXAMPLES (CRITICAL FOR STABILITY)

Input: [Short Example Input] Output: [Perfect Example Output]

Input: [Short Example Input 2] Output: [Perfect Example Output 2]

# ACTUAL INPUT

[Paste your real data here]
```

## 3. KEY TECHNIQUES FOR BEGINNERS

### A. Few-Shot Prompting (The "Examples" Section)

Always give at least **one** example (1-shot), ideally **three** (3-shot). This
fixes formatting errors better than any written instruction.

### B. Chain-of-Thought Lite (Thinking Tags)

Even fast models can make mistakes on math or logic. Ask them to "think" before
answering.

- **Instruction:** "Think step-by-step in `<thinking>` tags before outputting
  the JSON."
- **Why:** This gives the model "space" to calculate before committing to an
  answer.

### C. Negative Constraints

Tell the model what **NOT** to do.

- "Do not add introductory text."
- "Do not explain your reasoning, just give the code."

## 4. TROUBLESHOOTING COMMON ISSUES

| Problem                        | Solution                                                                          |
| :----------------------------- | :-------------------------------------------------------------------------------- |
| **Model ignores format**       | Move the "Output Format" section to the very bottom, right before the Input.      |
| **Model hallucinates details** | Add a rule: "If the answer is not in the text, state 'Unknown'."                  |
| **Response is too chatty**     | Add: "Return ONLY the result. No conversational filler."                          |
| **Logic is flawed**            | Ask the model to output a `<thinking>Step 1... Step 2...</thinking>` block first. |

## 5. EXAMPLE: TEXT EXTRACTION

**Task:** Extract meeting items from a rough email.

```markdown
# ROLE

You are a personal assistant.

# TASK

Extract action items from the email.

# RULES

- Output a JSON list of strings.
- Only include tasks with a deadline.

# EXAMPLES

Input: "Hi, can you buy milk by 5pm? Also, the weather is nice." Output: ["Buy
milk (Deadline: 5pm)"]

Input: "Just checking in. Please submit the report tomorrow." Output: ["Submit
report (Deadline: Tomorrow)"]

# INPUT

[User's Email]
```

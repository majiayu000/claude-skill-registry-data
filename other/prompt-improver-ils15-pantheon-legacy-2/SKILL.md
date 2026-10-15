---
name: prompt-improver
description: "Improve prompts using best practices for clarity, specificity, and structure. Use for optimizing AI agent and bot instructions."
context: fork
globs: []
alwaysApply: false
---

# Prompt Improver

Improve prompts using best practices for clarity, specificity, and structure. Includes simplification patterns for reducing token waste.

---

## Core Principles

1. **Be specific** — vague prompts get vague answers
2. **Provide context** — include relevant constraints and examples
3. **Define output format** — tell the model how to respond
4. **Use structure** — headings, lists, code blocks
5. **Set constraints** — what NOT to do is as important as what TO do

---

## Improvement Patterns

### Before → After

**Vague:**
```
Make this code better
```

**Specific:**
```
Refactor this function to:
1. Use async/await for all I/O
2. Add type hints to parameters and return
3. Extract the validation logic into a separate function
4. Keep the same behavior (tests must pass)
```

**Wordy:**
```
I need you to please help me understand what this code does because I'm not sure and it's kind of confusing and there are a lot of parts and I don't know where to start looking at it
```

**Concise:**
```
Explain what this code does. Summarize in 3 bullet points.
```

---

## Prompt Structure Template

```markdown
# Context
[What is the background? What problem are we solving?]

# Task
[What exactly should be done? Be specific.]

# Constraints
- [Constraint 1: e.g., "Use only existing libraries"]
- [Constraint 2: e.g., "Do not change the API"]

# Output Format
[How should the response be structured?]

# Examples (optional)
[Show expected input/output if helpful]
```

---

## Simplification Rules

- Remove filler words: "please", "I think", "maybe", "kind of"
- Use active voice: "Write tests" not "Could you write some tests?"
- One task per prompt (or numbered list for multiple)
- Use code blocks for code references
- Set explicit limits: "Max 3 suggestions", "Under 100 words"

---

## Anti-Patterns

- ❌ "Do your best" — model doesn't know what "best" means
- ❌ Multiple conflicting instructions in one prompt
- ❌ No output format specified
- ❌ Assuming model knows project context
- ❌ Overly long prompts with irrelevant details

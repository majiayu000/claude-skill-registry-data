---
name: skill-powerups
description: >
  Interactive tutorial-style lessons for custom skills. Invoke /powerup <skill>
  for a guided walkthrough with examples, exercises, and knowledge checks.
  Trigger: When user says "powerup", "tutorial", "teach me", or wants to learn a skill interactively.
license: MIT
metadata:
  author: JNZader
  version: "1.0"
  tags: [teaching, tutorials, interactive, onboarding]
  category: workflow
  source: shanraisshan/claude-code-best-practice
---

## Purpose

Transform static SKILL.md docs into interactive learning. Power-ups teach skills step-by-step with real examples, exercises, and knowledge checks.

---

## Invocation

```
/powerup <skill-name>           # full tutorial
/powerup <skill-name> --quick   # key concepts only
/powerup <skill-name> --test    # knowledge check only
```

---

## Power-Up Flow

### Step 1: Introduction
- What you'll learn (3 bullets)
- Estimated time
- Prerequisites

### Step 2: Concept Modules (one per core concept)
For each concept:
- **The Problem**: Why it matters
- **The Pattern**: Correct approach with real code
- **Anti-Pattern**: What NOT to do
- **Try It**: Small exercise
- **Check**: Verify they got it right

### Step 3: Knowledge Check
3-5 multiple choice questions from the concepts.

### Step 4: Summary
Key takeaways + link to full SKILL.md.

---

## Generating from SKILL.md

When no POWERUP.md exists, dynamically generate:
1. Read SKILL.md
2. Extract: Purpose, Rules, Examples, Anti-Patterns
3. Convert each Critical Rule into a module
4. Generate knowledge check questions
5. Present interactively

---

## Critical Rules

1. Power-ups are ALWAYS interactive — ask, wait, give feedback
2. Use real project code examples when possible
3. Keep each module under 2 minutes
4. ALWAYS end with a knowledge check
5. If user gets a question wrong, explain WHY before continuing
6. Never skip anti-patterns — knowing what NOT to do is critical

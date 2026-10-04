---
name: learning-mode-coding
description: >
  Activate when the user types "/learn" or "/learn <topic>".
  This switches Claude Code into a teaching-first coding mode for unfamiliar technologies.
  Do NOT trigger on any other signal — only the explicit /learn command.
  Once activated, stay in this mode for the remainder of the conversation unless the user says "/learn off".
---

# Learning Mode Coding

Teaching-first coding mode for Claude Code in dev containers.

## Rules

1. Never write code to files until user explicitly approves.
2. Never execute shell commands. Show exact command + explain what it does and why. User runs it themselves.
3. Explain WHY before WHAT. Every choice needs a reason.
4. One step at a time. Wait for user input between steps.
5. When any acronym appears for the first time in a session, expand it as: ACRONYM (Full Name: concise 1–2 line explanation of what it is). After the first occurrence, use the acronym alone.

## Flow

### 1. Scope

Read project context. Confirm task in 1–2 sentences. If unclear, ask one question.

### 2. Key Concepts

Explain 2–4 core concepts of the technology relevant to this task:
- What problem it solves (one sentence)
- Core mental model — how it thinks, its conventions, its opinions
- How it connects to this project

Brief. Senior-colleague briefing, not textbook.

### 3. Step Breakdown

List all implementation steps. Each: one line what + one line why.
Ask user to confirm or adjust before proceeding.

### 4. Per Step: Approach + Tradeoffs

For each step before writing code:
- Describe the approach
- Explain why (conventions, performance, maintainability)
- List alternatives with short pro/con if they exist
- Wait for user to pick

### 5. Per Step: Code + Explanation

After user picks:
- Show code in terminal (do NOT write to files)
- Explain block-by-block: what it does, why, gotchas
- For commands, use this format:

```
Command:
  <exact command>

What: <what it does>
Why: <why it's needed now>
```

### 6. Per Step: Confirm → Apply

User confirms → write to files. Summarize changes. Point to next step.

### 7. Repeat

Continue through steps. Recap progress every 2–3 steps.

## Overrides

- "just do it" / "skip explanation" → inline comments only, still show before writing. "why?" restores full explanation for any decision.
- Tangent question → answer in context, resume.
- Error after applying → explain what the error means in the technology's model, not just the fix.
- Existing code conflicts with convention → flag it, explain, don't refactor without asking.

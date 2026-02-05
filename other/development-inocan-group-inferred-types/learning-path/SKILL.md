---
name: learning-path
description: |
  Assess Claude Code knowledge and route to appropriate learning level.
  Use when: user wants to learn Claude Code, asks for guidance, or says "teach me".
  Triggers: "learn Claude Code", "teach me", "I'm new", "where do I start", "beginner".
---

# Learning Path Assessment

Determine user's Claude Code proficiency and guide them to the right level.

## Assessment Flow

### Step 1: Opening Question

Ask ONE question to gauge starting point:

```
"Have you used Claude Code before?"

A) Never — just installed it
B) A little — basic chat and file reading
C) Regularly — comfortable with tools and commands
D) Power user — I've built custom skills/agents
```

### Step 2: Branch by Answer

**If A (Never):** → Route to `foundations`
- Skip further assessment
- Start with absolute basics

**If B (A little):** Ask follow-up:
```
"Which of these have you done?"

A) Asked Claude to edit files
B) Used slash commands like /help
C) Both A and B
D) Neither — just chatted
```
- If D → `foundations`
- Otherwise → `intermediate`

**If C (Regularly):** Ask follow-up:
```
"Which of these have you set up?"

A) Custom slash commands
B) MCP servers
C) Hooks (pre/post commit, etc.)
D) None of these yet
```
- If D → `intermediate`
- Otherwise → `advanced`

**If D (Power user):** Verify with:
```
"What's your goal today?"

A) Learn something specific I haven't tried
B) Fill gaps in my knowledge
C) Just exploring what's new
```
→ Route to `advanced` with specific focus

## Level Descriptions

| Level | Profile | Focus |
|-------|---------|-------|
| Foundations | New user, <1 week | Basic commands, file ops, chat patterns |
| Intermediate | Comfortable user | Tools, MCP, customization, workflows |
| Advanced | Power user | Custom agents, skills, complex automation |

## After Routing

Once level is determined:

1. Explain what they'll learn at this level
2. Offer first topic or let them choose
3. Mention they can switch levels anytime with `/cc:level`

## Progress Tracking

Track in conversation context:
- Current level
- Completed topics (checklist style)
- Areas of interest

On return visits, ask:
```
"Welcome back! Last time we covered [X].
Want to continue, or explore something else?"
```

## Key Principles

| Principle | Implementation |
|-----------|----------------|
| One question at a time | Never ask multiple questions |
| Multiple choice preferred | Always offer A/B/C/D options |
| No judgment | All levels are valid starting points |
| Respect expertise | Don't over-explain to advanced users |
| Quick routing | 1-2 questions max to determine level |

## Transition Between Levels

User can move up or down:
- `/cc:level foundations` — go back to basics
- `/cc:level intermediate` — jump to middle
- `/cc:level advanced` — skip ahead

When user completes a level's core topics:
```
"You've covered the foundations! Ready to move to intermediate?
We'll explore [preview of next level topics]."
```

## Integration

After assessment, invoke appropriate skill:
- `foundations` skill for Level 1
- `intermediate` skill for Level 2
- `advanced` skill for Level 3

Each level skill has its own curriculum and reference docs.

---
name: pair-programming
description: Structure effective pairing sessions with an AI agent or human partner using driver/navigator roles. Apply pair programming principles to maximize knowledge transfer, code quality, and flow. Includes AI-specific prompting patterns for Copilot, Claude, and Codex.
triggers:
  - "pair with me"
  - "let's pair"
  - "driver navigator"
  - "pair programming"
  - "mob programming"
  - "walk me through this together"
audience:
  - engineer
---

# Pair Programming

Structure collaborative coding sessions for maximum quality and learning — with an AI agent or a human.

---

## Core Roles

### Driver
- Controls the keyboard / writes the code
- Focuses on implementation details and syntax
- Thinks tactically: "how do I write this?"

### Navigator
- Observes, thinks ahead, reviews as code is written
- Focuses on design, correctness, and direction
- Thinks strategically: "are we solving the right problem?"

**Key principle**: The navigator doesn't dictate line by line. The driver has autonomy over *how*; the navigator steers *what* and *why*.

---

## Pairing with an AI Agent

### When AI is the Navigator (You Drive)
Use this when: you know *what* to build, you want the AI to catch issues, suggest better approaches, and keep you from going down rabbit holes.

**Prompt pattern:**
```
I'm going to implement [feature/function]. 
Act as my navigator:
- Watch for edge cases I might miss
- Flag if my approach is headed the wrong direction
- Suggest alternatives only when you see a meaningfully better path
- Ask clarifying questions if the intent is ambiguous

Here's where I'm starting: [paste current code or describe starting point]
```

### When AI is the Driver (You Navigate)
Use this when: you have a clear design in mind, you want to move fast, and you'll review what the AI produces.

**Prompt pattern:**
```
I'll navigate, you drive. 
Implement [specific task] following these constraints:
- [constraint 1: language, pattern, library]
- [constraint 2: must not break existing interface]
- [constraint 3: follow existing conventions in this file]

Write it in small steps. After each step, pause and I'll tell you to continue or adjust.
```

### Ping-Pong (TDD Pairing)
AI writes the failing test → You write the code to pass it → AI refactors → repeat.

**Prompt pattern:**
```
Let's do ping-pong TDD for [function/feature].
You write the first failing test. I'll write the implementation to make it pass.
Then you refactor if needed. Then you write the next test.
Start with the simplest case.
```

---

## Human Pair Programming

### Session Setup (5 min)
1. **Goal**: What are we trying to accomplish this session?
2. **Driver starts**: Decide who drives first
3. **Swap cadence**: Every 25 minutes (Pomodoro) or at natural breakpoints
4. **Vocabulary**: Agree on how to signal role switches ("want to swap?" / "I'll take the wheel")

### During the Session
**Driver do's:**
- Think out loud — narrate your intent
- Say when you're stuck; don't silently struggle
- Accept direction from navigator without ego

**Navigator do's:**
- Look ahead: what's the next test? what could break?
- Speak up early if approach seems wrong — don't wait until it's built
- Stay at design level; don't dictate keystrokes

### Common Dysfunctions
| Dysfunction | Fix |
|---|---|
| Navigator goes silent | Check in: "Does this approach look right to you?" |
| Navigator micromanages keystrokes | "Let me drive how, you steer where" |
| Driver ignores navigator | Explicit agreement: navigator gets a veto |
| Sessions drag too long | Time-box with Pomodoro; swap roles to re-energize |
| No clear goal | Define the done condition before starting |

---

## Mob Programming (3+ people)

Scale pairing to the whole team:
- **One driver** at a time (rotates every 10-15 min)
- **Rest are navigators** — everyone contributes direction
- **Facilitator** manages rotation and keeps discussion productive
- **Best for**: complex problems, onboarding, critical paths, architecture decisions

---

## Pairing Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Watching, not navigating | Navigator browsing phone/email | Explicit navigator tasks: write the test, look up the docs |
| Unequal pairing | Senior always drives | Intentionally swap; junior learns by driving |
| No breaks | 4-hour marathon session, quality drops | Pomodoro: 25 min on, 5 min break |
| Pairing on everything | Teams burn out | Reserve pairing for: new features, hard bugs, onboarding, critical code |
| AI pairing without review | Accepting all AI output without reading | Navigator role: read and challenge every suggestion |

---

## When to Pair vs. Solo

**Pair when:**
- New feature in unfamiliar area
- Hard bug that's been stuck for > 30 min
- Security-sensitive or high-stakes code
- Onboarding a new team member
- Design decision with multiple valid approaches

**Solo when:**
- Well-understood, routine work
- Exploratory spike / prototype (pair to review the output)
- Documentation, config changes, dependency bumps

---

## Session Retrospective (2 min)

At the end of each pairing session:
```
What went well?
What slowed us down?
Any follow-up tasks?
Would we pair on this type of work again?
```

---

## References
- Kent Beck: *Extreme Programming Explained*
- Martin Fowler: [Pair Programming](https://martinfowler.com/articles/on-pair-programming.html)
- Woody Zuill: [Mob Programming](https://mobprogramming.org/)
- LeadDev: [How to pair effectively with AI coding assistants](https://leaddev.com/ai-assisted-development)

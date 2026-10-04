---
name: superpowers-office-hours
description: >
  Use when the user wants to explore a product idea, validate a concept, get clarity on what to
  build, or get unstuck on a product decision. YC-style product framing — six forcing questions
  that expose demand reality before any code is written. No implementation. Produces a design doc.
  Use when asked "office hours", "product framing", "think about this idea", "is this a good idea",
  "validate my concept", "what should I build", "help me clarify this".
---

> **DEPRECATED** — use `/office-hours` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Office Hours

**Purpose:** Reframe product thinking before any code is written. YC partner posture — hard diagnostic, not cheerleading.

**Core principle:** No implementation. No code. One question at a time.

---

## Modes

| Mode | Posture | When |
|------|---------|------|
| **Startup** | Hard diagnostic | Real product, revenue ambition, market validation |
| **Builder** | Enthusiastic collaborator | Side projects, hackathons, learning, OSS |

Detect mode from context. If the user mentions revenue, customers, or a specific market — use Startup. If they mention learning, exploring, or a hobby — use Builder.

---

## Phase 1: Context Gathering

Read existing project files:

```bash
ls -la
cat README.md 2>/dev/null || true
cat package.json 2>/dev/null | head -30 || true
find . -maxdepth 2 -name "*.md" -not -path "./node_modules/*" 2>/dev/null
```

Detect: Is this greenfield or iteration? What stage is the product? Any existing office-hours output to build on?

---

## Phase 2: Diagnostic (one question at a time)

Ask **one question per message**. Wait for the answer before asking the next.

### Startup Mode — Six Forcing Questions

1. **Demand evidence:** "How do you know people want this? Not how you feel — what evidence exists? Have you talked to users? Is there revenue? Traffic data? Waitlist signups?"

2. **Status quo:** "What do people do today instead of this? Name the specific alternative. Why is that worse? What would make someone switch?"

3. **Specific users:** "Who is the specific person who will use this first? Not 'developers' or 'businesses' — a name and a job title. What are they doing right now that this replaces?"

4. **Narrowest wedge:** "What's the smallest version of this that proves the core value? Strip everything that isn't essential. What remains if you remove 80% of the features?"

5. **Real observation:** "What have you personally observed — not inferred, not researched — that tells you this problem exists at scale?"

6. **Future fit:** "If this works, what does it look like in 2 years? What's the wedge that opens? Does the initial idea lead somewhere meaningful, or is it a dead end?"

### Builder Mode — Design Thinking Exploration

1. "What would the most impressive version of this look like — not for shipping, just for dreaming?"

2. "What excites you most about this idea? What's the one part you'd build first even if no one used it?"

3. "What would you learn by building this that you can't learn any other way?"

4. "Who would you show this to first, and what would you want their reaction to be?"

---

## Phase 3: Premise Challenge

Before generating alternatives, agree on the foundational assumptions:

```
FOUNDATIONAL ASSUMPTIONS
════════════════════════════════
1. [Assumption from Q1 — demand]
2. [Assumption from Q2 — status quo]
3. [Assumption from Q3 — users]
4. [Assumption from Q4 — wedge]
5. [Assumption from Q5 — observation]
6. [Assumption from Q6 — trajectory]
════════════════════════════════

Are these correct? Which would you challenge most?
```

---

## Phase 4: Alternatives Generation

Present 2-3 approaches with tradeoffs:

| Approach | Description | Risk | Upside |
|----------|-------------|------|--------|
| **Minimal** | MVP that proves core value | Low | Low |
| **Ideal** | Complete vision | High | High |
| **Creative** | Unexpected approach | Unknown | High |

Recommend one based on the diagnostic answers. Always recommend the minimal viable wedge — completeness costs near-zero with AI, but the first step should be as small as possible.

---

## Phase 5: Design Doc Output

Save to `docs/superpowers/specs/YYYY-MM-DD-office-hours.md`:

```markdown
# Office Hours — [Project Name]

**Date:** YYYY-MM-DD
**Mode:** [Startup/Builder]
**Product stage:** [Greenfield/Iteration]

## Problem Statement
[1-2 sentences on the core problem]

## Six Diagnostic Answers

1. **Demand evidence:** [Answer]
2. **Status quo:** [Answer + specific alternatives]
3. **Specific users:** [Answer + job title]
4. **Narrowest wedge:** [Answer + what's removed]
5. **Real observation:** [Answer]
6. **Future fit:** [Answer + 2-year vision]

## Foundational Assumptions
- [List of agreed-upon assumptions]
- [Which to challenge]

## Proposed Approach
[Minimal / Ideal / Creative — recommendation + rationale]

## Next Step
[What's the first thing to do]
[What the next skill should be]
```

Commit the design doc.

---

## Phase 6: Handoff

Signal to the user what was revealed and what to do next:

1. **Synthesis:** What the diagnostic exposed (one sentence)
2. **Tier recommendation:**
   - Startup mode: "This is ready for `/superpowers-plan-ceo-review`" if the idea is strong, or "needs more validation" if demand is unproven
   - Builder mode: "This is ready for `/superpowers-writing-plans`" or "keep exploring"
3. **Assignment:** Explicitly ask the user to commit to the next action

---

## Key Rules

- **No implementation** — this skill produces a document, not code
- **One question per AskUserQuestion** — never batch
- **Hard diagnostic, not cheerleading** — if demand isn't proven, say so
- **Mandatory assignment** — end with a specific next action, not open-ended
- **Read prior output** — if office-hours output exists, reference it before starting

---

## Completion Status

- **DONE** — Diagnostic complete, design doc written and committed
- **DONE_WITH_CONCERNS** — Diagnostic done but assumptions are weak
- **BLOCKED** — User won't engage with diagnostic questions
- **NEEDS_CONTEXT** — Need more context to ask the right questions

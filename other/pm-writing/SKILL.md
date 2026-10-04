---
name: pm-writing
description: "Rewrite or generate PM documents with extreme clarity. Applies principles of canonical docs, numbered lists over bullets, force-ranked priorities, BLUF structure, and visual-first communication. Transforms vague PM writing into precise, actionable docs."
argument-hint: "[paste text to rewrite OR describe what you need to write]"
---

# PM Writing Skill

Transform vague product writing into precise, actionable communication. Or generate new docs from scratch using PM writing best practices.

## When to Use
- User has a draft doc and wants it sharpened
- User needs to write a doc from scratch with extreme clarity
- User says `/pm-writing` followed by text to rewrite or a description
- Any PM communication that needs to be clearer, shorter, or more actionable

## Two Modes

### Mode 1: Rewrite
User pastes existing text. Rewrite it applying all principles below. Show before/after.

### Mode 2: Generate
User describes what they need. Generate it from scratch using the principles below.

---

## The 10 Principles of PM Writing

### 1. Bottom Line Up Front (BLUF)
The first sentence of any document should answer: "What do you need from the reader?"

**Bad:** "Background on Q4 planning: Over the past several months, we've been evaluating various approaches to our recommendation system..."
**Good:** "We need to decide by Friday whether to rebuild the recommendation engine (8 weeks) or patch the current one (2 weeks). I recommend rebuilding. Here's why."

Never make the reader hunt for the point. Lead with the decision, ask, or conclusion.

### 2. Numbered Lists Over Bullets
Use numbered lists instead of bullet points. Numbers allow precise referencing in feedback and discussion.

**Bad:**
- Improve onboarding flow
- Fix search latency
- Add export feature

**Good:**
1. Improve onboarding flow (activation +15%)
2. Fix search latency (p95 from 2s → 500ms)
3. Add export feature (top enterprise request)

Now a reviewer can say "I disagree with #2's priority" instead of "the second thing you mentioned."

### 3. One Canonical Doc Per Topic
Every project should have exactly one source of truth. It links to everything else but IS the definitive reference.

**Structure of a canonical doc:**
- Title, owner, last updated date
- Status (Draft / Active / Archived)
- The content itself (goals, decisions, open questions)
- Links to related docs (not duplicated content)

Never let the same information live in two places. When something changes, update the canonical doc.

### 4. Canonical Nomenclature
Use consistent names for things. If the feature is called "Smart Search" in the PRD, it's "Smart Search" in the design doc, the eng spec, the launch plan, and Slack.

**Bad:** The doc calls it "intelligent search," the ticket says "AI search," and the meeting notes say "the new search thing."
**Good:** Pick one name. Use it everywhere. Put it in the canonical doc.

### 5. Force-Rank, Never Group
When listing priorities, never say "these are all important." Stack-rank them. Ranking should feel uncomfortable — that means you're actually making choices.

**Bad:** "Our priorities this quarter are growth, quality, and platform stability."
**Good:**
1. Platform stability (P0 — nothing else matters if the system is down)
2. Quality (P1 — retention depends on it)
3. Growth (P2 — invest only after 1 and 2 are green)

### 6. Quantify Everything
Replace vague words with numbers. If you don't have exact numbers, estimate and flag it.

**Bad:** "This will significantly improve performance."
**Good:** "This will reduce p95 latency from 2.1s to ~500ms (estimated, need load testing to confirm)."

**Bad:** "Many users are affected."
**Good:** "~12K MAU (18% of paid users) hit this bug weekly."

### 7. Every Hypothesis Needs Five Parts
Never write a vague hypothesis. Every testable claim needs:

1. **Action**: What are we changing?
2. **Metric**: What outcome are we measuring?
3. **Magnitude**: How much change do we expect?
4. **Segment**: For which users?
5. **Conditions**: Under what circumstances?

**Bad:** "Adding onboarding tooltips will improve activation."
**Good:** "Adding 3-step onboarding tooltips (action) will increase D7 activation (metric) by 8-12% (magnitude) for new free-tier users (segment) who sign up via organic search (conditions)."

### 8. Make Decisions Visible
When a decision is made, write it down with:
- What was decided
- Who decided it
- When it was decided
- What alternatives were considered
- When to revisit

**Format:**
> **Decision [date]:** We will use approach B (streaming API). Decided by [owner] after evaluating batch API (too slow) and WebSocket (over-engineered). Revisit if latency requirements change.

### 9. Three Options With a Recommendation
When presenting a decision to stakeholders, always provide:
- Option A (conservative)
- Option B (moderate) — usually your recommendation
- Option C (ambitious)

For each: one-sentence description, key trade-off, estimated effort.

End with: "I recommend Option B because [one sentence reason]."

Never present a problem without a recommended solution. Never present only one option (that's not a decision, it's a decree).

### 10. Write for Scanners, Not Readers
Most stakeholders will spend 30 seconds on your doc. Design for that.

- **Headers** that tell the story (someone reading only headers should get the gist)
- **Bold** the key numbers and decisions
- **Tables** for comparisons (never compare things in paragraph form)
- **Short paragraphs** (3 sentences max)
- **TL;DR at the top** (always)

---

## Anti-Patterns to Fix

| Bad Pattern | Fix |
|---|---|
| "I think we should maybe consider..." | "We should [X]. Here's why." |
| "There are some concerns about..." | "Risk: [specific risk]. Mitigation: [specific action]." |
| "We need to align on..." | "Decision needed: [specific question]. Options: [A/B/C]." |
| "Going forward, we'll..." | "By [date], [owner] will [specific action]." |
| "Various stakeholders..." | "[Name/team] and [name/team]." |
| "Significant improvement..." | "[X]% improvement in [metric]." |
| "ASAP" | "By [specific date]." |
| Wall of text | Numbered list with one idea per line |

## Output Format

### For Rewrites:
Show the rewritten text, then a "Changes made" section listing which principles were applied and why.

### For New Docs:
Generate the document applying all 10 principles. Flag any places where the user needs to provide specific data (numbers, names, dates).

## Tone
Direct but not aggressive. Confident but not arrogant. The goal is respect through clarity — honoring the reader's time by being precise.

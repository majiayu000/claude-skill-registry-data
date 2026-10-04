---
name: ux-review
description: Walk a UI feature as a real user before shipping it. Identifies the cognitive friction the user will hit — confusion, dead-ends, wrong-target clicks — and reports it with severity. Use this BEFORE calling a UI feature done. Breaks the rework loop where the user reviews in prod and sends it back.
user-invocable: true
---

# UX Review

The biggest source of rework on UI work is shipping something that the agent has only ever read in code form. The user opens it in production, can't figure out where to click, tries the wrong thing, and sends it back. This skill makes the agent USE the page as a fresh user and catch the friction before the user does.

## When to invoke

- After implementing a UI change, before calling it done
- Before opening a PR for any UI feature
- Before merging on UI-impacting ship-skill runs (`/ship-auto`, `/ship-guarded`)
- Anytime an agent says "the UI is ready" — invoke this first

## What you'll need

- The UI running locally (a dev server URL) OR a deployed URL
- The user goal(s) the page is supposed to enable
- `claude-in-chrome` MCP tools (the skill assumes they're available)

If `claude-in-chrome` isn't connected, stop and ask the user to start Chrome with the extension. Don't try to "review from the code" — that defeats the purpose.

## The walkthrough

Walk each user goal as if you've never seen the page before. For each goal:

1. **Land on the page cold.** First impression — what does this page tell you it does, without reading carefully? If a first-time user couldn't answer "what is this?" in 3 seconds, that's a finding.

2. **Find your starting point.** Where does your eye go first? Is the primary action visually dominant? If the most prominent element isn't what the user should click first, that's a finding.

3. **Try to complete the goal.** Click, type, navigate. Note every moment of:
   - "Where do I go now?" (next-step ambiguity)
   - "Is that clickable?" (affordance failure)
   - "What does this button do?" (label clarity)
   - "Did that work?" (feedback failure)
   - "I made a mistake — how do I undo?" (recovery failure)

4. **Try to mess it up.** Submit empty fields. Click the wrong thing first. Use keyboard only. What breaks?

5. **Try to do it on mobile.** Resize to ~375px width. Targets too small? Layout broken? Important content below the fold?

Take screenshots at the key states — initial load, mid-flow, completion, error states.

## The heuristic checklist

After the walkthrough, evaluate against these. For each, mark Pass / Issue / Critical:

**Visibility & feedback (Nielsen #1)**
- Does the system tell the user what's happening at all times?
- After every action, is there visible confirmation within ~1 second?

**Match between system and real world (Nielsen #2)**
- Are labels in the user's language, not technical jargon?
- Do icons match what the user would expect them to mean?

**User control and freedom (Nielsen #3)**
- Is there an obvious way to undo a mistake?
- Can the user back out of any flow without losing progress?

**Consistency and standards (Nielsen #4)**
- Do similar things look similar? Different things look different?
- Does the page follow conventions the user already knows from other sites?

**Error prevention (Nielsen #5)**
- Are dangerous actions confirmed before they happen?
- Are inputs validated as the user types, not after submit?

**Recognition over recall (Nielsen #6)**
- Are options visible, or does the user have to remember what's available?
- Is necessary information available where it's needed?

**Flexibility and efficiency (Nielsen #7)**
- Are there shortcuts for power users (keyboard, bulk actions)?
- Can the user customize what they see frequently?

**Aesthetic and minimalist design (Nielsen #8)**
- Is every element on the page necessary for the user's goal?
- Does decoration compete with the primary action for attention?

**Recover from errors (Nielsen #9)**
- When something goes wrong, does the message say what happened, why, and what to do next?
- Are error messages constructive, not blaming?

**Help and documentation (Nielsen #10)**
- If help is needed, is it findable in context?
- Can the user accomplish the goal without leaving the page to read docs?

**Motor / Fitts's Law**
- Are click targets ≥44×44px on mobile, ≥24×24px on desktop?
- Is the most-used target closest to where the user's hand/cursor naturally rests?
- Are destructive actions far from frequent ones?

**Visual hierarchy**
- Does the visually dominant element on the page match the user's most likely first action?
- Does the eye naturally flow in the order the user needs to read/act?
- Is there enough contrast between primary and secondary actions?

**Goal completion**
- Did you actually accomplish the goal?
- How many steps did it take vs. how many it should have?
- At any point did you guess what to do, or did the page tell you?

## The report

Produce a single markdown report with:

```markdown
## UX Review — [feature name]
**Reviewed:** [URL] at [timestamp]
**Goals tested:** [list]

### Goal completion
- Goal 1: ✅ completed in 3 steps (expected 3)
- Goal 2: ⚠️ completed in 7 steps (expected 4) — got lost looking for X

### Critical issues (block ship)
1. **[Heuristic]** — [what's wrong, where, why it matters]

### Issues (should fix before ship)
1. **[Heuristic]** — [what's wrong, where, why it matters]

### Polish (post-ship OK)
1. **[Heuristic]** — [what's wrong, where, why it matters]

### Screenshots
- [path/to/initial.png] — initial load
- [path/to/midflow.png] — mid-flow
- [path/to/error.png] — error state

### What worked well
- [Notable strengths — keep doing these]
```

## How to use the report

- **Critical issues:** do not ship. Fix and re-run the review.
- **Issues:** fix before opening PR, or open PR with explicit acknowledgement and follow-up tickets.
- **Polish:** open as follow-ups, ship the main feature.

## Anti-patterns

- **Don't review from the code.** The whole point is to see what the user sees. If you can't run it, say so and stop.
- **Don't grade your own homework.** If the agent that built the feature is doing the review, dispatch a fresh subagent without context to walk it cold. Familiarity hides friction. Tell it what to return: pass/fail per goal, findings with severity, and screenshot *paths* — never page text, DOM, or a click-by-click narration.
- **Don't over-engineer the heuristics.** The point is to catch obvious problems quickly, not write a 10-page evaluation.
- **Don't skip the goal-completion test.** Heuristic violations can be wrong; failure to complete a goal can't.

## Future enhancements (not yet implemented)

- Wire `npx -y a11y-mcp-server` for automated WCAG/keyboard scans
- Wire Lighthouse for performance + accessibility scoring
- For high-stakes UI changes, dispatch multiple persona-driven walkthroughs (UXAgent-style)

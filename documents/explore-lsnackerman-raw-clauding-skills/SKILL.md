---
name: explore
description: Build topic reserves by searching your entire system, or run discovery mode to find what connects across territories. Use when consolidating scattered knowledge on a topic, before writing/sharing, or when curiosity has no specific target.
argument-hint: [topic, or omit for discovery mode]
---

# /explore - Build Topic Reserves

Search your system for everything on a topic. Build rich reserves that combine synthesis, verbatim texture, and source references. Or (if you don't have a specific topic) run discovery mode to find what connects across territories.

---

## Two Modes (Both Work at Any Stage)

**Topic mode** (with an argument): "explore X." You know what you're looking for. Output is a compounding reserve that grows over time as you keep exploring the same topic.

**Discovery mode** (no argument): "see what's there." You're listening for what wants to surface. Output is a timestamped snapshot of cross-territory connections; a moment-in-time view, not a compounding doc.

These aren't gated by system age. New systems benefit from discovery mode (find unexpected connections in what little exists). Mature systems benefit from topic mode (depth on threads you already know matter). Read what you're asking the system to show you, and pick.

---

## What To Do

1. **Clarify mode**: topic or discovery? If topic mode, ask if not specified: "What topic are we exploring?"
2. **Search everywhere** — task docs, session logs, reference material, random notes, anywhere content lives in your system
3. **Gather everything** — see "What to Gather" below
4. **Output** to `reserves/[topic].md` (topic mode) or `reserves/discovery-YYYY-MM-DD.md` (discovery mode). Create the `reserves/` folder if it doesn't exist.

---

## Inline vs Parallel Search (Read Your Signal)

**Inline** (you do the searching): grep, glob, read files yourself. Fast, low overhead, your context window holds the texture as you go.

**Parallel** (fan out sub-agents): split the system into territories, send a sub-agent to each, assemble the returns.

The choice is about scope:
- **Inline fits** when you can hold the search in one head: 3-5 file reads, narrow topic, fast iteration matters
- **Parallel fits** when the search would saturate your context: many territories to scan, broad topic, you want results without losing the rest of your working memory

If you're not sure, start inline. Switch to parallel when you notice you're losing track of what you've already found.

---

## What to Gather

- **Decisions** made about this topic, including the why
- **Insights and patterns** that emerged, things noticed over time
- **Verbatim texture** — the back-and-forth that shows how thinking happened, questions still open
- **Genesis** — what triggered the exploration?
- **Contrast structures** — "the default approach does X, we do Y"
- **Source references** — which doc, which session, which date

---

## Output Format

```markdown
# [Topic] - Exploring Reserves

**Last updated**: YYYY-MM-DD
**Sources**: [list of docs mined]

---

## Key Insights
- Insight 1
- Insight 2

## Decisions Made
| Decision | Why | Source |
|---|---|---|

## Verbatim Texture
### [Context/Source]
> "Your exact words"

AI's response...

*Why this matters: [brief note]*

## Patterns Noticed
## Open Questions
## Related
```

---

## Philosophy

**Fill the tank before you drive.** Your system often has what you need already, scattered across files.

**Reserves are living docs.** Each exploration adds to what's there. The second pass on a topic is always richer than the first. When new material lands mid-session (a decision, a pattern, a reframe that touches a topic you've already explored) add it back to the reserve.

**Texture matters.** Verbatim exchanges preserve HOW you think together, not just what you concluded.

---

## Skill Check (After Every Explore)

Quick scan: anything about this exploration that felt off or could be smoother?

- Did the search strategy find what mattered, or miss obvious locations?
- Was the output format useful or too dense?
- Did the exploration surface things you didn't know you had?
- Was it clear when to stop exploring vs keep digging?
- Did the mode (topic vs discovery) and search style (inline vs parallel) fit what you were actually doing?

**If yes** → update this skill now. The improvement compounds.

**If no** → move on. Not every exploration teaches something.

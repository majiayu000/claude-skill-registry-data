---
name: presentation-builder
description: Transform ideas, outlines, or documents into structured slide content with clear titles, bullet points, and speaker notes. Adapts to presentation type (pitch decks, business reviews, technical workshops, educational talks). Use when user says "create slides", "build a deck", "pitch deck", "presentation structure", "talk structure", "keynote", "slide deck", "conference talk", or needs slide content for any format. Also trigger when user has content they want to present to an audience - even if they don't explicitly say "presentation" or "slides".
---

# Presentation Builder

## How It Works

### Step 1: Gather Inputs

Ask the user:
1. **Audience** - Who is in the room? (investors, team, clients, community)
2. **Duration** - How long? (5 min = 5-7 slides, 15 min = 12-15 slides, 30 min = 20-25 slides)
3. **Purpose** - What decision or action should the audience leave with?
4. **Content** - What does the user have? (raw notes, doc, outline, or just a topic)

### Step 2: Select Structure Template

**Pitch Deck** (investors, sponsors):
Problem > Solution > Market Size > How It Works > Traction/Proof > Team > Ask

**Business Review** (leadership, stakeholders):
Context > Performance vs. Goal > Key Findings > Risks/Blockers > Decisions Needed > Next Steps

**Technical Workshop** (practitioners):
Problem Definition > Concepts > Demo/Walkthrough > Common Pitfalls > Hands-On Exercise > Key Takeaways

**Educational Talk** (community, general audience):
Hook/Story > Core Idea > Evidence/Examples > Implications > What To Do Next

### Step 3: Generate Slide Content

For each slide:
- **Title**: 5-10 words, states the takeaway - not the topic
  - Weak: "Market Overview" - Strong: "TAM is $4B and growing 30% YoY"
- **Bullets**: 3-5 max. If you have 8 bullets, you have 2 slides.
- **Visual placeholder**: `[IMAGE: description of what visual would go here]`
- **Speaker note**: 1-2 sentences of what to say out loud (include only if requested)

### Step 4: Output Format

Deliver as numbered slides in markdown:

```
## Slide 1: [Title]
- Bullet 1
- Bullet 2
- Bullet 3
[IMAGE: description]
Speaker note: ...
```

After the slides, add:
- Slide count and estimated time at a comfortable pace
- One sentence on the best tool for rendering (Gamma for visual polish, Google Slides for collaboration, Canva for design flexibility)

## Rules

- Keep slides to 3-5 bullets. Beyond 5, the audience reads instead of listening - the slide competes with the speaker instead of supporting them.
- Every slide title must state a takeaway, not a label. Audiences remember "Revenue grew 40% in Q3" but forget "Revenue Update." A takeaway title means even someone skimming the deck gets the story.
- If the user's content has more material than slides allow, recommend what to cut. Cramming dilutes every point - a focused deck with 12 strong slides beats 20 slides where half are filler.
- Slide count = duration in minutes / 2 (rough guide; adjust for content density).

## Anti-Patterns

**1. Wall-of-text slide**
Bad: A slide with 8 bullets and a paragraph of context underneath
Good: Split into two slides, each with 3-4 bullets that the speaker elaborates on verbally

**2. Label title**
Bad: "Market Overview"
Good: "TAM is $4B and growing 30% YoY"

**3. Reading the slides**
Bad: Speaker notes that repeat the bullet text word for word
Good: Speaker notes that add context, stories, or data the bullets don't show

**4. Everything-in-the-deck**
Bad: 30 slides for a 15-minute talk because "the content is important"
Good: 12 slides for the talk, appendix slides for the Q&A backup

**5. Decoration over clarity**
Bad: Complex charts with 6 data series and no callout
Good: One chart, one trend line highlighted, one takeaway in the title

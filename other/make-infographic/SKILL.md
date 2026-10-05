---
name: make-infographic
description: Research or verify factual inputs, write a concise source-backed brief, and turn it into one readable infographic. Use when facts or data must be checked before visual design; never invent statistics or let image generation rewrite approved copy.
---
# Make Infographic
## Catalog
- Display name: Make Infographic
- Categories: Social Media, Layout & Design
- Status: Ready
- Route label: Research plus GPT Image 2
- Tone: cyan
- Short description: Research, write, and visualize a sourced infographic.
## What this skill does
- Produces a factual content brief before image generation.
- Organizes one message, five to seven evidence points, labels, units, and a source line.
## How to use
Provide topic, audience, locale, channel, ratio, and mandatory sources or claims.
#### Make a sourced infographic
```text
Research household water-saving actions and make a Chinese vertical infographic with sources.
```
## Workflow
1. Research primary or authoritative sources; record URLs, dates, units, geography, and caveats.
2. Freeze exact title, subtitle, five to seven points, labels, and source line.
3. Choose comparison, process, timeline, map, hierarchy, or dashboard structure from the data relationship.
4. Use `gpt-image` v1.0 at Medium with the frozen brief and ask it to render the complete infographic; retry only the incorrect text or hierarchy with a stricter prompt.
5. Compare every number and word to the brief; reject invented facts, bad units, illegible type, or misleading charts.
When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output
- Media type: One infographic image plus approved text brief
- Default quantity: 1
- Content per image: One message and five to seven evidence points
- Default layout: Relationship-led information hierarchy
- Model policy: GPT Image 2 Medium with agent-led copy verification and revision
- Downstream use: Reports, education, and social explainers

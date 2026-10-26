---
name: ux-research-synthesis
description: Use when turning user interview transcripts, research notes, usability test notes, survey answers or support tickets into findings, themes, insights, an affinity map, personas, a journey map or "how might we" opportunities, or when summarising what users said.
---

# UX Research Synthesis

## Overview

Turn raw research into findings a team can trust and act on. Every insight is traced to participants and quotes, shows how many people it came from, and separates what people did from what they said.

## Inputs

- Transcripts, notes, recordings' text, survey exports or tickets. One file or section per participant is easiest.
- The research question or goal, if given. If missing, infer it from the questions asked and state it.
- Participant details (role, segment, plan) if available.

## Method

1. **Inventory.** List every source with a participant ID (P1, P2…) and segment. Replace names, emails, companies and other personal details with the ID.
2. **Extract observations.** Go through each participant and pull atomic notes: one behaviour, pain, need, workaround or quote per note, tagged with the participant ID. Mark each as **did** (observed or described a real past event) or **said** (opinion, wish, prediction).
3. **Cluster.** Group notes by similarity into themes (affinity mapping). Name each theme as a finding in a full sentence, not a topic word: "People export to Excel because the report cannot be filtered by date", not "Reporting".
4. **Count.** For each theme, count distinct participants (n of N). Note which segments it comes from and any participant who said the opposite.
5. **Write insights.** For the strongest themes: what happens, why it happens, and what it means for the product.
6. **Opportunities.** Turn each insight into one or two "How might we…" questions. Do not jump to features.
7. **Optional artefacts,** only if asked and supported by the data: personas (built from behaviour patterns seen in at least two participants), a journey map (stages, actions, thoughts, pains, opportunities).
8. **Confidence and gaps.** Say what the data cannot answer, where the sample is thin, and any bias in how questions were asked.

## Output

```
## Research synthesis: <study name>

**Research question:** <…>
**Participants:** N = <n> (<segments>) · **Sources:** <interviews, tests, survey…>

### Key findings
1. **<finding as a sentence>** — <n>/<N> participants (<segments>)
   - Evidence: "<verbatim quote>" — P3; <observed behaviour> — P5
   - Why: <underlying cause>
   - Implication: <what this means for the product>
   - Confidence: <high / medium / low> because <reason>

### Opportunities
- How might we <…>? (from finding 1)

### Contradictions and outliers
- <what didn't fit, and who>

### Gaps and next research
- <what we still don't know and how to find out>

### Appendix: themes
| Theme | Participants | Did / said | Example quote |
|---|---|---|---|
```

Confidence:
- **High:** most participants, across segments, with observed behaviour.
- **Medium:** several participants, or mostly stated rather than observed.
- **Low:** one or two participants, or one segment only.

## Rules

- Quotes are verbatim and attributed. Never invent, merge or "tidy up" a quote; shorten only with "…".
- Always show n of N. One participant is an anecdote: say "one participant", never "users".
- Weight what people did over what they said they would do. Feature requests are evidence of a need, not the solution.
- Keep personal data out: participant IDs only, no names, emails, employers or anything that identifies someone.
- Do not invent personas, numbers or segments that the data does not show.
- If the sample is too small or too narrow for a conclusion, say so instead of stretching.

## Common mistakes

- Themes named with one word ("Onboarding") that say nothing about what was learned.
- Counting mentions instead of people: one talkative participant looks like a pattern.
- Turning every request into a feature recommendation.
- Hiding the participant who disagreed.
- Personas with invented hobbies, ages and stock-photo names.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)

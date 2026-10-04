---
name: product-research-synthesizer
description: "Synthesizes qualitative and quantitative user research into product insights through a five-phase method: inventory the data, code observations into a codebook, build interpretive themes rated by evidence strength with counter-evidence, map insights to product opportunities, and package a full readout or executive summary. Use when the user has interview notes, survey responses, usability findings, support tickets, or analytics and wants them coded, themed, turned into opportunities, or written up as a research readout."
---

# Product Research Synthesizer

You help product teams turn raw research into insights they can build on. You take interview notes, survey answers, usability sessions, support tickets, and metrics, code them, group them into evidence-rated themes, translate those themes into product opportunities, and write the readout. Everything you analyze comes from the user or from their uploaded documents and connected knowledge sources; you never supply research data of your own.

## The method at a glance

Run the five phases below one after another, in order. If you jump to recommendations (Phase 5) before the data has been properly coded (Phase 2) and themed (Phase 3), the insights you produce will not be trustworthy.

### Phase 1: Take inventory of the evidence

Start by cataloging what data exists and what it is like:

```
EVIDENCE INVENTORY
  Study:               [name of the research project]
  Question it answers: [what the research was designed to find out]

  What we have:
  | Kind of source         | How many | Collected via                    | Who took part | When         |
  |------------------------|----------|----------------------------------|---------------|--------------|
  | [interviews, say]      | [n]      | [1:1 / group / unmoderated]      | [segment]     | [date range] |
  | [survey replies, say]  | [n]      | [open-ended / structured / mixed]| [segment]     | [date range] |

  Segment coverage:
  | Segment   | Planned n | Achieved n | Status: over / under / met |
  |-----------|-----------|------------|----------------------------|
  | [segment] | [n]       | [n]        | [status]                   |

  Limits we already know about:
  - [for instance: power users only, so newcomers' perspective is missing]
  - [for instance: 15% of those surveyed replied, so self-selection bias is likely]
```

Then decide whether this data can credibly answer the research question at all. When important participant segments are absent or the samples are very small, raise that limitation prominently, because it constrains every finding that comes after it.

### Phase 2: Break the material into coded observations

Coding breaks raw material into structured units you can analyze. It takes the most effort of any phase, which is exactly why people are tempted to skip it. Don't.

**First, extract observations.** Work through each source and pull out discrete observations: particular things a participant said, did, or went through. Keep to one observation per unit.

```
OBSERVATION
  Who:        [participant ID, anonymized]
  From:       [interview / survey / usability test / support ticket]
  Raw record: [the participant's words verbatim, or what they were seen doing]
  Trigger:    [the prompt behind it: question posed, task tried, or scenario]
```

**Next, attach codes.** Give each observation a short descriptive label that captures its concept. Hold yourself to these habits:

- Borrow the participants' own words where you can, and don't force your own framework onto the data too early.
- Let an observation carry several codes when it touches several themes; behavior often does.
- Begin with open coding, working up from the data, before bringing in any predefined categories.
- When different participants describe the same concept in different words, give it one consistent code.
- Count how often each code appears, but do NOT treat frequency as importance. A rare but severe pain point can outweigh a common mild one.

**Finally, keep a codebook** and organize codes in it as they build up:

```
CODEBOOK
| Code label | Meaning          | Typical quote           | Participants (n) |
|------------|------------------|-------------------------|------------------|
| [label]    | [what it covers] | [a representative line] | [count]          |
```

### Phase 3: Build and weigh themes

A theme is a pattern that appears when related codes are grouped. It is NOT a recap of single observations. Rather, it makes an interpretive claim about what those observations mean taken together.

1. **Group codes** that point to one underlying pattern. Good signals are codes that:
   - tend to show up together (the same participants display both)
   - describe different sides of one experience
   - form a cause-and-effect chain, one leading to the next
2. **Name the theme** as an interpretive statement, not a topic.
   - Weak, a topic: "Reporting"
   - Strong, an interpretation: "Users stop relying on in-app reports once exporting to a spreadsheet feels quicker than filtering"
3. **Rate its strength** using this scale:

| Level | What it takes | Confidence and how to use it |
|---|---|---|
| **Strong** | 5+ participants spread across multiple segments; a consistent pattern backed by specific, detailed evidence | High: a sound basis for product decisions |
| **Moderate** | 3-4 participants, or support concentrated in a single segment; the pattern is clear but coverage is narrow | Medium: worth acting on while keeping the limits in mind |
| **Emerging** | 1-2 participants; the observation stands out but does not yet form a pattern | Low: a hypothesis to research further, not grounds for a decision |

4. **Write up each theme:**

```
THEME: [interpretive statement]
  Evidence level:   [Strong / Moderate / Emerging]
  Built from codes: [the codes grouped into this theme]
  Backing:
    - P[id] said "[word-for-word quote]"; context: [situation]
    - P[id] said "[word-for-word quote]"; context: [situation]
    - P[id] was seen [behavior]; context: [situation]
  Contradicting observations: [anything that argues against the theme]
  Where it shows up: [the participant segments that exhibit it]
  Connections:      [how it interacts with other themes, if it does]
```

Before you accept a theme, test it:

- It must rest on direct evidence, meaning quotes or observed behaviors, never on inferences.
- Go looking for counter-evidence, the observations that contradict it. If you found none, the theme probably hasn't been challenged hard enough.
- When two themes overlap heavily, either combine them or draw a sharper line between them.

### Phase 4: Turn insights into opportunities

An insight explains what is happening and why. An opportunity says what could be done about it. Map each theme across like this:

```
FROM INSIGHT TO OPPORTUNITY
  The insight:     [what's going on and the reason, taken from one theme]
  Evidence level:  [the theme's rating: Strong / Moderate / Emerging]
  Effect on users: [how it affects them: severity × frequency]
  The opportunity: [what the product team might do in response]
  Kind of opportunity:
    - Pain relief:      take friction away or lessen it
    - Unmet need:       give users a capability they currently lack
    - Delight:          surprise users by exceeding what they expected
    - Efficiency gain:  speed up a workflow they already have, by a meaningful margin
  Confidence:      [how likely it is that the opportunity is real, judged from evidence level plus effect on users]
```

Weigh opportunities on four factors. This is a research-based input to RICE, not a substitute for it.

- **Evidence strength:** stronger themes yield opportunities you can be more confident in.
- **User impact:** severity (how much does it hurt?) × breadth (how many users does it reach?).
- **Strategic alignment:** does the opportunity tie into current OKRs or the product strategy?
- **Feasibility signal:** did users mention or demonstrate workarounds that point toward a solution?

Rank them in this order:

1. Strong evidence with high impact
2. Moderate evidence with high impact
3. Strong evidence with moderate impact

Opportunities backed only by emerging evidence belong on a "further research needed" list, not in the product backlog.

### Phase 5: Package the readout

Shape the synthesis for whoever will read it; different audiences need different formats.

**Full readout**, written for product, design, and anyone with a stake in the research:

```
# [Project name]: Research Synthesis
[date] · prepared by [researcher]

## 1. What we asked and how
[learning goals, research approach, who participated]

## 2. Who we heard from
[segments covered, sample size per segment, gaps we know about]

## 3. Themes, strongest evidence first
  Theme 1: [the theme's interpretive claim] (Strong / Moderate / Emerging)
    [evidence summary, with a few representative quotes]
  Theme 2: ...

## 4. Opportunities, ranked by confidence × impact
  | # | Opportunity (traced to a theme) | Evidence level | Impact       |
  |---|---------------------------------|----------------|--------------|
  | 1 | [description]                   | [level]        | [assessment] |
  | 2 | ...                             |                |              |

## 5. What we recommend
[specific product actions; for each, the evidence it rests on and its confidence level]

## 6. What this research can't tell us
[limitations and caveats: gaps in the sample, constraints of the method]

## 7. Next research questions
[open questions this work surfaced, each paired with a method to pursue it]
```

**Executive summary**, for readers who care about the bottom line more than the methodology:

```
[Project name] research in brief, [Date]

Headline: [the single most important insight, in one sentence]
Based on: [n participants · methods · segments covered]

Three insights that matter most:
| # | Insight   | Backing data point | Confidence (H/M/L) |
|---|-----------|--------------------|--------------------|
| 1 | [insight] | [data point]       | [H/M/L]            |
| 2 | [insight] | [data point]       | [H/M/L]            |
| 3 | [insight] | [data point]       | [H/M/L]            |

Actions we recommend:
| # | Action   | Owner  | Priority (High/Medium/Low) |
|---|----------|--------|----------------------------|
| 1 | [action] | [name] | [priority]                 |
| 2 | [action] | [name] | [priority]                 |

Caveats: [the main limitations, in one sentence]
```

## Mixing qualitative and quantitative evidence

When you have both kinds (for example interview themes alongside survey percentages and analytics), combine them this way:

1. **Numbers establish the "what."** Lead with metrics and survey data to see WHAT is going on: which features go unused, where users drop off, how satisfaction scores look.
2. **Qualitative data explains the "why."** Use interviews and observation to account for WHY those quantitative patterns exist.
3. **Triangulate.** Agreement between qual and quant raises your confidence. Disagreement calls for investigation, and the disagreement is an insight in its own right.
4. **Never use one to "validate" the other.** Qual and quant answer different questions: qual explains motivation and context, quant measures scale and frequency.

## Ground rules

- **NEVER invent participant quotes, observations, or research data.** Each observation, code, and theme has to trace back to source material the user provided.
- **NEVER call findings "statistically significant" unless a quantitative analysis supports it.** What qualitative research yields is thematic patterns rated by evidence strength, never statistical significance.
- **Always show counter-evidence.** When you present a theme, point out the observations that contradict it. Leaving counter-evidence out amounts to fabrication.
- **Label where every element comes from:** `[Study data]` for material taken from the user's research, `[Method scaffolding]` for structure this skill supplies, and `[My interpretation, researcher to confirm]` for your own reading of the evidence.

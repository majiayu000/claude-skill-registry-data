---
name: presentation-engine
description: >
  Activate when the user needs to create conference presentation slides from a
  completed paper. Extracts key content, designs a slide structure, generates
  slide content with speaker notes, and produces a presentation-ready markdown
  file. Supports IS/CS conference formats (15-20 min presentations).
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Presentation Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (presentation-engine)
> **Input:** [paper source], target format: [conference talk / workshop / poster]
> **Output:** presentation.md with [N] slides + speaker notes
> ```

# Presentation Engine

## Core Principle

A conference presentation is NOT a paper read aloud. It's a persuasion exercise:
convince the audience in 15-20 minutes that your research matters, your method is
sound, and your findings are interesting. This engine transforms a paper into a
focused, visually driven presentation with clear narrative flow.

## When to Activate

- User says "create slides", "make a presentation", "conference talk"
- User says "prepare presentation for [venue]", "slide deck"
- After paper acceptance at a conference
- User runs `/generate-slides`

## Prerequisites

- `draft.md` or `latex/paper.tex` exists (complete paper)
- `figures/` directory with generated figures (optional but recommended)

---

## Step 1: EXTRACT Key Content

### From Each Section

Read the paper and extract:

| Section | Extract | Max Slides |
|---------|---------|-----------|
| **Title/Abstract** | Title, authors, affiliations, 1-sentence summary | 1 |
| **Introduction** | Motivation hook, gap, RQ(s) | 2-3 |
| **Theoretical Background** | Key theory/framework, 1-2 core concepts | 1-2 |
| **Methodology** | Method name, key design choices, data summary | 2-3 |
| **Results/Findings** | Top 3-5 findings, key tables/figures | 4-6 |
| **Discussion** | Key implications (2-3), limitations (1-2) | 2-3 |
| **Conclusion** | Main takeaway, future directions | 1 |

### What to Leave Out

- Detailed literature review (one framework slide is enough)
- Methodological minutiae (sampling details, coding tables)
- All limitations (pick the 2 most honest ones)
- Roadmap paragraph
- Most of the related work

---

## Step 2: DESIGN Slide Structure

### Standard Conference Talk (15-20 min, 15-18 slides)

```markdown
## Slide Structure

1. **Title Slide** — Title, authors, affiliations, venue, date
2. **Motivation** — Why should the audience care? (practical hook)
3. **Problem / Gap** — What don't we know? What's missing?
4. **Research Question(s)** — Clear, prominent, memorable
5. **Theoretical Lens** — Key framework (1 visual if possible)
6. **Method Overview** — Approach in 3-5 bullet points + visual
7. **[Method Detail]** — Optional: sample, process, timeline
8. **Results 1** — First major finding (with figure/table)
9. **Results 2** — Second major finding
10. **Results 3** — Third major finding (or synthesis)
11. **[Results 4]** — Optional: additional finding or robustness
12. **Discussion: What This Means** — Interpretation of findings
13. **Implications** — For theory AND practice (split or combined)
14. **Limitations & Future** — Honest, brief, forward-looking
15. **Conclusion / Takeaway** — One memorable message
16. **Thank You / Q&A** — Contact info, paper reference
```

### Short Talk (10 min, 10-12 slides)

Remove slides 6 (method detail), 11 (results 4), and merge 12-13.

### Workshop / Seminar (30-45 min, 25-30 slides)

Add: deeper literature context, method details, additional findings, more
discussion, interactive elements.

---

## Step 3: GENERATE Slide Content

### Format: Markdown Slides

Generate slides in Marp-compatible markdown format:

```markdown
---
marp: true
theme: academic
paginate: true
---

# [Paper Title]
## [Subtitle if applicable]

**[Author 1]**, [Author 2], [Author 3]
[Affiliation(s)]
[Venue] — [Date]

---

# Motivation

[Striking opening statement or statistic]

- [Key trend 1]
- [Key trend 2]
- [Key challenge]

> "[Compelling quote or statistic]" — [Source]

<!-- speaker notes:
Open with the practical relevance. Spend 1 minute here.
Make the audience feel the problem before you state the RQ.
-->

---

# The Gap

What we **know**: [established knowledge, 2-3 points]

What we **don't know**: [specific gap]

Why it **matters**: [consequence of the gap]

<!-- speaker notes:
Transition from what we know to what's missing.
Emphasize why this gap matters for both theory and practice.
-->

---

# Research Question

> **RQ: [Research Question]**

[1-2 sentences contextualizing the question]

<!-- speaker notes:
Pause after showing the RQ. Let the audience read it.
This is the anchor of your entire talk.
-->

---
```

### Slide Design Principles

For each slide:
- **One idea per slide** — never more
- **Maximum 5-6 bullet points** — prefer 3-4
- **Maximum 7 words per bullet** — use fragments, not sentences
- **One figure or table per slide** — large, readable
- **Speaker notes** for every slide — 2-5 sentences of what to say

### Figure Integration

For figures from the paper:
- Reference existing `figures/fig_*.png` files
- Recommend which figures work on slides (some are too detailed)
- Suggest simplifying complex figures for presentation

---

## Step 4: GENERATE Speaker Notes

### Speaker Note Template per Slide Type

**For Motivation slides:**
```
Open with [the hook]. Pause for effect.
Key message: [what the audience should feel/understand].
Transition: "This brings us to the question of..."
Time: ~1 minute
```

**For Results slides:**
```
Present [finding]. Point to [specific part of figure/table].
Explain what this means: [interpretation in plain language].
Connect to RQ: "This tells us that [answer to RQ aspect]."
If asked about [likely question]: [prepared answer].
Time: ~2 minutes per result slide
```

**For Discussion slides:**
```
Summarize: "So what does this mean?"
Key implication: [most important takeaway].
Compare to prior work: "Unlike [Author], we find [contrast/extension]."
Time: ~2 minutes
```

---

## Step 5: SAVE Output

### Output Files

| File | Content |
|------|---------|
| `presentation/presentation.md` | Marp-compatible slide deck with speaker notes |
| `presentation/speaker_notes.md` | Standalone speaker notes (for rehearsal) |
| `presentation/slide_outline.md` | Slide-by-slide outline (for quick reference) |
| `presentation/figures/` | Presentation-optimized figures (if modified) |

### Checkpoint

```
🎤 PRESENTATION READY
━━━━━━━━━━━━━━━━━━━━
Paper: "[Title]"
Format: [Conference talk / Workshop / Seminar]
Slides: [N] slides (~[N] minutes estimated)

Structure:
  1-3:   Introduction & Motivation
  4-5:   Theory & Method
  6-10:  Results
  11-14: Discussion & Implications
  15-16: Conclusion & Q&A

📁 Saved: presentation/

→ Review slides and speaker notes
→ Rehearse with speaker notes (target: [N] min)
→ Render with Marp: marp presentation.md --pdf
```

---

## Error Recovery

- **Paper too long for slot:** Prioritize ruthlessly. Focus on 2-3 findings, not all.
- **No figures in paper:** Generate simple visuals for key findings via figure-engine.
- **Multiple RQs:** Dedicate 1 slide to listing all RQs, then focus the talk on answering the most important one.
- **Paper is in German, talk in English (or vice versa):** Translate key terms, keep framework names in original language.

---

## Integration

| Scenario | Integration |
|----------|-------------|
| After paper acceptance | Natural next step |
| Figure-engine | Generate presentation-specific visuals |
| Writing-engine | Refine speaker note language |
| Submission-engine | Presentation deadline tracking |

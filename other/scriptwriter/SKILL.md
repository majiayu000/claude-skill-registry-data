---
name: scriptwriter
description: Write video ad scripts with full production notes. Creates scene-by-scene breakdowns including dialogue, B-roll suggestions, on-screen text, camera direction, and timing. Outputs individual script files plus combined overview for approval.
---

# Scriptwriter

Write production-ready video ad scripts for social/Meta social content.

## Output Structure

### Individual Script Files (for production)
```
~/clawd/output/{project}-social-content/
├── scripts/
│   ├── 01-{script-name}.md
│   ├── 02-{script-name}.md
│   └── ...
```

### Combined Overview (for approval)
```
├── scripts-overview.md    # All scripts in one doc
```

## Script Template

Each script file follows this structure:

```markdown
# {Brand} Video Ad Script: {Title}

**Duration:** {X} seconds  
**Format:** {Talking head / Screen recording / Animation / Mixed}  
**Aspect Ratio:** {9:16 / 1:1 / 16:9}  
**Funnel Stage:** {TOFU / MOFU / BOFU}  
**Landing Page:** {URL}

---

## 📋 Overview

| Element | Details |
|---------|---------|
| **Hook** | {One-line hook strategy} |
| **Emotion** | {Emotional journey: X → Y → Z} |
| **CTA** | {Call to action} |
| **Tone** | {Voice/energy description} |

---

## 🎬 SCENE 1: HOOK (0:00 - 0:03)

### Shot
- **Type:** {Shot type}
- **Setting:** {Location/background}
- **Energy:** {Mood/energy level}

### Dialogue
> "{Exact words}"

### On-Screen Text
```
{Text that appears on screen}
```

### B-Roll Options
1. {Option 1}
2. {Option 2}

### Direction
- {Camera/performance direction}
- {Timing notes}

---

[Continue for each scene...]

---

## 📝 FULL SCRIPT (Clean Copy)

{Complete script without formatting for teleprompter}

**Word count:** {N} words  
**Reading time:** ~{N} seconds

---

## 🎨 THUMBNAIL CONCEPT

{2-3 thumbnail options with descriptions}

---

## 🎥 PRODUCTION NOTES

{Equipment, recording tips, editing notes}

---

## 📊 VARIATIONS TO TEST

| Element | A | B |
|---------|---|---|
| {Element} | {Version A} | {Version B} |

---

## ✅ PRE-PUBLISH CHECKLIST

- [ ] Audio is clear
- [ ] Captions added
- [ ] End card holds 2+ seconds
- [ ] Landing page works
- [ ] Link in description/comments
```

## Script Structure by Duration

### 15-Second Script (Stories/Reels)
```
[0-2s]  HOOK - Pattern interrupt
[2-8s]  VALUE - One key insight
[8-13s] CTA - Clear next step
[13-15s] END CARD
```

### 25-30 Second Script (Standard)
```
[0-3s]   HOOK - Pattern interrupt
[3-10s]  PROBLEM - Agitate pain point
[10-20s] SOLUTION - Present offer
[20-27s] PROOF + CTA - Social proof + action
[27-30s] END CARD
```

### 45-60 Second Script (Long-form)
```
[0-5s]   HOOK - Strong opening
[5-15s]  PROBLEM - Deep agitation
[15-30s] SOLUTION - Explain transformation
[30-45s] PROOF - Testimonials/results
[45-55s] CTA - Clear call to action
[55-60s] END CARD
```

## Hook Formulas

### Pattern Interrupt
> "If you're still [wrong behavior], you're [consequence]."

### Curiosity Gap
> "I [achieved result] and here's what nobody tells you..."

### Controversial Take
> "Stop [common advice]. Here's what actually works."

### Identity Call-Out
> "This is for [specific person] who [specific situation]..."

### Question Hook
> "Why do [surprising thing] when you could [better alternative]?"

### Result Lead
> "[Company] went from [before] to [after]. Here's how."

## On-Screen Text Guidelines

1. **Keep it short** — 3-5 words max per text element
2. **Reinforce, don't repeat** — Add to dialogue, don't duplicate
3. **Use hierarchy** — Important words bigger/bolder
4. **Time it right** — Appear with dialogue, not before
5. **Position consistently** — Same area throughout video

### Text Styles
```
EMPHASIS: All caps, bold
"Quote style": In quotation marks
Stat/number: Large, accent color
CTA: Arrow or emoji pointing (👇 ➡️)
```

## B-Roll Categories

### Screen Recordings
- Tool interfaces (ChatGPT, Make, etc.)
- Workflow automations running
- Results/dashboards
- Course/product preview

### Talking Head Variations
- Different angles (straight, 3/4)
- Different framings (tight, medium, wide)
- Gestures and reactions

### Stock/Generic
- Person working at laptop
- Team collaboration
- Frustration → success moments
- Abstract tech visuals

### Brand Specific
- Product screenshots
- Customer testimonials (clips)
- Behind-the-scenes
- Event footage

## Emotional Arcs

### TOFU (Awareness)
```
Frustration → Curiosity → Hope
"I'm stuck" → "Wait, what?" → "I could do this"
```

### MOFU (Consideration)
```
Skepticism → Understanding → Confidence
"Does this work?" → "This makes sense" → "I need this"
```

### BOFU (Decision)
```
Hesitation → Trust → Urgency
"Is it worth it?" → "Others got results" → "I should act now"
```

## Pacing Guidelines

| Duration | Words | Pace |
|----------|-------|------|
| 15s | 35-45 | Fast, punchy |
| 30s | 65-80 | Conversational |
| 45s | 100-120 | Room to breathe |
| 60s | 140-160 | Storytelling pace |

**Rule of thumb:** 2.5-3 words per second for natural delivery.

## Workflow

### 1. Receive Brief
From `/social-content-planner` or direct request:
- Ad concept and funnel stage
- Target duration
- Key messaging points
- Landing page
- Brand voice guidelines

### 2. Write Script
- Start with hook (most important)
- Build emotional arc
- Time out each section
- Add B-roll suggestions
- Include on-screen text

### 3. Review & Polish
- Read aloud for timing
- Check word count vs duration
- Ensure CTA is clear
- Verify landing page alignment

### 4. Add Production Notes
- Thumbnail concepts
- A/B test variations
- Equipment suggestions
- Editing notes

### 5. Deliver
- Save individual script file
- Add to overview document
- Send for approval

## File Naming Convention

```
{NN}-{slug}.md

01-free-crash-course.md
02-ai-readiness-quiz.md
03-ai-operator-course.md
04-team-training-case-study.md
```

## Overview Document Structure

```markdown
# {Brand} Social Content Scripts Overview

**Social Content:** {Name}
**Total Scripts:** {N}
**Date:** {YYYY-MM-DD}

---

## Summary

| # | Script | Duration | Funnel | Status |
|---|--------|----------|--------|--------|
| 1 | Free Crash Course | 30s | TOFU | ✅ Ready |
| 2 | AI Readiness Quiz | 25s | TOFU | ✅ Ready |
| 3 | AI Operator Course | 35s | MOFU | ✅ Ready |
| 4 | Team Training | 40s | BOFU | ✅ Ready |

---

## Script 1: Free Crash Course

[Full script content]

---

## Script 2: AI Readiness Quiz

[Full script content]

---

[Continue for all scripts...]
```

## Integration

Works with:
- `/social-content-planner` — Provides creative briefs
- `/creative_director` — Orchestrates full asset creation
- `/ad_designer` — Creates companion image ads
- `/page_designer` — Creates landing pages scripts point to

## Quality Checklist

Before delivering any script:

- [ ] Hook grabs attention in first 3 seconds
- [ ] Emotional arc is clear
- [ ] Dialogue sounds natural (read aloud)
- [ ] Word count matches duration
- [ ] CTA is specific and clear
- [ ] On-screen text reinforces (not duplicates)
- [ ] B-roll suggestions are actionable
- [ ] Thumbnail concepts included
- [ ] A/B variations provided

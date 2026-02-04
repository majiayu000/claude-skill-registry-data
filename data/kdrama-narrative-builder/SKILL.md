---
name: kdrama-narrative-builder
description: Create emotionally compelling murder mystery narratives using Danpyeonsun methodology and K-drama storytelling principles. Designs 3-act dramatic structures, complex morally-gray characters, bittersweet endings, and scene-by-scene emotional beats. Use when writing scenarios for detective games, designing murder mystery plots, or creating K-drama style narratives with moral complexity.
---

# K-Drama Narrative Builder

Create emotionally resonant murder mystery narratives using award-winning Korean storytelling methodology (Danpyeonsun 2024).

## Purpose

This skill applies K-drama narrative principles to murder mystery games:
- Danpyeonsun's 3-act dramatic structure
- Morally complex characters (no pure good/evil)
- Bittersweet, thought-provoking endings
- Emotional beats synchronized with gameplay
- Korean cultural context and corporate themes

## When to Use This Skill

Use this skill when:
- Writing scenarios for murder mystery or detective games
- Designing complex character relationships and motivations
- Creating multiple endings with emotional depth
- Planning scene-by-scene emotional progression
- Adapting K-drama storytelling to interactive games

## Danpyeonsun Success Principles

### 1. Unprecedented Emotional Impact

**Goal**: Create "peak" storytelling moments that players remember

**Techniques**:
- **Emotional Crescendos**: 2-3 high-impact reveals per act
- **Distinctive Voices**: Each character has unique speech patterns, motivations
- **Atmospheric Moments**: Use visual/audio design to amplify emotion

**Web App Application**:
- Scene transitions with dramatic animations
- Character voice-overs (recorded audio clips)
- Dynamic background music shifts

### 2. Perfect Story Structure

**3-Act Framework**:

```
Act 1: Setup (30 min, 25% content)
├─ Introduce mystery (victim, setting, stakes)
├─ Meet suspects (3-5 characters)
├─ Discover first clues (easy puzzles)
└─ Establish emotional connection

Act 2: Confrontation (60 min, 50% content)
├─ Interrogate suspects (AI NPC dialogues)
├─ Collect contradictory evidence
├─ Plot twist (nothing is as it seems)
├─ Moral dilemma emerges
└─ "Dark night of the soul" moment

Act 3: Resolution (30 min, 25% content)
├─ Final clues converge
├─ Truth revealed
├─ Player makes final choice
├─ Ending (5 variations)
└─ Emotional aftermath
```

### 3. Complex Characters (Simple Plot)

**Principle**: Better to have simple plot with rich characters than complex plot with flat characters.

**Character Depth Model**:
- **Surface**: What player sees initially
- **Layer 1**: Revealed through interrogation
- **Layer 2**: Discovered through evidence
- **Core Truth**: Hidden until final revelation

**Example**:
```
Character: CEO (정우진)
├─ Surface: Cold, ruthless businessman
├─ Layer 1: Pressured by board, financial crisis
├─ Layer 2: Protecting company from scandal
└─ Core: Sacrificed ethics to save jobs (moral gray)
```

See `references/character-depth-templates.md` for 10 character arcs.

## K-Drama Storytelling Principles

### Principle 1: Moral Ambiguity (No Black & White)

**Avoid**:
- Pure evil villain
- Perfect hero
- Clear right/wrong choices

**Embrace**:
- Villain with sympathetic motive
- Hero with character flaws
- Choices with trade-offs (save one person, sacrifice another)

**Example from "Secret Forest"**:
```
Prosecutor (protagonist):
- Flaw: Emotionally detached (brain surgery side effect)
- Strength: Unbiased by emotion
- Moral: Is justice without empathy truly justice?
```

### Principle 2: Subtlety & Implication (Not Explicit)

**Show, Don't Tell**:
- Romance: Lingering gazes, not explicit declaration
- Tension: Uncomfortable silences, not shouting
- Guilt: Nervous habits, not confession

**Web App Implementation**:
```typescript
// Instead of: "Character A loves Character B"
// Show through:
- Dialogue choices (protective, jealous)
- Evidence (love letters, photos)
- NPC reactions (blush emoji, pauses)
```

### Principle 3: Bittersweet Endings

**Korean Preference**: Realistic, complex outcomes over purely happy

**Ending Types**:
1. **Pyrrhic Victory**: Justice served, but personal cost
2. **Moral Compromise**: Saved someone, but at ethical price
3. **Incomplete Truth**: Solved crime, but deeper mystery remains
4. **Tragic Irony**: Right choice, wrong reason OR Wrong choice, right reason
5. **Hopeful Ambiguity**: Open-ended, player interprets

## 15-Scene Emotional Arc

**Emotional Beat Progression** (for 120-min game):

| Scene | Time | Act | Emotion | Narrative Purpose |
|-------|------|-----|---------|-------------------|
| 0 | 0-5 min | 1 | Curiosity | Hook (discover victim) |
| 1-2 | 5-15 min | 1 | Intrigue | Meet suspects, gather clues |
| 3-4 | 15-30 min | 1 | Concern | Stakes raised, time pressure |
| 5 | 30-35 min | 2 | Suspicion | First suspect interrogation |
| 6-8 | 35-60 min | 2 | Tension | Contradictions emerge |
| 9 | 60-70 min | 2 | Shock | Plot twist (perspective shift) |
| 10-11 | 70-90 min | 2 | Despair | "No solution" moment |
| 12 | 90-100 min | 3 | Hope | New evidence appears |
| 13 | 100-110 min | 3 | Clarity | Truth becomes clear |
| 14 | 110-120 min | 3 | Resolution | Final choice & ending |

**Key Moments**:
- **Scene 4 → 5 Transition**: "Who can I trust?" (emotional peak 1)
- **Scene 9**: Plot twist (emotional peak 2)
- **Scene 14**: Final revelation (emotional peak 3)

## Scenario Writing Workflow

Copy this checklist:

```
Scenario Development:
- [ ] Step 1: Define core mystery (victim, suspects, truth) [30 min]
- [ ] Step 2: Create character matrix (5 suspects) [45 min]
- [ ] Step 3: Design 3-act structure (15 scenes) [60 min]
- [ ] Step 4: Write scene-by-scene outlines [90 min]
- [ ] Step 5: Design 5 endings (emotional variations) [60 min]
- [ ] Step 6: Write opening scene (hook) [30 min]
- [ ] Step 7: Create dialogue samples (each suspect × 5) [90 min]
- [ ] Step 8: Map evidence to scenes [45 min]
- [ ] Step 9: Review emotional arc consistency [30 min]
- [ ] Step 10: Iterate with narrative-storyteller agent [30 min]
```

**Total time**: ~8 hours for complete scenario

## 5-Suspect Character Matrix

| Character | Role | Surface | Hidden Motive | Truth |
|-----------|------|---------|---------------|-------|
| 이윤아 | Marketing Dir | Professional | Blocked promotion | **KILLER** |
| 박서준 | Coworker | Timid | Bullied by victim | Witness |
| 김민지 | Junior Dev | Emotional | Harassed | Red Herring |
| 최우진 | Investor | Arrogant | Financial pressure | Accomplice |
| 정수아 | Secretary | Loyal | Secret affair | Evidence holder |

**Relationship Web**:
```
     Victim (강대현, CTO)
    /    |    |    |    \
  이윤아  박서준 김민지 최우진 정수아
    ↓     ↓     ↓     ↓     ↓
  Killer Witness Herring Accomplice Holder
```

## Korean Corporate Culture Themes

**Authentic Korean Setting**:
- Office hierarchy (상사/부하)
- After-work culture (회식, 야근)
- Performance pressure (성과주의)
- Workplace politics (파벌, 비리)

**Cultural Details** (makes Korean players connect emotionally):
- Kakaotalk messages (not SMS)
- Soju bottles in trash (post-회식)
- Employee badges (사원증)
- Meeting room names (Korean place names)

See `references/korean-cultural-elements.md`.

## Bittersweet Ending Examples

### Ending 1: "정의의 승리" (Justice Prevails... But)

**Outcome**: Killer arrested, case closed
**Bitterness**: Victim's family destroyed, company bankrupted, innocent coworkers lose jobs
**Player feels**: Victory hollow - justice came at too high a cost
**K-drama parallel**: "Secret Forest" (corruption exposed, but system unchanged)

### Ending 2: "침묵의 합의" (Silent Agreement)

**Outcome**: Player discovers truth but chooses to hide it
**Reason**: Protecting victim's family from scandal OR saving company/jobs
**Player feels**: Morally compromised but pragmatic
**K-drama parallel**: "Stranger" (some truths better left buried)

### Ending 3: "진실의 대가" (The Price of Truth)

**Outcome**: Truth revealed, but player becomes next target
**Consequence**: Killer escapes, player must go into hiding
**Player feels**: Pyrrhic victory, personal sacrifice
**K-drama parallel**: "Signal" (changing past creates new problems)

### Ending 4: "복수의 순환" (Cycle of Revenge)

**Outcome**: Player frames wrong person (red herring)
**Irony**: Innocent person suffers while real killer escapes
**Player feels**: Guilt, realization of rushed judgment
**K-drama parallel**: "Mouse" (creating monsters while hunting them)

### Ending 5: "잠들지 못하는 밤" (Sleepless Nights) - TRUE ENDING

**Outcome**: Full truth revealed - victim's suicide, not murder, but everyone contributed (neglect, pressure, betrayal)
**Revelation**: No single killer, collective responsibility
**Player feels**: Profound sadness, existential weight
**K-drama parallel**: "My Mister" (pain comes from societal structure, not individuals)

**Why This is True Ending**: Most emotionally complex, requires discovering ALL evidence including victim's diary entries that show descent into despair.

## Integration with Game Mechanics

### Emotional Beat → Puzzle Design

Each emotional beat should correspond to puzzle difficulty:

```
Curiosity (Scene 0): Easy puzzle (confidence building)
Suspicion (Scene 5): Medium puzzle (engagement)
Shock (Scene 9): Hard puzzle (matches emotional intensity)
Despair (Scene 11): Very Hard (frustration matches character despair)
Clarity (Scene 13): Easy again (allow completion)
```

### Character Arc → Evidence Discovery

```
이윤아's Character Arc:
├─ Scene 3: Player finds "Helpful colleague" surface evidence
├─ Scene 6: Interrogation reveals "Ambitious, frustrated" layer
├─ Scene 9: Evidence shows "Embezzlement victim" motive
└─ Scene 13: Diary reveals "Driven to desperation" truth
```

## Outsourcing Guide

**When hiring Korean scenario writer** (recommended budget: 1M-2M KRW):

1. **Provide**:
   - This SKILL.md
   - Character matrix template
   - 15-scene structure template
   - Emotional beats guide

2. **Request**:
   - 15 scene narratives (500-800 words each)
   - 5 suspect dialogue samples (10 Q&A each)
   - 5 ending scripts (800-1200 words each)
   - Evidence descriptions (16 items)

3. **Review Criteria**:
   - Moral complexity (no pure villains)
   - Bittersweet tone (avoid Hollywood happy ending)
   - Korean authenticity (cultural details)
   - Emotional arc consistency

Template for writer brief in `references/writer-outsourcing-brief.md`.

## Anti-Patterns

❌ **Exposition Dumps**: Long text blocks explaining everything
✅ **Organic Discovery**: Learn through found documents, overheard dialogue

❌ **Flat Suspects**: One-dimensional villain
✅ **Complex Humans**: Sympathetic killer, flawed witness

❌ **Linear Plot**: Single path to truth
✅ **Branching Discovery**: Multiple paths, player determines pace

❌ **Hollywood Ending**: Perfect justice, everyone happy
✅ **Bittersweet Reality**: Justice exists but personal costs

## Resources

**Danpyeonsun Analysis**: `references/danpyeonsun-methodology.md` - Award-winning techniques
**Character Templates**: `references/character-depth-templates.md` - 10 suspect archetypes
**Emotional Beats**: `references/emotional-progression-guide.md` - Scene-by-scene timing
**Ending Design**: `references/bittersweet-endings-library.md` - 20 ending variations
**Cultural Context**: `references/korean-cultural-elements.md` - Authentic details
**Outsourcing**: `references/writer-outsourcing-brief.md` - Hiring guide

## Success Criteria

Well-crafted K-drama narrative should:
- ✅ Make players question their moral judgments
- ✅ Create empathy for all characters (even killer)
- ✅ Deliver emotional impact through subtlety
- ✅ Feel authentically Korean (not translation)
- ✅ Leave players thinking after game ends
- ✅ Support multiple playthroughs (new insights each time)
- ✅ Integrate puzzles organically (not arbitrary obstacles)
- ✅ Achieve 4.5+ emotional satisfaction rating

---

**Version**: 1.0
**Last Updated**: 2025-01-04
**Author**: K-Drama Narrative Specialist

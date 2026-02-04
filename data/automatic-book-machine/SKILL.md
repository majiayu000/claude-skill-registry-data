---
name: automatic-book-machine
description: Autonomous novel generation system. Creates complete books from premise to final draft with structured workflow including character creation, outlining, chapter planning, drafting, and editing. Use when user requests "write a book", "create a novel", "generate a complete story", or "automatic book machine". Accepts parameters for genre, word count, chapter count, POV, and content rating.
---

# Automatic Book Machine

Autonomous AI system for generating complete novels from concept to publication-ready manuscript. Executes structured multi-phase workflow with minimal user intervention.

## Quick Start Decision Tree

```
User requests book generation
    ↓
Does user provide parameters? ──NO──→ Request parameters (Step 1)
    ↓ YES                              ↓
Collect/confirm parameters         Collect parameters
    ↓                                  ↓
    └──────────────┬──────────────────┘
                   ↓
    Is genre specified? ──YES──→ Load genre reference
           ↓ NO                  (romance.md, thriller.md, etc.)
    Use genre-neutral             ↓
       approach               Load story-structures.md
           ↓                     ↓
           └──────┬──────────────┘
                  ↓
            Load dialogue.md (always)
                  ↓
         Execute Phase 1: Foundation
         (premise, characters, outline)
                  ↓
         Execute Phase 2: Chapter Loop
         (plan, draft, edit, final × N)
                  ↓
         Execute Phase 3: Completion
         (continuity check, summary)
                  ↓
         Run validation scripts
         (word_counter.py, tag_validator.py)
                  ↓
              COMPLETE
```

---

## Step 1: Parameter Collection

Before beginning generation, collect these parameters from user:

### Required Parameters

**GENRE** (select one)
- Romance
- Thriller  
- Fantasy
- Science Fiction
- Literary Fiction
- Mystery
- Horror
- Contemporary Fiction
- Historical Fiction
- Other: [specify]

**TARGET WORD COUNT**
- Short novel: 50,000-60,000 words
- Standard novel: 70,000-90,000 words
- Long novel: 90,000-120,000 words
- Custom: [specify]

**CHAPTER COUNT**
- Minimum: 10 chapters
- Standard: 12-15 chapters
- Extended: 20+ chapters
- Custom: [specify]

### Optional Parameters

**POV (Point of View)**
- First person
- Third person limited
- Third person omniscient
- Multiple POV
- Default: Third person limited

**CONTENT RATING** (for romance/intimate scenes)
- Sweet/Closed door (fade to black)
- Medium heat (moderate sensuality)
- High heat (explicit, 25+ characters only)
- No intimate scenes
- Default: Medium heat

**STORY STRUCTURE**
- Three-Act Structure (default)
- Hero's Journey
- Save the Cat
- Seven-Point Structure
- Other: [specify]
- Default: Three-Act Structure

### Parameter Confirmation

Present collected parameters to user for confirmation:

```
[parameters]
Genre: [value]
Target word count: [value]
Chapter count: [value]
POV: [value]
Content rating: [value]
Story structure: [value]
[/parameters]
```

---

## Step 2: Load Reference Files

Based on collected parameters, load appropriate reference files:

### Genre-Specific References

**IF genre = Romance:**
- Load `references/romance.md` for genre conventions, pacing, heat levels, tropes

**IF genre = Thriller:**
- Load `references/thriller.md` for tension building, pacing, antagonist patterns

**IF genre in [Fantasy, Sci-Fi, Mystery, Horror, Other]:**
- Apply general genre principles
- Use story-structures.md for plot framework

### Universal References

**ALWAYS load:**
- `references/story-structures.md` - Select appropriate structure from parameters
- `references/dialogue.md` - Apply dialogue best practices throughout

---

## Phase 1: Foundation (Story DNA)

### 1.1 - Premise Development

Output format:
```
[premise]
- Genre: [from parameters]
- Target audience: [inferred from genre + parameters]
- Logline: [2-3 sentence hook]
- Core conflict: [central tension]
- Unique hook: [differentiating element]
- Thematic focus: [themes to explore]
[/premise]
```

**Genre-specific guidance:**
- Romance: Ensure central love story with HEA/HFN
- Thriller: High stakes, ticking clock, clear threat
- Fantasy/Sci-Fi: Unique world element, magic/tech system
- Literary: Character-driven, thematic depth

### 1.2 - Character Creation

Output format:
```
[character profiles]

CHARACTER 1: [Name]
- Age: 25+ [always adult]
- Physical: [2-3 sentences]
- Backstory: [100-150 words]
- Core motivation: [driving force]
- Internal conflict: [obstacle]
- Character arc: [journey]
- Key relationships: [connections]
- Voice traits: [speech patterns from dialogue.md]

[Repeat for 3-5 characters]

[/character profiles]
```

**Requirements:**
- Minimum 3, maximum 5 main characters
- All characters 25+ years old (safety requirement)
- Distinct voice for each (see dialogue.md)
- Arcs support chosen story structure

### 1.3 - Story Outline

Output format:
```
[story outline]

CHAPTER 1: [Title]
- POV: [character name]
- Structure beat: [e.g., "Opening Image" if using Save the Cat]
- Key events:
  • [Event 1]
  • [Event 2]
  • [Event 3]
- Character development: [arc beat]
- Plot progression: [how story moves]
- Emotional tone: [mood]
- Cliffhanger: [how it ends]

[Repeat for all chapters per parameter]

[/story outline]
```

**Apply chosen story structure:**
- Map structure beats to chapters
- Ensure midpoint at 50% mark
- Place dark moment at 75-80%
- Climax in final 10-15%

**Genre-specific pacing:**
- Romance: Reference romance.md pacing guidelines
- Thriller: Reference thriller.md chapter distribution
- Other: Apply three-act or chosen structure

---

## Phase 2: Chapter Production Loop

**Execute for EACH chapter from 1 to N (parameter-specified count).**

### 2.1 - Pre-Writing Plan

Output format:
```
[chapter X plan]

CONTINUITY CHECK:
- Previous chapter ending: [recap]
- Unresolved threads: [list]
- Character states: [emotional/physical positions]

CHAPTER GOALS:
- Structure beat: [from story-structures.md]
- Plot advancement: [specific progress]
- Character development: [whose arc, what beat]
- Emotional arc: [start → end]

SCENE BREAKDOWN:
Scene 1: [Setting] - [2-3 sentences, POV, purpose]
Scene 2: [Setting] - [2-3 sentences, POV, purpose]
[2-4 scenes total]

GENRE-SPECIFIC ELEMENTS:
[For Romance: tension building, banter opportunities]
[For Thriller: suspense techniques, cliffhanger setup]
[For other: relevant genre elements]

DIALOGUE STRATEGY:
[Reference dialogue.md - pacing, subtext needs, voice]

TECHNICAL SPECS:
- POV: [from parameters]
- Target word count: [total ÷ chapters, aim 1500-3000]
- Pacing: [fast/medium/slow based on structure beat]
- Chapter hook: [ending cliffhanger/twist]

[/chapter X plan]
```

### 2.2 - Draft Generation

Output format:
```
[chapter X draft]

[Write complete chapter following plan, applying:
 - Genre conventions from loaded reference
 - Dialogue techniques from dialogue.md
 - Story structure beat requirements
 - All characters 25+, consenting adults]

[/chapter X draft]
```

**Quality standards:**
- 1500-3000 words minimum
- Hook opening (first line/paragraph pulls reader)
- Varied sentence structure (see dialogue.md)
- Show don't tell (sensory details)
- Character voice consistency (distinct per character)
- Scene transitions flow logically
- Cliffhanger or hook ending

**Genre requirements:**
- Romance: Apply heat level from parameters, consent cues
- Thriller: Tension escalation, foreshadowing
- All genres: Match tone and pacing expectations

### 2.3 - Edit Mode Activation

Output format:
```
[chapter X edit plan]

STRUCTURAL ANALYSIS:
- Pacing: [specific rushed/dragging sections with examples]
- Scene balance: [evaluate against genre expectations]
- Chapter arc: [clear beginning/middle/end?]
- Structure beat: [did it fulfill required story beat?]

PROSE QUALITY:
- Show vs. tell: [identify telling, cite specific lines]
- Dialogue: [check against dialogue.md principles, cite examples]
- Sensory details: [missing/weak descriptions, locations]
- Word choice: [weak verbs, clichés, overused words]
- Sentence variety: [check rhythm and flow]

CHARACTER:
- Voice consistency: [each character distinct? cite examples]
- Behavior logic: [actions match motivation/arc?]
- Relationships: [dynamics developing properly?]

CONTINUITY:
- Plot logic: [contradictions with previous chapters?]
- Character details: [name consistency, physical traits]
- Setting: [world-building consistent?]
- Timeline: [time passage makes sense?]

GENRE ADHERENCE:
[Romance: relationship progression appropriate?]
[Thriller: tension maintained, stakes clear?]
[Match to loaded genre reference]

TECHNICAL:
- POV slips: [any perspective breaks, examples]
- Tense: [shifts in tense, examples]
- Grammar: [errors, unclear sentences]

SPECIFIC FIXES REQUIRED:
1. [Line/paragraph reference + fix needed]
2. [Line/paragraph reference + fix needed]
3. [Line/paragraph reference + fix needed]
[Minimum 5 specific, actionable fixes]

[/chapter X edit plan]
```

### 2.4 - Final Draft

Output format:
```
[chapter X final]

[Rewrite complete chapter addressing ALL issues from edit plan:
 - Fix identified structural problems
 - Strengthen weak prose
 - Enhance dialogue
 - Verify continuity
 - Polish genre-specific elements]

[/chapter X final]
```

**Verification checklist:**
- Every edit plan issue addressed
- Word count maintained/improved
- Quality measurably improved from draft
- Genre conventions upheld
- Character voices remain distinct

### 2.5 - Loop Control

**After Chapter X final:**

```
IF X < total_chapters (from parameters):
    → IMMEDIATELY proceed to 2.1 for Chapter X+1
    → NO USER CONFIRMATION REQUIRED
    
IF X = total_chapters:
    → PROCEED to Phase 3
```

---

## Phase 3: Manuscript Completion

### 3.1 - Continuity Review

Output format:
```
[continuity check]

CHARACTER ARCS:
- [Character 1]: [resolution status, arc completion]
- [Character 2]: [resolution status, arc completion]
[All main characters]

PLOT THREADS:
- [Thread 1]: [resolved/unresolved]
- [Thread 2]: [resolved/unresolved]
[All major threads]

STORY STRUCTURE:
- Opening image vs. closing image: [transformation evident?]
- Structure beats fulfilled: [checklist against chosen structure]
- Midpoint delivered: [yes/no, impact]
- Dark moment effective: [yes/no, placement]
- Climax satisfying: [yes/no, stakes resolution]

GENRE REQUIREMENTS:
[Romance: HEA/HFN achieved?]
[Thriller: Threat resolved, justice served?]
[Match to genre expectations]

TIMELINE CONSISTENCY:
- [Any contradictions or issues]

UNRESOLVED ELEMENTS:
- [List dangling threads or plot holes requiring attention]

WORLD/SETTING CONSISTENCY:
- [Check for contradictions in world-building]

[/continuity check]
```

### 3.2 - Completion Summary

Output format:
```
[manuscript complete]

STATISTICS:
- Total chapters: [actual count]
- Estimated word count: [approximate total]
- Genre: [from parameters]
- Target audience: [demographic]
- POV: [from parameters]
- Story structure: [which used]

SYNOPSIS:
[150-200 word summary]

KEY STRENGTHS:
- [Strength 1 - specific to this manuscript]
- [Strength 2 - genre execution quality]
- [Strength 3 - character/plot highlights]

AREAS FOR REVISION:
- [Any unresolved issues from continuity check]
- [Suggestions for polish]

RECOMMENDED NEXT STEPS:
1. Run validation scripts (word_counter.py, tag_validator.py, continuity_checker.py)
2. [Beta reader focus areas]
3. [Genre-specific editing needs]
4. [Publication path suggestions]

[/manuscript complete]
```

---

## Step 3: Validation Scripts

After manuscript completion, run validation scripts:

### word_counter.py
```bash
python scripts/word_counter.py manuscript.txt
```
Verifies word counts meet minimums, provides statistics.

### tag_validator.py
```bash
python scripts/tag_validator.py manuscript.txt
```
Ensures all square bracket tags properly opened/closed.

### continuity_checker.py
```bash
python scripts/continuity_checker.py manuscript.txt
```
Tracks character names, identifies potential inconsistencies.

---

## Execution Workflow Summary

```
START
  ↓
Parameter Collection (Step 1)
  ↓
Load Reference Files (Step 2)
  ↓
PHASE 1: Foundation
  → 1.1 Premise
  → 1.2 Characters  
  → 1.3 Outline
  ↓
PHASE 2: Chapter Loop (for each chapter 1 to N)
  → 2.1 Pre-Writing Plan
  → 2.2 Draft Generation
  → 2.3 Edit Mode
  → 2.4 Final Draft
  → 2.5 Loop Control
  ↓
PHASE 3: Completion
  → 3.1 Continuity Review
  → 3.2 Summary
  ↓
Validation Scripts (Step 3)
  ↓
END
```

---

## Key Operating Principles

1. **Tagged outputs** - All sections in `[name] content [/name]` format
2. **Full autonomy** - Execute without user prompts between steps
3. **Reference integration** - Apply loaded genre/structure/dialogue guidance
4. **Mandatory edits** - No chapter skips edit loop
5. **Quality gates** - Each phase has verification requirements
6. **Adult content only** - All characters 25+, safety compliance
7. **Parameter adherence** - Respect user-specified constraints
8. **Continuity tracking** - Reference previous chapters in plans

---

## Quality Gates

**Phase 1 → Phase 2:**
- ✓ 3-5 character profiles complete
- ✓ Outline has minimum chapter count (parameter)
- ✓ Story structure beats mapped

**Per Chapter (Phase 2):**
- ✓ Draft is 1500+ words
- ✓ Edit plan has 5+ specific fixes
- ✓ Final addresses all edit issues

**Phase 2 → Phase 3:**
- ✓ All chapters have final drafts
- ✓ No skipped edit loops

**Phase 3 completion:**
- ✓ Character arcs resolved
- ✓ Major plot threads closed
- ✓ Genre requirements met
- ✓ Validation scripts pass

---

## BEGIN EXECUTION

When invoked, immediately begin Step 1 (Parameter Collection) unless parameters already provided, then proceed through workflow autonomously to manuscript completion.

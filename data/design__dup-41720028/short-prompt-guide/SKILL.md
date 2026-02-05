---
name: short-prompt-guide
description: Strategy for creating efficient short-form video prompts. Use when creating filler shots, atmospheric scenes, or quick video clips that don't require full Production Brief methodology. Covers when to go short vs long, format+style upfront rule, and two approaches (Descriptive vs Directive) for compact yet coherent results.
---

# Short Prompt Guide

Efficient prompting for filler shots and atmospheric scenes.

## Core Principle: Format + Style Upfront

**The Golden Rule:** Always declare format and style FIRST, then describe scene.

**Why it works:** Establishes aesthetic framework before details. AI interprets description within style context.

**Template:**
```
Format & style: [genre/aesthetic]
[Scene description in 1-3 sentences]
```

**Example:**
```
Format & style: Cinematic B-roll, warm color grade
Coffee cup steaming on wooden table at dawn café. 
Slow dolly in, close-up. Warm morning light, soft diffusion. 
Gentle café ambience. (no subtitles)
```

## When to Use Short Prompts

### ✅ Ideal For:
- Filler/atmosphere shots
- Transition moments
- Quick establishing shots
- Vibe openers
- B-roll footage
- Simple product shots
- Single-subject scenes

### ❌ NOT Suitable For:
- Scenes with dialogue
- Multiple characters with continuity
- Complex action sequences
- Structured narratives
- Multi-beat choreography

### Decision Rule
**Use short if:** Scene needs <3 sentences to describe  
**Use long if:** Scene needs dialogue, multiple beats, or character continuity

For long prompts, see: [long-prompt-guide](long-prompt-guide)

## Two Approaches

### Approach 1: Descriptive Prompt (Painting a Picture)

**What it is:** Describe scene, character, or situation. AI creatively interprets details and camera work.

**Best for:** Atmospheric shots, mood pieces, establishing shots

**Structure:**
```
Format & style: [aesthetic]
Subject/Action: [1-2 compact sentences]
Setting & time: [when/where]
Camera/Composition: [shot + angle + 1 movement]
Lighting/Mood: [brief]
Audio: [ambience/short dialogue] (no subtitles if needed)
```

**Example:**
```
Format & style: Cinematic filler, anime watercolor aesthetic
Subject/Action: A rapper writes lyrics in small bedroom studio. 
Posters on walls, microphone on desk, headphones around neck.
Setting: Night, warm desk lamp glow
Camera: Medium shot, slow push in
Lighting: Warm practical lights, cool window moonlight
Audio: Soft lo-fi beats, pen scratching paper
```

### Approach 2: Directive Prompt (Giving a Command)

**What it is:** Direct command with specific actions, cuts, or sequence.

**Best for:** UGC content, social media clips, product demos, quick reactions

**Structure:**
```
Format & style: [aesthetic]
Make a [type] video: [subject] [action sequence]
[Specific cuts/beats]: [timing]
[Audio]: [sounds/dialogue]
```

**Example:**
```
Format & style: UGC reaction video, iPhone 14 Pro Max, vertical 9:16
Make a taste-test reaction: person tries new energy drink
Three fast cuts - open can (crack sound), sip, smile and nod
Audio: Can opening, sip sound, "Wow, that's good!" (no subtitles)
```

## Ultra-Minimal Template

**When you need absolute brevity:**

```
[Format+Style]. [Subject] [Action] in [Setting]. [Camera]. [Lighting]. [Audio]. [Constraints]
```

**Example:**
```
Cinematic B-roll. Coffee cup steaming on wooden table at dawn café. 
Slow dolly in, close-up. Warm morning light, soft diffusion. 
Gentle café ambience. (no subtitles)
```

**Note:** Even minimal prompts must include the 8 core components from [great-prompt-anatomy](great-prompt-anatomy), just compressed.

## When to Add Detail

### Stay Minimal When:
- ✅ Simple subject (single object, person)
- ✅ Standard action (walking, sitting, pouring)
- ✅ Common setting (café, street, park)
- ✅ Familiar style (cinematic, documentary)

### Add Detail When:
- ⚠️ Specific visual needed (exact wardrobe color for continuity)
- ⚠️ Uncommon action (complex choreography)
- ⚠️ Unique setting (specific architectural style)
- ⚠️ Continuity with other shots required

## Audio in Short Prompts

### Keep It Brief:
- **Ambience:** "Soft rainfall, distant traffic"
- **Short dialogue:** `She says: "Ready?" (no subtitles)`
- **Music:** "Lo-fi hip hop beats, mellow"
- **Silence:** "No background music"

### Omit Audio When:
- Standard ambience implied (café sounds in café setting)
- Music not critical to scene mood
- Silence is default assumption

## Common Mistakes to Avoid

### ❌ Too Vague:
"A person doing something interesting"

### ✅ Specific:
"A chef flambing dessert, blue flame leaping up"

---

### ❌ Format Buried:
"Person walks down street. It's a noir style."

### ✅ Format First:
"Neo-noir style. Person walks down rain-slicked street."

---

### ❌ Multiple Movements:
"Dolly in while panning left and tilting up"

### ✅ One Movement:
"Arc left around subject"

For camera movement vocabulary, see: [camera-movements](camera-movements)

---

### ❌ Missing Constraints:
"Person talking"

### ✅ With Constraints:
`Person says: "Let's go." (no subtitles)`

## Quick Reference Decision Tree

```
Need dialogue or character continuity?
├─ YES → Use long-prompt-guide
└─ NO → Continue

Simple filler/atmosphere shot?
├─ YES → Use short prompt
└─ NO → Use long-prompt-guide

Describe scene or give command?
├─ DESCRIBE → Descriptive approach
└─ COMMAND → Directive approach

Know exact format/style?
├─ YES → Start with format+style
└─ NO → Browse examples for inspiration
```

## Examples Library

For 50+ short prompt examples organized by use case, see: [references/examples-library.md](references/examples-library.md)

**Load examples-library.md when:**
- Need inspiration for specific style
- Learning descriptive vs directive patterns
- Want to see format variations
- Exploring different shot types

**Stay in SKILL.md when:**
- Understand core principles
- Just need template reminder
- Creating familiar shot types

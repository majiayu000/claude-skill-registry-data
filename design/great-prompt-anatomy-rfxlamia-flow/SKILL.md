---
name: great-prompt-anatomy
description: Essential framework for creating solid Veo 3 prompts. Use when constructing video prompts, validating prompt completeness, or teaching prompt structure. Defines 8 mandatory components (Subject, Setting, Action, Style/Genre, Camera/Composition, Lighting/Mood, Audio, Constraints) that every prompt must include for professional results.
---

# Great Prompt Anatomy

Every solid Veo 3 prompt requires 8 mandatory components.

## The 8 Must-Have Components

### 1. Subject
**What it is:** Who or what appears in the shot  
**Example:** "A glass of red wine" or "Young couple under umbrella"  
**Why mandatory:** Defines focal point; AI will invent subject if not specified

### 2. Setting
**What it is:** Where and when the scene happens  
**Example:** "White linen tablecloth" or "Rain-soaked cobblestone street at dusk"  
**Why mandatory:** Anchors spatial and temporal context

### 3. Action
**What it is:** What's unfolding in the scene  
**Example:** "Tips over in slow motion" or "She adjusts umbrella, faint smile"  
**Why mandatory:** Drives narrative momentum; static without action

### 4. Style/Genre
**What it is:** Visual aesthetic and mood category  
**Example:** "Cinematic realism" or "Neo-noir with high-contrast shadows"  
**Why mandatory:** Guides AI's aesthetic decisions; consistency requires explicit style

### 5. Camera/Composition
**What it is:** Shot size, angle, and movement  
**Example:** "Close-up, low angle" or "Medium shot with gentle dolly-in"  
**Why mandatory:** Defines cinematography; without this, AI chooses randomly  
**Reference:** Use [camera-movements skill](camera-movements) for movement vocabulary

### 6. Lighting/Mood
**What it is:** Light sources and emotional tone  
**Example:** "Moody with single warm spotlight" or "Soft natural sunlight, muted palette"  
**Why mandatory:** Shapes atmosphere; lighting is 50% of visual impact

### 7. Audio
**What it is:** Dialogue, ambient sound, music cues  
**Formats:**
- Dialogue: `He says: "We don't have much time."`
- Ambience: "Soft string quartet fades into silence"
- Clean frames: Add `(no subtitles)` if dialogue without text overlay wanted  
**Why mandatory:** Sound sells the scene; silence is also a choice that must be specified

### 8. Constraints
**What it is:** Prohibitions or exact requirements  
**Example:** "(no subtitles)" or "exactly six candles on the table"  
**Why mandatory:** Prevents unwanted elements; AI creative unless constrained

## Complete Example

**Basic Prompt (all 8 components):**
```
Close-up, low angle. A glass of red wine tips over in slow motion on a white 
linen tablecloth. Rich burgundy liquid spills and spreads. Lighting: moody, 
with a single warm spotlight. Audio: soft string quartet fades into silence. 
(no subtitles)
```

**Component Breakdown:**
1. ✅ Subject: Glass of red wine
2. ✅ Setting: White linen tablecloth
3. ✅ Action: Tips over in slow motion, liquid spills
4. ✅ Style: (Implied cinematic realism from description)
5. ✅ Camera: Close-up, low angle
6. ✅ Lighting: Moody, single warm spotlight
7. ✅ Audio: Soft string quartet fades to silence
8. ✅ Constraints: (no subtitles)

## Audio Detail Patterns

### Dialogue Format
- Standard: `Character name: "Dialogue text"`
- Example: `She whispers: "Stay a little longer."`

### Ambient Sound
- Be specific: "Hollow wind whistling through ruins" vs generic "wind"
- Layer sounds: "Soft rainfall, muffled footsteps, distant café hum"

### Music
- Describe style and timing: "Soft piano underscore with subtle reverb"
- Note changes: "String quartet fades into silence"

### Silence
- Specify explicitly: "No background music" or "Complete silence"
- Silence is intentional, not default

### Subtitle Control
- Clean frames: Add `(no subtitles)` after dialogue
- Example: `He says: "Perfect timing." (no subtitles)`

## Styling & Realism Controls

**Big-budget drama:**
"Shot on 50mm lens, soft natural light, muted color palette"

**Gritty and raw:**
"Handheld camera shake, harsh fluorescent lighting, visible grain"

**Stylized neo-noir:**
"High-contrast shadows with glowing neon signs, wet reflections"

**Continuity rule:** Repeat same visual cues across multiple prompts for recurring characters and consistent style.

## Validation Checklist

Before releasing prompt, verify:
- [ ] All 8 components present
- [ ] Camera movement uses standardized vocabulary
- [ ] Audio format correct (dialogue with colon)
- [ ] Constraints explicitly stated
- [ ] Style clear and consistent

## When to Read Extended Examples

For detailed examples of each component with variations, see: [references/examples.md](references/examples.md)

**Load examples.md when:**
- Need inspiration for specific component
- Exploring different style approaches
- Learning genre-specific patterns
- Want to see complete prompt variations

**Stay in SKILL.md when:**
- Quick validation needed
- Basic understanding sufficient
- Working with familiar patterns

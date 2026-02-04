---
name: long-prompt-guide
description: Production Brief methodology for complex Veo 3 video scenes. Use when creating scenes with dialogue, character continuity, structured settings, or multi-beat sequences. Provides 11-block framework (Format & Tone, Main Subjects, Wardrobe & Props, Location & Framing, Lighting & Palette, Continuity Rules, Actions & Camera Beats, Montage Plan, Dialogue, Sound & Foley, Finish) for professional, replicable results.
---

# Long Prompt Guide - Production Brief Method

Structured methodology for complex scenes requiring dialogue and continuity.

## When to Use Long Prompts

### ✅ Ideal For:
- Scenes with dialogue
- Multiple characters with continuity
- Structured settings (foreground/midground/background)
- Multi-beat action sequences (>3 beats)
- Recurring characters across shots
- Emotional narrative moments
- Complex choreography

### ❌ NOT Suitable For:
- Simple filler shots
- Quick B-roll
- Atmosphere-only scenes
- Single-subject static shots

### Decision Rule
**Use long if:** Scene needs dialogue OR >3 action beats OR character continuity  
**Use short if:** Scene is simple filler or atmospheric

For short prompts, see: [short-prompt-guide](short-prompt-guide)

## Production Brief Framework

The Production Brief consists of **11 blocks**. Include only relevant blocks - skip non-applicable ones.

### Block 1: Format & Tone (MANDATORY)

**Purpose:** Establish overall genre and emotional direction

**What to include:**
- Genre: Cinematic ad, UGC reaction, music video, mini-scene, documentary
- Tone: Emotional realism, nostalgic, tender, gritty, comedic, suspenseful
- Rhythm: Fast-paced, slow contemplative, rhythmic, atmospheric

**Example:**
```
Format & Tone: Cinematic mini-scene - emotional realism with soft 
romantic rhythm and atmospheric intimacy. Tone: nostalgic, tender, 
immersive.
```

### Block 2: Main Subject(s) (MANDATORY)

**Purpose:** Define characters and their chemistry

**What to include:**
- Number of characters
- Brief physical description (age, key features)
- Relationship dynamic
- Emotional state

**Example:**
```
Main Subject(s): A young couple standing close under one umbrella 
in the rain - their chemistry quiet but electric, eyes locked, 
hesitant smiles.
```

### Block 3: Wardrobe and Props (HIGHLY RECOMMENDED)

**Purpose:** Ensure visual continuity across cuts

**What to include:**
- Specific clothing colors and styles
- Key accessories (jewelry, watches, etc.)
- Props that play narrative role
- Items that reflect light interestingly

**Why critical:** AI must recreate exact wardrobe across multiple shots. Without specifics, colors/styles will vary.

**Example:**
```
Wardrobe and Props: She wears beige trench coat, pearl earrings, 
carries transparent umbrella; he wears navy jacket, white shirt, 
wristwatch reflecting streetlight. Props: umbrella, takeaway coffee 
cup gently steaming.
```

### Block 4: Location & Framing (MANDATORY)

**Purpose:** Establish spatial relationships and composition

**What to include:**
- Specific location with sensory details
- **Foreground elements** (closest to camera)
- **Midground elements** (main action area)
- **Background elements** (depth and context)
- Shot size and angle guidance

**Why critical:** FG/MG/BG structure prevents "floating in void" feeling. Spatial anchoring maintains coherence.

**Example:**
```
Location & Framing: Rain-soaked cobblestone street at dusk outside 
softly glowing café.
Foreground: falling raindrops and bokeh reflections.
Midground: the couple framed beneath the umbrella.
Background: café sign glowing amber, blurred city silhouettes.
Camera alternates between gentle dolly-ins, over-shoulder close-ups, 
and slow ¾ circular arcs to preserve emotional depth.
```

### Block 5: Lighting & Palette (MANDATORY)

**Purpose:** Define visual mood and color consistency

**What to include:**
- Primary light sources (practical, natural, artificial)
- **Color palette** (3-5 specific colors) - COLOR ANCHORS
- Light direction (key, fill, back)
- Atmospheric effects (haze, diffusion, bloom)

**Continuity rule:** Repeat color anchors in every related shot for consistency.

**Example:**
```
Lighting & Palette: Warm café light spilling onto cool blue-gray rain.
Light sources: diffused streetlight key from camera left, amber window 
backlight.
Color anchors: blush pink, amber gold, navy blue, cool gray, ivory 
skin tones.
Soft diffusion lens and wet reflections maintain continuity.
```

### Block 6: Continuity Rules (CRITICAL FOR MULTI-SHOT)

**Purpose:** Lock elements that MUST remain constant across cuts

**What to include:**
- Weather conditions
- Time of day
- Lighting conditions
- Wardrobe (reference Block 3)
- Location atmosphere

**Why critical:** Without explicit rules, AI may change weather, time, or lighting between shots.

**Example:**
```
Continuity Rules: Consistent light rain throughout, dusk lighting 
(blue hour), café window glow always visible in background, wardrobe 
unchanged.
```

### Block 7: Actions & Camera Beats (MANDATORY FOR SEQUENCES)

**Purpose:** Choreograph precise timing of subject actions and camera movement

**Structure:** Time-bounded beats, each with:
- Time range (e.g., 0-4s)
- ONE subject action
- ONE camera movement (from [camera-movements](camera-movements) vocabulary)

**Critical rules:**
- One beat = ONE camera movement (prevent conflicts)
- Use standardized vocabulary
- Subject action paired with camera action
- Timing explicit (avoids ambiguity)

**Example:**
```
Actions & Camera Beats (0-12s):

0-4s - Wide shot: camera slowly pushes in through rain toward 
couple; she adjusts umbrella, faint smile.

4-8s - Medium shot: he reaches for her hand; droplets cascade 
down joined fingers; camera drifts laterally, catching reflection 
of neon light across faces.

8-12s - Close-up: their foreheads gently meet; camera rises 
slightly, focusing on breath mixing in rain-haze before fading 
into soft blur.
```

### Block 8: Montage Plan (OPTIONAL - FOR COMPLEX EDITS)

**Purpose:** Define cut types, pacing, and transitions

**What to include:**
- Cut types (jump cut, match cut, L-cut, J-cut)
- Insert shots (detail emphasis)
- Transitions (whip-pan, flash-frame, crossfade)
- Pacing rhythm (fast/slow)

**Example:**
```
Montage Plan: Three inserts: (raindrop hitting umbrella → fingertip 
touch → smile). Smooth match cuts guided by piano rhythm; final 
0.5-second emotional hold before fade-out. Transitions use natural 
lens flares from passing car headlights.
```

### Block 9: Dialogue (IF APPLICABLE)

**Purpose:** Scripted speech with proper formatting

**Format:** `Character name: "Dialogue text"`

**Options:**
- With subtitles (default)
- Without subtitles: add `(no subtitles)` after dialogue

**Example:**
```
Dialogue:
Whisper (female): "Stay a little longer."
He exhales softly, smiling. (no subtitles)
```

### Block 10: Sound & Foley (HIGHLY RECOMMENDED)

**Purpose:** Layer realistic soundscape

**What to include:**
- **Micro-sounds** (peel, snap, pour, shoe squeak, breath)
- **Ambient audio** (environmental base layer)
- **Music** (if applicable, with timing)
- **Silence** (explicitly note if intentional)

**Why detailed:** Generic "rain sounds" vs "soft rainfall, muffled footsteps, umbrella fabric tension" creates immersion difference.

**Example:**
```
Sound & Foley: Soft rainfall, muffled footsteps on wet cobblestone, 
umbrella fabric tension, faint breath, distant café hum, soft piano 
underscore with subtle reverb.
```

### Block 11: Finish (OPTIONAL - FOR STYLE POLISH)

**Purpose:** Post-processing aesthetic touches

**What to include:**
- Film grain intensity
- Halation (glow around highlights)
- LUT intent (color grading direction)
- Chromatic effects
- Poster frame (final memorable image)

**Example:**
```
Finish: Light film grain, warm halation on highlights, gentle 
chromatic bloom around neon reflections. LUT intent: vintage romance 
with balanced teal-amber contrast. Poster frame: their hands clasped 
beneath umbrella, neon reflections rippling across puddled ground 
like living light.
```

## Progressive Detail Strategy

**Start core, expand as needed:**

### Minimum Viable (4 blocks):
1. Format & Tone
2. Main Subjects
4. Location & Framing
7. Actions & Camera Beats

### Standard (7 blocks):
Add: 3. Wardrobe & Props, 5. Lighting & Palette, 10. Sound & Foley

### Maximum (all 11 blocks):
For flagship content, multi-shot continuity, or client work

## Integration with Other Skills

**Camera movements:** Use [camera-movements](camera-movements) vocabulary in Block 7

**Validation:** Cross-reference with [great-prompt-anatomy](great-prompt-anatomy) to ensure 8 core components present

**Quick scenes:** If scene simpler than expected, fall back to [short-prompt-guide](short-prompt-guide)

## Common Mistakes

### ❌ Vague Timing:
"At some point he smiles"

### ✅ Precise Timing:
"4-8s: he smiles as she touches his hand"

---

### ❌ Multiple Movements Per Beat:
"0-4s: Dolly in while arc left"

### ✅ One Movement Per Beat:
"0-4s: Dolly in" OR "0-4s: Arc left"

---

### ❌ Missing FG/MG/BG:
"They stand on street"

### ✅ Spatial Anchors:
"FG: raindrops, MG: couple, BG: café glow"

---

### ❌ Generic Colors:
"Nice lighting"

### ✅ Color Anchors:
"Amber gold, navy blue, blush pink"

## Complete Examples

For 3-5 full Production Brief implementations with all blocks, see: [references/complete-examples.md](references/complete-examples.md)

For blank template with fill-in guidance, see: [references/production-brief-template.md](references/production-brief-template.md)

**Load examples when:**
- Need to see complete workflow
- Learning Production Brief structure
- Want genre-specific patterns
- Building first long prompt

**Load template when:**
- Ready to create own prompt
- Need structured fill-in guide
- Want step-by-step instructions

**Stay in SKILL.md when:**
- Just need block reminders
- Quick reference for structure
- Understanding methodology

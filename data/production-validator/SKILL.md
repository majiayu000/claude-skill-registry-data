---
name: production-validator
description: >
  AI video pipeline validator for Veo 3 feasibility, 8-second scene chunking, and shot continuity.
  
  USE WHEN: Validating screenplays for AI video generation, chunking scenes into 8-second segments,
  generating continuation prompts, scoring feasibility risk, or adding editing metadata.
  
  PIPELINE POSITION: screenwriter → **production-validator** → imagine/arch-v
  
  INPUT: XML from screenwriter skill (scene tags with duration, action, key_visuals)
  OUTPUT: Enhanced XML with validation, chunks, continuity tags, and Veo 3 prompts
  
  KEY FUNCTIONS:
  - Veo 3 feasibility validation with risk scoring (LOW/MEDIUM/HIGH/CRITICAL)
  - 8-second scene chunking with continuation prompts
  - Shot continuity tagging for editors
  - Technical optimization for AI-friendly alternatives
---

# Production Validator

Validate screenplays for AI video generation feasibility and prepare for Veo 3 production.

## Quick Start Workflow

```
1. RECEIVE screenplay XML from screenwriter skill
2. VALIDATE each scene for Veo 3 feasibility
3. CHUNK scenes >8 seconds into 8s segments
4. GENERATE continuation prompts for each chunk
5. TAG shot continuity relationships
6. OUTPUT validated XML ready for imagine/arch-v
```

## Core Functions

### 1. Feasibility Validation

Score each scene element against Veo 3 capabilities:

**Risk Levels:**
- `LOW` - Veo 3 handles well (single subject, simple motion, standard camera)
- `MEDIUM` - May need iteration (moderate complexity, 2-3 subjects)
- `HIGH` - Likely to fail (complex multi-object motion, text rendering)
- `CRITICAL` - Will fail (impossible physics, conflicting movements)

**Risky Elements Quick Check:**
| Element | Risk | AI-Friendly Alternative |
|---------|------|------------------------|
| Multiple objects in motion | HIGH | Focus on one subject per beat |
| Text/signs visible | HIGH | Remove text, add in post |
| Complex hand gestures | MEDIUM | Simplify to basic poses |
| Dialogue + music together | MEDIUM | Separate into distinct beats |
| Multiple camera movements | CRITICAL | One movement per 8s chunk |
| Character without ref image | MEDIUM | Add detailed visual anchor |
| Rapid scene changes | HIGH | Extend individual beats |

**For full risky elements catalog:** [references/veo3-knowledge-base.md](references/veo3-knowledge-base.md)

### 2. Scene Chunking (8-Second Rule)

Veo 3 generates maximum 8 seconds per clip. Scenes must be chunked:

**Chunking Logic:**
```
IF scene_duration <= 8s:
  → Single chunk (no split needed)
IF scene_duration > 8s AND <= 16s:
  → Split into 2 chunks
IF scene_duration > 16s:
  → Split into ceil(duration/8) chunks
```

**Chunk Structure:**
- Each chunk: 6-8 seconds (prefer 8s for maximum content)
- Continuation setup: End each chunk on clear visual anchor
- Continuation prompt: Reference previous chunk's ending

**For detailed chunking workflow:** [references/chunking-workflow.md](references/chunking-workflow.md)

### 3. Continuity Tagging

Tag shot relationships for editing:

**Shot Relationships:**
- `new` - Fresh scene, no connection to previous
- `continues_from_[id]` - Direct continuation of previous chunk
- `match_cut_from_[id]` - Visual match to previous shot
- `jump_cut_from_[id]` - Same subject, different angle/time

**Transition Types:**
- `hard_cut` - Instant transition (default)
- `dissolve` - Gradual blend (passage of time)
- `fade` - Fade to/from black (scene break)
- `wipe` - Stylized transition

**For continuity system details:** [references/continuity-tagging.md](references/continuity-tagging.md)

### 4. Prompt Optimization

Transform screenplay action into Veo 3-optimized prompts:

**Prompt Structure:**
```
[Shot type + Camera] [Subject description] [Action] [Setting] [Lighting] [Style] [Audio] [Constraints]
```

**Optimization Rules:**
1. ONE camera movement per chunk
2. Subject description in first 50 words
3. Specific cinematic terms (dolly, crane, track)
4. Include audio cues (ambient, SFX, dialogue)
5. Add negative prompts for common issues

**For optimization patterns:** [references/prompt-optimization.md](references/prompt-optimization.md)

---

## Input Format (from screenwriter)

```xml
<scene number="1" duration="30s">
  <slugline>EXT. WASTELAND - DAWN</slugline>
  <location>Wasteland</location>
  <time>Dawn</time>
  <characters>Unit-7</characters>
  <mood>desolate, lonely</mood>
  <key_visuals>
    <visual>post-apocalyptic wasteland</visual>
    <visual>boxy robot with blue optical sensor</visual>
  </key_visuals>
  <action>
Robot rolls across wasteland. Discovers flower between concrete slabs.
  </action>
</scene>
```

## Output Format

```xml
<validated_scene number="1" original_duration="30s">
  <feasibility_check>
    <risk_score>LOW</risk_score>
    <risky_elements>
      <element risk="NONE">Single subject - optimal for Veo 3</element>
    </risky_elements>
    <safe_for_veo3>true</safe_for_veo3>
  </feasibility_check>
  
  <chunks>
    <chunk id="1a" duration="8s">
      <shot_type>establishing</shot_type>
      <shot_relationship>new</shot_relationship>
      <action>Wide establishing shot of post-apocalyptic wasteland...</action>
      <veo3_prompt>
Cinematic establishing shot, wide angle, post-apocalyptic wasteland with ruined 
skyscrapers silhouetted against pale sun, gray dust covering cracked ground, 
thick smog atmosphere, slow dolly forward, golden hour lighting through 
pollution, photorealistic, high detail. Audio: wind howling, distant debris 
settling. negative prompt: no text, no multiple moving objects
      </veo3_prompt>
      <camera_movement>Slow dolly forward</camera_movement>
      <continuation_setup>Camera ends focused on ground-level debris field</continuation_setup>
    </chunk>
    
    <chunk id="1b" duration="8s" continues_from="1a">
      <shot_type>continuation</shot_type>
      <shot_relationship>continues_from_1a</shot_relationship>
      <action>Medium shot: Robot (Unit-7) enters frame...</action>
      <veo3_prompt>
[CONTINUATION] Medium shot, boxy robot with weathered chrome body and glowing 
blue optical sensor rolls across cracked asphalt from left, mechanical treads 
leaving marks in gray dust, slow deliberate movement, same wasteland environment, 
maintain lighting and atmosphere, static camera. Audio: mechanical whirring, 
treads on gravel. negative prompt: no lighting change, no character drift
      </veo3_prompt>
      <camera_movement>Static (robot enters frame)</camera_movement>
      <continuation_setup>Robot reaches pile of rubble</continuation_setup>
    </chunk>
    
    <chunk id="1c" duration="8s" continues_from="1b">
      <shot_type>reveal</shot_type>
      <shot_relationship>continues_from_1b</shot_relationship>
      <action>Close-up: Robot discovers flower...</action>
      <veo3_prompt>
[CONTINUATION] Close-up shot, small yellow flower with delicate petals between 
gray concrete slabs, robot's blue optical sensor visible in frame (slight dilation 
suggesting surprise), weathered metal fingers slowly reaching toward flower, 
shallow depth of field, same golden lighting, intimate moment. Audio: gentle wind, 
mechanical servo whir. negative prompt: no hand distortion, maintain flower detail
      </veo3_prompt>
      <camera_movement>Slow dolly closer to flower</camera_movement>
      <editing_transition>Hold final frame for dissolve</editing_transition>
    </chunk>
  </chunks>
  
  <editing_notes>
    - Chunks 1a-1c flow continuously (24s total)
    - Smooth cuts between chunks (maintain spatial continuity)
    - Final frame (flower close-up) holds for transition to next scene
    - Character consistency: Repeat "boxy robot, weathered chrome, blue optical sensor"
  </editing_notes>
</validated_scene>
```

---

## Validation Workflow

### Step 1: Parse Input
```
RECEIVE XML from screenwriter
EXTRACT: duration, characters, key_visuals, action
VALIDATE: Required fields present
```

### Step 2: Risk Assessment
```
FOR each scene:
  SCAN action for risky elements (see knowledge base)
  CALCULATE risk_score based on element count/severity
  FLAG elements that need optimization
  SUGGEST alternatives for HIGH/CRITICAL elements
```

### Step 3: Chunking
```
IF duration > 8s:
  CALCULATE chunk_count = ceil(duration / 8)
  DISTRIBUTE action across chunks
  ENSURE each chunk has:
    - Clear subject/action
    - One camera movement
    - Continuation setup (except last)
```

### Step 4: Prompt Generation
```
FOR each chunk:
  BUILD veo3_prompt using structure:
    [Camera + Shot] + [Subject] + [Action] + [Setting] + 
    [Lighting] + [Style] + [Audio] + [Negative prompts]
  ADD [CONTINUATION] prefix if continues_from previous
  INCLUDE character description repetition for consistency
```

### Step 5: Continuity Tagging
```
FOR each chunk:
  SET shot_relationship based on connection
  SET camera_movement (ONE per chunk)
  SET continuation_setup (visual anchor for next)
  SET editing_transition if applicable
```

### Step 6: Output
```
GENERATE validated_scene XML
INCLUDE: feasibility_check, chunks, editing_notes
VALIDATE: All chunks ≤8s, all have veo3_prompt
```

---

## Integration with Pipeline

**Receives from:** `screenwriter` (XML with scene, duration, action)

**Feeds into:**
- `imagine` skill - Uses veo3_prompts for still image generation (Path 2)
- `arch-v` skill - Uses continuation metadata, camera movements, audio cues

**Cross-references:**
- `camera-movements` skill - Validates camera movement terminology
- `great-prompt-anatomy` skill - Validates 8 mandatory prompt components
- `long-prompt-guide` / `short-prompt-guide` - Applies appropriate prompt methodology

---

## Success Criteria

- ✅ All scenes chunked into ≤8 second segments
- ✅ Each chunk has continuation instructions
- ✅ Risk scoring for Veo 3 feasibility
- ✅ Clear continuity tags for editing
- ✅ Optimized prompts for each chunk
- ✅ Character consistency maintained via description repetition

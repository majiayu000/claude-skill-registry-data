---
name: nano-banana-prompt-engineer
description: "Craft and improve prompts for Google's Nano Banana Pro (Gemini 3 Pro Image) using the ICS/SCALS framework. Use for \"Nano Banana\", \"Gemini 3 Pro Image\", \"image generation prompt\", fixing failed generations, or multi-image sequences with character consistency."
---

# Nano Banana Pro Prompt Engineer

Transform natural language image requests into production-quality Nano Banana Pro prompts.

## Reference Document

**CRITICAL**: Before crafting any prompt, read `references/nano-banana-prompting-reference.md` for:
- Six essential prompt components with examples
- Technical parameter specifications
- Advanced techniques (pseudo-code variables, perspective blending, intentional imperfection)
- Success rate data by task type
- Troubleshooting guidance

## Core Workflow

### Step 1: Analyze User Request

Extract from user's natural language:
- **Subject**: Who/what is the primary focus
- **Intent**: Product shot, portrait, infographic, art, etc.
- **Quality level**: Quick draft vs. production-ready
- **Special requirements**: Text rendering, character consistency, real-time data

### Step 2: Consult Reference

Read relevant sections from `references/nano-banana-prompting-reference.md`:
- Match intent to template category
- Identify applicable advanced techniques
- Note technical parameters needed

### Step 3: Apply Framework

Structure prompt using six mandatory components:
1. **Subject** — Specific entity with distinguishing details
2. **Action** — What the subject is doing (verb/state)
3. **Location** — Environment/setting context
4. **Composition** — Camera angle, framing, perspective
5. **Lighting** — Illumination physics and mood
6. **Style/Medium** — Artistic rendering mode

### Step 4: Add Technical Parameters

Include as needed:
- Aspect ratio (1:1, 16:9, 9:16, 4:3, 21:9, etc.)
- Resolution (2K for web, 4K for print)
- Camera/lens specs for photorealistic work
- Text in double quotes for text rendering

### Step 5: Apply Advanced Techniques

Select based on task complexity:

| Technique | When to Use |
|-----------|-------------|
| **Pseudo-code variables** | Multi-element scenes, product sequences, preventing attribute drift |
| **Perspective blending** | Surreal art, technical diagrams, layered information |
| **Intentional imperfection** | Photorealism, vintage aesthetics, documentary style |
| **14-image context** | Character consistency, brand identity, style transfer |

### Step 6: Deliver Optimized Prompt

Output format:

```
### Analysis
[1-2 sentences: task type, complexity, key requirements]

### Optimized Prompt
[Complete ready-to-use prompt in code block]

### Technical Notes
- Aspect ratio: [ratio] — [reason]
- Resolution: [size] — [reason]
- Techniques applied: [list]
- Expected success rate: [percentage based on task type]

### Usage Tips
[Any model-specific guidance: silent downgrade warning, text rendering limits, etc.]
```

## Quick Reference: Prompt Patterns

**Product photography:**
```
Subject: [PRODUCT] with [material/texture details]
Composition: [angle], fills [X]% of frame
Lighting: [studio setup], [shadows/highlights]
Background: [surface/color]
Style: [photography style], [resolution]
Constraint: [text/logo requirements]
```

**Portrait/headshot:**
```
Subject: [person description]
Attire: [clothing details]
Pose: [position], [expression]
Background: [backdrop type]
Lighting: [setup], [key/fill/rim]
Style: Photorealistic, [skin detail level]
Technical: [lens], [aperture]
```

**Infographic/diagram:**
```
Task: [type] titled "[TITLE]"
Structure: [sections with labels]
Layout: [arrangement description]
Style: [design style], [color palette]
Text: [font guidance], ensure legibility
```

**Character sequence:**
```
Context: [X] reference images of [CHARACTER]
Instruction: Generate [N]-panel [sequence type]
Panel 1: [shot type], [action], [expression]
Panel 2: [continuation]
...
Consistency: Maintain [specific features]
Style: [unified aesthetic]
```

## Constraints

- **Text limits**: Keep text under 50 words per image; 5-word taglines have ~94% success
- **Character consistency**: Maximum 5 faces reliably maintained
- **Silent downgrade**: Warn user to verify "Thinking..." indicator appears
- **API text**: Enclose in double quotes; uppercase resolution ("4K" not "4k")

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Text garbled | Verify Pro model active; use quotes; reduce text length |
| Waxy/AI look | Add intentional imperfection keywords |
| Attribute drift | Use pseudo-code variables |
| Faces blending | Reduce characters; use reference images |
| Missing elements | Mention early in prompt; use two-pass approach |

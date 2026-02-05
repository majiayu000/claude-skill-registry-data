---
name: tacosdedatos-illustrator
description: Create complete post banner illustrations for tacosdedatos from concept to final image. Use this skill when you need to create a banner image for a new post, generate an illustration that matches the tacosdedatos visual style, or produce publication-ready artwork. This is the main creative orchestration skill that handles the full workflow.
---

# tacosdedatos Illustrator

End-to-end illustration creation for tacosdedatos post banners.

**Required**: Read `agents/shared/illustration-style-guide.md` for modes, colors, templates.

**Related skills**: `image-prompt-writer` (prompt-only), `image-validator` (QA-only), `gemini-imagegen` (API details).

---

## The Creative Workflow

### Phase 1: Discovery

**Gather inputs** (ask if not provided):

| Input | Question |
|-------|----------|
| Post title | What's the article called? |
| Summary | What's it about in 1-2 sentences? |
| Tone | Technical, reflective, playful, personal? |
| Key concept | What ONE idea should the image capture? |

### Phase 2: Creative Direction

**1. Select the illustration mode**

| Content Type | Mode |
|--------------|------|
| Technical tutorial, architecture | Abstract/Geometric |
| Evolution, before/after | Paper-Cut/Layered |
| Reflective, philosophical | Surrealist/Evocative |
| Growth, learning journey | Nature + Tech Fusion |
| Personal narrative | Atmospheric/Cinematic |
| How-to, energetic | Playful Cartoon |
| Data analysis | Data Dashboard |

**2. Identify the visual metaphor**

Don't illustrate literally. Find a metaphor:
- AI agents → orchestra conductor
- Data pipeline → flowing river of shapes
- Learning journey → garden cultivation
- Time management → melting clock

**3. Plan the composition**

- Single focal point
- Generous negative space
- 2-3 accent colors max
- Dark background (usually)

### Phase 3: Prompt Crafting

Use the `image-prompt-writer` skill internally, or craft manually using templates from `illustration-style-guide.md`.

**Prompt structure**:
```
[Style] on [background color].
[Subject/metaphor description].
Colors: [specific hex codes].
Style: [texture, composition notes].
[Negative constraints].
```

**Always include negatives**:
```
no text, no words, no labels, no watermarks, no signatures, no logos
no photorealism, no 3D render, no harsh gradients, no glossy surfaces
```

### Phase 4: Generation

Use the `gemini-imagegen` skill to generate.

**Settings**:
- Model: `gemini-3-pro-image-preview`
- Aspect ratio: `16:9` or `3:2` (landscape)
- Resolution: `2K` (balance of quality/speed)

**CRITICAL**: Save to `/tmp/` with UUID filename for Discord delivery:
```python
import uuid
filename = f"/tmp/{uuid.uuid4()}.jpg"
image.save(filename)
print(f"Image saved to: {filename}")
```

### Phase 5: Validation

Check the generated image against the quality checklist:

- [ ] Fits the selected mode
- [ ] Uses colors from palette
- [ ] Has subtle texture/grain
- [ ] No embedded text
- [ ] Clear visual metaphor
- [ ] Generous negative space
- [ ] Proper aspect ratio (landscape)

**If validation fails**: Iterate with refined prompt. Common fixes:
- Add more specific color hex codes
- Emphasize "no text" in negatives
- Simplify the composition
- Add "subtle grain texture"

### Phase 6: Delivery

Provide the final image with context:

```markdown
## Post Banner: [Title]

**Mode**: [Selected mode]
**Metaphor**: [Visual concept]

Image saved to: /tmp/[uuid].jpg

### Design Rationale
[Explain your creative choices - why this mode, why this metaphor, what the visual elements represent]

### Prompt Used
[Include for reproducibility]
```

---

## Iteration Patterns

### If colors are wrong
Re-prompt with explicit hex codes:
```
Colors MUST be exactly: background #121212, accents #E63946 and #A8DADC
```

### If text appears
Strengthen negatives:
```
Absolutely no text, no letters, no words, no writing, no labels, no numbers
```

### If too cluttered
Simplify prompt:
```
Single focal element only. Generous negative space. Minimal composition.
```

### If style is off
Add texture cues:
```
Subtle risograph grain texture. Flat illustration style. No gradients.
```

---

## Example Workflow

**Request**: "Create a banner for 'Construye tu primer equipo de IA esta tarde'"

**1. Discovery**
- Title: "Construye tu primer equipo de IA esta tarde"
- Summary: Tutorial on building an AI agent team quickly
- Tone: Energetic, practical, empowering
- Key concept: Orchestrating multiple AI agents

**2. Creative Direction**
- Mode: Abstract/Geometric (technical + orchestration theme)
- Metaphor: Conductor's baton directing flowing data streams
- Composition: Baton on left, streams flowing right to binary/music notes

**3. Prompt**
```
Flat digital illustration on very dark background (#121212).
A conductor's baton on the left, directing three flowing wave-like streams that carry musical notes and binary code.
Colors: Crema Nevada (#F1FAEE) for the baton, Azul Niebla (#A8DADC) for the streams, Rojo Fuego (#E63946) for accent marks on the streams.
Style: clean geometric, subtle grain texture, generous negative space, elegant flow.
No text, no words, no photorealism, no 3D render, no harsh gradients.
```

**4. Generate** using gemini-imagegen with 16:9, 2K

**5. Validate** - Check all criteria

**6. Deliver** with rationale

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Literal representation | Visual metaphor |
| Multiple competing focal points | Single clear subject |
| Generic stock style | Specific mode + texture |
| Skip validation | Always check output |
| Forget negative prompts | Include all exclusions |
| Use wrong file path | Always `/tmp/` + UUID |

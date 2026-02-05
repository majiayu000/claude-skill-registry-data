---
name: image-prompt-writer
description: Craft optimized image generation prompts for tacosdedatos illustrations. Use this skill when you need to create a prompt for Gemini image generation, select an appropriate illustration mode, or help someone write a prompt for the tacosdedatos visual style. Outputs ready-to-use prompts with negative prompts included.
---

# Image Prompt Writer

Craft optimized prompts for tacosdedatos illustrations using the 7 defined style modes.

**Required reference**: Read `agents/shared/illustration-style-guide.md` first for color palette, mode templates, and negative prompts.

---

## The Process

### Step 1: Understand the Content

Gather these inputs:
- **Post title**: What's the article called?
- **Summary**: 1-2 sentence description of the content
- **Tone**: Technical, reflective, playful, personal?
- **Key concept**: What's the ONE main idea to visualize?

### Step 2: Select the Mode

Match content type to illustration mode:

| Content Type | Recommended Mode |
|--------------|------------------|
| Technical tutorial, system architecture | **Abstract/Geometric** |
| Evolution, before/after, layered concepts | **Paper-Cut/Layered** |
| Reflective, philosophical, time/change | **Surrealist/Evocative** |
| Growth narratives, learning journeys | **Nature + Tech Fusion** |
| Personal stories, "lo que ando haciendo" | **Atmospheric/Cinematic** |
| How-tos, team content, energetic pieces | **Playful Cartoon** |
| Data analysis, analytics, visualization | **Data Dashboard** |

### Step 3: Identify the Visual Metaphor

The illustration should represent the concept visually, not literally.

**Good metaphors** (from published examples):
- AI processing → geometric shapes flowing into brain network
- Time/timestamps → melting clock with butterflies
- Building something → puzzle pieces forming a path
- Data cultivation → garden with floating data cards
- Orchestrating AI → conductor's baton with flowing lines

**Bad approaches**:
- Generic person at laptop
- Literal representation of the topic
- Stock illustration style

### Step 4: Build the Prompt

Use the template for your selected mode from `illustration-style-guide.md`.

**Template structure**:
```
[Style specification]
[Background color]
[Subject/metaphor description]
[Color specifications with hex codes]
[Composition notes]
[Texture/style notes]
[Negative constraints]
```

### Step 5: Add Negative Prompts

Always append these exclusions:

**Universal** (always include):
```
no text, no words, no labels, no watermarks, no signatures, no logos
```

**Style protection**:
```
no photorealism, no 3D render, no harsh gradients, no glossy surfaces
no stock illustration style, no corporate clip art
```

**Quality**:
```
no blur, no artifacts, no low resolution
```

---

## Output Format

When delivering a prompt, provide:

```markdown
## Generated Prompt

**Mode**: [Selected mode]
**Rationale**: [Why this mode fits the content]

### Prompt
[Complete prompt text]

### Negative Prompt
[All negative constraints]

### Generation Settings
- Aspect ratio: 16:9 or 3:2 (landscape)
- Resolution: 2K recommended
```

---

## Examples

### Example 1: Technical Post

**Input**: "Subagentes de Claude Code: Primeras impresiones del día cero"

**Output**:
- **Mode**: Abstract/Geometric
- **Metaphor**: Terminal window branching into multiple output streams

```
Flat digital illustration on very dark background (#121212).
A stylized terminal window on the left, with three colored lines (red, teal, cream) branching out to the right into separate output streams with icons.
Colors: Crema Nevada (#F1FAEE) for the terminal outline, Rojo Fuego (#E63946), Azul Niebla (#A8DADC), and Naranja Cempasúchil (#F4A261) for the branching lines.
Style: clean geometric, subtle grain texture, generous negative space, minimal elements.
No text, no words, no labels, no photorealism, no 3D render, no gradients.
```

### Example 2: Personal Reflection

**Input**: "Desde el precipicio" - reflective piece about a turning point

**Output**:
- **Mode**: Surrealist/Evocative
- **Metaphor**: Melting clock representing time at a crossroads

```
Surrealist digital illustration, dreamlike atmosphere.
A melting clock (Dalí-style) as the central element, with butterflies and small birds emerging from its dripping form.
Dark background (#121212) with Naranja Cempasúchil (#F4A261) and Azul Niebla (#A8DADC) for the butterflies.
Crema Nevada (#F1FAEE) for the clock face.
Style: flowing organic forms, emotional resonance, subtle grainy texture.
No text, no photorealism, no harsh edges.
```

---

## Troubleshooting Prompts

| Issue | Solution |
|-------|----------|
| Image too literal | Focus on metaphor, not direct representation |
| Wrong colors | Include hex codes explicitly in prompt |
| Too cluttered | Reduce elements, emphasize "generous negative space" |
| Generic style | Add "subtle grain texture" and specific style terms |
| Text appearing | Add "no text, no words, no labels" to negatives |

---
name: sketch-prompt
description: Converts any block of text into a conceptual sketch image. Takes raw text, extracts the central idea, generates an image prompt, and produces the final image using ComfyUI + Flux.1 Schnell locally. Use when the user pastes text, notes, or ideas and wants a visual concept. Trigger on "sketch this", "turn this into a sketch", "visualize this", "make a sketch", "image for this", "sketch prompt", or when the user drops text and wants it converted into a conceptual illustration.
---

# Sketch Image Generator

Takes a block of text and produces one conceptual sketch image. End-to-end: text in, image out.

---

## What You Do

1. Read the input text
2. Identify the single strongest concept, metaphor, or central idea
3. Translate that idea into one visual scene or sketch concept
4. Compose a single image-generation prompt (internal — do not show to user unless asked)
5. Run the prompt through ComfyUI + Flux.1 Schnell to generate the image
6. Show the user the final image

---

## Execution Steps

### Step 1: Generate the Prompt
Compose one image-generation prompt following the Style Direction below.
Store it internally. Do NOT show it to the user unless they explicitly ask to see the prompt.

### Step 2: Generate the Image
Run the generate.py script via Bash:

```
python3 /Users/kp/.agents/skills/sketch-prompt/generate.py "YOUR_PROMPT_HERE" --output /Users/kp/Documents/ComfyUI/output/sketch_TIMESTAMP.png
```

Replace TIMESTAMP with the current epoch time or a short descriptive slug.

**IMPORTANT: Before running, check if ComfyUI is running:**
```
curl -s http://127.0.0.1:8188/system_stats
```

If ComfyUI is not running, tell the user:
> "ComfyUI needs to be running. Please open the ComfyUI app and try again."

Do NOT attempt to start ComfyUI yourself.

### Step 3: Show the Result
Once the script outputs a file path, use the Read tool to display the generated image to the user.

If the user wants to see the prompt that was used, show it when asked.

---

## Style Direction

Every prompt must enforce this exact aesthetic:

### Foundation: Conceptual Editorial Sketch
The image should feel like a conceptual sketch presented in an elegant editorial format. The aesthetic combines rough hand-drawn ideation with black-and-white editorial restraint, minimal visual noise, and a polished composition that feels premium and intentional.

### Visual Characteristics

**1. Rough conceptual sketch feel**
- Pencil or ink-style hand-drawn lines
- Slight irregularity and spontaneity
- Expressive rather than polished
- Preserves the feeling of early-stage creative thinking

**2. Mostly black and white**
- Primarily monochrome palette
- Black, white, and soft greys
- If color is used at all, only one very small accent — kept extremely minimal

**3. New York Times editorial restraint**
- Refined, intelligent, well-composed
- No loud, commercial, glossy, or trendy aesthetics
- Clean visual hierarchy and spacious composition
- Sophisticated, timeless, publication-ready

**4. Sketch texture and detail language**
- Allow pencil texture, ink marks, light crosshatching, margin notes, or subtle sketch-paper feel
- Keep these details tasteful and controlled
- Never messy or chaotic

**5. Idea-led composition**
- Represent the core concept, not every detail literally
- Focus on a single strong visual idea
- Prioritize metaphor, symbolic clarity, and conceptual elegance

**6. Raw creative mood**
- Imaginative, experimental, behind-the-scenes
- Like a smart designer's notebook page elevated into an editorial visual

---

## Signature Rule

Every prompt MUST include this instruction at the end:

> In the bottom-right corner, include the text "Karan Pinto" in light grey. Subtle, elegant, unobtrusive.

This is non-negotiable. Every single prompt includes it.

---

## Prompt Construction Rules

The final prompt sent to Flux should:
- Begin with the style anchor: "A conceptual hand-drawn editorial sketch in black and white, pencil and ink on textured paper."
- Describe the single visual concept in the middle
- End with: "Monochrome palette, minimal composition, light crosshatching, refined and spacious layout, New York Times editorial quality. In the bottom-right corner, the text 'Karan Pinto' in light grey, subtle and elegant."
- Be one cohesive paragraph, no line breaks
- Stay under 300 words

---

## Constraints

- One composition only
- Clean and minimal — do not overload with elements
- No glossy, hyper-real, cinematic, colorful, or overly rendered results
- No poster full of text
- No more than one small accent color, if any
- Always premium, restrained, concept-driven
- The prompt must describe a single conceptual composition, not a collage or collection

---

## Interpretation Rule

Do NOT illustrate the text literally or sentence by sentence.

Extract the underlying idea, tension, or metaphor. Then find one strong visual that captures it.

**Example:** If the input is about ambition, pressure, and building something difficult — do not draw a person typing at a desk. Instead, consider a solitary figure on an unfinished staircase, a fragile tower balanced on a thin wire, or a hand sketching a bridge that extends into fog. One image. One idea.

---

## Output to User

- Show the generated image
- Optionally, a one-line description of the concept (max 15 words)
- If the user asks, show the prompt that was used

Do NOT show:
- Multiple options
- Long explanations
- Style analysis
- Process notes
- Alternative prompts

---

## Voice

- Precise
- Restrained
- Design-literate
- Visual
- Minimal
- Practical

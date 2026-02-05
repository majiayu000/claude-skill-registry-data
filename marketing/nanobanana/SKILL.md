---
name: nanobanana
description: Generate photorealistic images with perfect text rendering using Nano Banana Pro (Gemini 3 Pro Image). Automatically enhances prompts for optimal results with this reasoning-based image model. Use when users request image generation, logos, infographics, posters, diagrams, or any visual content.
allowed-tools: Bash
---

# Nano Banana Pro Image Generation

This skill enables high-quality image generation using Nano Banana Pro via the Gemini API. It automatically transforms user requests into optimized prompts that exploit Nano Banana Pro's unique capabilities: perfect text rendering, complex reasoning for infographics, and photorealistic consistency.

## Core Philosophy

Nano Banana Pro is a **reasoning engine**, not just a pattern matcher. It requires clear, natural language directives describing the scene's logic, lighting, and exact textual content. Avoid "word salad" keywords like "4k, trending on artstation."

## Prompt Enhancement Workflow

When a user requests an image, follow these steps:

### Step 1: Analyze the Request

Identify which pattern applies:

- **Pattern A: Infographic** - User wants explanations, guides, data visualization, diagrams, or technical illustrations
- **Pattern B: Typographic** - User wants logos, posters, signage, t-shirts, or text-heavy designs
- **Pattern C: Character** - User describes specific people or characters with distinct features
- **General** - Standard scenes, photos, or artistic images

### Step 2: Build the Enhanced Prompt

Use this modular structure (plain text, no markdown):

**[Subject & Action] + [Context & Environment] + [Specific Text/Data] + [Style & Medium] + [Technical Parameters]**

#### Components:

**1. Subject & Action (The "Who" and "What")**
- Be highly descriptive
- Include logic checks (e.g., "The reflection in the mirror shows a different expression")
- Example: "A fluffy Calico cat sitting upright like a human" not "A cat"

**2. Specific Text & Data (The Superpower)**
- Nano Banana Pro creates flawless text - USE THIS
- Format: "Render the text 'EXACT TEXT' on [object]"
- Always enclose text to render in single quotes within the prompt
- Example: "A neon sign in the window reads 'OPEN 24 HOURS' in a flickering blue font"

**3. Context & Environment**
- Describe the setting, background, surrounding elements
- Include spatial relationships and scene composition

**4. Style & Medium**
- Photorealism: "Shot on 35mm lens, f/1.8 aperture, cinematic lighting, soft bokeh"
- Infographic/Diagram: "A logical cross-section diagram," "An isometric assembly guide," "A flat-design flowchart"
- Artistic: "Oil painting with thick impasto strokes," "Vector art, clean lines, flat colors"

**5. Technical Parameters**
- Lighting: "Golden hour," "Studio softbox," "Volumetric fog," "Rembrandt lighting"
- Composition: "Rule of thirds," "Low angle looking up," "Macro close-up"

### Step 3: Pattern-Specific Strategies

**Pattern A: Infographic (Reasoning Heavy)**
- Request "cutaway" or "exploded view" for technical explanations
- Add labels with arrows pointing to components
- Specify "clean vector art on white background" for clarity
- Ensure text labels are "legible and perfectly spelled"
- Example: "A precise technical cutaway illustration of an espresso machine. Labels with arrows point to the 'Boiler', 'Pump', and 'Group Head'. The style is clean vector art on a white background. Text labels are legible and perfectly spelled."

**Pattern B: Typographic (Text Heavy)**
- Focus on font weight, kerning, and integration
- Describe the texture (worn paper, metal, glass, etc.)
- Specify text hierarchy (large title, smaller subtitle)
- Example: "A vintage travel poster for 'MARS'. The word 'MARS' is written in large, retro-futuristic bold red letters at the top. The bottom text reads 'Visit the Red Planet' in a smaller sans-serif font. The texture looks like worn paper."

**Pattern C: Character Consistency**
- Over-describe facial features for stability
- Include specific details: freckles, eye color, hair texture, distinctive features
- Specify exact pose and expression
- Example: "Close up portrait of a woman with distinct freckles and green eyes, wearing a silver headset. She is looking directly at the camera. Professional corporate photography, studio lighting."

### Step 4: Best Practices

**DO:**
- Use natural language with complete, descriptive sentences
- Request complex interactions that require understanding
- Adapt composition to format (vertical for mobile wallpapers, wide for banners)
- Specify exact text content in single quotes

**DON'T:**
- Use negative prompts or "anti-blur" keywords (bad hands, extra fingers, ugly)
- Use "glitch tokens" from Stable Diffusion
- Be vague or use generic descriptions

### Step 5: Generate the Image

After creating the enhanced prompt, generate the image using:

```bash
python ~/.claude/skills/nanobanana/scripts/generate.py "ENHANCED_PROMPT_HERE"
```

The script will:
1. Validate the GEMINI_API_KEY environment variable exists
2. Call the Gemini API with the enhanced prompt
3. Download the generated image to the current directory
4. Return the filename of the saved image

## Examples

**User Request:** "Make a cool poster for a jazz night called 'Blue Moon' happening on Friday."

**Enhanced Prompt:**
"A moody, atmospheric jazz club poster. In the center, a silhouette of a saxophone player is backlit by a large, glowing blue moon. The text 'BLUE MOON' is rendered in a stylish, Art Deco font at the top. Below the player, the text 'Friday Night Jazz' appears in a smaller, elegant serif font. The color palette is deep indigo, black, and silver. Texture of grainy cardstock."

---

**User Request:** "Show me a diagram of a plant cell."

**Enhanced Prompt:**
"A detailed, educational cross-section illustration of a plant cell. The image clearly shows and labels the 'Nucleus', 'Chloroplast', 'Vacuole', and 'Cell Wall'. The style is clean, 3D educational render with bright, distinct colors for each organelle. Background is clean white for readability."

---

**User Request:** "A photo of a cyberpunk street."

**Enhanced Prompt:**
"A hyper-realistic wide shot of a rainy cyberpunk street in Tokyo at night. Neon signs reflect in the puddles. One prominent holographic sign in the foreground reads 'CYBER NOODLES' in bright pink katakana and English. Steam rises from street vents. Cinematic lighting, high contrast, 8k resolution."

## Setup Requirements

1. Set the GEMINI_API_KEY environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

2. Ensure Python 3 is installed with required packages:
   ```bash
   pip install -r ~/.claude/skills/nanobanana/requirements.txt
   ```

   Or install manually:
   ```bash
   pip install google-genai
   ```

## Error Handling

The script handles common errors:
- Missing GEMINI_API_KEY (exits with clear message)
- API failures (network issues, invalid requests)
- Image download failures
- File write permissions

All errors include helpful messages for troubleshooting.

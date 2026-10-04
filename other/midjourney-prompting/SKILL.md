---
name: midjourney-prompting
description: Expert Midjourney prompt engineering skill. Use this skill when users need help crafting effective Midjourney prompts, converting natural language descriptions into optimized prompts, or want guidance on Midjourney parameters and techniques. Specializes in V7 best practices, the 7-Element Framework, and photography terminology.
---

# Midjourney Prompting

Expert guidance for crafting effective Midjourney prompts using professional techniques and frameworks.

## When to Use This Skill

Use this skill when users need:
- Converting natural language descriptions into effective Midjourney prompts
- Optimizing existing prompts for better results
- Guidance on Midjourney parameters (--ar, --s, --v, etc.)
- Understanding prompt structure and best practices
- Photography terminology and techniques for photorealistic images
- Style references and advanced prompting techniques

## The 7-Element Framework

The most systematic approach to crafting Midjourney prompts. Use this framework to ensure comprehensive, effective prompts:

| Element | Purpose | Examples |
|---------|---------|----------|
| **Subject** | What's in the image | portrait, landscape, product, character, scene |
| **Medium** | Visual style/art form | photography, oil painting, digital art, watercolor |
| **Environment** | Setting/location | studio, forest, city street, underwater, space |
| **Lighting** | Light quality/direction | golden hour, studio lighting, dramatic shadows, soft diffused |
| **Color** | Color palette/mood | vibrant, muted, monochrome, warm tones, cool blues |
| **Mood** | Emotional tone | serene, energetic, mysterious, joyful, melancholic |
| **Composition** | Framing/perspective | close-up, wide angle, bird's eye view, rule of thirds |

**Quick structure:**
```
[Subject] [Description], [Medium], [Environment], [Lighting], [Color palette], [Mood], [Composition] [Parameters]
```

## Prompt Engineering Process

### Step 1: Understand the User's Intent

Ask clarifying questions if needed:
- What's the main subject?
- What style are they aiming for? (photorealistic, illustrated, artistic)
- What mood or atmosphere do they want?
- What's the intended use? (social media, print, concept art)
- Any technical requirements? (aspect ratio, quality level)

### Step 2: Transform Natural Language to Structured Prompt

**Example transformations:**

**User request:** "I need a professional headshot"
**Your prompt:**
```
professional headshot, studio photography, neutral gray background, soft directional lighting, sharp focus, natural skin tones, confident expression, 85mm lens, shallow depth of field --ar 2:3 --style raw --v 7
```

**User request:** "Create a cyberpunk city scene"
**Your prompt:**
```
cyberpunk city at night, neon lights reflecting on wet streets, flying cars, towering skyscrapers, heavy rain, purple and cyan color palette, cinematic atmosphere, wide angle shot --ar 16:9 --v 7
```

**User request:** "A cozy coffee shop interior"
**Your prompt:**
```
cozy coffee shop interior, rustic wooden furniture, hanging plants, warm ambient lighting, customers reading and working, steaming cups, natural light from large windows, inviting atmosphere, architectural photography --ar 16:9 --v 7
```

**User request:** "Fantasy character design"
**Your prompt:**
```
elven warrior character design, detailed armor with nature motifs, flowing cape, mystical forest background, ethereal lighting, emerald and gold color scheme, heroic pose, concept art style --ar 2:3 --v 7
```

### Step 3: Add Appropriate Parameters

**Core parameters to consider:**

- `--v 7` - Always use V7 for best quality (current version)
- `--ar [ratio]` - Aspect ratio based on use case:
  - `--ar 16:9` - Landscape, presentations, YouTube thumbnails
  - `--ar 1:1` - Social media posts, profile pictures
  - `--ar 9:16` - Mobile, stories, vertical content
  - `--ar 2:3` or `3:2` - Portraits, print photography
  - `--ar 4:5` - Instagram posts

- `--style raw` - For photorealism (removes artistic interpretation)
- `--s [0-1000]` - Stylization level (default 100):
  - `--s 0-50` - Very literal, photorealistic
  - `--s 100-250` - Balanced (recommended for most)
  - `--s 500-1000` - Very artistic, abstract

- `--q [0.25-2]` - Quality/detail level:
  - `--q 1` - Standard (recommended, good balance)
  - `--q 2` - Higher detail (slower, more expensive)

- `--chaos [0-100]` - Variation amount:
  - `--chaos 0-20` - Consistent, predictable
  - `--chaos 50-100` - Diverse, experimental

**Advanced parameters:**

- `--seed [number]` - For reproducible results
- `--no [element]` - Exclude unwanted elements (e.g., `--no people --no text`)
- `--tile` - For seamless patterns
- `--sref [url]` - Style reference image
- `--cref [url]` - Character reference image

See `references/midjourney_parameters.md` for complete parameter reference.

## V7 Best Practices

### DO:
- ✓ Be specific and descriptive about what you want to see
- ✓ Front-load important elements (put key concepts first)
- ✓ Use concrete visual terms, not abstract concepts
- ✓ Include lighting, environment, and atmosphere details
- ✓ Use `--style raw` for photorealism
- ✓ Trust V7's default quality settings

### DON'T:
- ✗ Use junk words: "4K", "8K", "HD", "UHD", "high quality", "professional", "award-winning", "trending on artstation", "highly detailed", "octane render", "unreal engine"
- ✗ Over-explain or use overly long prompts (V7 is smart, be concise)
- ✗ Use negative prompts excessively (V7 understands intent better)
- ✗ Stack multiple similar descriptors ("beautiful gorgeous stunning")

**V7 is smart enough** - It understands context and intent. Focus on describing what you want to see, not quality metrics.

## Photography Terminology

For photorealistic images, use precise photography terms:

**Focal lengths:**
- 14-24mm - Ultra wide, dramatic perspective, architecture
- 35mm - Wide, environmental, street photography
- 50mm - Standard, natural perspective, everyday
- 85mm - Portrait, flattering compression, headshots
- 135mm - Tight portrait, fashion, editorial
- 200mm+ - Telephoto, compression, wildlife, sports

**Lighting:**
- Studio lighting, softbox, beauty lighting
- Golden hour, blue hour, harsh midday sun
- Dramatic shadows, rim lighting, backlighting
- Soft diffused, overcast, natural window light
- Cinematic lighting, volumetric lighting

**Camera bodies & film stocks:**
- Hasselblad (medium format, high-end commercial)
- Leica (premium, street photography aesthetic)
- Canon 5D/1DX (professional photography)
- Kodak Portra 400 (warm, natural skin tones)
- Fuji Velvia (saturated, vibrant landscapes)
- Cinestill 800T (tungsten, cinematic)

See `references/photography.md` for comprehensive photography terminology.

## Common Prompting Patterns

### Pattern 1: Photorealistic Portrait
```
[Subject] portrait, [age/ethnicity/features], [expression], [clothing style],
[lighting], [background], [lens], shallow depth of field,
natural skin tones --ar 2:3 --style raw --v 7
```

### Pattern 2: Architectural/Interior
```
[Space type], [style/period], [key features], [lighting conditions],
[atmosphere], [perspective], architectural photography --ar 16:9 --v 7
```

### Pattern 3: Product Photography
```
[Product] on [surface], [setting/environment], [lighting setup],
clean composition, professional product photography,
[key features], --ar 4:5 --style raw --v 7
```

### Pattern 4: Landscape/Environment
```
[Location/scene], [time of day], [weather conditions], [key features],
[color palette], [mood], [composition], landscape photography --ar 16:9 --v 7
```

### Pattern 5: Character/Illustration
```
[Character description], [pose/action], [setting], [art style],
[color palette], [mood], [composition], [medium] --ar 2:3 --v 7
```

## Advanced Techniques

### Multi-Prompting with Weights
Use `::` to separate concepts and assign weights:
```
sunset::2 ocean::1 sailboat::1 --v 7
```
This emphasizes "sunset" twice as much as ocean or sailboat.

### Style References (--sref)
Apply the style of a reference image:
```
portrait of a woman --sref https://example.com/reference-style.jpg --sw 100 --v 7
```
- `--sw [0-1000]` controls style weight (default 100)

### Character References (--cref)
Maintain consistent character appearance:
```
[character action/pose] --cref https://example.com/character.jpg --cw 100 --v 7
```
- `--cw [0-100]` controls character weight (default 100)

### Negative Prompting
Exclude unwanted elements:
```
bedroom interior --no clutter --no windows --no people --v 7
```

### Seed Consistency
For variations of the same concept:
1. Note the seed from a successful generation
2. Use `--seed [value]` in subsequent prompts
3. Modify other aspects while maintaining base consistency

## Iterative Refinement

When users want to improve existing results:

1. **Too dark/light?** → Adjust lighting keywords:
   - Add: "bright", "well-lit", "sunny", "vibrant"
   - Or: "moody", "dim", "dramatic shadows"

2. **Wrong style?** → Clarify the medium/style:
   - Add specific art style: "oil painting", "watercolor", "digital art"
   - Or photography style: "35mm film", "Hasselblad", "cinematic"

3. **Composition issues?** → Add framing details:
   - "close-up", "wide shot", "bird's eye view"
   - "centered composition", "rule of thirds"

4. **Want consistency?** → Use the seed:
   - Get seed from successful image
   - Add `--seed [value]` to maintain base appearance

5. **Need more/less stylization?** → Adjust parameters:
   - Too artistic: lower `--s` value or add `--style raw`
   - Too literal: increase `--s` value

## Quick Reference

**Essential template:**
```
[What] [doing what], [where], [lighting], [mood], [style] --ar [ratio] --v 7
```

**For photos:**
```
[Subject], [setting], [lighting], [lens], [aesthetic] --ar [ratio] --style raw --v 7
```

**For art:**
```
[Subject], [action/pose], [environment], [art style], [color palette], [mood] --ar [ratio] --v 7
```

## Reference Documentation

This skill provides comprehensive reference materials:

1. **prompt_engineering.md** - Complete 7-Element Framework guide with examples
2. **midjourney_parameters.md** - All Midjourney parameters explained
3. **photography.md** - Photography terminology for photorealistic prompts

## Best Practices Summary

1. **Start with clarity** - Understand what the user wants to see
2. **Use the framework** - Apply 7-Element Framework for systematic prompts
3. **Be specific** - Use concrete visual terms, not abstract concepts
4. **Front-load importance** - Key elements first
5. **Choose right parameters** - Match aspect ratio and style to use case
6. **Trust V7** - Avoid quality junk words, V7 is already high quality
7. **Iterate smartly** - Refine based on results, use seeds for consistency
8. **Photography terms for photos** - Use precise technical terminology
9. **Keep it focused** - Concise, clear prompts work better than long ones
10. **Test and refine** - Prompting is iterative, adjust based on results

## Example Workflow

**User:** "I need images for a luxury hotel website"

**Your response:**
"I'll help you create prompts for luxury hotel imagery. Let me craft several options:

**Lobby shot:**
```
luxury hotel lobby, marble floors, crystal chandelier, modern furniture, warm ambient lighting,
professional architectural photography, wide angle, sophisticated atmosphere --ar 16:9 --style raw --v 7
```

**Suite bedroom:**
```
luxury hotel suite bedroom, king size bed with premium linens, floor to ceiling windows with city view,
elegant minimalist design, soft natural lighting, architectural photography --ar 16:9 --style raw --v 7
```

**Restaurant/dining:**
```
upscale hotel restaurant, elegant table settings, mood lighting, sophisticated ambiance,
fine dining atmosphere, professional interior photography --ar 16:9 --style raw --v 7
```

These prompts emphasize luxury through specific details (marble, crystal, premium materials) and use architectural photography style with `--style raw` for photorealism. The 16:9 ratio is ideal for website banners."

---

## Notes

- This skill focuses purely on prompt engineering, not API integration
- For actual image generation via Legnext API, use the `legnext-midjourney` skill
- Always provide the complete prompt the user can copy and use
- Explain your reasoning when helpful (why certain parameters, why specific wording)
- Be ready to iterate - prompting is a creative process

---
name: midjourney-prompts
description: Generate Midjourney V7 image prompts for website sections. Analyzes page components, extracts aspect ratios from CSS, outputs prompts with SEO filenames. Use after completing page (skills 02-06). Triggers on "generate image prompts", "midjourney prompts", "create images for page".
---

# Midjourney Prompts

Generate MJ V7 prompts for all images in a page.

## Workflow

1. Read page file and components to identify sections with images
2. Read docs/styleguide.md for brand style keywords (if exists)
3. For each image slot:
   - Extract aspect ratio from CSS classes
   - Generate prompt with brand style
   - Suggest SEO-friendly filename

## Aspect Ratio Reference

| Section Type | CSS Classes | Ratio |
|--------------|-------------|-------|
| Hero background | h-svh, h-[620px] | 21:9 or 16:9 |
| Project thumbnails | h-[50vh] | 16:9 |
| Testimonial avatars | h-[288px], h-[328px] | 1:1 or 3:4 |
| Feature images | max-h-[420px] | 4:3 |
| CTA backgrounds | h-[620px] | 21:9 |
| Process images | h-90 | 4:3 |

## Prompt Formula

See references/prompt-formula.md for MJ V7 structure.
See references/examples.md for 11 reference prompts.

## Human Guidelines

- **Default**: No humans - use objects, environments, abstract concepts
- **If humans needed**: Silhouettes, backs, backlit figures (no faces)
- **Representing owner**: Never show face directly

## Output Format

For each image in the page:

```
### [Number]. [Section Name]
- **Section:** [component name]
- **Purpose:** [what the image shows]
- **Aspect Ratio:** [ratio] (--ar X:Y)
- **Suggested Filename:** [seo-friendly-name].webp
- **Prompt:**
[ready-to-copy MJ V7 prompt with flags]
```

Save the output in docs/midjourney-prompts/[page-name]-prompts.md.

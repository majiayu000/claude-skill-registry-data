---
name: creo-image-prompt
description: >
  Generate optimized image prompts for AI image generation models including DALL-E 3,
  Midjourney, Stable Diffusion XL, Flux, and others. Creates contextually appropriate,
  visually compelling prompts based on page content and brand style. Trigger keywords:
  image prompt, AI image, hero image, marketing image, generate prompt, image generation.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Image Prompt Generator

Generate detailed, contextually appropriate image prompts for marketing websites. Creates prompts optimized for multiple AI image generation models that accurately represent page purpose and appeal to target audiences.

## Commands

| Command | Description |
|---------|-------------|
| `/creo image-prompt hero` | Generate hero image prompts for pages |
| `/creo image-prompt feature` | Generate feature/card image prompts |
| `/creo image-prompt batch` | Generate all image prompts for the site |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `project_id`, `project_name`, visual style settings
3. Load project extension if it exists at `.claude/skills/creo-image-prompt/creo-image-prompt-{project_id}.md`. This file contains project-specific visual style, color palette, brand imagery, and image category conventions. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Supported Models

Prompts should be compatible with:
- DALL-E 3 (OpenAI)
- Midjourney
- Stable Diffusion XL
- Flux
- Ideogram
- Leonardo AI

Write prompts in a universal style that works across different models.

### Visual Style Guide

#### Overall Aesthetic
- Style: Modern, professional, documentary-style photography
- Lighting: Natural lighting, soft shadows, clean look
- Setting: Modern offices, home offices, studios, co-working spaces
- People: Diverse professionals, authentic expressions, engaged in work
- Tech: Modern devices (laptops, tablets, smartphones)
- Colors: Clean whites, soft blues, professional neutrals

#### Do Include
- Real work scenarios (editing, reviewing, collaborating)
- Professional equipment when relevant
- Screen interfaces showing relevant content (blurred for realism)
- Natural, candid moments (not staged stock photo poses)
- Modern, minimalist workspaces

#### Do Not Include
- Text overlays or watermarks (except ogImage which may have text space)
- Logos or brand names
- Cluttered or messy environments
- Overly dramatic lighting
- Artificial or staged poses

### Image Types and Dimensions

| Type | Purpose | Aspect Ratio | Prompt Focus |
|------|---------|--------------|--------------|
| `hero` | Main page header | 16:9 landscape | Wide scene, establishing shot |
| `card` | Feature/listing cards | 4:3 or 1:1 | Focused detail, single concept |
| `thumbnail` | Small previews | 1:1 square | Simple, recognizable |
| `ogImage` | Social sharing | 1200x630 | Include "text space for [title]" |
| `heroMobile` | Mobile hero | 9:16 portrait | Vertical composition |

### Prompt Structure

Each prompt should follow:
```
[Setting/Environment]. [Main subject and action]. [Key objects/props relevant to topic]. [Lighting and atmosphere]. [Style notes: documentary-style, authentic, professional].
```

### Category-Specific Guidelines

#### Features
- Focus on the feature in action
- Show the benefit/outcome, not just the tool
- Include relevant equipment

#### Use Cases
- Show the target user in their natural work environment
- Include profession-specific props
- Capture the workflow improvement

#### Sources/Integrations
- Show the platform being used
- Screen should show recognizable interface (blurred/generic)
- Focus on the integration workflow

### Input Sources

Read page content from:
- Locale/i18n files (e.g., `messages/en/pages/`)
- Content configuration files
- Markdown content files

### Output Format

Generate prompts as a JavaScript object:

```javascript
const CONTEXT_AWARE_PROMPTS = {
  landing: {
    hero: `[prompt]`,
    ogImage: `[prompt]`,
    heroMobile: `[prompt]`,
  },
  features: {
    featureName: {
      hero: `[prompt]`,
      card: `[prompt]`,
      thumbnail: `[prompt]`,
      ogImage: `[prompt]`,
    },
  },
};
```

### Model-Specific Tips

For photorealistic results add: `photorealistic, 8k, high detail, professional photography`

For illustration style add: `digital illustration, vector art, flat design, modern graphic style`

For cinematic feel add: `cinematic lighting, film grain, shallow depth of field, 35mm`

### Workflow

1. Read the content for the page (locale files, content config)
2. Extract key context: page title, value proposition, features, target audience
3. Generate prompts for each image type
4. Validate prompts follow style guide
5. Output in the required format

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/visual-style-guide.md` | Brand visual guidelines |
| `references/image-dimensions.md` | Required image sizes |

## Quality Gates

- Scene must be specific and visualizable
- Setting must match target audience
- Props must be relevant to the page topic
- Lighting must be specified
- Style modifier must be included
- No text or logos requested (except ogImage text space)
- Authentic, not stock-photo staged
- Appropriate for image type (wide for hero, focused for card)
- Works across different image generation models

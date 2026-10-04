---
name: gpt-image-prompts
description: "Search and browse 476+ curated GPT-Image-2 prompts across 5 categories. Use when creating image generation prompts, looking for visual style inspiration, or crafting prompts for OpenAI image generation API. Triggers on: 'image prompt', 'gpt image', 'image generation prompt', 'visual style prompt'."
---

# GPT Image Prompt Library

Browse and search a curated collection of 476+ production-tested prompts for GPT-Image-2
(OpenAI image generation), organized by category with example outputs.

Source: [EvoLinkAI/awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts)

## Prompt Database

The full prompt collection is stored as JSON at:
`~/.claude/skills/gpt-image-prompts/references/gpt_image2_prompts.json`

## Usage

### Search by keyword
```bash
cat ~/.claude/skills/gpt-image-prompts/references/gpt_image2_prompts.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
query = '${QUERY}'.lower()
results = [p for p in data if query in json.dumps(p).lower()]
for r in results[:10]:
    print(json.dumps(r, indent=2))
"
```

### Browse by category
```bash
cat ~/.claude/skills/gpt-image-prompts/references/gpt_image2_prompts.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
categories = set()
for p in data:
    if 'category' in p:
        categories.add(p['category'])
print('\n'.join(sorted(categories)))
"
```

## Workflow

1. User asks for image prompt inspiration or wants to generate an image
2. Search the JSON database by keyword, category, or style
3. Present matching prompts with their descriptions
4. Optionally adapt/customize the prompt for the user's specific needs
5. If the user has OpenAI API access, help them call the image generation endpoint

## Categories (5 main)

The collection spans: Product Photography, Lifestyle & Fashion, Architecture & Interior,
Food & Beverage, and Abstract & Artistic styles.

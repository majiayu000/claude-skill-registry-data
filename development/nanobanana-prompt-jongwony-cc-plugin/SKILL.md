---
name: nanobanana-prompt
description: Image generation prompts
---

# Nanobanana Image Generation

Generate high-quality images using nanobanana MCP with Gemini Imagen.

## Core Principle

**"Describe the scene, don't just list keywords."**

Use narrative, descriptive paragraphs with rich context and specific details.

---

## Prompt Workflow

### 1. Clarify Requirements

Use `AskUserQuestion` to gather:
- **Purpose**: website, social media, product, illustration
- **Style**: photorealistic, illustrated, stylized, minimalist
- **Elements**: subject, composition, colors, mood, lighting
- **Specs**: aspect ratio, background (transparent/solid)
- **Text**: exact wording, font style (if applicable)

### 2. Select Strategy

| Use Case | Strategy | Reference |
|----------|----------|-----------|
| Marketing photos | Photorealistic | `references/strategies.md` |
| Icons, stickers | Stylized | `references/strategies.md` |
| Logos, posters | Text Rendering | `references/strategies.md` |
| E-commerce | Product Mockups | `references/strategies.md` |
| Banners | Minimalist | `references/strategies.md` |
| Comics | Sequential Art | `references/strategies.md` |

### 3. Craft Prompt

Apply these principles:
- **Hyper-specificity**: Detail trumps brevity
- **Context**: Explain intended purpose
- **Semantic positivity**: Describe what you want, not what to avoid
- **Cinematic language**: Use photography/artistic terminology

### 4. Generate & Iterate

```
nanobanana generate image mcp or nanobanana edit image mcp.
```

Collect feedback with `AskUserQuestion` and refine.

---

## Quick Checklist

- [ ] Purpose and context defined
- [ ] Visual style specified
- [ ] Key elements described (subject, lighting, mood)
- [ ] Technical specs included (if needed)
- [ ] Narrative description (not keyword list)

---

## References

- **Detailed strategies**: `references/strategies.md`
- **Prompt examples**: `references/EXAMPLE.md`
- **Setup & troubleshooting**: `references/setup.md`

**Search patterns:**
- Photorealistic: `grep "Photorealistic" references/EXAMPLE.md`
- Illustrations: `grep "Illustration" references/EXAMPLE.md`
- Product shots: `grep "Product" references/EXAMPLE.md`

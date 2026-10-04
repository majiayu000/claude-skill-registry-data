---
name: content-generator
description: "AI content generation for blogs, social media, marketing copy. Supports multiple formats, tones, and languages."
triggers:
  - "generate content"
  - "write blog post"
  - "内容生成"
  - "写文章"
  - "marketing copy"
---

# Content Generator

AI-powered content creation for multiple platforms.

## Supported Content Types

| Type | Platform | Length | Tone |
|------|----------|--------|------|
| Blog Post | Website | 1000-3000w | Professional |
| Tweet | Twitter | 280c | Casual |
| LinkedIn | LinkedIn | 1300c | Professional |
| Email | Marketing | 200-500w | Persuasive |
| Product Desc | E-commerce | 100-300w | Sales |

## Usage

### Generate Blog Post

```bash
# From topic
hermes content blog --topic "AI trends 2026" --length 1500

# From outline
hermes content blog --outline outline.md

# With SEO optimization
hermes content blog --topic "Next.js tutorial" --seo --keywords "nextjs,react,tutorial"
```

### Social Media

```bash
# Twitter thread
hermes content twitter --topic "10 coding tips" --format thread

# LinkedIn post
hermes content linkedin --topic "My startup journey" --tone professional

# Instagram caption
hermes content instagram --image product.jpg --tone casual
```

### Marketing Copy

```bash
# Landing page
hermes content landing --product "SaaS Tool" --audience developers

# Email campaign
hermes content email --type welcome --product "Hermes Agent"

# Ad copy
hermes content ad --platform google --product "AI Tools" --keywords "productivity"
```

## Content Styles

- **Professional** — Business, formal
- **Casual** — Conversational, friendly
- **Technical** — Developer-focused
- **Persuasive** — Sales-oriented
- **Storytelling** — Narrative-driven

## SEO Optimization

```bash
# Generate with SEO
hermes content blog --topic "AI tools" \
  --seo \
  --keywords "ai tools,productivity,automation" \
  --meta-description "Best AI tools for 2026"

# Analyze existing content
hermes content analyze article.md --seo
```

## Multi-language

```bash
# Generate in Chinese
hermes content blog --topic "AI趋势" --lang zh

# Translate existing content
hermes content translate article.md --to es,fr,de
```

## Templates

### Blog Post Structure
```markdown
# Title (H1)
## Introduction
## Main Points
### Point 1
### Point 2
### Point 3
## Key Takeaways
## Conclusion
## FAQ
```

### Social Media Thread
```
🧵 Thread: [Topic]

1/ [Hook - attention grabber]

2/ [Main point 1]

3/ [Main point 2]

...

10/ [Conclusion + CTA]
```

## Pitfalls

1. **Fact-checking** — AI may generate inaccurate info, verify facts
2. **Plagiarism** — Run plagiarism check before publishing
3. **Brand Voice** — Customize tone to match brand
4. **Legal Review** — Review marketing copy for compliance

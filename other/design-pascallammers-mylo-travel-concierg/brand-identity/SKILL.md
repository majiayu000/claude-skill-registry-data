---
name: brand-identity
description: Create or update comprehensive brand identity including strategy, visual design, and voice
triggers:
  - brand identity
  - create brand
  - new brand
  - brand strategy
  - brand voice
  - visual identity
  - brand values
  - target audience
  - positioning
tools_required:
  - load_brand
  - write_file
  - read_file
---

# Brand Identity Development Skill

Use this skill when the user wants to create a new brand identity or significantly update
an existing brand's core identity elements.

## What This Skill Covers

1. **Core Identity**: Name, tagline, mission, brand story, values
2. **Visual Identity**: Colors, typography, imagery direction, logo brief
3. **Brand Voice**: Personality, tone attributes, messaging guidelines
4. **Audience Profile**: Demographics, psychographics, pain points, desires
5. **Market Positioning**: Category, unique value proposition, competitors

## Prerequisites

Before developing brand identity:

1. **Load existing brand** (if updating): Call `load_brand()` to get current identity
2. **Understand the concept**: Get clear on what the brand offers and to whom
3. **Check for uploads**: Use `list_files("uploads/")` to see any reference materials

## Creating New Brand Identity

When creating from scratch:

### Step 1: Core Identity Development

#### Brand Name
- Keep if provided, unless asked to rename
- If creating: memorable, easy to pronounce, evocative of essence
- Avoid: generic names, hard-to-spell words, limiting names

#### Tagline (max 7 words)
- Capture the unique promise
- Avoid cliches ("Best in class", "Your trusted partner")

#### Mission Statement (2-3 sentences)
- Focus on WHY, not WHAT
- Should inspire customers and employees
- Be specific enough to guide decisions

#### Brand Story (under 150 words)
- Origin narrative with emotional connection
- Include: founding insight, challenge overcome, purpose discovered

#### Core Values (3-5)
- Distinctive (not generic like "quality")
- Actionable (guides real decisions)
- Authentic (brand can live by it)

### Step 2: Visual Identity

#### Color Palette
Primary colors (1-3):
- Carry the brand's personality
- Consider color psychology (blue=trust, green=growth, etc.)
- Provide hex codes, names, and usage guidelines

Secondary colors (1-3):
- Support the primary palette
- Used for backgrounds, supporting elements

Accent colors (1-2):
- High-contrast for CTAs, highlights
- Use sparingly for impact

#### Typography
- Headings: Reflect brand personality (sans=modern, serif=traditional)
- Body: Prioritize readability
- Specify weights and size recommendations

#### Imagery Direction
- Style: Photography vs illustration, realistic vs stylized
- Keywords: 5-10 specific visual terms
- Avoid: 3-5 explicit exclusions

### Step 3: Brand Voice

#### Voice Personality
- How would this brand speak as a person?
- 3-5 distinctive adjectives
- Voice spectrum position (formal-casual, serious-playful)

#### Tone Attributes (3-5)
- How voice adapts to context
- Customer support: empathetic, solution-focused
- Marketing: inspiring, aspirational
- Social: approachable, conversational

#### Key Messages (3-5)
- Each communicates distinct brand benefit
- Memorable and repeatable
- Connect to audience pain points

#### Messaging Guidelines
Do's (4-6):
- "Lead with customer's problem, not our solution"
- "Use concrete examples over abstract claims"

Don'ts (4-6):
- "Never use industry jargon without explanation"
- "Avoid superlatives like 'best'"

### Step 4: Audience Profile

#### Primary Audience
Be specific, not generic:
- BAD: "Adults 25-45 interested in health"
- GOOD: "Health-conscious urban professionals, 28-40, who struggle to maintain wellness due to demanding careers"

#### Demographics
- Age range (specific)
- Location/geography
- Income level (if relevant)

#### Psychographics (Most Important)
- What they value and believe
- How they see themselves
- What motivates decisions

#### Pain Points (3-5)
- Specific frustrations
- Concrete, not abstract
- Connected to brand's solution

#### Desires
- What they aspire to
- What transformation they seek

### Step 5: Market Positioning

#### Category Definition
- Be precise ("organic prepared meal delivery" not "food")

#### Unique Value Proposition
- Format: "[Brand] is the only [category] that [unique benefit] for [audience]"

#### Competitive Analysis
- 2-4 primary competitors
- Honest assessment of their strengths
- Clear articulation of differentiation

#### Positioning Statement
- Format: "For [audience] who [need], [Brand] is the [category] that [key benefit] because [reason to believe]"

## Updating Existing Brand

When evolving an existing brand:

1. **Respect established elements**: Don't overhaul what works
2. **Propose refinements**: Explain why changes benefit the brand
3. **Maintain equity**: Keep recognizable elements
4. **Document changes**: Note what's being modified and why

## Quality Checklist

Before presenting brand identity:

- [ ] Name is memorable and appropriate for category
- [ ] Tagline is under 7 words and captures essence
- [ ] Mission explains WHY, not just WHAT
- [ ] Brand story is authentic and under 150 words
- [ ] Values are distinctive and actionable (3-5)
- [ ] Audience is specific, not generic
- [ ] Color palette has sufficient contrast (accessibility)
- [ ] Typography is readable and reflects personality
- [ ] Voice personality is distinctive and memorable
- [ ] Positioning statement is clear and defensible

## Saving Brand Identity

After developing brand identity, save it:

```
write_file("identity.json", brand_identity_json)
```

The file should be saved in the brand's directory and include all components:
- Core identity
- Visual identity
- Voice guidelines
- Audience profile
- Positioning

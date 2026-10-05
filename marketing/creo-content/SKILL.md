---
name: creo-content
description: >
  Marketing content strategist that creates compelling copy using JTBD framework,
  customer pain points, and competitive positioning. Generates i18n-ready JSON content
  for landing pages, feature pages, pricing pages, and marketing materials.
  Trigger keywords: marketing copy, content strategy, landing page copy, feature copy,
  pricing copy, JTBD content, i18n content.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Marketing Content Strategy

Create compelling, conversion-focused marketing copy based on customer pain points, JTBD framework, and competitive advantages. Output is i18n-ready JSON for integration with internationalization systems.

## Commands

| Command | Description |
|---------|-------------|
| `/creo content landing` | Generate landing page content |
| `/creo content feature` | Generate feature page content |
| `/creo content pricing` | Generate pricing page content |
| `/creo content <page-type>` | Generate content for any page type |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `project_id`, `project_name`, `project_url`, `locales`, `voice_and_tone`, `content_path`
3. Load project extension if it exists at `.claude/skills/creo-content/creo-content-{project_id}.md`. This file contains project-specific brand voice, tone, target audience, JTBD, pain points, and i18n conventions. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Pain Point Psychology

Customers buy solutions to problems. Identify:
- **Functional pains**: Time wasted, manual work, errors
- **Emotional pains**: Frustration, anxiety, embarrassment
- **Financial pains**: High costs, hidden fees, unpredictable pricing
- **Social pains**: Looking incompetent, missing deadlines

### JTBD Framework

Every piece of content connects to a specific customer job:

```
When [SITUATION/CONTEXT],
I want to [MOTIVATION/ACTION],
So I can [EXPECTED OUTCOME/BENEFIT].
```

### Content Creation Process

#### Step 1: Understand the Context
1. Read the target page/section requirements
2. Identify the primary audience segment
3. Review pain points for that segment
4. Check competitive messaging opportunities

#### Step 2: Apply JTBD Framework
- Who is the customer? (segment)
- What job are they trying to do?
- What pain points block them?
- How does the product solve this?
- What outcome do they achieve?

#### Step 3: Write with Pain-First Structure

Hero Section Formula:
```
[Pain Point / Problem Statement]
       |
[Solution / Promise]
       |
[Key Benefit / Outcome]
       |
[CTA with Value]
```

#### Step 4: Output i18n-Ready JSON

```json
{
  "hero": {
    "badge": "Category Label",
    "headline": "Transform Your Workflow",
    "subheadline": "Detailed value proposition addressing pain points.",
    "cta": {
      "primary": "Start Free",
      "secondary": "See How It Works"
    }
  },
  "features": {
    "title": "Why Teams Choose Us",
    "items": [
      {
        "icon": "globe",
        "title": "Feature Name",
        "description": "Benefit-focused description."
      }
    ]
  }
}
```

### Copywriting Principles

#### Lead with Benefits, Not Features
| Feature | Benefit |
|---------|---------|
| "Fast processing" | "Save 10 hours every week" |
| "99.9% uptime" | "Never miss a deadline" |
| "API access" | "Integrate in minutes, not weeks" |

#### Use Power Words
- Action: Transform, Unlock, Accelerate, Simplify, Automate
- Emotion: Confident, Effortless, Powerful, Seamless
- Results: Instant, Accurate, Professional, Complete

#### Write Scannable Copy
- Headlines: 6-12 words max
- Subheadlines: One clear benefit
- Body: 2-3 sentences per paragraph max
- Bullets: Start with verbs, parallel structure

### Page-Specific Guidelines

#### Homepage
- Goal: Capture attention, establish value, drive signup
- Primary CTA: Start Free Trial
- Secondary CTA: See Demo / Learn More

#### Feature Pages
- Goal: Deep dive into specific capability
- Structure: Problem, Solution, How It Works, Benefits, CTA

#### Pricing Page
- Goal: Convert visitors to paying customers
- Structure: Clear tiers, feature comparison, FAQ, guarantee

#### Use Case Pages
- Goal: Connect with specific audience segment
- Structure: Segment Pain, Our Solution, Success Story, Getting Started

### Anti-Patterns to Avoid

Do not write:
- "Our product is the best in the market"
- "We use advanced AI technology"
- "Sign up now to get started"
- Generic benefits without specifics

Do write:
- "Save 10 hours every week on [task]"
- "95%+ accuracy, verified by independent testing"
- "Start free -- no credit card required"
- Specific outcomes and measurable results

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/pain-points-framework.md` | Customer pain analysis by segment |
| `references/voice-and-tone.md` | Brand voice guidelines |

## Quality Gates

- Every piece of content must address a real customer pain point
- Headlines must lead with benefits, not features
- Content must be scannable (understand value in 5 seconds)
- CTA must be clear and action-oriented
- JSON structure must be valid and i18n-ready
- No jargon -- a non-technical person must understand it
- Competitive advantages must be highlighted
- JTBD alignment must be documented for each section

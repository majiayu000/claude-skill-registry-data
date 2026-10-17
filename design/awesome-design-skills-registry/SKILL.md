---
name: awesome-design-skills-registry
description: Pull and use curated DESIGN.md and SKILL.md files for AI-powered design systems and agentic workflows
triggers:
  - pull a design skill into my project
  - use typeui design skills with cursor
  - get a design system skill file
  - browse available design skills
  - install a design skill for ai agents
  - add a SKILL.md for my design system
  - preview design skills from typeui
  - configure my project with design skills
---

# Awesome Design Skills Registry

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

**awesome-design-skills** is a curated registry of 67 design system skill files optimized for AI-powered agentic tools (Claude Code, Cursor, Codex, Google Stitch). Each skill ships as a folder containing:

- `SKILL.md` — AI-agent instructions (tokens, component rules, accessibility constraints, quality gates)
- `DESIGN.md` — Human-readable design intent, rationale, and implementation notes

Pull any skill into your project with a single command using the [TypeUI CLI](https://github.com/bergside/typeui.sh).

**Official registry:** https://typeui.sh/design-skills

## Installation

### Install TypeUI CLI

The TypeUI CLI is the recommended way to pull design skills:

```bash
npx typeui.sh pull <slug>
```

No installation required — `npx` runs the latest version directly.

Alternatively, install globally:

```bash
npm install -g typeui.sh
```

## Core Commands

### Pull a Design Skill

Pull a specific design skill by slug:

```bash
npx typeui.sh pull glassmorphism
```

This creates a `design-skills/glassmorphism/` folder in your project with:
- `SKILL.md` (AI agent instructions)
- `DESIGN.md` (human documentation)

### List All Available Skills

Browse all 67 skills interactively:

```bash
npx typeui.sh list
```

Outputs a filterable list with slugs, descriptions, and preview URLs.

### Pull Multiple Skills

Pull multiple skills in one command:

```bash
npx typeui.sh pull brutalism glassmorphism claymorphism
```

### Preview Before Pulling

Visit the web gallery to preview styles before pulling:

```bash
# Open in browser
open https://typeui.sh/design-skills
```

Or preview a specific skill:

```bash
open https://typeui.sh/design-skills/glassmorphism
```

## Available Design Skills (67 Total)

### Style Categories

**Modern & Minimalist:**
- `clean` — Clean, minimal design with breathing room
- `flat` — Flat design with bold colors and simple shapes
- `contemporary` — Modern, balanced, accessible
- `elegant` — Refined typography and subtle interactions

**Expressive & Creative:**
- `brutalism` — Bold, raw, unapologetic design
- `glassmorphism` — Frosted glass effects with depth
- `claymorphism` — Soft, tactile, 3D elements
- `gradient` — Vibrant gradients and smooth color transitions
- `artistic` — Asymmetric layouts and creative freedom
- `doodle` — Hand-drawn, playful, sketch-like
- `colorful` — Vibrant, saturated color palettes

**Professional & Enterprise:**
- `enterprise` — Conservative, scalable, accessible
- `corporate` — Professional, trustworthy, structured
- `dashboard` — Data-dense interfaces with clear hierarchy
- `application` — Functional, utilitarian UI patterns

**Specialized:**
- `agentic` — AI-first design patterns for agentic workflows
- `claude` — Claude Code-optimized design tokens
- `bento` — Grid-based card layouts
- `levels` — Gaming-inspired progression UI
- `cafe` — Warm, inviting, community-focused

**Full list of 67 skills:** https://typeui.sh/design-skills

## Using Design Skills with AI Agents

### Claude Code (Claude Desktop)

1. Pull the skill into your project:
```bash
npx typeui.sh pull agentic
```

2. Reference it in your conversation:
```
@design-skills/agentic/SKILL.md

Build a dashboard using this design system
```

3. Claude Code reads `SKILL.md` and generates code following:
   - Color tokens
   - Typography scale
   - Component patterns
   - Accessibility rules
   - Quality gates

### Cursor

1. Pull the skill:
```bash
npx typeui.sh pull glassmorphism
```

2. Add to `.cursorrules` or reference directly:
```
Use the design system defined in design-skills/glassmorphism/SKILL.md
```

3. Cursor applies the design tokens when generating UI code.

### Codex / GitHub Copilot

1. Pull the skill:
```bash
npx typeui.sh pull brutalism
```

2. Open `SKILL.md` in your editor alongside your code files
3. Copilot reads context and suggests components matching the design system

## File Structure

After pulling a skill, your project structure:

```
your-project/
├── design-skills/
│   ├── glassmorphism/
│   │   ├── SKILL.md        # AI agent instructions
│   │   └── DESIGN.md       # Human documentation
│   ├── brutalism/
│   │   ├── SKILL.md
│   │   └── DESIGN.md
│   └── claymorphism/
│       ├── SKILL.md
│       └── DESIGN.md
├── src/
└── package.json
```

## Anatomy of SKILL.md

A typical `SKILL.md` file contains:

### 1. Brand & Mission
```markdown
## Brand & Mission

A design system focused on glass-like surfaces with depth and blur.
```

### 2. Color Tokens
```markdown
## Color Palette

- Primary: hsl(220, 90%, 56%)
- Background: hsl(220, 20%, 10%)
- Surface: hsl(220, 20%, 16%) with 40% opacity
- Border: hsl(0, 0%, 100%) with 10% opacity
```

### 3. Typography
```markdown
## Typography

- Font family: Inter, system-ui, sans-serif
- Scale: 12px, 14px, 16px, 20px, 24px, 32px, 48px
- Line height: 1.5 for body, 1.2 for headings
```

### 4. Component Patterns
```markdown
## Button

- Background: rgba(255, 255, 255, 0.1)
- Backdrop-filter: blur(10px)
- Border: 1px solid rgba(255, 255, 255, 0.2)
- Padding: 12px 24px
- Border-radius: 12px
```

### 5. Accessibility Rules
```markdown
## Accessibility

- WCAG 2.2 AA compliant contrast ratios (4.5:1 for text)
- Keyboard-first navigation (Tab, Enter, Escape)
- Focus visible: 2px solid ring with 2px offset
- ARIA labels on all interactive elements
```

### 6. Quality Gates
```markdown
## Quality Gates

- [ ] All interactive elements keyboard-accessible
- [ ] Color contrast passes WCAG AA
- [ ] Focus states visible
- [ ] Loading states for async actions
- [ ] Error messages actionable and clear
```

## DESIGN.md Overview

`DESIGN.md` is the human companion to `SKILL.md`. It includes:

- **Design Overview:** High-level visual direction
- **Rationale:** Why these tokens/patterns exist
- **References:** Links to inspiration (Dribbble, Behance, etc.)
- **Maintenance Notes:** How to keep the system aligned

Example snippet:

```markdown
## Design Overview

Glassmorphism creates depth through layered, semi-transparent surfaces.
Inspired by Apple's Big Sur and Microsoft Fluent Design.

## Rationale

- Blur effects create visual hierarchy without heavy shadows
- Translucency allows background content to remain contextually visible
- Works well in dark mode with reduced eye strain
```

## Code Examples

### React Component Using Glassmorphism Skill

```tsx
import React from 'react';

export function GlassCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div
      className="glass-card"
      style={{
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: '12px',
        padding: '24px',
      }}
    >
      <h2 style={{ fontSize: '24px', fontWeight: 600, marginBottom: '16px' }}>
        {title}
      </h2>
      {children}
    </div>
  );
}
```

### Tailwind CSS Config for Brutalism Skill

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#FF6B00',
        background: '#FFFFFF',
        text: '#000000',
        border: '#000000',
      },
      fontFamily: {
        sans: ['Space Grotesk', 'monospace'],
        display: ['Space Mono', 'monospace'],
      },
      borderWidth: {
        DEFAULT: '3px',
        thick: '6px',
      },
      boxShadow: {
        brutal: '8px 8px 0 0 #000000',
      },
    },
  },
};
```

### CSS Variables from Enterprise Skill

```css
:root {
  /* Colors */
  --color-primary: hsl(210, 100%, 50%);
  --color-background: hsl(0, 0%, 100%);
  --color-surface: hsl(210, 20%, 98%);
  --color-border: hsl(210, 20%, 88%);
  --color-text: hsl(210, 20%, 14%);

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}
```

## Common Patterns

### Pattern 1: Multi-Skill Projects

Use multiple skills for different sections:

```bash
# Landing page uses Glassmorphism
npx typeui.sh pull glassmorphism

# Dashboard uses Enterprise
npx typeui.sh pull enterprise

# Marketing uses Gradient
npx typeui.sh pull gradient
```

Reference each skill in the appropriate component folder:

```
src/
├── landing/         # Uses design-skills/glassmorphism/SKILL.md
├── dashboard/       # Uses design-skills/enterprise/SKILL.md
└── marketing/       # Uses design-skills/gradient/SKILL.md
```

### Pattern 2: Custom Overrides

Pull a base skill and override specific tokens:

```bash
npx typeui.sh pull clean
```

Edit `design-skills/clean/SKILL.md`:

```markdown
## Color Palette (Customized)

- Primary: hsl(280, 90%, 56%)  /* Changed from blue to purple */
- Background: hsl(0, 0%, 100%)
- Text: hsl(0, 0%, 10%)
```

### Pattern 3: Git Workflow

Commit design skills to your repository:

```bash
git add design-skills/
git commit -m "Add glassmorphism and enterprise design skills"
git push
```

Now all team members and AI agents reference the same design system.

### Pattern 4: Monorepo Setup

Pull skills at the root or per package:

```bash
# Root-level (shared across packages)
npx typeui.sh pull enterprise

# Package-specific
cd packages/web
npx typeui.sh pull glassmorphism

cd ../mobile
npx typeui.sh pull friendly
```

## Configuration

### Custom Output Directory

Specify a custom directory for design skills:

```bash
npx typeui.sh pull glassmorphism --output ./docs/design-system
```

### Environment Variables

If you fork the TypeUI CLI or self-host the registry:

```bash
# .env
TYPEUI_REGISTRY_URL=https://your-registry.com/api
```

Then pull from your custom registry:

```bash
export TYPEUI_REGISTRY_URL=https://your-registry.com/api
npx typeui.sh pull custom-skill
```

## Troubleshooting

### Skill Not Found

If a skill slug is invalid:

```bash
npx typeui.sh pull nonexistent-skill
# Error: Skill "nonexistent-skill" not found in registry
```

**Solution:** List available skills:

```bash
npx typeui.sh list
```

Or browse at https://typeui.sh/design-skills

### Network Timeout

If the registry is unreachable:

```bash
npx typeui.sh pull glassmorphism
# Error: Request timeout
```

**Solution:** Check your internet connection or try again later.

### Permission Denied

If `npx` cannot create the `design-skills/` folder:

```bash
npx typeui.sh pull glassmorphism
# Error: EACCES: permission denied, mkdir 'design-skills'
```

**Solution:** Run with elevated permissions or change directory ownership:

```bash
sudo npx typeui.sh pull glassmorphism
```

Or:

```bash
sudo chown -R $USER:$USER .
npx typeui.sh pull glassmorphism
```

### Stale Cache

If you're seeing outdated skill content:

**Solution:** Clear `npx` cache:

```bash
npx clear-npx-cache
npx typeui.sh pull glassmorphism
```

Or force-reinstall:

```bash
npm install -g typeui.sh@latest
typeui.sh pull glassmorphism
```

## Advanced Usage

### Programmatic Access

If you're building tooling that integrates the registry:

```javascript
import { fetch } from 'node-fetch';

async function fetchSkill(slug) {
  const response = await fetch(`https://typeui.sh/api/skills/${slug}`);
  const data = await response.json();
  return data;
}

const glassmorphism = await fetchSkill('glassmorphism');
console.log(glassmorphism.skill_md); // SKILL.md content
console.log(glassmorphism.design_md); // DESIGN.md content
```

### Creating Custom Skills

Fork the registry and create your own skill:

```bash
git clone https://github.com/bergside/awesome-design-skills.git
cd awesome-design-skills/skills
mkdir my-custom-skill
```

Create `SKILL.md` and `DESIGN.md`:

```markdown
<!-- skills/my-custom-skill/SKILL.md -->
# My Custom Skill

## Brand & Mission
A custom design system for internal tools.

## Color Palette
- Primary: hsl(180, 80%, 50%)
- Background: hsl(0, 0%, 98%)
```

Submit a pull request to add your skill to the registry.

## Integration with Other Tools

### Storybook

Document design tokens in Storybook:

```tsx
// .storybook/preview.tsx
import { SKILL_MD } from '../design-skills/glassmorphism/SKILL.md';

export const parameters = {
  docs: {
    page: () => <Markdown>{SKILL_MD}</Markdown>,
  },
};
```

### Figma Variables

Export design tokens from `SKILL.md` to Figma variables:

```bash
# Use a community plugin or script
npx figma-export design-skills/glassmorphism/SKILL.md
```

### Design Linter

Lint your codebase against `SKILL.md` rules:

```bash
npx design-lint --skill design-skills/enterprise/SKILL.md src/
```

(Example tool — replace with your preferred linter)

## Best Practices

1. **Commit design skills to version control** — Keep design and code in sync
2. **Reference SKILL.md in AI agent prompts** — Use `@design-skills/slug/SKILL.md` in Cursor/Claude
3. **Update DESIGN.md when you override tokens** — Document why you diverged
4. **Use one skill per product area** — Landing (Glassmorphism), Dashboard (Enterprise), Docs (Clean)
5. **Pull skills early in the project** — Establish design foundations before building components

## Resources

- **Registry:** https://typeui.sh/design-skills
- **GitHub:** https://github.com/bergside/awesome-design-skills
- **CLI:** https://github.com/bergside/typeui.sh
- **Awesome Badge:** [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

## License

MIT License — See [LICENSE](https://github.com/bergside/awesome-design-skills/blob/main/LICENSE)

---

**When to use this skill:**

- You need a design system for AI agents (Claude Code, Cursor, Codex)
- You want consistent design tokens across your project
- You're building with agentic workflows and need design constraints
- You want to preview and pull pre-built design systems quickly

**Quick reference:**

```bash
# Pull a skill
npx typeui.sh pull glassmorphism

# List all skills
npx typeui.sh list

# Preview in browser
open https://typeui.sh/design-skills
```

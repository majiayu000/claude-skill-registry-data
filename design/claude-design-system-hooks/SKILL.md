---
name: claude-design-system-hooks
description: AI-powered design-to-code engine that generates production-ready UI components from natural language using Claude API
triggers:
  - generate a design system with Claude
  - create UI components from description
  - build responsive layouts with AI
  - convert design mockups to code
  - use Claude for design automation
  - generate accessible components
  - create design tokens automatically
  - build component library with AI
---

# Claude Design System Hooks

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## What This Project Does

Claude Design System Hooks is a neuro-adaptive design orchestration engine that transforms natural language descriptions into production-ready UI code. It bridges Claude AI's cognitive capabilities with multi-framework code generation, allowing you to create entire design systems, component libraries, and responsive UI patterns through conversational prompts.

Key capabilities:
- **Design-as-Dialogue**: Describe UIs in natural language, get framework-specific code
- **Multi-Framework Output**: Generate identical designs in React, Vue, Angular, or vanilla HTML/CSS
- **Design Token Extraction**: Automatically parse color palettes, typography, spacing from specs
- **Accessibility-First**: Built-in WCAG 2.2 compliance checks during generation
- **Plugin Ecosystem**: Extend with Figma sync, Storybook integration, A11y auditing

## Installation

### Prerequisites

```bash
# Requires Node.js 18.x or higher
node --version  # should be >= 18.0.0

# Requires npm 10.x or higher
npm --version  # should be >= 10.0.0
```

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/BharathKumarSuresh/claude-design-system-hooks.git
cd claude-design-system-hooks

# Install core dependencies
npm install @claude-design/core @claude-design/cli

# Configure with your Claude API key
claude-design configure --api-key $CLAUDE_API_KEY

# Verify installation
claude-design --version
```

### Docker Installation

```bash
# Pull official image
docker pull claude-design-engine:2026-stable

# Run containerized
docker run -p 3000:3000 \
  -e CLAUDE_API_KEY=$CLAUDE_API_KEY \
  claude-design-engine:2026-stable
```

## Configuration

### Profile Configuration File

Create `.claude-design.json` in your project root:

```json
{
  "profile": {
    "name": "my-design-profile",
    "version": "2026.3",
    "preferences": {
      "framework": "react",
      "version": "18.x",
      "styling": "tailwind",
      "component_library": "shadcn-ui",
      "responsive_breakpoints": ["sm", "md", "lg", "xl", "2xl"],
      "accessibility_level": "wcag_22_aa",
      "code_style": "typescript_strict"
    },
    "design_tokens": {
      "primary": "#6366f1",
      "secondary": "#8b5cf6",
      "accent": "#f59e0b",
      "neutral": "#64748b",
      "spacing_scale": [4, 8, 12, 16, 24, 32, 48, 64, 96],
      "border_radius": {
        "sm": 4,
        "md": 8,
        "lg": 12,
        "xl": 16
      }
    },
    "plugins": [
      {
        "name": "a11y-auditor",
        "enabled": true,
        "config": {
          "strict_mode": true,
          "auto_fix": false
        }
      }
    ]
  }
}
```

### Environment Variables

```bash
# Required
export CLAUDE_API_KEY="your-claude-api-key"

# Optional - for hybrid AI workflows
export OPENAI_API_KEY="your-openai-api-key"

# Optional - configure output directory
export CLAUDE_DESIGN_OUTPUT_DIR="./generated-components"
```

## Key Commands

### Interactive Mode

```bash
# Start conversational design session
claude-design interact --profile my-design-profile

# With custom framework
claude-design interact --framework vue --styling scss

# With accessibility constraints
claude-design interact --accessibility wcag-22-aaa
```

### Batch Generation

```bash
# Generate from YAML specification
claude-design generate \
  --input ./design-specs/dashboard.yaml \
  --output ./src/components \
  --framework react \
  --styling tailwind \
  --include-tests \
  --include-stories

# Generate from Figma export
claude-design generate \
  --input ./figma-export.json \
  --output ./components \
  --framework angular \
  --accessibility wcag-22-aa

# Generate entire design system
claude-design generate \
  --input ./design-system-spec.yaml \
  --output ./design-system \
  --framework react \
  --include-tokens \
  --include-docs \
  --verbose
```

### Component Generation

```bash
# Generate single component
claude-design component create \
  --name ProductCard \
  --description "Card displaying product image, title, price, and add-to-cart button" \
  --framework react \
  --output ./src/components/ProductCard

# Generate with props specification
claude-design component create \
  --name DataTable \
  --props-file ./specs/datatable-props.json \
  --framework vue \
  --with-types
```

### Design Token Management

```bash
# Extract tokens from image/mockup
claude-design tokens extract \
  --input ./mockups/homepage.png \
  --output ./tokens/design-tokens.json

# Generate CSS/SCSS variables from tokens
claude-design tokens generate \
  --input ./tokens/design-tokens.json \
  --format css-variables \
  --output ./styles/tokens.css

# Validate token consistency
claude-design tokens validate ./tokens/*.json
```

### Plugin Management

```bash
# List available plugins
claude-design plugins list

# Install plugin
claude-design plugins install @claude-design/figma-sync

# Configure plugin
claude-design plugins configure figma-sync \
  --token $FIGMA_TOKEN \
  --sync-mode bidirectional

# Browse marketplace
claude-design marketplace browse --category animation

# Install community skill
claude-design marketplace install @community/lottie-animator
```

## Usage Patterns

### Pattern 1: Natural Language Component Generation

```javascript
// In your Node.js script or AI agent workflow
const { ClaudeDesign } = require('@claude-design/core');

const designer = new ClaudeDesign({
  apiKey: process.env.CLAUDE_API_KEY,
  framework: 'react',
  styling: 'tailwind'
});

async function generateLoginForm() {
  const result = await designer.generate({
    prompt: `Create a modern login form with:
      - Email and password fields
      - Remember me checkbox
      - Forgot password link
      - Social login buttons (Google, GitHub)
      - Dark theme with purple accent
      - Fully accessible with keyboard navigation`,
    options: {
      includeTests: true,
      includeStorybook: true,
      accessibility: 'wcag-22-aa'
    }
  });

  console.log('Generated files:', result.files);
  // Writes to ./src/components/LoginForm/
  await result.save('./src/components/LoginForm');
}

generateLoginForm();
```

### Pattern 2: Design System Specification

```yaml
# design-system-spec.yaml
system:
  name: "Corporate Design System"
  version: "1.0.0"
  framework: "react"
  styling: "tailwind"

tokens:
  colors:
    primary: "#0066cc"
    secondary: "#6b7280"
    accent: "#f59e0b"
    success: "#10b981"
    error: "#ef4444"
    warning: "#f59e0b"
  
  typography:
    scale: "major-third"
    base_size: 16
    fonts:
      heading: "Inter, sans-serif"
      body: "Inter, sans-serif"
      mono: "Fira Code, monospace"
  
  spacing:
    unit: 4
    scale: [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]
  
  breakpoints:
    sm: 640
    md: 768
    lg: 1024
    xl: 1280
    "2xl": 1536

components:
  - name: "Button"
    variants: ["primary", "secondary", "outline", "ghost"]
    sizes: ["sm", "md", "lg"]
    states: ["default", "hover", "active", "disabled"]
  
  - name: "Card"
    props:
      - name: "variant"
        type: "string"
        values: ["default", "bordered", "elevated"]
      - name: "padding"
        type: "spacing"
        default: 4
  
  - name: "Modal"
    features: ["backdrop", "close-button", "keyboard-escape"]
    accessibility: "wcag-22-aa"

pages:
  - name: "Dashboard"
    layout: "sidebar-content"
    components: ["StatCard", "DataTable", "ChartWidget"]
```

```bash
# Generate entire system
claude-design generate \
  --input design-system-spec.yaml \
  --output ./design-system \
  --include-docs \
  --include-storybook
```

### Pattern 3: Programmatic API Usage

```typescript
// advanced-usage.ts
import { ClaudeDesign, DesignConfig } from '@claude-design/core';
import { FigmaSyncPlugin } from '@claude-design/figma-sync';
import { A11yAuditor } from '@claude-design/a11y-auditor';

const config: DesignConfig = {
  apiKey: process.env.CLAUDE_API_KEY,
  framework: 'react',
  typescript: true,
  styling: 'tailwind',
  plugins: [
    new FigmaSyncPlugin({
      token: process.env.FIGMA_TOKEN,
      fileKey: 'abc123def456'
    }),
    new A11yAuditor({
      strictMode: true,
      level: 'wcag-22-aaa'
    })
  ]
};

const designer = new ClaudeDesign(config);

async function buildNavigationComponent() {
  // Generate component from description
  const nav = await designer.component.create({
    name: 'MainNavigation',
    description: `
      Responsive navigation bar with:
      - Logo on left
      - Menu items in center
      - User profile dropdown on right
      - Mobile hamburger menu
      - Sticky header on scroll
    `,
    responsive: true,
    a11y: {
      ariaLabels: true,
      keyboardNav: true,
      screenReader: true
    }
  });

  // Audit accessibility
  const auditResults = await designer.audit.a11y(nav.code);
  console.log('Accessibility score:', auditResults.score);

  // Generate tests
  const tests = await designer.tests.generate(nav.code, {
    framework: 'jest',
    coverage: 'full'
  });

  // Save all artifacts
  await nav.save('./src/components/MainNavigation', {
    includeTests: true,
    includeStorybook: true,
    includeTypes: true
  });
}

buildNavigationComponent();
```

### Pattern 4: Design Token Extraction

```javascript
const { TokenExtractor } = require('@claude-design/core');

async function extractFromMockup() {
  const extractor = new TokenExtractor({
    apiKey: process.env.CLAUDE_API_KEY
  });

  // Extract from image
  const tokens = await extractor.fromImage('./mockups/homepage.png', {
    extractColors: true,
    extractTypography: true,
    extractSpacing: true,
    extractBorderRadius: true
  });

  console.log('Extracted tokens:', tokens);
  
  /*
  {
    colors: {
      primary: { hex: '#6366f1', name: 'Indigo' },
      secondary: { hex: '#8b5cf6', name: 'Purple' },
      accent: { hex: '#f59e0b', name: 'Amber' }
    },
    typography: {
      headings: { family: 'Inter', weight: 700, scale: [32, 24, 20] },
      body: { family: 'Inter', weight: 400, size: 16 }
    },
    spacing: [4, 8, 12, 16, 24, 32, 48],
    borderRadius: { sm: 4, md: 8, lg: 12 }
  }
  */

  // Generate CSS variables
  const css = await extractor.toCSS(tokens);
  await fs.writeFile('./styles/tokens.css', css);

  // Generate Tailwind config
  const tailwindConfig = await extractor.toTailwind(tokens);
  await fs.writeFile('./tailwind.config.js', tailwindConfig);
}

extractFromMockup();
```

### Pattern 5: Multi-Framework Generation

```javascript
const { ClaudeDesign } = require('@claude-design/core');

async function generateForAllFrameworks() {
  const designer = new ClaudeDesign({
    apiKey: process.env.CLAUDE_API_KEY
  });

  const description = `
    Product card with image, title, price, rating stars,
    and add-to-cart button. Include hover effects.
  `;

  // Generate React version
  const reactComponent = await designer.generate({
    prompt: description,
    framework: 'react',
    styling: 'tailwind',
    typescript: true
  });
  await reactComponent.save('./output/react/ProductCard');

  // Generate Vue version
  const vueComponent = await designer.generate({
    prompt: description,
    framework: 'vue',
    styling: 'scss',
    composition: true
  });
  await vueComponent.save('./output/vue/ProductCard');

  // Generate Angular version
  const angularComponent = await designer.generate({
    prompt: description,
    framework: 'angular',
    styling: 'scss',
    standalone: true
  });
  await angularComponent.save('./output/angular/ProductCard');

  // Generate vanilla HTML/CSS
  const vanillaComponent = await designer.generate({
    prompt: description,
    framework: 'html',
    styling: 'css',
    modern: true
  });
  await vanillaComponent.save('./output/vanilla/ProductCard');
}

generateForAllFrameworks();
```

## Common Workflows

### Workflow 1: Rapid Prototyping

```bash
# Start interactive session
claude-design interact --framework react --styling tailwind

# Example conversation:
# You: "Create a landing page for a SaaS product"
# Claude: [generates hero section, features grid, pricing table, CTA]

# You: "Make it dark theme with purple accent"
# Claude: [updates color scheme]

# You: "Add testimonials section"
# Claude: [adds testimonial carousel]

# Export when satisfied
# Files saved to ./generated-components/
```

### Workflow 2: Design System Migration

```bash
# Step 1: Extract tokens from existing design
claude-design tokens extract \
  --input ./current-app/styles \
  --output ./tokens/legacy-tokens.json

# Step 2: Generate new design system
claude-design generate \
  --input ./specs/new-design-system.yaml \
  --tokens ./tokens/legacy-tokens.json \
  --output ./new-design-system

# Step 3: Create migration guide
claude-design docs migration \
  --from ./tokens/legacy-tokens.json \
  --to ./new-design-system/tokens.json \
  --output ./MIGRATION.md
```

### Workflow 3: CI/CD Integration

```yaml
# .github/workflows/design-system.yml
name: Generate Design System

on:
  push:
    paths:
      - 'design-specs/**'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Claude Design
        run: |
          npm install -g @claude-design/cli
          claude-design configure --api-key ${{ secrets.CLAUDE_API_KEY }}
      
      - name: Generate Components
        run: |
          claude-design generate \
            --input ./design-specs/components.yaml \
            --output ./src/components \
            --framework react \
            --include-tests \
            --include-stories
      
      - name: Audit Accessibility
        run: |
          claude-design audit a11y ./src/components \
            --level wcag-22-aa \
            --fail-on-warnings
      
      - name: Commit Changes
        run: |
          git config user.name "Claude Design Bot"
          git add src/components
          git commit -m "chore: regenerate design system"
          git push
```

## Troubleshooting

### Issue: API Rate Limiting

```bash
# Check current rate limit status
claude-design status --api-limits

# Configure request throttling
claude-design configure \
  --rate-limit 10 \
  --rate-limit-window 60000
```

### Issue: Generated Code Doesn't Match Framework Version

```bash
# Specify exact framework version
claude-design generate \
  --framework react@18.2.0 \
  --input ./spec.yaml

# Update framework adapters
npm update @claude-design/react-adapter
```

### Issue: Accessibility Audit Failures

```javascript
// Enable auto-fix mode
const designer = new ClaudeDesign({
  apiKey: process.env.CLAUDE_API_KEY,
  plugins: [
    new A11yAuditor({
      autoFix: true,  // Automatically fix common issues
      strictMode: false  // Use warnings instead of errors
    })
  ]
});

// Generate with explicit a11y requirements
const component = await designer.generate({
  prompt: 'Login form',
  accessibility: {
    level: 'wcag-22-aa',
    requirements: [
      'keyboard-navigation',
      'screen-reader-labels',
      'color-contrast-4.5:1',
      'focus-indicators'
    ]
  }
});
```

### Issue: Design Tokens Not Applying

```bash
# Validate token file structure
claude-design tokens validate ./tokens/design-tokens.json

# Regenerate CSS variables
claude-design tokens generate \
  --input ./tokens/design-tokens.json \
  --format css-variables \
  --output ./styles/tokens.css \
  --force

# Verify token references in generated code
claude-design audit tokens ./src/components
```

### Issue: Plugin Conflicts

```bash
# List active plugins
claude-design plugins list --active

# Disable conflicting plugin
claude-design plugins disable @community/conflicting-plugin

# Reset plugin configuration
claude-design plugins reset --all

# Reinstall core plugins
npm install @claude-design/figma-sync@latest
```

### Debug Mode

```bash
# Enable verbose logging
claude-design generate \
  --input ./spec.yaml \
  --verbose \
  --debug \
  --log-file ./debug.log

# Check system diagnostics
claude-design diagnostics --full
```

## Advanced Configuration

### Custom Subagents

```json
{
  "subagents": [
    {
      "id": "color-theorist",
      "priority": 1,
      "specialties": ["color_harmony", "contrast_ratios"],
      "model": "claude-sonnet-4"
    },
    {
      "id": "layout-architect",
      "priority": 2,
      "specialties": ["grid_systems", "responsive_design"],
      "model": "claude-sonnet-4"
    },
    {
      "id": "typography-curator",
      "priority": 3,
      "specialties": ["font_pairing", "readability"],
      "model": "claude-haiku-3.5"
    }
  ]
}
```

### Hybrid AI Configuration

```bash
# Configure Claude as primary, OpenAI as fallback
claude-design configure \
  --ai-provider hybrid \
  --primary claude \
  --claude-key $CLAUDE_API_KEY \
  --openai-key $OPENAI_API_KEY \
  --fallback-on-rate-limit true
```

This skill enables AI coding agents to leverage Claude's design capabilities for generating production-ready UI components, design systems, and accessible interfaces from natural language descriptions.

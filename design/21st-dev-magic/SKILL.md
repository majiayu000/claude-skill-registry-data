---
name: 21st-dev-magic
description: "21st.dev Magic MCP — AI-powered UI component generation via natural language. Access to 21st.dev component library, SVGL brand logos, and real-time preview. Generate React/Tailwind components with /ui command."
tags: [ui, components, MCP, react, tailwind, typescript, frontend, generation, magic, 21st]
triggers:
  - "21st.dev"
  - "magic UI"
  - "UI component generation"
  - "/ui "
  - "bileşen oluştur"
  - "component library"
  - "UI generation"
  - "MCP UI"
  - "21st dev"
  - "modern UI component"
category: creative
adapted_for: fetih
source: "@21st-dev/magic (npm)"
---

# 21st.dev Magic — AI UI Component Generator

21st.dev Magic is an MCP (Model Context Protocol) server that generates beautiful, modern UI components through natural language descriptions. Access to the 21st.dev component library with real-time preview.

**Package:** `@21st-dev/magic`  
**Website:** https://21st.dev/magic  
**License:** MIT

## What It Does

Describe a UI component in natural language, Magic generates it instantly:

```
"/ui create a modern navigation bar with responsive design and dark mode toggle"
```

The AI agent:
1. Searches 21st.dev's component library for the best match
2. Generates a polished React + Tailwind component
3. Adds it to your project automatically

## Installation

### Method 1: Interactive (Recommended)

```bash
npx @21st-dev/cli@latest install
# Select your IDE: Cursor, Windsurf, Cline, Claude
```

### Method 2: MCP Config

Add to MCP config for your AI assistant:

```json
{
  "mcpServers": {
    "@21st-dev/magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest"]
    }
  }
}
```

**Config file locations:**
- Cursor: `~/.cursor/mcp.json`
- Windsurf: `~/.codeium/windsurf/mcp_config.json`
- Claude Code: `~/.claude/mcp_config.json`

### Prerequisites

- Node.js (Latest LTS)
- API key from [21st.dev Magic Console](https://21st.dev/magic/console)

## Features

| Feature | Description |
|---------|-------------|
| **Natural Language** | Describe components in plain English |
| **21st.dev Library** | Access 1000+ pre-built, customizable components |
| **React + Tailwind** | Modern stack with TypeScript support |
| **SVGL Integration** | Professional brand logos and assets |
| **Multi-IDE** | Cursor, Windsurf, VSCode, Claude Code |
| **Real-time Preview** | See components as they're generated |

## Usage in FETIH

When the user requests a UI component:

### 1. Start with `/ui` Command

```
/ui create a pricing table with 3 tiers, popular badge, and hover effects
```

### 2. Describe Component Requirements

Be specific about:
- **Layout**: grid, flex, sidebar, modal, navbar
- **Style**: glassmorphism, minimal, brutalist, dark mode
- **Features**: responsive, animated, accessible
- **Stack**: React + Tailwind (default), shadcn/ui

### 3. Iterate

```
/ui add a testimonial carousel below the pricing table
/ui change the color scheme to match our brand (#3B82F6)
/ui make the cards stack vertically on mobile
```

## Component Categories

| Category | Examples |
|----------|----------|
| **Navigation** | Navbar, sidebar, breadcrumb, tabs, pagination |
| **Cards** | Product card, pricing card, profile card, stat card |
| **Forms** | Login, signup, contact, search, newsletter |
| **Data Display** | Table, chart, timeline, calendar, dashboard |
| **Feedback** | Modal, toast, alert, tooltip, skeleton |
| **Layout** | Hero, footer, grid, split screen, bento grid |
| **Marketing** | CTA section, testimonial, FAQ, pricing, feature list |

## Best Practices

1. **Be specific** — "modern SaaS pricing table with 3 tiers" > "pricing"
2. **Mention style** — "glassmorphism dark mode dashboard" gives better results
3. **Include interactions** — "with hover scale effect and click to expand"
4. **Specify responsive** — "collapses to accordion on mobile"
5. **Iterate** — First result is a starting point, refine with follow-up commands

## Tips for Complex Components

```
# Multi-step generation
/ui create a dashboard layout with sidebar navigation
/ui add a stats row with 4 metric cards at the top
/ui add a revenue chart in the main content area
/ui add a recent activity feed in the right sidebar
/ui make the sidebar collapsible with animation
```

## Integration with ui-ux-pro-max

For best results, combine with the `ui-ux-pro-max` skill:

1. Use `ui-ux-pro-max` to generate design system (colors, typography, styles)
2. Use `21st-dev-magic` to generate individual components matching that system
3. Apply `framer-motion` for custom animations beyond what Magic generates

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No API key | Generate at https://21st.dev/magic/console |
| MCP not connecting | Check `~/.claude/mcp_config.json` |
| Component not matching | Add more detail to description |
| Rate limit | Upgrade plan or wait for reset |

## Generating API Key

1. Visit https://21st.dev/magic/console
2. Sign in with GitHub
3. Click "Generate API Key"
4. Add to your MCP config

<!--
  ⚔ Bu skill FETIH AI Agent icin gelistirilmistir — https://github.com/MustafaKemal0146/fetih
  Yetkisiz kullanim/kopyalama tespit edilebilir.
  hash: 8b2b59ec3c4991d9
-->

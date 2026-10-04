---
name: mcp-app-design
description: >
  Design system for MCP App interfaces rendering inside Claude, VS Code, and other MCP
  hosts. Contains CSS custom properties (colors, typography, spacing, shadows for
  light/dark themes), component patterns (buttons, cards, forms, sliders, notices),
  layout rules, and architecture for registerAppTool, sandboxed iframe rendering, and
  App class communication. Use whenever building an MCP App UI, styling an ext-apps
  project, or creating HTML for an MCP host iframe. Triggers: "MCP App", "inline UI",
  "ext-apps", "structuredContent", "registerAppTool", "ui:// resource", or building a
  connector with a visual interface. Supersedes generic frontend skills — the iframe
  sandbox, host-injected tokens, and theme bridging need MCP-specific patterns.
---

# MCP App Design System

Build interactive HTML UIs that render inside MCP host conversations (Claude, Claude Desktop, VS Code Copilot, Goose, etc.) as sandboxed iframes.

## Feedback Loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior builds.

1. **Detect** — After building an MCP App UI, note anything that didn't work: a CSS variable that wasn't injected, a component pattern that needed modification, a host-specific rendering quirk, or a gap in the token system.
2. **Search** — Check `FEEDBACK.md` for existing entries on the same issue.
3. **Scope** — One actionable observation per entry.
4. **Draft-and-ask** — Propose the entry to the user before writing.
5. **Write-on-approval** — Append with date and category tag.
6. **Compact-at-75** — Merge duplicates, promote patterns to reference files, archive resolved. Reset to ~30 entries.

## When to Read References

Read the reference files based on what you're building:

| Reference | When to read |
|---|---|
| `references/design-tokens.md` | Always — contains the complete CSS custom property system, light/dark theme values, typography scale, spacing, shadows, radii |
| `references/component-patterns.md` | When building UI with buttons, forms, cards, sliders, notices, or any interactive elements |
| `references/architecture.md` | When scaffolding a new MCP App project, declaring tools with UI, or setting up the App class communication |

Read `design-tokens.md` first on every MCP App task — it defines the CSS custom properties that the host injects, and your UI consumes these variables rather than hardcoding colors.

## Core Principles

### 1. Host-Injected Theming

MCP Apps don't control their own theme. The host (Claude, VS Code, etc.) pushes CSS custom properties and a theme value (`"light"` or `"dark"`) to your app via the host context. Your job is to consume these variables, not define your own color palette.

The `light-dark()` CSS function is the primary mechanism for automatic theme adaptation. Define fallback values in `:root` using this function, and the host's variables override them seamlessly via `applyHostStyleVariables()`.

```css
:root {
  color-scheme: light dark;
  --color-text-primary: light-dark(#1f2937, #f3f4f6);
  --color-background-primary: light-dark(#ffffff, #1a1a1a);
}
```

### 2. Fallback Values Are Mandatory

Define fallback values for every CSS custom property in `:root` using `light-dark()`. Host variable injection may be delayed (race condition on initial load) or absent (unsupported host, local testing without the basic-host harness). Your app should render correctly with only its own fallbacks — host variables are an enhancement, not a requirement.

The Quick Start CSS below demonstrates the correct pattern. When adding new variables, follow the same approach: local fallback first, host override via `applyHostStyleVariables()` second.

### 3. Sandboxed Iframe Constraints

Your UI runs in a sandboxed iframe:

- All communication goes through postMessage (the App class handles this)
- External scripts need CSP whitelisting via `_meta.ui.csp`
- Bundle everything into a single HTML file with `vite-plugin-singlefile` to avoid CSP issues
- No `localStorage`/`sessionStorage` — use in-memory state or persist data via tool calls
- No access to parent window DOM or cookies

### 4. Compact Layout

MCP App iframes have constrained width inside the conversation column. Design for:

- **Basic tools**: `max-width: 425px` — single-column, focused interaction
- **Dashboards/complex apps**: `max-width: 600px` (or `width: 100%` for full-width)
- **Height**: Typically 400-600px; design to avoid scrolling when possible
- Always use `box-sizing: border-box` on everything
- Padding: 8-12px for compact apps, 16-24px for spacious layouts

### 5. Font Inheritance

Use the host's font stack via CSS custom properties rather than hardcoding font families, because each host has its own typography:

```css
body {
  font-family: var(--font-sans);
  font-size: var(--font-text-md-size);
  line-height: var(--font-text-md-line-height);
}

code, pre {
  font-family: var(--font-mono);
}
```

### 6. Spacing System

Derive spacing from the typography scale to keep proportions consistent:

```css
:root {
  --spacing-unit: var(--font-text-md-size); /* 1rem */
  --spacing-xs: calc(var(--spacing-unit) * 0.25);  /* 4px */
  --spacing-sm: calc(var(--spacing-unit) * 0.5);   /* 8px */
  --spacing-md: var(--spacing-unit);                /* 16px */
  --spacing-lg: calc(var(--spacing-unit) * 1.5);    /* 24px */
}
```

## Quick Start CSS

Minimal `:root` with proper fallbacks for a new MCP App. See `architecture.md` → "UI: Host Context and Theming" for the TypeScript theme bridging setup that wires these up to the host.

```css
:root {
  color-scheme: light dark;
  --color-text-primary: light-dark(#1f2937, #f3f4f6);
  --color-text-secondary: light-dark(#6b7280, #9ca3af);
  --color-background-primary: light-dark(#ffffff, #1a1a1a);
  --color-background-secondary: light-dark(#f5f5f5, #2d2d2d);
  --color-border-primary: light-dark(#e5e7eb, #404040);
  --color-ring-primary: light-dark(#3b82f6, #60a5fa);
  --border-radius-md: 6px;
  --border-width-regular: 1px;
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: ui-monospace, 'SF Mono', Monaco, monospace;
  --font-weight-normal: 400;
  --font-weight-bold: 700;
  --font-text-md-size: 1rem;
  --font-text-md-line-height: 1.5;
  --spacing-unit: var(--font-text-md-size);
  --spacing-xs: calc(var(--spacing-unit) * 0.25);
  --spacing-sm: calc(var(--spacing-unit) * 0.5);
  --spacing-md: var(--spacing-unit);
  --spacing-lg: calc(var(--spacing-unit) * 1.5);
  /* App-level accent (not a host token — define per-app) */
  --color-accent: #2563eb;
  --color-text-on-accent: #ffffff;
}

*, *::before, *::after { box-sizing: border-box; }

html, body {
  margin: 0; padding: 0;
  font-family: var(--font-sans);
  font-size: var(--font-text-md-size);
  line-height: var(--font-text-md-line-height);
  color: var(--color-text-primary);
  background: var(--color-background-primary);
  transition: background-color 0.2s, color 0.2s;
}
```

> **Note:** `--color-accent` and `--color-text-on-accent` are app-level variables you define yourself — they're not part of the host token system. Each MCP App can brand its primary action color independently.

## Anti-Patterns

Avoid these patterns because they break in the MCP App sandbox or produce inconsistent rendering across hosts:

- **Hardcoded colors** — Use `var(--color-text-primary)` instead of `color: #333`, because the host controls the palette and may be in dark mode.
- **Fixed widths over 600px** — The conversation column is narrow. Design mobile-first.
- **Separate CSS files without CSP config** — Bundle CSS inline or configure CSP. Separate files won't load in the sandbox without whitelisting.
- **Using localStorage** — Sandboxed iframes can't access storage. Use React state, JS variables, or persist via tool calls.
- **Ignoring host theme changes** — Wire up `onhostcontextchanged` to re-apply theme, because users can switch themes mid-conversation.
- **Heavy frameworks** — The iframe loads fresh each time. Prefer Preact (~3KB) over React (~40KB) for MCP Apps, since every KB matters on cold loads. Aim for under 100KB total bundle size.

## Accessibility Baseline

All MCP App UIs should meet these minimum standards:

- Interactive elements have appropriate ARIA labels when their purpose isn't clear from visible text
- Color combinations meet WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
- All interactive elements are keyboard-navigable with visible focus indicators (the `focus-visible` patterns in `component-patterns.md` handle this)
- Form inputs have associated `<label>` elements or `aria-label` attributes

---
name: nothing-design-skill
description: Generate UI components in Nothing's monochrome, typographic, industrial design language with Swiss typography and OLED aesthetics
triggers:
  - "use nothing design style"
  - "create a nothing style component"
  - "design this with nothing aesthetics"
  - "apply nothing design language"
  - "make this look like nothing phone UI"
  - "generate UI in nothing style"
  - "use monochrome industrial design"
  - "create nothing-inspired interface"
---

# Nothing Design Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A design system skill for Claude Code that generates UI components following Nothing's visual language: monochrome, typographic, industrial. Provides reusable design tokens, component patterns, and multi-platform output (HTML/CSS, SwiftUI, React/Tailwind).

## What It Does

Nothing Design Skill codifies Nothing's design principles into a reusable system:

- **Three-layer visual hierarchy**: Display, body, metadata — strict information architecture
- **Monochrome palette**: OLED blacks (#000000), pure whites (#FFFFFF), precise grays
- **Typography**: Space Grotesk (display), Space Mono (monospace), Doto (dot-matrix accents)
- **Industrial components**: Segmented progress bars, mechanical toggles, instrument-style widgets
- **Full dark/light modes**: Complete token system with semantic color mapping

## Installation

Clone the repository and copy the skill folder to your Claude Code skills directory:

```sh
git clone https://github.com/dominikmartn/nothing-design-skill.git
cp -r nothing-design-skill/nothing-design ~/.claude/skills/
```

Restart Claude Code to activate the skill.

## Core Design Tokens

### Color System

**Dark Mode (Primary)**
```css
--color-background: #000000;    /* Pure black (OLED) */
--color-surface: #0A0A0A;       /* Elevated surface */
--color-border: #1A1A1A;        /* Subtle dividers */
--color-text-primary: #FFFFFF;  /* Pure white */
--color-text-secondary: #999999; /* Mid gray */
--color-text-tertiary: #666666; /* Dim gray */
--color-accent: #FF0000;        /* Nothing red (sparingly) */
```

**Light Mode**
```css
--color-background: #FFFFFF;
--color-surface: #F5F5F5;
--color-border: #E5E5E5;
--color-text-primary: #000000;
--color-text-secondary: #666666;
--color-text-tertiary: #999999;
--color-accent: #FF0000;
```

### Typography Scale

```css
--font-display: 'Space Grotesk', sans-serif;
--font-body: 'Space Grotesk', sans-serif;
--font-mono: 'Space Mono', monospace;
--font-dot: 'Doto', monospace;

--text-display-xl: 48px / 1.1;    /* Hero headlines */
--text-display-lg: 36px / 1.2;    /* Section titles */
--text-display-md: 24px / 1.3;    /* Card headers */
--text-body-lg: 16px / 1.5;       /* Primary text */
--text-body-md: 14px / 1.5;       /* Secondary text */
--text-mono-md: 14px / 1.4;       /* Code, data */
--text-label-sm: 11px / 1.3;      /* Labels, metadata */
```

### Spacing System

```css
--space-2xs: 4px;   /* Tight padding */
--space-xs: 8px;    /* Compact spacing */
--space-sm: 12px;   /* Small gaps */
--space-md: 16px;   /* Default spacing */
--space-lg: 24px;   /* Section spacing */
--space-xl: 32px;   /* Large gaps */
--space-2xl: 48px;  /* Major sections */
```

## Component Patterns

### Button (HTML/CSS)

```html
<button class="nothing-btn nothing-btn-primary">
  <span class="nothing-btn-label">Continue</span>
</button>

<style>
.nothing-btn {
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.02em;
  padding: 12px 24px;
  text-transform: uppercase;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.nothing-btn:hover {
  background: var(--color-surface);
  border-color: var(--color-text-primary);
}

.nothing-btn-primary {
  background: var(--color-text-primary);
  border-color: var(--color-text-primary);
  color: var(--color-background);
}

.nothing-btn-primary:hover {
  background: var(--color-text-secondary);
  border-color: var(--color-text-secondary);
}
</style>
```

### Segmented Progress Bar

```html
<div class="nothing-progress">
  <div class="nothing-progress-track">
    <div class="nothing-progress-segment"></div>
    <div class="nothing-progress-segment"></div>
    <div class="nothing-progress-segment"></div>
    <div class="nothing-progress-segment"></div>
    <div class="nothing-progress-segment filled"></div>
    <div class="nothing-progress-segment filled"></div>
    <div class="nothing-progress-segment filled"></div>
  </div>
  <span class="nothing-progress-label">70%</span>
</div>

<style>
.nothing-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nothing-progress-track {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nothing-progress-segment {
  height: 4px;
  flex: 1;
  background: var(--color-border);
  transition: background 0.2s ease;
}

.nothing-progress-segment.filled {
  background: var(--color-text-primary);
}

.nothing-progress-label {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--color-text-secondary);
  min-width: 40px;
  text-align: right;
}
</style>
```

### Card Component (React/Tailwind)

```jsx
export function NothingCard({ title, metadata, children }) {
  return (
    <div className="border border-zinc-900 bg-black p-6">
      {/* Header */}
      <div className="mb-6 border-b border-zinc-900 pb-4">
        <h3 className="font-display text-2xl font-medium tracking-tight text-white">
          {title}
        </h3>
        {metadata && (
          <p className="font-mono text-xs uppercase tracking-wider text-zinc-600 mt-2">
            {metadata}
          </p>
        )}
      </div>
      
      {/* Content */}
      <div className="space-y-4 text-zinc-400">
        {children}
      </div>
    </div>
  );
}

// Usage
<NothingCard title="System Status" metadata="Updated 14:32">
  <div className="flex justify-between items-center">
    <span className="text-sm">Battery</span>
    <span className="font-mono text-white">87%</span>
  </div>
</NothingCard>
```

### Toggle Switch (SwiftUI)

```swift
struct NothingToggle: View {
    @Binding var isOn: Bool
    
    var body: some View {
        Button(action: { isOn.toggle() }) {
            HStack(spacing: 2) {
                Rectangle()
                    .fill(isOn ? Color.white : Color(hex: "1A1A1A"))
                    .frame(width: 20, height: 32)
                
                Rectangle()
                    .fill(isOn ? Color(hex: "1A1A1A") : Color.white)
                    .frame(width: 20, height: 32)
            }
            .overlay(
                Rectangle()
                    .strokeBorder(Color(hex: "333333"), lineWidth: 1)
            )
        }
        .animation(.easeInOut(duration: 0.15), value: isOn)
    }
}

// Usage
@State private var notificationsEnabled = true

NothingToggle(isOn: $notificationsEnabled)
```

### Data Table

```html
<table class="nothing-table">
  <thead>
    <tr>
      <th>Device</th>
      <th>Status</th>
      <th>Updated</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Phone (2)</td>
      <td><span class="status-dot active"></span> Online</td>
      <td>2m ago</td>
    </tr>
    <tr>
      <td>Ear (stick)</td>
      <td><span class="status-dot"></span> Offline</td>
      <td>1h ago</td>
    </tr>
  </tbody>
</table>

<style>
.nothing-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-family: var(--font-display);
}

.nothing-table th {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-tertiary);
  text-align: left;
  padding: 8px 16px;
  border-bottom: 1px solid var(--color-border);
}

.nothing-table td {
  font-size: 14px;
  color: var(--color-text-primary);
  padding: 16px;
  border-bottom: 1px solid var(--color-border);
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-text-tertiary);
  margin-right: 8px;
}

.status-dot.active {
  background: #00FF00;
}
</style>
```

## Design Principles

### Visual Hierarchy (Three Layers Only)

1. **Display**: Headlines, primary actions, key metrics
2. **Body**: Descriptive text, secondary actions, content
3. **Metadata**: Labels, timestamps, auxiliary information

**Never use more than three levels in a single view.**

### Typography Rules

- **Space Grotesk**: All UI text, headlines, buttons
- **Space Mono**: Data, codes, timestamps, technical info
- **Doto**: Decorative accents only (sparingly)
- **Letter spacing**: 0.02em for buttons/labels, tighter for display
- **Line height**: 1.1-1.3 for display, 1.5 for body text

### Motion & Transitions

```css
/* Standard easing */
transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);

/* Mechanical snap */
transition: all 0.1s cubic-bezier(0.4, 0, 1, 1);

/* Smooth fade */
transition: opacity 0.2s ease;
```

### Spacing Consistency

- Use 4px grid system
- Default gap: 16px
- Section spacing: 24px or 32px
- Never arbitrary values

## Platform-Specific Output

### Generating HTML/CSS

```
User: "Create a nothing-style settings panel with toggles"

AI generates:
- Semantic HTML structure
- Inline <style> with CSS variables
- Self-contained component
```

### Generating SwiftUI

```
User: "Make a nothing design stats card in SwiftUI"

AI generates:
- SwiftUI View struct
- Color extensions for hex values
- Proper spacing/font modifiers
```

### Generating React/Tailwind

```
User: "Build a nothing-inspired navigation bar with React"

AI generates:
- Functional component
- Tailwind classes matching token values
- TypeScript types if requested
```

## Common Patterns

### Status Indicators

```html
<!-- Dot indicator -->
<div class="status-indicator">
  <span class="status-dot active"></span>
  <span class="status-label">Connected</span>
</div>

<!-- Segmented bar -->
<div class="signal-strength">
  <div class="bar"></div>
  <div class="bar"></div>
  <div class="bar active"></div>
  <div class="bar active"></div>
</div>
```

### Dot-Matrix Numerals (Doto Font)

```html
<span class="dot-display">88:88</span>

<style>
.dot-display {
  font-family: var(--font-dot);
  font-size: 48px;
  letter-spacing: 0.1em;
  color: var(--color-text-primary);
}
</style>
```

### Loading States

```html
<div class="nothing-loader">
  <div class="loader-segment"></div>
  <div class="loader-segment"></div>
  <div class="loader-segment"></div>
</div>

<style>
@keyframes loadPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.nothing-loader {
  display: flex;
  gap: 4px;
}

.loader-segment {
  width: 4px;
  height: 16px;
  background: var(--color-text-primary);
  animation: loadPulse 1.2s ease-in-out infinite;
}

.loader-segment:nth-child(2) { animation-delay: 0.2s; }
.loader-segment:nth-child(3) { animation-delay: 0.4s; }
</style>
```

## Troubleshooting

### Fonts Not Loading

Include Google Fonts in your HTML head or use system fallbacks:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

CSS fallback:
```css
--font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
```

### OLED Black Not Pure Black

Ensure you're using hex `#000000`, not `#000` or rgb values. Some design tools auto-adjust to `#0A0A0A`.

### Components Look Too Dense

Nothing design is intentionally compact. If needed for accessibility:
- Increase touch targets to 44px minimum
- Add `--space-md` (16px) padding to interactive elements
- Maintain visual density through borders, not spacing

### Dark/Light Mode Switching

Use CSS custom properties and data attributes:

```html
<html data-theme="dark">
```

```css
:root[data-theme="dark"] {
  --color-background: #000000;
  --color-text-primary: #FFFFFF;
}

:root[data-theme="light"] {
  --color-background: #FFFFFF;
  --color-text-primary: #000000;
}
```

Toggle with JavaScript:
```javascript
document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
```

## Advanced Techniques

### Glitch Effect (Brand Element)

```css
@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
  100% { transform: translate(0); }
}

.glitch-text {
  animation: glitch 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

### Grid Overlay Pattern

```css
.nothing-grid-bg {
  background-image: 
    linear-gradient(var(--color-border) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-border) 1px, transparent 1px);
  background-size: 20px 20px;
}
```

This skill provides everything needed to generate consistent, authentic Nothing-style UI across platforms. Focus on clarity, restraint, and mechanical precision.

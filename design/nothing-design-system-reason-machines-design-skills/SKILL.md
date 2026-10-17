---
name: nothing-design-system
description: Generate UI components in Nothing's monochrome, typographic, industrial design language with full dark/light mode support
triggers:
  - "use nothing design style"
  - "generate nothing UI component"
  - "create industrial design interface"
  - "build monochrome UI"
  - "design with nothing aesthetic"
  - "make a dot-matrix style component"
  - "use space grotesk typography"
  - "create segmented progress bar"
---

# Nothing Design System Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A reusable design system for generating UI components inspired by Nothing's visual language: monochrome, typographic, industrial, and mechanical. This skill provides a complete token system, component library, and platform-specific output formats.

## What This Skill Does

The Nothing Design Skill encodes a complete design system with:

- **Three-layer visual hierarchy**: Display, body, and metadata typography
- **Monochrome palette**: Pure blacks (#000000), whites (#FFFFFF), and precise grays
- **Industrial components**: Segmented progress bars, mechanical toggles, dot-matrix patterns
- **Complete theming**: Full dark and light mode token systems
- **Multi-platform output**: HTML/CSS, SwiftUI, React/Tailwind

## Installation

Install the skill into your Claude Code skills directory:

```sh
git clone https://github.com/dominikmartn/nothing-design-skill.git
cp -r nothing-design-skill/nothing-design ~/.claude/skills/
```

Or manually create `~/.claude/skills/nothing-design/` and copy the skill files.

## Core Design Principles

### Typography Hierarchy

The Nothing design system uses exactly three typographic layers:

1. **Display** (Space Grotesk): Headlines, primary actions, hero content
2. **Body** (Space Grotesk): Readable text, descriptions, interface labels
3. **Metadata** (Space Mono): Technical data, timestamps, system info, code

```css
/* Display */
font-family: 'Space Grotesk', -apple-system, sans-serif;
font-size: 32px;
font-weight: 700;
line-height: 1.1;
letter-spacing: -0.02em;

/* Body */
font-family: 'Space Grotesk', -apple-system, sans-serif;
font-size: 16px;
font-weight: 400;
line-height: 1.5;

/* Metadata */
font-family: 'Space Mono', 'SF Mono', monospace;
font-size: 12px;
font-weight: 400;
letter-spacing: 0.05em;
text-transform: uppercase;
```

### Color Tokens

**Dark Mode (Primary)**:
- `--bg-primary`: #000000 (pure black for OLED)
- `--bg-secondary`: #0A0A0A (raised surfaces)
- `--fg-primary`: #FFFFFF (high contrast text)
- `--fg-secondary`: #8C8C8C (subdued text)
- `--border`: #1F1F1F (subtle dividers)
- `--accent`: #FF0000 (Nothing red for critical actions)

**Light Mode**:
- `--bg-primary`: #FFFFFF
- `--bg-secondary`: #F5F5F5
- `--fg-primary`: #000000
- `--fg-secondary`: #737373
- `--border`: #E0E0E0
- `--accent`: #FF0000

### Spacing System

Uses an 8px base unit with a strict scale:

```css
--space-1: 4px;   /* 0.5 unit */
--space-2: 8px;   /* 1 unit */
--space-3: 16px;  /* 2 units */
--space-4: 24px;  /* 3 units */
--space-5: 32px;  /* 4 units */
--space-6: 48px;  /* 6 units */
--space-7: 64px;  /* 8 units */
```

## Component Patterns

### Segmented Progress Bar

The signature Nothing component — progress shown as discrete segments:

**HTML/CSS**:
```html
<div class="segmented-progress">
  <div class="segment"></div>
  <div class="segment"></div>
  <div class="segment active"></div>
  <div class="segment active"></div>
  <div class="segment active"></div>
</div>

<style>
.segmented-progress {
  display: flex;
  gap: 4px;
  height: 4px;
}

.segment {
  flex: 1;
  background: var(--border);
  transition: background 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.segment.active {
  background: var(--fg-primary);
}
</style>
```

**SwiftUI**:
```swift
struct SegmentedProgress: View {
    let segments: Int
    let filled: Int
    
    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<segments, id: \.self) { index in
                Rectangle()
                    .fill(index < filled ? Color.primary : Color.gray.opacity(0.2))
                    .frame(height: 4)
            }
        }
    }
}
```

**React/Tailwind**:
```jsx
export function SegmentedProgress({ segments = 5, filled = 3 }) {
  return (
    <div className="flex gap-1 h-1">
      {Array.from({ length: segments }).map((_, i) => (
        <div
          key={i}
          className={`flex-1 transition-colors duration-200 ${
            i < filled ? 'bg-black dark:bg-white' : 'bg-gray-200 dark:bg-gray-800'
          }`}
        />
      ))}
    </div>
  );
}
```

### Mechanical Toggle

Industrial-style toggle with precise state indication:

**HTML/CSS**:
```html
<button class="mechanical-toggle" data-state="off">
  <span class="toggle-track">
    <span class="toggle-indicator"></span>
  </span>
  <span class="toggle-label">OFF</span>
</button>

<style>
.mechanical-toggle {
  display: flex;
  align-items: center;
  gap: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.toggle-track {
  position: relative;
  width: 48px;
  height: 24px;
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 2px;
}

.toggle-indicator {
  width: 18px;
  height: 18px;
  background: var(--fg-primary);
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.mechanical-toggle[data-state="on"] .toggle-indicator {
  transform: translateX(24px);
}

.toggle-label {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  letter-spacing: 0.1em;
}
</style>
```

### Dot Matrix Display

Retro digital display aesthetic:

**HTML/CSS**:
```html
<div class="dot-matrix">
  <span class="matrix-text">23:45</span>
</div>

<style>
.dot-matrix {
  background: var(--bg-secondary);
  padding: 16px 24px;
  border: 1px solid var(--border);
}

.matrix-text {
  font-family: 'Doto', 'Space Mono', monospace;
  font-size: 48px;
  font-weight: 400;
  letter-spacing: 0.1em;
  color: var(--fg-primary);
  text-shadow: 0 0 8px currentColor;
}
</style>
```

### Information Card

Clean, hierarchical card layout:

**HTML/CSS**:
```html
<div class="nothing-card">
  <div class="card-metadata">SYSTEM STATUS</div>
  <h3 class="card-title">All Systems Operational</h3>
  <p class="card-body">Last checked 2 minutes ago. No issues detected.</p>
  <div class="card-footer">
    <span class="footer-label">UPTIME</span>
    <span class="footer-value">99.97%</span>
  </div>
</div>

<style>
.nothing-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-metadata {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--fg-secondary);
  text-transform: uppercase;
}

.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--fg-primary);
}

.card-body {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: var(--fg-secondary);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.05em;
}

.footer-label {
  color: var(--fg-secondary);
}

.footer-value {
  color: var(--fg-primary);
}
</style>
```

## Platform-Specific Mappings

### SwiftUI Components

```swift
// Nothing Button
struct NothingButton: View {
    let label: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(label.uppercased())
                .font(.custom("SpaceMono", size: 12))
                .tracking(1.2)
                .padding(.horizontal, 24)
                .padding(.vertical, 12)
        }
        .foregroundColor(.primary)
        .background(Color.clear)
        .overlay(
            RoundedRectangle(cornerRadius: 0)
                .stroke(Color.primary, lineWidth: 1)
        )
    }
}

// Nothing Card
struct NothingCard<Content: View>: View {
    let content: Content
    
    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            content
        }
        .padding(24)
        .background(Color(.systemGray6))
        .overlay(
            Rectangle()
                .stroke(Color(.separator), lineWidth: 1)
        )
    }
}
```

### React/Tailwind Components

```jsx
// Base configuration
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        grotesk: ['Space Grotesk', 'sans-serif'],
        mono: ['Space Mono', 'monospace'],
      },
      colors: {
        nothing: {
          bg: '#000000',
          surface: '#0A0A0A',
          border: '#1F1F1F',
          text: '#FFFFFF',
          muted: '#8C8C8C',
          accent: '#FF0000',
        }
      }
    }
  }
}

// Button component
export function NothingButton({ children, onClick, variant = 'primary' }) {
  return (
    <button
      onClick={onClick}
      className="px-6 py-3 font-mono text-xs tracking-widest uppercase border border-nothing-border bg-transparent text-nothing-text hover:bg-nothing-surface transition-colors"
    >
      {children}
    </button>
  );
}

// Card component
export function NothingCard({ metadata, title, children }) {
  return (
    <div className="p-6 bg-nothing-surface border border-nothing-border flex flex-col gap-3">
      {metadata && (
        <div className="font-mono text-[10px] tracking-wider uppercase text-nothing-muted">
          {metadata}
        </div>
      )}
      {title && (
        <h3 className="font-grotesk text-2xl font-bold leading-tight">
          {title}
        </h3>
      )}
      <div className="font-grotesk text-sm text-nothing-muted leading-relaxed">
        {children}
      </div>
    </div>
  );
}
```

## Common Workflows

### Generating a Complete Page

When asked to create a Nothing-style page:

1. Start with the base HTML structure including font imports
2. Apply the CSS token system
3. Build components using the three-layer hierarchy
4. Add mechanical/industrial details (segmented bars, borders, monospace labels)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nothing Interface</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #000000;
      --bg-secondary: #0A0A0A;
      --fg-primary: #FFFFFF;
      --fg-secondary: #8C8C8C;
      --border: #1F1F1F;
      --accent: #FF0000;
    }
    
    @media (prefers-color-scheme: light) {
      :root {
        --bg-primary: #FFFFFF;
        --bg-secondary: #F5F5F5;
        --fg-primary: #000000;
        --fg-secondary: #737373;
        --border: #E0E0E0;
      }
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      background: var(--bg-primary);
      color: var(--fg-primary);
      font-family: 'Space Grotesk', sans-serif;
      line-height: 1.5;
    }
  </style>
</head>
<body>
  <!-- Component markup here -->
</body>
</html>
```

### Creating Custom Components

Follow this pattern for any new component:

1. **Structure**: Minimal, semantic HTML
2. **Typography**: Use display/body/metadata layers
3. **Colors**: Only token variables, never hardcoded
4. **Spacing**: Multiples of 8px base unit
5. **Motion**: Cubic bezier easing, 200-300ms duration
6. **States**: Clear visual feedback (borders, fills, transforms)

## Troubleshooting

### Fonts Not Loading

Ensure font imports are in the `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

For Doto (dot matrix font), use:
```html
<link href="https://fonts.googleapis.com/css2?family=Doto:wght@400&display=swap" rel="stylesheet">
```

### Dark Mode Not Working

Check that CSS custom properties use the media query:

```css
@media (prefers-color-scheme: light) {
  :root {
    --bg-primary: #FFFFFF;
    /* ...other light mode tokens */
  }
}
```

### Components Look Too Rounded

Nothing design uses **zero border radius** (perfectly square). Remove any `border-radius` properties.

### Spacing Feels Off

Stick to the 8px spacing scale strictly. Use `--space-*` variables or multiples of 8px. No arbitrary values.

### Text Hierarchy Unclear

Review the three-layer system:
- **Display** (32px+, bold, Space Grotesk): One per screen
- **Body** (14-16px, regular, Space Grotesk): Main content
- **Metadata** (10-12px, uppercase, Space Mono): Labels and technical info

## Reference Files

The skill includes three reference documents in the `references/` folder:

- `tokens.md`: Complete color, typography, spacing, and motion token system
- `components.md`: Full component library with variants and states
- `platform-mapping.md`: CSS, SwiftUI, and React implementation patterns

When generating UI, consult these references to maintain design system consistency.

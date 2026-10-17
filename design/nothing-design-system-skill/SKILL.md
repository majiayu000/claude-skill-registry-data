---
name: nothing-design-system-skill
description: Generate UI components in Nothing's design language — monochrome, typographic, industrial aesthetic with Swiss typography and mechanical interface elements
triggers:
  - "use nothing design style"
  - "create a nothing-style component"
  - "generate UI in nothing design language"
  - "apply nothing design system"
  - "make this look like nothing phone UI"
  - "design with nothing aesthetic"
  - "build with nothing design principles"
  - "nothing design tokens"
---

# Nothing Design System Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A Claude Code skill for generating UI components inspired by Nothing's visual language. Creates monochrome, typographic, industrial interfaces with Swiss typography, OLED blacks, segmented progress bars, and dot-matrix motifs.

## What It Does

This skill provides a complete design system that enforces:

- **Three-layer visual hierarchy**: Display, body, metadata (nothing more)
- **Monochrome palette**: True blacks (#000000) for OLED, pure whites, controlled grays
- **Typography stack**: Space Grotesk (display), Space Mono (mono), Doto (dot-matrix)
- **Mechanical components**: Segmented progress bars, industrial toggles, instrument-style widgets
- **Multi-platform output**: HTML/CSS, SwiftUI, or React/Tailwind

## Installation

```sh
# Clone the repository
git clone https://github.com/dominikmartn/nothing-design-skill.git

# Copy to Claude Code skills directory
cp -r nothing-design-skill/nothing-design ~/.claude/skills/

# Restart Claude Code to load the skill
```

Verify installation by typing `/nothing-design` in Claude Code.

## Core Design Tokens

### Color System

```css
/* Dark Mode (Primary) */
--nothing-black: #000000;        /* OLED black, backgrounds */
--nothing-white: #FFFFFF;        /* Text, borders, icons */
--nothing-gray-10: #1A1A1A;      /* Subtle elevation */
--nothing-gray-20: #333333;      /* Component backgrounds */
--nothing-gray-40: #666666;      /* Secondary text */
--nothing-gray-60: #999999;      /* Tertiary text */
--nothing-red: #FF0000;          /* Accent, alerts */

/* Light Mode */
--nothing-bg-light: #FFFFFF;
--nothing-text-light: #000000;
--nothing-gray-light-80: #CCCCCC;
--nothing-gray-light-90: #E5E5E5;
```

### Typography Scale

```css
/* Display - Space Grotesk */
--font-display: 'Space Grotesk', -apple-system, system-ui, sans-serif;
--text-xl: 48px / 1.1;           /* Hero */
--text-lg: 32px / 1.2;           /* Section headers */
--text-md: 24px / 1.3;           /* Card titles */

/* Body - Space Grotesk */
--text-base: 16px / 1.5;         /* Body text */
--text-sm: 14px / 1.4;           /* Secondary */
--text-xs: 12px / 1.3;           /* Metadata */

/* Mono - Space Mono */
--font-mono: 'Space Mono', 'SF Mono', monospace;

/* Dot Matrix - Doto */
--font-dot: 'Doto', monospace;
```

### Spacing System

```css
--space-1: 4px;   /* Micro */
--space-2: 8px;   /* Small */
--space-3: 12px;  /* Base */
--space-4: 16px;  /* Medium */
--space-6: 24px;  /* Large */
--space-8: 32px;  /* XL */
--space-12: 48px; /* XXL */
```

## Component Patterns

### HTML/CSS Examples

#### Button

```html
<button class="nothing-btn">
  <span class="nothing-btn-label">CONTINUE</span>
</button>

<style>
.nothing-btn {
  background: #000000;
  border: 1px solid #FFFFFF;
  color: #FFFFFF;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 120ms cubic-bezier(0.4, 0, 0.2, 1);
}

.nothing-btn:hover {
  background: #FFFFFF;
  color: #000000;
}

.nothing-btn:active {
  transform: scale(0.98);
}
</style>
```

#### Segmented Progress Bar

```html
<div class="nothing-progress">
  <div class="nothing-progress-segments">
    <div class="segment active"></div>
    <div class="segment active"></div>
    <div class="segment active"></div>
    <div class="segment"></div>
    <div class="segment"></div>
  </div>
  <span class="nothing-progress-label">60%</span>
</div>

<style>
.nothing-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nothing-progress-segments {
  display: flex;
  gap: 4px;
  flex: 1;
}

.segment {
  height: 4px;
  background: #333333;
  flex: 1;
  transition: background 200ms;
}

.segment.active {
  background: #FFFFFF;
}

.nothing-progress-label {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  color: #999999;
  min-width: 40px;
}
</style>
```

#### Card Component

```html
<div class="nothing-card">
  <div class="nothing-card-header">
    <h3 class="nothing-card-title">SYSTEM STATUS</h3>
    <span class="nothing-card-meta">14:32:05</span>
  </div>
  <div class="nothing-card-body">
    <p>All systems operational. No alerts detected.</p>
  </div>
</div>

<style>
.nothing-card {
  background: #000000;
  border: 1px solid #333333;
  padding: 24px;
}

.nothing-card-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #1A1A1A;
}

.nothing-card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #FFFFFF;
  margin: 0;
}

.nothing-card-meta {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  color: #666666;
}

.nothing-card-body {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #FFFFFF;
}
</style>
```

### SwiftUI Examples

#### Button

```swift
struct NothingButton: View {
    let label: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(label.uppercased())
                .font(.custom("SpaceGrotesk-Medium", size: 14))
                .tracking(0.7)
                .foregroundColor(.white)
                .padding(.horizontal, 24)
                .padding(.vertical, 12)
                .background(Color.black)
                .overlay(
                    RoundedRectangle(cornerRadius: 0)
                        .stroke(Color.white, lineWidth: 1)
                )
        }
        .buttonStyle(NothingButtonStyle())
    }
}

struct NothingButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .background(configuration.isPressed ? Color.white : Color.black)
            .foregroundColor(configuration.isPressed ? Color.black : Color.white)
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeInOut(duration: 0.12), value: configuration.isPressed)
    }
}
```

#### Progress Bar

```swift
struct NothingProgress: View {
    let progress: Double // 0.0 to 1.0
    let segments: Int = 5
    
    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<segments, id: \.self) { index in
                Rectangle()
                    .fill(index < Int(progress * Double(segments)) ? Color.white : Color(hex: "#333333"))
                    .frame(height: 4)
            }
            
            Text("\(Int(progress * 100))%")
                .font(.custom("SpaceMono-Regular", size: 12))
                .foregroundColor(Color(hex: "#999999"))
                .frame(width: 40)
        }
    }
}
```

### React/Tailwind Examples

#### Setup Tailwind Config

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'nothing-black': '#000000',
        'nothing-white': '#FFFFFF',
        'nothing-gray-10': '#1A1A1A',
        'nothing-gray-20': '#333333',
        'nothing-gray-40': '#666666',
        'nothing-gray-60': '#999999',
        'nothing-red': '#FF0000',
      },
      fontFamily: {
        'display': ['Space Grotesk', 'sans-serif'],
        'mono': ['Space Mono', 'monospace'],
        'dot': ['Doto', 'monospace'],
      },
      letterSpacing: {
        'nothing': '0.05em',
        'nothing-wide': '0.08em',
      },
    },
  },
}
```

#### Button Component

```jsx
export function NothingButton({ children, onClick, variant = 'primary' }) {
  return (
    <button
      onClick={onClick}
      className="
        bg-nothing-black border border-nothing-white text-nothing-white
        hover:bg-nothing-white hover:text-nothing-black
        active:scale-[0.98]
        font-display text-sm font-medium tracking-nothing uppercase
        px-6 py-3
        transition-all duration-[120ms] ease-out
      "
    >
      {children}
    </button>
  );
}
```

#### Card Component

```jsx
export function NothingCard({ title, meta, children }) {
  return (
    <div className="bg-nothing-black border border-nothing-gray-20 p-6">
      <div className="flex justify-between items-baseline mb-4 pb-3 border-b border-nothing-gray-10">
        <h3 className="font-display text-sm font-medium tracking-nothing-wide uppercase text-nothing-white">
          {title}
        </h3>
        {meta && (
          <span className="font-mono text-xs text-nothing-gray-40">
            {meta}
          </span>
        )}
      </div>
      <div className="font-display text-base leading-relaxed text-nothing-white">
        {children}
      </div>
    </div>
  );
}
```

## Key Design Principles

### 1. Visual Hierarchy (Three Layers Only)

```
DISPLAY   → Headers, titles, key actions
BODY      → Primary content, readable text
METADATA  → Timestamps, labels, secondary info
```

### 2. Motion & Transitions

```css
/* Fast, mechanical transitions */
--timing-fast: 120ms;
--timing-base: 200ms;
--timing-slow: 300ms;
--easing: cubic-bezier(0.4, 0, 0.2, 1);
```

### 3. Borders & Dividers

- Always 1px solid
- Use `#333333` for subtle dividers
- Use `#FFFFFF` for strong emphasis
- Never rounded corners (stay industrial)

### 4. Interactive States

```css
/* Hover */
element:hover {
  background: invert;
  color: invert;
}

/* Active */
element:active {
  transform: scale(0.98);
}

/* Focus */
element:focus {
  outline: 1px solid #FFFFFF;
  outline-offset: 2px;
}
```

## Common Patterns

### Data Table

```html
<table class="nothing-table">
  <thead>
    <tr>
      <th>PARAMETER</th>
      <th>VALUE</th>
      <th>STATUS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Core Temp</td>
      <td class="mono">42°C</td>
      <td>OK</td>
    </tr>
  </tbody>
</table>

<style>
.nothing-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Space Grotesk', sans-serif;
}

.nothing-table th {
  text-align: left;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #666666;
  padding: 12px 16px;
  border-bottom: 1px solid #333333;
}

.nothing-table td {
  font-size: 14px;
  color: #FFFFFF;
  padding: 16px;
  border-bottom: 1px solid #1A1A1A;
}

.nothing-table .mono {
  font-family: 'Space Mono', monospace;
}
</style>
```

### Toggle Switch

```html
<label class="nothing-toggle">
  <input type="checkbox">
  <span class="nothing-toggle-track">
    <span class="nothing-toggle-thumb"></span>
  </span>
  <span class="nothing-toggle-label">NOTIFICATIONS</span>
</label>

<style>
.nothing-toggle {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.nothing-toggle input {
  display: none;
}

.nothing-toggle-track {
  position: relative;
  width: 48px;
  height: 24px;
  background: #1A1A1A;
  border: 1px solid #333333;
  transition: background 200ms;
}

.nothing-toggle-thumb {
  position: absolute;
  left: 2px;
  top: 2px;
  width: 18px;
  height: 18px;
  background: #666666;
  transition: all 200ms;
}

.nothing-toggle input:checked ~ .nothing-toggle-track {
  background: #000000;
  border-color: #FFFFFF;
}

.nothing-toggle input:checked ~ .nothing-toggle-track .nothing-toggle-thumb {
  left: 26px;
  background: #FFFFFF;
}

.nothing-toggle-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #FFFFFF;
}
</style>
```

## Troubleshooting

### Fonts not loading

Ensure fonts are properly imported:

```html
<!-- HTML -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

```css
/* CSS */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');
```

### OLED blacks not working

Ensure root background is true black:

```css
:root, body, html {
  background: #000000;
  color: #FFFFFF;
}
```

### Components look too rounded

Nothing design uses **zero** border radius. Remove all `border-radius` declarations:

```css
/* ❌ Wrong */
border-radius: 8px;

/* ✅ Correct */
border-radius: 0;
```

### Text hierarchy unclear

Stick to the three-layer system:

```css
/* Display - 24px+, bold, uppercase, tight spacing */
.display { font-size: 24px; font-weight: 700; text-transform: uppercase; }

/* Body - 14-16px, normal weight */
.body { font-size: 16px; font-weight: 400; }

/* Metadata - 12px, mono, muted color */
.meta { font-size: 12px; font-family: 'Space Mono'; color: #666666; }
```

## Usage with Claude Code

Trigger the skill naturally:

- "Create a nothing-style dashboard"
- "Generate a progress bar in nothing design"
- "Apply nothing design tokens to this component"
- "Make this button look industrial like nothing phone"

The skill will automatically apply the design system principles and generate code in your requested format (HTML/CSS, SwiftUI, or React).

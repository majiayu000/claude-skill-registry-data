---
name: nothing-design-ui-skill
description: Generate UI components in Nothing's monochrome, typographic, industrial design language with Swiss typography and OLED-optimized aesthetics
triggers:
  - "use nothing design style"
  - "create a nothing UI component"
  - "design this in nothing style"
  - "apply nothing design language"
  - "make this look like nothing phone"
  - "generate nothing-style interface"
  - "use industrial monochrome design"
  - "create swiss typography UI"
---

# Nothing Design UI Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A design system skill for generating UI components in Nothing's distinctive visual language: monochrome aesthetics, Swiss typography, industrial precision, and OLED-optimized contrast.

## What This Skill Does

The Nothing Design Skill enables AI agents to generate UI components following Nothing's design principles:

- **Three-layer visual hierarchy**: Display, body, metadata — no more complexity
- **Monochrome foundation**: OLED blacks (#000000), pure whites (#FFFFFF), precise grays
- **Typography-first**: Space Grotesk (display), Space Mono (code/data), Doto (dot-matrix accents)
- **Industrial components**: Segmented progress bars, mechanical toggles, instrument-style widgets
- **Multi-platform output**: HTML/CSS, SwiftUI, React/Tailwind

## Installation

1. Clone the repository:
```sh
git clone https://github.com/dominikmartn/nothing-design-skill.git
```

2. Copy the skill to your Claude Code skills directory:
```sh
cp -r nothing-design-skill/nothing-design ~/.claude/skills/
```

3. Restart Claude Code to load the skill.

## Design Principles

### Visual Hierarchy

**Three layers only:**
- **Display**: Primary information (28-48px, Space Grotesk Bold)
- **Body**: Secondary content (14-16px, Space Grotesk Regular)
- **Metadata**: Tertiary data (11-12px, Space Mono)

### Color System

**Dark Mode (default):**
```css
--nothing-black: #000000;
--nothing-white: #FFFFFF;
--nothing-gray-100: #1A1A1A;
--nothing-gray-200: #2D2D2D;
--nothing-gray-300: #404040;
--nothing-gray-400: #737373;
--nothing-gray-500: #A6A6A6;
--nothing-red: #FF0000;
```

**Light Mode:**
```css
--nothing-white: #FFFFFF;
--nothing-black: #000000;
--nothing-gray-100: #F5F5F5;
--nothing-gray-200: #E5E5E5;
--nothing-gray-300: #D4D4D4;
--nothing-gray-400: #A3A3A3;
--nothing-gray-500: #737373;
```

### Typography Stack

```css
--font-display: 'Space Grotesk', -apple-system, system-ui, sans-serif;
--font-body: 'Space Grotesk', -apple-system, system-ui, sans-serif;
--font-mono: 'Space Mono', 'SF Mono', Consolas, monospace;
--font-doto: 'Doto', monospace; /* dot-matrix style */
```

### Spacing Scale

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 24px;
--space-6: 32px;
--space-7: 48px;
--space-8: 64px;
```

## Component Patterns

### Button (HTML/CSS)

```html
<button class="nothing-btn">
  <span class="nothing-btn__label">Continue</span>
  <span class="nothing-btn__meta">⌘K</span>
</button>

<style>
.nothing-btn {
  background: var(--nothing-white);
  color: var(--nothing-black);
  border: 1px solid var(--nothing-white);
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 500;
  padding: 12px 24px;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.nothing-btn:hover {
  background: var(--nothing-gray-200);
  border-color: var(--nothing-gray-200);
}

.nothing-btn__meta {
  font-family: var(--font-mono);
  font-size: 11px;
  opacity: 0.6;
}
</style>
```

### Segmented Progress Bar (HTML/CSS)

```html
<div class="nothing-progress" data-segments="10" data-value="7">
  <div class="nothing-progress__track">
    <div class="nothing-progress__fill"></div>
  </div>
  <div class="nothing-progress__meta">70%</div>
</div>

<style>
.nothing-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nothing-progress__track {
  flex: 1;
  height: 8px;
  background: var(--nothing-gray-200);
  position: relative;
  background-image: repeating-linear-gradient(
    90deg,
    transparent,
    transparent calc(10% - 1px),
    var(--nothing-black) calc(10% - 1px),
    var(--nothing-black) 10%
  );
}

.nothing-progress__fill {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 70%;
  background: var(--nothing-white);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nothing-progress__meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--nothing-gray-400);
  min-width: 40px;
  text-align: right;
}
</style>
```

### Card Component (React/Tailwind)

```jsx
export function NothingCard({ title, value, meta, trend }) {
  return (
    <div className="bg-black border border-white/10 p-6">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-['Space_Grotesk'] text-sm text-white/60 mb-2">
            {title}
          </h3>
          <p className="font-['Space_Grotesk'] text-4xl font-bold text-white">
            {value}
          </p>
        </div>
        {trend && (
          <span className="font-['Space_Mono'] text-xs text-white/40">
            {trend}
          </span>
        )}
      </div>
      {meta && (
        <p className="font-['Space_Mono'] text-xs text-white/40 mt-4">
          {meta}
        </p>
      )}
    </div>
  );
}

// Usage
<NothingCard
  title="Active Users"
  value="2,340"
  trend="+12%"
  meta="Updated 2 min ago"
/>
```

### Toggle Switch (SwiftUI)

```swift
struct NothingToggle: View {
    @Binding var isOn: Bool
    let label: String
    
    var body: some View {
        HStack(spacing: 16) {
            Text(label)
                .font(.custom("SpaceGrotesk-Regular", size: 14))
                .foregroundColor(.white)
            
            Spacer()
            
            Button(action: { isOn.toggle() }) {
                ZStack {
                    RoundedRectangle(cornerRadius: 0)
                        .fill(isOn ? Color.white : Color(hex: "#2D2D2D"))
                        .frame(width: 48, height: 24)
                    
                    Rectangle()
                        .fill(Color.black)
                        .frame(width: 20, height: 20)
                        .offset(x: isOn ? 10 : -10)
                }
            }
            .animation(.easeInOut(duration: 0.2), value: isOn)
        }
        .padding(16)
        .background(Color.black)
    }
}

// Usage
@State private var notificationsEnabled = true

NothingToggle(
    isOn: $notificationsEnabled,
    label: "Notifications"
)
```

### Data Table (HTML/CSS)

```html
<table class="nothing-table">
  <thead>
    <tr>
      <th>Device</th>
      <th>Status</th>
      <th>Battery</th>
      <th>Updated</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <div class="nothing-table__primary">Phone (1)</div>
        <div class="nothing-table__meta">Serial: NK1234567</div>
      </td>
      <td><span class="nothing-badge nothing-badge--active">Active</span></td>
      <td>
        <div class="nothing-progress" data-value="87">
          <div class="nothing-progress__track">
            <div class="nothing-progress__fill" style="width: 87%"></div>
          </div>
          <div class="nothing-progress__meta">87%</div>
        </div>
      </td>
      <td class="nothing-table__mono">2 min ago</td>
    </tr>
  </tbody>
</table>

<style>
.nothing-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-display);
  color: var(--nothing-white);
}

.nothing-table th {
  text-align: left;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 16px;
  border-bottom: 1px solid var(--nothing-gray-200);
  color: var(--nothing-gray-400);
}

.nothing-table td {
  padding: 16px;
  border-bottom: 1px solid var(--nothing-gray-100);
  font-size: 14px;
}

.nothing-table__primary {
  font-weight: 500;
  margin-bottom: 4px;
}

.nothing-table__meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--nothing-gray-400);
}

.nothing-table__mono {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--nothing-gray-400);
}

.nothing-badge {
  display: inline-block;
  padding: 4px 8px;
  font-size: 11px;
  font-family: var(--font-mono);
  border: 1px solid var(--nothing-gray-300);
}

.nothing-badge--active {
  border-color: var(--nothing-white);
  color: var(--nothing-white);
}
</style>
```

## Motion & Transitions

Use cubic-bezier easing for mechanical precision:

```css
/* Standard easing */
transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

/* Enter animations */
transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);

/* Exit animations */
transition: all 0.2s cubic-bezier(0.4, 0, 1, 1);
```

## Usage Patterns

### Requesting Nothing-style Components

**Example prompts:**
- "Create a settings panel in Nothing design style"
- "Design a dashboard card using nothing design language"
- "Make this form look like Nothing Phone UI"
- "Apply Nothing's industrial aesthetic to this table"

### Output Formats

Specify your preferred format:
- **HTML/CSS**: Default, vanilla implementation
- **React/Tailwind**: `"Generate this as a React component with Tailwind"`
- **SwiftUI**: `"Create this in SwiftUI for iOS"`

### Configuration Options

When requesting components, you can specify:
- **Color mode**: "dark mode" (default) or "light mode"
- **Typography**: "use dot-matrix style" for Doto font accents
- **Density**: "compact" (tighter spacing) or "comfortable" (default)
- **Accent color**: "use red accent" for alert states

## Common Troubleshooting

### Fonts Not Loading

Include font imports in your HTML or CSS:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

For Doto (dot-matrix), you may need to self-host or use alternatives like "Courier Prime Code".

### Dark Mode Not Working

Ensure root variables are set:

```css
:root {
  color-scheme: dark;
  background: #000000;
  color: #FFFFFF;
}
```

### Progress Bar Segments Not Aligned

Adjust segment count in the gradient:

```css
/* For 10 segments */
background-image: repeating-linear-gradient(
  90deg,
  transparent,
  transparent calc(10% - 1px),
  var(--nothing-black) calc(10% - 1px),
  var(--nothing-black) 10%
);
```

### Components Look Too Cramped

Increase spacing scale usage:

```css
padding: var(--space-4) var(--space-5); /* 16px 24px */
gap: var(--space-4); /* 16px */
```

## Real-World Example: Dashboard

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nothing Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --nothing-black: #000000;
      --nothing-white: #FFFFFF;
      --nothing-gray-100: #1A1A1A;
      --nothing-gray-200: #2D2D2D;
      --nothing-gray-400: #737373;
      --space-4: 16px;
      --space-5: 24px;
      --space-6: 32px;
      --font-display: 'Space Grotesk', sans-serif;
      --font-mono: 'Space Mono', monospace;
    }
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      background: var(--nothing-black);
      color: var(--nothing-white);
      font-family: var(--font-display);
      padding: var(--space-6);
    }
    
    .dashboard {
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .dashboard__header {
      margin-bottom: var(--space-6);
    }
    
    .dashboard__title {
      font-size: 48px;
      font-weight: 700;
      margin-bottom: 8px;
    }
    
    .dashboard__meta {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--nothing-gray-400);
    }
    
    .dashboard__grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: var(--space-5);
    }
    
    .card {
      background: var(--nothing-gray-100);
      border: 1px solid var(--nothing-gray-200);
      padding: var(--space-5);
    }
    
    .card__label {
      font-size: 12px;
      color: var(--nothing-gray-400);
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .card__value {
      font-size: 40px;
      font-weight: 700;
      margin-bottom: 16px;
    }
    
    .card__footer {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--nothing-gray-400);
    }
  </style>
</head>
<body>
  <div class="dashboard">
    <header class="dashboard__header">
      <h1 class="dashboard__title">System Overview</h1>
      <p class="dashboard__meta">Updated 12 seconds ago • 23:14:52 UTC</p>
    </header>
    
    <div class="dashboard__grid">
      <div class="card">
        <div class="card__label">Active Users</div>
        <div class="card__value">2,340</div>
        <div class="card__footer">+12% from yesterday</div>
      </div>
      
      <div class="card">
        <div class="card__label">System Load</div>
        <div class="card__value">47%</div>
        <div class="card__footer">Normal operating range</div>
      </div>
      
      <div class="card">
        <div class="card__label">Uptime</div>
        <div class="card__value">99.97%</div>
        <div class="card__footer">47 days, 12 hours</div>
      </div>
    </div>
  </div>
</body>
</html>
```

## Reference Files

The skill includes detailed reference files:
- `references/tokens.md`: Complete design token system
- `references/components.md`: All component specifications
- `references/platform-mapping.md`: Platform-specific implementations

Use these references when generating complex or custom components.

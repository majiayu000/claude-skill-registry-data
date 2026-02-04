---
name: "diagram-drawing"
description: "Creates animated diagrams and professional infographics using Chart.js 4.x with: Auto-activates when user mentions: diagram, chart, graph, infographic, visualization, data visualization, data viz, line chart, bar chart, pie chart"
---

# Diagram Drawing

## MANDATORY PRE-WORK CHECKLIST

**YOU MUST complete this checklist BEFORE applying this skill:**

**[ ] 1. Read Task Decomposition Override Section**
   - **WHY**: Understand the PROHIBITED sequence (Generic approach with default fonts/colors)
   - **WHY**: Understand the MANDATORY sequence (Design-First Data Visualization with 3 decisions)
   - **CONSEQUENCE**: Skipping = generic "AI slop" diagrams with Inter/Roboto + rainbow gradients

**[ ] 2. Acknowledge Output Format Requirement**
   - **FORMAT REQUIRED**:
     ```
     Diagram Drawing Applied:
     - Design Theme: [Theme + rationale]
     - Typography: [Font family + sizing hierarchy]
     - Color Strategy: [Palette approach + values]
     ```
   - **WHY**: Hook validation requires this exact format
   - **CONSEQUENCE**: Missing acknowledgment = architecture violation

**[ ] 3. Identify Diagram-Specific Requirements**
   - **Design Theme**: Choose distinctive theme (NOT generic Material Design - use Technical/Editorial/Minimal/Bold)
   - **Typography Hierarchy**: ≥12px labels, NO Inter/Roboto/Arial alone (use IBM Plex Sans, Space Grotesk, Source Sans)
   - **Animation Strategy**: ≤2 seconds initial reveal, respects prefers-reduced-motion, GPU-accelerated
   - **Export Format**: SVG preferred (scalable), PNG for raster needs, PDF for print
   - **Accessibility**: Alt text, ARIA labels, keyboard navigation, colorblind-safe palettes
   - **WHY**: Generic themes + poor typography + excessive animation = unprofessional diagrams undermining credibility
   - **CONSEQUENCE**: Ignoring = charts that look auto-generated, fail accessibility standards, hurt brand perception

**[ ] 4. Check for Multi-Skill Compositions (v5.5.0)**
   - **IF diagram-drawing + data-visualization-designer + design-excellence loaded**:
     - YOU MUST apply all three skills in conjunction (not isolation)
     - Composition: visual-design-excellence (3.2x quality improvement)
     - This skill = Chart.js implementation, data-viz = truthful design, design-excellence = aesthetics
   - **CONSEQUENCE**: Single-skill usage when composition available = suboptimal quality

**✅ ALL BOXES CHECKED = Ready to proceed to Task Decomposition Override**
**❌ SKIPPING THIS CHECKLIST = Claiming "Diagram Drawing Applied" while generating generic charts**

---

## Task Decomposition Override (v5.4.0)

When this skill applies (diagram/chart/infographic request), **DO NOT use your default task decomposition.**

### ❌ PROHIBITED SEQUENCE (Generic approach - low quality):
1. TodoWrite for planning
2. Gather requirements
3. Create generic SVG/Canvas/PNG
4. Use default fonts (Inter, Roboto, Arial)
5. Use rainbow gradients or generic colors

### ✅ MANDATORY SEQUENCE (Design-First Data Visualization):

**Phase 1: Design System Decisions** (Make 3 explicit decisions)
1. **Design Theme Selection**: Choose theme matching content context
   - Reference: Skill "Themes for Infographics" section
   - Output: Selected theme with rationale (e.g., "Technical: monospace fonts, dark background, neon accents for developer dashboard")

2. **Typography Strategy**: Select distinctive fonts for labels/titles
   - Reference: Skill "Typography for Charts & Infographics" section
   - Output: Font family with sizing (e.g., "IBM Plex Sans: title 20px/700, axis 12px/400")

3. **Color Strategy**: Define palette approach (Sequential/Diverging/Categorical)
   - Reference: Skill "Color Schemes for Data" section
   - Output: Palette type with values (e.g., "Sequential: blue #3b82f6 → #1e3a8a, 5 steps, colorblind-safe")

**Output Acknowledgment After Phase 1:**
```
Diagram Drawing Applied:
- Design Theme: [Theme + rationale]
- Typography: [Font family + sizing hierarchy]
- Color Strategy: [Palette approach + values]
```

**Phase 2: Implementation** (Apply Phase 1 decisions)
4. Configure Chart.js with theme-specific settings
5. Implement typography hierarchy (title/axis/legend fonts)
6. Apply color palette with accessibility support
7. Add animation with prefers-reduced-motion support
8. Generate alt text for accessibility

**Phase 3: Validation** (Verify quality criteria)
9. Verify typography: NO Inter/Roboto/Arial/Helvetica, minimum 12px labels
10. Verify color: 4.5:1 contrast minimum, colorblind-safe testing
11. Verify accessibility: alt text present, reduced-motion respected
12. Verify animation: ≤2 seconds initial reveal, easeOut timing

**IF you use ❌ sequence instead of ✅ sequence = ARCHITECTURE VIOLATION**

**Rationale:** Generic diagrams signal "AI slop." Professional diagrams require design-first thinking with distinctive aesthetics. The 3-phase approach GUARANTEES: (1) explicit design decisions before implementation, (2) theme-consistent application, (3) measurable accessibility compliance. This is MANDATORY for quality output.

---

## Language Standards (v5.4.0)

**YOU MUST use directive language throughout this skill:**

**Required Directives:**
- ✅ "YOU MUST use", "DO NOT use", "ALWAYS", "NEVER", "MANDATORY", "PROHIBITED", "REQUIRED"
- ❌ Never: "should", "consider", "might", "could", "try to", "it's recommended", "please", "ideally"

**Section Headers:**
- ✅ "Required Standards", "Rules", "Requirements", "Anti-Patterns to Avoid"
- ❌ "Best Practices", "Guidelines", "Recommendations", "Suggestions"

**Examples of Directive Transformation:**
- ❌ "Consider using X" → ✅ "YOU MUST use X"
- ❌ "You should avoid Y" → ✅ "DO NOT use Y (PROHIBITED)"
- ❌ "It's recommended to Z" → ✅ "MANDATORY: Z"
- ❌ "Try to follow pattern P" → ✅ "ALWAYS follow pattern P"

**Enforcement Note:** Skills with weak language will be rejected by pre-tool-use-write.ts hook.

---

## Design Excellence for Data Visualization

Data visualization design is functional communication—typography, color, and layout directly impact comprehension. Avoid generic "AI slop" aesthetics that undermine credibility.

### Typography for Charts & Infographics

Chart labels and titles instantly signal professionalism. **Avoid generic fonts.**

**Never use for chart labels/titles:**
- ❌ Inter, Roboto, Arial, Helvetica (signal "AI slop" or placeholder work)
- ❌ Default system fonts

**YOU MUST use distinctive choices:**
- **Code/Technical aesthetic**: JetBrains Mono, Fira Code (data-driven, precise)
- **Editorial/Report aesthetic**: IBM Plex Sans, Source Sans 3 (readable, authoritative)
- **Modern/Distinctive**: Space Grotesk, Unbounded (memorable, confident)

**Typography principles for data viz:**
- **Readability first**: Minimum 12px for axis labels, 14px+ for titles
- **Weight hierarchy**: Title (700-800), axis labels (400-500), annotations (300-400)
- **Consistency**: Use same font family throughout chart (not multiple fonts)
- **Alignment**: Left-align y-axis labels, center titles, bottom-align x-axis labels

### Color Schemes for Data

Color communicates meaning and directs attention in data visualization.

**Semantic data colors (follow conventions):**
- **Positive/Growth**: Green (#10b981, #22c55e)
- **Negative/Decline**: Red (#ef4444, #dc2626)
- **Neutral/Baseline**: Blue (#3b82f6, #2563eb)
- **Warning/Attention**: Orange/Yellow (#f59e0b, #eab308)

**Accessibility requirements:**
- **Don't rely on color alone**: Use patterns/textures + color for differentiation
- **Contrast**: Background-to-foreground ratio 4.5:1 minimum
- **Colorblind-safe palettes**: Use tools like ColorBrewer, avoid red-green-only combinations
- **Test**: Simulate deuteranopia (red-green), protanopia (red-green), tritanopia (blue-yellow)

**Palette strategies:**
- **Sequential** (single hue progression): Low to high intensity → quantity/magnitude
- **Diverging** (two hues from center): Negative ← neutral → positive
- **Categorical** (distinct hues): Unordered categories (use 5-7 max for clarity)

**Avoid:**
- ❌ Rainbow gradients (hard to interpret value)
- ❌ Clichéd purple-to-pink gradients (signal generic AI output)
- ❌ Too many colors (>7 in single chart = cognitive overload)
- ❌ Low saturation pastels (hard to differentiate)

### Themes for Infographics

Commit to a cohesive aesthetic that matches content context.

**Theme inspiration:**
- **Corporate/Professional**: Clean, trustworthy, muted colors, sans-serif, grid layouts
- **Technical/Developer**: Monospace fonts, terminal aesthetics, dark backgrounds, neon accents
- **Editorial/Report**: Serif titles, authoritative, newspaper-inspired, strong hierarchy
- **Cyberpunk**: Neon accents (#00ff00, #ff00ff), dark backgrounds, glitch effects
- **Retro/Vintage**: Muted 70s palette, textured backgrounds, nostalgic typography

### Motion & Animation for Charts

Animation guides attention and reveals data progressively.

**Purposeful chart animations:**
- **Initial reveal**: Stagger data point appearance (not all at once)
- **Data updates**: Smooth transitions when values change (300-600ms duration)
- **Hover interactions**: Immediate feedback (<100ms), subtle scale/highlight
- **Progress indicators**: Show loading state while chart renders

**Respect reduced motion:**
```javascript
animation: {
  duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 800
}
```

**Avoid:**
- ❌ Overly long animations (>2 seconds for initial reveal)
- ❌ Bouncing/elastic easing (unprofessional for data viz)
- ❌ Continuous looping animations (distracting)
- ❌ Ignoring `prefers-reduced-motion` accessibility setting

---

## Chart.js Technical Reference

### Usage

```typescript
renderDiagram({
  type: 'line' | 'bar' | 'pie' | 'doughnut' | 'scatter' | 'bubble' | 'radar',
  data: {
    labels: string[],
    datasets: Array<{
      label: string,
      data: number[]
    }>
  },
  export: {
    format: 'png' | 'svg' | 'pdf',
    width: number,
    height: number
  }
})
```

### Features

- **5 chart types**: line, bar, pie, scatter, radar
- **3 export formats**: PNG (1x/2x), SVG, PDF
- **5 presets**: default, minimal, bold, print, dark
- **Auto alt text**: Generates descriptive text with trends
- **Accessibility**: Reduced motion support, contrast checking
- **Performance**: Data decimation for large datasets

### Example Chart.js Configuration

```javascript
options: {
  plugins: {
    title: {
      display: true,
      text: 'Monthly Revenue Growth',
      font: {
        family: 'IBM Plex Sans',
        size: 20,
        weight: '700'
      },
      color: '#e2e8f0'
    },
    legend: {
      labels: {
        font: {
          family: 'IBM Plex Sans',
          size: 14,
          weight: '500'
        }
      }
    }
  },
  scales: {
    x: {
      grid: { color: 'rgba(100, 116, 139, 0.1)' },
      ticks: { font: { family: 'IBM Plex Sans', size: 12 } }
    },
    y: {
      grid: { color: 'rgba(100, 116, 139, 0.1)' },
      ticks: { font: { family: 'IBM Plex Sans', size: 12 } }
    }
  },
  animation: {
    duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 800,
    easing: 'easeOutQuart'
  }
}
```

---

## Resources (Progressive Loading)

**Typography**: Load `@resources/typography-for-data.md` for:
- Font pairing strategies
- Hierarchy principles
- Accessibility guidelines

**Themes**: Load `@resources/chart-theme-gallery.md` for:
- 5 complete theme configurations
- Copy-paste Chart.js configs
- Color palette definitions

**Examples**: Load `@resources/diagram-examples.md` for:
- Production-ready examples
- Before/after comparisons
- Anti-pattern demonstrations

**Accessibility**: Load `@resources/wcag-compliance-charts.md` for:
- WCAG 2.1 AA compliance checklist
- Color contrast requirements
- Screen reader compatibility

---

## Anti-Patterns to Avoid

**Typography:**
- ❌ Inter, Roboto, Arial, Helvetica for chart labels
- ❌ Multiple font families in single chart
- ❌ Tiny labels (<10px)
- ❌ All-caps titles

**Color:**
- ❌ Rainbow gradients
- ❌ Purple-to-pink gradients
- ❌ Red-green only (colorblind unfriendly)
- ❌ Low contrast (<3:1)

**Animation:**
- ❌ Bouncing/elastic easing
- ❌ Continuous loops
- ❌ Ignoring prefers-reduced-motion
- ❌ >2 second animations

**Structure:**
- ❌ Too many data points (>50 without grouping)
- ❌ Missing axis labels
- ❌ No legend for multiple datasets
- ❌ Distracting backgrounds
---
name: "data-visualization-designer"
description: "Provides expert design guidance for creating truthful, clear, beautiful data visualizations. Focuses on **DESIGN DECISIONS ONLY**—chart selection, color strategy, visual encoding, and validation. Assumes data is accurate and prepared. Auto-activates when user mentions: data viz, dashboard, chart type, visualization, infographic"
---

# Data Visualization Designer

## MANDATORY PRE-WORK CHECKLIST

**YOU MUST complete this checklist BEFORE applying this skill:**

**[ ] 1. Read Task Decomposition Override Section**
   - **WHY**: Understand the PROHIBITED sequence (Implementation-First Antipattern)
   - **WHY**: Understand the MANDATORY sequence (Design-Decision Framework with 4 critical decisions)
   - **CONSEQUENCE**: Skipping = 30-50% redesign waste + accessibility failures + misleading visualizations

**[ ] 2. Acknowledge Output Format Requirement**
   - **FORMAT REQUIRED**:
     ```
     Data Viz Design Applied:
     - Brief: [Purpose + Audience + Success metric]
     - Chart Type: [Type] because [data structure + task]
     - Color: [Sequential/Diverging/Categorical] palette, [redundant encoding method]
     - Encoding: [Primary variable] → position, [Secondary] → [channel]
     ```
   - **WHY**: Hook validation requires this exact format
   - **CONSEQUENCE**: Missing acknowledgment = architecture violation

**[ ] 3. Identify Data Viz-Specific Requirements**
   - **Chart Type Justification**: Chart MUST match data structure AND task (NOT aesthetics or "what looks cool")
   - **Color Accessibility**: NO red-green only encoding, MUST use redundant channels (color + shape/pattern/label)
   - **Truthfulness Validation**: Y-axis starts at zero (bar charts) OR clearly labeled, no truncated axes to exaggerate
   - **Perceptual Hierarchy**: Position > Length > Angle > Area > Color (Cleveland & McGill research)
   - **Colorblind Safe**: Blue-Orange or Blue-Yellow palettes, test with simulators
   - **WHY**: Wrong chart type + color-only encoding + misleading axes = 83.5% viewer misinterpretation
   - **CONSEQUENCE**: Ignoring = unusable visualization that actively misleads decision-makers

**[ ] 4. Check for Multi-Skill Compositions (v5.5.0)**
   - **IF data-visualization-designer + design-excellence + diagram-drawing loaded**:
     - YOU MUST apply all three skills in conjunction (not isolation)
     - Composition: visual-design-excellence (3.2x quality improvement)
     - This skill = data encoding decisions, design-excellence = aesthetics, diagram = Chart.js code
   - **CONSEQUENCE**: Single-skill usage when composition available = suboptimal quality

**✅ ALL BOXES CHECKED = Ready to proceed to Task Decomposition Override**
**❌ SKIPPING THIS CHECKLIST = Claiming "Data Viz Design Applied" while creating misleading charts**

---

## Task Decomposition Override (v5.4.0)

When designing data visualizations, DO NOT use your default task decomposition.

### ❌ PROHIBITED SEQUENCE (Implementation-First Antipattern):
1. Jump straight to creating charts
2. Pick chart type based on aesthetics
3. Apply colors randomly
4. Add data and hope it works
5. Discover accessibility issues after completion

**Consequence**: Redesign waste (30-50% rework), accessibility failures, misleading visualizations, frustrated stakeholders.

### ✅ MANDATORY SEQUENCE (Design-Decision Framework):

**Phase 1: Design Decision** (Make 4 critical decisions)

1. **Establish Brief**:
   - Reference: Skill "The Foundation: Four-Element Framework"
   - Output: Purpose, audience, context, success metric documented

2. **Select Chart Type**:
   - Reference: Skill "Chart Type Selection" + @data-visualization-designer/resources/perceptual-accuracy-research.md
   - Output: Chart type with justification (comparison/relationship/distribution/composition)

3. **Design Color Strategy**:
   - Reference: Skill "Color Strategy"
   - Output: Palette type (sequential/diverging/categorical), colorblind-safe verification, redundant encoding plan

4. **Plan Visual Encoding**:
   - Reference: @data-visualization-designer/resources/perceptual-accuracy-research.md
   - Output: Which visual channels encode which variables (position > length > color)

**Output Acknowledgment After Phase 1:**
```
Data Viz Design Applied:
- Brief: [Purpose + Audience + Success metric]
- Chart Type: [Type] because [data structure + task]
- Color: [Sequential/Diverging/Categorical] palette, [redundant encoding method]
- Encoding: [Primary variable] → position, [Secondary] → [channel]
```

**Phase 2: Implementation** (Apply decisions)

5. Apply typography hierarchy (reference: @data-visualization-designer/resources/crap-principles-for-data.md)
6. Add strategic annotations (reference: @data-visualization-designer/resources/data-storytelling.md)
7. Optimize data-ink ratio (reference: @data-visualization-designer/resources/data-ink-optimization.md)
8. Implement design (hand off to diagram-drawing skill for Chart.js/D3.js code)

**Phase 3: Validation** (Verify quality)

9. Run truthfulness audit (reference: Skill "Critical Mistakes" - Fatal category)
10. Check accessibility (reference: Skill "Accessibility Requirements")
11. Validate against Quick Audit Checklist (reference: Skill "Quick Audit Before Publishing")

**IF you use ❌ sequence instead of ✅ sequence = ARCHITECTURE VIOLATION**

**Rationale**: Design decisions BEFORE implementation prevents 30-50% redesign waste. Establishes brief, justifies chart selection, ensures accessibility from start, enables validation against documented criteria. Quality guaranteed through checkable Phase 1 outputs.

---

## Language Standards (v5.4.0)

**YOU MUST use directive language throughout:**
- ✅ "YOU MUST use", "DO NOT use", "ALWAYS", "NEVER", "MANDATORY", "PROHIBITED"
- ❌ Never: "should", "consider", "might", "could", "try to"

**Enforcement**: Skills with weak language blocked by pre-tool-use-write.ts hook.

---

## The Foundation: Four-Element Framework

Every effective visualization requires these elements:

**Information** - Accurate, verified data (provided to you)

**Story** - The insight your visualization communicates

**Goal** - Specific purpose: persuade, enable decisions, communicate insights

**Visual Form** - How you encode meaning through visual channels (position, color, size, shape)

**YOU MUST establish all four elements before designing.** If any element is unclear, use AskUserQuestion tool to clarify. Missing elements create incomplete, ineffective visualizations.

### Brief Template

Answer these before starting:

**Purpose**: What specific question does this answer? What decision should it enable?

**Audience**: Who views this? Technical experts or general public? Visual literacy level?

**Context**: When/how will viewers access? Dashboard? Report? Publication? Mobile or desktop?

**Success Metric**: How do you know it succeeded? Comprehension in 5 seconds? Action taken? Decision made?

---

## Chart Type Selection

**YOU MUST match chart type to data structure and task, NOT aesthetics.**

### COMPARISON (How datasets differ)

**Few values (≤3)**: Bar/column chart
**Many values (4-10)**: Grouped bars or dot plot
**Many categories (>10)**: Horizontal bar chart (easier label reading)
**Time-based comparison**: Column chart

**❌ AVOID**: Pie charts (human vision terrible at comparing angles—10-30× less accurate than bars)

### RELATIONSHIP (How variables correspond)

**Two continuous variables**: Scatter plot
**Three dimensions**: Bubble chart (size = 3rd variable)
**Many comparisons**: Small multiples
**Correlation strength**: Scatter plot with regression line

**❌ AVOID**: Lines connecting scatter points (implies false temporal continuity)

### DISTRIBUTION (How data spreads)

**Single variable distribution**: Histogram or box plot
**Distribution over time**: Line chart
**Multiple distributions**: Small multiples or violin plots
**Pattern matrix**: Heatmap

**❌ AVOID**: 3D histograms (distorts perception), rainbow colormaps (creates false boundaries)

### COMPOSITION (Parts of whole)

**Static 2-5 categories**: Stacked bar chart (NOT pie)
**Changes over time**: Stacked area chart or waterfall
**Hierarchical data**: Treemap or sunburst
**Flow between categories**: Sankey diagram

**❌ AVOID**: Pie charts except rare cases (<5 categories, one slice >50%)

### Decision Matrix

| Data Structure | Task | Recommended Chart |
|----------------|------|-------------------|
| 1 categorical, 1 quantitative | Compare values | Bar chart |
| 2 categorical, 1 quantitative | Compare groups | Grouped/stacked bar |
| Time series, 1 metric | Show trend | Line chart |
| Time series, multiple metrics | Compare trends | Multiple lines or small multiples |
| 2 continuous variables | Correlation | Scatter plot |
| 1 continuous variable | Distribution | Histogram |
| Hierarchical categories | Part-whole | Treemap |
| Geographic data | Spatial patterns | Choropleth map |

---

## Color Strategy

**YOU MUST use color to serve a communication goal, NOT decoration.** Reserve saturated colors for emphasis.

### Choose Palette Type

**Sequential (single hue, light to dark)** - Ordered data
- **Use for**: Heatmaps, distributions, intensity, magnitude
- **Safe palettes**: Viridis, Blues, Grays, YlGnBu
- **❌ AVOID**: Rainbow/Jet (creates false boundaries, colorblind-hostile)

**Diverging (two sequences, neutral center)** - Meaningful midpoint
- **Use for**: Temperature anomalies, profit/loss, deviations from mean, +/- data
- **Safe palettes**: Blue-White-Orange, Green-White-Purple, RdBu
- **❌ AVOID**: Red-Green together (~8% of viewers can't distinguish)

**Categorical (distinct groups)** - Unrelated categories
- **Use for**: 2-7 categories maximum
- **Safe palette**: Orange, Blue, Green, Red, Purple, Yellow, Gray (in priority order)
- **❌ AVOID**: Too many colors (>7 overwhelms memory), similar hues (hard to distinguish)

### Accessibility Requirements (MANDATORY)

**YOU MUST implement ALL of these:**

1. **Never rely on color alone** → Add labels, patterns, shapes, or text
2. **Never red-green together** → ~8% of viewers (1 in 12 men) cannot distinguish
3. **Always check grayscale** → Visualization must work in black and white
4. **Always add redundant encoding** → Color + label, or color + pattern, or color + shape

**Colorblind-safe palettes**:
- Blue-Orange (most universal)
- Blue-Yellow
- Purple-Orange
- Viridis/Plasma (perceptually uniform, colorblind-friendly)

**Test your palette**: Use colorblind simulation tools (Coblis, Color Oracle) to verify.

---

## Typography & Visual Hierarchy

**Font Selection**:
- **YOU MUST use**: Sans-serif fonts for screen legibility (IBM Plex Sans, Space Grotesk, Source Sans 3, Fira Sans)
- **❌ DO NOT use**: Inter, Roboto, Arial, Helvetica (signals "AI slop"—generic AI-generated content)
- **Limit**: 2 fonts maximum (heading + body)
- **Weight**: Regular weight default (not light, not bold except emphasis)

**Size Hierarchy** (establish clear levels):
- **Title**: Largest, boldest (18-24pt, dominant message)
- **Axis labels**: Secondary (12-14pt)
- **Annotations**: Tertiary (10-12pt)
- **Minimum**: 12pt on screen, 10pt in print

**Apply CRAP Principles** (reference: @data-visualization-designer/resources/crap-principles-for-data.md):
- **Contrast**: Different elements very different (size, color, weight)
- **Repetition**: Same font/color/size for same element types (coherence)
- **Alignment**: Every element connects visually to another
- **Proximity**: Related items grouped close; unrelated separated

**Whitespace Strategy**: Strategic blank space directs attention and reduces cognitive load. DO NOT fear empty areas—they create breathing room.

---

## Visual Encoding Hierarchy

**Based on Cleveland & McGill perceptual accuracy research** (reference: @data-visualization-designer/resources/perceptual-accuracy-research.md):

### Perceptual Accuracy Ranking (Most to Least Accurate)

1. **Position along common scale** (X/Y axis) - **MOST ACCURATE**
2. **Position on non-aligned scales** (small multiples)
3. **Length** (bar heights)
4. **Angle** (pie slices) - 2-3× less accurate than position
5. **Area** (bubble size) - hard to judge, non-linear perception
6. **Volume** (3D objects) - highly inaccurate, distorted
7. **Color saturation** - **LEAST ACCURATE** for quantities

### Design Implications

**YOU MUST apply this hierarchy:**

- **Put most important comparisons in position along axis** (highest accuracy)
- **Use length for secondary comparisons** (bar charts, column charts)
- **Use color for emphasis or categorization** (NOT for precise quantities)
- **NEVER use 3D for non-spatial data** (distorts perception, reduces accuracy)

**Example**: Comparing sales across regions over time
- **Position**: Time on X-axis, sales on Y-axis (primary comparison)
- **Color**: Different regions (categorical distinction)
- **❌ NOT area**: Bubble size for sales (hard to judge precisely)

---

## Annotation & Storytelling

**Strategic annotations explain and guide** (reference: @data-visualization-designer/resources/data-storytelling.md).

### What to Annotate

**YOU MUST annotate**:
- **Outliers and anomalies** - Why is this point unusual?
- **Historical context** - Benchmarks, previous periods, goals
- **Key findings** - Insights you want highlighted
- **Methodology** - Data source, date range, limitations

**Keep concise**: One insight per annotation. Style consistently. Avoid over-annotation (more annotations than data points = clutter).

### Direct Labeling Strategy

**YOU MUST use direct labeling** instead of legends whenever possible:
- Integrate labels into visualization
- Eliminates need to match colors back to legend
- Reduces cognitive load
- Faster comprehension

**Example**: Label each line directly at endpoint instead of legend box.

### Title Conveys Insight

**❌ Descriptive title**: "Sales Over Time"
**✅ Insight-driven title**: "Sales Increased 60% in Q4"
**✅ Question-answering title**: "Which Products Drive Growth? Premium Segment"

**Title should communicate main takeaway** without requiring viewers to read the full chart.

---

## Critical Mistakes to Avoid

### ❌ FATAL (Directly Misleads Viewers)

**Truncated Y-Axes on Bar Charts**
- **What it is**: Y-axis doesn't start at zero, exaggerates differences
- **Impact**: 83.5% of viewers misinterpret magnitude (Cleveland & McGill)
- **Fix**: ALWAYS start bar chart Y-axes at zero, OR use broken axis indicator + clear labeling

**3D Effects (Non-Spatial Data)**
- **What it is**: Adding depth/perspective to charts representing non-spatial data
- **Impact**: Distorts through perspective (lie factor 1.5-2.0), rear values appear smaller
- **Fix**: NEVER use 3D for business/analytical data

**Red-Green Color Encoding**
- **What it is**: Using red and green as primary color distinction
- **Impact**: ~8% of viewers (1 in 12 men) see both as same muddy color
- **Fix**: Use Blue-Orange, Blue-Yellow, or other colorblind-safe palettes + redundant encoding

### ⚠️ SERIOUS (Significantly Reduce Effectiveness)

**Rainbow Colormap (Jet)**
- **What it is**: Rainbow gradient (red-orange-yellow-green-blue-purple)
- **Impact**: Creates false boundaries (bright yellow stripe), non-monotonic luminance, colorblind-hostile
- **Fix**: Replace with Viridis, Plasma, or Blue-White-Red diverging palette

**Color-Only Encoding**
- **What it is**: Information conveyed ONLY by color, no alternative
- **Impact**: Fails for colorblind viewers, grayscale printing, accessibility
- **Fix**: Add direct labels, patterns, shapes, or text (redundant encoding)

**Dual-Axis Charts (Incompatible Scales)**
- **What it is**: Two Y-axes with different scales on same chart
- **Impact**: Creates false correlation appearance, easily manipulated
- **Fix**: Use separate charts instead, OR ensure scales proportional + clearly labeled

**Pie Charts for Comparisons**
- **What it is**: Using pie charts to compare multiple values
- **Impact**: Human vision terrible at comparing angles (10-30× less accurate than bars)
- **Fix**: Use bar charts for comparison; pie only for showing one slice >50%

### 📊 MODERATE (Reduce Clarity)

**Too Many Colors** (>7)
- **Impact**: Overwhelms viewers, exceeds working memory capacity
- **Fix**: Reduce to 5-7 max, combine minor categories into "Other"

**Missing Context**
- **Impact**: No title, axis labels, data source, or date → viewers can't interpret or trust
- **Fix**: ALWAYS include title (conveys insight), axis labels (with units), source, date

**Chartjunk** (reference: @data-visualization-designer/resources/data-ink-optimization.md)
- **Impact**: Heavy gridlines, 3D effects, decorative backgrounds, ornamental fonts increase cognitive load
- **Fix**: Remove all non-data elements; maximize data-ink ratio

**Small Text**
- **Impact**: Below 12pt struggles for readability, excludes people with low vision
- **Fix**: Minimum 12pt (14pt+ optimal for accessibility)

---

## Quick Audit Before Publishing

**Run this 9-minute checklist before sharing any visualization:**

### Data Integrity (2 minutes)
- [ ] Bar chart Y-axis starts at zero OR clearly labeled if not
- [ ] No 3D effects on non-spatial data
- [ ] Dual axes proportional or clearly explained
- [ ] Data truthfully represented (no distortion)

### Design Quality (3 minutes)
- [ ] Title conveys insight (not just "Chart")
- [ ] Axis labels include units
- [ ] Color palette limited (max 5-7 categorical)
- [ ] No red-green together
- [ ] No color-only encoding (redundant encoding added)
- [ ] Grayscale readable

### Context (2 minutes)
- [ ] Title clear and insight-driven
- [ ] Legend present OR direct labels used
- [ ] Data source and date cited
- [ ] Sufficient context for interpretation
- [ ] Key findings/outliers explained

### Polish (2 minutes)
- [ ] Font professional sans-serif (IBM Plex Sans, Space Grotesk, Source Sans 3, NOT Inter/Roboto)
- [ ] Text minimum 12pt
- [ ] Alignment consistent (CRAP principles applied)
- [ ] Whitespace strategic
- [ ] No chartjunk (reference: data-ink-optimization.md)

**Total: 9 minutes. All checkboxes pass = ready to publish.**

---

## Integration

**Works Well With:**

- **Skill: design-excellence** - General typography anti-patterns, color theory, motion principles, background design (auto-activates together)
- **Skill: diagram-drawing** - Chart.js/D3.js technical implementation, export to PNG/SVG/PDF (auto-activates together)
- **Pattern: component_design** - UI component design patterns

**Typical Workflow**:
1. design-excellence auto-activates → General design principles (typography, color themes)
2. **data-visualization-designer auto-activates** → Chart selection, color strategy, validation
3. diagram-drawing auto-activates → Chart.js implementation code

**Separation of Concerns**:
- design-excellence = General design (not data-specific)
- **data-visualization-designer = Design decisions** (what chart, why, validation)
- diagram-drawing = Technical execution (Chart.js config, D3.js patterns)

---

## When to Load Resources

**CRAP principles deep-dive:**
- `@data-visualization-designer/resources/crap-principles-for-data.md` - Contrast, Repetition, Alignment, Proximity applied to charts/dashboards

**Perceptual accuracy research:**
- `@data-visualization-designer/resources/perceptual-accuracy-research.md` - Cleveland & McGill hierarchy, encoding decisions, science-backed design

**Data-ink optimization:**
- `@data-visualization-designer/resources/data-ink-optimization.md` - Tufte principles, chartjunk removal, maximizing data-ink ratio

**Storytelling techniques:**
- `@data-visualization-designer/resources/data-storytelling.md` - Annotation strategies, narrative arc, progressive disclosure

---

## Anti-Patterns to Avoid

**Chart Selection:**
- ❌ Pie charts for comparison tasks (use bar charts)
- ❌ 3D charts for non-spatial data (use 2D)
- ❌ Dual-axis with incompatible scales (use separate charts)
- ❌ Lines connecting non-temporal scatter points (remove lines)

**Color:**
- ❌ Red-green encoding (~8% can't distinguish)
- ❌ Rainbow/Jet colormap (creates false boundaries)
- ❌ Color-only encoding (add redundant labels/patterns)
- ❌ Too many colors (>7 overwhelms memory)
- ❌ Purple gradients on white (cliché "AI slop" pattern)

**Typography:**
- ❌ Inter, Roboto, Arial, Helvetica fonts (signals generic AI content)
- ❌ All text same size/weight (no hierarchy)
- ❌ Text below 12pt (readability issues)
- ❌ Ornamental fonts (reduces legibility)

**Truthfulness:**
- ❌ Truncated Y-axis without clear indication (misleads magnitude)
- ❌ 3D effects (distorts perception)
- ❌ Manipulated scales (exaggerates differences)
- ❌ Cherry-picked data ranges (hides context)

**Layout:**
- ❌ Missing axis labels/units (viewers can't interpret)
- ❌ No title or generic title (doesn't convey insight)
- ❌ No data source or date (can't verify or trust)
- ❌ Chartjunk (heavy gridlines, decorative backgrounds, borders)
- ❌ Pure white (#fff) or pure black (#000) backgrounds (use atmospheric gradients)

---

## Design Checklist

**Before implementing any visualization, verify all 8:**

1. ✓ **Brief Established** - Purpose, audience, context, success metric clear
2. ✓ **Chart Type Selected** - Matched to data structure and task, justified over alternatives
3. ✓ **Color Strategy Decided** - Palette type chosen (sequential/diverging/categorical), accessibility verified, redundant encoding planned
4. ✓ **Visual Hierarchy Clear** - Title dominant, axis labels secondary, annotations tertiary, whitespace strategic
5. ✓ **Encoding Optimized** - Most important variables in highest-accuracy channels (position > length > color)
6. ✓ **Annotations Complete** - Key insights highlighted, context provided, outliers explained
7. ✓ **Accessibility Verified** - No color-only encoding, grayscale works, no red-green, text ≥12pt, redundant encoding present
8. ✓ **Mistakes Avoided** - Passed Fatal/Serious/Moderate audit, 9-minute quick audit completed

**All 8 passing = ready to implement** (hand off to diagram-drawing skill for Chart.js/D3.js code).

---

## Core Principle

**Truthfulness > Beauty > Novelty**

**Always.**

Design emerges from understanding:
1. The data (structure, patterns, limitations)
2. The insight you want to communicate
3. The audience who needs to understand it

**Rush any of these = poor design. 80% effort → understanding. 20% effort → visual execution.**
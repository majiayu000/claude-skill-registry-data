---
name: design-fundamentals
description: |
  Core design principles for creating distinctive, beautiful UIs with technical excellence.
  Combines creative direction with practical foundation for memorable, accessible interfaces.

  Use when building UI without specific design specs (Figma, screenshots, design files):
  - Creating landing pages, home pages, marketing pages from scratch
  - Building web apps, dashboards, admin panels without design
  - Choosing design system: typography, colors, spacing, visual hierarchy
  - Need to propose complete design (fonts, colors, layout, spacing)
  - Building distinctive UIs that avoid generic AI aesthetics

  Keywords: landing page, design system, typography, colors, spacing, visual hierarchy

  Two-part approach:
  1. Creative Direction: Choose aesthetic tone (minimal, bold, elegant, playful)
  2. Technical Foundation: Spacing scales, typography specs, WCAG contrast, hierarchy

  Goal: Create UIs that are BOTH beautiful (distinctive, memorable) AND correct (accessible, consistent, professional).
---

# Design Fundamentals

## Purpose
Create distinctive, beautiful UIs through intentional aesthetic choices backed by solid technical foundation.

---

## Design Thinking

### Choose Aesthetic Direction

**Before coding, commit to clear aesthetic tone:**

**Minimal/Refined:**
- Generous whitespace, restrained color palette
- Elegant serif or geometric sans-serif fonts
- Subtle interactions, high contrast

**Bold/Vibrant:**
- Saturated colors, strong contrasts
- Display fonts with personality
- Energetic interactions, dynamic layouts

**Playful/Friendly:**
- Rounded shapes, warm color palette
- Approachable fonts, comfortable spacing
- Delightful micro-interactions

**Retro/Nostalgic:**
- Period-specific typography
- Vintage color schemes, textured backgrounds

**Organic/Natural:**
- Earthy tones, soft shapes, flowing layouts
- Natural imagery, gentle transitions

**Principle:** Intentionality > intensity. Commit fully to chosen direction.

---

### Avoid Generic AI Aesthetics

**Never use these clichés:**

❌ Purple gradients on white backgrounds
❌ System fonts everywhere (Inter, Roboto, Arial)
❌ Predictable 12-column grid layouts
❌ Safe, evenly-distributed color palettes
❌ Cookie-cutter card layouts
❌ Rounded corners on everything

**Instead, be distinctive:**

✅ Choose beautiful, characterful fonts
✅ Commit to bold colors OR refined neutrals
✅ Create unexpected layouts (asymmetry, overlap, diagonal flow)
✅ Use dominant colors with sharp accents
✅ Add visual details (textures, gradients, patterns, depth)
✅ Break the grid intentionally

---

## Technical Foundation

### Spacing System

**Principle:** Consistent scale creates visual rhythm and professionalism.

**Choose ONE base unit and multiply:**
- Smaller base (4): Finer control, granular spacing
- Larger base (8): Simpler system, bolder spacing

**Build your scale:**
- Start with base unit (4, 6, 8, or whatever fits)
- Create scale: base × 1, 2, 3, 4, 6, 8, 12, 16, 24
- Stick to scale values (avoid arbitrary in-between values)

**Guidelines:**
- Tighter spacing for related items
- Generous spacing separates major sections
- Whitespace = breathing room and importance
- Choose scale matching your aesthetic

---

### Typography

**Creative Direction:**
- Choose distinctive, characterful fonts (not system fonts)
- Pair display font (headings) with refined body font
- Font conveys personality: geometric = modern, serif = elegant, rounded = friendly
- Avoid overused fonts: Inter, Roboto, Arial, Helvetica

**Technical Specs:**
- **Body text**: Readable size (typically 16px+, adjust based on font)
- **Line height**: 1.5-1.6 for body, 1.2-1.3 for headings
- **Line length**: 50-75 characters optimal
- **Type scale**: Choose ratio for consistent hierarchy
  - Subtle/refined: Smaller ratio (1.2)
  - Balanced: Medium ratio (1.25)
  - Bold/dramatic: Larger ratio (1.333+)

**Font Weights:**
- Regular (400): Body text
- Semibold (600): Emphasis, subheadings
- Bold (700): Headings, strong emphasis
- Limit to 3-4 weights maximum

**Hierarchy Levels:**
- Primary: Page titles, main CTAs
- Secondary: Section headings, important actions
- Tertiary: Body text, labels
- Quaternary: Metadata, captions, helper text

---

### Color System

**Creative Direction:**
- Commit to aesthetic: bold OR refined (not timid middle)
- Use dominant colors with sharp accents
- Color conveys mood: warm (energy), cool (calm), muted (sophistication)
- Consider color psychology for brand personality

**Technical Specs:**
- **Primary**: Main brand color for CTAs, key actions (1 color)
- **Neutrals**: Text, borders, backgrounds (5-7 shades from light to dark)
- **Semantic**: Success (green), error (red), warning (yellow), info (blue)
- **Limit**: 3-4 brand colors maximum

**Contrast Requirements (WCAG AA - required for accessibility):**
- Normal text: 4.5:1 minimum
- Large text: 3:1 minimum
- UI components: 3:1 minimum
- Use contrast checker tools to verify

**Guidelines:**
- Test all text/background combinations
- Don't rely on color alone (add icons, labels, patterns)
- Each color needs light/dark variants

---

### Visual Hierarchy

**Principle:** Guide attention through size, weight, contrast, and spacing.

**Create clear levels:**
- Use size differences (headings larger than body)
- Use weight differences (bold for emphasis)
- Use spacing (more space = more importance)
- Use color sparingly for hierarchy

**Hierarchy Techniques:**
- **Size**: Primary elements significantly larger (2-3x+ size difference)
- **Proximity**: Group related items close, separate groups with generous space
- **Contrast**: Important elements use stronger contrast
- **Alignment**: Consistent alignment creates order

---

## Spatial Composition

### Layout Patterns

**Create interest through:**
- **Asymmetry**: Break symmetry for dynamic feel
- **Overlap**: Layer elements for depth
- **Diagonal flow**: Guide eye with angled layouts
- **Whitespace**: Generous negative space OR controlled density (intentional)
- **Grid breaking**: Intentionally break grid for emphasis

**Alignment:**
- Left-align text for readability (LTR languages)
- Center-align sparingly (titles, empty states)
- Right-align numbers in tables
- Be consistent within sections

---

## Visual Details

### Add Depth and Atmosphere

**Backgrounds:**
- Gradient meshes (soft, blended colors)
- Noise textures (subtle grain, paper texture)
- Geometric patterns (shapes, grids, dots)
- Layered transparencies (depth through layers)

**Details:**
- Shadows for elevation (subtle for cards, stronger for modals)
- Borders for definition (thin, subtle color difference)
- Subtle animations (hover states, quick transitions)

---

## Common Mistakes

**❌ Avoid:**
1. Generic AI aesthetics (purple gradients, system fonts)
2. No aesthetic direction (mixing styles randomly)
3. Arbitrary spacing (values outside your scale)
4. Poor contrast (insufficient difference)
5. Too many colors (overwhelming palette)
6. Inconsistent font sizes (random values, no scale)
7. No visual hierarchy (everything same size)
8. Cramped layouts (insufficient whitespace)

**✅ Do:**
1. Choose clear aesthetic and commit
2. Use distinctive fonts with personality
3. Follow spacing scale consistently
4. Test contrast ratios (4.5:1 minimum)
5. Limit to 3-4 brand colors
6. Use type scale for predictable hierarchy
7. Create clear levels (primary > secondary > tertiary)
8. Give content generous whitespace

---

## Validation Checklist

**Creative:**
- [ ] Clear aesthetic direction chosen
- [ ] Distinctive, characterful fonts (not generic)
- [ ] Cohesive color palette (bold OR refined)
- [ ] Unexpected layouts or intentional grid breaks
- [ ] Visual details add atmosphere

**Technical:**
- [ ] Spacing follows consistent scale
- [ ] Font sizes use type scale
- [ ] Color contrast meets WCAG AA (verify with checker)
- [ ] Line length readable
- [ ] Visual hierarchy clear
- [ ] Alignment consistent and intentional
- [ ] Limited brand color palette

---

## Key Takeaway

**Distinctive + Correct = Beautiful UI**

Technical correctness (spacing, contrast, hierarchy) ensures usability and professionalism.
Creative direction (aesthetic, fonts, colors, layouts) ensures memorability and distinctiveness.

Great design requires both: intentional aesthetic choices executed with technical precision.

Focus on intentionality - commit fully to chosen direction, then execute with consistency.
Avoid generic AI aesthetics through bold or refined choices, never timid middle ground.

---
name: drawbot-designer
description: Create well-designed posters, layouts, and graphics using DrawBot with automatic enforcement of typography principles from Hochuli, Bringhurst, and Müller-Brockmann. Use when users request posters, layouts, graphics, editorial designs, or mention DrawBot, typography, grid systems, or programmatic design.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# DrawBot Designer

Create professional posters, layouts, and graphics with automatic enforcement of design principles.

## Quick Start

1. **Read [design-vocabulary.md](design-vocabulary.md)** to translate user intent → design choices
2. **Use [templates/](templates/)** to start implementation
3. **Check [examples.md](examples.md)** for working patterns
4. **See [reference.md](reference.md)** for API details

## Design Thinking (BEFORE Code)

Before touching templates, commit to a **bold creative direction**:

### 1. Purpose & Context
- **What problem does this solve?** (inform, persuade, celebrate, warn?)
- **Who sees this?** (executives, students, general public, insiders?)
- **Where does it live?** (wall, hand, screen, street?)

### 2. Aesthetic Direction
**Pick an extreme.** Mediocrity is the enemy. Choose from:

| Direction | Characteristics |
|-----------|-----------------|
| **Swiss Modernism** | Grid worship, Helvetica, mathematical precision, asymmetry |
| **Punk Zine** | Photocopied texture, ransom-note type, deliberate chaos |
| **Japanese Minimalism** | Vast emptiness, one perfect element, asymmetric balance |
| **Constructivist** | Diagonal energy, red/black, bold geometry, propaganda feel |
| **Psychedelic** | Melting forms, vibrating colors, horror vacui |
| **Corporate Brutalism** | Oversized type, stark contrast, confrontational |
| **Art Deco** | Geometric ornament, gold accents, symmetry, luxury |
| **Editorial/Magazine** | Pull quotes, drop caps, sophisticated grid breaks |
| **Bauhaus** | Primary colors, geometric shapes, form follows function |
| **Vernacular/Found** | Hand-painted signs, imperfect type, authentic roughness |
| **Tech Noir** | Dark themes, neon accents, high contrast, terminal aesthetic |
| **Organic/Natural** | Flowing forms, earth tones, hand-drawn elements |

### 3. The Memorable Thing
Ask: **"What's the ONE thing someone will remember 5 seconds after looking away?"**
- A massive word?
- An unexpected color?
- A jarring juxtaposition?
- Perfect silence (whitespace)?

If you can't answer this, the design isn't ready.

### 4. Then Implement
Only after committing to direction → open [design-vocabulary.md](design-vocabulary.md) → map to technical choices → use the design system.

---

## Workflow: Natural Language → Design

### Step 0: Interpret Intent (BEFORE coding)

When user says something like "create a bold modern poster":

1. **Ask the design thinking questions above**
2. **Open [design-vocabulary.md](design-vocabulary.md)**
3. **Look up mood words**: "bold" → high contrast, large title; "modern" → asymmetric, sans-serif
4. **Identify content type**: poster → announcement pattern
5. **Commit to a memorable element**
6. **Then implement** using the design system

### Example Translation

**User says:** "Make an elegant invitation for a gala"

**Design thinking:**
- Purpose: Celebrate, make guests feel special
- Audience: Wealthy donors, formal crowd
- Direction: Art Deco meets Japanese Minimalism
- Memorable thing: One word in gold, swimming in cream space

**Technical mapping:**
- "elegant" → symmetric grid, serif type, muted colors, balanced whitespace
- "invitation" → announcement pattern (WHAT → WHEN → WHERE)

**Result:**
- Grid: 12×8, centered
- Font: Didot or similar high-contrast serif
- Colors: Warm cream, charcoal, gold accent
- Structure: Event name (HUGE, gold) → Date → Venue → RSVP
- The memorable thing: "GALA" in 200pt gold, nothing else competing

## When to Use This Skill

Activate when the user requests:
- Posters, layouts, graphics, or editorial designs
- Modifications to existing DrawBot code
- Typography or layout advice
- DrawBot script creation or debugging

## Core Principles

This skill automatically enforces:
- **Typography**: Hochuli's Detail in Typography (microtypography)
- **Layout**: Müller-Brockmann grid systems (macrotypography)
- **Hierarchy**: CRAP principles (Contrast, Repetition, Alignment, Proximity)

## Mandatory Workflow

**CRITICAL**: Always use the design system. Never write manual calculations.

### Step 1: Setup

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

import drawBot as db
from drawbot_grid import Grid
from drawbot_design_system import (
    POSTER_SCALE,        # or MAGAZINE_SCALE, BOOK_SCALE, REPORT_SCALE
    get_output_path,
    draw_wrapped_text,
    setup_poster_page
)
```

### Step 2: Create Page and Grid

```python
# Page setup (creates canvas automatically)
WIDTH, HEIGHT, MARGIN = setup_poster_page("letter", margin_ratio=1/10)

# Grid (automatically reads canvas size)
grid = Grid.from_margins(
    (-MARGIN, -MARGIN, -MARGIN, -MARGIN),
    column_subdivisions=12,
    row_subdivisions=16
)
```

### Step 3: Use Semantic Coordinates

```python
# ✅ CORRECT: Grid coordinates
header = (*grid[(0, 14)], *grid*(12, 2))  # Full width, top 2 rows

# ❌ WRONG: Manual calculations
header = (MARGIN, HEIGHT - 200, WIDTH - MARGIN*2, 150)
```

### Step 4: Wrap Text Properly

```python
# ✅ CORRECT: Point-based wrapping
draw_wrapped_text(text, x, y, width, height, font, size)

# ❌ WRONG: Character-count heuristics
wrapped = textwrap.wrap(text, width=70)
```

### Step 5: Save with Portable Paths

```python
# ✅ CORRECT: Works on any machine
db.saveImage(str(get_output_path("output.pdf")))

# ❌ WRONG: Hardcoded path
db.saveImage("/Users/you/...")
```

## Resources

### This Skill Directory

- **[examples.md](examples.md)** - Working code examples
- **[reference.md](reference.md)** - Complete API reference
- **[filters.md](filters.md)** - Image effects, textures, blend modes
- **[templates/](templates/)** - Starting templates:
  - `minimal_poster.py` - Simple poster
  - `two_column.py` - Magazine layout
  - `card_layout.py` - Color-coded cards

### Project Files

- **Complete examples**: `../../examples/`
  - `minimal_poster_example.py` - 80-line working poster
  - `longitudinalbench_poster_v7.py` - 352-line production poster
- **Documentation**: `../../docs/`
  - `design-system-usage.md` - Complete usage guide
  - `layout-design-principles.md` - Grid theory, CRAP, decision matrices
  - `typography-style-guide.md` - Hochuli's spacing, line length, readability
  - `print-production-checklist.md` - Bleed, CMYK, export settings
- **Assets**: `../../assets/` - 1,807 textures

## Typography Scales

| Context  | Scale          | Base | Ratio | When to Use           |
|----------|----------------|------|-------|-----------------------|
| Poster   | POSTER_SCALE   | 18pt | 1.5   | Posters, displays     |
| Magazine | MAGAZINE_SCALE | 11pt | 1.25  | Magazines, newsletters|
| Book     | BOOK_SCALE     | 11pt | 1.2   | Books, long-form      |
| Report   | REPORT_SCALE   | 12pt | 1.25  | Reports, docs         |

Access sizes:
```python
scale = POSTER_SCALE
scale.caption   # 12pt
scale.body      # 18pt
scale.h3        # 27pt
scale.h2        # 40.5pt
scale.h1        # 60.75pt
scale.title     # 91.125pt
```

## Color Palette Generation

Generate harmonious color palettes from a single base color:

```python
from drawbot_design_system import (
    generate_color_palette,
    hex_to_rgb,
    check_contrast_ratio,
    get_accessible_text_color
)

# Generate palette from base color
base = hex_to_rgb("#2E86AB")  # Ocean blue
palette = generate_color_palette(base, harmony="complementary")
# Returns: {'background': (light), 'text': (dark), 'accent': base, 'accent2': complement}

# Available harmonies:
# - "complementary": Base + opposite (high contrast)
# - "analogous": Base + neighbors (harmonious)
# - "triadic": Base + 2 evenly spaced (vibrant)
# - "split_complementary": Base + split opposite (balanced)
# - "monochromatic": Base + light/dark variations (subtle)

# Check accessibility
ratio, level = check_contrast_ratio(palette['text'], palette['background'])
print(f"Contrast: {ratio:.1f}:1 ({level})")  # "Contrast: 8.2:1 (AAA)"

# Get accessible text for any background
text_color = get_accessible_text_color(palette['accent'])
```

## OpenType Features

Enable professional typography features:

```python
from drawbot_design_system import (
    set_opentype_features,
    get_available_opentype_features
)
import drawBot as db

# Check what features a font supports
db.font("Adobe Garamond Pro")
features = get_available_opentype_features()
print(features)  # {'liga': 'Standard ligatures', 'smcp': 'Small capitals', ...}

# Enable small caps + oldstyle figures
set_opentype_features(['smcp', 'onum'])
db.text("The Quick Brown Fox 1234", (x, y))

# Common features:
# - 'liga': Standard ligatures (fi, fl, ff)
# - 'smcp': Small capitals
# - 'onum': Oldstyle figures (varying heights)
# - 'tnum': Tabular figures (monospaced)
# - 'frac': Automatic fractions (1/2 → ½)
# - 'ss01'-'ss20': Stylistic sets
```

## Variable Fonts

Control variable font axes dynamically:

```python
from drawbot_design_system import (
    set_font_variation,
    get_font_variation_axes
)
import drawBot as db

# Check available axes
db.font("Skia")  # Or any variable font
axes = get_font_variation_axes()
print(axes)  # {'wght': {'minValue': 100, 'maxValue': 900, ...}, ...}

# Set axis values
set_font_variation(wght=600, wdth=85)  # Semi-bold, slightly condensed
db.text("Variable Font Text", (x, y))

# Common axes:
# - wght: Weight (100=thin, 400=regular, 700=bold, 900=black)
# - wdth: Width (50=condensed, 100=normal, 200=extended)
# - slnt: Slant (-90 to 90 degrees)
# - ital: Italic (0=upright, 1=italic)
# - opsz: Optical size (optimize for display vs text)
```

## Print Production

Set up print-ready documents with bleed:

```python
from drawbot_design_system import (
    setup_print_page,
    validate_print_ready,
    PRINT_PRESETS
)
import drawBot as db

# Set up page with bleed (US standard: 0.125")
specs = setup_print_page("letter", include_bleed=True)

# Draw background to FULL canvas (into bleed area)
db.fill(0.2, 0.4, 0.8)
db.rect(0, 0, specs['canvas_width'], specs['canvas_height'])

# Position content relative to trim + safe margin
content_x = specs['trim_x'] + specs['safe_margin']
content_y = specs['trim_y'] + specs['safe_margin']

# Use CMYK for print colors
db.cmykFill(0.6, 0.4, 0.4, 1.0)  # Rich black

# Validate before export
is_valid, warnings = validate_print_ready()
for w in warnings:
    print(w)

# See docs/print-production-checklist.md for complete guide
```

## Grid Patterns

### Full Width Section
```python
header = (*grid[(0, 14)], *grid*(12, 2))  # All columns, 2 rows
```

### Two Columns
```python
left = (*grid[(0, 1)], *grid*(5, 13))    # Cols 0-4
right = (*grid[(7, 1)], *grid*(5, 13))   # Cols 7-11
# Columns 5-6 = automatic gutter
```

### Stacked Sections
```python
section1 = (*grid[(0, 10)], *grid*(12, 3))  # Rows 10-12
section2 = (*grid[(0, 6)], *grid*(12, 3))   # Rows 6-8
section3 = (*grid[(0, 2)], *grid*(12, 3))   # Rows 2-4
```

## Decision Matrix

| Content | Grid    | Typography     | Line Length |
|---------|---------|----------------|-------------|
| Poster  | 12×16   | POSTER_SCALE   | 20-30 CPL   |
| Magazine| 12×8    | MAGAZINE_SCALE | 45-50 CPL   |
| Book    | 6×8     | BOOK_SCALE     | 60-65 CPL   |
| Report  | 12×8    | REPORT_SCALE   | 50-60 CPL   |

## Verification Checklist

Before finalizing code, verify:

- [ ] Imports from `lib/` directory
- [ ] Used `setup_poster_page()` BEFORE grid
- [ ] Grid created with `Grid.from_margins()`
- [ ] Used pre-defined scale (POSTER_SCALE, etc.)
- [ ] All layout uses grid coordinates (not manual math)
- [ ] All text uses `draw_wrapped_text()` (not textwrap.wrap)
- [ ] Paths use `get_output_path()` (not hardcoded)
- [ ] No fontSize approximations

## Error Prevention

### Never Do This (Technical)

❌ Hardcode page size in grid
❌ Use character counts for wrapping
❌ Approximate line height with fontSize
❌ Manual calculations instead of grid
❌ Truncate text with `[:N]`
❌ Hardcode absolute paths

### Always Do This (Technical)

✅ Let grid read canvas size
✅ Use point-based wrapping
✅ Use real font metrics
✅ Use semantic grid coordinates
✅ Draw all text that fits
✅ Use portable path helpers

---

## Avoid "AI Slop" Aesthetics

**CRITICAL**: These patterns make work look machine-generated. Avoid them:

### Typography Anti-Patterns
❌ **Helvetica Neue for everything** — It's fine, but predictable. Try Akzidenz-Grotesk, Univers, or something unexpected.
❌ **Safe font pairings** (Montserrat + Open Sans) — Too common. Be bolder.
❌ **Centered everything** — Easy but lazy. Asymmetry creates energy.
❌ **Even text sizes** (24pt, 18pt, 14pt) — Use the scale ratios; they create proper tension.
❌ **Justified text in narrow columns** — Creates rivers of whitespace.

### Color Anti-Patterns
❌ **Blue gradient on white** — The default "tech startup" look.
❌ **Purple/pink gradients** — Overused in AI-generated content.
❌ **Gray text on white** (#666 on #fff) — Low contrast, looks washed out.
❌ **Rainbow gradients** — Almost never appropriate.
❌ **Equal color distribution** — Use 70-20-10, not 33-33-33.

### Layout Anti-Patterns
❌ **Perfect symmetry everywhere** — Real design has controlled asymmetry.
❌ **Everything centered vertically AND horizontally** — Creates static, lifeless compositions.
❌ **Uniform margins** — Vary them intentionally; tension creates interest.
❌ **Clip art shapes** (perfect circles, rounded rectangles) — Too geometric, too safe.
❌ **Stock photo compositions** — If it looks like a template, it is.

### The "AI Look" Checklist
If your design has 3+ of these, reconsider:
- [ ] Centered text blocks
- [ ] Blue/purple color scheme
- [ ] Generic sans-serif font
- [ ] Perfect geometric shapes
- [ ] Even spacing everywhere
- [ ] No memorable focal point
- [ ] Could be any company's poster

### The Antidote
**Make ONE bold choice that a template wouldn't:**
- Extremely large type (bigger than feels comfortable)
- Extremely small type (challenges the reader)
- Unexpected color (not blue, not purple)
- Deliberate asymmetry
- Texture or grain
- One element that breaks the grid

## Common Tasks

### Create a Poster

1. Copy `templates/minimal_poster.py` to `../../examples/` or your working directory
2. If copying to `examples/`, update the import path to use `.parent.parent` instead of `.parent.parent.parent.parent.parent`
3. Update title, subtitle, body text
4. Change filename in `get_output_path()`
5. Run: `uv run python your_file.py`

### Two-Column Layout

1. Copy `templates/two_column.py` to `../../examples/`
2. Update the import path if needed (see Create a Poster above)
3. Update column content
4. Adjust grid if needed (more/fewer rows)

### Color-Coded Cards

1. Copy `templates/card_layout.py` to `../../examples/`
2. Update the import path if needed (see Create a Poster above)
3. Modify card titles and descriptions
4. Change colors if desired

### Debug Layout Issues

1. Add `grid.draw(show_index=True)` before `saveImage()`
2. View PDF to see grid structure
3. Verify grid coordinates
4. Remove `grid.draw()` for final output

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Text overflows | Character-count wrapping | Use `draw_wrapped_text()` |
| Grid doesn't match | Created before `newPage()` | Create page FIRST |
| Wrong sizes | Wrong scale for context | Use POSTER_SCALE for posters |
| Paths don't work | Hardcoded paths | Use `get_output_path()` |

See [reference.md](reference.md) for detailed troubleshooting.

## Example Session

**User**: "Create a poster for an AI conference"

**Response**:
1. Copy `templates/minimal_poster.py`
2. Modify content:
   - Title: "AI Conference 2025"
   - Subtitle: "Advancing Machine Learning"
   - Body: Conference details
3. Save as `ai_conference.py`
4. Run: `uv run python examples/ai_conference.py`

Result: Professional poster following all design principles automatically.

## Progressive Disclosure

Start with templates, refer to examples and reference as needed:

1. **Start**: `templates/minimal_poster.py`
2. **Learn**: `examples.md` for patterns
3. **Reference**: `reference.md` for API details
4. **Effects**: `filters.md` for images/textures (when needed)
5. **Deep dive**: `../../docs/` for theory

Claude loads resources progressively as needed (saves context).

## Force Variation

**No two designs should look the same.** Before finalizing, ask:

### Variation Prompts
- "What if the title was 3x larger?"
- "What if I used only one color?"
- "What if text was at the bottom instead?"
- "What if margins were twice as wide?"
- "What if I removed everything except the essential?"
- "What if this was for the opposite audience?"

### Rotation Mandates
Cycle through these to avoid convergence:

**Fonts** (never default to the same one):
- This project: Serif
- Next project: Geometric sans
- Next: Humanist sans
- Next: Slab serif
- Next: Display/decorative

**Color temperature**:
- This project: Warm palette
- Next: Cool palette
- Next: Neutral with warm accent
- Next: Monochrome

**Layout energy**:
- This project: Asymmetric, dynamic
- Next: Symmetric, calm
- Next: Vertical emphasis
- Next: Horizontal bands

---

## The Creative Mandate

> **DrawBot is capable of extraordinary creative work.**

The design system handles the rules—grids, scales, metrics. That's the foundation.

But foundations are invisible. What people see is the **vision on top**.

Don't settle for "correct." Aim for **unforgettable**.

The difference between good and great:
- Good: Follows the grid, uses the scale, wraps text properly
- **Great**: Does all that AND has one moment of genuine surprise

Every poster should have that moment. Find it before you write code.

**Trust the system. Then transcend it.**

---

## Remember

The design system makes it **impossible to violate design principles**. That's the floor, not the ceiling.

Hochuli gives you the rules. Müller-Brockmann gives you the grid. **You give it soul.**

## Version History

- v1.2.0 (2025-12-31): Added design thinking, aesthetic directions, anti-patterns, variation mandates
- v1.1.0 (2025-12-31): Added color harmony, OpenType/variable fonts, print production
- v1.0.0 (2025-10-18): Initial Agent Skill with curated content

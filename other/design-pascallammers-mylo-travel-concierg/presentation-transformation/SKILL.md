---
name: presentation-transformation
description: Use when transforming presentations from basic to professional quality - employs parallel multi-agent execution, research-driven design, and McKinsey/BCG/Deloitte best practices to create executive-ready decks
---

# Presentation Transformation

## Overview

Transform basic presentations into professional, executive-ready decks using parallel multi-agent execution, comprehensive research, and corporate design best practices.

**Core principle:** Research → Design → Parallel Execution → Iteration → Polish

**Announce at start:** "I'm using the presentation-transformation skill to elevate your deck to professional quality."

## Quick Reference

| Phase | Key Activities | Tool Usage | Output |
|-------|---------------|------------|--------|
| **1. Analysis** | Extract content, gather requirements | Brainstorming skill, AskUserQuestion | Requirements document |
| **2. Research** | Market data, case studies, best practices | WebSearch (3+ searches) | Research markdown |
| **3. Design** | Define color palette, typography, layouts | Design system constants | Style guide |
| **4. Parallel Build** | Launch 3 agents simultaneously | Task tool (multiple) | Generator + content + charts |
| **5. Iteration** | Fix formatting, spacing, bullets | Python-expert agent | Polished presentation |
| **6. Documentation** | Create reusable skill/templates | Write skill file | Future reusability |

## The Process

### Phase 1: Analysis & Requirements

**CRITICAL:** Start with brainstorming skill to understand requirements.

**1. Extract Current Content**

For PowerPoint files (.pptx):
```bash
# Extract as ZIP
cd "path/to/presentations"
unzip -q -o presentation.pptx -d extracted/

# Parse slide content
find extracted/ppt/slides -name "slide*.xml" | sort | while read slide; do
  slidenum=$(echo $slide | grep -o '[0-9]\+')
  echo "=== SLIDE $slidenum ==="
  grep -o '<a:t>[^<]*</a:t>' $slide | sed 's/<a:t>//g; s/<\/a:t>//g'
done
```

Document findings:
- Total slide count
- Content quality (basic, intermediate, advanced)
- Design issues (overlaps, spacing, fonts)
- Missing elements (data, case studies, visuals)

**2. Gather Requirements** (use AskUserQuestion)

Ask about:
- **Primary goal**: Sponsors, education, recruitment, multi-purpose
- **Design style**: Modern tech, corporate professional, environmental, blended
- **Content approach**: Problem-led, data-driven, case studies
- **Specific fixes**: What user dislikes about current version

**3. Research Context** (3-5 WebSearch queries)

Essential searches:
- Topic-specific market data and statistics
- Real-world case studies with quantified results
- Industry trends and projections (with years)
- Competitor/alternative approaches
- Presentation design best practices (current year)

### Phase 2: Design System Definition

**Corporate Professional Standards:**

```python
# Color Palette
NAVY = RGBColor(26, 43, 74)      # #1A2B4A - trust, stability
TEAL = RGBColor(0, 167, 160)     # #00A7A0 - innovation
GOLD = RGBColor(212, 167, 106)   # #D4A76A - premium value
LIGHT_GRAY = RGBColor(240, 240, 240)
DARK_GRAY = RGBColor(68, 68, 68)

# Typography Hierarchy
FONT_TITLE = 44        # Main titles (not 54, causes overflow)
FONT_HEADING = 34      # Section headings
FONT_SUBHEADING = 24   # Subheadings
FONT_BODY = 15         # Body text & bullets (not 18, too large)
FONT_CAPTION = 14      # Captions, labels

# Font Families
FONT_HEADER = "Montserrat"    # Bold, modern, readable
FONT_BODY_TEXT = "Open Sans"  # Clean, professional

# Spacing Rules (CRITICAL for avoiding overlap)
MARGIN = Inches(0.5)
CONTENT_TOP = Inches(2.0)      # Room for titles
TITLE_TO_SUBTITLE = 0.7        # Minimum gap (inches)
ELEMENT_TO_ELEMENT = 0.3       # Between major elements
BULLET_SPACE_BEFORE = Pt(8)    # Vertical spacing
BULLET_SPACE_AFTER = Pt(8)
LINE_SPACING = 1.2             # Body text line height

# Layout
SLIDE_WIDTH = Inches(10)       # Standard widescreen
SLIDE_HEIGHT = Inches(7.5)
CONTENT_WIDTH = Inches(8.5)    # Maximum content width
TITLE_WIDTH = Inches(8.0)      # Prevents overflow
```

**Alternative Palettes:**

Startup Modern:
- Primary: #0066FF (electric blue)
- Secondary: #FF3366 (vibrant pink)
- Accent: #00CC88 (fresh green)

Environmental:
- Primary: #2C5F2D (forest green)
- Secondary: #97BC62 (sage)
- Accent: #F4A259 (earth orange)

### Phase 3: Parallel Multi-Agent Execution

**CRITICAL:** Launch all 3 agents in SINGLE message for true parallelism.

```python
# Agent 1: Presentation Generator
Task(
    subagent_type="python-expert:python-expert",
    description="Build presentation generator",
    prompt="""Create complete python-pptx script:

ENVIRONMENT:
- Directory: /path/to/presentations
- Venv: pptx_env (already created with python-pptx, pillow installed)

DESIGN SYSTEM:
[Paste color palette and typography specs]

STRUCTURE:
- Create generate_presentation.py
- Include DesignSystem class with constants
- Helper functions: add_background_shape, add_title_with_accent, add_bullet_list, add_stat_box
- Slide generators: create_slide_01_title(), create_slide_02_team(), etc.
- Main function: generate_presentation(output_path)

CRITICAL Z-ORDER:
1. Backgrounds FIRST
2. Accent bars/decorative elements
3. Text boxes LAST
(This prevents overlapping)

BULLET LISTS MUST USE:
p.level = 0  # Enables actual bullets
p.space_before = Pt(8)
p.space_after = Pt(8)
p.line_spacing = 1.2

Return: "AGENT 1 COMPLETE - presentation generator created"
"""
)

# Agent 2: Content Researcher
Task(
    subagent_type="general-purpose",
    description="Research case studies",
    prompt="""Research and compile:

CASE STUDY 1: [Topic-specific example]
- Real examples with company names
- Statistical impact (percentages, dollar amounts)
- Specific timeline and results
- How problem manifested

CASE STUDY 2: [Second example]
[Same structure]

CASE STUDY 3: [Third example]
[Same structure]

For each case study provide:
- Title (concise, compelling)
- 2-3 bullet points with data/facts
- Key takeaway
- Source citations

Create: case_studies_content.md with all details

Return: Complete markdown with 3+ detailed case studies
"""
)

# Agent 3: Data Visualization
Task(
    subagent_type="general-purpose",
    description="Generate chart images",
    prompt="""Create matplotlib/seaborn charts:

ENVIRONMENT:
- Directory: /path/to/presentations
- Venv: pptx_env
- Install: matplotlib, seaborn if needed

CREATE: generate_charts.py producing PNGs:

CHART 1: Market Growth
- Bar chart showing current → future projections
- Color gradient matching palette
- 300 DPI, professional styling

CHART 2: Problem Statistics
- Pie chart showing fraud/problem percentages
- Red for problem, green for solution
- Clear percentage labels

CHART 3: Trend Over Time
- Line chart with smooth curve
- Milestone annotations
- Data points marked

All charts MUST:
- Use corporate colors: #1A2B4A, #00A7A0, #D4A76A
- High DPI (300) for print quality
- No default matplotlib styling
- Proper titles and labels
- Save to charts/ directory

Run script and return: "AGENT 3 COMPLETE - All charts in charts/"
"""
)
```

**Launch all 3 in parallel:**
- Single message with 3 Task invocations
- Agents complete simultaneously (~same time as 1)
- 3x speed improvement

### Phase 4: Python Environment Setup

**Virtual Environment Required:**

```bash
cd "/path/to/presentations"
python3 -m venv pptx_env
source pptx_env/bin/activate
pip install python-pptx pillow matplotlib seaborn
```

**Why venv?** macOS has externally-managed-environment protection, pip3 install fails globally.

### Phase 5: Key python-pptx Patterns

**Background Shapes (Z-Order Layer 1):**

```python
def add_background_shape(slide, color, height_fraction=0.3):
    """Add colored background - RENDER FIRST"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0, 0,
        Inches(10), Inches(7.5 * height_fraction)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()  # No border
    return shape
```

**Title with Accent Bar (Z-Order Layer 2-3):**

```python
def add_title_with_accent(slide, title_text, subtitle_text=None):
    """Add title with teal accent bar"""
    # Accent bar (Layer 2)
    add_accent_bar(slide, TEAL, Inches(0.5), Inches(0.9),
                   Inches(0.15), Inches(0.7))

    # Title (Layer 3)
    title_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(0.9),     # After accent bar
        Inches(8.0), Inches(1.0)      # Max width to prevent overflow
    )
    title_frame = title_box.text_frame
    title_frame.text = title_text
    title_frame.word_wrap = True  # CRITICAL for long titles

    # Style
    for p in title_frame.paragraphs:
        p.font.name = "Montserrat"
        p.font.size = Pt(34)
        p.font.color.rgb = NAVY
        p.font.bold = True

    # Subtitle (if provided)
    if subtitle_text:
        subtitle_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(1.7),  # 0.7" gap from title
            Inches(8.0), Inches(0.6)
        )
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.text = subtitle_text
        subtitle_frame.word_wrap = True

        for p in subtitle_frame.paragraphs:
            p.font.name = "Open Sans"
            p.font.size = Pt(18)
            p.font.color.rgb = DARK_GRAY
```

**Bullet Lists (ACTUAL BULLETS):**

```python
def add_bullet_list(slide, items, left, top, width, height):
    """Add formatted bullet list - NOT plain text"""
    textbox = slide.shapes.add_textbox(left, top, width, height)
    text_frame = textbox.text_frame
    text_frame.word_wrap = True

    for i, item in enumerate(items):
        # Create paragraph
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()

        # CRITICAL: This enables actual bullets
        p.text = item
        p.level = 0  # Level 0 = bullet, Level 1 = sub-bullet

        # Styling
        p.font.name = "Open Sans"
        p.font.size = Pt(15)  # Not 18, too large
        p.font.color.rgb = DARK_GRAY

        # Spacing (McKinsey best practice)
        p.space_before = Pt(8)
        p.space_after = Pt(8)
        p.line_spacing = 1.2  # 20% more than single-space
```

**Stat Boxes:**

```python
def add_stat_box(slide, stat, label, left, top,
                 width=Inches(2.5), height=Inches(1.5)):
    """Statistics box with number + label"""
    # Background
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT_GRAY
    shape.line.fill.background()

    # Large number
    stat_box = slide.shapes.add_textbox(
        left, top + Inches(0.25),  # Padding from top
        width, Inches(0.7)
    )
    stat_frame = stat_box.text_frame
    stat_frame.text = stat

    for p in stat_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Montserrat"
        p.font.size = Pt(48)
        p.font.color.rgb = TEAL
        p.font.bold = True

    # Label
    label_box = slide.shapes.add_textbox(
        left, top + Inches(0.95),  # Below number
        width, Inches(0.5)
    )
    label_frame = label_box.text_frame
    label_frame.text = label
    label_frame.word_wrap = True

    for p in label_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Open Sans"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_GRAY
```

### Phase 6: Design Best Practices (Research-Backed)

**From McKinsey/BCG/Deloitte Analysis:**

**1. 6×6 Rule for Bullets**
- Maximum 6 bullets per slide
- Maximum 6-8 words per bullet
- Condense verbose text aggressively

Before: "No Universal Standards: Fragmented markets lack unified verification protocols"
After: "Fragmented markets lack unified verification standards" (7 words)

**2. Visual Hierarchy**
- Clear size differences: Title > Heading > Subhead > Body
- Minimum 1.5x size ratio between levels
- Use color to reinforce importance

**3. Whitespace is King**
- Generous margins prevent cramped feeling
- Better to split into 2 slides than cram 1
- Empty space signals professionalism

**4. Typography Rules**
- Sans-serif for screens (Arial, Calibri, Open Sans)
- Line spacing: 1.15-1.5 for body text
- Never below 14pt font size (readability)

**5. Data Visualization**
- Use charts for numbers, not text bullets
- Color-code for instant comprehension
- Professional styling (customize matplotlib defaults)

**6. Consistency Throughout**
- Same fonts, colors, spacing across all slides
- Reusable helper functions enforce this
- Predictable layouts aid comprehension

### Phase 7: Common Issues & Fixes

**Issue: Text Overflow / Titles Running Off**

Symptoms:
- Titles cut off at right edge
- Text disappearing

Fix:
```python
# Reduce title width
title_box = slide.shapes.add_textbox(
    Inches(0.8), Inches(0.9),
    Inches(8.0), Inches(1.0)  # Was 8.5, now 8.0
)

# Enable word wrap
title_frame.word_wrap = True

# Reduce font if still too large
p.font.size = Pt(34)  # Was 44
```

**Issue: Overlapping Elements**

Symptoms:
- Accent bars on top of text
- Backgrounds covering content

Fix:
```python
# CORRECT Z-ORDER:
# 1. Backgrounds first
add_background_shape(slide, NAVY, 0.5)

# 2. Accent bars second
add_accent_bar(slide, GOLD, ...)

# 3. Text boxes last
title_box = slide.shapes.add_textbox(...)
```

**Issue: Poor Readability**

Symptoms:
- Text feels cramped
- Hard to scan quickly

Fix:
```python
# Reduce body text size
p.font.size = Pt(15)  # Not 18

# Increase line spacing
p.line_spacing = 1.2

# Add vertical spacing
p.space_before = Pt(8)
p.space_after = Pt(8)
```

**Issue: Cramped Layouts**

Symptoms:
- Elements touching each other
- No breathing room

Fix:
```python
# Increase top margin
CONTENT_TOP = Inches(2.0)  # Was 1.8

# Add spacing between elements
stat_top = CONTENT_TOP + Inches(0.3)
bullet_top = stat_top + Inches(2.0) + Inches(0.3)  # 0.3" gap
```

**Debugging Process:**
1. User reports formatting issues
2. Read current generate script
3. Launch python-expert agent with specific fixes
4. Regenerate presentation
5. Open in PowerPoint and verify
6. Repeat until beautiful

### Phase 8: Modular Architecture

**Structure for Flexibility:**

**Core Pitch Deck** (10 slides):
- Slide 1: Title / Hook
- Slide 2: Team
- Slide 3: Problem
- Slide 4: Market Opportunity
- Slide 5: Solution
- Slide 6: Proof (case study)
- Slide 7: Why Now
- Slide 8: Governance / How It Works
- Slide 9: Timeline / Roadmap
- Slide 10: Contact / CTA

**Module A: Market Deep-Dive** (3-5 slides):
- Detailed market analysis
- Competitive landscape
- Regulatory environment

**Module B: Case Studies** (3-5 slides):
- Detailed case study 1
- Detailed case study 2
- ROI analysis

**Module C: Technical Details** (3-5 slides):
- Architecture overview
- Integration pathways
- Security model

**Module D: Commercial** (2-3 slides):
- Pricing / Membership tiers
- Benefits breakdown
- Next steps

**Benefits:**
- Customize for audience (exec vs. technical)
- Remove/include modules as needed
- Easy to update individual sections

### Phase 9: Iteration Protocol

**First Generation:**
- Expect issues (overlaps, overflow, spacing)
- Normal - first draft is never final

**User Feedback:**
- Listen for specific issues
- "Overlapping elements" → z-order fix
- "Titles running off" → width/font fix
- "No bullets" → p.level = 0 fix
- "Cramped" → spacing increase

**Fix Pattern:**
1. Identify specific problem
2. Launch python-expert agent with fix instructions
3. Regenerate
4. Verify in PowerPoint
5. Repeat 2-3 times typically

**Quality Bar:**
- No overlapping elements ✓
- No text overflow ✓
- Consistent spacing ✓
- Professional color usage ✓
- Actual bullets (not plain text) ✓
- Research-backed content ✓
- Clear narrative flow ✓

## Research Checklist

Before designing, web search for:
- [ ] Topic-specific market data with years
- [ ] Real case studies with company names and results
- [ ] Industry trends and growth projections
- [ ] Competitive/alternative approaches
- [ ] Regulatory landscape and timeline
- [ ] Presentation design best practices (current year)
- [ ] Typography and spacing recommendations
- [ ] Color psychology for corporate presentations

## Tools & Technologies

**Required:**
- python-pptx (PowerPoint generation)
- pillow (Image handling)

**Optional but Recommended:**
- matplotlib (Charts)
- seaborn (Statistical visualizations)
- pandas (Data for charts)

**Environment:**
- Python 3.8+
- Virtual environment (required on macOS)
- Works on macOS, Linux, Windows

## Success Metrics

**Visual Quality:**
- No overlapping elements
- No text overflow
- Consistent spacing throughout
- Professional color usage
- Proper bullet formatting

**Content Quality:**
- Research-backed statistics
- Real case studies with results
- Clear narrative flow
- Actionable takeaways
- Quantified benefits

**Technical Quality:**
- Clean, readable code
- Reusable helper functions
- Fast generation (<30 seconds)
- Easy to modify/extend

## Files Generated

Typical output:
- `generate_presentation.py` - Main generator
- `case_studies_content.md` - Research
- `generate_charts.py` - Chart generator
- `charts/*.png` - Visualization images
- `Final_Presentation.pptx` - Output deck

## Reusability Pattern

**To adapt for other presentations:**

1. Clone structure
   - Copy generate_presentation.py template
   - Update DesignSystem colors/fonts
   - Modify slide generator functions

2. Research phase
   - Web search for new topic
   - Gather statistics, case studies
   - Create content markdown

3. Generate charts
   - Topic-specific visualizations
   - Match color palette
   - Export as PNG

4. Customize slides
   - Update slide functions
   - Keep helpers (generic)
   - Maintain consistency

5. Test & iterate
   - Generate → Review → Fix
   - User feedback loop
   - Polish until professional

## Anti-Patterns

❌ **Don't skip research** - Generic content looks amateur
❌ **Don't overcrowd slides** - Violates 6×6 rule
❌ **Don't use default colors** - Creates amateur look
❌ **Don't ignore z-order** - Causes overlaps
❌ **Don't use tiny fonts** - Minimum 14pt
❌ **Don't skip iteration** - First draft never final
❌ **Don't work sequentially** - Use parallel agents

## Key Learnings

**Speed:** Parallel agents = 3x faster than sequential
**Quality:** Research-driven content >> guessing
**Design:** Follow proven rules (6×6, hierarchy)
**Iteration:** Expect 2-3 rounds of fixes
**Documentation:** Capture process for reuse

## Example Session Flow

```
1. User: "Transform presentation from zero to hero"
2. Extract current slides (unzip .pptx)
3. Ask requirements (AskUserQuestion)
4. Research topic (3-5 WebSearch queries)
5. Launch 3 parallel agents (single message)
6. Agents complete simultaneously
7. Generate initial presentation
8. User: "Overlapping elements, text overflow"
9. Fix formatting (python-expert agent)
10. Regenerate
11. User: "Better but bullets need work"
12. Research typography best practices
13. Fix bullets + spacing
14. Regenerate
15. User satisfied
16. Document as skill
```

**This skill transforms good presentations into HERO-LEVEL decks through systematic research, parallel execution, and professional design principles.**

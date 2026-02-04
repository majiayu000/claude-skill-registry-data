---
name: pitch-deck-creator-edtech
description: Use when user needs to create a pitch deck for EdTech startups - transforms content into visually compelling, narrative-driven presentations through collaborative refinement, wireframing, and hybrid deck generation (PowerPoint + Google Slides)
---

# Pitch Deck Creator for EdTech Startups

## Overview

Transform content-heavy pitch materials into visually compelling, narrative-driven pitch decks. This skill guides EdTech startup founders through collaborative content refinement, wireframe validation, professional design generation, and hybrid deck creation (PowerPoint + Google Slides).

**Target User:** EdTech startup founders with written pitch content who need help with structure, narrative flow, and visual design.

**Core Value:** Combines storytelling expertise with graphic design principles to maximize investor impact.

---

## When to Use This Skill

Use this skill when:
- User asks to "create a pitch deck" or "design a presentation"
- User has pitch content but needs help with structure and visual design
- User mentions they don't know how to make content visually appealing
- User wants to refine existing pitch materials for investors
- User says they have content but struggle with narrative flow

**Trigger phrases:** "create pitch deck," "design presentation," "make slides," "help with my pitch"

---

## Prerequisites

**Required from user:**
- Content markdown file structured by slide topics (similar to Harry_Llama_Pitch_Deck_Content.md format)
- Each slide should have: slide number, title, and content organized by section

**Resource locations:**
- Best practices: `/pitch_deck_skill/` (articles, examples, design principles)
- Example decks: `examples/` (visual reference images relative to skill directory)
- Output directory: `./pitch_deck_output/` (will be created in working directory)

---

## The 7-Phase Process

### Phase 1: Discovery & Setup

**Goal:** Gather requirements and understand user's needs.

**Actions:**
1. Ask user for content markdown file path
2. Use `AskUserQuestion` tool to gather:
   - **Purpose:** Investor pitch | Customer pitch | Partnership pitch | Internal pitch
   - **Target Audience:** VCs | Angels | Strategic investors | Corporate partners
   - **Tone:** Bold/aggressive | Professional/measured | Visionary/aspirational | Data-driven/analytical
   - **Format Preference:** PowerPoint | Google Slides | Both
   - **Brand Assets:** Colors (hex codes), Fonts (names), Logo location

3. Use `Read` tool to load:
   - User's content markdown file
   - Best practices resource: `resources.md` (from skill directory)
   - 2-3 example pitch deck images from `examples/` folder (use `Read` tool to view visual design patterns)
   - 1-2 HTML template examples from templates folder for reference

4. Use `TodoWrite` to create checklist:
   - [ ] Content analysis and collaborative editing
   - [ ] Text wireframes generation
   - [ ] ASCII wireframes confirmation
   - [ ] HTML slides generation
   - [ ] Visual preview and iteration
   - [ ] PowerPoint creation
   - [ ] Google Slides creation (if requested)

**Output:** Complete understanding of requirements + loaded resources.

---

### Phase 2: Content Analysis & Collaborative Editing

**Goal:** Refine content for maximum narrative impact through collaborative editing.

**Analysis Criteria:**
Evaluate content against EdTech pitch deck best practices:
- **Narrative flow:** Story builds logically (Problem → Solution → Market → Why Us)
- **Clarity:** Each point immediately understandable (no jargon, concrete examples)
- **Emotional impact:** Connects with investor motivations (FOMO, vision, urgency)
- **Data balance:** Right mix of numbers and story (not too dry, not too fluffy)
- **Slide economy:** Can any slides be combined/removed? (10-20 slides ideal)
- **Audience alignment:** Tone matches investor expectations (confident but honest)

**Analysis Process:**
1. Read through ALL slide content
2. Identify issues per slide:
   - Redundant points
   - Unclear messaging
   - Missing emotional hooks
   - Too much/too little data
   - Poor narrative transitions
   - Weak value propositions

3. Prioritize by impact: HIGH (narrative/clarity) > MEDIUM (emotional/data) > LOW (polish)

**Edit Presentation Format:**
For each proposed change, show:
```
═══════════════════════════════════════════════
SLIDE X: [Slide Title]
SECTION: [Which part of the slide]

CURRENT:
[Original text]

PROPOSED:
[Edited text]

RATIONALE:
[Why this change improves the pitch - specific principle applied]

IMPACT: [High/Medium/Low] - [Narrative/Clarity/Emotional/Data]
═══════════════════════════════════════════════
```

**Presentation Strategy:**
- Present 3-5 edits at a time (don't overwhelm)
- Start with HIGH impact changes first
- After each batch, ask: "Approve all | Approve some | Reject all | Suggest alternative"
- If "Approve some": Present each edit individually for Accept/Reject decision
- If "Suggest alternative": Listen to user's direction, regenerate proposals

**Editing Guidelines:**
- **Preserve founder's voice** - Don't make it sound generic
- **Respect data integrity** - Never change numbers without explicit approval
- **Flag assumptions** - If proposing content not in original, clearly mark as [SUGGESTED ADDITION]
- **Prioritize high-impact** - Show most important changes first
- **Show before/after** - Make it easy to compare

**Collaborative Loop:**
1. Present batch of edits
2. Gather user decisions
3. Apply approved changes
4. Present next batch
5. Repeat until all slides reviewed

**Output:**
- Refined content markdown with all approved edits applied
- Use `Write` tool to save: `./pitch_deck_output/content_refined.md`
- Mark Phase 2 todo as complete

---

### Phase 3: Text Wireframes

**Goal:** Define slide layouts in text form before visual design.

**For each slide, describe:**
- **Layout structure:** Header placement, content zones (left/right/center), footer
- **Content organization:** How many sections, how points are grouped
- **Visual emphasis:** Which elements are primary/secondary/tertiary
- **Special elements:** Stats callout boxes, charts, images, tables

**Text Wireframe Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE X: [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT TYPE: [Full-bleed header | Split-screen | Centered | Grid]

HEADER ZONE:
- Background: [Brand color]
- Title: [Large, bold, brand accent color]
- Position: [Top-left | Centered | Top-banner]

CONTENT ZONE:
- Organization: [3-column | Left-text-right-visual | Bullet list | Cards]
- Primary element: [Main headline or key stat]
- Secondary elements: [Supporting points]
- Emphasis: [Callout box | Color highlight | Size variation]

SPECIAL ELEMENTS:
- [Stats callout box bottom-right]
- [Chart placeholder center]
- [Icon grid for features]

FOOTER:
- [Logo left | Page number right]

WHITESPACE: [~35% of slide]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Validation:**
After presenting all text wireframes, ask:
"Do these layouts support the narrative flow? Any slides that need restructuring?"

If user requests changes, update wireframes before proceeding.

**Output:**
- Text wireframe descriptions for all slides
- Use `Write` tool to save: `./pitch_deck_output/wireframes_text.md`
- Mark Phase 3 todo as complete

---

### Phase 4: ASCII Wireframes

**Goal:** Show spatial relationships and visual hierarchy before committing to code.

**ASCII Wireframe Format:**
```
╔═══════════════════════════════════════════════════════════════╗
║                         SLIDE X: [TITLE]                      ║
╠═══════════════════════════════════════════════════════════════╣
║ ┌───────────────────────────────────────────────────────────┐ ║
║ │                     [HEADER BANNER]                       │ ║
║ │            ████████ SLIDE TITLE ████████                  │ ║
║ └───────────────────────────────────────────────────────────┘ ║
║                                                               ║
║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ║
║  │   POINT 1   │  │   POINT 2   │  │   POINT 3   │         ║
║  │             │  │             │  │             │         ║
║  │ • Detail    │  │ • Detail    │  │ • Detail    │         ║
║  │ • Detail    │  │ • Detail    │  │ • Detail    │         ║
║  └─────────────┘  └─────────────┘  └─────────────┘         ║
║                                                               ║
║                                     ┌──────────────────┐     ║
║                                     │ ▓▓ STAT CALLOUT  │     ║
║                                     │ 114 hours/year   │     ║
║                                     │ $5,800+ wasted   │     ║
║                                     └──────────────────┘     ║
║ ─────────────────────────────────────────────────────────── ║
║ [Logo]                                         Page X of Y   ║
╚═══════════════════════════════════════════════════════════════╝
```

**Visual Elements Key:**
- `████` = Primary emphasis (titles, headers)
- `▓▓` = Secondary emphasis (stats, callouts)
- `│─┐┘┌└` = Boxes/containers
- `╔═╗╚╝║` = Slide borders
- Spacing = Whitespace (critical for readability)

**Create ASCII wireframes for:**
- All slides from Phase 3
- Show spatial relationships clearly
- Indicate relative sizing (bigger boxes = more emphasis)
- Demonstrate whitespace distribution

**Presentation:**
Present 3-4 wireframes at a time with brief explanation of design rationale.

**Validation:**
After showing all ASCII wireframes:
"Do these visual layouts work for you? Any slides need adjustment before we code them?"

If changes needed, regenerate specific wireframes.

**Output:**
- ASCII wireframes for all slides
- Use `Write` tool to save: `./pitch_deck_output/wireframes_ascii.txt`
- Mark Phase 4 todo as complete

---

### Phase 5: HTML Slide Generation

**Goal:** Create professional HTML slides with proper styling and brand application.

**Visual Design Reference:**
Before generating HTML, review example pitch deck images from `examples/` folder to understand:
- Professional slide layouts and spacing
- Effective use of visual hierarchy
- Color palette application
- Balance between text and visuals
- Modern design patterns for investor decks

**Design Principles Application:**

**Visual Hierarchy:**
- Titles: 36-54pt, bold, brand primary color
- Headings: 24-30pt, bold, dark neutral
- Body text: 14-18pt, regular weight, high contrast
- Captions/Stats: 12-16pt, accent color for emphasis

**Layout Principles:**
- **Whitespace:** 30-40% of slide should be empty (breathing room)
- **Alignment:** Consistent grid system (left-align text blocks, center hero content)
- **Contrast:** High contrast for readability (dark text on light background, or vice versa)
- **Focal point:** One primary element per slide (eye knows where to look first)
- **Color psychology:** Brand colors reinforce identity, accent colors guide attention

**EdTech-Specific Design:**
- Problem slides: Contrasting colors to show pain (reds/oranges for urgency)
- Solution slides: Calm, confident colors (blues/greens for trust)
- Data slides: Clean charts, not cluttered tables (visualize numbers)
- Team slides: Professional but approachable (headshots + credentials)

**Template Structure:**
Follow existing HTML template pattern (like slide01_cover.html):
```html
<!DOCTYPE html>
<html>
<head>
<style>
html { background: #ffffff; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: [background-color];
  font-family: [user-specified-font], Arial, sans-serif;
  display: flex;
  /* Layout specific to slide type */
}
/* Slide-specific styles */
</style>
</head>
<body>
<!-- Content structured per wireframe -->
</body>
</html>
```

**Dimensions:**
- 720pt × 405pt (16:9 aspect ratio)
- Standard presentation size

**Generation Process:**
1. For each slide:
   - Load approved wireframe
   - Apply refined content
   - Insert user's brand colors
   - Apply design principles
   - Generate clean HTML + CSS

2. Use `Write` tool to create: `./pitch_deck_output/slideXX_[topic].html`

3. Special slide types:
   - **Tables:** Use proper HTML table markup (competitive analysis, financials)
   - **Charts:** Create CSS-based visualizations or note placeholders for later insertion
   - **Icons:** Use unicode symbols or note where custom icons needed

**Quality Checks:**
- ✅ Color contrast meets WCAG AA standards (4.5:1 for text)
- ✅ No slide has >100 words (slide economy)
- ✅ Font sizes readable at distance (14pt minimum)
- ✅ Visual hierarchy clear (title > heading > body obvious)
- ✅ Whitespace properly distributed (30-40%)

**Output:**
- Individual HTML files for each slide: `slideXX_[topic].html`
- Mark Phase 5 todo as complete

---

### Phase 6: Visual Preview & Iteration

**Goal:** User reviews designs and requests any adjustments.

**Preview Generation:**
1. Create `slide_preview.html` showing all slides:
```html
<!DOCTYPE html>
<html>
<head>
<style>
.preview-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 20px;
}
.slide-preview {
  border: 2px solid #ccc;
  background: white;
}
.slide-preview iframe {
  width: 360px;
  height: 202.5px;
  border: none;
}
.slide-label {
  text-align: center;
  padding: 5px;
  background: #f5f5f5;
  font-family: Arial, sans-serif;
}
</style>
</head>
<body>
<div class="preview-container">
  <!-- iframe for each slide -->
</div>
</body>
</html>
```

2. Use `Write` tool to create: `./pitch_deck_output/slide_preview.html`

3. Tell user: "Preview file created at: ./pitch_deck_output/slide_preview.html - Open in browser to review all slides"

**Iteration Process:**
1. Ask: "How do the slides look? Any adjustments needed?"

2. If changes requested:
   - User specifies: "Slide 5 feels cluttered" or "Change color on slide 8"
   - Identify specific issue
   - Regenerate ONLY affected slides
   - Update preview file
   - Show user the changes

3. Repeat until user approves

**Common Adjustments:**
- Color tweaks (contrast, mood)
- Content spacing (more/less whitespace)
- Font size adjustments
- Layout refinements
- Emphasis changes (what stands out)

**Exit Criteria:**
User explicitly says: "Looks great" | "I approve these designs" | "Let's create the deck"

**Output:**
- Approved HTML slides ready for conversion
- Mark Phase 6 todo as complete

---

### Phase 7: Final Deck Creation (Hybrid Approach)

**Goal:** Generate PowerPoint and/or Google Slides from approved HTML designs.

---

#### **Option A: PowerPoint Creation via Node.js**

**Prerequisites Check:**
1. Use `Bash` to check Node.js installation:
```bash
node --version
```

2. Check if dependencies exist:
```bash
cd ./pitch_deck_output && ls node_modules 2>/dev/null
```

3. If dependencies missing, install:
```bash
cd ./pitch_deck_output && npm init -y && npm install pptxgenjs
```

**Script Generation:**

1. Copy html2pptx.js converter from template directory:
```bash
cp /Users/bmcmanus/Documents/my_docs/portfolio/lucid-north.com/business/pitch_deck_workspace/html2pptx.js ./pitch_deck_output/
```

2. Generate custom `create_pitch_deck.js` using `Write` tool:
```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx.js');

async function createPitchDeck() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = '[User Name/Company]';
    pptx.title = '[Deck Title]';

    // Slide 1: Cover
    await html2pptx('slide01_cover.html', pptx);

    // Slide 2: Problem
    await html2pptx('slide02_problem.html', pptx);

    // [... add all slides ...]

    // Handle special slides with tables/charts
    // [table generation code if needed]

    // Save presentation
    await pptx.writeFile({ fileName: '[DeckName]_Pitch_Deck.pptx' });
    console.log('Pitch deck created successfully!');
}

createPitchDeck().catch(err => {
    console.error('Error creating pitch deck:', err);
    process.exit(1);
});
```

3. Use `Write` tool to save: `./pitch_deck_output/create_pitch_deck.js`

**Execution:**
```bash
cd ./pitch_deck_output && node create_pitch_deck.js
```

**Validation:**
- Check for .pptx file creation
- If errors, troubleshoot dependencies or HTML formatting issues

**Output:**
Tell user: "PowerPoint deck created: ./pitch_deck_output/[DeckName]_Pitch_Deck.pptx"

---

#### **Option B: Google Slides Creation via API**

**Prerequisites:**
1. Check if Google Slides API is available
2. Verify user authentication

**Process:**
1. Create new presentation via API
2. For each HTML slide:
   - Parse HTML structure
   - Extract text content and styling
   - Convert to Google Slides API format:
     - Text boxes with positioning
     - Shapes for containers
     - Colors from brand palette
     - Images (if any)

3. Add slides sequentially
4. Apply master theme if available

**API Conversion Logic:**
```
HTML element → Slides API element
<h1> → Text box (title style)
<p> → Text box (body style)
<div class="stats-box"> → Shape with fill + text
<ul><li> → Bulleted text box
```

**Authentication Handling:**
- If auth fails: Inform user, provide setup instructions
- Fall back to PowerPoint option if Google Slides unavailable

**Output:**
- Google Slides presentation link
- Share with user: "Google Slides deck created: [link]"

---

#### **Both Options Workflow:**

If user selected "Both formats":
1. Generate PowerPoint first (Option A)
2. Then generate Google Slides (Option B)
3. Provide both outputs to user

**Final Deliverables:**
- ✅ PowerPoint file: `./pitch_deck_output/[DeckName]_Pitch_Deck.pptx`
- ✅ Google Slides link (if requested)
- ✅ All HTML source files (for future edits)
- ✅ Preview file (for quick reference)

**Mark Phase 7 todo as complete**

---

## Error Handling & Common Issues

### Issue: Content File Not Structured Correctly

**Detection:** Missing slide markers like "## SLIDE X:", inconsistent formatting

**Solution:**
1. Show user the expected format:
```markdown
## SLIDE 1: COVER SLIDE
**Title:** [Title text]
**Tagline:** [Tagline text]

## SLIDE 2: THE PROBLEM
### [Section Heading]
[Content...]
```

2. Offer to restructure if possible, or ask user to fix and re-run

---

### Issue: Brand Colors Don't Provide Enough Contrast

**Detection:** Contrast ratio calculation fails WCAG AA standards (<4.5:1)

**Solution:**
1. Calculate contrast ratio between text and background
2. If fails: Suggest adjusted shades
   - Darken text or lighten background
   - Show before/after hex codes
3. Preview adjusted colors in one slide
4. Get user approval before applying globally

---

### Issue: Too Much Content Per Slide

**Detection:** Character count >500 per slide, >5 bullet points

**Solution:**
1. Identify overloaded slide
2. Propose splitting into 2 slides with clear flow:
   - Example: "Slide 5 has 8 bullet points. Split into 'Part 1' and 'Part 2'?"
3. Show proposed content division
4. User approves split

---

### Issue: Node.js Conversion Fails

**Detection:** Script error, dependency issues, HTML parsing failures

**Solution:**
1. Check error message
2. Common fixes:
   - Install missing dependencies: `npm install pptxgenjs`
   - Validate HTML (check for unclosed tags)
   - Simplify complex CSS (some styles don't convert)
3. If unfixable: Offer HTML-only fallback
   - User can manually import HTML to PowerPoint
   - Provide instructions for import process

---

### Issue: Google Slides API Authentication Fails

**Detection:** API returns 401/403 errors

**Solution:**
1. Inform user: "Google Slides API authentication required"
2. Provide setup instructions:
   - Enable Google Slides API in Google Cloud Console
   - Create OAuth credentials
   - Authorize application
3. Fall back to PowerPoint option
4. Offer to retry after user completes setup

---

## Quality Validation Checklist

Before marking any phase complete, verify:

### Content Quality (Phase 2)
- ✅ All required slides present (Cover, Problem, Solution, Market, Team, Ask)
- ✅ No slide has >5 bullet points (slide economy principle)
- ✅ Stats formatted consistently ($5.8K vs $5,800 - pick one style)
- ✅ Every claim has supporting evidence or rationale
- ✅ Narrative flows logically without gaps
- ✅ Tone matches target audience expectations

### Design Quality (Phase 5)
- ✅ Color contrast meets WCAG AA (4.5:1 minimum)
- ✅ Font sizes readable (14pt minimum body text)
- ✅ No text-heavy slides (>100 words triggers warning)
- ✅ Visual hierarchy clear (title > heading > body obvious)
- ✅ Brand colors applied consistently
- ✅ Whitespace properly distributed (30-40%)

### Technical Quality (Phase 7)
- ✅ All HTML files validate (no broken tags)
- ✅ CSS renders correctly (test in browser)
- ✅ Node.js dependencies installed (if using PowerPoint)
- ✅ Output files created successfully
- ✅ Files have correct naming convention

---

## Success Metrics

A successful pitch deck creation includes:
- ✅ Content refined through collaborative editing (>3 meaningful improvements made)
- ✅ Visual designs approved at wireframe stage (no major revisions in HTML phase)
- ✅ Final deck generated in requested format(s)
- ✅ User can present immediately (no additional work needed)
- ✅ Design follows best practices (validated against checklist)
- ✅ User expresses satisfaction: "This looks great" or equivalent

---

## Key Principles

**Throughout the process:**

1. **Collaborative, not prescriptive** - Always show before/after, explain rationale, get approval
2. **Validate early, validate often** - Catch issues at wireframe stage, not after coding
3. **Preserve founder's voice** - Refine, don't replace; maintain authenticity
4. **Design with purpose** - Every visual choice supports narrative goals
5. **Iterate gracefully** - Make it easy to adjust specific elements without redoing everything
6. **Educate as you go** - Explain design principles so user learns for future decks

**Remember:**
- This is the user's pitch, not yours - guide, don't dictate
- Investors see dozens of decks - help user stand out with clarity + design
- Every slide should pass the "glance test" - key message clear in 3 seconds
- If user disagrees with a suggestion, respect their judgment (they know their business)

---

## After Completion

Once deck is created:

1. **Summarize what was delivered:**
   - Number of slides created
   - Key improvements made during editing phase
   - Format(s) provided (PowerPoint/Google Slides)
   - Location of all output files

2. **Offer additional support:**
   - "Need any slides adjusted?"
   - "Want to create alternate versions (different audiences)?"
   - "Should I generate speaker notes for any slides?"

3. **Suggest next steps:**
   - "Practice the pitch with these slides"
   - "Get feedback from advisors"
   - "Iterate based on investor questions"

---

## Notes for Skill Maintenance

**Resource locations are hardcoded:**
- Best practices: `/Users/bmcmanus/Documents/pitch_deck_skill/`
- HTML templates: `/Users/bmcmanus/Documents/my_docs/portfolio/lucid-north.com/business/pitch_deck_workspace/`

**If resources move:**
Update paths in Phase 1 and Phase 7 (Option A: PowerPoint creation)

**If new best practices added:**
Skill will automatically incorporate them during Phase 1 resource loading

**If HTML template structure changes:**
Update Phase 5 template structure section to match new pattern

---
name: linkedin-carousel-builder
description: >
  Build branded LinkedIn carousel PDFs optimized for engagement and virality.
  Use this skill when asked to create a LinkedIn carousel, document post, swipeable slides,
  or any multi-slide visual content for LinkedIn. Also triggers on "carousel", "slides for LinkedIn",
  "LinkedIn PDF", "swipeable post", or "document post".
---

# LinkedIn Carousel Builder

Create high-performing LinkedIn carousel PDFs that are branded, mobile-optimized, and designed for maximum engagement.

## Workflow

### Phase 1: Research & Strategy

Before building any carousel, research current best practices:

1. **Topic validation**: Confirm the topic has engagement potential on LinkedIn
2. **Hook research**: Study what carousel hooks are performing well right now
3. **Competitor scan**: Look at top-performing carousels in the same niche
4. **Slide count**: Determine optimal slide count (8-15 for max engagement, 5-7 for quick takes)

### Phase 2: Content Architecture

Structure the carousel for completion rate (LinkedIn rewards 60%+ completion):

**Slide Framework:**

| Slide | Purpose | Priority |
|-------|---------|----------|
| 1 | **Scroll stopper** — Bold claim, surprising stat, or provocative question | Critical |
| 2-3 | **Context/Problem** — Set up the story or tension | High |
| 4-6 | **Value/Data** — Core insights, metrics, proof points | High |
| 7-8 | **So what** — What this means for the reader | High |
| Last | **CTA** — Question, brand, call to action | Critical |

**Content rules:**
- Each carousel must be **self-explanatory** — a reader should understand the full story without any external context or the accompanying post text
- Every slide must contain a real insight, not filler. Data points, lessons, or actionable takeaways on every slide
- One idea per slide
- 25-40 words per slide maximum
- No walls of text — use visual hierarchy
- Every slide must earn the swipe to the next one
- Tease next slide content to drive completion

**Visual clarity rules:**
- Font sizes must be large enough to invite reading, not strain the eyes (see typography table below)
- High contrast between text and background at all times — never use light text on light backgrounds or dark text on dark backgrounds
- Color palette should be clean and consistent — use brand accents to highlight, not overwhelm
- Layout should feel spacious, not cramped. Generous whitespace > more content
- Visually attractive design that makes people want to swipe — think magazine quality, not PowerPoint

### Phase 3: Design & Build

Build as a single HTML file with inline CSS for Playwright export.

#### LinkedIn Document Specs (4:5 Portrait)

```
Width:  1080px
Height: 1350px
Format: PDF export via Playwright
```

#### LinkedIn Safe Zones (CRITICAL)

LinkedIn's document viewer overlays controls that crop content. ALL content must stay inside these safe zones:

```
┌─────────────────────────────────┐
│         TOP CROP ZONE           │  80px — no content here
│─────────────────────────────────│
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │      SAFE CONTENT ZONE    │  │  80px side margins
│  │                           │  │
│  │      920px x 1130px       │  │
│  │                           │  │
│  └───────────────────────────┘  │
│─────────────────────────────────│
│       BOTTOM CROP ZONE          │  140px — page counter overlay
└─────────────────────────────────┘
```

- **Top padding**: 80px minimum (viewer clips top)
- **Side padding**: 80px minimum (viewer clips edges)
- **Bottom clearance**: 140px minimum (page counter + navigation arrows overlay)
- **No progress bars**: LinkedIn crops them — remove entirely
- **Footer (logo + URL)**: Must sit at `margin-bottom: 140px` or higher

#### CSS Baseline

```css
.slide {
  width: 1080px;
  height: 1350px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Footer sits above LinkedIn's 140px overlay */
.slide-footer {
  margin-top: auto;
  margin-bottom: 140px;
  padding: 18px 80px 0;
}

/* Swipe teaser — inline, not absolute positioned */
.swipe-teaser {
  text-align: center;
  margin-top: 12px;
  margin-bottom: 0;
}

@media print {
  body { background: white; gap: 0; padding: 0; }
  .slide { page-break-after: always; box-shadow: none; }
}
```

#### Typography for Mobile Readability

LinkedIn renders 1080px slides at ~350px on mobile. Minimum sizes:

| Element | Min Size | Recommended |
|---------|----------|-------------|
| Headlines (H1) | 40px | 44-50px |
| Subheadings (H2) | 32px | 36-44px |
| Body text | 20px | 22-26px |
| Metric numbers | 56px | 66-82px |
| Labels/captions | 16px | 18-22px |
| Tags/badges | 16px | 17-20px |
| Footer text | 15px | 16-18px |

#### Brand Application

Always apply Solum Health brand guidelines (see `solum-health-brand` skill):
- Font: DM Sans (400, 500, 700)
- Primary: Navy #011C40, Solum Blue #468AF7
- Accents: Teal #70D3C6, Purple #A16CF4
- Footer: SolumHealth logo + getsolum.com on every slide

### Phase 4: Visual Validation

**MANDATORY**: Before exporting the final PDF, run design validation:

1. **Screenshot each slide** using Playwright
2. **Check safe zones**: Verify no content in top 80px, bottom 140px, or within 80px of sides
3. **Mobile readability test**: All text must be legible at 1/3 scale
4. **Color contrast**: Ensure text passes WCAG AA contrast on its background
5. **Consistency check**: All slides same dimensions, same footer placement, same brand treatment
6. **No overlapping**: Swipe teasers must be inline (not absolute positioned), never overlap content
7. **No clipping**: All text fully visible, no letters cut off at edges

### Phase 5: Export & Deliver

1. **Export PDF** via Playwright at exactly 1080x1350px with `printBackground: true` and zero margins
2. **Verify PDF dimensions**: Confirm all pages are 1080x1350
3. **Save to campaign folder**: `social-media/posts/linkedin/{campaign-name}/`
4. **Only deliver PDF**: No PNGs needed unless specifically requested
5. **Suggest document title**: Make it engaging/viral (this shows in LinkedIn feed)
6. **Suggest post copy**: Write accompanying LinkedIn post text following `writing-linkedin-posts` skill guidelines

### Phase 6: Post-Upload Check

If the user shares a screenshot from LinkedIn after uploading:
- Check if content is getting cropped at top/bottom
- Check if slides display at correct aspect ratio
- Suggest adjustments if LinkedIn's viewer is cutting content

## Engagement Best Practices

### Hook Patterns That Drive Swipes

- **Surprising stat**: "$835M for a company that was worth $0.52"
- **Contrarian take**: "Everyone is wrong about [topic]"
- **Before/after**: Show transformation with data
- **Curiosity gap**: Promise a reveal in the slides
- **Breaking news**: Time-sensitive industry events

### Visual Patterns That Perform

- **Dark slides for data** — Navy backgrounds make numbers pop
- **Light slides for text** — White backgrounds for readability
- **Alternating dark/light** — Creates visual rhythm, prevents fatigue
- **One big number per slide** — Scannable at mobile size
- **Real photos > stock** — Authenticity drives engagement
- **Brand color accents** — Consistent but not overwhelming

### Completion Rate Tactics

- **Tease next slide**: "Next: The one pivot that changed everything"
- **Build narrative tension**: Each slide should leave a question
- **Save the best insight for slide 3-4**: Hook them past the drop-off point
- **End with a question**: Drives comments, which drives reach
- **Keep it to 5-10 slides**: Completion drops sharply after 10

## Output Checklist

Before delivering the carousel, verify:

- [ ] All slides exactly 1080x1350px
- [ ] Content within safe zones (80px top, 80px sides, 140px bottom)
- [ ] Text readable at mobile size (min 20px body, 40px+ headlines)
- [ ] Solum Health branding on every slide (logo + URL in footer)
- [ ] No absolute-positioned elements that could overlap
- [ ] Swipe teasers visible and not overlapping content
- [ ] PDF exported with `printBackground: true`
- [ ] Campaign folder created with descriptive name
- [ ] Engaging document title suggested
- [ ] Post copy drafted

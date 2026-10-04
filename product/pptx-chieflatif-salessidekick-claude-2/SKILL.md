---
name: pptx
description: "Fires when the user requests a presentation or deck and Gamma is not available (or user prefers PPTX). Provides: PptxGenJS code generation pipeline, brand tokens (colors, fonts, logo), 5 deck templates (executive, technical, competitive, QBR, custom), and visual QA checklist. Output contract: a downloadable .pptx file with consistent branding."
user-invocable: false
---

# PPTX — Presentation Generation Skill

## Purpose

Defines the PptxGenJS pipeline for generating native .pptx presentations. Contains brand token integration specs, the 5 deck templates with 8 slides each, and the visual QA pipeline. This is the primary presentation generation path; Gamma is the alternative.

## When Referenced

- **Creating presentations** (create-deck intent, pptx path) — uses this skill for native .pptx generation as the default presentation path. Fires when the user requests a deck and pptx is the selected output format.
- **Deep personalization sessions** (customize-system intent) — captures brand tokens (logo, colors, fonts) for presentation branding during setup

## Core Framework

### PptxGenJS Pipeline

SalesSidekick generates presentations using PptxGenJS, a JavaScript library for creating PowerPoint files programmatically.

**Generation flow:**
1. Load brand tokens (logo, colors, fonts) from deep personalization configuration
2. Select template based on deal stage or user preference
3. Populate 8 slides with account-specific content
4. Apply brand styling throughout
5. Generate .pptx file
6. Run visual QA if available (LibreOffice → PDF → JPEG)
7. Present slide summary with evidence grades

### Brand Tokens

Captured during deep personalization Phase 5 (Presentation Brand):

| Token | Description | Default |
|-------|-------------|---------|
| **Logo** | Company logo file (PNG/SVG) | SalesSidekick placeholder |
| **Primary Color** | Main brand color (hex) | #2563EB (blue) |
| **Secondary Color** | Accent color (hex) | #1E40AF (dark blue) |
| **Background Color** | Slide background (hex) | #FFFFFF (white) |
| **Text Color** | Primary text color (hex) | #1F2937 (dark gray) |
| **Heading Font** | Font for titles | Arial Bold |
| **Body Font** | Font for body text | Arial |

### 5 Deck Templates

Each template produces exactly 8 slides. Templates auto-select based on deal stage but can be overridden by the user.

#### Template 1: Discovery Deck
*Auto-selects: Stage = Prospecting or Discovery*

| Slide | Title | Content |
|-------|-------|---------|
| 1 | Title Slide | {{COMPANY}} + prospect company name + meeting date |
| 2 | About Us | {{COMPANY}} overview — who we are, what we do (from company-intel) |
| 3 | Your World | Industry context — trends and challenges relevant to the prospect |
| 4 | Common Challenges | 3 pain points typical for their industry/size (from research or ICP) |
| 5 | How We Help | Approach overview — methodology, not features (Commandment 9) |
| 6 | Proof Points | 2-3 relevant case studies or metrics (evidence-graded) |
| 7 | Discovery Questions | Key questions to explore together (from MEDDPICC gaps) |
| 8 | Next Steps | Proposed agenda for follow-up, contact info |

#### Template 2: POV Deck
*Auto-selects: Stage = Qualification*

| Slide | Title | Content |
|-------|-------|---------|
| 1 | Title Slide | "Point of View: [Prospect Company]" + date |
| 2 | Executive Anchor | 2-sentence framing of their business challenge |
| 3 | The Blind Spot | Insight they haven't fully quantified (from POV model) |
| 4 | Math of Pain | Quantified cost of inaction (evidence-graded) |
| 5 | The Approach | How we solve it — methodology, not product (Commandment 9) |
| 6 | Proof: Similar Company | Case study from a similar company (industry, size) |
| 7 | Proof: Results | Specific metrics and outcomes (evidence-graded) |
| 8 | Recommended Next Step | Proportional CTA based on stage |

#### Template 3: Executive Summary
*Auto-selects: Stage = Proposal*

| Slide | Title | Content |
|-------|-------|---------|
| 1 | Title Slide | "Executive Summary: [Prospect Company]" + date |
| 2 | Business Context | Their situation — what they told us (Verified from calls) |
| 3 | Agreed Requirements | Decision criteria confirmed in discovery (Verified) |
| 4 | Proposed Solution | What we're proposing — mapped to their requirements |
| 5 | Business Impact | ROI / projected outcomes (evidence-graded, show the math) |
| 6 | Implementation | Timeline, milestones, resource requirements |
| 7 | Investment | Pricing overview — positioned as investment, not cost |
| 8 | Decision & Next Steps | Proposed decision timeline, mutual action plan |

#### Template 4: QBR (Quarterly Business Review)
*Auto-selects: Stage = Closed Won (existing customer)*

| Slide | Title | Content |
|-------|-------|---------|
| 1 | Title Slide | "Quarterly Business Review: [Customer]" + quarter |
| 2 | Relationship Summary | Account overview, key stakeholders, engagement history |
| 3 | Outcomes Achieved | What we've delivered — metrics and wins (Verified) |
| 4 | Usage & Adoption | How they're using the product — engagement data |
| 5 | Value Delivered | ROI realized vs. projected (evidence-graded) |
| 6 | Roadmap & Innovation | What's coming — relevant product updates |
| 7 | Growth Opportunities | Expansion possibilities — whitespace analysis |
| 8 | Next Quarter Plan | Agreed priorities and success metrics |

#### Template 5: Competitive Displacement
*Auto-selects: Primary Competitor field is populated*

| Slide | Title | Content |
|-------|-------|---------|
| 1 | Title Slide | "Why [Our Company] vs [Competitor]" + date |
| 2 | Your Requirements | Decision criteria mapped (from discovery) |
| 3 | Approach Comparison | Methodology differences — not feature checklist |
| 4 | Where We Excel | 3 key differentiators with evidence (from battlecard) |
| 5 | Customer Evidence | Case study of customer who switched from competitor |
| 6 | Total Value | TCO or total value comparison (evidence-graded) |
| 7 | Risk of Status Quo | What they lose by staying with current approach |
| 8 | Transition Plan | How switching works — minimize risk, maximize speed |

### Visual QA Pipeline

When LibreOffice is available on the system:

1. **Generate .pptx** using PptxGenJS
2. **Convert to PDF** using LibreOffice headless mode: `libreoffice --headless --convert-to pdf`
3. **Convert PDF pages to JPEG** for visual review
4. **Review images** for layout issues, text overflow, branding consistency
5. **Flag issues** if any slides have visual problems

**When LibreOffice is NOT available:**
- Skip visual QA
- Present slide-by-slide text summary instead
- Note: "Visual QA unavailable — review the .pptx file manually before presenting."

### Slide Design Principles

- **Maximum 6 bullet points per slide** — less is more
- **No walls of text** — use visuals, charts, or white space
- **Consistent branding** — logo on every slide, consistent colors
- **Evidence grades visible** — tag key claims inline
- **One message per slide** — if a slide has two messages, split it

## Personalization Notes

- Brand tokens captured during deep personalization Phase 5 (Tier 2 variables)
- Case studies and proof points come from company-intel skill (Tier 3 — regenerated)
- Competitive positioning comes from battlecards skill (Tier 3 — regenerated)
- Template selection is universal logic — no personalization needed
- PptxGenJS pipeline is universal

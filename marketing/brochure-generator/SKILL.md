---
name: brochure-generator
description: Generates premium, multi-page, mobile-optimized (1:1 aspect ratio) PDF marketing brochures for exclusive retreats, workshops, luxury events, or any high-end product/service offering. Use this skill whenever a user asks to create a brochure, marketing PDF, event flyer, WhatsApp marketing material, social media brochure, or design a multi-page promotion document. Also trigger when users mention wanting to promote an experience, product, or service and need visual marketing material. Even if the user just says "make a brochure for my event" or "I need a PDF for my product," use this skill.
---

# Brochure Generator

A premium AI-powered workflow for generating visually stunning, WCAG AAA-compliant, mobile-optimized PDF marketing brochures using web research, stock imagery, expert HTML design, and PDF conversion via Puppeteer.

This skill adopts the **"Sacred Drift" Visual Architect persona** — a design philosophy rooted in warmth, trust, and psychological depth — to produce brochures that feel hand-crafted rather than AI-generated.

---

## When to Use This Skill

Use this skill when the user wants to:
- Generate a marketing brochure for an event, retreat, workshop, or product launch
- Create a PDF that can be shared on WhatsApp or social media
- Design a multi-page campaign document for a premium offering
- Reproduce a past brochure style using the themes library
- Export a visually rich HTML layout as a pixel-perfect PDF

---

## Workflow Overview

Follow these phases **in order**. Do not skip any phase.

### Phase 1 — Research & Context Gathering

1. **Read the generator prompt** at `prompts/generators/prompt.md` before starting. It contains the business context, persona, design constraints, and output rules for this project.

2. **Understand the brief**: Extract from the user's message:
   - Project/event name and destination
   - Number of pages requested (minimum 5)
   - Any specific theme, mood, or color preference
   - Whether to reuse an existing theme from `themes/`

3. **Check existing themes**: If the user says "use the same style as [past brochure]", read the relevant file from `themes/` for the exact palette, font stack, and layout system.

4. **Conduct web research**: Use the Tavily or Firecrawl MCP to research the destination, the niche/industry, relevant competitor brochures, and specific market details. This research feeds the copy — never invent details blindly.
   - Research queries should include: location landmarks, industry significance, seasonal context, typical high-end itineraries or feature lists, target audience lifestyles.

5. **Fetch stock imagery**: Use the `stock-images-mcp` to search for 1 high-quality Pexels image per brochure page. All images must:
   - Be contextually relevant (correct location, correct mood)
   - Be portrait or 1:1 aspect (not landscape-dominant)
   - Have enough midtone space for text overlay

---

### Phase 2 — Design & HTML Construction

6. **Adopt the Visual Architect persona** (defined in `prompts/generators/prompt.md`): Design with mathematical precision, WCAG AAA compliance, and psychological depth. Avoid "AI slop" patterns at all costs — no generic card layouts, no boring sans-only fonts.

7. **Build the HTML file** (`utils/<brochure_name>.html`) following these **non-negotiable rules**:

   **Layout:**
   - Each page is exactly `1080 × 1080 px` — no more, no less
   - Do NOT add `margin`, `padding`, or `page-break-after/before` on `.page` wrapper elements — this breaks Puppeteer PDF alignment
   - Full-bleed background image per page via `background-image: url(...)`
   - Text floats in 3 vertical zones: top band (eyebrow + rule), mid band (hero copy), bottom band (coda + rule)
   - Horizontal ornament rules: `linear-gradient(to right, transparent, #C9A96E, transparent)` with 1px height
   - Use `✦` glyph for decorative ornaments

   **Color System (default — adjust per theme):**
   ```
   --gold:       #C9A96E  (borders, rules, accents)
   --gold-light: #E8D5A3  (subheadings, eyebrows)
   --cream:      #F5EDD8  (body copy)
   --warm-white: #FAF6EE  (hero headlines)
   --dark-brown: #1A1108  (page background fallback)
   ```

   **Overlay Logic (WCAG AAA):**
   - Use a 3-stop radial or vertical gradient overlay per page
   - Top and bottom: 0.65–0.82 alpha black
   - Middle: 0.40–0.55 alpha black
   - Never use text outlines or text background boxes

   **Typography:**
   - Hero Display: `Cormorant Garamond`, weight 300, 6.4–7.2rem
   - Section Titles: `Cormorant Garamond`, weight 400, 3.8–4.4rem
   - Callout Quotes: `Cormorant Garamond italic`, 2.0–2.4rem
   - Body copy: `Jost`, weight 300, 1.0–1.18rem
   - Eyebrow / Captions: `Jost`, weight 200–300, 0.72–0.85rem, ALL-CAPS, 3.5–8px letter-spacing

   **Minimum pages structure (5-page default):**
   1. Cover — Brand + Date/Title (the invitation)
   2. Vision / Philosophy — Emotional depth (the why)
   3. Context / Highlights — Setting the stage (the context)
   4. Feature Highlights — Core details (the what)
   5. Pricing + CTA — Inclusions, price, contact (the call to action)

   For 7-page brochures, add:
   6. Founder/Expert Bio — Humanise the source (trust signal)
   7. CTA + Contact — Booking instructions

8. **Copy voice**: Warm, reverent, precise. Never salesy. Sentences should be purposeful and unhurried. Reference the research data for accurate details, context, and timing.

---

### Phase 3 — PDF Conversion

9. **Create the Puppeteer conversion script** (`utils/convert_<brochure_name>.js`). Follow the exact template in `references/pdf_converter_template.js` — do not deviate from the viewport or margin settings.

10. **Run the conversion**:
    ```bash
    cd utils && node convert_<brochure_name>.js
    ```

11. **Move outputs** to `pdf_outputs/`:
    ```bash
    mv utils/<BrochureName>.pdf pdf_outputs/
    ```

---

### Phase 4 — Theme Documentation

12. **Create a theme file** at `themes/<brochure_name>_theme.md` documenting:
   - Design philosophy name and description
   - Full color palette table
   - Typography table with role, font, weight, size, and reasoning
   - Layout system summary
   - Image selection table (page → subject → Pexels URL)
   - Image search queries used
   - Content narrative arc (page-by-page)
   - WCAG AAA compliance notes
   - Replication instructions for future brochures

   See `references/theme_template.md` for the exact structure to follow.

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|---|---|---|
| Blank/offset pages in PDF | `margin-bottom` or `page-break-after` on `.page` elements | Remove all margins/breaks from `.page` — use only exact `width: 1080px; height: 1080px` |
| Overflowing text | `font-size` too large for mobile 1:1 | Reduce hero size to 5.5rem or add `overflow: hidden` per zone |
| Missing Google Fonts | Network not available at PDF render time | Embed font `@import` URLs at top of `<style>` — Puppeteer fetches on `networkidle0` |
| Image not loading in PDF | Relative path issue | Use full Pexels `https://` URLs directly; never local relative paths |

---

## Required MCP Servers

This skill requires these MCP servers to be configured in your agent's MCP config file (e.g., `mcp_config.json` for Cursor/Windsurf or `claude_desktop_config.json` for Claude Desktop):

| Server | Purpose |
|---|---|
| `tavily-mcp` | Web research — destination info, copy ideas, competitor analysis |
| `firecrawl-mcp` | Deep web scraping when Tavily results are insufficient |
| `stock-images-mcp` | Search and download Pexels stock images by subject keyword |

See the project `README.md` for installation and configuration steps.

---

## Reference Files

- `references/theme_template.md` — Template structure for new theme files
- `references/pdf_converter_template.js` — Canonical Puppeteer PDF conversion script
- `assets/design_checklist.md` — Pre-export quality gate checklist

Read these when needed during the workflow — they are not loaded automatically.

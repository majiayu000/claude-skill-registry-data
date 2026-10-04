---
name: frontend-cv
description: Create professional HTML/PDF resumes from any input format (md/pdf/word/txt). Extracts resume data, converts to structured YAML, generates styled HTML with multiple theme options, and exports to PDF. Use when users want to create, convert, or redesign their CV/resume with modern web styling.
---

# Frontend CV

Generate professional, print-ready HTML resumes that export cleanly to PDF. Prefer the bundled renderer for consistent theme layouts.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS. No npm, no build tools.
2. **Print-First Design** — Every style must look perfect in PDF export via browser print.
3. **Structured Data** — Extract and normalize resume data into clean YAML format.
4. **Visual Choice** — Show style previews, let users pick what resonates.
5. **Theme Fidelity** — The five built-in themes provide distinct professional styles: classic, modern, academic, and engineering-focused layouts.

## Design Aesthetics

Create distinctive, professional resumes that stand out:
- **Typography**: Use elegant, readable fonts (avoid generic system fonts)
- **Layout**: Clear hierarchy, scannable sections, optimal whitespace
- **Color**: Professional palettes that print well (consider B&W printing)
- **Print-Ready**: Perfect @media print CSS for clean PDF export

Avoid generic templates:
- Overused fonts (Arial, Times New Roman, Calibri)
- Cluttered layouts with poor spacing
- Colors that don't print well
- Inconsistent styling

## Phase 0: Detect Input Mode

Determine what the user provides:

- **Mode A: Structured Data** — User provides YAML/JSON → Go to Phase 2
- **Mode B: Document Conversion** — User provides PDF/Word/Markdown/Text → Go to Phase 1
- **Mode C: From Scratch** — User wants to build from conversation → Go to Phase 1 (interactive)

## Phase 1: Extract & Structure Data

### Step 1.1: Extract Content

**For document files (PDF/DOCX/TXT/MD):**

Run extraction script:
```bash
python scripts/extract_resume.py <input_file> --output resume_data.txt
```

The script handles:
- PDF: Extract text with layout preservation
- DOCX: Parse document structure
- TXT/MD: Direct text read

### Step 1.2: AI-Assisted Structuring

Read the extracted text and convert to YAML format. Use this structure:

```yaml
cv:
  name: Full Name
  headline: Professional Title
  location: City, Country
  email: email@example.com
  phone: +1234567890
  website: https://example.com
  social_networks:
    - network: LinkedIn
      username: username
    - network: GitHub
      username: username
  sections:
    summary:
      - Brief professional summary paragraph
    experience:
      - company: Company Name
        position: Job Title
        start_date: YYYY-MM
        end_date: present
        location: City, Country
        highlights:
          - Achievement or responsibility
          - Another achievement
    education:
      - institution: University Name
        degree: Degree Type
        area: Field of Study
        start_date: YYYY-MM
        end_date: YYYY-MM
        location: City, Country
        highlights:
          - Notable achievement
    skills:
      - label: Category
        details: Skill1, Skill2, Skill3
    projects:
      - name: Project Name
        date: YYYY
        summary: Brief description
        highlights:
          - Key feature or achievement
```

Save as `resume_data.yaml` and show to user for confirmation.

**Ask user:** "I've structured your resume data. Please review and let me know if anything needs adjustment."

## Phase 2: Style Selection

### Step 2.1: Ask Style Preference

Ask (header: "Style"):
How do you want to choose your resume style?
- "Show me previews (Recommended)" — Generate 5 visual previews
- "Pick from list" — Choose from preset themes directly

**If direct selection:** Show available themes and skip to Phase 3.

Available themes:
- **Classic** — Centered header with blue accents, stable and versatile
- **ModernCV** — Left-aligned header with side date column
- **Sb2nov** — Academic serif typography style
- **Engineering Classic** — Light blue engineering aesthetic
- **Engineering Resumes** — Black and white compact single-page layout

### Step 2.2: Generate Style Previews

Generate 5 HTML previews using the bundled renderer and the user's real data.

Save to `.claude-design/cv-previews/`:
- `style-classic.html`
- `style-moderncv.html`
- `style-sb2nov.html`
- `style-engineeringclassic.html`
- `style-engineeringresumes.html`

Open each preview automatically.

### Step 2.3: User Selection

Ask (header: "Theme"):
Which style do you prefer?
- Classic
- ModernCV
- Sb2nov
- Engineering Classic
- Engineering Resumes
- Mix elements

If "Mix elements", ask for specifics.

## Phase 3: Generate Full Resume

Generate complete HTML resume using:
- Structured YAML data from Phase 1
- Selected style from Phase 2

Prefer the bundled renderer over hand-writing HTML:

```bash
python3 scripts/render_html.py resume_data.yaml resume.html classic
```

Supported renderer themes:
- `classic`
- `modern`
- `sb2nov`
- `engineeringclassic`
- `engineeringresumes`

**Before generating, read:**
- [references/theme-presets.md](references/theme-presets.md) — Theme characteristics and when to use each
- [references/html-template.md](references/html-template.md) — Shared HTML shell and section structure

The bundled renderer already inlines print-safe CSS.

**Key requirements:**
- Single self-contained HTML file
- Use the bundled renderer's inline CSS output as the source of truth
- Add `@media print` rules for clean PDF export
- Use web fonts (Google Fonts/Fontshare)
- Inline editing support (optional, ask user)
- Detailed comments for each section

**Print optimization:**
- Page breaks: `page-break-inside: avoid` for sections
- Colors: Ensure readability in B&W
- Margins: Standard print margins (0.5-0.75in)
- Font sizes: 10-12pt body, appropriate hierarchy

## Phase 4: PDF Export

After generating HTML:

1. **Open in browser**: `open resume.html`
2. **Instruct user**:
   - Press Cmd+P (Mac) or Ctrl+P (Windows)
   - Select "Save as PDF"
   - Adjust margins if needed (usually "Default" works)
   - Save

Alternative: Provide Python script for automated PDF generation (requires weasyprint or playwright).

## Phase 5: Delivery

1. **Clean up** — Delete `.claude-design/cv-previews/` if exists
2. **Open** — Launch HTML in browser
3. **Summarize**:
   - File location and theme name
   - How to export PDF (Cmd+P → Save as PDF)
   - How to edit: If editing enabled, click any text to edit, Ctrl+S to save
   - Customization: CSS variables in `:root` for colors/spacing

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [references/html-template.md](references/html-template.md) | Shared HTML shell and theme structure | Phase 3 (generation) |
| [references/theme-presets.md](references/theme-presets.md) | Five theme specifications | Phase 2 (style selection) |
| [scripts/extract_resume.py](scripts/extract_resume.py) | Document extraction script | Phase 1 (extraction) |
| [scripts/render_html.py](scripts/render_html.py) | Main renderer for all five themes | Phase 2-4 |

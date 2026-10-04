---
name: pdf-artisan
description: Guides agents and sub-agents to generate
---
# PDF Artisan Protocol

You are operating under the **PDF Artisan** protocol. As an agent or sub-agent, you generate publication-grade, beautifully designed PDF documents that strictly adhere to user requirements with zero content omission or unwanted deviations.

---

## 1. The 4 Non-Negotiable Standards of PDF Creation

### Standard 1: Zero Deviation & Zero Omission
- **Exact Content Fidelity**: If the user provides specific items, figures, table columns, or text:
  - Include every single data point provided.
  - Do NOT invent filler text, unrequested sections, or imaginary testimonials.
  - Preserve exact names, dates, amounts, and currencies.
- **Structural Integrity**: Follow the requested hierarchy (Title -> Executive Summary -> Details -> Breakdown -> Footer).

### Standard 2: Multilingual & Arabic RTL Perfection
- When generating documents in Arabic or bilingual (Arabic/English):
  - **Text Direction**: Always set `direction: rtl; text-align: right;` for Arabic containers.
  - **Letter Shaping**: In Python-based generators (ReportLab), always process Arabic strings with `arabic_reshaper` and `python-bidi.algorithm.get_display` to prevent disconnected or backwards letters.
  - **Typography**: Use clean, legible Arabic typefaces (e.g. Cairo, Amiri, Tajawal, Arial).

### Standard 3: Print-Ready Visual Hierarchy
- **Margins & Spacing**: Standard A4 page margins (15mm - 20mm).
- **Page Break Control**: Avoid awkward splits across pages. Use `break-inside: avoid;` or `page-break-inside: avoid;` on table rows, cards, and signature blocks.
- **Running Headers & Footers**: Include document title in header and `Page X of Y` in footer.
- **Table Polish**: Alternating row backgrounds (zebra striping), clear header contrast, and numerical column alignment (right-aligned for numbers).

### Standard 4: Automated Generation via `generate_pdf.py`
Use the provided script to generate PDFs reliably:
```powershell
python C:/Users/goldl/.gemini/config/skills/pdf-artisan/scripts/generate_pdf.py --html "<PATH_TO_HTML>" --output "<OUTPUT_PDF>"
```
Or for programmatic ReportLab generation:
```powershell
python C:/Users/goldl/.gemini/config/skills/pdf-artisan/scripts/generate_pdf.py --report --title "طھظ‚ط±ظٹط± ط§ظ„ظ…ط´ط±ظˆط¹" --output "<OUTPUT_PDF>"
```

---

## 2. Recommended Workflow
1. **Gather Requirements**: Review all fields, tables, and branding requested by user.
2. **Select Template**: Pick an appropriate base from [pdf_design_templates.md](./references/pdf_design_templates.md).
3. **Draft HTML/CSS**: Fill with user content, verifying all Arabic text has RTL attributes.
4. **Compile & Verify**: Run `generate_pdf.py` and inspect the output.

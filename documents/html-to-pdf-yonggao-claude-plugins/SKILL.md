---
name: html-to-pdf
description: Converts HTML files to PDF or PNG format. Use this skill when the user asks to convert, export, or generate PDF/PNG from HTML files, or when they want to create printable documents, presentations, or long-form images from web pages or HTML reports.
---

# HTML to PDF/PNG Converter Skill

This skill helps you convert HTML files to PDF or PNG format with various options for output quality and page layout.

## When to Use This Skill

Use this skill when the user wants to:
- Convert HTML files to PDF
- Generate PNG screenshots from HTML
- Create printable documents from web pages
- Export HTML reports as PDFs
- Generate long-form images without page breaks
- Create presentation-ready PDFs from HTML

## Available Conversion Methods

### Method 1: Multi-Page PDF (Standard A4)
Best for: Printing, archiving, traditional documents

**Command:**
```bash
python html_to_pdf_final.py input.html output.pdf
```

**Features:**
- Standard A4 page format
- Zero margins for seamless appearance
- Background colors and gradients preserved
- Multiple pages with page breaks
- Optimized file size (~5-6 MB for typical reports)

### Method 2: Single-Page Long Image PDF
Best for: Online viewing, presentations, no page breaks

**Command:**
```bash
python html_to_long_image.py input.html
```

**Features:**
- Generates a full-page PNG screenshot first
- Converts PNG to single-page PDF
- NO page breaks - entire content on one page
- Perfect for presentations and online viewing
- Smaller file size (~1-2 MB)
- Two output files: `.png` and `.pdf`

### Method 3: Advanced Multi-Method Converter
Best for: Fallback options, compatibility

**Command:**
```bash
python html_to_pdf_converter.py input.html output.pdf
```

**Features:**
- Tries WeasyPrint first (best CSS support)
- Falls back to Playwright if needed
- Automatic dependency installation
- Handles complex CSS and gradients

## Required Dependencies

The skill requires Playwright and Pillow. The scripts auto-install dependencies if missing:

```bash
pip install playwright pillow pypdf
playwright install chromium
```

## Step-by-Step Instructions

### For Standard Multi-Page PDF:

1. **Verify the HTML file exists:**
   ```bash
   ls -la *.html
   ```

2. **Run the converter:**
   ```bash
   python html_to_pdf_final.py your_file.html
   ```

3. **Open the result:**
   ```bash
   open your_file_final.pdf
   ```

### For Single-Page Long Image PDF:

1. **Verify the HTML file exists:**
   ```bash
   ls -la *.html
   ```

2. **Run the long image converter:**
   ```bash
   python html_to_long_image.py your_file.html
   ```

3. **Check outputs:**
   ```bash
   # View the PNG screenshot
   open your_file_fullpage.png

   # View the PDF version
   open your_file_fullpage.pdf
   ```

## Troubleshooting

### Issue: Playwright browser not found

**Solution:**
```bash
playwright install chromium
```

### Issue: Page breaks visible in PDF

**Solution:** Use the long image method instead:
```bash
python html_to_long_image.py your_file.html
```

### Issue: Content appears cut off

**Causes & Solutions:**
- **CSS animations not complete**: Script waits 2 seconds for animations
- **Lazy loading**: Script scrolls through entire page to trigger loading
- **Large file size**: Scripts handle files up to 20MB+

### Issue: Blank PDF output

**Solution:** Use the long image method which uses screenshot instead of PDF rendering:
```bash
python html_to_long_image.py your_file.html
```

## Output Files

After conversion, you'll get:

**Multi-Page PDF:**
- `filename_final.pdf` - Standard A4 multi-page PDF

**Long Image Method:**
- `filename_fullpage.png` - Complete screenshot as PNG (6-10 MB)
- `filename_fullpage.pdf` - Single-page PDF from image (1-2 MB)

## Best Practices

1. **For online viewing/presentations:** Use `html_to_long_image.py`
   - No page breaks
   - Smooth scrolling experience
   - Smaller file size

2. **For printing/archiving:** Use `html_to_pdf_final.py`
   - Standard A4 pages
   - Better for physical printing
   - Professional document format

3. **For complex CSS:** Use `html_to_pdf_converter.py`
   - Multiple fallback methods
   - Better compatibility

## Implementation Notes

### Script Locations
All scripts should be in the project directory:
- `html_to_pdf_final.py` - Main multi-page converter
- `html_to_long_image.py` - Long image generator
- `html_to_pdf_converter.py` - Advanced multi-method converter

### Key Features Implemented

1. **Animation Handling**: All scripts disable CSS animations/transitions
2. **Lazy Loading**: Scripts scroll through content to trigger loading
3. **Background Preservation**: All gradients and colors render correctly
4. **Zero Margins**: Seamless page appearance without visible borders
5. **Chinese Font Support**: Handles CJK characters properly

## Examples

### Example 1: Convert BP Report to Multi-Page PDF
```bash
python html_to_pdf_final.py 202510_Alpha_Intelligence_BP.html
# Output: 202510_Alpha_Intelligence_BP_final.pdf (22 pages, 5.7 MB)
```

### Example 2: Create Single-Page Presentation PDF
```bash
python html_to_long_image.py 202510_Alpha_Intelligence_BP.html
# Output:
#   - 202510_Alpha_Intelligence_BP_fullpage.png (6.1 MB)
#   - 202510_Alpha_Intelligence_BP_fullpage.pdf (1.6 MB, 1 page)
```

### Example 3: Batch Convert Multiple Files
```bash
for file in *.html; do
    python html_to_long_image.py "$file"
done
```

## Advanced Usage

### Custom Output Paths
```bash
python html_to_pdf_final.py input.html custom_output.pdf
python html_to_long_image.py input.html
```

### Check PDF Page Count
```bash
python -c "from pypdf import PdfReader; r = PdfReader('output.pdf'); print(f'Pages: {len(r.pages)}')"
```

### Verify File Sizes
```bash
ls -lh *.pdf *.png
```

## Performance Expectations

- **Processing Speed**: ~5-10 seconds for typical HTML files
- **Memory Usage**: ~100-200 MB during conversion
- **PDF File Size**: 1-6 MB depending on method
- **PNG File Size**: 6-10 MB for full-page screenshots

## Success Criteria

A successful conversion should:
1. ✅ Generate PDF/PNG without errors
2. ✅ Include all HTML content (no truncation)
3. ✅ Preserve colors, gradients, and styling
4. ✅ Handle Chinese/CJK characters correctly
5. ✅ Create readable file sizes (< 10 MB)

## Quick Reference

| Need | Use | Output |
|------|-----|--------|
| Printing | `html_to_pdf_final.py` | Multi-page A4 PDF |
| Online viewing | `html_to_long_image.py` | Single-page PDF + PNG |
| Maximum compatibility | `html_to_pdf_converter.py` | Multi-page PDF with fallbacks |

---
name: claude-photo-manager
description: Handle photo uploads, analysis, and processing in Claude Code. This skill should be used when users want to upload images, analyze screenshots, process photos, or work with visual content in Claude Code conversations.
---

# Claude Photo Manager

This skill provides comprehensive photo and image handling capabilities for Claude Code, enabling users to upload, analyze, process, and manage visual content efficiently.

## When to Use This Skill

Use this skill when:
- User wants to upload photos/images for analysis
- Processing screenshots for debugging
- Analyzing UI mockups or designs
- Working with visual content for development
- Converting between image formats
- Extracting text from images (OCR)
- Comparing visual designs
- Documenting visual issues or bugs

## Supported Image Operations

### 1. Image Upload and Analysis
- Accept PNG, JPG, JPEG, GIF, WebP, BMP, TIFF formats
- Analyze screenshots for debugging purposes
- Examine UI mockups and designs
- Review code documentation images
- Process photographs with context

### 2. Image Processing and Enhancement
- Resize images for different use cases
- Optimize image file sizes
- Convert between image formats
- Apply filters and adjustments
- Crop and edit images programmatically

### 3. Visual Content Analysis
- Extract text from images (OCR)
- Identify UI components in screenshots
- Analyze color palettes and design elements
- Compare two images for differences
- Detect objects and features in photos

## Upload Methods

### Method 1: Direct Upload (Recommended)
```bash
# User can simply drag and drop or select image files
# Claude Code will automatically accept and analyze them
```

### Method 2: File Path Reference
```bash
# Reference local files for Claude to read
"Por favor analizá esta imagen: /path/to/image.png"
```

### Method 3: Base64 Encoding (for small images)
```bash
# Provide base64 encoded image data
"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
```

## Common Use Cases and Solutions

### Use Case 1: UI Bug Analysis
When users report visual bugs:

**Input:** Screenshots of the issue
**Analysis Steps:**
1. Identify UI components involved
2. Analyze layout and positioning
3. Check for visual inconsistencies
4. Suggest CSS/React Native fixes
5. Compare with expected design

**Example Response:**
"Analizando el screenshot que subiste, veo que hay un problema de alineación en el componente de tareas. El botón de eliminar está cortado y el texto no tiene suficiente espacio de padding. Te sugiero ajustar el CSS así:"

### Use Case 2: Design Review
When users want feedback on designs:

**Input:** Mockups, wireframes, or UI designs
**Analysis Steps:**
1. Evaluate visual hierarchy
2. Check spacing and proportions
3. Analyze color contrast and accessibility
4. Suggest improvements
5. Verify consistency with design system

### Use Case 3: Error Debugging
When users share error screenshots:

**Input:** Error messages, console logs, or crash reports
**Analysis Steps:**
1. Extract and transcribe error text
2. Identify error type and source
3. Search for related code issues
4. Provide specific fixes
5. Suggest debugging approaches

### Use Case 4: Code Documentation
When users share code screenshots:

**Input:** Code snippets, documentation images
**Analysis Steps:**
1. Transcribe text from images
2. Analyze code structure
3. Identify potential issues
4. Suggest improvements
5. Convert to editable text format

## Image Processing Scripts

### Image Optimization Script
```bash
# Optimize images for web use
python .claude/skills/claude-photo-manager/scripts/optimize_image.py input.jpg output.jpg --quality 80 --max-width 1200
```

### Screenshot Analyzer
```bash
# Analyze UI components in screenshots
python .claude/skills/claude-photo-manager/scripts/analyze_screenshot.py screenshot.png
```

### Image Format Converter
```bash
# Convert between image formats
python .claude/skills/claude-photo-manager/scripts/convert_image.py input.png output.webp
```

### OCR Text Extractor
```bash
# Extract text from images
python .claude/skills/claude-photo-manager/scripts/extract_text.py image.png --output extracted_text.txt
```

## Best Practices for Image Analysis

### For Screenshots:
1. **High Resolution:** Ensure screenshots are clear and readable
2. **Context Included:** Show enough surrounding context
3. **Multiple Views:** Include before/after when relevant
4. **Annotations:** Mark specific areas of concern if possible

### For Designs:
1. **Actual Size:** Use real dimensions when possible
2. **Multiple States:** Show different UI states (hover, active, disabled)
3. **Responsive Views:** Include mobile and desktop versions
4. **Color References:** Include hex codes or color values

### For Bug Reports:
1. **Reproduction Steps:** Include screenshots of each step
2. **Expected vs Actual:** Show both states
3. **Browser/Device Info:** Include environment details
4. **Console Errors:** Include relevant error messages

## Integration with Development Workflow

### STEEB App Integration:
When analyzing STEEB app images:
- Check for component consistency
- Verify dark/light mode compatibility
- Analyze task list performance
- Review social feed layouts
- Examine settings panel organization

### Code Review Integration:
When reviewing code-related images:
- Extract and format code snippets
- Check for syntax errors
- Suggest optimizations
- Verify coding standards compliance

### Documentation Enhancement:
When processing documentation images:
- Extract text for searchable content
- Convert diagrams to code equivalents
- Create markdown documentation
- Generate alt text for accessibility

## Error Handling and Troubleshooting

### Common Issues:
1. **File Size Too Large:** Compress or optimize images
2. **Unsupported Format:** Convert to supported format
3. **Corrupted Files:** Attempt repair or request new files
4. **Poor Quality:** Request higher resolution images
5. **Privacy Concerns:** Redact sensitive information

### Error Recovery:
```bash
# Validate image files
python .claude/skills/claude-photo-manager/scripts/validate_image.py image.png

# Attempt image repair
python .claude/skills/claude-photo-manager/scripts/repair_image.py corrupted_image.jpg
```

## Performance Considerations

### For Large Images:
- Implement progressive loading
- Use image compression
- Consider tiling for very large images
- Cache processed results

### For Batch Processing:
- Process images in parallel when possible
- Implement queuing for multiple uploads
- Use memory-efficient algorithms
- Provide progress feedback

## References and Resources

- Image format specifications and best practices
- Claude Code file upload limitations
- UI/UX design principles and guidelines
- Accessibility standards for visual content
- Privacy and security considerations for images

## Assets and Templates

### Analysis Templates:
- UI bug report template
- Design review checklist
- Error analysis framework
- Performance audit template

### Processing Tools:
- Image comparison utilities
- Color palette extractors
- Component detection scripts
- Text extraction tools
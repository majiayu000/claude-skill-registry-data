---
name: study-viewer
description: Converts the learning Markdown into a standalone, split-screen interactive HTML page. Left pane for EN/CN text, right pane for deep linguistic analysis.
---

# Study Viewer

Transforms structured Markdown into a modern dual-pane web interface.

## Core Workflow
1. **Parsing**: Read the `index.md` from `wiki/synthesis`.
2. **Structuring**: Use regex or a Markdown parser to separate content into Paragraphs and Analysis blocks.
3. **HTML Generation**: 
   - Inject the content into a pre-defined HTML/CSS template.
   - **Left Pane**: `<div class="content">` for original text and translation.
   - **Right Pane**: `<div class="analysis">` for the 6-point analysis.
4. **Persistence**: Save the output as `interactive.html` in the same directory as the source.

## Guidelines
- Use CSS Flexbox/Grid for the split-screen layout.
- Ensure the font and spacing are optimized for long-form reading.
- (Optional) Add simple JS to highlight matching blocks on hover.

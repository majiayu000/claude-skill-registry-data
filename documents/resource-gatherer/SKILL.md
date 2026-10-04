---
name: resource-gatherer
description: Handles comprehensive resource acquisition, categorization, and asset management. Adaptive to various sources (URLs, PDFs, local paths) and centralizes media in a lowercase 'assets' folder.
---

# Resource Gatherer

Focuses on the acquisition and organization of resources into a structured workspace.

## Core Workflow
1. **Adaptive Acquisition**: Select the best tool based on input type:
   - **Simple URL**: Use `tavily-extract` (basic).
   - **JS-Heavy/Dynamic URL**: Use `tavily-extract --extract-depth advanced` or `browser-use` skill.
   - **Documentation Set/Multiple URLs**: Use `tavily-crawl`.
   - **PDF (Local/URL)**: 
     - Use `run_shell_command` with tools like `pandoc` or `pdf2txt` to convert to Markdown.
     - For scanned PDFs, use OCR or multi-modal analysis.
   - **Local File**: Use `read_file`.
   - **Local Directory**: Use `glob` or `list_directory` to map the structure, then selectively read key files to build context.
2. **Categorization**: Infer a category (e.g., `AI`, `Tech`, `Business`) from the content.
... (rest of the steps)
   - Create `raw/article/[Category]/[Article_Title]/assets/`.
   - Ensure `assets` is lowercase.
4. **Asset Management**: 
   - Download all images/media to the `assets/` folder.
   - Update Markdown links in the raw content to `assets/filename`.
5. **Raw Storage**: Save the cleaned raw Markdown to `raw/article/[Category]/[Article_Title]/index.md`.

## Guidelines
- Centralize all assets in `raw`. NEVER duplicate assets in `synthesis` folders.
- Use the exact article title for directory and filename.

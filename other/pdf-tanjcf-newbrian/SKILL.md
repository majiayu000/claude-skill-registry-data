---
name: pdf
description: Read, create, inspect, render, and verify PDF files in the active NewBrain workspace.
---
# PDF

- Use a real CJK font for Chinese output and avoid unsupported glyphs.
- Verify the `%PDF-` signature, non-zero size, page count, and extracted text before reporting success.
- Render representative pages when layout matters; fix clipping, blank pages, missing glyphs, and broken links.
- Return the PDF itself as the primary artifact, not only its generator script.

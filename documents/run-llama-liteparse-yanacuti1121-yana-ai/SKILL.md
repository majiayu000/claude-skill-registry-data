---
name: run-llama--liteparse
description: "LiteParse — Rust document parser của LlamaIndex: PDF/Word/Excel/PPT/image → JSON với bounding boxes. Node.js/Python/WASM bindings. Tesseract OCR bundled, không cần cloud."
allowed-tools: Bash, Read, Write
user-invocable: true
---

LiteParse: fast local document parser viết bằng Rust — PDF + office docs + images → structured JSON với spatial bounding boxes. Zero cloud dependency.

## Install

```bash
# Node.js
npm install liteparse

# Python
pip install liteparse

# Rust
cargo add liteparse
```

## Supported Formats

```
Native:   PDF (trực tiếp, không convert)
Office:   .doc .docx .odt .ppt .pptx .odp .xls .xlsx .ods .csv .tsv
Images:   JPG PNG GIF BMP TIFF WebP SVG
          (qua ImageMagick → OCR)
```

## API

```typescript
import { parse } from 'liteparse'

// JSON với bounding boxes
const result = await parse('document.pdf', { format: 'json' })
// result.pages[0].blocks[0].bbox = { x, y, width, height }
// result.pages[0].blocks[0].text = "..."

// Plain text với layout preserved
const text = await parse('report.docx', { format: 'text' })

// Screenshot tại DPI tùy chỉnh
await parse('slide.pptx', { format: 'screenshot', dpi: 300 })
```

```python
from liteparse import parse

result = parse("document.pdf", format="json")
for page in result["pages"]:
    for block in page["blocks"]:
        print(block["text"], block["bbox"])
```

## Performance

```
Parallel OCR processing  — configurable worker threads
Selective OCR            — chỉ chạy khi cần (không phải mọi page)
Page-range targeting     — parse trang 10-20, skip phần còn lại
Default DPI: 150         — tùy chỉnh được
```

## OCR Options

```
Default: Tesseract (bundled, offline)
HTTP backends: EasyOCR, PaddleOCR (accuracy cao hơn)
Custom: implement theo API spec
```

## CLI

```bash
liteparse document.pdf --format json --pages 1-10 --output result.json
liteparse batch/ --format text --workers 4
```

## Khi nào dùng

- RAG pipeline: parse docs → chunk → embed
- Extract structured data từ PDF reports
- Convert office docs sang Markdown cho LLM context
- OCR images trong batch pipeline

## Source

https://github.com/run-llama/liteparse · Apache-2.0 · +1613⭐/week

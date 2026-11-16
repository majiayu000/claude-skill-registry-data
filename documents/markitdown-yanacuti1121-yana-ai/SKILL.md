---
name: markitdown
description: Convert mọi file (PDF, Word, Excel, PowerPoint, Image, Audio, HTML, CSV, YouTube URL) thành Markdown cho LLM. Tích hợp vào YAMTAM vault để import tài liệu.
triggers:
  - markitdown
  - convert file to markdown
  - pdf to markdown
  - word to markdown
  - import document
  - import pdf
  - đọc file pdf
  - convert tài liệu
  - vault import
  - đưa file vào vault
---

# markitdown — File → Markdown Converter

**Source**: github.com/microsoft/markitdown  
**Version**: 0.1.6 (installed)  
**License**: MIT · Built by Microsoft AutoGen team

## Supported formats

| Format | Notes |
|--------|-------|
| PDF | Text extraction |
| Word (.docx) | Full structure |
| PowerPoint (.pptx) | Slides → Markdown |
| Excel (.xlsx) | Tables |
| Image | EXIF + OCR (với LLM) |
| Audio | Transcription |
| HTML | Clean text |
| CSV / JSON / XML | Structured |
| YouTube URL | Transcript tự động |
| EPub | Chapters |

## Basic usage

```python
from markitdown import MarkItDown

md = MarkItDown()

# Convert file
result = md.convert("document.pdf")
print(result.text_content)

# Convert URL
result = md.convert("https://example.com")

# Convert YouTube → transcript
result = md.convert("https://youtube.com/watch?v=xxx")
```

## CLI

```bash
markitdown document.pdf > output.md
markitdown document.pdf -o output.md
markitdown https://example.com -o page.md
```

## Tích hợp YAMTAM vault

```bash
# Import PDF vào vault
python3 tools/vault-import.py document.pdf

# Import thư mục
python3 tools/vault-import.py --dir ./docs/ --ext pdf,docx

# Import + ghi vào knowledge base
python3 tools/vault-import.py report.pdf --tag bao-cao --lang vi
```

## Với LLM (AI-powered OCR cho ảnh scan)

```python
import anthropic
from markitdown import MarkItDown

client = anthropic.Anthropic()
md = MarkItDown(llm_client=client, llm_model="claude-haiku-4-5-20251001")

result = md.convert("scan_bai_thi.jpg")
print(result.text_content)
```

## Khi nào dùng trong YAMTAM

- Import sách giáo khoa tiếng Việt (PDF) → vault search
- Convert báo cáo Word/Excel → context cho Claude
- Đọc slide PowerPoint → summary tự động
- Transcribe YouTube tiếng Việt → text searchable
- Parse CSV lớn → Markdown table cho LLM
- Đọc tài liệu JNMT (Word, PDF) → AI context

---
name: markitdown
description: 輕量 Python 工具，將各種檔案格式（PDF、Word、PowerPoint、Excel、圖片、HTML、CSV、JSON、XML、ZIP、YouTube、EPub 等）轉換為 Markdown，適用於 LLM 文本分析與跨階段文件前處理。
version: 1.0.0
tags: [文件轉換, markdown, pdf, docx, pptx, xlsx, ocr, 文本分析]
trigger_phrases: [轉成 Markdown, 轉換文件為 Markdown, markitdown, 文件轉 Markdown]
---

# markitdown - 跨格式文件轉 Markdown

## 用途
Microsoft MarkItDown 是一個輕量 Python 工具，專門將各種檔案格式轉換為結構化 Markdown，適用於：
- LLM 文本分析前處理
- 需求文件結構化
- 測試報告格式轉換
- 維運文件匯入
- 跨階段文件整合

## 支援格式
PDF、PowerPoint、Word、Excel、圖片（EXIF + OCR）、Audio（EXIF + 語音轉錄）、HTML、CSV、JSON、XML、ZIP、YouTube URL、EPub。

## 安裝
```bash
pip install markitdown[all]
```

## 使用方式
### 命令列
```bash
markitdown path-to-file.pdf > document.md
markitdown path-to-file.pdf -o document.md
```

### Python API
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("example.pdf")
print(result.text_content)
```

### Optional Dependencies
```bash
pip install markitdown[pdf, docx, pptx]
```

## 與 SSDLC 階段的應用
- **Phase 01（需求分析）**：將 PDF/Word 需求文件轉為 Markdown 進行結構化
- **Phase 04（測試驗證）**：將測試報告（PDF/Excel）轉為 Markdown 分析
- **Phase 06（維護營運）**：將日誌文件、維運手冊轉為 Markdown 整合

## 來源
- GitHub：https://github.com/microsoft/markitdown
- 授權：MIT
- 本機外部資源：external-resources/markitdown/

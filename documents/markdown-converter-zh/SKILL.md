---
name: markdown-converter-zh
description: 使用 markitdown 将文档和文件转换为 Markdown 格式。支持转换 PDF、Word (.docx)、PowerPoint (.pptx)、Excel (.xlsx, .xls)、HTML、CSV、JSON、XML、图片（带 EXIF/OCR）、音频（带转录）、ZIP 压缩包、YouTube 链接或电子书到 Markdown 格式，用于 LLM 处理或文本分析。
---

# Markdown 转换器

使用 markitdown 工具将各种文档格式转换为 Markdown。非常适合为 LLM 处理或文本分析准备内容。

## 设置

安装 markitdown（Python 包）：

```bash
pip install markitdown
```

## 使用方法

### 基本转换

```bash
./convert.js /path/to/document.pdf
./convert.js /path/to/document.docx
./convert.js /path/to/spreadsheet.xlsx
./convert.js /path/to/presentation.pptx
```

### 支持的格式

- **文档：** PDF (.pdf), Word (.docx), RTF (.rtf)
- **电子表格：** Excel (.xlsx, .xls), CSV (.csv)
- **演示文稿：** PowerPoint (.pptx)
- **网页：** HTML (.html, .htm), URL 链接
- **数据：** JSON (.json), XML (.xml)
- **图片：** PNG, JPG 等（带 EXIF 元数据和 OCR）
- **音频：** MP3, WAV 等（带转录）
- **压缩包：** ZIP (.zip) - 解压并转换内容
- **电子书：** EPUB (.epub)
- **视频链接：** YouTube 链接（提取字幕）

### 选项

```bash
./convert.js --help
```

## 示例

```bash
# 将 PDF 转换为 Markdown
./convert.js report.pdf

# 转换 Word 文档
./convert.js contract.docx

# 转换网页
./convert.js https://example.com/article

# 转换 YouTube 视频（提取字幕）
./convert.js https://youtube.com/watch?v=VIDEO_ID

# 转换 Excel 电子表格
./convert.js data.xlsx
```

## 使用场景

- 为 LLM 分析准备文档
- 将旧格式文档转换为现代格式
- 使用 OCR 从图片中提取文本
- 转录音频文件
- 将网页转换为 Markdown
- 处理 YouTube 视频字幕
- 批量转换多种文件类型

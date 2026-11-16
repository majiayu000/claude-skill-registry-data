---
name: paddlepaddle--paddleocr
description: "PaddleOCR — OCR toolkit 80+ ngôn ngữ: PP-OCR (general), PP-Structure (layout+table), PP-ChatOCR (LLM key extraction). PDF/image → text/structured data. Apache-2.0."
allowed-tools: Bash, Read, Write
user-invocable: true
---

PaddleOCR: multilingual OCR toolkit của Baidu — text detection + recognition + document structure analysis + LLM-powered key info extraction.

## Install

```bash
pip install paddlepaddle   # CPU
# pip install paddlepaddle-gpu  # GPU
pip install paddleocr
```

## 3 Solutions

```
PP-OCR          — general text detection + recognition
PP-Structure    — document layout analysis + table recognition
PP-ChatOCR      — key info extraction với LLM (hỏi đáp về document)
```

## Basic Usage

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')  # hoặc 'ch', 'fr', 'de'...
result = ocr.ocr('document.jpg', cls=True)

for line in result[0]:
    bbox, (text, confidence) = line
    print(f"{text} ({confidence:.2f})")
```

## Document Structure

```python
from paddleocr import PPStructure

engine = PPStructure(table=True, ocr=True)
result = engine('report.pdf')

for item in result:
    print(item['type'])  # 'text', 'title', 'table', 'figure'
    if item['type'] == 'table':
        print(item['res']['html'])  # table → HTML
```

## Language Support

80+ ngôn ngữ: Chinese, English, French, German, Japanese, Korean, Arabic, Hindi, Vietnamese...

## Performance

```
PP-OCRv4:     Chinese accuracy +4.5% vs v3 | English +10%
PP-StructureV2: Layout 11x faster | model 95% smaller | table +6% accuracy
```

## Extra Tools

```
PPOCRLabel  — semi-automatic annotation tool
Style-Text  — synthetic training data generator
Mobile demo — iOS/Android via EasyEdge
Industrial  — 9 vertical models: digital displays, license plates, handwriting
```

## Khi nào dùng

- Extract text từ scanned PDFs, receipts, invoices
- Structured extraction: tables từ financial reports
- Multilingual docs với mix ngôn ngữ
- Thay thế cloud OCR (Google Vision, AWS Textract) — chạy offline

## Source

https://github.com/PaddlePaddle/PaddleOCR · Apache-2.0 · +747⭐/week

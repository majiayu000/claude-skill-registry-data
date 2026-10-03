---
name: pdf
description: "Read, create, edit, split, merge, rotate, watermark, fill, encrypt/decrypt, OCR, or extract text/tables/images from PDF files; use whenever .pdf is mentioned or requested."
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see forms.md) | See forms.md |
| **Markdown → 출판품질 PDF** | **scripts/markdown_to_pdf.py** | **아래 섹션 참조** |

---

## Markdown → 출판품질 PDF (한국 기본값)

`scripts/markdown_to_pdf.py`는 playwright(Chromium) 기반 마크다운 → 출판품질 PDF 변환기입니다.
한국 환경에 맞게 A4/25mm 마진/Pretendard 폰트를 기본으로 사용합니다.

### 한국 기본값

| 항목 | 기본값 | 비고 |
|------|--------|------|
| 페이지 | A4 (210×297mm) | 한국/유럽 표준 |
| 마진 | 25mm | 한국 출판 표준 |
| 본문 폰트 | Pretendard → Noto Sans KR → 시스템 sans | 자동 다운로드 (SIL OFL 1.1) |
| 코드 폰트 | D2Coding → JetBrains Mono → monospace | 자동 다운로드 (SIL OFL 1.1) |
| 페이지번호 | 하단 중앙 "N / M" | |
| 날짜 형식 | YYYY년 M월 D일 | |
| 외부 이미지 fetch | 허용 (networkidle까지 대기) | Chromium이 외부 리소스를 로드 — 트래커 차단 아님 |

### 사용법

```bash
# 80% 케이스 — 무플래그
python skills/pdf/scripts/markdown_to_pdf.py generate spec.md
# → spec.pdf 생성, stdout에 경로 한 줄

# 출력 경로 지정
python ... markdown_to_pdf.py generate spec.md docs/spec.pdf

# 표지 + TOC 포함 (출판 모드)
python ... markdown_to_pdf.py generate \
  --cover --toc \
  --title "프로젝트 명세서" \
  --author "팀 이름" \
  --org "회사명" \
  spec.md

# 워터마크 (한글/영문 모두 지원)
python ... markdown_to_pdf.py generate --watermark "초안" memo.md
python ... markdown_to_pdf.py generate --watermark "DRAFT" memo.md
python ... markdown_to_pdf.py generate --watermark "대외비" memo.md

# 프리뷰 (HTML 렌더 후 브라우저 자동 오픈, PDF 라운드트립 회피)
python ... markdown_to_pdf.py preview spec.md

# 폰트 미리 다운로드 + 의존성 점검
python ... markdown_to_pdf.py setup
```

### 페이지 구성 옵션 (현재 CLI의 질문 방식 권장)

마크다운을 PDF로 만들 때, 다음을 사용자에게 물어보고 적용하세요:

**Q1: 표지 페이지를 추가할까요?**
- A) 추가 (외부 공유용) → `--cover --title "..." --author "..."`
- B) 추가 안 함 (내부 메모) → 옵션 없음

**Q2: 목차(TOC)를 포함할까요?**
- A) 포함 (10페이지 이상이면 추천) → `--toc`
- B) 포함 안 함 (짧은 문서)

**Q3: 워터마크가 필요한가요?**
- A) DRAFT/초안 (작업 중) → `--watermark "초안"`
- B) 대외비/CONFIDENTIAL → `--watermark "대외비" --confidential`
- C) 없음 (최종본)

**Q4: H1마다 새 페이지로 시작?**
- A) 예 (장 단위 문서) → 기본값 (옵션 불필요)
- B) 아니오 (메모/단편) → `--no-chapter-breaks`

### 옵션 레퍼런스

| 옵션 | 설명 |
|------|------|
| `--title TEXT` | 문서 제목 (생략 시 첫 H1) |
| `--subtitle TEXT` | 부제 |
| `--author TEXT` | 저자 (표지 표기) |
| `--org TEXT` | 조직/팀명 (표지 표기) |
| `--date TEXT` | 날짜 (생략 시 오늘, 한국식) |
| `--cover` | 표지 페이지 추가 |
| `--toc` | 목차 추가 |
| `--watermark TEXT` | 대각선 워터마크 |
| `--confidential` | 좌측하단 CONFIDENTIAL 푸터 (페이지번호는 우측) |
| `--no-chapter-breaks` | H1마다 페이지 분할 안 함 |
| `--skip-fonts` | 폰트 자동 다운로드 건너뜀 |
| `--quiet` | 진행상황 출력 끔 |

### Output Contract

스크립트 자동화/체이닝을 위한 명확한 출력 규약:

```
stdout: <output-path>           ← 한 줄, 경로만 (성공 시)
stderr: 진행상황 메시지         ← --quiet로 끔
exit:
  0 = 성공
  1 = 인자 오류 (입력파일 없음/.md 아님)
  2 = 렌더링 실패
  3 = 의존성 누락 (playwright/markdown 미설치)
  4 = 네트워크 실패 (정의됨, 현재 미사용 — 폰트 다운로드 실패는 fallback 처리)
```

캡처 예시:
```bash
PDF=$(python markdown_to_pdf.py generate spec.md 2>/dev/null) && open "$PDF"
```

### 의존성 설치

```bash
pip install playwright markdown pygments
playwright install chromium     # 첫 실행 시 1회만
```

**왜 playwright?** 우리 `/minos` 스킬이 이미 playwright + Chromium을 사용하므로
의존성이 중복되지 않습니다. Windows/Mac/Linux 모두 동일한 렌더링 결과를 보장하고,
GTK 같은 시스템 라이브러리 의존성이 없습니다.

**셋업 한 방에:**
```bash
python skills/pdf/scripts/markdown_to_pdf.py setup
# → 의존성 점검 + Chromium 다운로드 + 한글 폰트 다운로드
```

폰트는 첫 실행 시 `~/.cache/agent-customizations/fonts/`에 자동 다운로드됩니다 (SIL OFL 1.1 라이선스).
오프라인 환경이면 `--skip-fonts`로 시스템 폰트만 사용 가능합니다.

### Clio 통합

`/clio` 스킬의 Phase 3에서 산출물(PRD/TECHNICAL/USER-MANUAL)을 PDF로 자동 출력할 때 사용됩니다. Clio가 호출하는 명령:

```bash
# USER-MANUAL은 표지 + TOC 포함 (외부 공유 빈도 높음)
python markdown_to_pdf.py generate \
  --cover --toc \
  --title "{프로젝트명} 사용자 매뉴얼" \
  USER-MANUAL.md

# PRD/TECHNICAL은 TOC만 (내부 문서)
python markdown_to_pdf.py generate --toc PRD.md
python markdown_to_pdf.py generate --toc TECHNICAL.md
```

## Next Steps

- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md
- **Markdown → 출판 PDF**: 위 섹션 참조 (한국 기본값: A4 + Pretendard)

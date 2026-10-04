---
name: report-analyzer
description: "Analyze large PDF or PPTX reports (consulting, research, market analysis) and produce a structured summary with key data, insights, and section overview. Trigger this skill when the user mentions: 'analyze report', 'report summary', 'report analysis', 'key takeaways from report', 'break down the report', 'what's in the report', 'summarize the report', 'проанализируй отчёт', 'разбери отчёт', 'summary отчёта', 'ключевые выводы из отчёта', 'что в отчёте', 'краткое содержание отчёта'. Also trigger when a user uploads a PDF or PPTX file and asks to summarize, extract insights, or review it — even if they don't use the exact phrases above. If a large document is uploaded with any request related to understanding its contents, use this skill."
version: 1.0.0
---

# Report Analyzer

Analyzes large reports (PDF, PPTX) and produces a structured summary with key data and insights.

Target audience: product managers, marketers, analysts, finance professionals, C-level executives.

---

## Language Detection

Detect the language from the user's message. Use that language for all output — the summary document, clarifying questions, and responses. If the user writes in Russian, respond and generate the output in Russian. If in English — in English.

---

## Input

- A PDF or PPTX report file
- The user specifies the file name or path in their message, or uploads the file directly

---

## Output

A structured summary document (up to 1.5 pages) containing:
- Report metadata
- Executive Summary
- Key figures and data
- Key insights
- Report structure

---

## Instructions

### Step 1 — Locate the input file

The user specifies the report file name in their message. Locate the file using this order:

1. Check the current working directory and subdirectories (e.g. `input/` folder or project root)
2. If the user provided a full path — use it directly

**File search:**
```bash
find . -iname "*.pdf" -o -iname "*.pptx" 2>/dev/null
```

**If the file is not found** — ask the user:
> "Please specify the exact file name or path to the report, or upload the file directly. Supported formats: PDF, PPTX."

**If the format is not supported:**
> "This skill works with PDF and PPTX files. Please provide a file in one of these formats."

---

### Step 2 — Ask clarifying questions

Ask the user the following questions before proceeding:

**Question 1:** "What is the analysis focus?"
- General overview
- Numbers and data
- Strategic takeaways
- Everything combined

**Question 2:** "What output file format do you prefer?"
- .md
- .pdf
- .docx

Do not create the output file until both questions are answered.

---

### Step 3 — Read and process the file

**For PDF:**
```python
import pdfplumber

with pdfplumber.open("path/to/file.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
        # Extract tables
        tables = page.extract_tables()
```

Also extract metadata:
```python
from pypdf import PdfReader
reader = PdfReader("path/to/file.pdf")
meta = reader.metadata
pages_count = len(reader.pages)
```

**For PPTX:**
```bash
python -m markitdown presentation.pptx
```

If text extraction fails (scanned PDF) — use OCR:
```python
import pytesseract
from pdf2image import convert_from_path
images = convert_from_path('file.pdf')
for image in images:
    text += pytesseract.image_to_string(image)
```

---

### Step 4 — Perform analysis

Based on the extracted text, generate content according to the structure below.

**Analysis rules:**
- Extract only facts and data from the report — do not infer or fabricate
- All numbers must be exact — as in the original
- Formulate insights in the third person ("the authors note", "the report indicates")
- If data is contradictory — flag it explicitly
- Output document must not exceed 1.5 pages

**How to identify insights (selection criteria):**

An insight is a statement from the report that meets at least one criterion:

1. **Non-obvious** — the finding contradicts conventional wisdom or expectations ("contrary to popular belief...", "unexpectedly...")
2. **Quantitative shift** — a sharp change in a metric (growth/decline >20%, trend reversal, record)
3. **Causal relationship** — the report explicitly links cause and effect ("X led to Y", "the main driver is Z")
4. **Forecast or warning** — authors make a prediction or flag a risk with specific parameters
5. **Actionability** — a finding that enables a management decision (not just a description of the situation)

**How to formulate an insight:**
- One sentence, two at most
- Lead with the substance, not the context
- Include specific numbers where available
- Bad: "The AI market is growing" → Good: "The GenAI market grew 68% YoY to $127B, outpacing analyst forecasts by 15 p.p."

**Number of insights:** 5–7. If the report contains fewer significant findings — do not pad to 5 artificially.

**Adaptation by focus:**
- **General overview** — balanced across all sections
- **Numbers and data** — expanded data table, condensed insights
- **Strategic takeaways** — expanded insights, condensed data table
- **Everything combined** — all sections in full (within the 1.5-page limit)

---

### Step 5 — Generate the output file

Use the structure from the "Output Format" section below.

**By format:**
- `.md` — write the file directly
- `.pdf` — first generate `.md`, then use the pdf skill if available
- `.docx` — first generate `.md`, then use the docx skill if available

**File naming:**
`report-summary_REPORT-NAME_YYYY-MM-DD.extension`

Example: `report-summary_mckinsey-ai-trends_2026-03-18.md`

Save the file in the project output folder or current working directory. Deliver the file to the user.

---

## Output Format

```markdown
# Report Summary: [Report Title]

**Analysis date:** [date]

---

## Report metadata

| Parameter | Value |
|-----------|-------|
| Title | [full title] |
| Author / source | [company or author] |
| Publication date | [date or year] |
| Length | [page count] |
| Original language | [language] |
| Type | [consulting / research / analytics / market review / other] |

---

## Executive Summary

[3–5 sentences: core thesis of the report, main argument, key conclusion]

---

## Key figures and data

| Metric / indicator | Value | Context |
|--------------------|-------|---------|
| [metric 1] | [value] | [explanation] |
| [metric 2] | [value] | [explanation] |
| ... | ... | ... |

---

## Key insights

1. [insight 1]
2. [insight 2]
3. [insight 3]
4. [insight 4]
5. [insight 5]

---

## Report structure

| Section | Summary |
|---------|---------|
| [Section 1] | [1–2 sentences] |
| [Section 2] | [1–2 sentences] |
| ... | ... |
```

---

## Negative Cases

- Do not add personal assessments or recommendations — only report content
- Do not exceed 1.5 pages in the output document
- Do not use filler phrases ("Sure, here's the analysis...")
- Do not retell the entire report — highlight what matters
- Do not round or alter numbers from the original
- Do not create the file until both clarifying questions are answered

---

## Dependencies

```bash
pip install pdfplumber pypdf markitdown --break-system-packages
```

For PPTX:
```bash
pip install "markitdown[pptx]" --break-system-packages
```

For OCR (scanned PDFs):
```bash
pip install pytesseract pdf2image --break-system-packages
```

---
name: pdf
description: Create PDF files — text documents (Vietnamese OK), chart pages, merging PDFs. Use when the user asks for a PDF or a downloadable .pdf file.
license: Same as the Scarlet repository
metadata:
  default_enabled: "true"
  display_name: PDF
---

# pdf — PDF files

Written by Scarlet for its sandbox. Available: `pypdf` (read, merge, split,
rotate, metadata) and `matplotlib` (draws new pages). **Not** available:
reportlab, LibreOffice, pandoc, Poppler, `pip install`, network.

## How to make a file

Call `run_code` with `skill="pdf"`. The helper `make_pdf.py` sits next to
your code:

```python
import matplotlib.pyplot as plt
from make_pdf import text_pdf

fig = plt.figure(figsize=(8.27, 11.69))
plt.bar(["T1", "T2", "T3"], [4, 7, 5])
plt.title("Số đơn hàng")

text_pdf("bao-cao.pdf", "Báo cáo tháng 10", [
    "Đoạn thứ nhất, viết thành câu đầy đủ. Dòng dài tự xuống hàng, hết trang tự sang trang.",
    "Đoạn thứ hai.",
], figures=[fig])
print("ok")
```

- `text_pdf(path, title, paragraphs, figures=())`: A4, title in bold, plain
  paragraphs (no bold/italic/tables inside the text), then one page per
  matplotlib figure. Text is real text (searchable, copyable).
- A table: draw it on a figure with `plt.table(...)` (turn the axes off) and
  pass the figure in `figures`.
- `merge_pdfs(path, inputs)`: join PDFs you wrote earlier in the same run.
  Name the parts with a leading dot (`.part1.pdf`) so only the result is sent.
- Other page work with `pypdf`: `PdfReader("x.pdf")`, `PdfWriter()`,
  `page.rotate(90)`, `writer.add_metadata({...})`, `writer.write(...)`.

If the user needs a richly formatted document (styles, tables in text),
suggest the `docx` skill instead — Word can save it as PDF.

## Rules

- Save with a **relative** file name (current folder). Every file left there
  is sent to the user as a download — write exactly one `.pdf`.
- The user's uploaded files are **not** in the sandbox — you cannot open a
  PDF the user attached; build from the conversation text.
- A traceback in `stderr` means fix the code and call `run_code` again.
- After success, tell the user the file is ready to download in the panel.

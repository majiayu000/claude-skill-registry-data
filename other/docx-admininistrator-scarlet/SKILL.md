---
name: docx
description: Create Word documents (.docx) — reports, letters, headings, lists, tables, images. Use when the user asks for a Word file or a downloadable .docx.
license: Same as the Scarlet repository
metadata:
  default_enabled: "true"
  display_name: Word (.docx)
---

# docx — Word documents

Written by Scarlet for its sandbox. Only `python-docx` (plus `pillow`,
`matplotlib` for images) is available — no LibreOffice, no pandoc, no
`pip install`, no network.

## How to make a file

Call `run_code` with `skill="docx"`. The helper `make_docx.py` sits next to
your code, so import it:

```python
from make_docx import build_docx

build_docx("leave-request.docx", [
    {"type": "heading", "text": "Thông tin", "level": 1},
    {"type": "paragraph", "text": "Kính gửi Trưởng phòng ..."},
    {"type": "bullets", "items": ["Ngày nghỉ: 12/10", "Lý do: việc gia đình"]},
    {"type": "table", "rows": [["Hạng mục", "Số tiền"], ["Đi lại", 120000]]},
], title="Đơn xin nghỉ phép")
print("ok")
```

Block types:

| `type` | Keys | Notes |
|---|---|---|
| `heading` | `text`, `level` (1–9, default 1) | `title=` adds a level-0 Title on top |
| `paragraph` | `text` | plain text, Vietnamese is fine |
| `bullets` / `numbered` | `items` (list of str) | |
| `table` | `rows` (list of lists) | first row is the header (bold), grid style |
| `image` | `path`, `width_in` (default 6) | a PNG/JPEG you wrote in the same run |
| `page_break` | — | |

Need something the helper does not cover (fonts, alignment, headers,
footers)? Use `python-docx` directly — `document = Document()`, `document.add_...`,
`document.save("name.docx")`.

## Rules

- Save with a **relative** file name (current folder). Every file you leave
  there is sent to the user as a download — so write exactly one `.docx`.
- Intermediate files (a chart PNG for an `image` block) must start with a dot,
  e.g. `.chart.png`; dot-files are not sent.
  For a chart: `import matplotlib; matplotlib.use("Agg")`, then
  `plt.savefig(".chart.png", dpi=150)`.
- The user's uploaded files are **not** in the sandbox — build from the
  conversation text.
- A traceback in `stderr` means fix the code and call `run_code` again.
- After success, tell the user the file is ready to download in the panel;
  do not paste the file content back.

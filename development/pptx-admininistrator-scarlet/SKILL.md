---
name: pptx
description: Create PowerPoint decks (.pptx) — title slides, bullet slides, charts and images, speaker notes. Use when the user asks for slides, a presentation or a .pptx file.
license: Same as the Scarlet repository
metadata:
  default_enabled: "true"
  display_name: PowerPoint (.pptx)
---

# pptx — PowerPoint decks

Written by Scarlet for its sandbox. `python-pptx`, `pillow` and `matplotlib`
are available — no LibreOffice, no Node, no `pip install`, no network.

## How to make a file

Call `run_code` with `skill="pptx"`. The helper `make_pptx.py` sits next to
your code:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from make_pptx import build_pptx

plt.bar(["Q1", "Q2", "Q3"], [12, 18, 25])
plt.title("Doanh thu (tỷ đồng)")
plt.savefig(".revenue.png", dpi=150, bbox_inches="tight")

build_pptx("ke-hoach.pptx", [
    {"title": "Kế hoạch quý 4", "subtitle": "Phòng Kinh doanh"},
    {"title": "Mục tiêu", "bullets": ["Tăng doanh thu 20%", ["Kênh online", 1], "Giữ chân khách cũ"],
     "notes": "Nhấn mạnh kênh online."},
    {"title": "Doanh thu theo quý", "image": ".revenue.png"},
])
print("ok")
```

Slide dict:

| Keys | Slide |
|---|---|
| `title`, `subtitle` | title slide (no `bullets` / `image`) |
| `title`, `bullets` | bullet slide; a bullet is `"text"` or `["text", level]`, level 0–4 |
| `title`, `image` | picture fitted under the title (PNG/JPEG written in the same run) |
| `notes` (any slide) | speaker notes |

Keep it to 3–6 bullets per slide, short phrases, one idea per slide. Slides
are 4:3 with the plain default theme. For anything else (shapes, tables,
colours) use `python-pptx` directly: `Presentation()`, `prs.slides.add_slide(...)`,
`prs.save("name.pptx")`.

## Rules

- Save with a **relative** file name (current folder). Every file left there
  is sent to the user as a download — write exactly one `.pptx`; chart images
  must start with a dot (`.revenue.png`) so they are not sent.
- The user's uploaded files are **not** in the sandbox — build from the
  conversation text.
- A traceback in `stderr` means fix the code and call `run_code` again.
- After success, tell the user the file is ready to download in the panel.

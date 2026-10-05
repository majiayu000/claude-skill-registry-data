---
name: pdf
slug: pdf-generator
version: 1.1.0
displayName: PDF 生成器（PDF Generator）
summary: "基于 token 设计系统的高品质 PDF 生成技能，支持从零创建（15 种文档类型 + 封面）、填写表单字段、重排现有文档三大场景，自动适配 CJK 中文字体。v1.1.0 新增 Windows 跨平台支持（run_pipeline.py）。来源：github.com/MiniMaxAI，作者：MiniMaxAI，许可证：MIT。"
tags: pdf, document-generation, reportlab, cover-page, form-fill, reformat, cjk
description: "Use this skill when visual quality and design identity matter for a PDF. CREATE: make a PDF, generate a report, write a proposal, create a resume. FILL: fill in the form, fill out this PDF. REFORMAT: reformat this document, apply our style, convert Markdown/text to PDF. Triggers: PDF, pdf, 生成PDF, PDF报告, 简历, 提案, 排版."
license: MIT
metadata:
  category: document-generation
  author: MiniMaxAI
---

## 输出规则（必读）

- **只保存到本地**：所有生成或编辑的文件保存到用户指定路径或当前工作目录，操作完成后告知用户完整的文件路径。
- **禁止向对话发送文件内容**：不要将文件内容（文本、二进制、base64 等任何形式）粘贴或发送到用户的聊天/会话中。大文件会导致整个 session 卡死。
- **如需预览**：只在对话中展示简短的摘要信息（如文档标题、页数等元信息），不要展示完整内容。

## 工具调用纪律

- **禁止读取源代码文件**（`.py` / `.js` / `.sh`）。所有操作通过 Quick Start 命令完成。
- **禁止手动编辑中间文件**（`tokens.json`、XML 等）。如需自定义参数，使用 CLI 的 `--flag`。
- **命令失败时**：只看错误信息的最后几行，不要去读源码调试。常见错误见下方 Troubleshooting。
- **reference 文件**：`design/design.md` 仅在需要自定义设计风格（字体、颜色、布局）时阅读，常规使用无需阅读。
- **依赖安装**：只运行一次环境准备脚本，不要手动重复 `pip install` 或 `npx playwright install`。
- **Windows 注意**：使用 `python`（不是 `python3`），使用 `python scripts/run_pipeline.py` 代替 `bash scripts/make.sh run`。

## 环境准备（首次使用 **必须自动执行**，无需询问用户）

读完本 SKILL.md 后，立即静默运行依赖安装脚本。**不要问用户是否需要安装。**

```bash
# macOS / Linux / WSL
bash scripts/make.sh fix

# Windows（PowerShell）
powershell -ExecutionPolicy Bypass -File scripts/setup_deps.ps1
```

无需单独运行 `check`，也无需手动 `pip install` 或 `npm install`。脚本已包含全部依赖的检测与安装。

**平台检测：** 如果 `bash` 命令不可用（Windows CMD），改用 `python scripts/run_pipeline.py`（见 Quick Start）。Windows 上 Python 命令是 `python`（不是 `python3`）。

# minimax-pdf

Three tasks. One skill.

## Quick Start

**创建 PDF：**
```bash
# macOS / Linux / WSL
bash scripts/make.sh run \
  --title "Report Title" --type report \
  --author "Author" --accent "#2D5F8A" \
  --content content.json --out report.pdf

# Windows（CMD 或 PowerShell）
python scripts/run_pipeline.py --title "Report Title" --type report --author "Author" --accent "#2D5F8A" --content content.json --out report.pdf
```

**填写 PDF 表单：**
```bash
# macOS / Linux
python3 scripts/fill_inspect.py --input form.pdf
python3 scripts/fill_write.py --input form.pdf --out filled.pdf \
  --values '{"Name": "张三", "Date": "2025-04"}'

# Windows
python scripts/fill_inspect.py --input form.pdf
python scripts/fill_write.py --input form.pdf --out filled.pdf --values "{\"Name\": \"张三\", \"Date\": \"2025-04\"}"
```

**重排现有文档：**
```bash
# macOS / Linux
bash scripts/make.sh reformat \
  --input source.md --title "标题" --type report --out output.pdf

# Windows — 先用 reformat_parse.py 提取内容，再走 run_pipeline.py
python scripts/reformat_parse.py --input source.md --out content.json
python scripts/run_pipeline.py --title "标题" --type report --content content.json --out output.pdf
```

**文档类型速查：** `report` · `proposal` · `resume` · `portfolio` · `academic` · `general` · `minimal` · `stripe` · `diagonal` · `frame` · `editorial` · `magazine` · `darkroom` · `terminal` · `poster`

**CJK 中文支持：** 自动检测。当 content.json 包含中文/日文/韩文时，自动注册系统 CJK 字体并切换为左对齐排版。无需手动配置字体路径。

---

## Route table

| User intent | Route | Scripts used |
|---|---|---|
| Generate a new PDF from scratch | **CREATE** | `palette.py` → `cover.py` → `render_cover.js` → `render_body.py` → `merge.py` |
| Fill / complete form fields in an existing PDF | **FILL** | `fill_inspect.py` → `fill_write.py` |
| Reformat / re-style an existing document | **REFORMAT** | `reformat_parse.py` → then full CREATE pipeline |

**Rule:** when in doubt between CREATE and REFORMAT, ask whether the user has an existing document to start from. If yes → REFORMAT. If no → CREATE.

---

## Route A: CREATE

Full pipeline — content → design tokens → cover → body → merged PDF.

```bash
# macOS / Linux / WSL
bash scripts/make.sh run \
  --title "Q3 Strategy Review" --type proposal \
  --author "Strategy Team" --date "October 2025" \
  --accent "#2D5F8A" \
  --content content.json --out report.pdf

# Windows
python scripts/run_pipeline.py --title "Q3 Strategy Review" --type proposal --author "Strategy Team" --date "October 2025" --accent "#2D5F8A" --content content.json --out report.pdf
```

**Doc types:** `report` · `proposal` · `resume` · `portfolio` · `academic` · `general` · `minimal` · `stripe` · `diagonal` · `frame` · `editorial` · `magazine` · `darkroom` · `terminal` · `poster`

| Type | Cover pattern | Visual identity |
|---|---|---|
| `report` | `fullbleed` | Dark bg, dot grid, Playfair Display |
| `proposal` | `split` | Left panel + right geometric, Syne |
| `resume` | `typographic` | Oversized first-word, DM Serif Display |
| `portfolio` | `atmospheric` | Near-black, radial glow, Fraunces |
| `academic` | `typographic` | Light bg, classical serif, EB Garamond |
| `general` | `fullbleed` | Dark slate, Outfit |
| `minimal` | `minimal` | White + single 8px accent bar, Cormorant Garamond |
| `stripe` | `stripe` | 3 bold horizontal color bands, Barlow Condensed |
| `diagonal` | `diagonal` | SVG angled cut, dark/light halves, Montserrat |
| `frame` | `frame` | Inset border, corner ornaments, Cormorant |
| `editorial` | `editorial` | Ghost letter, all-caps title, Bebas Neue |
| `magazine` | `magazine` | Warm cream bg, centered stack, hero image, Playfair Display |
| `darkroom` | `darkroom` | Navy bg, centered stack, grayscale image, Playfair Display |
| `terminal` | `terminal` | Near-black, grid lines, monospace, neon green |
| `poster` | `poster` | White bg, thick sidebar, oversized title, Barlow Condensed |

Cover extras (inject into tokens via `--abstract`, `--cover-image`):
- `--abstract "text"` — abstract text block on the cover (magazine/darkroom)
- `--cover-image "url"` — hero image URL/path (magazine, darkroom, poster)

**Color overrides — always choose these based on document content:**
- `--accent "#HEX"` — override the accent color; `accent_lt` is auto-derived by lightening toward white
- `--cover-bg "#HEX"` — override the cover background color

**Accent color selection guidance:**

You have creative authority over the accent color. Pick it from the document's semantic context — title, industry, purpose, audience — not from generic "safe" choices. The accent appears on section rules, callout bars, table headers, and the cover: it carries the document's visual identity.

| Context | Suggested accent range |
|---|---|
| Legal / compliance / finance | Deep navy `#1C3A5E`, charcoal `#2E3440`, slate `#3D4C5E` |
| Healthcare / medical | Teal-green `#2A6B5A`, cool green `#3A7D6A` |
| Technology / engineering | Steel blue `#2D5F8A`, indigo `#3D4F8A` |
| Environmental / sustainability | Forest `#2E5E3A`, olive `#4A5E2A` |
| Creative / arts / culture | Burgundy `#6B2A35`, plum `#5A2A6B`, terracotta `#8A3A2A` |
| Academic / research | Deep teal `#2A5A6B`, library blue `#2A4A6B` |
| Corporate / neutral | Slate `#3D4A5A`, graphite `#444C56` |
| Luxury / premium | Warm black `#1A1208`, deep bronze `#4A3820` |

**Rule:** choose a color that a thoughtful designer would select for this specific document — not the type's default. Muted, desaturated tones work best; avoid vivid primaries. When in doubt, go darker and more neutral.

**content.json 格式：** 必须是 JSON **数组**（`[...]`），每个元素是一个 block 对象。不要写成单个对象 `{}`。示例：`[{"type":"h1","text":"标题"}, {"type":"body","text":"正文段落"}]`

**content.json block types:**

| Block | Usage | Key fields |
|---|---|---|
| `h1` | Section heading + accent rule | `text` |
| `h2` | Subsection heading | `text` |
| `h3` | Sub-subsection (bold) | `text` |
| `body` | Justified paragraph; supports `<b>` `<i>` markup | `text` |
| `bullet` | Unordered list item (• prefix) | `text` |
| `numbered` | Ordered list item — counter auto-resets on non-numbered blocks | `text` |
| `callout` | Highlighted insight box with accent left bar | `text` |
| `table` | Data table — accent header, alternating row tints | `headers`, `rows`, `col_widths`?, `caption`? |
| `image` | Embedded image scaled to column width | `path`/`src`, `caption`? |
| `figure` | Image with auto-numbered "Figure N:" caption | `path`/`src`, `caption`? |
| `code` | Monospace code block with accent left border | `text`, `language`? |
| `math` | Display math — LaTeX syntax via matplotlib mathtext | `text`, `label`?, `caption`? |
| `chart` | Bar / line / pie chart rendered with matplotlib | `chart_type`, `labels`, `datasets`, `title`?, `x_label`?, `y_label`?, `caption`?, `figure`? |
| `flowchart` | Process diagram with nodes + edges via matplotlib | `nodes`, `edges`, `caption`?, `figure`? |
| `bibliography` | Numbered reference list with hanging indent | `items` [{id, text}], `title`? |
| `divider` | Accent-colored full-width rule | — |
| `caption` | Small muted label | `text` |
| `pagebreak` | Force a new page | — |
| `spacer` | Vertical whitespace | `pt` (default 12) |

**chart / flowchart schemas:**
```json
{"type":"chart","chart_type":"bar","labels":["Q1","Q2","Q3","Q4"],
 "datasets":[{"label":"Revenue","values":[120,145,132,178]}],"caption":"Q results"}

{"type":"flowchart",
 "nodes":[{"id":"s","label":"Start","shape":"oval"},
          {"id":"p","label":"Process","shape":"rect"},
          {"id":"d","label":"Valid?","shape":"diamond"},
          {"id":"e","label":"End","shape":"oval"}],
 "edges":[{"from":"s","to":"p"},{"from":"p","to":"d"},
          {"from":"d","to":"e","label":"Yes"},{"from":"d","to":"p","label":"No"}]}

{"type":"bibliography","items":[
  {"id":"1","text":"Author (Year). Title. Publisher."}]}
```

---

## Route B: FILL

Fill form fields in an existing PDF without altering layout or design.

```bash
# Step 1: inspect (macOS: python3, Windows: python)
python3 scripts/fill_inspect.py --input form.pdf

# Step 2: fill
python3 scripts/fill_write.py --input form.pdf --out filled.pdf \
  --values '{"FirstName": "Jane", "Agree": "true", "Country": "US"}'
```

**Windows 用户：** 将上方 `python3` 替换为 `python`。

| Field type | Value format |
|---|---|
| `text` | Any string |
| `checkbox` | `"true"` or `"false"` |
| `dropdown` | Must match a choice value from inspect output |
| `radio` | Must match a radio value (often starts with `/`) |

Always run `fill_inspect.py` first to get exact field names.

---

## Route C: REFORMAT

Parse an existing document → content.json → CREATE pipeline.

```bash
# macOS / Linux / WSL
bash scripts/make.sh reformat \
  --input source.md --title "My Report" --type report --out output.pdf

# Windows — 分两步
python scripts/reformat_parse.py --input source.md --out content.json
python scripts/run_pipeline.py --title "My Report" --type report --content content.json --out output.pdf
```

**Supported input formats:** `.md` `.txt` `.pdf` `.json`

---

## Environment

```bash
# macOS / Linux
bash scripts/make.sh check   # verify all deps
bash scripts/make.sh fix     # auto-install missing deps

# Windows
powershell -ExecutionPolicy Bypass -File scripts/setup_deps.ps1
```

| Tool | Used by | Install |
|---|---|---|
| Python 3.9+ | all `.py` scripts | system（Windows 上命令为 `python`） |
| `reportlab` | `render_body.py` | `pip install reportlab` |
| `pypdf` | fill, merge, reformat | `pip install pypdf` |
| Node.js 18+ | `render_cover.js` | system |
| `playwright` + Chromium | `render_cover.js` | `npm install -g playwright && npx playwright install chromium` |

---

## Troubleshooting

| 问题 | 原因 | 修复 |
|---|---|---|
| 中文/日文/韩文显示为方块或乱码 | CJK 字体自动检测已内置，如仍出现说明系统无可用 CJK 字体 | macOS 通常自带 STHeiti，无需操作；Linux 运行 `apt install fonts-noto-cjk` |
| `TypeError: unsupported operand type(s) for \|` | Python 版本低于 3.9 | 升级 Python 至 3.9+；脚本已含 `from __future__ import annotations` 兼容 |
| Playwright / Chromium 报错 | Chromium 浏览器未安装 | 运行 `npx playwright install chromium`（环境准备脚本已包含） |
| content.json 格式错误 | content.json 不是 JSON 数组 | 确保文件是 `[{...}, {...}]` 数组格式，不是 `{...}` 对象 |
| 封面页空白 | Node.js 或 Playwright 未就绪 | 重新运行环境准备脚本 |
| Windows 上 `bash` 不可用 | Windows 没有 bash | 使用 `python scripts/run_pipeline.py` 代替 `bash scripts/make.sh run` |
| Windows 上 `python3` 不可用 | Windows Python 命令是 `python` | 将所有 `python3` 替换为 `python` |
| `/tmp/` 路径不存在 (Windows) | Windows 无 Unix 临时目录 | `run_pipeline.py` 自动使用系统临时目录，无需手动指定 |

---
name: markdown-nine-grid-clipboard
description: Convert Chinese or mixed-language text, iMandalArt cards, Obsidian 九宮, 表格, Mandala notes, or eight-domain outlines into a Markdown 3x3 nine-grid table with an ◎ center, then copy, save, append, or hand it to apps that render Markdown tables such as Obsidian and AIDA. Use when the user asks for Markdown 九宮格, Obsidian 九宮, Markdown table 九宮, 曼陀羅表格, nine-grid clipboard, AIDA table output, or conversion between Markdown 九宮, iMandalArt, and 81-grid workflows.
---

# Markdown Nine Grid Clipboard

## Purpose

Create a copyable Markdown 3x3 nine-grid table for apps that render Markdown tables.

Markdown 九宮 is:

- A real Markdown table.
- Nine cells only.
- A compact center plus eight surrounding fields.
- Good for Obsidian, AIDA, GitHub, ChatGPT, Hermes notes, and app handoff.

It is not:

- iMandalArt phone text art.
- A PE2 fixed-width card.
- A visual 81-cell Mandala chart.

## Nine-Grid Family

Keep these formats connected but distinct:

| Format | Role | Use |
|---|---|---|
| Markdown 九宮 | structured Markdown table | Obsidian/AIDA/table apps |
| iMandalArt | square phone-readable card | Hermes/Discord visual card |
| 81 宮 | 9x9 expansion | full Mandala expansion |

Markdown 九宮 can take an existing iMandalArt with eight fields and turn it into a table. It can also become the first-layer input for iMandalArt or 81 宮 expansion.

## Cell Rules

1. Create exactly nine cells.
2. The center cell must contain `◎`.
3. Use the center as an integrated summary, not a copied title.
4. Preserve this spatial order:
   - top-left, top-center, top-right
   - middle-left, center, middle-right
   - bottom-left, bottom-center, bottom-right
5. If a cell is six Chinese characters or fewer, keep it on one line.
6. If a cell is longer than six Chinese characters, split it into two lines with `<br>`.
7. When the source already has title and content, format the cell as `title<br>content`.
8. Do not create extra Markdown rows for title/content. The table still has exactly three visual rows and nine cells.

Example:

```markdown
| 權威訊號<br>原詞命名者 | 時代轉折<br>語言正換代 | 代理工程<br>新主戰場起 |
|---|---|---|
| 創業痛點<br>更快做產品 | ◎交付新核心 | 示範能力<br>測修再部署 |
| 一人公司<br>能力被放大 | 工具名稱冷<br>流程才主角 | 交付風險<br>驗收更重要 |
```

## Workflow

1. Read the user's source text or table-like card.
2. Detect whether the source is already a 3x3 iMandalArt, an eight-domain outline, or raw prose.
3. Extract eight surrounding fields and one center summary.
4. Add `◎` to the center if the source center lacks it.
5. Compress each cell:
   - `<= 6` Chinese characters: one line.
   - `> 6` Chinese characters: title/content or two-line split.
6. Render as a Markdown table.
7. Use `scripts/copy_grid.py` to validate, format, copy, and optionally save/append the table.
8. If the user asks to send to Obsidian, AIDA, or another Markdown-rendering app:
   - Prefer an available MCP connector for that app.
   - Otherwise use a CLI or file path the user has already provided.
   - If no app route is available, copy to clipboard and show the table.

## Script

Run from the skill directory:

```bash
python3 scripts/copy_grid.py --cells cells.json
```

Useful options:

```bash
python3 scripts/copy_grid.py --cells cells.json --out grid.md --no-copy
python3 scripts/copy_grid.py --cells cells.json --append-to ObsidianNote.md --target obsidian
python3 scripts/copy_grid.py --cells cells.json --target aida
```

`cells.json` accepts either strings or title/content objects:

```json
{
  "top_left": {"title": "權威訊號", "content": "原詞命名者"},
  "top_center": "時代轉折換代",
  "top_right": "代理工程主場",
  "middle_left": "創業痛點加速",
  "center": "交付成新核心",
  "middle_right": {"title": "示範能力", "content": "測修再部署"},
  "bottom_left": "一人公司放大",
  "bottom_center": "工具名稱冷流程主角",
  "bottom_right": "交付風險驗收更要"
}
```

The script:

- Requires all nine cells.
- Adds `◎` to the center when missing.
- Splits long string cells into Markdown `<br>` lines.
- Prints the Markdown table.
- Copies to macOS clipboard unless `--no-copy` is set.
- Writes or appends to Markdown files when `--out` or `--append-to` is provided.

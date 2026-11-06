---
name: presentations
description: Create, edit, inspect, and verify PPTX/HTML presentation files with charts, stage diagrams, and showcase images.
---
# Presentations

- Prefer `artifact.create` with `format: "pptx"` or `format: "html"`. PPTX also writes a companion `*.slides.html` for browser presentation.
- Build decks like a designed webpage, not a Word outline: dark title/closing, varied layouts, one idea per slide, generous hierarchy.
- **Every deck must include visuals**, not text-only slides:
  - **≥1 chart slide** (`layout: "chart"`) with real numbers from the source document
  - **≥1 stage/process slide** (`layout: "timeline"` or `"process"`) for milestones, rollout, or workflow
  - **≥1 image/showcase slide** (`layout: "image"`) — call `image_generate` first when helpful, then pass `imagePath`
- Pass structured `slides` with optional `layout`: `title` | `section` | `bullets` | `columns` | `cards` | `stat` | `chart` | `timeline` | `process` | `image` | `closing`.
- Keep bullets ≤ 5 per slide; never dump long paragraphs. Split dense content across more slides.
- Use CJK-safe fonts (Microsoft YaHei). Theme is ink + teal — do not invent purple/gray Office defaults.
- Reopen/inspect the file before claiming success. For HTML decks, tell the user they can open the `.html` / `.slides.html` to present with arrow keys.

## Chart slide (统计图)

```json
{
  "title": "市场规模趋势",
  "layout": "chart",
  "body": "数据来源：行业报告 2024",
  "chart": {
    "type": "bar",
    "categories": ["2022", "2023", "2024"],
    "values": [120, 180, 240],
    "seriesName": "销量（万辆）"
  }
}
```

Supported chart types: `bar`, `line`, `pie`, `doughnut`, `area`. Extract categories and values from tables or prose in the source — do not invent numbers.

## Stage / process slide (阶段图)

```json
{
  "title": "实施路径",
  "layout": "timeline",
  "phases": [
    { "label": "P1", "title": "调研摸底", "body": "现状与痛点梳理" },
    { "label": "P2", "title": "试点验证", "body": "2-3 个场景上线" },
    { "label": "P3", "title": "全面推广", "body": "标准化复制" }
  ]
}
```

Use `layout: "process"` as an alias for `timeline`.

## Image / showcase slide (展示图)

1. When a visual helps (产品图、场景图、封面图), call `image_generate` with a concrete prompt.
2. Pass the downloaded workspace path as `imagePath` (e.g. `.newbrain/generated-media/image/xxx.png`).
3. If generation is skipped, still add an image slide with `imagePlaceholder` describing the intended visual.

```json
{
  "title": "产品场景示意",
  "layout": "image",
  "imagePath": ".newbrain/generated-media/image/scene.png",
  "caption": "智慧园区巡检场景"
}
```

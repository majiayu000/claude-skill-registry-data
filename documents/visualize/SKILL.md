---
name: visualize
description: |
  End-user visualization — diagrams (Mermaid mindmaps/flowcharts/sequence/ER),
  LaTeX math in chat or UI cards, and Chart.js HTML charts/dashboards from CSV/Excel/JSON.
  Use when the user wants to visualize, draw a diagram, mind map, flowchart, plot data,
  chart a spreadsheet, or explain with equations.
  Triggers on: "시각화", "다이어그램", "마인드맵", "flowchart", "mermaid", "차트 만들어줘",
  "plot this", "dashboard from CSV", "수식 그려줘", "visualize this".
  Not for document editing (docx/pptx) or raw format conversion (to-md).
---

# Visualize

One skill for **showing** things. Prefer in-chat/UI renderers for diagrams and math; use bundled scripts only for **tabular → HTML charts**.

## Choose a path

| Need | Path | Detail |
| --- | --- | --- |
| Mindmap, flowchart, sequence, ER, state | **Chat / UI markdown** | `` ```mermaid `` fence. See [diagrams.md](references/diagrams.md). |
| Equations | **Chat / UI markdown** | `$inline$` / `$$display$$` (KaTeX). See [diagrams.md](references/diagrams.md). |
| Diagram + user input | **`ui__presentInteractive`** | `format: "markdown"` (or `auto`) + `interaction`. |
| Final report with visuals | **`ui__reportResult`** | Same Mermaid/LaTeX fences in markdown. |
| Charts/dashboards from **tabular** data | **This skill’s scripts** | CSV/Excel/JSON → HTML. See [charts.md](references/charts.md). |
| Custom interactive HTML widget | **`ui__presentInteractive` `format: "html"`** | Only when markdown Mermaid/charts cannot express it. |

LibrAgent already renders Mermaid and LaTeX in chat, `ui__reportResult`, `ui__presentInteractive` (markdown), and PDF export — do not invent a separate renderer.

## Default workflow

1. **Classify** with the table. Mixed asks (architecture + sales CSV) → Mermaid in chat **and** chart HTML via [charts.md](references/charts.md).
2. **Diagrams/math** → emit complete fences in the reply (finish the closing ``` before relying on render). Load [diagrams.md](references/diagrams.md) for examples.
3. **Tabular charts** → read [charts.md](references/charts.md), then run `scripts/visualize.py` (inspect → chart/dashboard).
4. **Avoid** fetching CDN Mermaid in ad-hoc HTML for simple diagrams, dumping Mermaid as ` ```text `, or opening a browser solely to view a diagram that already renders in chat.

## Not this skill

| Skill | Use for |
| --- | --- |
| **to-md** | Extract text from PDF/XLSX without charting |
| **docx** / **pptx** | Author formatted documents |
| **deep-research** | Narrative research reports |
| **workspace-indexer** | Batch markdown index for a repo |

## References

- [diagrams.md](references/diagrams.md) — Mermaid & LaTeX in chat/UI
- [charts.md](references/charts.md) — tabular → Chart.js HTML
- [charts-request-patterns.md](references/charts-request-patterns.md)
- [charts-dashboard-spec.md](references/charts-dashboard-spec.md)
- [charts-output-format.md](references/charts-output-format.md)
- [charts-error-handling.md](references/charts-error-handling.md)

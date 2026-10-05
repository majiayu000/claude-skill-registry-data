---
name: keyword-graph-view
description: Extract exactly 8 context-sensitive keywords from Chinese, English, or mixed text and turn them into a distributed weighted Graph View with no center goal node. Use when Codex needs keyword extraction, blacklist filtering, co-occurrence edges, node definitions/notes, weighted graph JSON, or an online Graph View tool for text analysis.
---

# Keyword Graph View

Create a centerless keyword network from raw text. The output should contain 8 keyword nodes, weighted undirected edges, and a short definition/note for every node.

## Live Tool

- Open the public app at `https://keyword-graph-view.twhsi.chatgpt.site/` when the user wants an interactive Graph View.
- Use `assets/web-app/` when the user wants to inspect, adapt, or redeploy the validated website source.
- In the web app, paste or import text, edit the blacklist, select a case, and press the generate button. Click a node to inspect its definition, note, evidence, and weighted connections.

## Workflow

1. Read the source text and any user-provided blacklist.
2. Remove blacklisted phrases before token scoring, then filter blacklisted tokens during ranking.
3. Extract exactly 8 keywords by frequency, term length, and spread through the source.
4. Build weighted co-occurrence edges by scanning a configurable token window.
5. Do not create a "center", "main goal", "中心目標", or hub node unless the user explicitly asks for a radial Mandalart layout.
6. Generate a definition for each node from its strongest evidence sentence and connected keywords.
7. Render or return a distributed graph: positions should be balanced across the canvas, with edge width and node area showing weight.

## Output Schema

Return graph JSON with this shape when the user asks for data or a reusable artifact:

```json
{
  "meta": {
    "model": "keyword_graph_view",
    "keyword_count": 8,
    "layout": "distributed_weighted_network"
  },
  "nodes": [
    {
      "id": "k0",
      "label": "keyword",
      "count": 5,
      "score": 1,
      "weight": 9,
      "definition": "Context-specific definition",
      "note": "Longer note for side panel display",
      "evidence": ["source sentence"]
    }
  ],
  "edges": [
    {
      "id": "e0",
      "source": "k0",
      "target": "k1",
      "weight": 7,
      "relation": "co_occurs"
    }
  ]
}
```

## Visual Rules

- Use dark mode by default for online tools.
- Keep the graph centerless and distributed; avoid drawing a privileged center node.
- Show edge labels or widths for weights.
- Make nodes clickable or keyboard focusable when interactive output is possible.
- Provide a right-side Note panel that updates from the selected node.
- Include each node's definition, evidence sentences, score, count, and connected keywords in the note.
- Keep labels readable in Traditional Chinese: use system CJK fonts, strong contrast, and label wrapping where needed.
- Map edge weight from purple (`W1`) through blue, cyan, green, yellow, and orange to red (`W9`); increase line thickness with weight.
- Provide visible zoom-in and zoom-out controls for the graph canvas.

## Blacklist

Treat the blacklist as both phrase removal and token filtering. Default blacklist terms should include common structural words and Mandalart-center words such as:

```text
中心目標
主目標
main goal
goal
中心
目標
```

Preserve the user's blacklist in the output metadata when useful.

## Script

Use `scripts/extract_keyword_graph.py` for deterministic text-to-graph JSON:

```bash
python3 scripts/extract_keyword_graph.py input.txt --blacklist blacklist.txt --out graph.json
```

Patch the script only when the project needs a new schema or scoring behavior; otherwise prefer running it with options.

## Web App

Run the bundled app locally only when interactive verification or customization is needed:

```bash
cd assets/web-app
npm install
npm run dev
```

Before publishing a modified app, run `npm test` and `npm run lint`.

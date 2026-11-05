---
name: slides
description: Build a self-contained HTML presentation from a simple JSON outline — arrow-key navigation, gradient theme, no dependencies, opens in any browser.
---

# slides

Create a polished, standalone presentation as a single `.html` file. Navigate with
the arrow keys or space; it needs no PowerPoint and no internet.

## How to run

1. First write the outline as JSON into the out-box with the `Write` tool
   (e.g. `deck.json`):

```json
{
  "title": "Q3 Review",
  "subtitle": "Optional subtitle",
  "slides": [
    { "title": "Agenda", "bullets": ["Wins", "Numbers", "Next steps"] },
    { "title": "One big idea", "text": "A single centered statement." }
  ]
}
```

2. Then build the deck:

```
python3 <skill_dir>/run.py <spec.json> <output.html>
```

- `<spec.json>` — the JSON outline you just wrote (in the out-box).
- `<output.html>` — a path **inside the out-box**.

Standard library only. After running, tell the user the saved path and that they
can open it in a browser and present with the arrow keys.

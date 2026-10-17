---
name: flow
description: Draw a flow diagram (what talks to what) or a sequence diagram (who calls whom, in what order, who waits). A chat diagram of about 12 boxes or fewer is drawn by hand and checked with fd --lint; a larger one, or one that also needs a picture page or walkthrough, is written in Mermaid and rendered as Unicode box art (fd) or a clean/sketch-style picture page (pic). Use when a reply needs a diagram bigger than a few boxes, when the user asks for a flow or sequence diagram, or before building a narrated walkthrough (diagrams:walkthrough reads the same Mermaid).
---

# Flow and sequence diagrams

## First: count the boxes

| Diagram | Make it by |
|---|---|
| About 12 boxes or fewer, for chat only | **drawing it by hand**, then `fd --lint` ([By hand, then lint](#by-hand-then-lint)) |
| Larger, or it also needs a picture page or a walkthrough | Mermaid, then `fd` or `pic` |

Decide this before you write any Mermaid. A hand layout of a small diagram is shorter and clearer: 5 boxes drawn by hand fit in 11 rows, and the same 5 boxes from `fd` take 31.

## Mermaid: one source, three outputs

One Mermaid source, three outputs. The `diagrams:walkthrough` skill is the top layer and reads the same Mermaid.

```
Mermaid ─┬─► fd file.mmd ─────────► Unicode text in a ```text fence (chat)
         ├─► pic file.mmd ────────► picture page: clean (default) or sketch
         └─► walkthrough skill ──► picture + voice, cues, quiz
```

## Pick the diagram type by the question

| The reader asks | Draw | Mermaid header |
|---|---|---|
| What are the parts, and what flows between them? | flow | `graph LR` (a chain) or `graph TD` (a tree) |
| In what order do calls happen? Who waits for whom? When does the reply go back? | sequence | `sequenceDiagram` |
| Both (a new system, an incident) | flow first, then the sequence of the one path that matters | both |

A sequence shows what a flow hides. Example: at checkout the shop tells the customer "processing" *before* the payment provider confirms; the confirmation arrives later by webhook. A flow diagram cannot show that ordering.

## 1. Chat text (works everywhere)

Two ways to make it. Both end in a ```` ```text ```` fence.

| Diagram | Make it by | Why |
|---|---|---|
| About 12 boxes or fewer, chat only | **drawing it by hand**, then `fd --lint` | Hand layout reads better: tight groups, labels on arrows, a legend row |
| Also needs a picture page or a walkthrough, or is larger | Mermaid, then `fd` | One source for every output, alignment is exact |

### By hand, then lint

Draw with box-drawing characters: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`, dotted `┄ ┆` for async, rounded `╭ ╮ ╰ ╯` for storage, arrowheads `▶ ◀ ▲ ▼` (sync) and `▷ ◁ △ ▽` (async). Lay it out across and down: put a group frame around parallel boxes, label arrows next to the line, and add one `Legend:` row for the line styles. Then check it:

```bash
"${CLAUDE_SKILL_DIR}/fd" --lint diagram.txt     # or pipe the text in: ... | fd --lint -
```

- The check finds lines that are one column off, junctions with nothing under them, arrowheads that stop short of a box, and anything over 90 columns or 45 rows. Each problem has its row and column. Fix every one, then lint again. Paste only a diagram that passes.
- Rows that start with `Legend` or `Key` are not checked, because their sample arrows touch nothing.
- A line that touches a box edge or crosses another line without a junction is allowed. A line next to a junction whose arm points at empty space is reported as misplaced.

### From Mermaid

```bash
"${CLAUDE_SKILL_DIR}/fd" diagram.mmd
```

- Paste stdout into a ```` ```text ```` fence. It is plain Unicode, so it reads the same in the terminal and in the desktop app. Never paste raw Mermaid into chat: neither surface renders it.
- stderr reports the size (`fd: 43 cols x 37 rows`) and notes. Keep chat text within 90 columns and about 45 rows. If a note says it is too big, shorten labels, split the diagram, or make a picture instead.
- Use `graph LR` for a chain of calls: it reads left to right, like the request, and stays short. Use `graph TD` for a tree or a wide fan-out. `fd` switches an `LR` flow to `TD` by itself when it is wider than 90 columns or its lines fail the check.
- In a sequence, write branches as a `Note over X: ...`. `alt`/`opt`/`loop` blocks render badly as text, and `fd` warns about them.
- Chat text is single-colour by nature. Shapes carry meaning: `[( )]` store (rounded), `{ }` decision (◇), `-.->` async (dotted).
- `fd file --ascii` gives plain + - | > for limited terminals. `fd file --json` prints the parsed diagram.

#### Bigger Mermaid flows that spread across and down

`graph LR` with a fan-in and a fan-out still fits chat when it stays under 90 columns. The layout follows the order of the arrows, so write the source with care:

- Write the main path's arrows first. The first arrow out of a node stays on the main row; later arrows branch down. (`orders --> pay` before `orders --> db` keeps the payment path straight.)
- Put the parallel ends of a fan-in or fan-out in a `subgraph` (`Clients`, `Workers`). The group frame keeps their arrows apart.
- Lint the output too (`fd diagram.mmd | fd --lint -`): the renderer can put a line one column off. Read every arrow before you paste it. If two arrows share a line segment (a `┴` or `┬` where they join), a reader cannot tell which box an arrow comes from. Reorder the arrows or add a subgraph until each arrow has its own path.

## 2. Picture page (clean or sketch)

```bash
"${CLAUDE_SKILL_DIR}/pic" diagram.mmd --look look.json --title "Checkout" -o out.html
```

- **Clean is the default**: crisp lines and one text weight, with colour for emphasis. Use it for anything read for its values: real runs, comparisons, dense diagrams. `--theme sketch` gives hand-drawn boxes and arrows (rough.js) on graph paper, with the Architects Daughter font, for an early design that should look like a draft.
- Colour means the same in both themes. The fill says who runs a box; the outline and labels stay dark ink so text always wins.
- Arrows are routed by libavoid. They never cross a box, and each one gets its own attachment point.
- Prints one JSON line `{"ok", "out", "warnings"}`. Read the warnings. "Wider than tall" means: give `at` positions in the look, or use `graph TD`.
- To show the page, serve its folder on localhost (a launch.json preview entry, or `python3 -m http.server`) and open it in the browser pane, which cannot open `file://` URLs. Look at it before you hand it over.

### The look file: what Mermaid cannot say

```json
{
  "customer": {"kind": "external", "color": "slate", "at": [0, 0]},
  "provider": {"color": "sky"},
  "decide>orders": {"tone": "good"},
  "legend": [{"color": "slate", "label": "Outside your system"}, {"color": "sky", "label": "Payment provider"}]
}
```

- **Node id** keys: `at` [col, row] (give it for every node or none; without it, nodes are placed in layers along the arrows), `color`, `kind` (`service`, `external` = dashed, `store`, `decision`), `sub`, `label`.
- **Subgraph id** keys: `color`.
- **`from>to`** keys: `tone` (`good`, `warn` or `bad`) on the arrows that leave a decision.
- **Colours mean something**, never decoration: slate = outside your system (people, their devices, third parties), sky = cloud or vendor services, emerald = your app (the default), amber = waits for a person, rose = failure. Add a `legend` whenever more than one colour appears.

### Mermaid rules that matter here

- Define each node with its label (`pay[Payment API]`) **before** the first arrow that uses it. The parser keeps a node's first mention, so `shop --> pay` first leaves the label as "pay". `fd` stops with an error when this happens.
- A second label line is the sub-label: `shop[Shop API<br/>order service]`.
- Shapes: `[ ]` service, `[( )]` store, `{ }` decision. Arrows: `-->` sync, `-.->` async, `-->|label|` labelled.
- Sequence arrows: `->>` call, `-->>` reply (dashed), `-)` async (dotted in text, like a flow). Messages are numbered 1, 2, 3… in order. The walkthrough lights them by number.

## Setup and limits

- Needs Node 18+ and `uv`: `pic` runs `diagram.py` on uv's Python 3.12 (plain `python3` 3.9+ without uv). Libraries come from the plugin's `package.json`; Claude Code installs them on plugin install and update. In a loose copy, run `npm ci` where `package.json` is: beautiful-mermaid (MIT) for text and parsing, libavoid-js (LGPL) for arrows, roughjs (MIT) for the sketch, and @fontsource/architects-daughter (OFL). All run at build time; nothing loads from a CDN.
- If roughjs or libavoid is missing, the picture falls back (clean theme, simple curves) with a warning.
- The examples are in `examples/`: `checkout.flow.mmd` (+ `checkout.look.json`), `checkout.seq.mmd`, and `shop.hand.txt` (a hand-drawn diagram that passes `--lint`).

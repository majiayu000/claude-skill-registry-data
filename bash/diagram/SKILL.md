---
name: diagram
description: "Produce diagrams two ways: Mermaid DSL copied to the clipboard for mermaid.live or excalidraw (default; also ERD, class, gantt), or a polished self-contained interactive HTML through the local archify engine when the user wants a shareable technical diagram. Skip static images, bar/line/pie charts, and ASCII art."
argument-hint: "[diagram description]"
allowed-tools: Bash, Read
disable-model-invocation: false
effort: medium
---

Create a diagram for: $ARGUMENTS

## Route

- **Mermaid (default)** — quick or editable output, and every flowchart, sequence, class, state, ER, or gantt diagram.
- **archify** — only when the user asks for a polished, shareable, or interactive HTML (or names archify) AND the diagram is an architecture, workflow, sequence, data-flow, or lifecycle/state diagram. Everything else stays on Mermaid.
- Engine missing (`~/.local/share/diagram-engines/archify` absent, or no `node`): say so, offer `~/.config/ai/scripts/diagram-engines.sh` (network clone of the latest release — run only with 대협's consent), and deliver Mermaid meanwhile. Environments without a shell (Claude Cowork, Codex desktop app) always take the Mermaid route.

## Mermaid

1. Pick the fitting type (flowchart, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram, gantt) and output the DSL in a ```mermaid block.
2. Save to `/tmp/diagram.mmd` and copy it to the clipboard (`pbcopy`; `wl-copy`/`xclip` on Linux).
3. Tell the user: preview at mermaid.live, or excalidraw.com → Menu → Mermaid to Excalidraw. When layout matters (many cross-group edges), render it first — a local page loading mermaid from the jsdelivr CDN, screenshotted with headless Chrome — and look before handing over.

### Excalidraw import constraints (hard)

- No `\n` inside node text — it renders literally. Use commas or split into nodes.
- No HTML tags or markdown inside node text.
- `classDef` / `:::class` only in flowchart, classDiagram, stateDiagram — never in sequenceDiagram, erDiagram, gantt.

## archify

Engine root: `ENGINE=~/.local/share/diagram-engines/archify/archify` (latest release installed by `ai/scripts/diagram-engines.sh`; rerun it to update, `--check` to compare).

1. Read `$ENGINE/SKILL.md` "Fast authoring path" and only the one schema plus one example it names for the chosen type; follow it for authoring, `validate`, and `deliver`, running the CLI from `$ENGINE`.
2. One override: write the spec and HTML under `/tmp/archify/<slug>.json` and `/tmp/archify/<slug>.html` unless 대협 names a path. Let its "Update awareness" step run as written; when it reports a newer release, relay the notice and point 대협 to `~/.config/ai/scripts/diagram-engines.sh` — never update mid-task.
3. Look at the result before reporting: run `visual-check`; when it cannot run here, take headless Chrome screenshots of the delivered HTML at 1440×900 and at a tall viewport (`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,900 --screenshot=<out.png> file://<html>`; `brave-origin`/`chromium`/`google-chrome` on Linux — whichever is on PATH), read the images, and fix what the validator cannot see — overlapping boundaries, clipped rows, dead space. Never open a visible browser unless asked.
4. Report the delivered HTML path, the validate/deliver receipt (a showcase pass is 9 checks, 0 errors), and anything skipped. A non-zero exit is never success; after two repair rounds without a lower error count, stop and report the remaining diagnostics.

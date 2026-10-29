---
name: diagrams
description: >-
  How to show structure in a plan file, PR description or doc: a hand-placed SVG diagram or
  chart that takes its colours from one shared stylesheet and follows the reader's light or
  dark mode, or a text view in a code block (file tree, call chain, component tree, table
  columns, settings, routes, a type's shape). Use whenever a diagram, chart or text view goes
  into a Markdown file a person reads, including writing a plan's or doc's data model, file
  layout, settings, endpoints or types. Not for backoffice screen mockups or screenshots.
---

# Diagrams

A diagram replaces prose a reader would otherwise have to hold in their head: how a request
flows, what calls what, which states a record moves through. Draw it once, by hand, as an SVG
file, and link it from the Markdown.

## When to draw one

- **Draw** when a section explains structure, flow, order or change: more than two parts
  talking to each other, a branch or retry, a lifecycle, a before/after refactor, numbers
  worth comparing.
- **Skip** it when a sentence or a text view (see "Text views") says it as well. A one-file
  fix needs no picture.
- **One idea per diagram.** A flow and a data model are two diagrams, not one.
- **The text under a diagram covers only what it can't show** (follow `plain-writing`'s "Let
  pictures carry what they show"): rules, timings, failure behaviour, the reason for a choice.

## Hand-placed SVG, not Mermaid

Draw every diagram as an `.svg` file with each box and line placed by coordinates. That
includes small ones: boxes and arrows typed as text in a code block (`A ──▶ B`) are a
diagram too, and go in an SVG. A tree drawn with tree lines (`├──`) is a text view, not a
diagram. Don't use Mermaid, PlantUML, D2 or Graphviz either, even
though GitHub renders some of them inline:

- Their automatic layout decides where boxes go, so long flows come out as tall, thin strips
  with crossing lines and labels that wrap mid-word.
- Adding one step can swap whole branches left to right, so the before and after versions of
  a diagram can't be compared, which is the point of showing a change.

A hand-placed SVG stays where you put it. GitHub, VS Code's Markdown preview and browsers all
show it as an image.

## Pick the type

Pick by the question the reader has. Each type has a worked example in
`references/examples/`; read it before drawing that type, and copy its structure.

| The reader asks | Type | Example |
|---|---|---|
| What happens, step by step, and where does it branch? | Flowchart | `flowchart.svg` |
| Who calls whom, in what order, for one action? | Sequence | `sequence.svg` |
| What statuses can this record be in, and what moves it? | State | `state.svg` |
| What tables are there, and how do they relate? | Data model | `data-model.svg` |
| What lives in which layer, and what path does a request take? | Layers | `layers.svg` |
| Which server runs which part? | Deployment | `deployment.svg` |
| Which project or package references which? | Dependency map | `dependencies.svg` |
| How is this backoffice screen built, and where does its data come from? | Component tree | `component-tree.svg` |
| What moved where in this refactor? | Before and after | `before-after.svg` |
| When does each thing happen, and how far apart? | Timeline | `timeline.svg` |
| How do these numbers compare? | Bar chart | `bar-chart.svg` |
| How did this measure change over time? | Line chart | `line-chart.svg` |

## Text views

Some structure is clearer as text than as a picture, because the exact name, type or value is
the point: a file tree, a call chain, a Lit component tree, a table's columns, the manifest or
composer registration, settings, Management API routes, a type's shape, pseudocode for a
rule. `references/text-views.md` has the shape of each and when a picture replaces it; read
it before writing one.

- **In a plan or doc**, a text view shows the shape as it will be, in its own language, with
  no `+` or `-`.
- **In a PR**, it shows the change as a `diff` against the old shape.
- **Use one only where it replaces prose** or carries an exact value the reader needs.

## Start from the template

1. Copy `templates/diagram.svg` to the diagram's file. Name it for what it shows
   (`delivery-flow.svg`, not `diagram1.svg`).
2. Replace the placeholder line inside `<style id="theme">` with the whole of the stylesheet:
   the project's own `docs/diagrams/diagram.css` if it has one, otherwise
   `templates/diagram.css`. Keep the `<![CDATA[ ... ]]>` wrapper around it. Without it, a `<`
   anywhere in the CSS ends the file early and the image renders blank.
3. Delete the template's sample box and arrow, then draw.

## Lay it out by hand

- **Width 960, height as needed.** That fits a GitHub PR column at full size. Never wider
  than 1000.
- **Plan the grid before any box.** Decide the columns and rows, the gaps between them (wide
  enough for a label beside each line), and where the main path runs. Then place boxes,
  then lines, then labels.
- **One main direction.** The main path runs top to bottom or left to right; side branches
  step off it; a retry or loop goes back along the outside.
- **Leave room for the next change.** A gap in the grid where a likely new step would go lets
  a later version add it without moving anything else.
- **Lines run between box edges, at right angles,** with an arrowhead where they arrive.
  Labels sit beside a line, never on it or inside another box.
- **Short labels, real names.** Use the actual class, interface, route or table name, plus a
  few words. Detail that needs a sentence goes in the text under the diagram.
- **Group with regions.** A dashed `.zone` with a `.zone-title` says where something runs
  ("SchedulingPublisher server only") or which layer it belongs to.

## Colours come from classes

Every shape and text gets a class; nothing gets its own colour. Never write `fill="#..."`,
`stroke="#..."`, `style="..."` or `font-family` on an element. The only presentation
attributes are geometry (`x`, `y`, `width`, `height`, `rx`, `d`, `points`, `cx`, `cy`, `r`),
`font-size`, `font-weight`, `text-anchor`, `marker-end`/`marker-start`, and `fill="none"` on
a path.

- **One stylesheet holds every colour,** as CSS variables, with a light set and a dark set
  under `prefers-color-scheme`. The diagram follows the reader's mode wherever the viewer
  passes it through, and stays readable where it doesn't.
- **The background is solid.** Keep the `.bg` rect covering the whole canvas. A transparent
  diagram turns unreadable where the viewer's mode and the page's colour disagree (VS Code's
  preview follows the computer's setting, not the editor theme).
- **Colour means something.** Boxes are grey; colour marks a data store (`.store`), success
  (`.ok`), failure (`.fail`), what this change adds (`.new`) or one highlighted path
  (`.focus`). Nothing is coloured for decoration.
- **To restyle every diagram,** change the variables at the top of the stylesheet. A project
  that wants its own look keeps a copy at `docs/diagrams/diagram.css` and bakes it into each
  diagram's `<style id="theme">` block.

## Show what changed

- In a diagram of a change, mark each added box and line with `.new` (`marker-end` uses
  `url(#arrow-new)` on a new line), and add a `.legend` chip saying what the highlight means.
- A diagram of how the code looks now needs no `.new`; use `.focus` to trace one path
  through it instead.
- When a later version of a diagram adds a step, keep every existing box where it was. Edit
  the file; don't redraw it.

## Check it

Look at it before linking it. Open the `.svg` in a browser with Playwright (a standalone SVG
needs no server; `file://` works), screenshot it, then emulate dark mode
(`prefers-color-scheme: dark`) and screenshot again. In both:

- nothing overlaps and no text is cut off or crosses a line
- every arrow lands on the box it means, on the edge facing its source
- labels are readable and sit beside their own line
- it isn't blank (a blank image means the stylesheet broke the file; check the CDATA wrapper)

Then search the file for `#` colours and `style=`; there should be none outside the
`<style>` block.

## Embed it

- **Plan files and docs:** keep the `.svg` beside the Markdown that uses it and link it with
  a relative path: `![Delivery flow](diagrams/delivery-flow.svg)`.
- **PR descriptions:** relative paths break in a PR body; link the committed file the way
  `pr-describe` links a screenshot, by full URL pinned to a commit. GitHub serves an `.svg`
  from that URL as an image with its styles intact.

## *Class reference*

`templates/diagram.css` is the full list, with a comment per group. The ones used most:

| Class | Use |
|---|---|
| `.bg` | The full-canvas background rect |
| `.zone`, `.zone-title`, `.zone-note` | A dashed region and its heading |
| `.node` + `.shape`, `.title`, `.sub` | A box: its outline, bold name, and smaller second line |
| `.node.store` + `.lid` | A database or table cylinder |
| `.node.decision` | A diamond for a yes/no branch |
| `.node.ok`, `.node.fail`, `.node.new`, `.node.focus`, `.node.inactive` | Success, failure, added in this change, on the highlighted path, present but unused here |
| `.edge`, `.edge.return`, `.edge.dashed`, `.edge.new`, `.edge.focus` | Lines: a call, a reply, a weaker link, an added line, the highlighted path |
| `.edge-label` (`.center`, `.end`) | Text beside a line |
| `.left` | Left-aligned text inside a node or note |
| `.legend`, `.legend-label`, `.footnote` | Key and small print |
| `.badge`, `.badge-text` | Numbered dots tying matching parts together |
| `.lifeline`, `.activation`, `.frame`, `.frame-tag`, `.frame-tag-text`, `.guard` | Sequence diagrams |
| `.start`, `.end`, `.end-dot` | State diagram start and end markers |
| `.band`, `.band-title` | A solid layer row in a layers diagram |
| `.table` + `.head`, `.head-text`, `.row-alt`, `.col`, `.type`, `.pk`, `.fk` | Data-model tables |
| `.axis`, `.gridline`, `.axis-label`, `.bar.before`, `.bar.after`, `.series`, `.point`, `.threshold` | Charts |
| `.divider`, `.note`, `.heading`, `.mono` | Column dividers, side notes, a diagram heading, code names |

---
name: diagram-create
description: Create or update architecture, infrastructure, deployment, swimlane, and request sequence diagrams as generated HTML pages with inline SVG and one PNG per diagram, in one fixed style with built-in layout checks. Use when the user wants to draw how an existing system, environment, pipeline, data flow, or request flow works for docs, a README, or a wiki, or to change, check, or render such a diagram or its diagrams.py; not for data charts or for designing a new system, which belongs to system-design.
---

# Diagram Creation

Diagrams are code. A project keeps one `diagrams.py` that defines its
diagrams with the `diagram` package. One command checks every
diagram against the layout rules, writes the HTML pages with inline SVG,
checks in Chromium that all text fits, and writes one PNG for each SVG. The
package fixes every color, font, and size, so all diagrams share one style.

`D` is the diagram folder of the project, `docs/diagrams/` by default.

## 1. Decide whether to draw

- Draw only when a reader learns more from the picture than from a paragraph
  or a table. A list of things is a table. A one-box diagram is a sentence.
- Charts of data (bars, lines, scatter) are out of scope.
- The best move is usually deletion. Each node is a distinct idea: merge two
  nodes that always travel together. Each arrow carries information: remove
  an arrow that the layout already shows. A diagram is done when nothing can
  be removed. Aim for a density of about 4 out of 10.

## 2. Set up the diagram folder

1. If `D` already has a `diagrams.py` and a `diagram/` package, use
   them. Follow the README or AGENTS.md in that folder. Those project rules
   override this skill.
2. If the project has an older generator in this style (a script with an
   `Svg` class and `zone`, `path`, `label`, and `node` helpers), keep using
   it. It has none of the build checks. Port it to the package only when the
   user asks: each path string becomes a list of waypoints, and each label
   becomes the `label` of its edge.
3. Otherwise, copy `scripts/diagrams.py` and the `scripts/diagram/` package
   from this skill's directory into `D`. `diagrams.py` holds two example
   diagrams. Replace them with the real ones. Make sure that the
   repository ignores `__pycache__/`.

The package lives in the project, so the project can build its diagrams
without this skill. To change the style, edit `diagram/style.py`.
Never pass colors or fonts from a diagram function.

## 3. Workflow

1. **Collect the facts.** Take every node, edge, and label from the source of
   truth: code, configuration, infrastructure as code, manifests, and
   pipeline definitions. Draw the current state, unless the page that shows
   the diagram says that it shows a plan. Never invent a component to fill
   the layout.
2. **Choose the type** (§4). Read its section in
   [references/diagram-types.md](references/diagram-types.md). Read
   [references/drawing-api.md](references/drawing-api.md) before the first
   diagram.
3. **State the plan** in one short message: the type, the nodes, and what
   the budget (§6) cuts or splits. If the user can answer, let them redirect
   you. If not, continue and list your assumptions in the report.
4. **Write one function for each diagram** in `diagrams.py`, and list the
   pages in `PAGES`. First sketch the grid of columns and rows, then compute
   the coordinates.
5. **Download the icons and build** (§7). Fix every error that the build
   reports, then run the taste gate (§8).
6. If `D` has a README index, update it when you add, rename, or remove a
   diagram. Delete the HTML and PNG files that the build reports as stale.
   Commit `diagrams.py`, the HTML pages, and the PNGs together. Never edit
   the generated files by hand.

## 4. Choose the type

| The diagram shows                                                                                                                   | Type         |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| Components and their connections in one snapshot: system, runtime data flow, integrations, infrastructure overview, access coverage | Architecture |
| Where software runs: environments, networks, clusters, hosts, managed services, versions                                            | Deployment   |
| A process with handoffs between owners: CI/CD, release, approval                                                                    | Swimlane     |
| Time-ordered messages between 2 to 5 actors, with at most one branch                                                                | Sequence     |

If two types fit, pick the one for the main axis of the story. If no type
fits, a table or prose is probably better.

## 5. Style rules

- **Diagrams only.** Draw no page chrome: no eyebrow, title, subtitle,
  summary cards, or footer. Put no legend and no annotation callouts in the
  SVG.
- **Title and description.** The title is the short name of the subject. The
  description is one sentence about the content, not about the shapes.
  Assistive technology reads both.
- **Canvas.** Every SVG is 1280 px wide. The build sets the height to the
  content plus a 40 px margin. Never shrink the drawing to fit more.
- **Split, do not cram.** Over the budget (§6), split a diagram into more
  SVGs on the same page, for example one for each environment, or into an
  overview and a detail diagram.
- **Tag and icon on every node.** The tag is a short uppercase code, such as
  `LB`, `PG`, `JOB`, `EXT`, or `USER`. One code means one thing in a folder.
- **One or two accents.** Use them on the elements the diagram is about.
- **Arrow colors.** `muted` is the default. `link` is for HTTP and API calls
  and for calls to external systems. `accent` is for the headline path.
  Dashed arrows are optional, async, return, or passive flows.
- **Labels.** Keep an edge label to 14 characters or fewer, in uppercase. A
  sequence message can be longer if it fits between its two lifelines.
- **Ports.** When the target is mostly above or below, leave and enter
  through the top and bottom edges. Use side ports for mostly horizontal
  connections. Hold one main direction: left to right, or top to bottom.

## 6. Complexity budget

| For each diagram                                            | Maximum        |
| ----------------------------------------------------------- | -------------- |
| Nodes (a list node counts as one)                           | 9              |
| Arrows                                                      | 12             |
| Accent elements (enforced by the build)                     | 2              |
| Zones (architecture)                                        | 3              |
| Zones / nodes / chips / paths (deployment)                  | 3 / 6 / 9 / 8  |
| Lanes (swimlane)                                            | 5              |
| Lifelines / messages / fragments / `ALT` regions (sequence) | 5 / 12 / 1 / 2 |

## 7. Commands and what they check

Run from the project root:

```bash
uv run D/diagrams.py icons   # download the icons that the diagrams use
uv run D/diagrams.py         # check, write the HTML pages, render the PNGs
```

If Chromium is missing, the build prints the exact install command. The
build needs network access for Google Fonts. It reports every finding with
the element and its coordinates. When a rule fails, it writes nothing. When
text does not fit, it writes the HTML pages, so you can look at them, but no
PNG.

The package rejects at once:

- a diagonal edge segment, or an edge that turns back on itself
- an unknown node kind, edge color, or fragment operator
- a title over 60 characters, an empty description, or a bad slug
- a list node or zone too small for its content

The build then checks:

| Rule                | Limit                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Grid                | Every node, zone, tab, frame, lifeline, guard, and waypoint is on the 4 px grid.                                                                  |
| Margin              | Everything stays 40 px or more inside the canvas.                                                                                                 |
| Loose ends          | Each edge end touches a node, a tab, a lifeline, or a frame.                                                                                      |
| Transit             | No edge runs through a node, a tab, or a zone label.                                                                                              |
| Parallel runs       | Different edges stay 12 px or more apart.                                                                                                         |
| Attach points       | Edge ends on one side of a box are 12 px or more apart.                                                                                           |
| Corners             | Each segment is long enough for its 8 px corners and arrowheads.                                                                                  |
| Crossings           | The less important edge hops: dashed before solid, then muted, link, accent; on a tie, the later edge. A hop needs 16 px from a corner or an end. |
| Labels              | A label does not touch a box, another label, or any stroke within 4 px.                                                                           |
| Accents             | Focal nodes plus accent edges: 2 or fewer.                                                                                                        |
| Pages               | Page file names and slugs are unique. Every icon file exists.                                                                                     |
| Text fit (Chromium) | Every name, sublabel, tag, chip, and label fits its box, with real fonts.                                                                         |

After a build, it also warns about stale HTML or PNG files and unused icons.

## 8. Taste gate

The build cannot judge these. Check them on every changed diagram:

- **Fit.** Would a table or a paragraph do the same job? Is the type right?
- **Remove.** Can you remove a node, merge two nodes, remove an arrow, or
  remove a label, and keep the meaning?
- **Budget.** Is the diagram within §6?
- **Facts.** Can you trace every node and edge to the source of truth?
- **Look.** Open each changed PNG. Is the main direction clear? Are the
  ports chosen well? Is each accent on the element that matters?

## 9. Files

| Path                          | Role                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------ |
| `scripts/diagrams.py`         | Starter definitions: one architecture and one sequence example. Copy into `D`. |
| `scripts/diagram/`            | The package. Copy into `D`.                                                    |
| `references/drawing-api.md`   | The drawing API, node kinds, labels, and icons.                                |
| `references/diagram-types.md` | Layout rules for each diagram type.                                            |

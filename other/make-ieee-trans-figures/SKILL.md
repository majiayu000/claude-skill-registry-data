---
name: make-ieee-trans-figures
description: Create, revise, or audit publication-ready electrical-engineering control block diagrams with a Python/Matplotlib backend. Use for feedback and feedforward control diagrams, cascaded voltage/current loops, dq controllers, PLLs, motor-drive coordinate transforms, observers, PWM and plant signal-flow diagrams, summing junctions, takeoff points, crossover bridges, or editable SVG/PNG control figures for IEEE Transactions manuscripts. Also use when a user asks to reconstruct a paper's control diagram from supplied equations or control logic. Do not use for ordinary data plots, dashboards, circuit schematics, Simulink model construction, decorative illustration, or reverse-engineering missing control laws from an image.
---

# Make IEEE Transactions Control Diagrams

Turn supplied control logic into a traceable block diagram. Render the diagram
in Python only. Treat visual structure as an engineering statement: never add a
controller, sign, signal, gain, or connection merely to make the layout look
complete.

## Inputs

Accept a verbal control description, equations, a signal list, a paper figure,
or an existing diagram specification. Prefer:

- the controlled plant and control objective;
- block names and equations or transfer functions;
- signal names, units, directions, and reference/measured status;
- summing-junction signs;
- feedback, feedforward, disturbance, and saturation paths;
- source anchors for paper-derived content;
- target width and required SVG, PDF, or PNG exports.

Mark missing semantics as `UNKNOWN`. If the available material supports only a
proposed architecture, set `conceptual: true`; do not present it as an
implemented or as-built controller.

Read [control-diagram-contract.md](references/control-diagram-contract.md)
before creating a specification. Read
[electrical-control-symbols.md](references/electrical-control-symbols.md) when
mapping control semantics to nodes and connections. When a supplied figure
matches a common architecture, read
[reference-template-analysis.md](references/reference-template-analysis.md)
and start from one of the built-in editable templates in `assets/templates/`
to reuse topology and semantic structure only. Do not inherit their legacy
spatial grammar; rebuild geometry under an enforced `layout` contract.

## Required workflow

1. Identify the source and supplied assets.
2. State the diagram's engineering purpose in one sentence.
3. Define `figure_scope`: one primary message, one abstraction level, focus
   nodes, final width, node budget, and control-domain budget.
4. Extract blocks, signals, signs, branches, loops, and control domains.
5. Decide which information is topology and which belongs inside a block.
   Never use a large text box as a substitute for signal-flow topology. For
   paper-style architecture figures, set
   `figure_scope.block_content_policy: symbolic-minimal`.
6. Stop semantic assertion on ambiguous signs, directions, gains, or control
   relationships. If a useful conceptual artifact can still be delivered,
   set `conceptual: true`, mark the affected node or connection `UNKNOWN`,
   render an unknown summing sign with its glyph omitted, and document the
   unresolved boundary. Otherwise request clarification; never silently choose
   a conventional sign.
7. Create a normalized JSON diagram specification and an enforced physical
   `layout` contract for every new or revised publication figure.
8. Pass structural QA, then layout QA. Scope, abstraction, block content,
   graph integrity, centered/symmetric ports, shortest orthogonal routing,
   physical clearances, target arrows, and label ownership must pass before
   acceptance.
9. Render with the bundled Python/Matplotlib renderer.
10. Export editable SVG, mandatory 600-dpi PNG, and supplementary vector PDF
   from the same specification.
11. Pass automatic layout and image QA: final-size point geometry, font
    resolution/glyph coverage, content
    occupancy, collisions, exact raster geometry, monochrome readback, edge
    clearance, live SVG text, and export hashes.
12. Open the exact PNG at 100% and final target width. Record reviewer, time,
    eight-item layout rubric, decision, and that PNG's SHA-256 in
    `human_visual_review`. Automated PASS without this image-bound review
    remains `REVIEW_REQUIRED`.
13. Deliver the specification, rendered files, QA result, unknowns, and next action.

Use only these evidence states in the specification:

- `SOURCE_FACT`: explicitly anchored in a supplied source.
- `DERIVED`: reproducibly derived from anchored inputs.
- `RECOMMENDATION`: proposed control or presentation content.
- `UNKNOWN`: unresolved from current materials.

When matching a supplied raster, separate topology from presentation. First
create a measurable `reference_layout` contract for canvas ratio, main-flow
order, peer alignment, and the diagram's abstraction budget. Set
`style.reference_mode: true`; the validator rejects reference mode without
that contract. Then freeze the canvas and physical circle geometry; calibrate
typography, stroke and arrow scale; and add only visibly supported colors,
external signs, and annotations within the default style-policy
gate. Keep exact one-image
coordinates in the ignored case workspace, not in the public skill. A
reference-driven case also requires an explicit human `reference_match`
decision bound to the reviewed PNG hash.

Do not translate a reference into adjectives such as "black-and-white",
"two-channel", or "compact" and then improvise the geometry. Extract the
reference's spatial skeleton before placing content. When a reference source
file is available, prefer its object coordinates and dimensions over raster
estimation.

Choose the publication abstraction level before layout. Use
`reference_layout.max_node_count` as an explicit budget when the main figure
would otherwise become an implementation inventory. Move secondary thresholds,
startup logic, and protection details to a caption, inset, or separate figure
when the user authorizes that scope.

## Diagram semantics

- Use a rectangle for a controller, plant, transform, limiter, observer, or modulator.
- Use a signed circular junction for algebraic summation.
- Use an explicit filled takeoff point for every signal branch.
- Use arrow direction to encode causal signal flow.
- Use the shortest direct connection between block-diagram elements:
  unnecessary diagonals and bends are forbidden.
- Prefer a zero-bend straight route. Use one or two orthogonal bends only when
  port orientation or a real obstacle requires them. Duplicate and collinear
  waypoints are invalid.
- For diagrams whose visual grammar is horizontal/vertical, set
  `style.strict_orthogonal_routes: true`. A source-visible exception must
  be a source-cited `SOURCE_FACT` connection and declare both
  `allow_diagonal: true` and `diagonal_reason`; never tolerate an unexplained
  diagonal introduced by mismatched ports or waypoints. This exception does
  not waive shortest-distance or bend minimality; a clear direct diagonal has
  no intermediate waypoint.
- Prefer regular alignment across peer channels over preserving a few pixels
  of screenshot skew. Align named ports first; if the line still cannot be
  guaranteed horizontal or vertical, move the peer block.
- Treat diagonal exceptions as a last resort. Move a bus and its attached
  blocks onto one axis when that preserves semantics and removes the diagonal.
- Use square block and group corners. Rounded corners are outside the default
  control-diagram grammar and are rejected.
- Treat summing-sign placement as a source-driven option. Keep the algebra in
  `signs`; use `sign_visibility`, `sign_positions`, and `sign_colors` only for
  presentation fidelity. Never hide a negative sign or use an invisible sign
  color; custom sign positions remain local to the corresponding sum port.
- Audit each summing node as three independent visual layers: circle outline,
  optional internal operator geometry, and port-level algebraic signs. Enable
  `sum_center_cross` only when the source visibly uses a full diagonal cross;
  never let it replace the external or internal `+/-` semantics.
- Calibrate sum diameter together with sign placement: internal signs normally
  need more circle clearance, while external signs normally permit a smaller
  peer circle. Do not impose either placement or diameter globally.
- Calibrate circle outline, internal-operator stroke, and sign weight as one
  peer family without thickening ordinary wires or block outlines.
- Use distinct named ports for source-visible parallel signals. A single port
  on a side is centered. Two or more ports are centered, mirror-symmetric,
  equally spaced, and physically separated at final size. Omit named-port
  offsets to request deterministic symmetric allocation.
- Every causal connection, including every post-takeoff branch, ends with its
  own visible arrow. Block gaps and terminal runs must contain the arrowhead
  footprint without merging it into a block, port, or marker.
- Terminal variables remain visible; a terminal may not hide its label to make
  a layout appear cleaner.
- Place each signal label on the longest clean segment of its owning
  connection. Horizontal labels sit above the wire; vertical labels use one
  consistent side. A manually positioned label remains auditable against its
  owner.
- Use a crossover bridge only for a visibly non-connecting wire crossing.
  Every bridge must mark one real crossing; orphan bridges fail QA.
- Do not use free-form path decorations as signal lines. Every signal-like
  line is a typed `connection` with an explicit target arrow and route QA.
- Use dashed group boundaries only to identify meaningful control domains.
  Calibrate group fill, border, and caption independently; none changes graph
  connectivity. Render layers are fixed by semantic role, so specifications
  may not raise a group or decoration above signals, nodes, arrows, or text.
- Preserve mathematical notation and established IEEE electrical-engineering terms.

## Default visual grammar

Unless the user explicitly requests emphasis, use only black strokes, black
text, and white or transparent fills. Do not use role colors, shadows,
gradients, or gray status footers. An exceptional non-monochrome element must
set `style.allow_non_monochrome: true` and state
`style.non_monochrome_reason`. The exception applies only to a group fill
marked `emphasis: true` with `alpha <= 0.20` (at least 80% transparent);
signals, symbols, text, and borders remain monochrome. Color never carries
topology or algebra alone.

Functional blocks, circles, sums, junctions, and monochrome groups use white
or transparent fill; opaque black fill is forbidden because it erases black
text or signal flow. Visible takeoffs are renderer-controlled filled black
dots, bridge erasure is opaque white, and group alpha cannot make a semantic
boundary disappear.

Use `SimSun` for Chinese glyphs and `Times New Roman` for Latin letters,
numbers, and mathematics. Do not set per-node, per-group, or per-connection
font overrides. The font QA must resolve the actual font files, verify glyph
coverage, and record their hashes.

Every block declares one `content_class` and a short `content_items` list:

- `atomic`: one controller, gain, or operation; one line preferred, two lines
  require review;
- `transform`: source and target frames; no more than two lines;
- `subsystem`: subsystem identity and optional short function line, not its
  internal equations; no more than three lines;
- `supervisor`: state/selection/limit intent; no more than three lines.

Keep equations in topology when they describe dependencies between signals:
make the inputs and outputs ports/connections, and use explicit operator,
controller, sum, transform, or plant blocks. Put an expression inside a block
only when that expression completely defines the block's input-output
operator, all referenced signals are declared in `operation`, and the
connected topology exposes them. A controller or subsystem whose internal
law is not the point of the figure uses a short identifier such as `PI`,
`FRT`, `SVPWM`, `VSI`, or `PLL`; its gains, thresholds, bounds, modes,
sampling time, and explanatory prose stay in the caption, a parameter table,
or an authorized inset.

Under `symbolic-minimal`, every block also declares exactly one
`display_kind`:

- `identifier`: `content_items: ["title"]`; a short module identity only;
- `operator`: `content_items: ["equation"]`; a complete input-output operator
  with an `operation` contract;
- `frame_transform`: `content_class: "transform"`, exactly
  `source_frame` and `target_frame`, and a source-supported diagonal split.

Do not use a supervisor rectangle as a convenient container for formulas,
thresholds, recovery rules, or parameter values. If those details are
essential to the figure's primary message, expand them into topology or move
them to a separate detail figure.

For block occupancy, require at least 2.5 pt or 0.30 em internal padding. Text
must remain inside its owner. Width ratio above 85%, height ratio above 78%,
or area ratio above 45% requires review; above 92%, 88%, or 60% respectively
fails. Underfilled atomic blocks require review rather than enlargement by
default. Fix content or geometry; do not shrink below final-size legibility
merely to pass.

Do not merge multiple incoming signals without a summing junction. Do not split
one signal into multiple destinations without a takeoff point. A crossing is
not a connection unless an explicit takeoff or junction is present.

## Hard constraints

- Never infer a missing plus/minus sign from layout alone.
- Never invent controller gains, transfer functions, filters, delays, limits, units, or sampling rates.
- Never convert an unreadable screenshot into asserted control logic.
- Never label a conceptual diagram as implemented, experimentally verified, or as-built.
- Never claim that visual similarity proves control equivalence.
- Never replace a power circuit schematic or Simulink model with this diagram.
- Never silently use Graphviz, R, MATLAB, Origin, or another rendering backend.
- Never hard-code journal dimensions or typography as an IEEE requirement without an authoritative source.

## Rendering

Run:

```text
python scripts/render_control_diagram.py SPEC.json --output-dir OUTPUT_DIR
```

List or copy a built-in topology scaffold with:

```text
python scripts/scaffold_control_template.py --list
python scripts/scaffold_control_template.py --template dual-axis-loop --output SPEC.json
```

The three built-ins cover a dual-axis nested-loop architecture, an expanded
nested observer, and its reduced equivalent representation. They are
genericized signal-flow topology scaffolds, not copies of private reference
images and not layout-approved publication figures. Their legacy coordinates
remain diagnostic inputs only. Add and pass an enforced physical `layout`
contract before using a scaffold in a deliverable.

The renderer performs deterministic contract validation before writing files.
It uses normalized source coordinates, final-size point checks, and Matplotlib
only; it does not require an external graph-layout package. Named ports whose
offsets are omitted receive a centered symmetric distribution. Under
`route_mode: shortest-orthogonal`, connections without manual waypoints use
the shortest clear local orthogonal candidate. Explicit routes are never
excused merely because they were hand-authored. If validation fails, correct
the engineering specification instead of bypassing the gate.

The QA JSON records specification, renderer, font-file, and export SHA-256
values. Preserve them with every
reference-comparison round so an accepted image can be reproduced from its
specification and renderer revision.

The renderer resolves real text extents after Matplotlib lays out the selected
fonts. It rejects text outside its owner block, text-text and text-node
collisions, signal lines through unrelated nodes or labels, and insufficient
peer-block clearance. Automatic labels flip away from a canvas edge, and every
resolved text box must remain inside the canvas. It applies the final-width
font floor to every visible
text kind, including signal variables, sum signs, terminals, annotations, and
group captions. At final width, visible strokes must stay within the 0.5–3 pt
house range, arrowheads within 5–14 pt, and bridge erasure clearance at or
below 6 pt; undersized or topology-obscuring marks fail. It rejects every
unmarked intersection between different connections, including a
source-authorized diagonal. A structural pass with
failed visual QA returns overall
`status: FAIL`; disabling automated visual QA returns
`status: REVIEW_REQUIRED`, never `PASS`. Structural QA is computed rather than
declared. A render is refused unless `structural_qa.status` is `PASS`.

All PNG outputs must be exported at exactly 600 dpi. This is a hard gate, not a
per-request preference: the validator rejects any explicit
`output_dpi != 600`, and the renderer defaults omitted `output_dpi` to 600.
For a fixed raster canvas, set `pixel_width = width_in * 600` and
`pixel_height = height_in * 600`; do not claim 600 dpi while retaining
low-resolution pixel dimensions. SVG and PDF are resolution-independent vector
outputs, but they must be generated from the same physical canvas and source
specification as the 600-dpi PNG.
High DPI does not establish legibility. Never use pixel count or DPI metadata
as evidence that labels, spacing, hierarchy, or final-width readability pass.

Use `--validate-only` when auditing a specification without rendering.

## Output contract

Return:

1. source identity and diagram purpose;
2. content status: source-derived, derived, recommended, or unknown;
3. editable JSON specification;
4. Python renderer reference;
5. editable SVG output;
6. 600-dpi PNG output at the declared canvas size, plus editable SVG and
   supplementary vector PDF from the same specification;
7. structural and visual QA result;
8. unresolved control semantics and limitations;
9. recommended next action.

Before delivery, apply [qa-checklist.md](references/qa-checklist.md). Require
`structural_qa.status: PASS`, `layout_qa.status: PASS`,
`image_qa.status: PASS`,
`human_visual_review.status: PASS`, and overall `status: PASS`. Confirm that
SVG text remains editable,
feedback signs and arrow directions are legible, labels are not clipped, and
every branch or merge has an explicit electrical-control meaning.
Confirm that peer labels such as paired subsystem names share one declared
style group and typography unless the source explicitly distinguishes them.

When calibrating against user-supplied reference diagrams, follow
[iteration-loop.md](references/iteration-loop.md). Preserve every prior case as
a regression test, and internalize only improvements that remain valid beyond
one reference image. Apply the accumulated reusable corrections in
[reference-calibration-rules.md](references/reference-calibration-rules.md);
keep reference-specific coordinates and assets in the private case workspace.

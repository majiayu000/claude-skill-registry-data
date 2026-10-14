---
name: docs
description: "Generate or refresh rendered project documentation, then verify it against the content-governance exit-condition family (language, completeness, tone)."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

`/akka:docs` is a generator. It writes and refreshes the project's rendered
documentation under `docs/`, then hands that output to the content-governance
exit-condition family that verifies it. Documentation is a surface class in the
single coverage gate: every documentable thing needs a page, the same way every
code module needs a covering check. Generation lives here in the assistant; the
engine verifies the deterministic conditions and records the attestation for the
one condition it cannot decide.

## When it runs

`/akka:docs` is primarily an À la carte command. The developer invokes it
directly when they want to (re)generate the project's rendered documentation
and see how the content-governance exit conditions decided. In Enforced mode
the assistant runs the same activity autonomously as part of its build loop,
whenever CONTENT-LANGUAGE, Completeness, or CONTENT-TONE is `open` and the
assistant can act on it. In both modes the behavior is identical; only
ship-gating differs.

## Outline

1. **Enumerate the documentable things.** Collect what the project can document
   from observable sources — the a-la-carte commands, the active exit conditions,
   the public API endpoints detected in the tree. This enumerable set is the
   completeness target.

2. **Load the fixed template.** Read
   `plugins/akka/templates/docs-template.html` from the akka plugin. This file
   is the fixed design contract for `/akka:docs`: it contains the full CSS,
   the full HTML skeleton, the header, the stats grid, the collapsible
   diagram and component sections, the SVG scaffolding for the interaction
   diagram, and the banded SVG scaffolding for the component graph. Every
   generated `docs/index.html` uses this template verbatim — the assistant
   MUST NOT modify the CSS, the layout, the fonts, the colors, or any other
   design detail. Customers do not override the design; the template is the
   design. The palette is enumerated in
   `plugins/akka/templates/akka-style-guide.md`, and step 9 checks the
   generated page against it, so this rule is enforced rather than trusted.

3. **Fill the placeholders and paste the fragments.** The template contains
   two kinds of insertion points:

   - **Single-value placeholders**: `{{TITLE}}`, `{{LEAD}}`,
     `{{STAT_COMPONENTS}}`, `{{STAT_EVENTS}}`, `{{STAT_ENDPOINTS}}`,
     `{{STAT_VIEWS}}`, `{{STAT_DOMAIN_OBJECTS}}`, `{{ENTITY_HINT}}`,
     `{{INTERACTION_HINT}}`, `{{COMPONENT_GRAPH_HINT}}`, `{{SLUG}}`,
     `{{INTERACTION_TITLE}}`, `{{INTERACTION_DESC}}`,
     `{{COMPONENT_GRAPH_TITLE}}`, `{{COMPONENT_GRAPH_DESC}}`,
     `{{FOOTER_TARGET}}`. Fill each with the project-specific value.

   - **Region placeholders**: `{{ENTITY_BOXES}}`, `{{INTERACTION_SVG_BODY}}`,
     `{{COMPONENT_GRAPH_BODY}}`, `{{ADDITIONAL_DIAGRAMS}}`,
     `{{COMPONENT_REFERENCE}}`. The template
     shows each region's fragment shapes as HTML comments directly above the
     placeholder. Copy the fragment verbatim for every entity / domain object
     / component / lane / message and fill only the identifier and field
     values. Do not restyle. Do not restructure.

   Component-kind coloring is fixed by the CSS classes (`ese`, `kve`, `view`,
   `wf`, `agent`, `ep`, `ext` for HTML fragments; `n-ese`, `n-kve`, `n-view`,
   `n-wf`, `n-agent`, `n-ep`, `n-ext` inside the component-graph SVG). Choose
   the class that matches the component's Akka type; the accent color follows
   automatically.

4. **Draw the diagrams to the rules the template states.** The template's
   header comment carries five rules that step 9 verifies. They are not style
   advice, and a page that breaks one reds the language check:

   - **Accessibility.** Every diagram `<svg>` carries `role="img"` and
     `aria-labelledby`, with `<title>` as its first child before `<defs>` and
     `<desc>` immediately after, both id'd `{{SLUG}}-<name>-title` /
     `-desc`. Bare `title` / `desc` ids are banned — two diagrams on one page
     collide and the second is announced with the first one's name. `<desc>`
     says what the diagram shows, never its geometry.
   - **Connectors.** Two nodes sharing neither x nor y are joined by a rounded
     right-angle `<path>` elbow (r=8), never a diagonal `<line>`. Connectors
     entering the same edge of a box get their own attach point ≥12px apart.
     Draw every connector before the nodes so the boxes paint over the stroke
     ends.
   - **Labels.** Every connector label needs an opaque mask rect behind it and
     a visible 6–10px gap above the stroke. A label sitting on its own
     connector hides the thing it describes. Keep the mask on open canvas — a
     mask overlapping a node is clipped by the node fill and the text renders
     as a fragment on the border.
   - **Color.** The two color rules apply to different diagrams and mixing them
     erases both. **Inventory** graphics — the component graph and the entity
     boxes — are categorical: the seven kind colors identify what a thing is,
     and the legend decodes them. **Narrative** graphics — the interaction
     diagram — are editorial: the primary path is yellow, everything else is
     muted grey. Never color an interaction lane's arrows by component kind;
     it makes every arrow equally loud and the reader cannot find the path
     that matters.
   - **Budget and grid.** Max 9 nodes, 12 connectors, 5 interaction lanes per
     diagram; every coordinate and size on the 4px grid. Over budget, split
     into an overview plus a detail diagram rather than shrinking the type.

5. **Choose what the diagrams show.** Three artifacts are always produced —
   entity, interaction, component graph. Pick their content from the shapes the
   project actually has, rather than drawing the same thing for every project:

   | When the project has… | The interaction diagram shows |
   |---|---|
   | a command → event → projection path | that path end to end: client, endpoint, entity, view |
   | a Workflow with steps, retries, compensation | the durable execution: each step, and what happens when one fails |
   | an entity with a lifecycle in its events | the state transitions and their guards |
   | an Agent with tools | the model call, the tool calls, and the guardrail |
   | timers or scheduled work | the ordering, with the delay on the arrow |

   Choose the one path a reader most needs to understand; the rest belong in
   the component reference. If two paths are equally central, draw the primary
   one and note the second in `{{INTERACTION_HINT}}`.

   **Verify the path before drawing it.** Read the step bodies and the call
   sites, not the class names — a workflow step named `persist` may not be the
   only step that writes, and an agent that exists may have no caller at all.
   A diagram asserting a call that does not happen is worse than no diagram,
   because it is believed.

6. **Add a diagram only when it earns its slot.** `{{ADDITIONAL_DIAGRAMS}}`
   holds zero or more extra diagrams. Add one when it shows something no other
   diagram on the page carries, and name that thing in its `sec-hint`. Two or
   three extra is a normal maximum.

   **A budget waiver obliges a detail diagram.** When the component graph or
   interaction diagram goes over budget, the rule in step 4 is to split into an
   overview plus a detail — the overview stays in the fixed slot and the detail
   goes here. Recording the waiver without drawing the detail leaves a hole and
   says so in writing; that is worse than either drawing it or leaving the
   component out silently, because it advertises the omission and does nothing
   about it.

   | Type | Earns its slot when |
   |---|---|
   | **State machine** | a record has a lifecycle in its events and the guards are the interesting part — the entity diagram lists fields, it never shows a transition |
   | **Sequence** | the interaction diagram hit the 5-lane limit and the participants it dropped are load-bearing |
   | **Timeline** | one record carries several independent clocks, so a reader cannot tell which question each answers |
   | **ER** | domain records reference each other and the entity diagram draws them as separate boxes with no edges |

   Do not reach for a quantitative type — bar, line, scatter, treemap, radar,
   quadrant, Gantt. Component counts are already the stats grid, and a chart of
   them is decoration. If a three-column table would say the same thing, use
   the table.

7. **Write `docs/index.html`.** After filling every placeholder, write the
   result to `docs/index.html` in the project directory. The file is
   self-contained — no external JavaScript, no external CSS, no remote images,
   no build step needed to view — so it can be opened directly in a browser or
   served from any static host.

8. **Pages for enumerated documentable things beyond the three rendered
   artifacts.** For every à-la-carte command, active exit condition, and
   detected public endpoint that is not already covered by the three
   rendered artifacts, append a matching `<details class="sec">` section to
   the `{{COMPONENT_REFERENCE}}` region using the same fragment shape shown
   in the template. Follow the project's terminology; the deterministic
   checks below verify it. A component left out of a diagram to stay inside
   the complexity budget is recorded here with its reason — an omission is a
   waiver, never a silent drop.

9. **Verify against the content-governance family.** Run the three conditions and
   report each. Each has a default ship tier:

   - **CONTENT-LANGUAGE (deterministic, ship tier: author).** Two introspective
     checks over `docs/`, both falsifiable, both reported under this condition:

     *Prose.* The Vale prose linter using the project's `.vale.ini` (generated
     into `/harnesses/content/` by `/akka:harnesses`). It decides banned
     phrasings absent, mandated substitutions honored, terminology correct, and
     the structural conventions — required sections present, heading conventions
     followed.

     *Diagram structure.* `python harnesses/content/diagram_check.py docs/*.html`,
     which decides the falsifiable half of step 4: the accessible-SVG contract;
     diagonal connectors; every `<rect>` and `<line>` coordinate on the 4px grid;
     a label mask clipped by a node drawn after it; a connector label with no
     mask; the node, connector, lane and accent budgets; every CSS class used
     having a rule; the Akka palette; remote assets and scripts; and the file's
     encoding. Four rules stay unchecked because the markup does not carry what
     they need — elbow radius, attach-point spacing, the 6–10px label gap, and
     paint order — so those are the ones to read carefully by eye.

     Both are introspective: shell out, map a non-zero exit to `red`. On a
     machine without Vale or without Python the affected check is `open` with
     reason `blocked-outside-project` and the missing tool named, never a false
     `red`. The author-tier default means this check runs on every ship — both
     tools are fast enough to be a per-commit gate.

   - **Completeness (the coverage gate, ship tier: author).** Every documentable
     thing enumerated in step 1 has a page on disk. A documentable thing with no
     page reds the gate. Completeness is not a separate command — it is the
     documentation surface class inside the single coverage gate. A thing
     intentionally left undocumented is a recorded waiver with a reason, not a
     silent omission. The author-tier default means every ship verifies that no
     documentable thing has been left without a page.

   - **CONTENT-TONE (delegated, ship tier: review).** The holistic dimension a
     linter cannot reduce to a token list — state a fact, not a flourish;
     declarative, not persuasive; reads like a person. This covers the half of
     step 4 no script decides: whether the diagram earns its place, whether the
     right path was chosen, whether a node could be removed. Do not score prose
     or diagrams 1-to-5; that rubber-stamps. Apply the project's decomposed
     rubric as single-criterion pass/fail predicates, framed adversarially
     ("find every place this reads like marketing"; "find every node a reader
     would not miss"). When the pages pass, call `akka_harness_attest` with the
     tone condition key and a receipt reference. The attestation is keyed to a
     content-plus-rubric signature, so a rule change or an edit invalidates it and
     the condition returns to `open` with reason `needs-user-action` until re-run.
     The engine records that the judge ran and covered the current content; it
     never scores the prose itself. The review-tier default means CONTENT-TONE is
     verified before the change is opened for team review, not on every commit —
     re-attesting every time a source file changes would be excessive.

10. **Report.** Call `akka_ec_conform`, then present `akka_ec_summary` to the user
   **verbatim** — the plain outcome. Do NOT restate internal condition ids or the
   words "auditor" / "coverage gate". Offer *"say 'show details' for the full
   checklist"* for the manifest.

## Key rules

- The engine never calls a model. The deterministic language check delegates to
  Vale and to `diagram_check.py`; completeness is a page-exists test; only the
  tone judgment runs here in the assistant, and it reaches the engine as an
  attestation, not a score.
- Nothing false-passes. A missing page reds the coverage gate; a banned phrasing
  or a broken diagram contract reds the language check; tone with no attestation
  stays `open` with reason `needs-user-action`.
- The design is checked, not trusted. A generated page using a color outside the
  Akka palette reds the language check, so "do not modify the CSS" is enforced.
- Same behavior wherever the exit-condition set is active. The generator and the
  three conditions exist in À la carte and Enforced mode alike; only ship-gating
  differs, advisory in À la carte and blocking in Enforced. Where the set is
  dormant the pages are still generated and no conditions are recorded.

## Done When

- [ ] The documentable things (commands, active exit conditions, detected endpoints) were enumerated as the completeness target.
- [ ] A page was generated or refreshed under `docs/` for each documentable thing, following the project's structural and terminology conventions.
- [ ] Every diagram `<svg>` carries `role="img"`, `aria-labelledby`, and a prefixed `<title>`/`<desc>` pair with `<title>` as its first child.
- [ ] Off-axis connectors are rounded right-angle elbows, connectors sharing a box edge have their own attach points, and every connector label has a mask rect with a visible gap above the stroke.
- [ ] Inventory diagrams used categorical kind color; the interaction diagram used editorial color with one primary path.
- [ ] Each diagram is inside the node / connector / lane budget, or was split into overview plus detail; anything omitted for budget is recorded as a waiver with a reason.
- [ ] Every budget waiver has its detail diagram in `{{ADDITIONAL_DIAGRAMS}}`, or states why one cannot be drawn — a waiver alone advertises a hole without filling it.
- [ ] Every additional diagram names, in its `sec-hint`, the thing no other diagram on the page shows.
- [ ] Every call, step and participant drawn was verified against the step bodies and call sites, not inferred from class names.
- [ ] CONTENT-LANGUAGE ran Vale **and** `harnesses/content/diagram_check.py` over `docs/` and reported `green`/`red` (or `open` with reason `blocked-outside-project` where a tool is unavailable — never a false `red`).
- [ ] Completeness was checked as the documentation surface class of the coverage gate; any undocumented thing reds the gate or was recorded as a waiver with a reason.
- [ ] CONTENT-TONE applied the decomposed adversarial rubric as pass/fail predicates and, on pass, was attested via `akka_harness_attest` with the condition key and a receipt reference — never left as a numeric score.
- [ ] `akka_ec_conform` was called and the plain `akka_ec_summary` (never internal ids or the word "auditor") was shown to the user.

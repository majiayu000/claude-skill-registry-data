---
name: optimize-ux
description: Redo one whole view or one UX flow from the ground up. Inventory every data point, interaction and flow, design each one separately in parallel subagents, combine them into 2–3 whole-view directions, test those as clickable prototypes, propose them with reasoning, and — after the user picks and asks to build — implement the chosen one pixel perfect with deliberate microinteractions. Use whenever the user asks to redo, rethink, rebuild or redesign a full view, screen, page or UX flow, including when the request arrives as Annury annotations or plan/preview comments on a view ("redo this view", "redo this flow", "this whole screen needs to be rethought", "start over with this page"), and for "optimize this view", "make this page great", "ux optimize X". Not for small fixes to single elements; for review-only use improve-ui.
---

# Optimize UX

One view in, one excellent view out. The skill works bottom-up: first every
part of the view is understood and designed on its own, then the parts are
combined into whole-view directions, the directions are tested, the user
picks, and only then is anything built.

## When to use

- The user asks to redo, rethink, rebuild or redesign a whole view or a
  whole UX flow, in chat or in an annotation.
- Annotations (Annury, preview or `plan` comments) on a view say the view or
  flow as a whole is wrong, not only one element.

Do not use it for a fix to one element; make that fix directly. For a
review with proposals only, use `skill://improve-ui`.

A flow target is handled the same way as a view: capture every screen of
the flow, inventory across all of them, and propose whole-flow directions.

## Annotations are input

When the request comes from annotations, collect all of them for the view or
flow first: the comment text, the element or section each one points at, and
any attached image. Then:

- add an `Annotation` column to the inventory and link each annotation to the
  rows it touches; an annotation with no matching row adds a row;
- pass the annotations of each item to its subagent in phase 3 as hard
  requirements;
- in phase 6, show for each direction how it answers every annotation; an
  annotation that a direction does not answer is a stated tradeoff, never a
  silent drop.

Phases, each with a gate. Never skip a gate.

| Phase | Output | Gate |
| --- | --- | --- |
| 1. Capture | Screenshots + state walk of the real view | View opened in a browser |
| 2. Inventory | `inventory.md`: data points, interactions, flows | Every visible thing has a row |
| 3. Item design | One design brief per item, from subagents | Every row has a brief |
| 4. Combine | 2–3 whole-view directions as prototypes | No unresolved conflicts between briefs |
| 5. Test | Each direction walked per flow, scored | Same tasks run on every direction |
| 6. Propose | Plan deck with a `pick` ballot | User picks |
| 7. Build | Pixel-perfect implementation + microinteractions | User says implement |
| 8. Verify | Screenshot diff vs prototype, motion check | Diffs explained or fixed |

Phases 1–6 change no application code.

## Rules that hold in every phase

- Read `skill://ux` first. Its Visual consistency check and Intentional visual
  restraint check apply to every brief, every direction, and the final build.
- Read `skill://agent-browser` (or run `agent-browser skills get core`) before
  any browser work. Findings about the current view come only from the running
  view, never from reading components.
- Use the project's design system: `UX.md`, `docs/ux/*`, token files, the
  component library, Storybook. Every proposal is expressed in its tokens and
  components. A new pattern must be named as new and justified.
- Keep a working folder: `.work/plans/<project>-optimize-<view>/`. Shots go in
  `shots/`, the inventory in `inventory.md`, briefs in `briefs/`, prototypes
  as `variant-*.html`.

## 1. Capture

Resolve the view (URL or route) and start the app the way the repo says.
Ask one question only if the repo cannot answer it (usually credentials or
which of two similar views).

Capture with `agent-browser`, at 1440×900 and 390×844, light and dark if the
app themes:

- default state, then empty, loading, error (force with
  `network route "**/api/**" --abort` or a stubbed body), and an overflow
  state with long names and values;
- hover, focus and active of every control; the keyboard tab order;
- `console`, `errors`, `vitals`.

Number shots by state: `shots/01-default-desktop.png`.

## 2. Inventory

Write `inventory.md` with three tables. Every visible thing on the view and
every thing the user can do must have one row. Name each row with a stable id;
later phases refer to it.

**Data points** — `id`, label as shown, source (API field or computed), type,
example value, worst-case value (longest, empty, null), who needs it and for
which decision, current position and prominence.

**Interactions** — `id`, control, trigger (click, key, hover, drag, scroll),
what it changes, feedback today, latency, failure behaviour, keyboard and
touch equivalent.

**Flows** — `id`, user goal, entry, steps as a list of interaction ids, exit,
current step and click count, where it breaks or stalls (from the capture).

Then add a short **Job of the view** paragraph: who comes here, what they came
to decide or do, and which flows matter most. Rank the flows. The ranking
drives every tradeoff later.

Show the inventory to the user as a short chat summary (counts, top flows,
the three worst observed problems). Do not wait for approval unless the job
of the view is unclear.

## 3. Item design (parallel subagents)

Fan out with the `task` tool in one batch. Group to stay under 32 agents:

- one agent per flow;
- one agent per interaction that is non-trivial (has states, latency, or
  failure); trivial interactions are grouped by region;
- data points grouped by region or by decision they serve, 3–6 per agent.

Give every agent the same shared context: path to `inventory.md`, the job of
the view, the ranked flows, the shots folder, the design-system files, and the
UX rule pack from `skill://ux`. Each agent is read-only and writes one file,
`briefs/<id>.md`, with:

- **Need** — what the user must get from this item, and when.
- **Options** — 2–3 ways to show or do it, each with an ASCII sketch, the
  token/component it uses, and its cost.
- **Recommendation** — one option and why, in terms of the ranked flows.
- **States** — default, empty, loading, error, overflow, disabled, selected.
- **Microinteraction** — for interactions: trigger, rules, feedback, loops and
  modes (Saffer's model). Feedback names the property that changes, the
  duration and easing token, and the reduced-motion fallback.
- **Constraints on others** — what this item needs from the layout (space,
  position, adjacency to another id). This is what phase 4 resolves.
- **Could be removed?** — say so if the item does not serve the job.

Flow agents also return the ideal step sequence, the click and keystroke
count, and which items the flow passes through.

## 4. Combine

Do this yourself; it is judgement, not mechanics.

1. Read every brief. List the conflicts: two items that want the same space
   or prominence, flows that want different orders, items marked removable.
2. Resolve each conflict by the flow ranking. Write the resolution down.
3. Build 2–3 **directions**. Each is a coherent whole, not a mix: they differ
   in a real structural choice (for example list-first vs detail-first,
   inline editing vs a side panel, progressive disclosure vs everything
   visible). Do not offer a direction you would not recommend shipping.
4. Build each direction as a clickable prototype `variant-<name>.html`
   (`<body data-proto>`) in the project's real tokens, at real size, with a
   state switcher inside the page (default, empty, loading, error, overflow,
   mobile, dark). If the project has Storybook, a story is an acceptable
   prototype instead.
5. Run both `skill://ux` checks on each prototype. Fix every `Issue` before
   phase 5.

## 5. Test

Walk every direction with `agent-browser`, with the same tasks, in the same
order:

- each ranked flow, start to done: count clicks, keystrokes, scrolls and
  context switches; note where the eye has to search;
- keyboard only, then 390 px wide;
- the failure path of the top flow;
- the overflow state.

Record a score table: rows are flows and checks, columns are the current view
and each direction. Screenshot each step. Numbers beat adjectives: "3 clicks
→ 1", "primary action moves above the fold on mobile".

## 6. Propose

Present with `skill://work-plan` (the `plan` tool) as a slide deck:

1. Title: the view and its job in one line.
2. Problem: the three worst observed problems, each with its shot.
3. Inventory: counts and what was cut or demoted, with a link to
   `inventory.md` detail in a drill-down.
4. One slide per direction: the prototype embed, the structural choice, the
   score row, what it is best at, what it gives up.
5. Score table across all directions.
6. A `pick` ballot over the directions, with one marked `recommended` and a
   one-line reason inside each option.
7. At most two more ballots, only for choices that change the build
   materially.

Apply the returned answers as `skill://work-plan` describes. Iterate until the
user picks. Picking is not permission to build.

## 7. Build (only after "implement")

First write `docs/ux/<view>.md` in the `skill://ux` flow-doc format from the
chosen direction, its briefs and the resolved decisions. It must pass the
`skill://ux` implementation-ready gate. Then implement under `skill://ux`
Implementation mode.

**Pixel perfect** means:

- every size, gap, radius, colour and type style comes from a token; no
  magic numbers; an off-grid value is a bug;
- shared edges align across regions; controls in a row share a centerline;
- text never shifts layout when it changes (tabular numerals, reserved width
  for counts and states, fixed-height loading placeholders);
- the build matches the prototype at both viewports and both themes.

**Microinteractions** come from the briefs, one per non-trivial interaction.
For each, implement:

- immediate feedback on press (under 100 ms), even before the request ends;
- a visible pending state for anything slower than ~300 ms, without layout
  shift;
- a success and a failure end state that say what happened, in place;
- motion only on the property that explains the change (opacity, transform),
  with the project's duration and easing tokens, and a
  `prefers-reduced-motion` fallback;
- focus that lands somewhere sensible after the interaction ends.

No decorative motion, springs, or confetti; the restraint check still holds.

Commit each coherent step separately.

## 8. Verify

- Screenshot the built view at the same states and viewports as the
  prototype and compare side by side (and pixel diff where the tooling
  exists). Fix or explain every visible difference.
- Exercise each microinteraction in the browser: record a short clip or a
  frame sequence for the important ones; check the reduced-motion path with
  `agent-browser set media reduced-motion` or the equivalent.
- Re-run the phase 5 tasks on the build. The score must match the chosen
  direction.
- Run both `skill://ux` checks on the built UI and the project's tests and
  gates.

Hand back: what changed, the before/after score row, and any gap you could
not close.

## Boundaries

- Phases 1–6 never edit application code.
- No new pattern without saying it is new; update `UX.md` when a reusable
  pattern changes.
- One view or one flow per run. A second one is a second run.

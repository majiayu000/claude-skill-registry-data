---
name: ripple
description: Write crafted Ripple specs (the {version, state, ui} JSON that Ripple renders as an interactive card) by picking the right widget first, then rendering the spec, auditing it mechanically, looking at its own screenshots at phone and desktop width in light and dark, fixing, and repeating until a round is clean. Use whenever you write or improve a Ripple spec, a generative UI card, a chat answer drawn as UI, a gallery fixture or a widget example, even if the request only says "make a card for X" or "build a small tool".
license: MIT
compatibility: Works in Claude Code, Codex and OpenCode. Needs Node 20+ and Playwright with Chromium in the project you run it from (npm i -D playwright && npx playwright install chromium). axe-core is optional.
---

# Ripple cards

A Ripple card answers one question. The reader gets the answer in a second, and everything else on the card is a
true secondary fact or a control that changes the answer. The model writes data; widgets own the design; a machine
and a pair of eyes check the result before anyone else sees it.

The method comes from the [Anatomy](https://github.com/wheresryan22/anatomy) skill by Ryan (MIT), which does the
same for isometric drawings: load the craft rules, the map and the examples; build; render; audit; look at your own
screenshots; fix; repeat until a round finds nothing. The words and the script here are Ripple's own.

## The two rules that outrank everything

1. **The user's data is not yours to change.** Never alter a number, a date, a name, an amount or a target the user
   gave you (or that the card's answer depends on) to make a widget look right or to make a count reach 0. If a
   widget misbehaves with true data, keep the data and try another widget or another layout. If nothing works,
   ship the honest version and list the fault under **Widget faults** in your final answer.
2. **Sample data stays in the past or the present.** When you invent data, no date may fall after today (check the
   date before you write one). A "this month" card holds only days up to today; a forecast is the one place future
   days belong, and it says "Sample forecast".

## The quality bar

A card is done when all of these hold, in both themes, at both widths:

- **It is the right archetype.** A trip is an `itinerary`, a split bill a `bill-split`, a report an
  `exec-dashboard`, plans a `pricing-table`. A primitive tree is only for what no widget does.
- **The answer leads.** A `verdict` (on the widgets that take one), a title, or a first callout says it in one
  sentence.
- **Every number is true and formatted.** Derived from state, in a `stat` with a format, with its currency or unit,
  and the same everywhere it appears.
- **Nothing is cut, clipped, empty or leaked.** No ellipsis eating words, nothing past the card edge, no blank box,
  no NaN, `undefined`, `[object Object]` or raw JSON, no error box.
- **It reads at 360 px.** Tiles wrap, inputs get a row, no sideways scroll.
- **It is real.** Fictional but specific names and numbers, never "Person 1", "Item A", lorem ipsum or a real brand
  with a made-up price. Dates are plausible against today.

The two ways a card fails:

- **Abstract:** an icon, a title, three chips, "Metric 1, Metric 2, Metric 3". Nothing to read.
- **Flat:** one white card, a paragraph, a button. Or a form where an app belongs (a notepad built as inputs, a
  player built as buttons).

The fix for both is the same: the right widget, filled with real fields.

## Files

Paths are relative to this skill's folder (`<skill>` below: where this file lives, for example
`.claude/skills/ripple` or `~/.agents/skills/ripple`).

| File | Read it |
|---|---|
| `references/widgets.md` | Before choosing. Intent to the best widget, with the props it really takes. |
| `references/craft.md` | Before writing, and again when the audit or a screenshot shows a fault. |
| `references/examples/` | Open the closest one first. Five specs that render clean, each with one line on why. |
| `scripts/render.mjs` | Every round. Renders, shoots, audits. `node <skill>/scripts/render.mjs --help` for options. |
| `scripts/build.mjs` | For a kept card (a pocket, a saved widget, a gallery entry). Runs the whole loop below as one script. |

## Setup, once

`render.mjs` needs Playwright and Chromium. It resolves them from the folder you run it in, so run it from your
project (not from the skill folder) and pass the script's path:

```sh
npm i -D playwright && npx playwright install chromium   # skip if the project has them
npm i -D axe-core                                        # optional: accessibility counts
```

**Accessibility is not checked unless axe-core is installed.** Without it `axeViolations` is `null`, not 0, and a
clean round says nothing about labels, contrast or roles. Install it in the project you run from (`npm i -D
axe-core`, or point `RIPPLE_AXE` at an `axe.min.js`) before you call a card accessible, or say it was not checked.

It renders through a Ripple playground. The default is the public one,
`https://ripple-site.pawsites.workers.dev` (it moves to `https://ripple.pocketpaw.xyz` once that domain is live).
To test against your own Ripple build, serve the site and pass `--base` or set `RIPPLE_BASE`. The base must serve
`page-audit.js` (the shared audit `render.mjs` injects); `bun run build:site` writes it, and a deployed site has it
only after a `bun run deploy:site` that includes it:

```sh
# in a ripple checkout
bun install && cd packages/svelte && bun run build:site && bunx vite preview --port 4790
node <skill>/scripts/render.mjs card.json out --base http://localhost:4790
```

## The build loop

Work in this order. Most of the quality is decided in steps 1 and 2, before any JSON.

For a card that will be kept (a pocket, a saved widget, a gallery entry), you can hand the whole loop to
`build.mjs` instead of driving it by hand. It writes, renders, audits, has a critic look at the screenshots,
and stops clean, at no progress, at 4 rounds, at 200k tokens or at 300 s. It never keeps a round that
changed the user's data. Run it from the same folder as `render.mjs`:

```bash
node <skill>/scripts/build.mjs "<the ask>" <outdir> [--base <url>] [--model <alias>]
```

It uses the local `claude` CLI by default (`--model-cmd` swaps in any command). Read `<outdir>/result.json`:
`stopped`, the best round's `faults`, and `widgetFaults` for step 8. The steps below are what it does, and
what you do when you drive the loop yourself.

### 1. Understand the ask

Write one sentence: the question the card answers and who is asking. Then list the facts the card needs: the
numbers, the names, the dates, the choices the visitor makes. Mark which ones the user gave you (fixed, rule 1)
and which you will invent (fictional, plausible, never after today).

### 2. Pick the archetype and the widgets FIRST

- Look the intent up in `references/widgets.md`. **When a data widget fits, the card is that one widget holding
  only data.** Do not wrap it, do not add inputs beside it (it has its own), do not rebuild it from primitives.
- Only when nothing fits, sketch a primitive card: a `card` with sections, each section one idea, the answer first.
  Aim for 25 to 90 nodes.
- Open the closest example in `references/examples/` and copy its shape, not its words.
- Write down the widget(s) and why, in one line, before writing the spec. If you catch yourself hand-building a
  table of products, a list of slots or a set of stat tiles from a report, stop and go back to the map.

### 3. Write the spec

- `{ "version": "1.0", "state": {...}, "ui": {...} }`. The tree is `ui`, never `root` or `body`.
- Node keys in order: `type`, `props`, then `bind` and handlers, then `children`.
- Inputs bind to state; outputs are expressions of state; lists render with one `each`.
- A widget's `bind` sits on the node (next to `props`) and names a path in `state`: `"bind": "pick"` and
  `"bind": "{state.pick}"` both mean `state.pick`. The widget writes it when the visitor acts (a Choose, a tick).
  Leave the key out of `state` unless the card should open with a value already set, or another node reads it from
  the first paint (then seed the empty value, `""` or `[]`). `bill-split`'s key is never seeded.
- Money is `currency: "USD"` plus numbers; every derived number is a `stat` with a `format`.
- Use only widget types and props the manifest lists (`curl -s <base>/manifest.json`). A prop a widget does not
  take is dropped without a word. Leave out defaults.
- Save it as `<name>.json` in a working folder. Keep renders out of the user's source tree unless they asked for
  the files there.

### 4. Render and audit

```sh
node <skill>/scripts/render.mjs <spec.json> <outdir> [--base <url>] [--widths 380,1024] [--themes light,dark]
```

It opens the playground with the spec in the link, shoots only the preview surface at 380 and 1024 wide, light and
dark (`<outdir>/380-light.png`, `<outdir>/1024-dark.png`, ...), writes `<outdir>/audit.json`, prints the same JSON
and exits 0 when clean, 1 when any count is non-zero, 2 on a setup error (no Playwright, no server, bad spec, or a base
with no `page-audit.js`, which means deploying the site; the message says what to run; if Playwright's own Chromium build is missing, `npx playwright install chromium` or
`CHROME_PATH=<a chromium binary>` fixes it; the message lists the builds it found and the one it wanted). Use a fresh `<outdir>` per round (`out/r1`, `out/r2`) so you can compare. Several runs
can go at once; each starts its own browser and writes only to its outdir.

The audit counts, all targeting 0:

| Count | What it means | Usual fix (craft.md section) |
|---|---|---|
| `notRendered` | No box drew, or the preview showed an alert | JSON or schema error; read `specStatus` (1, 6) |
| `themeNotApplied` | The page did not switch theme | Harness problem, not the card |
| `errorBoxes` | "This widget hit an error", an unknown type, a rejected card | Bad prop shape or type (6) |
| `consoleErrors` | Console errors and page exceptions | Usually the same as an error box |
| `overflow` | Card scrolls sideways, an inner box scrolls sideways, or an element pokes past the card | Wrap tiles, shorten, give a row (2). A scroller the widget designed (a chip row, a table of 4+ items) may be accepted; it still counts, so name it in your answer |
| `clippedText` | Words cut by an ellipsis, overflow or a line clamp; an input whose value is wider than its box; svg text past its svg | Shorten at the source, not with CSS (2) |
| `emptyContainers` | An in-flow box of 40 px or more with nothing in it | Real data or remove it (4) |
| `badText` | NaN, undefined, null, Infinity, `[object Object]`, `{state.` unevaluated, raw JSON | Prop names and formats (5, 6) |
| `axeViolations` | axe-core violations, or `null` when axe-core is not installed (`axeHint` says how) | Labels, contrast, roles |

Each shot in `shots[]` lists the offenders with a locator (`widget=...`, the tag and class, the text), and
`surfaceWidth` says how wide the card really was (about 322 at a 380 viewport, 623 at 1024: the playground's
chrome takes the rest).

A pass is necessary, not sufficient. Gaming it is a bug: clamping text, hiding a box, blanking a value or changing
the data (rule 1) to make a count go to 0 makes the card worse.

### 5. Look at the screenshots

Open every PNG. The audit cannot see canvas charts, 3D models, contrast inside a drawing, wrong hierarchy, the same
number shown two ways, dates in the future, or words that contradict the data. Read each shot through the lenses
below, in order, and write down every fault before fixing any.

### 6. Fix

Fix the cause at the lowest layer you own: the widget choice before the props, the props before the words.
Prefer deleting a hand-built section in favour of a widget prop over adding more nodes. Never fix a cut word with
`overflow: hidden`.

**Never fix by editing the data.** When the only way to make a widget look right is to change a number, a date, a
target or a name, the fault is in the widget. Keep the data, try a different widget or layout, and if nothing
works, leave it and write it down for the **Widget faults** section.

### 7. Repeat, and stop

Re-render after every fix round. **Stop after a clean round** (every count 0, or only scrollers the widget designed (craft.md section 2), and no lens finds anything the spec
can fix at either width in either theme; faults inside a widget go to the Widget faults list and do not keep the
loop going) **or after 4 rounds.** If round 4 still has faults, stop anyway.

### 8. Answer

Give the user the final spec (or its path) and the 380 light screenshot, then these sections:

- **Widget:** the widget(s) and the one-line reason.
- **Rounds:** how many, and the last audit counts.
- **Sample data:** what you invented (so the user can swap in real values).
- **Widget faults:** every fault the spec could not fix without breaking rule 1, with the widget, the width and
  theme, the shot that shows it, and what the widget would need. Write "none" when there are none. These go back
  to Ripple as widget fixes; they are not your failure.

## Review lenses, in this order

Run them one at a time over all four shots. One lens, one pass: a reviewer looking for everything finds less.

1. **Archetype.** Is this the widget the map names for this ask? Is anything hand-built that a widget does? Are
   controls duplicated?
2. **The answer.** Can you say the card's answer after one second on the 380 shot? Is it at the top?
3. **Data truth.** Is every value the user gave you still exactly what they gave? Do the numbers agree with each
   other and with the words? Same value, same rounding, everywhere? Any placeholder names, identifiers as labels,
   brands with made-up facts?
4. **Dates.** Is any invented date after today? Do weekdays match their dates? Does "this week" or "this month"
   hold only days up to today?
5. **Numbers.** Every number formatted, with currency or unit, sensible decimals, no NaN or dash where a value
   belongs.
6. **Layout at 380.** Wrapping, nothing cut, nothing past the edge, inputs on their own row, no 4-up tiles.
7. **Hierarchy.** One heading per section, labels quieter than values, one primary action, most important first.
8. **Density.** Any dead region, empty box, a chart that is mostly blank, or the opposite: a wall of equal-weight
   text?
9. **States.** What does it show with no rows, the longest name, the biggest number, the last step, items ticked?
   Render a worst-case copy of the spec too (`card-ticked.json`). Changing state in a preview copy is not a data
   change; the spec you hand over keeps the user's data.
10. **Both themes.** Anything that vanishes or glares in dark or in light (models, drawings, tinted panels)?
11. **Interaction.** Inputs bound, outputs derived, a validate before any send, book or approve, only real actions.

## When to stop and say so

- The right widget does not exist: build the primitive card, finish the loop, and name the missing widget under
  Widget faults.
- A fault is inside a widget (it truncates at 360, it stacks tiles one per row, it ignores a prop): the spec cannot
  fix it without bending data; report it under Widget faults with the shot that shows it.
- `render.mjs` exits 2: read its message. It names the install command, the server it could not reach, or the
  site deploy it needs (a base with no `page-audit.js`).

## Known limits

- The audit sees one rendered state: the first. Steps, tabs, hover and open dialogs are eyes-only unless you render
  a copy of the spec seeded in that state. Two ways to seed it: a widget prop that picks the state
  (`comparison-layout`'s `chosen` or `defaultView`, a tab's initial value), or `state` set to the value the widget
  would write (the bind key, a ticked item). Save it as a separate preview file (`card-chosen.json`); changing state
  in a preview copy is not a data change, and the spec you hand over keeps the user's data.
- The shot widths are viewport widths; the card itself is narrower (see `surfaceWidth`).
- `chart` draws on canvas and `model-viewer` in WebGL: their insides are eyes-only.
- The public playground runs the latest released Ripple. A widget fix that is not released yet only shows against
  a local build (`--base`).

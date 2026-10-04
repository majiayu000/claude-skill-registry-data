---
name: jsgui3-verify
description: How to prove a jsgui3 SSR + client-activation app actually works, and the traps that make it look like it works when it does not. Use this skill whenever you change, review, or debug anything under src/ui/server/*/controls/ or any jsgui3 Control — before claiming a change works, when a control renders empty or stale, when adopting a stock jsgui3 control, or when a green test suite disagrees with what the page does. Also use it before writing "verified" in a commit message or ledger row about UI work.
---

# Verifying a jsgui3 app

jsgui3 renders on the server and **reattaches** in the browser. That seam is where
this project's UI bugs live, and it has a specific property that makes it
dangerous: **failures are silent and look like styling.** A control that lost its
data renders — it just renders empty, or stale, or blank-but-correctly-shaped.

Every UI defect this project has shipped was a *verification* failure, not a
coding failure. The code was plausible; the check was too weak to catch it.

## The rule that would have prevented all of them

> **Measure the runtime. Do not infer it from the source.**

In one session an agent read jsgui3's constructors and made three confident
claims about reattachment. All three were later measured **false**, and two had
already been written into a defect report for another team. The measurement that
settled them took about two minutes.

Reading a constructor and predicting what happens at runtime is **inference**.
Loading the page and looking is **measurement**. Say which one you did.

## The reattachment contract (measured, 2026-07-30)

What the client gets back, verified in a live browser — not read off the source:

| Restored | Not restored |
|---|---|
| The full control tree: `content._arr` repopulated, `.parent` set, descendants reachable by a plain recursive walk | Anything assigned to `this` during compose — `this.grid = grid` is **undefined** in the browser |
| `_ctrl_fields`, hydrated as real properties (a reattached `Panel` has `content_container`; a `Data_Grid` has `table`) | `data.model` — every reattached control gets a fresh empty `Data_Object` |
| Scalars the server put in `this._fields` (serialized to `data-jsgui-fields`) | Text nodes — raw text in SSR markup is in the DOM but absent from `content`, and `clear()` destroys it |
| DOM events, mutation API (`add()`, `clear()`, `add_class()`), mixins | A stock control's `columns` / `rows` unless it opted in (see traps) |

The mechanism: reattachment constructs every control down the **`spec.el`**
path, which **skips compose entirely**. That single fact explains most of the
table. `control-enh.js: pre_activate_content_controls` does the restoring.

Reach a collaborator by **walking the tree** (`.parent` upward, `content._arr`
downward, matching `__type_name`). Do not build a parallel registry of marker
attributes and `document.querySelector` — that was tried here, on the false
belief that the tree was flat, and deleted.

## The recipe

1. **Restart the server.** `Server({Ctrl})` publishes the SSR HTML and the bundle
   **once, at boot**. Editing a control and reloading the page shows you the old
   build. Almost every "my change did nothing" moment is this.
2. Load the page, wait for activation to settle (~1.5–2.5s), then assert.
3. **Console must be clean.** Check it explicitly. A swallowed error is how a
   dead feature survives for cycles.
4. Assert on **content**, not shape. See below.
5. Check the invariants for this app: `/tech/*` still 302s, `#node=` / `#branch=`
   deep links still select and scroll, SSR renders the board without activation,
   SSE `activity` patches / `cards` re-applies.

## Proof techniques that actually discriminate

**To prove a list repainted — marker-then-refresh.**
"It still looks populated" proves nothing; the SSR markup also looks populated.

```js
document.querySelector('SELECTOR').setAttribute('data-stale','1');
document.querySelector('[data-ps-refresh]').click();
// after the refresh: 0 elements with [data-stale] === it genuinely rebuilt
```

**To prove content is right — read it, do not count it.**
A stock `Chip` was given `spec.text` when it reads `spec.label`. It rendered the
correct *number* of correctly-shaped pills, all blank, for two cycles. The check
that missed it was `chips: 2`. The check that caught it read
`chips.map(c => c.textContent)`.

**Assert DOM properties, not `textContent`.** `textContent` counts hidden nodes,
which once produced a false "the pill appeared".

**For exactly-one-of behaviour, do it twice.** Select A, select B, then count.
One selection proves nothing about exclusivity — and the two paths (mouse and
hash/deep-link) can differ. They did: the mouse path deselected correctly while
the hash path did not, because it wrote `ctrl.selected = true` instead of
calling `action_select_only()`.

## Trap list

- **An SSR'd `Data_Grid`/`Data_Table` needs `persist_activation_state: true`.**
  Without it the reattached grid has zero columns and renders the right *number*
  of rows with **no cells** — which reads as a CSS bug. `aria-colcount` visibly
  drops from N to 0. A grid composed at **runtime** does not need it.
- **Check a stock control's spec before passing anything.** `Chip` takes `label`,
  not `text`. Read the `.d.ts` or the constructor; the library's specs are not
  guessable and the failure is silent.
- **Controls composed into an already-activated parent never activate.** Call
  `pre_activate()` **then** `activate()` on the new subtree. `pre_activate` is
  what installs the vdom→DOM sync listener — activate alone leaves the control
  live but deaf, so later `add_class()` and attribute writes silently do nothing.
- **Survey before building.** jsgui3 ships ~155 controls and ~48 mixins. Proposing
  to build `Panel`, `Chip`, `Badge` or `Button` has happened here more than once.
- **Stock controls carry their own theme.** `Key_Value_Table` and `Chip` ship
  light-on-white and read as holes cut in a dark page. Check computed styles, not
  just that the control rendered.
- **The deep relative requires are deliberate.** `../../../../../../../jsgui3-client`
  points at the sibling repo; `require('jsgui3-client')` resolves to an older
  `node_modules` copy. Do not "tidy" them into package specifiers.
- **CSS lives on the control** as `Ctrl.css = \`…\`` before `module.exports` — the
  documented `static css` hook. The bundler collects it from the bundle text.

## Reporting

State the evidence kind for every claim: **measured** (ran it, saw output),
**source-read** (read code, reasoned), **inferred** (weaker). If a check was not
run, do not imply it was — read the actual output before writing a number into a
commit message. "21/21 probes" was once written when the run said 19 pass, 1
fail, 1 skip.

If a claim is refuted later, record it **as refuted**, with the reason. A
withdrawn claim kept on the record is worth more than a plausible one quietly
deleted.

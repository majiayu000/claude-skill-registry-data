---
name: pr-feedback
description: Format review findings as a flat numbered list of issues, each locatable and phrased so the fix is obvious. Use when when the user asks to re-list, tighten, or restyle review findings.
---

Governs **how findings are written**, not how they are found. Run whatever review the task calls for, then report it in this shape.

A claim about how two things relate is checked in the code before it is written. A wrong mechanism in the lead sentence costs the reader more than a vague one.

## Shape

One flat numbered list. Nothing else — no `## Bugs` / `## Simplification` / `## Tests` headings, no severity labels, no summary paragraph before or after. Order by importance: real defects, then spec mismatches, then simplifications, then tests, then tooling/stories.

Each item is one short paragraph:

1. **Bold lead sentence** naming what is wrong, in plain words.
2. `file.tsx:LINE` references for every unnamed place the reader must open (a prop, a docblock, a wording). A uniquely named symbol (function, type, constant) is found by its name; skip its line reference.
3. One or two sentences of mechanism — enough that the reader sees the failure without re-deriving it.
4. A fix only when it isn't obvious from the problem, and always general: a direction ("Consider renaming X", "reject these fields, drop them on load, or move them onto the modes"), never the specific change. Phrase it as "Try X" or "Consider X". When the fix is obvious, state the problem as its cause instead ("the fixture seems not regenerated with the script after changing the JSON or mapper", not "Always regenerate the fixture").

## Vocabulary

Plain language over jargon. Name the mechanism rather than the technique: "the chart redraws far more often than the screen updates" beats "no rAF-debounce on the RO callback". Introduce a technical term only after the plain description, and only if the reader needs it to act.

The item must convey both what currently happens and what should happen — woven into the prose. Never split an item into labelled `Now:` / `Should:` halves.

## Address the author directly

Findings are written *to* the person who will fix them. Never "suggest X" or "it is suggested" — there is no third party to suggest to. Use "Try X", "Drop the numbers", "Move the check into the observer".


## Cut

- Trailing consequence clauses the reader already inferred — "…so Plotly redraws the lines too", "The export exists only to feed it", "hiding the one thing the story demonstrates".
- Editorial flourish — "this is the tell", "worth noting", "the one to look at".
- Session state — "already changed in your working tree", "as I mentioned above", and your own tool or access failures ("git.iter.org redirect-loops from here", "could not fetch the header").
- Rationale for the fix — "since the distinction only lands when they are stated together", "so they need writing as one set". The direction stands without an argument for it.
- Figurative language — "a dataset riding in either envelope", "the distinction doesn't land". Say it literally.
- Parallel clauses enumerating the places — "No X entry, no Y entry, and the Z entries just say…". Name the set and its size instead: "the four terms".
- Restating the reference in prose after giving it.
- Evidence the fix itself surfaces — the field-by-field diff of a stale generated file, the list of tests or call sites affected. Name the mismatch, then stop.
- Fixes the problem already implies, and specific fixes of any kind (exact props, layouts, replacement names).
- Code snippets and call arguments when naming the function is enough (`use store.setLeafValue()`, not the full call).
- Cross-references between items ("this also fixes item 3").

WRONG:
> **5. Reference selection could use the existing leaf setter.** `model-store.ts:791` only exists because the `*_ref` fields are optional (`model-schema.ts:165-167`). If the backend always sends all three refs, make them required and write through the leaves with `store.setLeafValue(ref.id, option.id.value)` and `store.setLeafValue(ref.name, option.name.value)`. This also keeps the baseline from item 3.

CORRECT:
> **5. Reference selection could use the existing leaf setter.** If the backend always sends all three refs, the refs could be required and written through `store.setLeafValue()`.

WRONG:
> **1. The fixture is written by hand.** `mocks/pcs/pcs-with-magnetics-controller-config.model.ts` doesn't match the JSON. Always regenerate the fixture with the script after changing the JSON or the mapper.

CORRECT:
> **1. The fixture seems not regenerated with the script after changing the JSON or the mapper.** `mocks/pcs/pcs-with-magnetics-controller-config.model.ts` says "Do not hand-edit" but doesn't match `pcs-with-magnetics-controller-config.json`.

WRONG:
> **6. Names still say "main settings".** Rename `updateMainSettingSelection` (`model-store.ts:791`) to e.g. `setControlReference`, and `CONTROLLER_MAIN_SETTING_FIELDS` (`fields.ts:17`) to e.g. `CONTROL_REFERENCE_FIELDS`.

CORRECT:
> **6. Names still say "main settings".** Consider renaming `updateMainSettingSelection` and `CONTROLLER_MAIN_SETTING_FIELDS`. The stale wording also sits in `fields.ts:15`.

WRONG:
> **9. The `FitParent` story only lets you drag width.** `Plot.stories.tsx:93` ships `resize: "horizontal"`, hiding the one thing the story demonstrates — `resize: "both"` (already changed in your working tree). The docblock at line 77 still says "as its width changes"; widen it to size.

CORRECT:
> **9. The `FitParent` story only allows to drag width.** `Plot.stories.tsx:93` — try `resize: "both"`. The docblock at line 77 still says "as its width changes".

WRONG:
> **7. `ResizeObserverMock` is duplicated word for word** — `Plot.test.tsx:11` and `PlotWithTraceDialog.test.tsx:13`.

CORRECT:
> **7. `ResizeObserverMock` is duplicated.** `Plot.test.tsx:11` and `PlotWithTraceDialog.test.tsx:13`.

WRONG:
> **8. One test can never fail.** `WaveformEditor.test.tsx:221` checks the component passes `WAVEFORM_EDITOR_PANEL_DIMENSIONS`, a constant exported from the component's own file. The export exists only to feed it.

CORRECT:
> **8. One test can never fail.** `WaveformEditor.test.tsx:221` checks the component passes `WAVEFORM_EDITOR_PANEL_DIMENSIONS`, a constant exported from the component's own file.

WRONG:
> **1. `CONTEXT.md` doesn't define either term this PR is about.** No `Dataset` entry, no `Configuration` entry, and the `sup-dto` / `psps-dto` entries just say "interchange encoding" — nothing about them being envelopes, or about a dataset riding in either one. Four coordinated entries are needed, since the distinction only lands when they are stated together. Worth checking the wording against `psps_interface.h` — `git.iter.org` just redirect-loops from here.

CORRECT:
> **1. `CONTEXT.md` doesn't define the four terms this PR turns on.** `Dataset` and `Envelope` are missing, and `sup-dto` and `psps-dto` need updating to relate to them. Confirm the wording against `psps_interface.h`.

## Merge

Two observations with the same root cause are one item. A fixed panel height and the row-wrap that multiplies it are one layout finding, not two.

## Short message form

When the findings are a message to post (a PR comment, a chat reply) rather than a review report, compress further:

- Open with one short line, e.g. "Some notes after review:". No closing line.
- Plain numbered items, no bold lead.
- Each item: what is wrong + where (file/line), then at most one short sentence of direction ("could be dropped in this PR", "will need to be updated").
- Drop the mechanism — the reader opens the reference. Drop consequences ("so after this merges the analysis runs without a token"), timing and coordination ("landing before or together with this PR"), and the reason behind a suggestion ("CI now runs the E2E suite on each PR").

WRONG:
> 1. **psps-deploy's Sonar stage still depends on the removed `sonar.login=$SONAR_LOGIN` line.** `build_sonar_report.sh:11` fills that placeholder with `sed`, so after this merges the release analysis runs without a token. Worth a separate change in psps-deploy, landing before or together with this PR, that passes the token to the scanner itself.
>
> 2. **`.husky/pre-push` still runs Cypress on every push.** CI now runs the E2E suite on each PR, so the local Cypress step could be dropped in this PR.

CORRECT:
> Some notes after review:
> 1. psps-deploy reads the removed `sonar.login=$SONAR_LOGIN` line (`build_sonar_report.sh:11`), so that will need to be updated.
> 2. `.husky/pre-push` still runs Cypress on every push. The local Cypress step could be dropped in this PR.


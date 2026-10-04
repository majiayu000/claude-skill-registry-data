---
name: interaction
description: "Build the curated interactive SET the Editor approved: the ONE narrative-bound hero centerpiece (an explorable/scrollytelling that makes the reader PRODUCE the lead finding) PLUS the ranked supporting playgrounds — each bound to a distinct finding — to the same three-layer-number standard, plus animation/transition craft. Consumes editor.json.interactives + imagineer.json + the Analyst's client_model. Outputs interaction.json (centerpiece + supporting[] + playtest_handoff) for the Programmer; may reach back into the Editor's spine when the lead finding should be hands-on."
argument-hint: [PROJECT_DIR]
allowed-tools: Bash(*), Read, Write, Edit, Glob
---

# Interaction Engineer

Your job is the single thing that lifts a competent multimodal article to **Pudding-grade**: turn the story's contestable claims into **playgrounds the reader operates** — they run the model / guess / enter their own value, and the finding becomes something they *produced*, not just read. You own the hero **centerpiece** interaction **AND the curated supporting set the Editor approved** (`editor.json.interactives`) — one earned hero plus any number of supporting playgrounds, each bound to a distinct finding — plus scrollytelling + transition craft. You do not redo the Designer's per-section visuals, and you build **nothing the Editor didn't curate**.

## Setup
- `PROJECT_DIR` = first argument.
- Read: `editor.md` + `editor.json` (the spine + **`editor.json.interactives`** = the curated `hero` + ranked `supporting[]` you build — the binding curation, not a hint), `imagineer.json` (the candidate concept pool; each `supporting`/`hero` entry's `concept_ref` points at an `img_xx` here, with its `archetype`/`reader_produces`/`feasibility`/`sketch`), `analyst.json` (findings + the **`client_model`**), `designer.json` (theme + per-section plan), `detective.json` (context). If `editor.json.interactives` is absent (older spine), fall back to the Editor's prose centerpiece nomination and build the hero only.
- Read the playbook **[`../../frontend-design-pro/references/interaction_playbook.json`](../../frontend-design-pro/references/interaction_playbook.json)** in full — `craft_principles`, `centerpiece_doctrine`, `universal_engine`, `recipes`, `portability_rules`. Follow it.
- Read the role-local **[`references/interaction_recipes.json`](references/interaction_recipes.json)** for harvested patterns this role owns that extend the shared playbook — including the **E1 interactive-hero verify-coexistence** recipe (the highest-value reusable rule: an interactive element that COEXISTS with the Verify layer over a provenance container — role=link sub-targets out of the Verify allow-list + every feature handler early-returns under `verify-on` + feature code never `stopPropagation`).
- Output: `PROJECT_DIR/interaction.json`. You MAY also `Edit` `editor.json`/`designer.json` to mark the centerpiece slot.

## Step 1 — Confirm the hero + enumerate the approved supporting set
**The hero centerpiece.** Use the Editor's `interactives.hero` (or, if absent, its prose-designated centerpiece finding). If none was designated, or a stronger one exists, **nominate it**: the one contestable claim the reader should produce themselves. This is your single licence to touch the Editor's spine — record the change + why in `interaction.json.spine_change`.

**The supporting set.** Take `editor.json.interactives.supporting[]` as your build list — each entry names a `finding` (a **distinct** `ana_xx`), a `purpose`, a `section`, an `archetype`, and a `concept_ref` into `imagineer.json`. Build **only** these; do not invent a playground the Editor didn't curate, and do not drop one without a recorded reason. If a curated entry fails the `earned_test` below (its finding duplicates the hero or another supporting, or it can't be made buildable/feasible), don't silently build it weakly — flag it back rather than ship a duplicate or a dead control.

Pick the mechanism for each (hero + every supporting) (interaction_playbook → `interaction_taxonomy`):
- **explorable_recompute** — DEFAULT when a `client_model` exists (model/derived headline): the reader changes an input and the output re-derives live.
- **guess_then_reveal** (data-bound) / **personal_input** — for "you assume X but actually Y".
- **scrollytelling** — when the argument is a sequence/funnel.

## Step 2 — Design the manipulate → recompute → payoff loop (for the hero AND each supporting)
Specify this loop **for the hero and for every approved supporting playground**. For each: the reader's **controls** (sliders/dropdowns/guess); **what recomputes** (which `client_model` function + inputs, or the `data_table` it reads); the **live output** (which chart updates + how it animates); the **payoff** (the realization). A supporting playground's loop is the same standard as the hero's, scoped to its own distinct finding.
- It must land **at or before the reveal** — the reader's action IS the reveal, not an illustration after the prose already gave the answer.
- **Play first — minimize reading before the control.** The manipulable control (slider/dropdown/guess input) must be reachable with MINIMAL reading: place it EARLY in the centerpiece section, **before** long expository prose or any param/specimen/"how it works" block, so the reader can manipulate it immediately and PRODUCE the finding. High entry friction (a paragraph + a params block before the reader reaches the slider) is a craft failure — front-load the control, keep instructions to a one-line affordance, and let any longer explanation follow the play. The payoff still lands at/before the reveal.
- **At rest**, show the exact published numbers (from the analyst `data_table`/forecast); **on interaction**, recompute via the `client_model` and show the delta ("your scenario vs the model").
- ONE earned **hero** centerpiece **+ the approved supporting set, each earned** — restraint is "every playground earns its place," not "only one." A playground earns its place by the **`earned_test`**: it is bound to a **distinct** finding the reader produces/feels (no two share one) **AND** it passes playtest (control → state → readout actually fires) **AND** it is not a duplicate of another. Build **NOTHING** the Editor didn't curate; an unearned widget is a pile, not abundance. Specify graceful degradation (page still makes its point if JS fails) + keyboard accessibility **for every element**.
- **Engagement floor (now hard).** On a resolved descriptive topic (`is_visual:false AND is_computational:false`) the engagement floor is hard — shipping zero interactives now blocks at the contract gate (`missing_engagement_floor`) unless an honest `engagement_blocker` is recorded. A simple `personal_input`/`sortable` on a descriptive finding (where the reader lands, sorting the catalog themselves) is the canonical satisfier; build the one the Editor curated rather than leaving the page interaction-free.

## Step 3 — Scrollytelling + transitions
If the spine is sequential/funnel, spec a sticky-graphic scrollytelling using the playbook engine (`position:sticky` + IntersectionObserver + a `steps[]` of functions). Otherwise spec the key animated transitions for the centerpiece (D3 transitions; never hard pops). For transition timing/easing, use the motion tokens in **[`../../frontend-design-pro/references/motion.json`](../../frontend-design-pro/references/motion.json)** rather than hardcoding durations.

## Step 4 — Verify the whole set is buildable
For the hero **and every supporting** explorable, confirm the `client_model` exists and works — `node` a quick call (e.g. `simulate()`) so the spec you hand the Programmer is real. Note the exact functions + input shape per element. The Imagineer's `feasibility` is a hint, not a guarantee — re-check anything you'll actually build; if a curated supporting entry won't run (model missing/errors), flag it back rather than ship a dead control. Then write the `playtest_handoff` block (below) so the Playtester can drive every built id.

## Output — `interaction.json`
Keep `centerpiece` (the hero — unchanged shape, `id: "int_01"`); ADD a sibling `supporting[]` array (one entry per approved supporting playground) and a `playtest_handoff` block listing **every** built id for the Playtester.
```json
{
  "centerpiece": {
    "id": "int_01", "based_on": ["ana_xx"], "section": "edt_xx",
    "mechanism": "explorable_recompute",
    "reader_produces": "the finding the reader generates themselves (e.g. 'nudge a team's Elo and watch the champion odds re-derive')",
    "controls": ["range slider: team Elo ±, dropdown: which team", "button: re-run N sims"],
    "client_model": { "file": "code/client_model.js", "fn": "simulate", "inputs": "(nSims, {team: deltaElo})" },
    "at_rest": "show published champion odds (Argentina 26.3% …)",
    "on_interact": "recompute via client_model; animate bars; show delta vs published",
    "payoff": "the reader sees the headline is contingent — they produced it",
    "placement": "at/before the reveal in edt_xx",
    "degradation": "static published chart if JS off", "a11y": "keyboard-operable controls"
  },
  "supporting": [
    {
      "id": "int_02", "role": "supporting", "concept_ref": "img_02", "based_on": ["ana_05"],
      "section": "edt_05", "mechanism": "guess_then_reveal",
      "reader_produces": "guess the gap, feel the correction when the real value lands",
      "controls": ["slider: your guess"],
      "client_model": null,
      "at_rest": "static real-value bar from ana_05",
      "on_interact": "draw guess+real bar from the data_table",
      "payoff": "the correction lands — the reader's intuition was off",
      "degradation": "static real-value bar",
      "a11y": "keyboard slider with label",
      "verify": { "kind": "computation", "recompute": "data_table", "three_layer": true }
    }
  ],
  "scrollytelling": null,
  "transitions": ["champion bars: D3 transition 600ms on recompute"],
  "spine_change": null,
  "playtest_handoff": {
    "build_ids": ["int_01", "int_02"],
    "per_id": {
      "int_02": {
        "expect_control_reachable": true,
        "expect_recompute": true,
        "readout_selector": "[data-play-out=int_02]",
        "oracle": null,
        "degradation_path": "static real-value bar from ana_05"
      }
    }
  }
}
```
- `supporting[]` — one object per approved supporting playground. Each carries its own `id` (`int_NN`), `role: "supporting"`, `concept_ref` (the `img_xx`, or `null`), a **distinct** `based_on` (`["ana_NN"]`), its `section`, `mechanism`, `reader_produces`, `controls`, `client_model` (or `null`), `at_rest`, `on_interact`, `payoff`, `degradation`, `a11y`, and a `verify` block (`kind`: `computation`|`fact`; `recompute`: `client_model`|`data_table`; `three_layer: true`). `[]` when only the hero is built.
- `playtest_handoff` — **REQUIRED**: `build_ids` lists EVERY built id (`centerpiece` + every `supporting[].id`); `per_id` gives the Playtester each element's expectations (`expect_control_reachable`, `expect_recompute`, the non-provenance `readout_selector` = `[data-play-out=int_NN]` or `null`, an `oracle` if the recompute has a known target, and the `degradation_path`).

**Tell the Programmer** to tag **each** built element `data-int="int_NN"` + `data-ana="ana_NN"` for traceability (the hero is `int_01`; each supporting its own `int_NN`), and optionally `data-play-out="int_NN"` on that element's live readout (a **non-provenance** hook the Playtester reads to catch chart-only changes the whole-container innerText diff misses — it is in no validate tuple/schema). Build only the curated set; tag nothing the Editor didn't approve.

Done when the Programmer can read `interaction.json` and build the curated SET — the hero centerpiece (the reader produces the lead finding, powered by the `client_model`) plus every approved supporting playground, each bound to a distinct finding and earning its place — with a `playtest_handoff` the Playtester can drive end to end.

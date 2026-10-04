---
name: imagineer
description: "Fan out MANY candidate interactive concepts from the data + narrative — the ideation pool the Editor curates a hero + supporting set from. Deliberate over-generation: one concept per finding worth making hands-on, each declaring its archetype, purpose, what the reader produces, and an honest feasibility (node-checked against the Analyst's client_model). Builds NOTHING on-page — img_xx concepts are internal and never reach HTML. Outputs imagineer.json after the Analyst, before the Editor."
argument-hint: "[PROJECT_DIR]"
allowed-tools: Bash(*), Read, Write, Glob
---

# Imagineer

Your job is **ideation, not construction**. You read the findings and the narrative and you fan out a wide pool of candidate *interactive concepts* — ways a reader could **produce** a finding (run the model, guess-then-reveal, enter their own value, play the odds) instead of just reading it. You deliberately **over-generate**: propose one concept for every finding worth making hands-on, even the marginal ones. The Editor curates this pool down to a hero + a ranked supporting set; the Interaction Engineer builds only what the Editor keeps.

You build **nothing on the page**. Your `img_xx` ids are **internal** — a planning vocabulary the Editor reads. They never reach the HTML, are tagged on no element, and are added to no provenance tuple. Your one job is to make the candidate pool rich, honest about feasibility, and bound to real findings.

## Setup
- `PROJECT_DIR` = first argument.
- `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story-pro/imagineer`).
- Read `PROJECT_DIR/analyst.json` — its `items` give you the findings (`ana_xx`: `label`, `content`, `data_table`, and any **`client_model`**). The `client_model`s are what make `explorable_recompute` concepts feasible; note which findings carry one.
- Read `PROJECT_DIR/detective.json` — for the shared **[`topic_profile`](../references/topic_profile.json)** (the S3 classifier: `is_computational` / `is_visual` / `tags`) that gates how hard you fan out.
- Read `PROJECT_DIR/editor.md` + `editor.json` **if they already exist** (the spine — which finding is the lead, the section order); they may not yet, since you usually run before the Editor. When absent, work straight from `analyst.json` and mark the lead candidate yourself.
- Output: `PROJECT_DIR/imagineer.json` (write incrementally).

## When to run (and when to stay light)
Key this off the shared **[`topic_profile`](../references/topic_profile.json)** (the same two-condition default the Cinematographer uses, read from `detective.json`; if absent, classify the dataset yourself the same way and record it). The pool's size should track what the data can actually support:

- **Fan out widely** when **`is_computational` is true** (the headline is a reproducible calculation — a probability, rate, ranking, model output, aggregate): these are the findings a reader can re-run, so `explorable_recompute` / `tune_the_assumption` / `scored_quiz` concepts are all on the table. Propose several.
- **Fan out moderately** when **`is_visual` is true** but the lead is not computational: `guess_then_reveal` / `personal_input` / scrollytelling concepts still let the reader produce a finding without a model.
- **An abstract topic is still a first-class flagship target** — read **[`../../frontend-design-pro/references/abstract_excellence.json`](../../frontend-design-pro/references/abstract_excellence.json)** to choose the engagement + narrative moves before deciding how hard to fan out. When **`is_computational` is true but `is_visual` is false** (finance, web-analytics, elections, pure statistics, benchmarks), the page wins on insight + transparency, not photos: the runnable-verify layer FAVORS these topics, and an `explorable_recompute` / `tune_the_assumption` on the computed headline is strong hero material — propose them. Reach also for `personal_input` "where you land" whenever the data has rows the reader fits into (income, age, region, score).
- **Engagement floor (purely-descriptive sub-case) — now a HARD floor** — when **BOTH `is_computational` and `is_visual` are false** (no computed headline to re-run, no imagery): you **MUST propose ≥1 simple engagement-floor concept** — a `personal_input` / `personal_input_where_you_land` or a `sortable` (`sortable_table`) (a `scored_quiz` also qualifies) on a **descriptive** finding (where you land in the distribution, sort the catalog yourself) — so the Editor isn't forced to ship an empty/charts-only page. This is NOT forced decoration: the restraint still holds — do not force a concept onto a finding with no reader-producible payoff. The ONLY sanctioned way to ship **zero** interactives on a resolved descriptive topic is for an explicit `engagement_blocker` reason to be recorded (e.g. the data has no row a reader fits into AND no entity set to sort). You are the one who **proposes** that blocker, but the contract gate (`missing_engagement_floor`) reads the honored reason **only** from `interaction.meta` (NOT from your `imagineer.json`) — so your recorded reason is **advisory**, and the Interaction Engineer must **propagate** it into `interaction.meta.engagement_blocker` (alias `engagement_floor_reason`) for the gate to honor it. "Ship zero with no recorded blocker" is **no longer allowed**: it hard-errors at the contract gate (`missing_engagement_floor`). (`privacy_sensitive` topics are auto-exempt.) When you propose the blocker, note in **one** item why the pool is near-empty (a clean editorial column + the signature annotated chart is acceptable) so the Editor sees the omission is intentional, and STOP.

Record the resolved `is_computational` / `is_visual` in `meta` so the Editor sees the gate you applied. On a resolved descriptive topic where you propose shipping zero interactives, also record an **advisory** copy of the escape field in `meta` — `engagement_blocker` (the honest reason no reader-fits-in lever exists; the alias `engagement_floor_reason` is also read here) — as your proposed blocker for the downstream roles. This recorded copy is advisory only: the contract gate (`missing_engagement_floor`) does NOT read it from `imagineer.json` — it reads the honored reason from `interaction.meta`. The Interaction Engineer must write the honored `engagement_blocker` / `engagement_floor_reason` into `interaction.meta` for the gate to pass.

## Step 1 — Walk the findings, propose a concept per hands-on opportunity
Go through every `ana_xx`. For each finding a reader could plausibly **produce** rather than read, draft a candidate `img_xx`. Be generous — a marginal concept the Editor cuts costs nothing; a finding you never imagined can't be curated. Pick the `archetype` from the interaction taxonomy:

- **explorable_recompute** — the finding has a `client_model`: the reader changes an input and the output re-derives live. The strongest hero material.
- **tune_the_assumption** — the reader sets an assumption delta (a slider) → the model re-runs against the cached published baseline → deltas re-render. Generalizes a model-output headline.
- **guess_then_reveal** / **scored_quiz** — for "you assume X but actually Y": the reader commits a guess, then the real value (from the `data_table`) lands.
- **personal_input** — the reader enters their own value → pull their row / percentile from the `data_table` → "you're here."
- **playable_game** — the lightest self-contained loop that makes the finding *felt* (e.g. repeatedly choosing under the data's real odds, watching the aggregate converge to the published rate).
- **scrollytelling** — when one finding is a sequence/funnel the reader steps through.

Mark exactly the concepts that could carry the whole piece with `hero_candidate: true` (usually the explorable on the lead finding); the rest `false`. The Editor makes the final hero call.

## Step 2 — Bind each concept to a real finding + an honest feasibility
Every concept must be **earnable**, not aspirational:
- `finding` = the **single** `ana_xx` the reader produces. (Two concepts may target the same finding — that's fine here; the Editor's curation forbids two *built* supporting elements sharing one finding, but the ideation pool may explore alternatives.)
- `needs.data_table` = the `ana_xx` whose `data_table` supplies the at-rest published numbers.
- `needs.client_model` = the exact `code/<file>.js:fn` reference when the archetype recomputes, else `null`.
- `reader_produces` = one line on what the reader *generates* (not what they see) — "nudge a team's Elo, watch champion odds re-derive", not "a chart of odds."
- `sketch` = a one-line build hint (controls → output): "slider(Elo)+dropdown(team)+button -> animated bars."

## Step 3 — node-check feasibility (honest, not hopeful)
For any concept whose `needs.client_model` is set, **confirm the model is real and runnable** the way the Interaction Engineer does (`interaction/SKILL.md` Step 4): `node` a quick call to the referenced function with a plausible input shape, e.g.

```
node -e "const m=require('PROJECT_DIR/code/client_model.js'); console.log(m.simulate(200,{}))"
```

Set `feasibility`:
- **high** — the model runs and returns the expected shape (or, for a no-model archetype, the `data_table` is present and chart-ready);
- **medium** — plausible but needs a wrapper the Analyst hasn't emitted, or the `data_table` needs reshaping;
- **low** — the model errors, is missing, or the data can't support the concept honestly.

Don't inflate. A `low` concept the Editor sees and cuts is better than a `high` claim the Builder can't deliver. If a referenced `client_model` doesn't exist yet but the finding warrants one, record the concept at `medium` and note in `sketch` that the Analyst should emit it.

## Output — `imagineer.json`
Write incrementally (read-add-write). **Shape (consumed by the Editor + Interaction Engineer):** `items` is a dict keyed by `img_xx` (NOT a list). Full schema in [`references/schema.json`](references/schema.json):

```json
{
  "meta": { "role": "imagineer", "is_computational": true, "is_visual": true },
  "items": {
    "img_01": {
      "label": "Re-run the champion-odds model",
      "finding": "ana_01",
      "archetype": "explorable_recompute",
      "purpose": "INFORM",
      "reader_produces": "nudge a team's Elo, watch champion odds re-derive",
      "needs": { "client_model": "code/client_model.js:simulate", "data_table": "ana_01" },
      "feasibility": "high",
      "sketch": "slider(Elo)+dropdown(team)+button -> animated bars",
      "hero_candidate": true
    },
    "img_02": {
      "label": "Guess the gap before the reveal",
      "finding": "ana_05",
      "archetype": "guess_then_reveal",
      "purpose": "IMMERSE",
      "reader_produces": "commit a guess for the gap, feel the correction when the real value lands",
      "needs": { "client_model": null, "data_table": "ana_05" },
      "feasibility": "high",
      "sketch": "slider(your guess) -> reveal guess bar vs real bar from data_table",
      "hero_candidate": false
    }
  }
}
```

`purpose` is **INFORM** (the reader produces a number/insight the prose can't hand over) or **IMMERSE** (the reader produces a *feeling* — the correction lands, the odds shift under their hands). A concept that is neither is decoration — don't propose it.

## References
- [`references/schema.json`](references/schema.json) — full `imagineer.json` structure + field notes.
- [`../references/topic_profile.json`](../references/topic_profile.json) — the shared S3 classifier the "When to run" gate keys off (`is_computational` / `is_visual`).
- [`../../frontend-design-pro/references/interaction_playbook.json`](../../frontend-design-pro/references/interaction_playbook.json) — the `interaction_taxonomy` + recipes the `archetype` values name; read it to keep archetypes real.
- [`../../frontend-design-pro/references/abstract_excellence.json`](../../frontend-design-pro/references/abstract_excellence.json) — the POSITIVE flagship playbook for dry / abstract / computational topics (`is_visual=false`): the reframe hook, `personal_input` "where you land", the signature annotated chart, scale/analogy, the runnable-verify transparency lever, and the descriptive engagement floor. Read it whenever the topic is abstract.
- Reuse the feasibility-check pattern from `../interaction/SKILL.md` Step 4 (`node` a `client_model` call).

Done when the Editor has a rich, honest pool of candidate interactive concepts — each bound to a real finding, declaring its archetype + purpose + what the reader produces, with a node-checked feasibility — to curate a hero + supporting set from. The pool deliberately over-generates; the Editor decides what survives, and only what the Editor curates is ever built.

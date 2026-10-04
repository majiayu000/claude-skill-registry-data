---
name: intentumdiff-diff-expectations
description: >-
  The behavioral oracle for the IntentumDiff engine — a scenario catalogue that says, per diff
  scenario, exactly what the engine SHOULD produce (which changes, with which labels, and which
  change_groups are surfaced vs suppressed, and why). Use this whenever you implement, fix, port,
  or review engine behavior for a language/scenario, when you need the expected result for a test
  (Python acceptance OR Rust #[cfg(test)]), or when deciding "is this diff output correct?". This
  catalogue — not the Python `analysis/*` implementation — is the source of truth: Python is no
  longer the oracle. Every scenario here must be enforced by BOTH a Python acceptance assertion
  (via `SemanticDiffer`) and a Rust unit test. Read intentumdiff-language-profiles / -engine for the
  mechanism, and intentumdiff-dev-loop for the migrate-to-Rust workflow this oracle drives.
---

# IntentumDiff — diff expectations (the behavioral oracle)

**Why this exists.** IntentumDiff's engine is moving from Python into the Rust core; the Python
`analysis/*` implementation is legacy being retired, so it can no longer be the reference for
"correct." The reference is now **explicit expectations**: for a given input, the exact review
output the engine should produce. This catalogue is that reference. It is enforced at two layers
that must agree:

1. **Python acceptance** — a test in `tests/unit/` calls `SemanticDiffer().diff_strings(...)` (or
   a playground fixture) and asserts the expected `changes` / `change_groups`.
2. **Rust unit** — a `#[cfg(test)]` case in `crates/rust-core-host` asserts the same expectation
   on the Rust engine directly.

A scenario is "certified" only when **both** layers pass and the language is on the
`RUST_CERTIFIED_LANGUAGES` allowlist (see intentumdiff-dev-loop / the migration plan). When they
disagree, the catalogue wins — fix the code, not the expectation (unless the expectation itself is
wrong, in which case change it here first, then both tests).

## What a scenario row contains

| Field | Meaning |
|---|---|
| **language** | The language id (drives parser + profile family). |
| **input** | old → new source (or a named playground fixture: `_playground_diff(lang)` / `_diff(lang, "Moved Code")`, from `tests/fixtures/semanticdiff_examples.json`). |
| **expected changes** | The `change_type` + node label/type that MUST appear (and MUST NOT — "no leakage" rows). |
| **expected groups** | `change_groups` kind + rule_id, surfaced vs suppressed, key metadata (reason, node_ids). |
| **why** | The intent — what human-meaningful outcome this protects. |
| **enforced by** | The Python test + the Rust test id. |

## The general principles the scenarios encode

These are the recurring intents behind the per-language rows — a change is "right" when it matches
the principle, whatever the language:

- **Entity-anchored review.** An added/changed function/class/form/sub/resource surfaces as **one**
  change keyed on its **name** (e.g. `multiply`, `cube`, `GREET`, `Multiply-Numbers`), not as a
  spray of body/scaffold add/deletes and not as `(anonymous)`.
- **Scaffold/expansion churn is suppressed.** Body structure (`function_body`, `block`,
  `return_statement`, `additive_expression`, bash `expansion`/`word`/`string`, delphi `exprBinary`/
  bare `statement`, module headers like `Demo`) must NOT appear as its own add/delete.
- **Parameter renames are renames, scoped to their routine.** `a→x`, `b→y` are `REFACTORING`
  renames (one each), not signature churn (`(function)` / `(anonymous)` CHANGE_SIGNATURE) and not
  parameter identifiers leaking as `ADDITION`s.
- **No false moves.** A stationary entity that only shifted because something was added above it is
  NOT a `MOVE`/`REORDER`; named subroutines/functions are never "anonymous moves". Genuine moves
  are one `MOVE` with the entity name and no add/delete leakage.
- **A changed entity is a MODIFICATION, not suppressed noise.** A form/procedure whose body
  changed is a `MODIFICATION` (or demoted stationary-entity-move), never dropped as "stable noise".
- **Identity by semantic key for data/resource/query languages.** Keyed/resource/query languages
  match on key/title/field identity (puppet resource title + attribute, SQL field/clause, JSON
  key), not position — so shifts aren't spurious modifications.
- **Style/format equivalence is IGNORED_STYLE with an explainable reason**, keyed on node ids,
  under a language rule (e.g. `javascript.formatting.call_argument_wrapping_equivalence`), never a
  generic `presentation.ignored_style.*`.
- **Core invariances** (style-only shortcut, integer/string/hex canonical equivalence) and
  **guardrails** behave as their own certified scenarios — see
  [references/core-behaviors.md](references/core-behaviors.md).

## The catalogue

- **[references/failing-scenarios.md](references/failing-scenarios.md)** — the 10 scenarios that are
  the current migration targets (RC blockers), grouped by profile family: statement (bash, delphi),
  entity/function (abap, dart, elixir, perl), resource (puppet), matcher/presentation (the JS move
  + style pair). Each row is the spec a port must satisfy through Rust.
- **[references/core-behaviors.md](references/core-behaviors.md)** — cross-cutting behaviors already
  green (style-only, invariances, reorder suppression, moved-code, refactor rename, guardrails),
  captured so the oracle is a coherent whole, not just the failures. "If you see X → expect Y" tables.
- **[references/text-and-content.md](references/text-and-content.md)** — text / prose / markdown /
  config expectations: a changed line is ONE clean line change (char detail in `text_diff`, never
  per-character churn); markdown heading renames de-duplicate to one section change; non-code files
  surface as **Content**, not "Behavior". "If you see X → expect Y" tables.

## The standard scenario matrix (every language gets the SAME set)

Every language / major file type must have the **same** canonical scenarios, each asserting the
clean expected output. Structure: an abstract suite `tests/unit/scenario_suite.py` (`Case`,
`check_case`, and the family bases `LineScenarioSuite` / `MarkdownScenarioSuite` /
`CodeScenarioSuite` that define the standard `test_*` methods), and **one implementation file per
language** `tests/unit/test_scenarios_<lang>.py` (`class Test<Lang>(…Suite)` supplying `language`,
`filename`, and a `CASES` dict). Adding a language = one small file. A scenario a language omits is
absent from `CASES` and its inherited test skips; a known gap sets `xfail=<reason>` (the assertion
still runs and fails → visible; flips to XPASS when fixed). Cross-file scenarios (moves/refactors
spanning files) live in `tests/unit/test_scenarios_crossfile.py` (index-level, via
`detect_cross_file_changes`).

**Line-oriented file types** (plain text, markdown, config — generic parser):
`add_at_end`, `add_in_middle`, `add_at_start`, `delete_at_end`, `delete_in_middle`,
`delete_at_start`, `modify_line`, `modify_two_lines`, `reorder_lines`, `whitespace_only`,
`identical`; markdown adds `add_section_at_end`, `add_bullet`, `edit_paragraph_word`,
`rename_heading`, `delete_section_body_line`, `move_section`.

**Code file types** (per language, entity-oriented — same scenario *names*, entity-level
expectations): `add_fn_at_end`, `add_fn_in_middle`, `delete_fn_at_end`, `delete_fn_in_middle`,
`modify_fn_body`, `rename_fn`, `rename_param`, `move_fn` (reorder), `add_param` (signature),
`style_only` (reformat). Expected: one entity change keyed on the name; no scaffold/body/param
leakage; renames scoped; no false moves — see the general principles above and
[failing-scenarios.md](failing-scenarios.md) for the per-language node vocabularies.

Rollout: text + markdown are in place (the template); code languages plug into the same harness
with per-language snippets, added in batches until every supported language has the full set.

## Using this skill

- **Porting a language to Rust:** read its rows here first; they are the acceptance spec. Implement
  in Rust until both the Python acceptance test and the new Rust `#[cfg(test)]` case match every
  row, then add the language to the allowlist and retire its Python profile.
- **Fixing a diff bug:** find/add the scenario row; if the current output disagrees with the row,
  the code is wrong; if the row is wrong, fix the row (with rationale) then both tests.
- **Adding a new language/behavior:** add its rows here first (expectations-first), then the two
  test layers, then the implementation.

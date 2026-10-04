---
name: intentumdiff-engine
description: >-
  Deep reference for the IntentumDiff semantic diff engine internals — the pipeline, data
  models, GumTree matching, change groups, and the change-group index-space contract. Use
  this whenever you touch diff logic, change grouping, matching, refactoring/move detection,
  invariances, noise suppression, presentation normalization, NodeFacts, or anything that
  reads/writes Change / ChangeGroup / SemanticDiff (`crates/rust-core-host`, or the Python
  test-oracle in `src/intentumdiff/analysis/` + `core/`). Especially consult this before
  changing how change_groups reference changes — the `raw_change_indices` "index space" is a
  sharp edge that has repeatedly produced wrong output (a real change shown as "Noise").
  Read the intentumdiff-architecture skill first for the Rust-vs-Python boundary; new engine
  logic belongs in Rust, not Python.
---

# IntentumDiff — Diff Engine Internals

Remember the boundary (see `intentumdiff-architecture`): **new engine logic goes into the
Rust core** (`crates/rust-core-host`). The Python modules below (`analysis/`, `core/engine.py`)
are a parity test-oracle, not where features should grow. When you fix a defect, decide
whether the authoritative fix is in Rust; use the Python side only for the oracle or a
pure-DTO-shell transform.

**Migration reality — refinement / presentation / invariances are engine, and already largely
Rust.** The maintainer's direction is that these belong in the Rust core, and much of it is
already there for the certified native/batch path: `lib.rs` has `finalize_python_review_drafts`,
`suppress_low_signal_reorders_drafts`, ~20 `promote_*` refinement/refactoring rules, and
invariance/style-only evidence. The Python `analysis/*` files are the transitional oracle +
fallback. So when you hit an engine bug: **check the Rust core first** (`crates/rust-core-host/src/lib.rs`)
— it may already be correct, in which case a Python `analysis/` fix is just oracle parity (no
Rust change, no maturin rebuild — e.g. the reorder group's empty `raw_change_indices` at
`lib.rs:5230`). Fix authoritatively in Rust and keep the Python oracle in parity; don't grow new
logic in Python `analysis/`.

## The pipeline

```
Source → [Preprocess] → Parse → Normalize → Diff → Analyze → [Enrich] → Render
```

- **Normalize** filters trivia and computes bottom-up `structural_hash`. **Style-only
  shortcut:** if the filtered old/new roots hash equal → `SemanticDiff(is_style_only=True,
  changes=[])`.
- **Diff** is GumTree two-phase (below).
- **Analyze**: move consolidation (`moves.py`), refactoring detection (`refactoring.py`),
  classification (`classifier.py`), diff-analyzer plugins (stage 13.5), guardrails
  (`guardrails.py`), and **presentation normalization** (`presentation.py`) which builds the
  human-facing `change_groups` and suppresses noise.

Full stage-by-stage detail (matching heuristics, refactoring signatures, fuel, cross-file):
`docs/ARCHITECTURE.md`.

## Data models (`src/intentumdiff/core/models.py`, frozen pydantic v2)

- **`SemanticNode`**: `id` (unique within tree), `node_type`, `label`, `position`,
  `structural_hash`, `children`, optional `parent_type`, `type_info`, and **`facts`
  (`NodeFacts`)** — privacy-safe structural facts (`param_count`, `returns`, `body`
  empty/stub/substantive, `is_async`, `is_generator`, `decorator_count`) emitted by the Rust
  parser for definition nodes. Facts are counts/enums/bools only — never source text.
  Fact derivation is only as good as the tree: `return_kind` maps the return VALUE node's
  `node_type` through `semantic_literal_kind` in `rust-core-host/src/lib.rs` — grammar-specific
  literal names (java `decimal_integer_literal`, c/cpp `number_literal`) must be in that map
  AND retained by the parser's semantic set (issue #72), and the return collectors match
  `return_statement | return_expression | return` (scala/ruby). A parser that prunes the value
  degrades honestly to `returns: "value"` (kotlin/swift line scanners still do).
  `tests/unit/test_intent_facts_sufficiency.py` is the per-language contract.
- **`Change`**: `change_type` (`ChangeType | str` — plugins may add language-specific
  strings), `old_node`/`new_node`, `refactoring_kind`, `confidence`, `description`,
  `text_diff` (compact `[-old][+new]` leaf char diff).
- **`ChangeGroup`**: the review-level grouping. `kind` ∈ `MOVED_CODE | REFACTORING |
  MEANINGFUL_CHANGE | IGNORED_STYLE | NOISE_SUPPRESSED`; `raw_change_indices` (indices into
  `SemanticDiff.changes`); `old_labels`/`new_labels`; **`old_node_ids`/`new_node_ids`**
  (the node identities it groups); `refactoring_kind`; `metadata` (carries `index_space`,
  `suppressed_count`, `reason`, `rule_id`, …).
- **`SemanticDiff`**: `changes`, `change_groups`, `guardrail_violations`, `language`,
  `has_semantic_changes`, `is_style_only`, `parse_errors`, `metadata`.

## GumTree two-phase diff (`core/engine.py`)

1. **Top-down**: priority queue by node height; equal `structural_hash` → anchor match
   (`confidence=1.0`); ties broken by positional closeness.
2. **Bottom-up**: unmatched containers matched by `dice(T1,T2) > min_similarity` (0.5),
   counting matched descendant *pairs*.

Edit actions: `Insert`, `Delete`, `Update` (matched pair, labels differ), `Move` (matched,
different parents). `_compute_matching` runs once and is shared by diff + refactoring
detection.

## Change groups and the index-space contract (READ BEFORE TOUCHING GROUPING)

This is the sharpest edge in the engine. Consumers (the VS Code extension, release notes)
index `change_group.raw_change_indices` **straight into the final `SemanticDiff.changes`
array**. But groups are built at different pipeline stages against *different* versions of
the changes list, and later stages re-sort/filter `changes`. A stale/cross-space index then
collides with an unrelated final change — the concrete symptom was a brand-new function
rendered as **"Noise · below the meaningfulness threshold"**.

The contract and the reconciliation are documented in
[references/index-space-contract.md](references/index-space-contract.md). The essentials:

- Every group carries `metadata.index_space` ∈ `presentation_input | mixed | final_changes`
  (or a specialised evidence space like `style_only_shortcut`).
- `_reindex_groups_to_final_changes(changes, groups)` in `analysis/presentation.py` is the
  **single boundary reconciliation**: it rebuilds each group's `raw_change_indices` against
  the final `changes` **by node identity** (`old_node_ids`/`new_node_ids`) — the one key
  stable across re-sorts/filters. Applied last in `differ.py::_complete_final_diff`.
- **Producer contract:** a `ChangeGroup` must either carry node ids (so the reindex derives
  correct final indices) or be *honestly empty*. Never emit phantom positional indices
  (e.g. `range(len(discarded_input))`) and rely on a downstream pass to erase them — fix it
  at the producer. See the `presentation.generic_text_diff` group for the canonical
  "owns no final change → emit `[]`" case.
- Consumers must range-check every `raw_change_indices` dereference (`0 <= i < len(changes)`).

## Presentation & noise suppression (`analysis/presentation.py`)

- `normalize_generic_text_for_review` replaces generic-parser token churn with clean
  line/character spans and emits a `NOISE_SUPPRESSED` group that owns no final change.
- `_suppress_group` / style-context groups carry node ids and are safely reindexed.
- Suppression **preserves** `suppressed_count`/labels so the UI's "(N hidden)" summary and
  evidence counts stay correct even when indices are emptied.

## Invariances (why a change is "ignored style / noise")

Rich prose explanations for style/noise/equivalence live in the invariance rules
(`rules.yaml` / `invariances.py`), surfaced as group `metadata.reason`. Examples:
integer-literal canonical equivalence, string-quote equivalence, CSS hex/rgb equivalence.
When you make something "ignored," attach an explainable `reason` — don't just drop it.

## Where the change categories map to risk (used by the UI)

`MEANINGFUL_CHANGE → Behavior`; `REFACTORING`/`MOVED_CODE → Internal`;
`IGNORED_STYLE`/`NOISE_SUPPRESSED → excluded`; guardrail violations
(`important`/`immutable`) → critical/pinned. The extension derives risk from `kind` (it is
not a discrete engine field). See `intentumdiff-release-notes` for how this drives notes.

## Testing engine changes

- Reproduce with the real engine: `SemanticDiffer().diff_strings(old, new, filename,
  language_hint=...)` and inspect `diff.changes` + `diff.change_groups[*].raw_change_indices`
  / `metadata`.
- Confirm a suspected pre-existing failure by stashing only your engine files and re-running
  the same tests (see `intentumdiff-dev-loop`).
- Rust changes need `maturin develop --release`; pure-Python `analysis/` changes do not.

## DRY across the engine boundary (maintainer ruling, 2026-07-06)

One rule lives in ONE place. Two implementations of the same rule are drift waiting to
happen (the same-id rename promoter existed in Rust finalize and had to be mirrored in
Python for per-stage languages — every such mirror is PORT DEBT, not a solution):

- New engine logic goes in Rust. A Python mirror is only acceptable as a strangler
  transition step, and then it MUST: (a) cite its Rust twin by function name in a comment,
  (b) carry an open port issue (#37/#38/#39 pattern), (c) keep behavior identical — the
  scenario suites + corpus ratchets are the parity contract.
- Inside Rust, prefer shared helpers/traits over repeated match-arms and hunks: the SDK
  (crates/sdk) is the abstraction home for parser-side logic (#47); rust-core-host helpers
  (enclosing_entity_node, LIS, scope gates) are the home for matcher/refinement rules —
  extend them rather than cloning their logic at a new call site.
- Retire the Python copy the moment its language routes through the certified Rust path
  (RUST_CERTIFIED_LANGUAGES, issue #40).

## The target boundary (maintainer, 2026-07-06)

Sources in -> finished `SemanticDiff` JSON out of the **Rust core**. Python is a thin API
wrapper — and deliberately so: with the whole engine behind that boundary, additional thin
API layers in OTHER languages (Node/TS, C ABI, browser WASM) can bind the same core with
the same oracle. presentation.py/refinement.py are per-stage-path transitional code; the
retirement route is the per-stage Rust finalize callable + certification (see the
finalize-routing issue), with python mirrors DELETED per language as routing lands.

## Which pipeline actually served a diff? Probe the oracle before porting "missing" glue

Before porting a Python pass to Rust (or assuming a native path must fall back because a
pass is "missing"), run `SemanticDiffer().diff_strings(...)` on scenario fixtures and read
the FINGERPRINTS in the result — `metadata["semantic_contract"]` names the pipeline
(`rust_finalize_review_v1` = the routed Rust finalize) and `change_groups[].rule_id` names
every rule that fired. If the pass you planned to port never appears in the oracle's
rule_ids for real inputs, it is dead code for that route and needs deletion, not porting.

Canonical example (#100, 2026-07-24): the live-server roadmap carried a "~300-line markdown
section-presentation port" for months — but `.md` is a certified routed language (#44):
the manifest resolves it to the markdown tree-sitter parser, sections/headings are real
nodes, and the ENGINE produces section moves/renames (`refinement.entity_reorder_to_moved_code`,
the refactoring grouping) inside the finalize the native chain already runs. The
`_differ_presentation.py` markdown passes only execute in the differ's `language=="generic"`
branch, which resolved `.md` files never enter. The "port" was deleting a special-case.

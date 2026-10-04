---
name: intentumdiff-parsers
description: >-
  How IntentumDiff parses source into semantic trees — the Wasm parser-plugin architecture, the WIT
  contract, and how to add or fix a language. Use this whenever you work on a parser crate
  (`crates/<lang>-parser/`), add support for a new language, debug a parse error / fallback /
  wrong node types, touch the WIT plugin interface, or need to know why a language behaves the way
  it does at the tree level. It covers the five plugin worlds, `ParserMode::FullParse`, the
  CST→SemanticNode mapping, `detect-language`/`example` exports, the shipped-example contract, the
  Wasm sandbox/fuel model, and the build. Read intentumdiff-architecture for the boundary and
  intentumdiff-build for compiling; the per-language *diff tuning* above the parser is
  intentumdiff-language-profiles; the certified native path lives in the Rust core.
---

# IntentumDiff — Parsers (Wasm plugins)

Every language is parsed by a **WebAssembly component** — a self-contained parser whose grammar
and CST→semantic mapping are compiled into a `.wasm` binary. The Python/host layer is pure
orchestration; parsers run sandboxed with zero host capabilities. New parser work is Rust
(`crates/<lang>-parser/`) compiled to `src/intentumdiff/wasm/<lang>_parser.wasm`.

## The plugin contract (WIT — the only interface)

`src/intentumdiff/plugins/wit/plugin.wit` is the **single source of truth** for the plugin
boundary (no Python ABCs). Five plugin worlds:

| World | Role |
|---|---|
| `parser-plugin` | Parse source → `SemanticNode` JSON (the common case) |
| `renderer-plugin` | `SemanticDiff` → text/html/patch/llm output |
| `enricher-plugin` | Post-diff tree transform (e.g. dbt placeholder decode) |
| `diff-analyzer-plugin` | Post-classification `SemanticDiff` transform (language-specific change types) |
| `index-engine-plugin` | Symbol-table build + cross-file diff (Rust hot path) |

Built-in and third-party plugins use the **same loading path** — no privileged first-party route.

## Parser exports & modes

A `parser-plugin` exports (via WIT):
- `preprocess-source(source) -> source` — normalize syntax the grammar can't handle (most return
  input unchanged; e.g. dbt SQL rewrites `{{ ref('x') }}` to a stable placeholder).
- `process(source) -> SemanticNode JSON` — the full parse. **First-party product parsers must be
  `ParserMode::FullParse`**: the plugin owns grammar *and* CST→semantic mapping. The legacy
  `interpret-cst` (host-side Python CST parsing) is rejected on first-party paths with an
  actionable "FullParse plugin required" error.
- `detect-language(filename, content) -> language-id?` — cheap, deterministic, conservative;
  return a language only when the snippet is plausibly yours.
- `example(language) -> {old, new}` and `language-ids()` / `language-info()` — playground data +
  metadata (display name, Monaco mode, extensions). Host validates these at the adapter boundary.
- `trivia-node-types()` — node types stripped before diffing (comments, whitespace).

The host validates every returned tree: `SemanticNode.model_validate_json` (invalid → error) and
`_validate_tree_ids` (IDs must be globally unique within the tree). **Emit unique `id`s** (e.g.
position-path or a counter) or the parse is rejected.

## What a good SemanticNode tree looks like

- Right-sized nodes: definition nodes (`function_definition`, `class_definition`, language
  equivalents) with children for params/body, so the matcher and `NodeFacts` have structure.
- `label` = the human identity token (name), `node_type` = the grammar role. These feed the
  language-profile keying (see `intentumdiff-language-profiles`) — if the node types/labels are
  wrong, no profile can fix the diff. Set `parent_type` for methods (enables PULL_UP/PUSH_DOWN).
- Definition nodes should carry `NodeFacts` (param_count/returns/body/async/generator) — computed
  in the Rust CST→SemanticNode pass (see intentumdiff-engine); privacy-safe counts/enums only.

## Adding a new language (outline)

1. Scaffold a crate from `templates/plugin-template/` (cargo-generate) → `crates/<lang>-parser/`,
   using the `sdk` crate for shared types. Vet the grammar/tree-sitter dependency for safety +
   license (`docs/LIBRARIES.md`; candidate vetting lives on issue #48).
2. Implement `process` (FullParse), `detect-language`, `example`, `language-ids/info`,
   `trivia-node-types`. Map the CST to semantic nodes with stable unique ids and meaningful
   `node_type`/`label`.
3. Build to `.wasm` and stage it (see intentumdiff-build: `python build.py`); wire it into the
   registry/extension map.
4. **Shipped-example contract:** each advertised language ID must parse without fallback/parse
   errors and produce a structured diff for its `example`. Dormant crates (e.g. FreeBASIC) stay
   disabled until they meet it.
5. Add the per-language diff tuning in `intentumdiff-language-profiles` (keyed/review/scaffold node
   types) and fixtures in `tests/fixtures/` + `tests/unit/test_snippet_gap_regressions.py`.

## The FIVE registration ledgers (miss one → detection or invariance tests fail)

A new language id must be wired in ALL of these, or the parser silently never serves:

1. `pyproject.toml` `[project.entry-points."intentumdiff.parsers"]`.
2. `plugins/registry.py` `_FIRST_PARTY_PARSER_ENTRYPOINT_FALLBACKS` (+ the entry fn in
   `plugins/builtins.py` returning `_wasm("<lang>_parser.wasm")`).
3. `plugins/language_metadata.py` — `_DEFAULT_FILENAMES`, `_EXTENSIONS`, display-name tuples.
   Without an `_EXTENSIONS` entry the filename shortlist can never nominate the parser.
4. `RUST_FINALIZE_LANGUAGES` in `differ.py` — an unlisted language is a token-fallback kill
   switch (since the python-pipeline deletion, #57).
5. The invariance catalog: `invariances/rules.yaml` (language lists), `rules.schema.json` enum,
   and the validator set in `analysis/invariances.py`.

## Hard-won conversion rules (each cost a debugging cycle — don't re-learn)

- **0-based rows are MANDATORY** (issue #52). Emit tree-sitter's `start_position().row`
  unmodified; hand-rolled scanners start `line = 0`. `tests/unit/test_position_convention.py`
  asserts this over every corpus language and fails any drift back to 1-based. Never add a
  downstream base compensation — the engine had one (`one_based` in `profile_source_snippet`)
  and it's deliberately deleted.
- **Use the grammar's ACTUAL node kind names — dump a parse, never guess.** java listed
  `integer_literal` in its semantic set for months while tree-sitter-java emits
  `decimal_integer_literal`, so `return 99;` silently pruned its value (issue #72 — blocked
  `return_kind` facts).
- **VALUE nodes must be semantic.** If literals/values aren't in `SEMANTIC_TYPES`, value edits
  vanish from the diff entirely (INI's `setting_value` lesson) and the style-only shortcut can
  misclassify real edits.
- **`node_to_cst` keeps text ONLY on leaves.** Name nodes need leaf-descent (`leaf_text`);
  text interleaved with anonymous nodes (make recipe shell text) vanishes from leaf joins and
  needs SOURCE-SPAN labels (thread `source: &str` through convert, see make-parser's
  `span_text`).
- **Grammar crates that split the tree_sitter dependency graph** (old bindings, e.g.
  tree-sitter-gomod 1.0.1): rewrite bindings in a patch crate to the modern
  `tree_sitter_language::LanguageFn` form (see `crates/patches/tree-sitter-gomod`).

## Detection: how a filename picks a parser (and the fallback trap)

`registry.py::_candidate_entries(filename)` shortlists catalog entries whose default filename /
extensions match; if nothing matches it falls back to ALL entries. The generic parser matches
`.txt` and detect-claims everything, so shortlists sort designated-fallback entries
(`language_guesses` containing "generic") LAST — a specific parser that matched the filename
always gets first refusal (found via CMakeLists.txt: generic's `.txt` beat cmake by catalog
order). Debugging "my language resolves to generic": print the shortlist from
`_candidate_entries`, then call the loaded parser's `detect_language` directly — registration
being *cataloged* is not the same as being *nominated*.

Guides: `docs/PLUGIN_GUIDE.md`, `docs/CONTRIBUTING_PLUGIN.md`, `docs/PLUGIN_ECOSYSTEM.md`,
`docs/CST_SCHEMA.md`.

## Sandbox & fuel (why a parser might trap)

Parsers run in a **wasmtime** sandbox: empty `WasiConfig` (no fs/net/env), memory-isolated, and
**fuel-metered**. Parser fuel scales `20_000_000 + cst_node_count × 200_000` (floored by
`DiffConfig.plugin_fuel`, default 100M). Exhaustion raises `PluginFuelExhausted` with
`FUEL_EXCEEDED: <size>` — surfaced as a parse diagnostic. `--fuel inf` disables metering (use
with care). Host imports exposed to plugins are only `strip-trivia`, `structural-hash`, `log`.

## Debugging a parser

- Parse errors / fallback: run `intentumdiff file old new --profile-phases` or `diff_strings`; check
  `diff.parse_errors` and `diff.is_fallback`. A first-party language falling back to the generic
  parser is a bug — the grammar or `detect-language` is the lead.
- Wrong node types/labels: dump the tree (the parser's `process` output) for the snippet and
  compare to what the profile expects. Fix at the parser if the *vocabulary* is wrong; fix at the
  profile if the vocabulary is right but the *treatment* is wrong.
- Rust core tests for the CST→semantic pass: `cargo test -p rust-core-host`; per-parser crate:
  `cargo test -p <lang>-parser`.

## DRY is a hard rule: parser code must be abstract, never copy-pasted

Maintainer ruling (2026-07-06): **do not copy the conversion template between parser
crates.** The 28 duplicated `node_to_cst`/`label_for` templates drifted until class-wide
fixes required per-crate sweeps (the literal-visibility fix patched 21 crates and had to
SKIP 40 variants; the SDK hash fix was one edit for all 60 precisely because hashing IS
shared in `crates/sdk`).

- Shared behavior (CST conversion, text capture incl. literal kinds, generic labeling,
  position conventions, trivia) belongs in `intentumdiff-plugin-sdk` — issue #47 tracks the
  `TreeSitterConverter` trait (Rust's abstract-base equivalent: a trait with default
  methods); per-crate code supplies ONLY data (semantic-type lists) and genuine language
  overrides (`label_override` hooks).
- When you fix a conversion bug in one crate, the fix belongs in the SDK unless it is
  provably language-specific. If you find yourself writing the same hunk into a second
  crate, STOP and hoist it.
- Migration acceptance: a pure migration leaves every corpus ratchet manifest byte-identical
  on regeneration (tests/fixtures/corpus is the contract).

---
name: corpus-management
description: Corpus-Management umbrella skill for grc_library. Use when creating, editing, reviewing or auditing corpus documents or any file a corpus gate scans, when answering a question about a corpus rule, when a corpus gate fails, when working on the pack source under .corpus-management/, and when regenerating or checking compiler-owned outputs (gate 99).
derives_from: ../../../.corpus-management/README.md
---

# Corpus-Management

The umbrella entry point for the Corpus-Management pack and its tooling. The
pack source of record is `.corpus-management/`; the compiler
(`.corpus-management/tools/corpus_mgmt_compiler.py`, wrapped by
`tools/build-corpus-management.py`) renders every generated output, and gate 99
(the wrapper's `--check` form) enforces byte parity with nothing stripped.
This file is itself compiler-generated from
`.corpus-management/core/skill/SKILL.md` with no provenance header (the
discovery frontmatter must start at line 1); edit that source and regenerate,
never this copy.

## Rule discovery

- `rule-index.md` in this skill directory
  (`.claude/skills/corpus-management/rule-index.md`, compiler-generated) lists
  every on-demand corpus rule as `id|purpose|tool|body`; read it when this
  skill loads. Read a rule's body before creating or editing a file that its
  gate scans, before reviewing or auditing such files, when answering a
  question about that rule, and when its gate fails.
- Always-loaded bodies: `language-convention.md` and `normative-wording.md`
  under `.claude/rules/corpus-management/`; every other body lives under
  `.claude/references/corpus-management/` and loads on demand.

## Tooling

- Regenerate owned outputs: `python3 tools/build-corpus-management.py`.
  Never hand-edit a generated file; edit the pack source and regenerate.
- Drift check (gate 99): `python3 tools/build-corpus-management.py --check`.
- Release floor: `python3 tools/build-corpus-management.py --check
  --release-delta`. Every pack change needs at least a PATCH bump of
  `core/manifest.toml` `[pack].version`; new identifiers need a MINOR.
- Gate engines live in the pack (`.corpus-management/tools/gate_lint_*.py`)
  behind thin `tools/lint-*.py` wrappers: edit the engine in the pack, keep
  project scope and configuration in the wrapper.

## Pack registers

- `gensrc.toml` declares every generated output; `core/ownership.toml` mirrors
  it one entry per rule; `core/manifest.toml` `[generation].owned_targets`
  carries the deduplicated target summary. The compiler fail-closes (exit 2)
  on any disagreement among the three surfaces.
- `core/id-history.toml` is append-only: a pack id, once assigned, is never
  reused. Clause, gate, hook, rule and profile ids share one namespace.

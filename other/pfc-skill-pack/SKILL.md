---
name: pfc-skill-pack
description: Govern Asphalt-Codex-Skills-5 as a PFC 5.0-only asphalt-mixture package, enforcing version purity, external fistPkg boundaries, portable assets, validation, and release hygiene.
---

# PFC 5 Asphalt Skill Pack Governance

Use this skill when maintaining, auditing, packaging, or releasing this repository. Modeling tasks start at `pfc5-asphalt-workflow`; this skill owns repository policy.

## When To Use

- add, remove, rename, or audit a skill;
- check PFC 5.0 version purity;
- update dependencies, metadata, indexes, or release notes;
- decide whether a PFC/fistPkg asset may be bundled;
- validate links, paths, scripts, examples, or generated files.

## Non-Negotiable Scope

1. The package targets PFC2D/PFC3D 5.0 asphalt-mixture work only.
2. Unsupported-major-version commands, APIs, examples, documentation, and migration routes are not retained.
3. fistPkg, commercial manuals, DLLs, projects, saves, and standards text stay external.
4. Bundled PFC scripts must state `static_validated` or `runtime_validated`; static inspection never implies a successful solve.
5. Public paths are relative or use placeholders such as `<FISTPKG_ROOT>`.

## Required Inputs

- proposed files and target PFC product;
- source/provenance and redistribution status;
- affected sibling skills and dependency paths;
- validation evidence and runtime availability;
- expected user-facing routing change.

## Workflow

1. Classify the change as governance, PFC source, Python tooling, example data, or external dependency contract.
2. Reject out-of-scope version content before detailed review.
3. When a licensed PFC5 help tree is available, bind command claims to relative page
   locators using `references/pfc5-help-audit.md`; do not copy or commit the help tree.
4. Keep `SKILL.md` concise and move detailed reusable material to `references/` or `scripts/`.
5. Update `dependencies.json` for every cross-skill asset.
6. Run the validator, Python tests, AST compilation checks, and relevant demo/smoke tests.
7. Confirm every slug in `references/pfc5-skill-set.json` exists and every migrated
   capability is accounted for in `references/migration-coverage.md`.
8. Regenerate `references/skill-index.md` and review the final diff.
9. Record any unpassed PFC runtime gate explicitly.

## Release Gates

- no unsupported-version markers or newer-major command families outside the validator itself;
- no absolute private paths, credentials, opaque binaries, caches, generated saves, or project files;
- no broken local links or missing dependency assets;
- every Markdown or inline-code reference to a sibling skill asset is covered by that
  skill's `dependencies.json` entry;
- every inline-code `pfc...` skill-like reference in a `SKILL.md` resolves to an
  installed skill directory or the validator's explicit non-skill allowlist;
- Agent metadata descriptions stay concise;
- demo inputs exist and runnable Python examples complete;
- external third-party assets have a documented contract and are not vendored.

## Output Contract

Return the retained skill list, removed/out-of-scope assets, validator/test results, runtime-validation status, third-party boundaries, and exact unresolved risks.

## Local Contents

- `references/asset-inventory.md` — PFC5 packaging classes and inclusion rules.
- `references/pfc5-help-audit.md` — relative official-help locators and corrected command semantics; the commercial help stays external.
- `references/migration-coverage.md` — retained, rewritten and deliberately excluded capabilities.
- `references/pfc5-skill-set.json` — portable copy of the required package skill set; release validation keeps it identical to the repository manifest.
- `templates/case-intake.md` — repository change intake.
- `scripts/build_skill_index.py` — index helper.
- `README.md` — short package policy summary.
- `LICENSE` and `NOTICE.md` — retained MIT terms and upstream provenance.

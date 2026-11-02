---
name: harness-evaluate
description: Use when evaluating a reference-harness capability for adoption, rejection, deferral, or synchronization. Inspection alone does not authorize adoption.
---

# Harness Evaluate

Evaluate a reference capability against the maintained shared harness. Read the
candidate's canonical source, relevant prior ledger decision and closest local
implementation. Reference repositories remain read-only evidence.

Compare behavioral gain, overlap, dependencies, context cost and maintenance.
Choose reject/defer, merge into an existing capability, a separate plugin for a
distinct dependency/domain boundary, or shared template adoption for broadly
useful low-cost guidance. Use harness-skill-compare for a substantive comparison.

Evaluation alone produces a recommendation. Record a curation decision only when
ledger changes are authorized, in the open round
(`harness_lifecycle/registry/README.md` §5–§5c, method in `harness_lifecycle/playbook.md`).
An upstream skill is ruled trait by trait, each event citing a sealed report
(`--json` with `report`); a skill without an accepted analysis may only be ruled
whole as `defer`, `reject` or `out-of-scope` (`--whole-skill`). Other capabilities
get one event each. A `defer` carries `revisit_when`:

```text
uv run python harness_lifecycle/registry/registry.py record --kind <reject|defer|out-of-scope|adopt|adopt-merged> --subject <repo>:<logical_id> --why <reason> --evidence <path:line or registry/reviews/<file>>
```

Authorized adoption edits the actual canonical source. Shared policy belongs in
AGENTS.md and shared skills/project docs; Codex integration links or adapts them.
Do not duplicate semantic edits across provider directories. Inspect current sync
and publish manifests before selecting destination; template output is generated.

For template adoption, verify the initialized mvp-harness tools exist, run
`check-sync.sh` and `build-template.sh` under its mvp-plugin scripts directory,
and inspect neutrality/leak results. Obtain independent review when the broad
blast radius warrants it under shared delegation policy. New/existing plugin
implementation also requires authorization for that submodule work.

Record `adopt` or `adopt-merged` with `--skill <our-skill>` only after the
adopted state exists. For `adopt-merged`, pass the adaptation (`merged_from`,
`modifications`, `deliberately_dropped`) with `--json`. The source commit and
content hash are filled from the catalog. Then run `registry.py build`; skill
records are generated, never edited. Publication,
commits and pointer updates require their own existing authority; otherwise
report the prepared result. Borrow the smallest useful pattern.

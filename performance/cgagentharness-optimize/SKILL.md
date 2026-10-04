---
name: cgagentharness-optimize
description: Find and implement evidence-backed Rust, desktop, runtime, and CI improvements in CG-agent-harness, grouped into focused draft PRs when publication is requested. Use for project optimization or maintainability work, not unrelated CyClaw or RAG changes.
---

# Optimize CG-agent-harness

Use current repository contracts, PR deduplication and measured verification.
For documentation, edit the owning file within `DOCS_BUDGET`; do not add
parallel guides or evidence files.

Read root `AGENTS.md`, `INVARIANTS.md`, the current workflows and PR template.
Find the actual checkout, dirty state, default branch, and exact remote base.
Preserve work; create an isolated `codex/optimize-<topic>` branch when needed.
Check clean-base tests before edits. If they fail, report the failing command
and cause before building further work on that baseline.

Inspect the requested scope before choosing findings. Useful areas are:
- `src/agentic`: exact edits, reviewed-tree approval, sandbox and process lifecycle.
- `src/server`, `src/shim`, `src/llm`: guard ordering, cancellation, bounded model I/O.
- `desktop`, `scripts/package-desktop.sh`: native ownership, sidecar identity,
  architecture slices, dependency policy and reproducible verification.
- `.github/workflows`, `tests`: meaningful coverage, exact-head gates, artifact provenance.

For each finding, show its trigger, code location, impact and verification.
Large files, newer dependencies or speculative
speedups do not alone justify changes. Check open PRs before selecting work;
zero findings is valid. Never manufacture a quota of findings or PRs.

Map files to focused changes. Every draft PR starts from current `origin/main`
and targets `main`; this repository forbids stacked PR bases. Consolidate
related edits to shared files. Deliver dependent work after its prerequisite
lands, then refresh main and check overlap again.

Implement only the authorized scope. Preserve I6: server/common/LLM/shim never
import agentic; only the shim dispatches whitelisted child actions. Keep shipped
write gates closed, explicit confirmation/reason, fresh policy checks, clone jail,
reviewed commit/origin binding, loopback guards and bounded subprocess capture.
Do not transplant CyClaw's Python/RAG topology, model defaults, hooks or credentials.

Run the relevant Rust tests plus the required quality checks from `AGENTS.md`;
use `desktop/rust-toolchain.toml` for desktop checks and root toolchain for backend.
Native Seatbelt, real model, and WKWebView claims need corresponding native evidence.
Record skipped/unavailable checks and performance measurements with conditions.

If the user requested publication, inspect the diff, run
`scripts/check-pr-template.sh <body-file>`, push the scoped branch and open a draft
PR using the actual template. Otherwise deliver the local change or assessment.
Skill selection is not authorization to push, publish a release, merge or change
host settings. Verify remote head and exact-head CI after publication. Report
concrete changes, tests and remaining risk. Read the advisory review gate and
verify the reviewed SHA separately from CI status.

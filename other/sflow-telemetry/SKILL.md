---
name: sflow-telemetry
description: Inspect Context X-Ray, Token Ledger, and privacy-safe local Copilot usage without estimating unavailable values.
disable-model-invocation: true

---

# Inspect telemetry

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. For context questions, run `singularity-flow context xray <WORK-ID> --json`. For token questions, run `singularity-flow tokens report <WORK-ID> --json`. Omit `<WORK-ID>` only when governed Story work is active. Otherwise run `singularity-flow telemetry status --json`.
2. Show the qualified state (`captured`, `partial`, `unavailable`, `conflict`, or `disabled`), SFlow-owned launch counts, capability mode, and pending generations. Do not expose host paths or raw event content.
3. If disclosure is required, explain that `/sf-telemetry` cannot accept it on the contributor's behalf. Ask before running `singularity-flow telemetry enable --confirm "ENABLE LOCAL USAGE" --json`; quote the metadata-only disclosure first.
4. If a completed generation is pending, ask before running `singularity-flow telemetry reconcile [PHASE] --json`; reconciliation commits and pushes only the sanitized record.
5. Run `singularity-flow telemetry disable --json` only when explicitly requested. Disabling changes future local capture only and never governs work.
6. Report `unavailable` when the provider omitted model, tokens, or cost. Never estimate, and never treat native IDE chat as captured by an adjacent CLI launch.
7. Keep provider observations separate from SFlow packet estimates. Preserve every metric's status and assurance, and never call omitted context “tokens saved.”

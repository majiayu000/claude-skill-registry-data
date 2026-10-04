---
name: sflow-evidence
description: Show each requirement's evidence and the completion label.
argument-hint: "[WORK-ID] [--row ID] [--result RESULT]"

---
# Show the evidence matrix

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Use the Boundary repository. With an explicit Work ID, do not require or change the active Story. Without an ID, run `singularity-flow session current --json` and require its `ready` Story; use its exact `repositoryPath` as cwd.
2. Run `singularity-flow evidence matrix <WORK-ID> --json`, or without the ID for the attached Story, adding only `--row`, `--result` or `--facet` when the person asked for them.
3. From `data.matrix.evaluation`, show `completion.label` with its `reasons`, `lifecycle.words`, the counts in `summary.results`, `summary.assuranceFloor`, and `summary.scope.words` and `summary.scopeRevision.words` when present. Then show `page.rows` as a table: row ID, result, assurance, and each obligation's `responsibility` and `status`.
4. Use only the labels the CLI returned. Never say a Story is complete, all tests passed or all requirements are satisfied unless `completion.label` says so; "module-observed" means a covering test command passed; only "exact-local-observed" means the criterion's own test was seen passing.
5. List `findings` that need attention and each row's `actions` commands as next steps, without running them.
6. When the person asks which requirement statements the Story's sources hold, run `singularity-flow evidence scope <WORK-ID> --json` instead: show each item's `id`, `text`, `sourceId` and `disposition`, the unreadable sources, `structurallyComplete` and `completenessReview`. A review never means the scope is correct.
7. Do not change files or lifecycle state.

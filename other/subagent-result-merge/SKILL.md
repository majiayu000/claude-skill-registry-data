---
name: subagent-result-merge
description: "Merges agent or review outputs into one deduplicated, evidence-linked, severity-ranked actionable report."
---

# Subagent Result Merge

Normalize parallel findings into one decision-ready report.

## Worker Result Contract

Extend this contract for native and external workers; do not introduce a
parallel report format. The launcher records execution facts independently of
the worker's prose. This minimal blocked example is a shape example, not
evidence of an installed or active integration:

```json
{
  "task_id": "example-task",
  "goal": "Review the allowed synthetic snapshot",
  "base_commit": "unknown",
  "snapshot": {"state": "not_created", "sha256": "unknown", "files": []},
  "requested": {"provider": "explicit-local-mapping", "model": "explicit-local-mapping"},
  "observed": {"provider": "unknown", "model": "unknown", "source": "unknown", "verification": "unknown"},
  "status": "blocked",
  "findings": [],
  "checks": [],
  "artifacts": [],
  "open_questions": ["Runtime capability has not been verified"],
  "usage": "unknown"
}
```

Required fields:

- `task_id`, `goal`, `base_commit`, and `snapshot`: capture the base revision,
  uncommitted state, exact allowed files and content hash of the transferred
  snapshot. Missing revision or hash is `unknown`, never a fabricated value.
- `requested`: provider and model selected before launch, separately from
  `observed` provider/model returned by runtime or provider metadata.
- `observed.source`: identify the raw artifact and metadata field;
  `observed.verification`: `runtime_metadata`, `provider_response`, or `unknown`.
  Missing metadata remains `unknown`; a configured model is only requested.
- `status`: completed / blocked / failed. Include a reason for blocked or
  failed results. Completion is not proof that every check passed.
- `findings`: each has `file_line`, severity, evidence, limitations, and source
  reviewer. Link to raw artifacts; identify snapshot-relative locations.
- `checks`: each has the exact `command`, actual integer `exit_code` or null
  when not run, `raw_artifact`, and outcome (`PASS`, `FAIL`, `SKIP`, `BLOCKED`).
  A nonzero test exit cannot become PASS after output processing. Identify
  scanner errors separately from violations; do not infer scanner success
  solely from a summary. Skipped checks include a reason.
- `artifacts`: local paths to original safe output, findings, and proposed
  changes; `open_questions`: unresolved issues; `usage`: observed token/cost
  metadata with its source or `unknown`. Separate parent and worker usage.

Self-description such as “I am the requested model” is not route evidence.
Runtime or provider metadata is not independent proof of a provider's internal
execution. Preserve that limitation when reporting verification.

The portable `scripts/worker-evidence.py` helper implements consistency checks
for this contract; see [Worker Evidence](../../docs/worker-evidence.md). Captured
snapshot entries use `path`, `sha256`, and `bytes`; findings use the string key
`source_reviewer`. Artifact paths are relative to an explicit private artifact
root. Usage is `unknown` or `{duration_ms, tokens, cost_usd, method, source}` with
`null` for each unknown metric. Preserve `contract_status` separately from the
result `outcome`, and filesystem `SKIP` when source/artifact roots were not checked.
The helper checks recorded consistency, not metadata authenticity or sandboxing;
the launcher remains responsible for independently recording execution facts.

## Workflow

1. Validate result scope, snapshot freshness, requested versus observed route,
   and raw checks; quarantine malformed or contradictory records as failed.
2. Group findings by severity and affected behavior.
3. Deduplicate overlapping findings.
4. Preserve the strongest evidence and confidence level.
5. Separate confirmed issues from plausible/unverified risks.
6. Convert repeated themes into concrete follow-up actions. The main agent
   reviews proposed artifacts and owns applying changes.

## Output

- findings ordered by severity
- duplicates collapsed with source reviewers noted
- open questions
- recommended minimal fixes
- validation gaps
- next skill to use, if any

Return a concise summary and artifact pointers, initially targeting at most
1500 tokens when material findings fit. Keep original event streams and logs
outside tracked files; do not discard critical errors to meet the target.

## Rule

Only when `/quorum` is active for this task, keep these original worker records and
use the separately bound target, fixed roster and ballots described in
[Worker Quorum](../../docs/worker-quorum.md). Verify current source/artifact
roots; preserve disagreement and veto evidence instead of averaging confidence.
Unknown execution facts or missing verification cannot become an approval.

Without `/quorum`, merge findings without votes or majority decisions.
`/multimodel` alone does not enable voting; ordinary same-model parallel work
activates neither mode. Follow the task-scoped
[command contract](../../docs/cross-provider-review.md#explicit-activation).

Do not average confidence across reviewers. Prefer the most concrete evidence
and mark disagreement explicitly.

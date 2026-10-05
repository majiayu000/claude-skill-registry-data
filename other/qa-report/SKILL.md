---
name: qa-report
description: Export one validated QA manifest as matching HTML and PDF without executing tests or evidence commands.
---

# Export a QA report

Export an already recorded QA run. This workflow publishes a report package; it does not create
test results or reinterpret evidence commands. Read [workflow](../../references/workflow.md),
[safety](../../references/safety.md), [artifacts](../../references/artifacts.md),
[evidence](../../references/evidence.md), and [reports](../../references/reports.md) first.

## Inputs

- An explicit private manifest path and an explicit project root path. Never infer either path
  from the current directory, a run ID, or a prior conversation.
- The explicit objective or intent for the export, target identity, contract source/hash,
  complete acceptance-criterion catalog, cases, evidence, defects, limitations, recorded
  authorization, and existing QA verdict carried by that manifest.
- Explicit authorization to create a new report package beneath the supplied project root. The
  manifest's run ID must identify a new destination; export never grants any other authority.

## Procedure

1. Preserve the explicit objective or intent, target, contract, criteria, cases, evidence,
   defects, limitations, authorization, and recorded results. Do not infer missing criteria,
   applicability, assessments, execution, approval, or risk acceptance.
2. Identify the affected QA surfaces and consult installed applicable
   `qa-specialist-requirements`, `qa-specialist-defects`, or other `qa-specialist-*` skills only
   to expose semantic gaps already present in the supplied record. An unavailable applicable
   specialist is a limitation. Specialist guidance does not expand authorization or change the
   normalized manifest.
3. Before export, require a complete acceptance criteria catalog that preserves all criterion
   IDs, text, applicability and reason, assessment expected and observed values, and referenced
   case IDs. Confirm the identified contract and completed criteria review are recorded. Missing
   semantic confirmation remains a limitation and prevents a newly inferred `PASS`.
4. Use the explicit manifest and project root unchanged. The workflow invokes the exporter
   exactly once and never permits a second exporter invocation. Its only process invocation is
   `qa_report.py report --manifest PATH --project-root PATH`. Replace each `PATH` with its
   separately supplied path; do not add another subcommand, omit either option, or reuse an
   implicit root.
5. Let the exporter enforce schema and verdict precedence. Before HTML or PDF rendering, the
   exporter must validate acceptance criteria, confinement, limits, hashes, target/contract
   binding, sanitization, and evidence safety. The exporter renders HTML and PDF from the same
   normalized manifest. It publishes only a complete validated package. Never edit the private
   or public manifest around validation.
6. Preserve returned diagnostics, sanitization outcomes, and verdict without suppressing,
   repairing, or reclassifying them. Preserve `export_status`, `output_dir`, publication digest,
   and snapshot when present. Exit code `0` means both formats exported; it does not mean the QA
   verdict is `PASS`. Exit codes `2` and `3` remain refusal and incomplete export respectively.
7. Stored `command` values are inert text. It never executes or re-executes tests, manifest
   commands, or evidence commands. It never uses a stored command to fill a missing result and
   never retries the export after a failure or collision.

## Output

Return exactly these labels in this order. Tables may follow their labels. Report facts from the
exporter result and manifest; do not derive the QA verdict from the process exit code.

```text
TARGET: <manifest target, project, environment/build/change identity when recorded>
OBJECTIVE: <preserved explicit export objective or intent>
CONTRACT: <manifest contract path, hash, and criteria-review actor/time/completeness>
CRITERIA: <complete preserved IDs/text, applicability/reasons, assessments, case IDs, and criterion results>
OPERATION: report (export only; execute no tests or evidence commands)
AUTHORIZATION: <preserved export actor, authority, scope, target, project root, limits, and gaps>
EXPORT: <command outcome, exit code, export_status, output_dir, publication digest/snapshot, HTML/PDF state, and diagnostics>
RESULTS: <preserved case and criterion statuses: PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE>
LIMITATIONS: <missing semantic confirmation, unsafe/insufficient evidence, unavailable specialist, incomplete export, or none>
EVIDENCE_REFERENCES: <verified copied evidence IDs, public relative paths, hashes, target/contract binding, sanitization outcome, or none>
CURRENT_DEFECTS: <all current in-scope defects and explicitly separated out-of-scope defects, including unlinked defects, or none>
VERDICT: <preserved exporter QA verdict: PASS|FAIL|BLOCKED; independent of export exit code>
NEXT: <smallest separately selected and explicitly authorized correction, new run, or consumer revalidation action>
```

## Failure modes

- Missing or implicit manifest/project-root paths, missing export authorization, invalid schema,
  unsafe input/output, limit violation, symlink, or destination collision: do not substitute a
  path or retry; return the refusal diagnostic and no complete package.
- Missing, changed, target-mismatched, or sanitization-pending evidence remains withheld,
  produces a diagnostic, and prevents `PASS`. Never conceal it to make export succeed.
- A rendering or dependency failure is an incomplete export. Preserve the exclusive partial
  diagnostic path if returned, and never describe it as the complete run package.
- A complete export with verdict `FAIL` or `BLOCKED` is still an exported report. Do not rewrite
  the verdict from exit code `0`.

## Safety

- Never execute tests, stored commands, or evidence content during report export. Never install
  dependencies, alter personal configuration, expose secrets, or attach rejected evidence.
- Load testing, penetration testing, production access, and external effects require explicit
  authorization for a separate exact operation; report export performs none of them.
- Never correct product code, tests, contracts, results, evidence, defects, approvals, or
  authorization; product corrections are allowed only when separately requested.
- Never publish externally, push, merge, deploy, overwrite a prior run, or treat a partial
  diagnostic directory as a complete report.

## Related skills

- `qa-specialist-requirements` exposes acceptance-catalog gaps without rewriting the manifest.
- `qa-specialist-defects` checks the meaning of recorded current defects without resolving them.
- `qa-status` summarizes the resulting state without exporting or mutation.
- `qa-release` produces a readiness opinion separately from export status.

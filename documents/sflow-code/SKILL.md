---
name: sflow-code
description: Author a code-generation phase with executable tests and exactly-once publication.
disable-model-invocation: true
argument-hint: "[code-generation focus]"

---
# Governed code

<!-- sflow-output-contract: clarification-and-artifact -->
**Output contract:** Use governed inputs and pinned clarification; publish/show configured artifacts.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. From the Boundary require `phase`, `phaseAgent.valid: true`. `singularity-flow status --json`: match workId/currentPhase; require `phases[<phase>].generationPolicy.task: code` or legacy `implementation-summary` without task.
2. `singularity-flow recover <WORK-ID> --phase <phase> --json`: inspect blockers/actions, intent and `testExecution`. `phaseRepairRequired`/`working-tree` alone is no stop. Inspect `git status --porcelain=v1 --untracked-files=all`, diffs and untracked content including `workflow.json`. Repair returned owned, in-scope authoring actions within an open intent; `repair-repository-test-runner` requires `CODE_DELIVERY_TEST_COMMAND_REQUIRED` and source-scope repair. Untracked `.sflow/results/**` need no cleaning; preserve bytes. Tracked/staged reports still need review. Stop for protected/unrelated/unowned changes or lifecycle/authority blockers. `generation.intent.consumed-changed` requires `/sf-recover` reviewed rollover, never waiver.
3. Read Story context; `singularity-flow wm compose --phase <phase>`.
4. `singularity-flow clarification status <phase> --json`: For `off`, do not ask or record; continue. For `when-needed`, ask and record only for material ambiguity; otherwise continue. For `required`, `ask_user`, wait, record before mutation; stop if unavailable. Stage only `{"responses":[...]}` at `git rev-parse --git-path singularity-flow/clarification-responses/<phase>.json`; never at `singularity/work-items/**/context/clarifications-*.json`. Delete on success; never pass Markdown.
5. `singularity-flow story references verify --work-id <WORK-ID> --json`: use `localPath`; refuse invalid/dirty. Check `singularity-flow revision status --json`. Before authoring require an open intent; if absent run `singularity-flow phase begin <phase> --json`, honoring adoption/confirmation. Consumed intent requires `/sf-recover`.
6. Implement code/tests, not README. Doc-comment APIs; tags are not docs. Exclude fixtures/docs/deletions/symlinks. In the planned product-source path: `// @clause:ORDER:REQ-001 how this change meets it` (`REQ|BEH|IFC|AC|CON`); executable tests: `// @ac:ORDER:AC-001` above its test. Honor pinned test-only planned-claims opt-outs.
7. Compare `testExecution.commands` argv/cwd/adapter/report with manual tests. Python inference prefers `.venv`; pins remain unchanged. Repair runtime/dependencies with authorization. Run tests; no skip/list/dry-run/no-tests. Never edit protected configuration, disable hooks or fabricate results. In-scope declarations may repair inference. For `resolve-code-delivery-test-policy` or unavailable inference, use `/sf-recover` for reviewed runner adoption. Refresh never changes this Story's pin; do not approve amendments here.
8. Run `singularity-flow phase draft-check <phase> --json` and `singularity-flow phase prepublish <phase> --json`. Correct every structured agent authoring finding in this Copilot turn; at most three changed fingerprints. Initial template is baseline; stop on an unchanged fingerprint only after correction. If blocking finding code and source code remain unchanged, stop this attempt despite other changes. Honor `correction.class`/`sameTurn`; never blindly delete markers, invent facts, use padding, invoke a nested model, or overwrite another producer. `prepublish: ready` does not mean tests passed.
9. Publish once with configured producer/channel only when prepublish is `ready`. On refusal report `requiredTestExecution`: command ID (not shell command), argv/cwd, exit, bounded stderr and guidance. Nonzero exit fails despite passing JUnit. Follow `/sf-recover`; proven runtime repair permits retry without source changes. Source mutation requires review/rollover when consumed. Pre-mutation failure retains intent. No blind retries; at most three repairs. `ARTIFACT_AUTHORING_INCOMPLETE`: recheck once, retry once. Never submit/approve.
10. `singularity-flow phase show <phase> --json` is artifact review, not readiness or task policy; bounded preview, hash-bound references; stop.

TRP: `singularity-flow explain test-recovery`; risks → `/sf-recover`; no auto-waiver or false passes.

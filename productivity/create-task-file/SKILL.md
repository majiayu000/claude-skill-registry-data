---
name: create-task-file
description: Create a detailed task folder and TASK.md, then create/link a matching GitHub issue and track its URL while open.
engines: [AGNOSTIC]
---

## When to use
Use when a substantial task needs a dedicated instruction file and issue-backed tracking.

Do not use while repository-root `BRAINSTORM.md` is active. Explicitly exit Brainstorm, generate its summary, and obtain an element-to-plan request before creating task state.

## Output
- task file path
- linked GitHub issue URL

## Notes
- The default workflow creates or links a matching GitHub issue.
- Open issue URLs are tracked in `../.hephaera/.cache/tasks/OPEN_ISSUES.md`.
- Use `--no-issue` only for exceptional local-only work.
- If the task already exists as a GitHub issue, use `../commands/import-task-from-issue.sh "<issue-ref>"` instead.
- These task commands require Python 3.9+; they never install it or any packages.

## Execution contract and resumption

Follow the [execution contract](references/execution-contract.md) for substantial ordinary tasks. Populate the generated task's deliverables, acceptance claims, starting state, authorization/capabilities, execution bounds, and continuation from the conversation before implementation. Reuse the canonical acceptance-evidence matrix; ask only for materially missing decisions.

Capture relevant baselines before changing behavior. Record bounded attempts and their observations without imposing an experiment ledger on trivial work. At meaningful stages and before handoff, record a task-local checkpoint of the contract, declared candidate files, and evidence. Validate freshness before resuming and before declaring completion; a handoff is a claim to inspect, not proof of current state.

Existing task files are preserved, not rewritten. Merge missing contract sections when continuing substantial legacy tasks; never silently erase user notes or reset a stopped execution window. Checkpoints do not replace Goal/Gauntlet state or grant publication permission.

Before retrying an uncertain issue creation, reconcile its task-local operation journal with GitHub. An empty remote listing does not establish that a timed-out write failed. Conflicting or unresolved outcomes must stop rather than create duplicates.

## Commands

```bash
../commands/create-task-file.sh "<unique_task_name>" ["Task Title"] [--no-issue]
../commands/record-task-checkpoint.sh "<task_name>" --artifact "<project-relative-file>" --evidence "<saved-evidence-file>" --next-action "<bounded-next-step>"
../commands/validate-task-checkpoint.sh "<task_name>" --phase resume
../commands/validate-task-checkpoint.sh "<task_name>" --phase complete
```

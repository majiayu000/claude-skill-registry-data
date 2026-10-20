---
name: "orchestrating-workflow"
description: 'Coordinate an end-to-end Jira or GitHub work-item workflow from initial fetch through per-task implementation. Use this skill when the user provides a Jira ticket URL, a GitHub issue URL, owner/repo/issue coordinates, says "work on ticket PROJECT-123", "work on issue owner/repo#42", "resume <work-item-key>", "continue this workflow", or asks for status without naming a specific phase. This top-level coordinator detects the platform from the input, loads the matching playbook just-in-time, keeps SKILL.md as a routing layer, and dispatches execution-heavy work to downstream skills or co-located utility subagents.'
---

# Orchestrating Workflow

You are a work-item workflow orchestrator. You do exactly three things:

- **Think** — interpret subagent summaries and current workflow state.
- **Decide** — choose the next phase, gate response, or recovery path.
- **Dispatch** — send work to a downstream skill or utility subagent.

Direct work is limited to reading this skill package, talking with the user, and dispatching helpers. Anything that touches files, the work-item platform, git, the codebase, or the web is delegated.

This skill package is standalone: every reference and utility subagent it owns lives inside this folder. Per-platform contracts live in two playbooks loaded just-in-time. Downstream phase skills are named runtime dependencies invoked by skill name through the host runtime; `preflight-checker` verifies they are available before use.

## Platform Detection

Detect the platform from the first input the user supplies and load the matching playbook for every per-platform decision:

| Signal                                                                                                                                                                                                                                                         | Platform | Playbook                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------- |
| `JIRA_URL` matching `https://<workspace>.atlassian.net/browse/<KEY>`, or `TICKET_KEY` matching a Jira key shape `<PROJECT>-<N>` where `<PROJECT>` contains no dash                                                                                             | `jira`   | [`./references/jira-playbook.md`](./references/jira-playbook.md)     |
| `ISSUE_URL` matching `https://<host>/<owner>/<repo>/issues/<N>` (including GitHub Enterprise), or `OWNER`+`REPO`+`ISSUE_NUMBER`, or `ISSUE_SLUG` matching `<owner>-<repo>-<N>` where the bare value has at least two dash-separated name segments before `<N>` | `github` | [`./references/github-playbook.md`](./references/github-playbook.md) |

Prefer explicit URLs and structured fields over bare resume keys. For unlabeled bare values, classify Jira only when the value has exactly one dash before the numeric suffix; classify GitHub only when it has at least two dash-separated name segments before the numeric suffix. If the input matches neither pattern or remains ambiguous, ask one targeted clarification question before dispatching any subagent.

## Inputs

Primary inputs live in each playbook. The playbook derives the shared workflow key TICKET_KEY, rendered as <KEY>: a Jira ticket key or a GitHub issue slug.

## Workflow Overview

```text
Phase 1: Fetch work item     -> docs/<KEY>.md
Phase 2: Plan tasks          -> docs/<KEY>-tasks.md + planning intermediates
Phase 3: Clarify + critique  -> docs/<KEY>-upfront-critique.md + task-plan updates
Phase 4: Create child items  -> docs/<KEY>-tasks.md updated with child-item links
Phase 5: Plan task execution -> docs/<KEY>-task-<N>-{brief,execution-plan,test-spec,refactoring-plan}.md
Phase 6: Clarify + critique  -> docs/<KEY>-task-<N>-critique.md + decisions.md
Phase 7: Kick off + execute  -> downstream execution summary + progress update
```

Phases 5-7 repeat per task until all tasks complete or the user stops.

## Progressive Loading Map

This is the primary navigation surface. Load only the file that answers the current decision; never preload the whole package.

| Need                                                                                                                        | Load                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Jira platform contract (identifier, transport, phase skills, snapshot sections, write model, status check, external URLs)   | [`./references/jira-playbook.md`](./references/jira-playbook.md)                                                                           |
| GitHub platform contract (identifier, transport, phase skills, snapshot sections, write model, status check, external URLs) | [`./references/github-playbook.md`](./references/github-playbook.md)                                                                       |
| Start, resume, gate rules, escalation summary, examples                                                                     | [`./references/workflow-policy.md`](./references/workflow-policy.md)                                                                       |
| Phases 1-4 procedure (linear pipeline)                                                                                      | [`./references/phases-1-4.md`](./references/phases-1-4.md)                                                                                 |
| Phases 5-7 per-task loop                                                                                                    | [`./references/task-loop.md`](./references/task-loop.md)                                                                                   |
| Exact artifact boundary checks and validator inputs                                                                         | [`./references/data-contracts.md`](./references/data-contracts.md)                                                                         |
| Error recovery, blockers, retry budgets                                                                                     | [`./references/error-handling.md`](./references/error-handling.md)                                                                         |
| Downstream phase skill names, dispatch inputs, dependency checks                                                            | [`./references/downstream-skills.md`](./references/downstream-skills.md)                                                                   |
| Shared concepts, runtime skill docs, web-source handling                                                                    | [`./references/external-sources.md`](./references/external-sources.md), then fetch one URL at a time from the per-playbook routing section |
| Utility work                                                                                                                | The single subagent file from [Subagent Registry](#subagent-registry)                                                                      |

External URLs are optional supporting material. When a bundled contract and a fetched URL conflict, the bundled contract wins.

## Subagent Registry

Use this registry as a lookup table. Read one subagent definition only when you are about to dispatch that subagent.

| Subagent                | Path                                                                           | Purpose                                                                            |
| ----------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `preflight-checker`     | [`./subagents/preflight-checker.md`](./subagents/preflight-checker.md)         | Validate workflow dependencies before starting                                     |
| `artifact-validator`    | [`./subagents/artifact-validator.md`](./subagents/artifact-validator.md)       | Verify phase preconditions and postconditions                                      |
| `progress-tracker`      | [`./subagents/progress-tracker.md`](./subagents/progress-tracker.md)           | Read, create, and update progress artifacts                                        |
| `status-checker`        | [`./subagents/status-checker.md`](./subagents/status-checker.md)               | Query the work-item platform for current state via the playbook-supplied transport |
| `codebase-inspector`    | [`./subagents/codebase-inspector.md`](./subagents/codebase-inspector.md)       | Summarize git branch, changes, and recent commits                                  |
| `code-reference-finder` | [`./subagents/code-reference-finder.md`](./subagents/code-reference-finder.md) | Locate symbols, files, and implementation touchpoints                              |
| `documentation-finder`  | [`./subagents/documentation-finder.md`](./subagents/documentation-finder.md)   | Find relevant docs and return concise summaries                                    |

## Downstream Skill Dependencies

Each numbered phase is owned by a named runtime skill listed in the active playbook's Phase Skill Map. Load [`./references/downstream-skills.md`](./references/downstream-skills.md) only when entering a phase, explaining a missing dependency, or running preflight. If the host runtime cannot invoke the required downstream skill by name, stop at preflight and ask the user to install or enable the missing workflow dependency.

## Output Contract

After each phase or gate, return only:

- A concise phase summary for the user
- The next required decision or confirmation, if any
- The file path, work-item identifier, or task number needed for the next dispatch

Use [`./references/data-contracts.md`](./references/data-contracts.md) for exact phase-boundary checks. Treat each downstream phase skill as authoritative for the internal structure of artifacts it owns.

This workflow maintains Category A1 persistent orchestration records on disk:

- `docs/<KEY>-progress.md`
- `docs/<KEY>-task-<N>-progress.md`
- The downstream phase artifacts listed in [Workflow Overview](#workflow-overview)

Category A1 artifacts are preserved for resumability and are not committed by the orchestrator. Ephemeral Category A2 dispatch payloads, if any, are cleaned up by the workflow that creates them. Implementation artifacts are handled by downstream execution skills.

## Start Or Resume

1. Detect the platform from the input (see [Platform Detection](#platform-detection)) and load the matching playbook.
2. Derive the stable workflow key value using the playbook's identifier-derivation rule: a Jira ticket key or a GitHub issue slug.
3. Dispatch `progress-tracker` with that value under the parameter name `TICKET_KEY` and `ACTION=read`.
4. Decide the resume point from the compact progress summary.
5. Dispatch `preflight-checker` with the workflow key under `TICKET_KEY`, `PLAYBOOK_PATH=<active playbook path>`, and `PHASES=<remaining phase range>`. The active playbook's `Preflight Transport Check` and `Phase Skill Map` rows define what the manifest expects.
6. If you need the resume mapping, gate rules, or standard phase cycle, load [`./references/workflow-policy.md`](./references/workflow-policy.md). If you need the phase-to-skill map, load [`./references/downstream-skills.md`](./references/downstream-skills.md).
7. Load the phase playbook for the current range and proceed one boundary at a time.

If resuming past Phase 1, tell the user what progress was found and confirm before continuing.

## Dispatch Contract

For any subagent dispatch:

1. Read the subagent definition from the registry and tell the subagent to read it at its absolute path resolved from this skill directory.
2. Pass TICKET_KEY and only explicitly needed inputs. When platform-specific behavior is required, pass PLAYBOOK_PATH as the active playbook's absolute path resolved from this skill directory.
3. Collect its structured summary.
4. Retain only the verdict and next-step-relevant details — discard raw file contents, full platform payloads, and large command output.

Parallel dispatch is allowed only for independent summary-producing work, such as pre-task context gathering. Dependent operations remain sequential.

## Escalation

Load [`./references/error-handling.md`](./references/error-handling.md) whenever a critical dependency, artifact, gate, blocker, or retry budget prevents forward progress. Keep only the summary needed to decide whether to retry, re-plan, pause, or ask the user.

## Example

<example>
Input: `JIRA_URL=https://workspace.atlassian.net/browse/PROJ-123`

1. Detect platform: `jira`. Load `./references/jira-playbook.md`.
2. Derive `TICKET_KEY=PROJ-123` from the URL per the playbook.
3. Dispatch `progress-tracker` with `TICKET_KEY=PROJ-123`, `ACTION=read`.
4. No progress found, so dispatch `preflight-checker` with `TICKET_KEY=PROJ-123`, `PLAYBOOK_PATH=<resolved-skill-directory>/references/jira-playbook.md`, `PHASES=1-7`.
5. Read `./references/phases-1-4.md` and enter Phase 1.
6. Invoke the playbook's Phase 1 downstream skill (`fetching-work-item`).
7. Dispatch `artifact-validator` with `TICKET_KEY=PROJ-123`, `PLAYBOOK_PATH=<resolved-skill-directory>/references/jira-playbook.md`, `PHASE=1`, `DIRECTION=postcondition`.
8. Dispatch `progress-tracker` with `TICKET_KEY=PROJ-123`, `PLAYBOOK_PATH=<resolved-skill-directory>/references/jira-playbook.md`, `ACTION=update`, `PHASE=1`, `STATUS=complete`, `SUMMARY="Work item fetched"`.
9. Tell the user: `Work item fetched. Moving to task planning.`

The orchestrator keeps only that summary, the workflow key, the active playbook path, and the next phase. </example>

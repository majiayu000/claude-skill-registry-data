---
name: workflow-orchestrator
description: select and stage a workflow from a repository sensemaking brief. use when the user has a diagnostic brief and wants a workflow plan, prompt chain, guided execution plan, or guarded orchestration with approval gates.
---
# workflow-orchestrator

## Workflow
1. **Consume Brief**: Review the diagnostic brief from `repo-sensemaker`.
2. **Select Workflow**: Match the recommended path to an available workflow in the `workflow-registry.yaml`.
3. **Plan**: Produce a Workflow Orchestration Plan with ordered steps and approval gates.
4. **Mode Selection**: Determine the execution mode (Default: `plan_only`).
5. **Execute/Generate**:
   - `plan_only`: produce the plan and stop.
   - `prompt_chain`: produce copy/paste prompts and stop.
   - `guided_execution`: execute one eligible step, validate its output artifact, write/update the run log, then stop for approval.
   - `autonomous_execution`: execute eligible steps until the next approval gate, failed validation, non-executable skill, or stop condition.
   - `yolo_execution`: execute only eligible steps with no intermediate approval, but stop immediately on missing artifact, invalid handoff, failed validation, non-executable skill, dirty git state, or run-log failure.

## Output Format
Every response must follow the [Workflow Orchestration Plan](references/workflow-orchestration-template.md) structure.
Use [Run Log Template](references/run-log-template.md) only when recording an actual guided or autonomous run.

## Execution Modes
Use [Execution Modes](references/execution-modes.md) as the source of truth. The inline behavior summary in the workflow above is only a control-plane shortcut.

## Boundary Rules
- **Safety First**: Default to `plan_only` mode. 
- **Contract Enforcement**: If a brief does not contain a valid machine-readable handoff, or the requested execution mode is not allowed by [Execution Modes](references/execution-modes.md), the orchestrator MUST refuse the request or downgrade to `plan_only` or `guided_execution`.
- **Handoff Compliance**: Transitions between skills in a workflow MUST comply with the [Artifact Contracts](references/artifact-contracts.yaml).
- **Execution Authority**: The orchestrator may execute only registry-approved steps where `availability.executable_by_orchestrator: true` and `availability.type` is either `local` or `local_command`.
  - `local` means the skill is bundled in this repository.
  - `local_command` means the skill is installed in the local working environment and MUST define an `invocation` block with `runtime`, `command`, `input_artifact`, and `output_artifact`.
  - `external`, `external_required`, and `prompt_only` steps must be treated as routing targets, not executable steps.
- **YOLO Mode Restrictions**: 
    - Requires exact opt-in: `"I choose yolo_execution and accept automated repository changes, feature-branch commits, bypassed gates, and recovery risk."`
    - Requires a feature branch (No direct commits to `main`).
    - Requires a [Run Log](references/run-log-template.md).
- **YOLO Step Completion**:
    - A YOLO step is not complete when a command is merely named.
    - A YOLO step is complete only when the declared `output_artifact` exists, satisfies `artifact-contracts.yaml`, and is recorded in the run log.
    - For `local_command` steps, the orchestrator MUST use the exact `invocation.command`; it must not invent command names.
    - After each step, preserve only the declared output artifact, compact run-log entry, and fields required by the next step.
    - Stop immediately if the command output cannot be mapped to the declared `output_artifact`.
- **Approval Gates**: Do not bypass approval gates in `guided_execution` or `autonomous_execution` mode. Only `yolo_execution` bypasses gates for eligible local/command skills.

## Local Command Execution

When executing a `local_command` step, the orchestrator MUST:

1. Read the skill's `invocation` block from `skill-registry.yaml`.
2. Pass only the declared `input_artifact` plus the minimal necessary context.
3. Invoke the declared `command`; do not invent command names.
4. Treat the declared `output_artifact` as the only valid result of the step.
5. Append a compact run-log entry before continuing.
6. Summarize prior full artifacts once more than one artifact exists in context.
7. Stop if the command, input artifact, output artifact, or runtime is missing.

A `local_command` step is not complete until its declared `output_artifact` exists and satisfies the next handoff contract.

## Hard Stop Conditions
The orchestrator MUST stop and report instead of continuing when any of these occur:
- The skill is `external`, `external_required`, or `prompt_only`.
- The next step is `workflow-orchestrator` itself, unless the mode is `plan_only`.
- The expected output artifact is missing, malformed, or does not satisfy `artifact-contracts.yaml`.
- The selected workflow does not explicitly allow the requested execution mode.
- The run log cannot be created or updated.
- The working tree is dirty before `autonomous_execution` or `yolo_execution`.
- The current branch is `main` or `master` during a mode that can mutate files.
- More than one retry would be required for the same step.
- The current context contains more than one full artifact from prior steps; summarize earlier artifacts before continuing.

## References
- [Workflow Orchestration Template](references/workflow-orchestration-template.md)
- [Skill Registry](references/skill-registry.yaml)
- [Workflow Registry](references/workflow-registry.yaml)
- [Artifact Contracts](references/artifact-contracts.yaml)
- [Execution Modes](references/execution-modes.md)
- [Git Safety Policy](references/git-safety-policy.md)
- [Recovery Policy](references/recovery-policy.md)
- [Approval Gates](references/approval-gates.md)
- [Run Log Template](references/run-log-template.md)

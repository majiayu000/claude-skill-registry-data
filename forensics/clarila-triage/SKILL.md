---
name: clarila-triage
description: "Assess an existing issue for readiness, duplication, priority evidence, dependencies and the appropriate next specialist. Use for intake routing, not issue authoring, reproduction execution or implementation."
---

# Choose the next eligible step

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the actual issue and current source/PR/workflow coverage. Use clarila-issue for missing problem definition and clarila-reproduce when observed behavior is required.
2. Check closed, duplicate, owner-held and already-owned work first. Preserve dispositions and unknown execution rather than queueing replacements.
3. Determine readiness from usable requirements, relevant evidence, repository scope and prerequisites. Derive priority from current authoritative policy and impact, never inflate it to obtain delivery authority.
4. Recommend the responsible engineer and only the specialists the acceptance requires. Product defines expected behavior; technical Plan handles justified dependencies.
5. Record ready, needs-info, duplicate, not-a-bug, blocked or investigation-needed with evidence and a concrete next owner/action. This recommendation is not permission to launch.

For each blocking prerequisite, name the evidence that would make the next step eligible and its current owner. Reassess that prerequisite when a reply or new source arrives, preserving already answered questions and unrelated holds. Distinguish impact/priority from execution readiness. Before recommending duplicate or already-fixed disposition, identify the covering issue/candidate and the integration source where its behavior applies.

The public [triage workflow](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/triage/SKILL.md) informs resumed-question and existing-coverage checks. Use Clarila's actual state vocabulary and current authorization for any provider update.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return readiness, supported priority, duplication/ownership findings, dependencies and a bounded next step.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

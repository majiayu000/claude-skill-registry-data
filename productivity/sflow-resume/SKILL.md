---
name: sflow-resume
description: Resume an existing Singularity Flow work item by ID, check out its branch, load durable workflow state, and identify the correct SDLC phase.
disable-model-invocation: true
argument-hint: "<WORK-ID> [--fetch]"

---
# Resume Singularity Flow work

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Run `singularity-flow resume <arguments>`.
2. The CLI activates the current phase's default governed agent automatically. Do not ask the contributor to select a role. Use `/sf-agent` only when they explicitly request an override.
3. Read `workflow.json`, `STATUS.md`, source context, and approved artifacts from earlier phases.
4. Run `singularity-flow wm check` as a read-only inspection. A missing or stale result never authorizes generation, provider work, file writes, commits, or publication.
5. If grounding is missing, stale, or unreachable, run only the read-only `singularity-flow wm availability --phase <ACTIVE-PHASE> --json`. Take an optional mutation solely from its exact `action.command` or an exact CLI `Run:` command; never infer a rebuild command, add `--task`, or derive scope from the Story title. If no exact command is returned, stop the optional World-Model path and offer `/sf-worldmodel --phase <ACTIVE-PHASE>` without delaying the resumed Story.
6. Before asking to run the optional world-model mutation command, disclose its source revision, views and depth, resolved model/provider or zero-token mode, that the provider may read the repository and write world-model files, and whether the target is the shared governed state branch or an explicitly configured local target. Ask for explicit affirmative consent and wait; do not run the command while waiting. Only an affirmative answer permits that exact command once, unchanged. A decline or unavailable consent leaves grounding untouched and ordinary phase work continues.
7. Verify the checked-out branch exactly matches the work ID.
8. Summarize the active governed agent, completed phases, active phase, rejection reason if present, required output, and world-model readiness. Keep the contributor's Git identity and approval authority separate.
9. Continue only in the active phase; recommend `/sf-phase` for custom phases and do not skip ahead.

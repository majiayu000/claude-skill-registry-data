---
name: sflow-sgos
description: Run an exact Singularity Governed Operating System command without changing its CLI family or bypassing its authority and confirmation boundaries.
disable-model-invocation: true
argument-hint: "<intent|program|process|policy|task|request|evidence|candidate|execution-unit|device|authority-store|pack|memory|meta-tool> <SUBCOMMAND> [arguments]"
---
# Governed SGOS command relay

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Relay one explicitly requested SGOS command to the same CLI family.

1. Require one listed family and an explicit subcommand. Never infer either value.
2. Run `singularity-flow $ARGUMENTS` from the resolved repository and preserve the complete result.
   Never prepend `workflow` or translate it into `singularity-flow workflow ...`.
3. Preserve every CLI model, trust, identity, revision, exact-hash, confirmation, and authority
   check. Never invent a file, ID, choice, approval, credential, digest, or human response.
4. Show a returned preview, plan, confirmation digest, or next command with its effects and stop.
   Confirm only after the contributor explicitly accepts the exact result in a later turn.
5. Never run a returned next command automatically. Execute only the explicitly requested operation
   after all CLI guards pass.
6. Use `/sf-sgos-create` for `singularity-flow intent workflow-guide` and
   `singularity-flow intent workflow-create`; `/sf-learn` for learning; and `/sf-workflows` only for
   the separate `singularity-flow workflow ...` catalog.

Report both equivalent invocations:

- Shell: `singularity-flow $ARGUMENTS`
- Copilot: `/sf-sgos $ARGUMENTS`

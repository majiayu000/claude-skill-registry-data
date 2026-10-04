---
name: sflow-session
description: Select an exact Story, open its managed local checkout or attach from remote, and bind its phase agent.
disable-model-invocation: true

---
# Attach the Copilot session to durable Git state

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; an exact selected workspace/repository is also valid before checkout exists; refuse if neither resolves; never search `$HOME`/parents.

Session setup only: no raw Git, source reads, edits, or lifecycle work. A deferred path is not cwd.

1. Preserve explicit `--workspace <WORKSPACE> --repository <REPOSITORY-ID>` selectors. Partial selectors: resolve only within the explicit workspace or ask; never fill from active workspace/cwd. With none, read `singularity-flow workspace current --json` and carry active `workspacePath`/`repositoryId` explicitly; an old host cwd must not replace that scope. No active workspace: opened Git root or ask. Never guess URLs.
2. Without an explicit work ID, run `singularity-flow session candidates --table` with that scope before status. Relay the entire table, progress, warnings, and scope verbatim; ask with `ask_user` or plain chat for an exact ID if missing, or a row mapped to that table's ID. A current binding or first row is not selection. Stop without attaching if no choice exists; no Home headings. Gaps: `singularity-flow session candidates --json --diagnostics` with the same selectors. Candidate `repositoryPath` is only the scan source, not the destination.
3. For the chosen ID, try `singularity-flow session open-local <WORK-ID> --json` with those selectors. Success opens its managed checkout without remote sync; report `localOnly: true`. Only `SESSION_LOCAL_STORY_UNAVAILABLE` or `SESSION_LOCAL_REPOSITORY_UNAVAILABLE` permits remote fallback. Stop on other refusals.
4. If local opening did not succeed, run `singularity-flow session attach <WORK-ID> --json` with the same selectors. This synchronizes the selected remote Story and returns its checkout. Unsafe or unverifiable state may refuse. Never manually merge, rebase, reset, force-checkout, stash, or discard work.
5. At the returned `repositoryPath`, run `singularity-flow session status --json`; require `ready === true`, `workId` exactly the chosen ID, and `activeAgent` equal the open/attach result's `agent` (`null` is valid for a completed Story). Stop on mismatch before context/nextsteps. Tell shell users to `cd` there. `/sf-agent` requires an explicit override request.
6. There run `singularity-flow session context --work-id <WORK-ID> --slice brief --max-output-bytes 32768 --json`. Never preload the repository.
7. There run `singularity-flow nextsteps <WORK-ID> --json`; report work, commit, agent, phase. For each action preserve order, timing, reason, `Copilot: <copilotCommand>`, and `Shell: <command>` from that same object. Do not merge distinct actions or invent missing routes.
8. For hook refusals, read `singularity-flow logs --event hook --level warn`; `hook.session.initiative` means no Story selection.
9. End the turn; do not continue into Story work.

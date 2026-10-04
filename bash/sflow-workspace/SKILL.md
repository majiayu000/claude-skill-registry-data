---
name: sflow-workspace
description: Select a saved Singularity Flow workspace and repository for this Copilot session, optionally binding the visible context to a Story ID.
disable-model-invocation: true

---
# Switch the active Singularity Flow workspace

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

1. Run `singularity-flow workspace list --table`; relay the complete table verbatim, including inactive rows and warnings. Do not substitute Home or an active-only summary.
2. If empty, check `singularity-flow workspace bootstrap status --json`. Offer an unfinished `/sf-workspace-bootstrap <BOOTSTRAP-ID>` instead of a duplicate. Otherwise offer explicit remote preparation: `singularity-flow workspace prepare <LEAD-URL> --id <ID> --capability <ID> [--lead-capability <ID>] --base <DIRECTORY> --initialize`, or contributor-selected clone preview: `singularity-flow workspace adopt <DIRECTORY> --id <ID> --base <DIRECTORY> --dry-run --json`. Never invent inputs, dirty confirmation, or selection.
3. For existing-clone adoption, show the canonical path, sanitized origin, branch, changed paths, preservation list, workspace-shell target, and `dirtyConfirmationRequired`. State that no fetch, checkout, stash, commit, reset, clean, or remote edit will occur. If dirty, require the contributor to review the paths and approve the exact returned hash; then require the exact workspace ID before running the non-dry-run command.
4. Ask with `ask_user` or plain chat for an exact workspace ID or row number. Map the chosen row to its exact workspace path in that table. IDs can repeat: an ID matching multiple rows requires a row/path choice. Never choose the first or current workspace automatically; ask again on ambiguous or absent answers.
5. Run `singularity-flow workspace status <WORKSPACE-PATH> --level readiness --json` at that exact selected path. This local read supplies repository members without remote calls. If multiple, ask which repository to use; preserve its exact ID and mark the reported lead repository.
6. Preserve any explicitly supplied Story/Jira ID. A workspace choice is not a Story choice or permission to attach a Story; the CLI may report an existing governed branch binding.
7. Run:

   `singularity-flow workspace use <WORKSPACE-PATH> --repository <REPOSITORY-ID> [--story <STORY-ID>] --json`

8. Reproduce the returned `prompt`, workspace, repository, path, `repositoryState`, branch, and Story. A planned `missing` checkout is selectable but not a shell cwd. Use a ready `repositoryPath` for later shell commands.
9. Do not launch nested Copilot. A new terminal session can start with `singularity-flow workspace copilot` in a ready checkout. For a planned checkout, use `/sf-start` or `singularity-flow workspace repair <WORKSPACE-PATH> --repository <REPOSITORY-ID>` first. The Copilot session name contains workspace and Story.
10. The context label is a session banner, not a replacement for Copilot's native `>` marker.

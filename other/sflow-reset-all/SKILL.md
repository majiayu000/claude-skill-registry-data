---
name: sflow-reset-all
description: Preview and explicitly reset the current repository plus machine registration while preserving physical workspaces and clones.
disable-model-invocation: true

---
# Reset repository and machine registration

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Run `singularity-flow reset-all --json` without `--yes` and show the complete remove and preserve lists.
2. Explain that governed repository configuration and machine registration are reset, while physical workspace directories, clones, application source, Git history, installed product surfaces, and VS Code keychain credentials are preserved.
3. Stop for explicit confirmation. Never infer consent from the original request or add `--yes` during preview.
4. Only after a separate confirmation, run `singularity-flow reset-all --yes --json`.
5. Report every changed path and the exact next initialization step. Never substitute factory reset, local reset, fresh install, or reinstall.


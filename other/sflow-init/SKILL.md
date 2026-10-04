---
name: sflow-init
description: Create deterministic smart initialization for a fresh repository, or verify and safely repair existing Singularity Flow assets without overwriting repository customizations.
disable-model-invocation: true
argument-hint: "[WORK-ID] [--base BRANCH] [--fetch]"

---
# Verify or repair branch initialization

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Setup only: do not implement, submit, approve, reset, stash, force-push, or edit customizations.

For explicitly requested smart or zero-manual initialization, require a fresh repository:

1. Run `singularity-flow init --smart-detect --dry-run --json` once. Show stacks, commands, gaps,
   suggestions, write set, and proposal SHA-256. Never run a detected command.
2. Ask explicitly about unresolved candidates and optional protections. Never infer ambiguity or
   select unchecked suggestions.
3. Show `--accept-proposal <file> --confirm <sha256>`; use `--yes` only after explicit acceptance.
4. Activate only after exact confirmation. Preserve the receipt, commit, readiness, and next
   command. Proposal-only and review-proposal files are not active law.
5. Run metadata-only `singularity-flow precheck --quick --json`. Offer Copilot `/sf-ready` and
   Shell `singularity-flow precheck --run --scope dependency-test --json`. Only the readiness flow
   (`/sf-ready` or its shown Shell equivalent)—not init—executes the confirmed repository plan.

On `INI_RECOVERY_REQUIRED`, run only its exact
`singularity-flow init --recover --proposal <SHA256> --json`; never edit its journal.

For ordinary `init`, `--check`, or `--repair`, continue with the compatible workflow below.

1. Run `singularity-flow init --check --json` first. Show branch, completeness, missing files, and
   validation errors.
2. Validate a supplied Work ID as letters, numbers, `.`, `_`, or `-`. If its branch is current, use
   `singularity-flow init --repair`. Otherwise require a clean tree and run
   `singularity-flow init --repair --work-id <WORK-ID> --base <BASE> --fetch`
   to create, reuse, or fast-forward it. Default to `main` only for a new branch; never modify base.
3. When no Work ID was supplied and the check reports missing assets, run
   `singularity-flow init --repair` on the current branch.
4. Restore only missing packaged files; never replace customization. Restore invalid files from Git.
5. Rerun `singularity-flow init --check --json`, then run
   `singularity-flow doctor --offline --json`. Report every remaining failure
   and warning with its exact fix.
6. Show `git status --short` and added files. Do not commit or push repair automatically.
7. Before the first Story, offer `/sf-ready` and
   `singularity-flow precheck --run --scope dependency-test --json`.

If the initial check is complete, make no changes and say that the branch is
already initialized.

---
name: sflow-doctor
description: Check whether this repository is healthy, and what to fix.
argument-hint: "[work ID] [--offline] [--performance]"

---
# Diagnose setup and recovery

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

1. Run `singularity-flow workspace current --json`. When it returns a repository, use only its exact
   `repositoryPath` as cwd; when it returns no selected repository, do not search for one.
2. With a repository, run `singularity-flow init --check --json`, then
   `singularity-flow doctor $ARGUMENTS`. Report each failure with its exact safe fix and summarize
   warnings separately. The initialization check covers workflow, portfolio, templates, prompts,
   and governed-agent files on the current branch. Recommend `/sf-init` when assets are missing.
3. Without a repository, run `singularity-flow workspace doctor --json`. It is machine-local and
   offline by default. Add `--network` only after the contributor explicitly chooses to contact the
   remotes named by unfinished bootstrap sessions. Relay proxy and certificate configuration source
   names, never their values; never request credentials or recommend disabling TLS.

All checks above are read-only. Do not reset, stash, switch branches, or edit configuration unless
the user explicitly asks you to apply a fix.

When the user asks about monorepo or Git slowness, pass `--performance --json`.
Relay the measured total/scoped file counts, warm status/fingerprint times, clone
mode, and recommendations. The benchmark is read-only: never enable FSMonitor,
untracked cache, sparse checkout, or a partial-clone fallback on the user's
behalf merely because the report recommends evaluating it.

When a failure is not explained by the current state, read what actually happened with `/sf-logs` — `singularity-flow logs --level warn` shows recent failures and refused tool calls, including the reason a hook blocked a command. Diagnose from the log rather than retrying blindly.

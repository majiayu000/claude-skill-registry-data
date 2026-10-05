---
name: do-init
description: Initialise a project for use with Maverick — verifies the GitHub App, installs the CLI if needed, writes the project config with integration tracking, scaffolds docs, generates project skills, runs an initial cybersecurity audit, then commits the changes and opens a PR.
user-invocable: true
disable-model-invocation: true
context: fork
---

# Init Maverick Project

Set up the current repository for Maverick — install the CLI if needed, validate the Maverick GitHub App, write the project-level config, scaffold docs and project skills, run the cybersecurity audit, then commit everything and open a pull request for the user to approve.

## Execution Context

This skill runs in its own forked context (`context: fork`) — you are
executing it directly; there is no separate agent to dispatch. Follow the
process below exactly and end with the structured result in the Return
section. Do not modify the user's project source code, perform git
operations beyond what the process prescribes, or provision
infrastructure.

## Process

### 1. Ensure the Maverick CLI is installed and matches the plugin

Run `command -v maverick` to check whether the CLI is already on PATH.

**If `maverick` is not on PATH**, dispatch the **/maverick:do-install** skill and wait for it to complete. After the install returns, re-run `command -v maverick` to confirm the binary is now resolvable. If it still is not (e.g. `~/.local/bin` is not on the user's PATH), report the install message verbatim to the user and stop — they need to fix PATH and re-invoke `/maverick:do-init` manually.

**If `maverick` is on PATH**, verify the installed CLI matches the loaded plugin. A stale binary from an earlier plugin version can be missing subcommands the rest of this skill depends on (e.g. `maverick integration`, `maverick preflight`).

- Read the installed CLI version: `maverick --version`
- Read the plugin version: `grep -Po '(?<=^version = ")[^"]+' "${CLAUDE_PLUGIN_ROOT}/pyproject.toml"`
- If they differ, dispatch **/maverick:do-install** to refresh the CLI. That skill always runs `uv tool install --force` from the plugin root, so it overwrites whatever is currently installed. After it returns, re-run `maverick --version` and confirm it now matches the plugin version. If it still does not, surface the mismatch to the user and stop.
- If the versions already match, skip to step 2.

`do-init` cannot complete without a CLI version that matches the plugin. The remaining steps invoke `maverick` directly and depend on subcommands that may have been added in newer versions.

### 2. Preflight — verify the Maverick GitHub App exists

Run:

```bash
uv run maverick preflight do-init
```

This runs the same `gh_app_configured` runtime check the issue-driven
workflows enforce. If it exits non-zero, **halt do-init immediately** and
report the stderr output verbatim to the user. The remaining steps make
file changes and open a PR; running them on a machine without a working
GitHub App is wasted work because nothing downstream of `do-init` will
function until the App is set up.

Maverick **does not** create the GitHub App. That is a manual human
action. If preflight fails, surface this to the user verbatim:

> The Maverick GitHub App is not configured. Maverick cannot create it
> for you — you need to do this manually before re-running `/maverick:do-init`.
>
> 1. Create a new GitHub App at <https://github.com/settings/apps/new>
>    with these permissions: contents: read, metadata: read,
>    pull-requests: write, issues: write.
> 2. Generate and download a private key for the App. Save it to
>    `~/.maverick/maverick-gh-app.pem` (or any path you prefer).
> 3. Install the App on the repo(s) you want Maverick to operate on.
>    Note the `installation_id` from the install URL.
> 4. Add a `gh_app` block to `~/.maverick/config.json`:
>
>    ```json
>    {
>      "gh_app": {
>        "app_id": <integer>,
>        "installation_id": <integer>,
>        "private_key_path": "~/.maverick/maverick-gh-app.pem"
>      }
>    }
>    ```
>
> 5. Verify with `maverick gh-app status` — it should print
>    `"configured": true`.
> 6. Re-run `/maverick:do-init`.

### 3. Initialise the project config

Run:

```bash
uv run maverick init
```

This detects the project's tech stack, writes `.maverick/config.json` with the detected modules and a fresh `integration` block (`init: true`, all other flags `false`), and prints a summary of what was detected. If a config already exists, the command preserves any integration flags that are already `true` — re-running is safe.

### 4. Initialise project-level overrides

Write `.maverick/settings.json` containing `{}` if the file does not already exist. This is where project-specific overrides go later; an empty object is the correct default. Do not overwrite an existing file.

### 5. Scaffold the technical documentation

Dispatch **/maverick:do-docs**. The greenfield mode of that skill flips `integration.tech_docs_scaffolded` to `true` automatically when it completes.

### 6. Generate project skills

Dispatch **/maverick:do-upskill**. It iterates every topic in `topics.json` and writes per-topic skills under `docs/maverick/skills/`, then flips `integration.upskill` to `true`.

### 7. Run the cybersecurity review

Dispatch **/maverick:do-cybersecurity-review**. It scans the existing codebase for common security risks (secrets, dependency vulnerabilities, auth/input-validation patterns), writes findings to `docs/security-audit.md`, and flips `integration.cybersecurity_reviewed` to `true`. The review is surface-only — it reports, it does not modify code. Any FAIL findings should be tracked as follow-up issues by the user.

### 8. Commit changes and open a pull request

The earlier steps wrote a number of new and modified files. Commit them on a fresh branch and open a PR for the user to approve.

1. **Sanity-check the working tree.** Run `git status --porcelain`. The only changed paths should be:
   - `.maverick/config.json`, `.maverick/settings.json`
   - `docs/maverick/skills/...` (from `do-upskill`)
   - `docs/...` content created by `do-docs` greenfield
   - `docs/security-audit.md` (from `do-cybersecurity-review`)

   If `git status` shows changes outside these paths, **abort and report to the user** — they have unrelated uncommitted work that should be handled first.

2. **Resolve base + branch.** Capture the current branch as the PR base:
   ```bash
   base="$(git branch --show-current)"
   ```
   Choose a branch name `chore/maverick-init`. If a branch with that name already exists locally or on `origin`, abort and tell the user — a previous init attempt may be in-flight.

3. **Create the branch and stage maverick paths only.**
   ```bash
   git checkout -b chore/maverick-init
   git add .maverick/
   [ -d docs/maverick ] && git add docs/maverick/
   [ -f docs/security-audit.md ] && git add docs/security-audit.md
   # Stage anything else under docs/ that do-docs greenfield created.
   git add -u docs/ && git add docs/
   ```
   Do **not** use `git add -A` or `git add .` — the goal is to stage only what `do-init` produced, not anything the user happened to leave in the tree.

4. **Commit** with a conventional message:
   ```bash
   git commit -m "chore: initialise Maverick"
   ```

5. **Push and open the PR**:
   ```bash
   git push -u origin chore/maverick-init
   gh pr create --base "$base" \
       --title "chore: initialise Maverick" \
       --body "$(cat <<'EOF'
   ## Summary

   This PR was generated by `/maverick:do-init`. Review the changes and merge when ready.

   ### What's in this PR
   - `.maverick/` — project config and integration tracking
   - `docs/maverick/skills/` — generated project-specific skills
   - `docs/security-audit.md` — initial cybersecurity audit findings (review FAIL items)
   - Other `docs/` content scaffolded by `do-docs`

   ### Verify after merge
   ```bash
   uv run maverick integration get
   ```
   EOF
   )"
   ```

6. Capture the PR URL from the `gh pr create` output and pass it through to the report in the next step.

### 9. Report

Print a final summary to the user:

- Detected modules (from step 3's output)
- Whether docs were scaffolded greenfield or already existed
- How many project skills were generated
- The number of security-audit findings at each severity, and the path to the audit report
- The current integration state: `uv run maverick integration get`
- The PR URL from step 8
- A one-line note that PR code review now runs locally as the `agent-code-reviewer` subagent during `do-issue-solo` / `do-epic`. If the project later wants the optional CI-side gate (multi-machine workflows, untrusted environments, audit needs), point the user at `mav-bp-remote-code-review` for the manual scaffold steps.

The integration checklist gives the user (and any future Maverick session) a clear view of what's been completed and what's still pending.

<!-- maverick-plugin-version: 4.0.2-dev -->

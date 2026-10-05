---
name: code-commit
description: Commit current changes using jj. Analyzes changes, suggests commit messages following repository conventions, splits when needed, and creates commits.
---

Commit current changes using Jujutsu (jj).

## Important

- Read the `jujutsu` skill before running any `jj` command.

## Commit Message Style

Commit messages provide a high-level overview of the change, NOT a detailed breakdown. They capture the _Why_ (reason/motivation), distinct from the _How_ (code) and _What_ (test code).

- **Prefer single-line messages**: Use a single subject line when the subject is sufficient to explain the change.
- **Strict body limit**: If a description body is necessary (to explain why or capture non-obvious context), keep the body within 3 lines maximum. Do not exceed 3 lines unless there is a strong reason; justify this reason to the user before creating the commit.
- **Focus on intent**: Explain the high-level why and the affected subsystem; do not enumerate file-level changes.
- **Do not enumerate changes**: Do not include file lists, change tallies, or bullet lists of modified files; the diff already shows these.
- **Keep it concise**: Reader understands the purpose at a glance without re-reading the diff.
- Follow the `jujutsu` reference for line length (<= 72 chars per line), mood, and style conventions.

### Examples

- **Bad (enumerating files and changes)**:

  ```
  update flake.nix, profiles/terra.nix, and nixos/system.nix to bump package versions and add wireguard module

  - Bumped lofi to v0.2.2
  - Added wireguard configuration module in nixos/system.nix
  - Updated terra profile to include wireguard
  - Modified flake inputs
  ```

- **Good (single-line)**: `profiles/terra: enable wireguard support and update packages`
- **Good (short body, within 3 lines)**:

  ```
  profiles/terra: enable wireguard support

  Wireguard replaces the previous OpenVPN tunnel for peer-to-peer routing.
  ```

- **Bad (overly detailed)**: `fix typo in home-manager/config/git.nix line 42 and rename git.nix to git-config.nix`
- **Good**: `hm/git: correct configuration typos and rename module`

## Process

### Step 0 - Load Jujutsu Skill

- Review the `jujutsu` skill and follow its Best Practices for local commit autonomy, revision references, logical grouping, and message style.

### Step 1 - Analyze Changes

- `jj diff -s` to inspect changed files; `jj diff` for the full diff.
- Focus on any user-specified files or paths.

### Step 2 - Analyze Existing Convention

- `jj log -r ::@ -n 20 --no-graph -T 'description ++ "\n---\n"'` to extract conventions:
  - Identify the scope prefix pattern (path-based like `<dir>/<name>:`, module, or component names).
  - Determine if conventional prefixes (`feat:`, `fix:`, `chore:`) are used; omit them if absent from history.
  - Note mood and separator conventions.

### Step 3 - Execute Commit

- Derive the message primarily from the diff, not conversation context, unless context explains an unobvious change. Follow **Commit Message Style** (prefer single-line; body within 3 lines maximum; justify to the user beforehand if exceeding 3 lines).
- If changes are logically distinct, split them (one message per split; do NOT use interactive `jj split`).
- Refer to the `jujutsu` reference for exact `jj commit` / `jj split` syntax and the commit+advance workflow.
- `jj commit` leaves the new working-copy `@` ready for new changes.

### Step 4 - Verify Line Lengths

- Run the `check-commit-msg.sh` script in this skill directory:
  - Reference it by absolute path; do NOT `cd` into the skill directory (`jj` must run in the repo working directory).
  - `/path/to/check-commit-msg.sh [REV]` where `REV` is a jujutsu revision/alias or git revision/ref.
  - `/path/to/check-commit-msg.sh -h` for all options.
- If any line exceeds the limit (per `jujutsu`), fix with `jj describe <rev> -m "<fixed-message>"`.

### Step 5 - Report

- Display resulting commit(s) with `jj log -r @- -n 1` (or more if split).
- For each commit, report its message and, if split, the reasoning and scope.

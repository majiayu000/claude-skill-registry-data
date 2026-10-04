---
name: git-submodule-manager
description: >
  Git worktree creation/switching, submodule branch synchronization, and monorepo commit/push management.
  Triggers on "worktree", "submodule", "branch sync", "create feature branch",
  "서브모듈", "브랜치 동기화", "feature 브랜치 생성" requests.
---

# Worktree Manager Skill

Unified Git worktree and submodule management for any monorepo with git submodules — no per-repo edits needed.

## Submodule Discovery

Submodule paths and default branches are auto-detected from `.gitmodules` at runtime — nothing is hardcoded in the scripts:

1. **Submodule list**: read directly from `.gitmodules` (`git config --file .gitmodules --get-regexp path`)
2. **Default branch per submodule**, in order:
   - the `branch = ...` entry in `.gitmodules`, if the repo owner set one via `git submodule set-branch --branch <branch> <path>`
   - otherwise, the submodule's own remote HEAD (`origin/HEAD`)

To pin a submodule to a non-default branch (e.g. an AI-only backend that tracks `develop-ai` instead of `develop`), run `git submodule set-branch` once in the target repo and commit the resulting `.gitmodules` change — the scripts pick it up automatically, no config file to maintain.

## Token-saving output modes

Every script accepts `--quiet` / `-q` alongside `--yes` / `-y`. It collapses output to one line per repo (no banner, no per-file diff dump) — **prefer `--quiet` for routine status/commit/push checks** so the tool output read back into context stays small. Only omit it when the user explicitly wants to see full file-level detail.

## Script Paths

All scripts use plugin-root-relative paths:
```
skills/git-submodule-manager/scripts/
├── _config.sh    # Shared config (auto-sourced)
├── create.sh     # Create worktree
├── status.sh     # Show status
├── commit.sh     # Unified commit
├── push.sh       # Unified push
├── pull.sh       # Unified pull
└── switch.sh     # Branch switching
```

## Operation Guides

### CREATE — Create Worktree

Creates a new worktree plus matching submodule branches for feature development.

**Triggers**: "create a worktree", "new feature branch", "feature worktree", "worktree 만들어줘", "새 기능 브랜치"

**Procedure**:
1. Confirm feature name and base branch (default: `main`)
2. Summarize what will be created:
   - Worktree path: `../{repo-name}-{feature-name}` (repo name is read from the current checkout, not hardcoded)
   - Main branch: `feature/{feature-name}` (from main)
   - Submodule branches: same feature branch name on each submodule
3. Run after user confirmation:
   ```bash
   bash skills/git-submodule-manager/scripts/create.sh {feature-name} {base-branch} --yes
   ```

---

### STATUS — Show Status

Displays the current worktree and the state of every submodule.

**Triggers**: "worktree status", "check branches", "submodule status", "상태 확인", "브랜치 확인"

**Procedure**:
1. Run directly (no confirmation needed), defaulting to `--quiet` unless the user wants full detail:
   ```bash
   bash skills/git-submodule-manager/scripts/status.sh --quiet
   ```
2. Parse output and report issues:
   - DETACHED HEAD → recommend checking out a branch
   - Branch mismatch → suggest the `switch` command
   - Unpushed commits (↑N) → suggest the `push` command

---

### COMMIT — Unified Commit

Commits all changed submodules and the main repo with the same message.

**Triggers**: "commit", "commit changes", "commit all", "커밋해줘", "변경사항 커밋"

**Procedure**:
1. Determine commit message:
   - If provided as argument: use it verbatim
   - Otherwise: analyze changes and generate a Conventional Commits–style message
     (`feat:`, `fix:`, `docs:`, `chore:`, etc.)
2. Summarize changes per submodule (`--quiet` shows changed-file counts only, not every path)
3. Run after user confirmation:
   ```bash
   bash skills/git-submodule-manager/scripts/commit.sh "{commit-message}" --yes --quiet
   ```
4. **Commit order**: each changed submodule (in `.gitmodules` order) → main (main includes submodule pointer updates)

---

### PUSH — Unified Push

Pushes submodules and the main repo that have unpushed commits to their remotes.

**Triggers**: "push", "push to remote", "push all", "푸시해줘", "원격에 올려줘"

**Procedure**:
1. List push targets with unpushed commit counts
2. ⚠️ On `--force`: warn about the risk and require explicit confirmation
3. Run after user confirmation:
   ```bash
   bash skills/git-submodule-manager/scripts/push.sh [--force] --yes --quiet
   ```
4. **Push order**: each submodule with unpushed commits (in `.gitmodules` order) → main

---

### PULL — Unified Pull

Fast-forward pulls the main repo and every submodule from their remote.

**Triggers**: "pull", "pull latest", "sync from remote", "풀받아줘", "최신 받아줘", "git pull"

**Procedure**:
1. Parse optional branch name:
   - If provided: pull that branch on main repo + all submodules (checkout first if needed)
   - If omitted: pull each repo's **current** branch
2. Abort if any repo has uncommitted changes (prevents merge conflicts)
3. Show the pull plan (per-repo target branch)
4. Run after user confirmation:
   ```bash
   bash skills/git-submodule-manager/scripts/pull.sh [branch-name] --yes
   ```
5. Uses `--ff-only` — stops on non-fast-forward (prevents accidental merge commits)
6. **Pull order**: main → each submodule in `.gitmodules` order (main first so submodule pointers stay current)

---

### SWITCH — Branch Switch

Switches branches on the main repo and every submodule at the same time.

**Triggers**: "switch branch", "checkout", "switch to", "브랜치 전환", "브랜치 바꿔줘", "체크아웃"

**Procedure**:
1. Confirm target branch name and optional `--create` flag
2. Check for uncommitted changes (abort if any exist)
3. Run after user confirmation:
   ```bash
   bash skills/git-submodule-manager/scripts/switch.sh {branch-name} [--create] --yes
   ```

---

## Cautions

- **Submodules first, always**: for commit/push, submodules must be processed before the main repo
- **Watch for detached HEAD**: verify the branch on every submodule before making changes
- **`--force` push**: do not use during team collaboration — requires explicit user consent
- **Main repo pointer updates**: submodule pointer changes are staged on the main repo automatically after submodules commit

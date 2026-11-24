---
name: github
description: "Use for Git and GitHub work. Commits, pushes, pulls, branches, PRs, PR red-team reviews, git guardrails/safety hooks, conflicts, stash, sync flows."
invocation: discipline
operad_source_colours: ["State"]
operad_target_colour: "State"
operad_arity: 1
operad_residual: "unknown"
---

# GitHub and Git Operations

**Deprecated skills:** `0-oe-commit`, `master-github-manager`, `commit`, `techne-qa-pr-reviewer`, `git-guardrails-claude-code` (all archived and consolidated here).

## Core Principles & Strict Push Directives

> [!IMPORTANT]
> **STRICT PUSH DIRECTIVE:** YOU MUST NEVER PUSH DIRECTLY TO ORIGIN/MAIN UNLESS AUTHORIZED BY A HUMAN. ALWAYS CREATE A PR AND AWAIT REVIEW OR MERGE SIGNAL.
>
> **STRICT STAGING & COMMIT DIRECTIVE:** Stage only explicitly named paths. Never use `git add .`, `git add -A`, or commit anything under `target/**`.

- **Policy:** `.sentinel/policies/git_discipline.md`
- **Version:** 2.3.0 (CPPMS, 0-oe-commit, techne-qa-pr-reviewer & git-guardrails-claude-code consolidation)

---

## When to Activate

Use this skill for any Git or GitHub operation:

- Automated CPPMS (Commit, Push, PR, Merge, Sync) workflows
- Committing changes ("commit", "stage", "pathspec land")
- Pushing to remote ("push", "push branch")
- Pulling or fetching ("pull", "fetch", "sync")
- Branch & worktree management ("branch", "checkout", "switch branch", "worktree")
- Pull requests ("PR", "pull request", "create PR", "merge PR")
- PR red-team audits & quality review ("review PR", "audit PR", "run red team PR review", "PR review", "techne-qa-pr-reviewer")
- Claude Code git safety hooks & command guardrails ("block dangerous git", "git guardrails", "git safety hooks", "git-guardrails-claude-code")
- Merge and conflict resolution ("merge", "conflict", "rebase")
- Emergency recovery ("git is stuck", "detached HEAD", "push rejected")
- Markdown isolate & stash management ("stash", "quote stash refs")

---

## Automated CPPMS Workflow (Commit, Push, PR, Merge, Sync)

When performing automated landing or multi-step PR creation:

1. **Pre-flight Inspection & Locus Ancestry:**
   - **Ensure Linear Ancestry with Main:** Run `git fetch origin main && git merge origin/main --no-edit` to verify that `origin/main` is an immediate ancestor of `HEAD` (`merge-base origin/main HEAD == origin/main`). This prevents `REFUSE_UNTIL_WITNESSED` locus preflight failures during automated CI/QA review (`review_pr.py`).
   - Run `git status` and `git diff --staged` to inspect the exact payload before staging.
   - Before editing, compare every protected evaluator path in the candidate tree with the exact trusted-head baseline. Ordinary repairs change inputs, recipes, fixtures, or callers; they do not change protected evaluator bytes.
   - Reproduce the named failing gate directly and run only its targeted tests while repairing.
   - For release-envelope custody gates and PR-authored versus merge-result scope rules, consult [Release-Envelope Custody & PR Scope](references/release_envelope_and_pr_scope.md).
2. **Selective Pathspec Staging — the only admitted path:**
   - **Stage only explicitly named paths. Never use `git add .`, `git add -A`, or commit anything under `target/**`.**
   - Stage with an explicit pathspec: `git add -- <files>`. Every path is named because someone decided to include it.
   - **Never** commit anything under `target/**` (including build outputs, transient caches, or nested worktrees).
   - **Never** commit unpacked CAS storage (`_intelligence/harvest/vault/**`). Unpacked cache trees belong in `.gitignore`; only sealed archives (`harvest_vault_archive.zip`) and audited manifests are tracked.
   - **Never** author a commit or PR described as "sync all local changes", "filesystem sync", or "sync working tree".
   - Before staging, verify the payload is exactly the intended set:
     ```powershell
     git status --short
     git add -- <files>
     git diff --cached --name-status
     git diff --cached --name-only | ForEach-Object { ($_ -split '/')[0] } | Group-Object -NoElement
     ```
3. **Pre-Commit Index Re-Verification & Gate Checks (`goo-precommit-index-reverify`):**
   - Snapshot `git diff --cached --name-only` immediately before `git commit`. Refuse commit if index drifts after pathspec add.
   - **Republication Checklist Pre-Commit Gate:** Execute the pre-commit gate before committing:
     ```powershell
     py -3.12 -m operations.use_cases.cicd.republication_checklist_gate
     ```
     Commit is permitted only when receipt status is `PASS`.
4. **Commit & Branch Push:**
   - Commit with descriptive title and Co-Author attribution.
   - Push feature branch to origin: `git push -u origin <branch-name>`.
5. **PR Creation & Merge Verification:**
   - Create PR using GitHub CLI: `gh pr create --title "..." --body "..."`. In PowerShell environments where multiline descriptions or markdown backticks may suffer quote escaping issues, write to a scratch file and use `gh pr create --title "..." --body-file "<path/to/pr_body.md>"`.
   - Await human merge signal or automated review checks before merging.
   - Land with a merge commit: `gh pr merge <n> --merge`. **Never `--squash`.**
   - Before pushing, report the changeset shape to the human — counts by change type (A/M/D) and by top-level directory.
6. **Local Sync & Worktree Cleanup:**
   - Update local main ref (`git fetch origin main:main`). If `main` is checked out in another active worktree (refusing direct ref update), update tracking refs with `git fetch origin --prune` and switch to detached `origin/main` (`git checkout --detach origin/main`) or a dedicated worktree branch.
   - Delete merged local feature branch (`git branch -d <branch-name>`), delete remote feature branch (`git push origin --delete <branch-name>`), and run `git fetch --prune`.

---

## Red-Team PR Review & Quality Gates (`techne-qa-pr-reviewer`)

**AuthorityEffect:** None

### Quick Command

```bash
py -3.12 -m governance.infrastructure.cicd_process_flow.review_pr <PR_NUMBER_OR_URL> --trusted-repository <ABSOLUTE_CLEAN_TRUSTED_REPOSITORY> --trusted-head <40_HEX_TRUSTED_HEAD> --output-dir <ABSOLUTE_EXTERNAL_AUDIT_DIRECTORY>
```

### What It Does Automatically

1. **Fetches PR Metadata**: Resolves branch, head SHA, title, and base ref via `gh pr view`.
2. **Worktree & Locus Resolution**: Finds active worktree or checks out PR branch cleanly without polluting active git state.
3. **Red Team ChatGPT Red Team v2 Quality & Truth Gate**:
   - **Census Verification**: 59 explicit `[workspace].members` paths, 60 resolved packages (`cargo metadata --no-deps`).
   - **Authority Fencing**: Asserts `ExecutionAuthority: NONE` on expansion roadmaps & `HISTORICAL_SNAPSHOT` on past audits.
   - **Operad Validation**: Verifies 0 errors in `.agents/operad/validate_operad.py`.
4. **Audit Report Artifact Emission**: Emits `_intelligence/omc_dags/omc_report_pr{NNNN}.md` and `.jsonl`.
5. **GitHub Comment Posting**: Posts formal audit comment directly to GitHub PR using `gh pr comment`.
6. **Direct URL Return**: Returns the direct URL of the posted comment.

### Mandatory Fast Repair Loop

1. Bind the base and candidate head, then compare all protected evaluator paths with the exact trusted-head baseline **before editing**.
2. Reproduce the named failing gate directly and run its targeted tests.
3. For executable runbook fences (`bash`, `sh`, or empty), write one complete command per line. Do not use backslash continuation.
4. Freeze the candidate head, run canonical review once, and bind the receipt/comment to that head. Never rerun an unchanged refusal.
5. Before expensive tests, resolve claimed runbook paths and Cargo targets in a clean exact-head tree.
6. Check disk budget before builds, reuse one scoped target cache, and remove only verified ignored caches.

### Specialized PR Review & Quality Gates

Detailed operational rules for PR review gates are located in [Specialized PR Review & Quality Gates](references/specialized_pr_review_and_quality_gates.md):
- **SHA-256 Content Hash Honesty Gate**
- **PR Relocation Bijection Guard**
- **Reserved Word & Valid Identifier Guard**
- **Tree-Diff Merge Isolation & Worktree Safety**
- **Local HTTP Containment & PR Trigger Coverage**

---

## Consolidated Operational Git Guards (`goo-` Track)

1. **Shared Checkout Capital Re-apply Guard (`goo-shared-checkout-capital-reapply-guard`)**:
   - Pathspec-commit session capital early. Refuse destructive commands on shared `main` when foreign WIP is present.
2. **Main-Ref Sync Without Checkout & Worktree Collision Guard (`goo-main-ref-sync-without-checkout`)**:
   - Use `git fetch origin main:main` to update local `main` ref directly without checking out `main` when blocked by foreign WIP.
   - **Linked Worktree Collision**: If `main` is checked out in another worktree (`git worktree list`), `git fetch origin main:main` fails with `fatal: refusing to fetch into branch 'refs/heads/main' checked out at ...`. Do not force or mutate that worktree; instead run `git fetch origin --prune` and switch to detached `origin/main` (`git checkout --detach origin/main`).
3. **Pre-Commit Index Re-Verification (`goo-precommit-index-reverify`)**:
   - Snapshot staged files immediately before `git commit` and refuse commit if index drifts after pathspec add.
4. **PowerShell Git-Ref Quote Guard (`goo-pwsh-git-ref-quote-guard`)**:
   - Quote all git revisions and range expressions containing `@` in PowerShell (e.g. `'@{u}..HEAD'`, `'HEAD@{1}'`, `'stash@{0}'`). Unquoted `@{...}` triggers PowerShell hash literal syntax errors (`ParserError: Missing '=' operator after key in hash literal`).
5. **Foreign Untracked Markdown Isolation (`goo-precommit-foreign-untracked-md-isolate`)**:
   - When untracked foreign markdown causes pre-commit lint blocks, isolate with:
     ```powershell
     git stash push -u -m "foreign-wip isolate for pathspec commit" -- <foreign-paths...>
     git stash pop "stash@{0}"
     ```
6. **Untracked Stash Inspection & Recovery Protocol (`goo-untracked-stash-recovery`)**:
   - When uncommitted files are missing after branch switching, inspect untracked stash commit refs (`stash@{N}^3`) and recover missing paths via `git checkout "stash@{N}^3" -- <paths...>`.
7. **Optional Education Diagnostics**:
   - `py -3.12 -m operations.use_cases.cicd.education_strands_gate` remains available for scoped diagnostics. It is not a commit or merge requirement; report its actual coverage and failures without treating removal of the requirement as a passing result.
8. **GitHub CLI GraphQL Token Scope Guard (`goo-gh-graphql-pat-scope-guard`)**:
   - Avoid bare `gh pr view <number>` when verifying PR merge status. Default queries inspect commit status check rollups, failing with `GraphQL: Resource not accessible by personal access token` on restricted tokens. Use explicit JSON projections: `gh pr view <number> --json state,mergedAt,mergeCommit,url`.

---

## Worktree Sandbox Protocols

See [Worktree Sandbox Protocol](references/worktree_sandbox_protocol.md) for complete instructions on:
- Paper pathspec landing (MD, claim ledger, action plan, indexes, receipts).
- Dirty shared checkout clean worktree landing workflow.
- Emergency recovery and playbooks: [Playbooks & Recovery](references/playbooks_and_recovery.md).

---

## Claude Code Git Guardrails & Safety Hooks (`git-guardrails-claude-code`)

**AuthorityEffect:** None

Sets up a `PreToolUse` hook for Claude Code that intercepts and blocks dangerous git commands (`git push`, `git reset --hard`, `git clean -fd`, `git branch -D`, `git checkout .`, `push --force`, `reset --hard`) before execution.

The bundled interception script is located at `scripts/block-dangerous-git.sh`.
For complete configuration, scope selection (project vs global), settings JSON, and verification steps, see [Claude Code Git Guardrails](references/claude_code_git_guardrails.md).

---

## De-Linting & Encoding Cleanliness (`RULE_MARKDOWN_DELINTING_001`)

Every file created or modified during the execution of this skill MUST be de-linted prior to turn completion. Run `/techne-docs-lint-hunter-killer` or `npx markdownlint-cli --fix` to verify **0 linter errors and 0 linter warnings**, and ensure UTF-8 encoding cleanliness (`RULE_UTF8_MOJIBAKE_CLEANLINESS_001`).

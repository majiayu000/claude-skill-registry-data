---
name: public-repo-git-gate
description: Run the public-repository gates for Git commits, pushes, and pull requests. Check staged and untracked scope, secrets and personal data, internal material, branches and remotes, PR base/head, CI, and merge prerequisites. Use when the user asks to commit, push, open a PR, review public repository content, or run the complete public-repository gate.
---

# Public Repository Git Gate

Treat Git commits, remote pushes, and pull requests as sequential public-content
gates. `.gitignore` is not a security boundary; inspect what Git will actually
commit or has already put under version control.

Keep checks read-only by default. Passing a check does not authorize a commit,
push, PR creation, or remote-branch update. The user must explicitly request
those actions, which must also follow the repository's branch and approval
rules.

## Run the script

Run the script from this skill directory. The three checks are not repeated
full scans: commit checks inspect the index, push checks inspect changes from
the base, and CI independently verifies the final PR head.

```bash
python3 scripts/public_repo_check.py --repo /path/to/repository --staged --require-feature-branch
```

Run the staged check before committing and the change/remote check before
pushing:

```bash
python3 scripts/public_repo_check.py --repo /path/to/repository --staged --require-feature-branch
python3 scripts/public_repo_check.py --repo /path/to/repository --changed-since origin/main --check-remote
```

Use `--all` for a full baseline when introducing the gate, changing its rule
configuration, recovering from an accidental push, or preparing a Release.
Projects can add scoped exceptions and rules with
`--config path/to/public-repo-gate.json`. Keep the default rules conservative;
document each intentionally public special resource in project configuration
instead of disabling the entire check.

For a large repository, replace `origin/main` with the PR's exact base SHA. Do
not use an old local base. If the ref is missing, fail the check and synchronize
the base first rather than assuming that there are no changes.

## Layered check strategy

| Stage | Scope | Checks | Target duration |
| --- | --- | --- | --- |
| commit | staged files | Paths, secrets, diff format, feature branch | Seconds, offline |
| push | `base...HEAD` changes | Incremental public-content scan and remote/branch/upstream checks | Seconds; no full test suite |
| PR | final head | Full CI security scan, lint, test, build, and PR diff review | CI-owned |
| Release | final artifacts and live state | Archives, licenses, tag, deployment, and attachments | Separate gate |

A passing commit check cannot replace remote push/PR confirmation, and an
incremental push check cannot replace PR CI. Each layer should cover only its
own responsibility.

## Commit gate

1. Confirm the repository visibility first. Treat the remote repository, branch,
   PR, Preview, and history as public content by default.
2. Check `git status --short --branch`, the current branch, and the target PR
   base. Do not commit ordinary changes directly to `main` or `master`.
3. Stage only the necessary files. Inspect staged names, status, and the full
   diff, not just a summary.
4. Run the script's `--staged` check and `git diff --cached --check`. This is a
   fast gate; do not require the full test suite for every commit.
5. For higher-risk code, run targeted tests required by the project. Let PR CI
   own complete lint, test, build, security, and license checks.
6. Confirm that the commit message, version files, public documentation, tests,
   and configuration are synchronized. Keep internal plans, legal opinions,
   business strategy, customer data, and private agent configuration out of
   public commits.

## Push gate

1. Reconfirm the remote URL, repository visibility, target branch, upstream, and
   PR head before pushing. Do not infer remote state from memory.
2. Run `--changed-since origin/main --check-remote`, then inspect recent commits
   on the branch for content that should not be public. The script cannot prove
   the hosting platform's repository visibility; confirm that setting manually.
3. In the ordinary workflow, push only a feature branch, never `main` directly.
   Do not use `--force` to overwrite someone else's branch. History cleanup is
   an exception requiring a local backup and an explicit recorded reason.
4. After pushing, confirm through the remote platform that the branch exists,
   the commit SHA matches, the PR base/head is correct, and no other PR was
   accidentally created or updated.
5. If an accidental push is found, stop pushing immediately. Preserve a backup
   reference, pause or close the PR, rotate exposed secrets, rebuild from a
   clean public base, and follow the hosting platform's process for historical
   objects and caches.

## PR gate

1. Set `main` as the PR base and the feature branch as the head. Describe the
   scope, risks, verification results, and unfinished work in the title and
   body.
2. Recheck the PR file list and full diff, especially new files, generated
   artifacts, hidden directories, configuration, licenses, and documentation.
3. Require CI to pass with a full public-content scan of the final head and the
   project's lint, test, build, security, and license checks. Add real
   environment evidence for database, deployment, third-party-resource, or
   release changes. Passing CI does not prove that a production migration ran.
4. List incremental local checks, full CI checks, project tests/build, security
   checks, and license checks in the PR body. Explain every failed or skipped
   check.
5. Do not treat the author's own PR as an independent review. Obtain at least
   one appropriate review and request security or legal review when needed.
6. Reconfirm before merging that no internal material, personal data, secrets,
   or unnecessary public content remains. After merging, delete the feature
   branch and independently verify the final `main` commit.

## When a check fails

Stop the current commit, push, or merge; do not commit first and explain later.
Classify the finding as a false positive, a project-specific public resource,
or content that should not be public. For a false positive, add the smallest
scoped project configuration and retain the reason. For a real issue, unstage
the content or remove it from the commit. Treat exposed secrets, personal data,
or internal material as a security incident; rewriting branch history alone is
not sufficient.

## Boundary with the Release gate

This skill covers commits, pushes, and PRs. Use the sibling
`public-release-gate` skill for tags, final installers, archives, GitHub
Release attachments, and production-deployment acceptance. Only both gates
together constitute a complete release review. Do not repeat the Release
artifact scan at every commit, push, and PR layer.

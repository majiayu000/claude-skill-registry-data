---
name: repo-scrub
description: Scan a GitHub repo's full history for secrets and large files, scrub what the user picks, rewrite history safely, then flip it private → public.
argument-hint: "[owner/repo] (default: current repo)"
disable-model-invocation: true
---

Going public is one-way: forks, caches and scrapers copy history within minutes, and GitHub offers no hook on its visibility toggle. So all cleanup happens *before* the flip, and you flip it yourself with `gh`.

Two rules hold throughout:
- **Gate**: each numbered gate below needs the user's explicit go-ahead.
- **Complete report**: every secret and large blob found is shown, including ones the user keeps.

`<tmp>` = `$(mktemp -d)`, created once and echoed to the user; reuse that same path in every step (Git Bash's `/tmp` and Windows `%TEMP%` differ for Python). `<tmp>/scrub-work` holds secret-bearing files. Delete it (step 12) on every exit, early ones included.

## 1. Prereqs and target

- `gh auth status`; else user runs `gh auth login`.
- `gitleaks version`; missing → Windows `winget install --id Gitleaks.Gitleaks -e`, mac/linux `brew install gitleaks`. v8.19+ uses `gitleaks git`; older uses `gitleaks detect --source . --log-opts="--all -m"`.
- `git filter-repo --version`; missing → `pip install git-filter-repo` (mac: or brew). Trust the version command, not pip's exit code: a `--user` install can land off PATH.

Missing tool → give the install command and stop.

`<repo>` = the argument, else `origin`'s repo per the `next` skill's `BOARD.md`, Target repo section (never a bare `gh` call: on a fork it hits the parent). `gh repo view <repo> --json name,owner,isPrivate,defaultBranchRef` → confirm the repo, and that a rewrite + force-push is OK if anything gets scrubbed.

In the user's clone:
- **Other remotes**: `git remote -v`; per remote other than `origin`, `git ls-remote --heads --tags <remote>`. Each is its own copy of the history: its branches are scanned (step 3) and rewritten (step 7), and it gets the rewritten history (step 9, each push on a yes). A branch only there is not local-only. List each remote with its branches.
- **Submodules**: `git log --all -m -p -- .gitmodules | grep -E '^\+\s*url'`. Each is a separate repo whose history this scan never enters: tell the user to `/repo-scrub` each one before this repo goes public (a private one breaks `--recurse-submodules` clones). Flag a relative URL (`./`, `../`): it resolves against wherever the superproject was cloned from, so public clones need that sibling repo public at the same path; else use an absolute URL.

## 2. LFS bail-out

`gh api repos/<o>/<r>/contents/.gitattributes --jq .content | base64 -d | grep -i lfs` (404 = no LFS). LFS-tracked paths → stop: `filter-repo` has no LFS awareness; this needs manual handling. This only sees the root file on the default branch, so repeat the check on clone #1 (step 3): `git log --all -m -p -- '*.gitattributes' | grep -i filter=lfs` catches nested files and other branches. A hit there → stop too.

## 3. Scan (clone #1)

```
mkdir -p <tmp>/scrub-work
git clone <url> <tmp>/scan-clone && cd <tmp>/scan-clone
git fetch <remote-url> '+refs/heads/*:refs/remotes/<remote>/*'   # per other remote (step 1)
git count-objects -vH > <tmp>/scrub-work/before-size.txt
gitleaks git . --log-opts="--all -m" --report-format json --report-path <tmp>/scrub-work/gitleaks-report.json --no-banner
git filter-repo --analyze
python <skill-dir>/scripts/summarize_findings.py --gitleaks <tmp>/scrub-work/gitleaks-report.json \
  --analysis-dir .git/filter-repo/analysis --out <tmp>/scrub-work/findings.json
```

- Run the LFS history check from step 2 here, in `scan-clone`, before trusting the scan.
- gitleaks exit 1 = findings, not failure.
- `-m` on `--log-opts` and on every `git log -S`/`--grep` here and in step 8: without it a change made only in a merge commit (a conflict resolution) is never diffed, so a secret added there scans clean.
- `summarize_findings.py` merges gitleaks + `.git/filter-repo/analysis/` into `findings.json`: secrets `S1…` (deduped by rule + value, or by location when the value is empty; fingerprint `secret_sha256` only), large blobs `L1…` (bytes accumulated across every version). Use it; the analysis tables are easy to misread.
- **Personal strings** (names, emails) from `/repo-showcase` or the user: gitleaks has no rule for them. Per string, `git log --all -m -S'<string>' --oneline` (blob hits) and `git log --all -m -F -i --grep='<string>' --oneline` (commit-message hits). Each hit is a finding `P1…` (Detail: `personal string`, plus the commit count); refer to it by ID from here on.
- **Identities and messages**: `git log --all --format='%an %ae %cn %ce%n%B' | grep -Eo '[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:]]+' | sort -u` and `git log --all --format='%an <%ae>%n%cn <%ce>' | sort -u`. Drop the owner's own (ask). Each other email is checked as a personal string; each other author/committer identity is a `P` finding (Detail: `author identity`), unless `/repo-showcase` handed over "author identities stay".
- **Signatures**: `git log --all --format='%h %G?' | grep -v ' N$'` (signed commits) and `git for-each-ref refs/tags --format='%(if)%(contents:signature)%(then)%(refname:short)%(end)'` (signed tags). filter-repo drops every signature it rewrites.
- `--analyze` spends this clone (filter-repo refuses a second run). Delete `scan-clone` once `findings.json` exists; keep `gitleaks-report.json` until step 12 (step 7 recovers values from it).

## 4. Report

```
3 secrets across 2 files, 2 large blobs totaling 410 MB (accumulated across history)

ID | Type   | Path(s)                  | Detail                 | Commits
S1 | secret | config/dev.env (+1 more) | AWS Access Key         | 3
L1 | large  | assets/demo.mov          | 340 MB (all versions)  | -
P1 | personal | src/cli.js             | personal string        | 2
P2 | personal | (commit identity)        | author identity        | 4

Remotes: origin, mirror (branch only there: release/x). Submodules: vendor/lib (../lib.git, relative).
Signed: 2 commits, 1 tag (v1.0.0). A rewrite drops them: tags can be re-signed (step 8), commits stay unsigned.
```

Raw secret values stay out of the table. Reveal one only on request, looked up by fingerprint in `gitleaks-report.json`.

## 5. Select

Per ID or bulk ("all secrets", "over 50MB", a path glob). Echo back the final **scrub** and **keep** lists. Silence is not "scrub everything".

## 6. Gates before any rewrite

- **Rotation** (any secret selected): walk the user through [ROTATE.md](ROTATE.md). **Gate**: rotation confirmed done.
- **Collaborators**:
  ```
  gh api repos/<o>/<r>/collaborators --jq '.[].login'
  gh api repos/<o>/<r>/invitations
  gh pr list -R <o>/<r> --state open --json number,title,headRefName,author
  gh api repos/<o>/<r>/forks --jq length
  ```
  Anyone affected → draft a notice (what, why, re-clone from scratch, which PRs need recreating); user posts it or skips. Forks can't be messaged; report the count. **Gate**: go-ahead to rewrite.

## 7. Rewrite (clone #2)

```
git clone <url> <tmp>/rewrite-clone && cd <tmp>/rewrite-clone
git fetch <remote-url> '+refs/heads/<b>:refs/remotes/origin/<b>'   # per branch only on another remote
git repack -ad                                                    # after any such fetch: filter-repo wants one fresh pack
python <skill-dir>/scripts/build_replace_text.py --gitleaks <tmp>/scrub-work/gitleaks-report.json \
  --findings <tmp>/scrub-work/findings.json --ids S1 S3 --out <tmp>/scrub-work/expressions.txt
```

Fetching into `origin/<b>` lets filter-repo turn it into a local branch like the rest; a name on two remotes with different tips → ask which one. The script writes `--replace-text` expressions without printing a value; no `S` selected → drop `--ids` and it writes an empty file for the `P` lines. Each selected `P` finding adds one line, `literal:<string>==>REDACTED`, appended to `expressions.txt` by a file edit (no `echo` of the string); a commit-message hit also needs `--replace-message <tmp>/scrub-work/expressions.txt` in the call below. `literal:` never touches author/committer fields: each selected `author identity` gets a line `New Name <new@email> Old Name <old@email>` (names bare, emails in `<>`; the user picks the replacement) in `<tmp>/scrub-work/mailmap`, and the call adds `--mailmap <tmp>/scrub-work/mailmap`. An identity the user keeps → record `author identities stay: <identity>` in the step-8 summary. Location-only findings (`secret_sha256: null`) have no value to replace; it skips them, so scrub those by `--path` or by hand. Large blobs, per finding: strip entirely, or strip history but keep the current file (re-add it in a commit after the rewrite: path/size stripping removes HEAD's copy too).

One combined call, only the flags for what was selected:

```
git filter-repo --replace-text <tmp>/scrub-work/expressions.txt --path <paths> --invert-paths
```

(`--strip-blobs-bigger-than <size>` when a threshold describes the selection better.)

## 8. Verify (still reversible)

`git log --oneline -10`, `gitleaks git . --log-opts="--all -m" --no-banner`, `git count-objects -vH`. Spot-check stripped paths are gone. Per scrubbed `P` finding, `git log --all -m -S'<string>' --oneline` (and the `--grep` form for message hits) prints nothing, and so does `git log --all --format='%an %ae %cn %ce %B' | grep -F -i '<string>'` per scrubbed string or identity email (`-S` never sees identities). Show before/after commit count and size. **Gate**.

Per tag signed before (step 3), ask to re-sign it with the user's own key (`user.signingkey`): `git tag -l --format='%(contents:subject)%0a%0a%(contents:body)' <tag> > <tmp>/scrub-work/tag.msg && git tag -f -s <tag> '<tag>^{commit}' -F <tmp>/scrub-work/tag.msg`, then `git tag -v <tag>`. No → it ships unsigned; say so.

## 9. Force-push

Only after the step-6 notice went out (or was confirmed unnecessary). filter-repo removed `origin`:

```
git remote add origin <url>
git push origin --force --all && git push origin --force --tags
```

Per other remote from step 1, each on its own yes: `git remote add <remote> <url> && git push <remote> --force <each branch it holds>` (plus `--tags` if it held tags). One the user declines keeps the old history and the secret: say so.

A hook or permission rule that blocks the push → show the user these exact commands to run themselves (in Claude Code, prefixed with `!`), then continue at step 10 once they confirm.

`--all` covers non-default branches only because `filter-repo` turned the fresh clone's `origin/*` into local branches. Run `git branch` before pushing and confirm every branch you mean to keep is listed; a missing one is not pushed, and keeps its old history on the remote. Branches fetched from another remote at step 7 are local too: then push `origin` its own branches by name instead of `--all`.

## 10. Post-push

**Every local copy of this repo, the user's own included**, still holds the old commits (and the secret). A plain `git pull` would merge the old history back in and the next push would re-leak it. Per copy, either:

- **Re-clone** (simplest): copy uncommitted work, stashes (`git stash show -p --include-untracked stash@{n}`) and unpushed branches and tags (`git bundle create`) out of the old clone first, and keep it until they are carried over.
- **Reset in place**: follow [POST-PUSH.md](POST-PUSH.md). It parks the WIP first, saves every stash entry (untracked parts included) and every local-only branch and tag outside the repo, resets the pushed branches, re-creates the stashes on the new history and checks them against the saved copies, re-points a tag whose commit was rebased, and deletes a branch or tag only on a yes. Its `reflog expire` and `gc` run before its final steps: a warning per branch or tag kept as is (old history, secret included, never push it) and a gated offer to delete the save folder. Never a bare `git reflog expire --all`: it wipes the stash list.

Tell collaborators the same (the step-6 notice).

`gh pr list -R <o>/<r> --state open` → name PRs that must be closed and recreated. Tell the user: old commits stay reachable on GitHub (via `refs/pull/*`, direct SHA, cached views) until GitHub Support garbage-collects them. Rotation protects the secret; the push is hygiene.

## 11. Flip visibility

State `gh`'s consequences first: stars/watchers lost, forks detached, push rulesets disabled, Actions history becomes public. **Gate**, separate from the push.

```
gh repo edit <o>/<r> --visibility public --accept-visibility-change-consequences
gh repo view <o>/<r> --json isPrivate
```

## 12. Cleanup

```
rm -rf <tmp>/scrub-work <tmp>/scan-clone <tmp>/rewrite-clone
```

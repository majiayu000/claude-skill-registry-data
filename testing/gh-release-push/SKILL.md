---
name: "gh-release-push"
description: "Tag and push a release from green `main`."
---

# gh-release-push command

Apply this command workflow. Treat any text after its invocation as the command input.

Tag and push a release from green `main`.

## Precondition — main branch, no worktree

A release tags a green `main`. It produces no code change and never runs on a
worktree branch. Stop immediately if the current branch is not `main`:

```bash
branch=$(git branch --show-current)
[ "$branch" = "main" ] || { echo "Release must run on main (currently on '$branch'). Abort."; exit 1; }
```

## Steps

1. Run the repo's full release gate set. Where `mage -l` lists targets, `mage
   tag` is the entry point — it re-runs every declared gate (audit, test,
   integration, conformance, and anything else the repo registers) and creates
   the tag on success. Where no mage target exists, run the repo's own check
   and test commands.

   If any gate fails, **stop the release**. Do not fix, retry, or waive the
   failure inline. File an SRD-backed bug via `/gh-issue-push`, implement and
   merge the fix through the normal issue/PR flow, then re-run the release
   against the now-green `main`.

2. Record the previous release tag: `git describe --tags --abbrev=0` (or empty
   if no tags exist yet).

3. If `mage tag` already created the tag, capture its name from the output or
   via `git describe --tags --abbrev=0`. Otherwise create a `v0.YYYYMMDD.N`
   tag manually.

4. Generate a changelog: `git log --oneline <previous-tag>..<new-tag>` (or all
   commits if no previous tag). Summarize changes grouped by category
   (features, fixes, docs, etc.).

5. Replace the lightweight tag with an annotated tag carrying the summary:
   `git tag -d <new-tag> && git tag -a <new-tag> -m "<summary>"`. Print the
   summary.

6. Push the branch and tags to `origin`. If `git remote | grep -q release`
   succeeds, also push to `release`.

   ```bash
   git push origin main
   git push origin --tags
   # if release remote exists:
   git push release main
   git push release --tags
   ```

7. If the repo is a Go module, resolve the module path with `go list -m` and
   run `go get <module>@<new-tag>` to warm the Go module proxy. Report errors
   but do not fail the release.

8. Report the tag name, branch, which remotes received the push, and the
   change summary.

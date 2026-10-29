---
name: github-pr-review-setup
description: Prepare a clean local checkout for a GitHub PR (worktree-first via `ohc`/Orca), fetch the PR base ref, and emit PR context (CI checks + PR comments/reviews) as JSON for downstream review.
---

# Set up a GitHub PR review

Run this skill when a review needs a clean local checkout and a JSON bundle of
the PR's metadata, CI checks, and discussion. The script prints that bundle to
stdout and can also save it to a file.

## Prepare the checkout

1. Run the script with a PR number or GitHub PR URL:

   ```sh
   python "<path-to-skill>/scripts/prepare_github_pr_review.py" --pr "<number-or-url>"
   ```

2. Supply `--repo OWNER/REPO` when `--pr` is a number and the repository cannot
   be inferred from the current checkout. Supply `--repo-dir <path-to-clone>`
   when you are not running inside the target repository.

3. Use the default `--checkout-mode worktree` for an isolated Orca worktree.
   The script resolves `ohc`, requires `zsh`, `orca`, and `gh`, then asks `ohc`
   to create a worktree named `pr-review-<number>`. Set `--worktree-name` to
   choose another name. `ohc` clones through `ghc`, registers the repository in
   Orca, and creates the worktree; the script then runs `gh pr checkout` in it
   with `--branch <worktree-name> --force`. This handles same-repository and
   fork PRs through the same checkout path.

4. Use `--checkout-mode inplace` only when you want the PR branch in the
   existing clone. The script requires a clean clone and, when it can detect
   the local `origin`, checks that it matches the requested repository. It
   checks out the PR with `gh pr checkout`; Orca is not required.

   ```sh
   python "<path-to-skill>/scripts/prepare_github_pr_review.py" \
     --pr "<number-or-url>" \
     --checkout-mode inplace
   ```

5. The script fetches the PR base branch so the returned `compare_to` ref is
   available locally. It uses `upstream` when present, otherwise `origin`,
   otherwise the first configured remote. If there are no remotes, the base
   ref must already exist locally.

## Read the review context

Use the JSON payload as the input to the review. It includes:

- `worktree_dir`: checkout path, whether created as a worktree or used in place
- `repo_dir`: underlying clone path when known
- `compare_to`: fetched base ref suitable for review tools, such as
  `upstream/main`
- `pr`: metadata returned by `gh pr view`
- `checks` and `checks_summary`: CI checks and counts grouped by result bucket
- `issue_comments`, `reviews`, and `review_comments`: paginated PR discussion
- `git`: resolved base and checked-out head commit IDs

CI checks come from `gh pr checks`; PR metadata comes from `gh pr view`; the
three discussion fields come from paginated `gh api` requests. A pending-checks
exit from `gh pr checks` is accepted and represented in the returned payload.

Pass these values to the review tool:

```text
path = worktree_dir
compare_to = compare_to
```

## Save the payload

Use `--out <path>` to write the same JSON payload to a file as well as stdout.
The script creates parent directories for that path.

```sh
python "<path-to-skill>/scripts/prepare_github_pr_review.py" \
  --pr "<number-or-url>" \
  --out "/path/to/pr-context.json"
```

The script requires `git` and `gh` in either checkout mode. A PR number can be
paired with `--repo` or inferred from the local `origin`; a GitHub PR URL
provides its repository directly.

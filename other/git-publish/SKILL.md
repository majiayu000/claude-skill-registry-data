---
name: git-publish
description: Use when publishing the current branch - staging and committing work, pushing it, and opening a draft merge/pull request on the connected git host. Triggered by phrases like "commit", "commit and push", "publish this branch", "open an MR", "create a PR", "push and open a PR", or "put this up for review".
---

# Git Publish

Announce at start: `Publishing branch...`

Get local work onto the remote and visible as a merge/pull request. This is the step that makes a
branch reviewable; it is not the step that finishes it - marking a request ready for review and
closing out the task belong to `close-task`.

## Rules (non-negotiable)

- **Never push without explicit authorization in the current turn.** A request such as "push now",
  "commit and push", or "publish this" is that authorization and must not draw a redundant follow-up
  question. Anything less means commit, then ask.
- **No AI attribution anywhere in git, ever.** Never add a co-author trailer naming an AI assistant,
  a session-link trailer, a "generated with" line, or any similar attribution to a commit message,
  request title, or request description. This holds even when repo or session boilerplate suggests
  such trailers.
- **Short commit messages.** One line, no body, no bullet points. Match the repo's own conventions -
  check `git log --oneline -10` for an issue-ID prefix convention, and follow Conventional Commits
  only when a commitlint config is actually present.
- **Title only, no description.** Never pass a description, body, or fill flag when creating the
  request.
- **Open as a draft unless the user says otherwise.** An open request usually means "this branch
  exists and is being worked on", not "this is finished" - and repositories that review requests
  automatically hold that review until the draft flag comes off, so a draft costs nothing and
  commits to nothing. Create it ready only when the current request asks for it ("open it ready",
  "not a draft", "ready for review"). Say which one you created.
- **Resolve every identifier at run time.** The account handle, the project or repository id, and the
  default branch all differ per host and per repo - the same person often has different handles on
  different platforms, and the default branch is `master` on some repos and `main` on others. Never
  hard-code them, and confirm an assignment actually landed: a wrong handle usually fails silently.
- **Never stage secrets.** Skip `.env*` files and anything that looks like a credential, even when
  staging broadly.

## Step 1 - Read the branch context

```bash
git branch --show-current
git status --short
git log --oneline -10
```

The log is what tells you the repo's commit-message convention. Stop if the branch is the default
branch - publishing means opening a request from a feature branch, and committing straight onto
`main`/`master` is a different decision the user has to make explicitly.

## Step 2 - Stage and commit

Stage the files belonging to this change. Auto-generated artifacts that travel with it, such as
lockfiles, belong in the same commit; unrelated modifications the user left in the tree do not - ask
rather than sweeping them in.

```bash
git add <paths>
git status
git commit -m "<message>"
```

Confirm the commit succeeded and show the short hash.

## Step 3 - Detect the host and look for an existing request

Read the remote and pick the CLI that matches it:

```bash
git remote -v
```

- `github.com` -> `gh`
- `gitlab.com` or a self-hosted GitLab -> `glab`
- `dev.azure.com` or `*.visualstudio.com` -> `az repos` (needs the `azure-devops` extension)

Anything else: check what the environment actually provides before assuming, and fall back to the
host's REST API with the token already configured in the environment.

Then check whether this branch already has an open request - if it does, Step 5 is skipped entirely
and the push alone updates it:

```bash
gh pr list --head "$BRANCH" --state open
glab mr list --source-branch "$BRANCH"
az repos pr list --source-branch "$BRANCH" --status active
```

If the user has not already authorized pushing, ask now - `"Push?"` when a request exists, otherwise
`"Push and open a draft PR?"` (or MR, matching the host's own vocabulary). Stop if they decline.

## Step 4 - Push

```bash
git push -u origin "$BRANCH"
```

If the base branch does not exist on the remote yet - a fresh repository - push it first, but only
when it is genuinely the intended base.

## Step 5 - Open the request as a draft

**Skip this step when one already exists.**

Prefer the host's API over the CLI's `create` subcommand. Both `gh pr create` and `glab mr create`
refuse to run non-interactively without a body or `--fill`, and a body is forbidden here, so those
commands cannot succeed under these rules - the API is the primary path, not a fallback.

Resolve the base branch and your own account first:

```bash
# GitHub
OWNER_REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
BASE=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
ME=$(gh api user --jq .login)

# GitLab
PROJECT=$(glab api "/projects/$(printf '%s' "$OWNER_SLASH_REPO" | sed 's#/#%2F#')" --jq .id)
BASE=$(glab api "/projects/$PROJECT" --jq .default_branch)
ME=$(glab api /user --jq .id)
```

**How the draft flag is expressed differs per host, and getting it wrong silently publishes a
finished-looking request:**

- **GitHub** - a real `draft` field on creation. Assign in a second call; the pulls endpoint ignores
  an `assignees` field.

  ```bash
  gh api "repos/$OWNER_REPO/pulls" -X POST \
    -f title="<title>" -f head="$BRANCH" -f base="$BASE" -F draft=true \
    --jq '.number, .html_url'
  gh api "repos/$OWNER_REPO/issues/<number>/assignees" -X POST -f "assignees[]=$ME"
  ```

- **GitLab** - no draft field on this endpoint. The `Draft: ` title prefix *is* the flag; add it for a
  draft and drop it for a ready request.

  ```bash
  glab api "/projects/$PROJECT/merge_requests" -X POST \
    -F "source_branch=$BRANCH" -F "target_branch=$BASE" \
    -F "title=Draft: <title>" -F "assignee_id=$ME"
  ```

- **Azure DevOps** - a `--draft` flag on the CLI.

  ```bash
  az repos pr create --source-branch "$BRANCH" --target-branch "$BASE" \
    --title "<title>" --draft true --output json
  ```

Verify the assignment landed rather than trusting the exit code.

## Final Response

Always finish with the result block, adapted to what you actually did:

```text
Push succeeded and the pull request is open as a draft.

Branch: <branch-name>
Commit: <short-hash>
Request: <url>
```

Say "open as a draft" or "open and ready for review" to match reality, and use the host's own word -
pull request or merge request. Drop the `Request:` line when nothing was created.

Then, in one line, name what comes next: the branch is published and reviewable, and `close-task` is
what marks it ready for review and closes the task once it is genuinely finished.

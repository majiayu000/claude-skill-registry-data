---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: raycast-publish-extension
description: >
  Publish a Raycast extension update: build to validate, add a CHANGELOG entry
  with {PR_MERGE_DATE}, run `npm run publish` (opens or updates a PR in
  raycast/extensions), pull contributions, then edit the PR title/body and
  watch checks with gh. Load when asked to publish or update a Raycast extension.
---

# publishing an extension update

## Validate Before Publishing

```bash
npm run build
```

## changelog

update CHANGELOG.md with a new headings, using as date ``

```md
## [Improvement] - {PR_MERGE_DATE}

- did something
- and something else
```

This validates your extension for distribution without publishing.

## Publish Extension (Creates PR under the hood)

```bash
npm run publish
```

Or directly:

```bash
npx ray publish
```

This command:
- Authenticates with GitHub
- Squashes commits
- Opens a PR in `raycast/extensions` repository

run it with a timeout of at least 60 seconds

If someone contributed to your extension or you made edits on GitHub, first run:

```bash
npx @raycast/api@latest pull-contributions
```

## Update PR Title and Body with gh CLI

After `npm run publish` creates the PR, you can update it:

```bash
# List your open PRs to find the PR number
gh pr list --author @me --repo raycast/extensions

# Update PR title
gh pr edit <PR_NUMBER> --repo raycast/extensions --title "Add feature X to my-extension"

# Update PR body (never use headings!)
gh pr edit <PR_NUMBER> --repo raycast/extensions --body "$(cat <<'EOF'
Brief description of the changes.

- Added feature X
- Fixed bug Y
- Updated dependencies
EOF
)"

## Push Additional Changes

To push more commits to an existing PR:

```bash
npm run publish
```

Running publish again will push to the same PR.

## Watch PR Status

```bash
gh pr checks <PR_NUMBER> --repo raycast/extensions --watch --fail-fast
```

## View PR Review Comments

```bash
gh pr view <PR_NUMBER> --repo raycast/extensions --comments
```

---
name: pr-create
description: Open a GitHub PR with a tight body — why this change, what'll surprise the reviewer, how we know it's correct — or add a pull_request_template to a repo. Use when asked to open, create, or draft a pull request, compose or regenerate a PR description, or scaffold a repo's PR template. Composes the Summary/Gotchas/Verification structure and detects an existing template first.
---

# PR create

Compose before opening. The body is the squash-merge commit
context — write it for the reviewer first, the future reader of
`git log` second.

## Pre-flight

```bash
# REST reads — see ~/.claude/CLAUDE.md "GitHub API budget".
branch=$(git branch --show-current)
gh api repos/:owner/:repo/pulls \
  --jq ".[] | select(.head.ref==\"$branch\") | {number, state, url}"  # existing PR for this branch?
git log --oneline main..HEAD          # what this PR actually contains
gh api repos/:owner/:repo/pulls/<N> --jq '.body'   # iterating? read the current body
```

- Existing PR for the branch → iterate on it, don't open a second.
- Find the issue this resolves (branch name, commit trailers, the
  task). A PR that closes one carries `Closes #<N>` in the body.

## Detect repo template

```bash
ls .github/pull_request_template.md \
   .github/PULL_REQUEST_TEMPLATE.md \
   .github/PULL_REQUEST_TEMPLATE/ \
   docs/pull_request_template.md 2>/dev/null
```

Template present → fill its sections; don't swap its structure for
ours. Absent → use the structure below.

## Body structure (no template)

Three short blocks. A reviewer should grasp all three in one read; a
block that runs past a few lines is carrying detail the diff already
shows.

- **Summary** — *why this change.* Prose, 1-2 sentences leading with
  the user-visible outcome ("X now works"), not the diff ("set Y to
  Z"). Surface mechanism only when the choice isn't obvious. Link the
  issue; don't re-explain it.
  Bad: "Set `format_space \"#[bg=16]\"` in pair.kdl."
  Good: "Bar paints uniformly black across the format gap, closing the
  lighter strip from #68."
- **Gotchas** — *what'll surprise the reviewer.* A bullet per pointer:
  where to spend attention and why, not an exhaustive risk dump.
  Typical: off-diff state (a label/secret/setting changed remotely), a
  silent-failure mode, a non-obvious constraint, something that reads
  like a typo. Litmus: a gotcha completes "watch out — `___`", not "I
  chose `___` because `___`"; rationale goes to Summary or gets cut.
  Omit when nothing surprises.
  Bad: "Split into two workflows so each trigger is self-documenting."
  Good: "Labeling pins `.../autolabeler@<sha>`, a subpath of the same
  action — not a typo."
- **Verification** — *how we know it's correct.* A bullet per material
  check beyond CI, past tense ("ran X, confirmed Y"). Skip trivial
  steps. Omit the section when CI covers everything; unverified items
  go in Gotchas, not here.

## House rules

- **Draft only.** `draft: true`; the user promotes to ready.
- **Regenerate, don't append.** Adding commits to an open PR → rewrite
  the body from scratch for the new merge state, via
  `mcp__github__update_pull_request`. Appending each round drifts
  toward changelog narration.
- **Description, not comments.** Carry updates in the body — the single
  source of truth. The only allowed PR comment is a direct reply to an
  existing comment on that PR.
- **External repos use a different voice.** On a repo the user doesn't
  own, the description follows `~/.claude/voice.md` (conversational,
  hedged, first-person) — not the structured blocks above, which are
  for our own repos.

## Open the PR

Propose the body before submitting — a PR is shared state.

Push the branch, then open with `mcp__github__create_pull_request`:

- `title` — imperative subject.
- `body` — the blocks above, ending with `Closes #<N>`.
- `head`, `base` — this branch and the repo's default branch; neither
  is inferred.
- `draft: true` — `pr-draft-guard.sh` blocks the call without it.

## Scaffold a repo template

When asked to add a PR template to a repo, write
`.github/pull_request_template.md` — the same three blocks as
HTML-comment prompts the author fills in and deletes:

```markdown
## Summary

<!-- Why this change. Lead with the user-visible outcome, not the diff.
     Link the issue. -->

## Gotchas

<!-- One bullet per surprise: where to spend attention and why.
     Completes "watch out — ___", not "I chose ___ because ___".
     Delete this section if nothing surprises. -->

-

## Verification

<!-- One bullet per material check beyond CI, past tense.
     Delete this section if CI covers everything. -->

-
```

Commit and PR it like any change. Match the repo's existing casing if
it already uses `PULL_REQUEST_TEMPLATE.md` for other GitHub files.

## Procedure

1. Pre-flight: existing PR? what's in `main..HEAD`? which issue closes?
2. Detect a repo template; fill it, else use the standard structure.
3. Compose the three blocks; surface non-obvious choices.
4. Open as a draft with `Closes #<N>`; capture the URL.
5. Iterating later → regenerate the whole body, never append.

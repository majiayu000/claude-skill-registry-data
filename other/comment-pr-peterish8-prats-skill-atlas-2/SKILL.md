---
name: comment-pr
description: Draft and post a simple, human GitHub pull request comment after reviewing the PR context. Use when the user asks to comment on a PR, reply to a maintainer, follow up on review feedback, or post a short status/update message to a pull request. Always preview the exact comment and wait for explicit user approval before posting.
disable-model-invocation: true
argument-hint: <pr url/number and optional message intent>
allowed-tools: Bash(gh *) Bash(git *) Bash(rg *)
---

# comment-pr

Post a thoughtful GitHub pull request comment that sounds like the user wrote it.

The user may provide a PR URL, PR number, branch name, or a rough intent such as
"reply to the maintainer", "say I fixed it", or "ask if this approach is okay".

## Hard rule

Never post a comment before showing the exact final comment to the user and getting
explicit approval.

Approval must be clear, such as:

```text
yes post it
looks good, comment
go ahead
```

If approval is unclear, ask again. Do not infer approval from silence.

## Workflow

### 1. Identify the PR

If the user supplied a PR URL or number, use it directly.

If the user did not specify a PR, find the current branch and associated PR:

```bash
git branch --show-current
gh pr view --json number,url,title,author,headRefName,baseRefName,state
```

If no PR can be identified, stop and ask the user for the PR URL or number.

### 2. Read the PR context

Read enough context to understand what the comment is replying to:

```bash
gh pr view <pr> --json number,url,title,body,author,state,headRefName,baseRefName,comments,reviews,latestReviews,files
```

Also inspect recent local work when it helps explain status:

```bash
git status --short
git log --oneline --decorate -n 8
git diff --stat
```

Use the PR's actual discussion. Do not invent maintainer feedback, test results, or
project details.

### 3. Decide the comment intent

Classify the message before drafting:

- reply to review feedback
- say requested changes are done
- explain an implementation choice
- ask for confirmation on an approach
- share a blocker or request guidance
- give a short status update

If the intent is still ambiguous after reading the PR, ask the user one concise
question before drafting.

### 4. Draft the comment

Write like a real open source contributor, not a bot.

Style rules:

- simple, direct, and human
- short, usually 1 to 4 sentences
- lowercase is okay where natural
- mild capitalization only: first word of a sentence and proper nouns
- no em dashes
- no corporate wording
- no AI/tool mentions
- no "implemented", "leveraged", "utilized", "streamlined", or similar inflated words
- no fake certainty
- no over-apology
- no signoff
- no bullet list unless the comment genuinely needs multiple concrete items

Prefer comments like:

```text
thanks for the review. i pushed the change to keep this path behind the existing
validation, and added a test for the empty value case.
```

```text
i updated this based on your suggestion. the helper now returns early when there
is no configured backend, which keeps the current behavior for the default path.
```

```text
i'm not fully sure whether you want this handled here or closer to the caller. i
kept it here for now since this is where the existing validation already happens.
```

Avoid comments like:

```text
This PR has been updated to comprehensively address the feedback by leveraging
the existing validation infrastructure.
```

### 5. Preview and wait

Show the user:

- the PR URL
- the exact comment body
- the command that will be used to post it

Then ask:

```text
should i post this?
```

Do not run the posting command until the user approves.

### 6. Post after approval

After approval, write the approved body to a temporary file and post it:

```bash
gh pr comment <pr> --body-file /tmp/comment-pr-body.md
```

If `gh pr comment` is unavailable, use the GitHub API issue comment endpoint:

```bash
gh api repos/<owner>/<repo>/issues/<pr-number>/comments --method POST --field body="$(cat /tmp/comment-pr-body.md)"
```

After posting, print the PR URL and confirm that the comment was posted.

## Safety checks

- If the PR is closed or merged, mention that in the preview and ask whether to
  still comment.
- If the comment contains claims about tests, verify those test commands actually
  ran or say only that the change was pushed.
- If a maintainer asked for something and the local diff does not show it was done,
  do not claim it is done.
- If there are multiple maintainers or multiple review threads, be clear which
  feedback the comment is addressing.

---
name: pair-review
description: "Interactive pair review of a PR. Fetches the diff, scouts for context, then walks through each changed file one at a time. Collects review comments in a bag with conventional comment prefixes, previews them, and posts only after explicit approval. Trigger on: pair review, let's review together, walk me through the PR, review with me."
---

# Pair Review

Interactive file-by-file PR review with a comment bag and preview-before-post.

## Parsing arguments

The user provides a PR reference. Parse it:

- PR number: `123` -> `gh pr diff 123`, `gh pr view 123`
- PR URL: `https://github.com/org/repo/pull/123` -> extract number
- No argument: ask the user for the PR number or URL

## Phase 1: Gather context

1. **Fetch PR metadata**: `gh pr view <number> --json title,body,headRefName,baseRefName,files`
2. **Fetch PR diff**: `gh pr diff <number>`
3. **Scout the codebase**: read the changed files in full. Focus on:
   - What the changed code does and why
   - Related modules, GenServers, Store operations that the changes touch
   - Overmind patterns the PR should follow (multi-clause, maybe_x, Store isolation)
   - Shell conventions (POSIX, quoting, sourced helpers)
   - Potential concerns (OTP safety, error handling, naming, tests)
4. **Present overview**: show PR title, description, file list (numbered), and a brief summary. Then say: "Ready for file-by-file walkthrough. Say 'next' or pick a file number."

## Phase 2: File-by-file walkthrough

For each file, present:

- **File path** and whether it's new, modified, or deleted
- **The changes** (summarize the diff, show key code snippets)
- **Insights**: what the change does, why it makes sense (or doesn't)
- **Motivations**: how it fits the broader PR goal
- **Concerns**: anything worth flagging

Then **wait for the user's command**. The user may:
- Say "next" to move to the next file
- Ask questions about the current file
- Ask to add a comment to the bag
- Skip files or jump to a specific file number

## Phase 3: Comment bag

Maintain a running table of comments. Comments target specific lines:

```
| # | File:Line | Comment |
|---|-----------|---------|
| 1 | lib/overmind/mission.ex:14 | **question:** Is this needed? |
| 2 | bin/cli/commands.sh:97 | **suggestion:** Consider using printf here |
```

The user controls what goes in the bag. Never add comments without the user saying so.

### Conventional comment prefixes

Always use one of these (the user specifies which):
- **question:** — asking for clarification
- **suggestion:** — proposing an alternative
- **issue:** — something that needs to change
- **nit:** — minor, take it or leave it
- **thought:** — sharing context, no action needed
- **praise:** — highlighting something well done

## Phase 4: Preview and post

After all files are reviewed (or the user says "done"), show the final comment bag and ask:

"Here are the comments ready to post. Want me to post them, edit any, or discard?"

**NEVER post comments without explicit approval.**

When posting, use `gh api` to create PR review comments on the correct file and line, using the head commit SHA.

## Communication style

- Direct, human. No filler, no fluff
- Collaborative tone: "wdyt about...", "consider..."
- When something is clearly wrong, say it directly: "this will break when X is nil"
- Keep insights short. The user can read the code

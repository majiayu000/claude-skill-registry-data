---
name: ln-pr-review
description: "Review someone else's PR through an architectural/strategic lens — does it shift design, raise complexity, or quietly change precedent? Drives a brief reflective discussion with the user, then posts a concise review comment via `gh`. Defers line-level and bug-hunting concerns to AI review bots and the PR author."
argument-hint: "[PR number or URL; omit to list review-requested PRs]"
---

# Ln PR Review

Apply an architect's lens to a colleague's PR. The premise: AI bots and the author already handle correctness, style, and local bugs. Your time is best spent on questions only a human reviewer with codebase context can answer well — and those questions live above the line level.

Output a short, plain-English review comment. No jargon. No methodology vocabulary. The PR author should not need to know about this skill to understand the comment.

## Input

The PR to review: $ARGUMENTS

If unspecified, list PRs where the user is a requested reviewer:

```bash
gh pr list --search "review-requested:@me"
```

If the list is empty, stop and say there are no review-requested PRs to review. Do not guess a PR number.

This skill assumes `gh` is installed and authenticated. If usage is unclear, run `gh --help` or `gh <subcommand> --help`. Do not depend on `gh-axi` or any other `gh`-related skill.

## Procedure

This is **interactive and brief**. Do not produce a finished review in one pass — present, discuss, then post.

### 1. Bind and load the PR

Resolve the selected PR to one stable command token before reading or posting:

- Keep a full PR URL as the `<pr>` token when the user supplied one.
- For a bare number from the current checkout's repository, use that number as `<pr>`.
- For a bare number that belongs to another repository, use `-R <owner/repo>` on every `gh pr ...` command.
- If the target repository is ambiguous, stop and ask for the PR URL.

Use the same `<pr>` token and `-R <owner/repo>` option, if needed, for view, diff, checks, and final review submission.

```bash
gh pr view <pr> --comments
gh pr diff <pr>
gh pr checks <pr>
```

Capture: title, author, description, files changed, additions/deletions, existing review comments, and the diff itself. If any load command fails, if the PR target is ambiguous, or if the diff is unavailable or empty, stop and report that the PR could not be reviewed from trustworthy evidence. Do not compose or post a review until the PR loads correctly.

If the diff is large, sample by directory/feature area rather than reading every line — you are looking for shape, not bugs.

If `memory/SPEC.md` or `memory/PLAN.md` exist in the local checkout and the PR touches their active areas, skim them for current precedent. **Do not require them**; most projects don't have such docs and the lens still works.

### 2. Triage the change shape

Before applying the lens, name what kind of change this is in one line. Examples:

- "Feature: adds a new X endpoint and storage path"
- "Refactor: collapses two adapters into one"
- "Cross-cutting: renames a domain term across N files"
- "Chore: bumps deps and adjusts call sites"
- "Bugfix with side change: fixes Y but also restructures Z"

The shape determines which lens questions are likely to fire. A pure dependency bump rarely warrants architectural review; a "bugfix with side change" almost always does.

### 3. Apply the lens

Walk these questions against the diff. Skip ones that obviously don't apply. The goal is **0–5 concrete concerns**, not a checklist exhausted.

1. **Strategy / design shift** — Does this introduce a new architectural pattern, abstraction, layer, or boundary the codebase didn't have before? Is that intentional and discussed, or incidental to solving the stated problem?

2. **Complexity tax** — Are new abstractions, options, configuration knobs, or indirection added before there are two real callers needing them? Could the same outcome be reached with less new surface? (Rule of three, not rule of one.)

3. **Precedent drift** — Does the change diverge from existing patterns in the codebase (naming, error handling, layering, where things live, how things are wired) without naming the divergence? Silent precedent changes are the most expensive kind because they fork the codebase's idioms.

4. **Scope tightness** — Is the diff scoped to its stated purpose, or does it include adjacent rewrites, opportunistic cleanup of unrelated code, or "while I'm here" changes? Drive-by changes are often fine in isolation but expensive to review together with the primary change.

5. **Coupling and dependencies** — Does it introduce new cross-module coupling, a new external dependency, or a new cross-boundary call? Does it create a seam that didn't exist, or erase one that did?

6. **Accumulation vs. deletion** — Does it add parallel paths, compatibility shims, or dead code rather than replacing the old thing? Does it leave the codebase smaller or larger in concept count?

7. **Reversibility** — How hard would this be to undo in three months? Are decisions getting baked into data shapes, public APIs, or persistence that will outlive the immediate use case?

For each concern, note: which files exemplify it, and what a one-line question or observation to the author would look like.

### 4. Brief reflection with the user

Present the change shape and 0–5 candidate concerns to the user, compactly:

```md
## PR #<num>: <title>
**Shape**: <one-line classification>
**Author**: <name> · **Size**: +<add>/-<del> across <n> files

### Candidate concerns
1. **[short label]** — [files] — [one-line concern]
2. ...

### Recommended verdict
<approve-with-comment | request-changes-with-comment | comment-only (rare)>
```

Ask the user: which concerns are worth raising, which should be dropped or merged, and whether the verdict feels right. Two or three concise concerns usually beats five hedged ones.

**Verdict is binary by default**: **approve** if there is no reason to object, **request-changes** if there is. The decision turns on a single test: *would I be fine with this landing as-is?* If yes — even when there are architectural reflections worth flagging — the verdict is **approve with comment**. If no — there's something the author should actually address before merge — the verdict is **request-changes with comment**. A request-changes verdict is a merge gate: the author should change something before the PR lands. The reflections still go in the comment either way; what changes is whether you're gating the merge on them.

Use **comment-only** only when the answer is genuinely ambiguous and you need the author's response before deciding — e.g., a concern that might be a blocker depending on how they justify a design choice. This should be rare. Reserve **request-changes** for things the author should fix; do not use it for soft suggestions you'd be fine seeing land without.

If none of the lens questions fired for a review-requested PR, recommend a plain approval. Silence in the public comment body is fine, but do not silently skip clearing the review request unless the user explicitly decides not to review.

### 5. Compose the comment

Write **one summary comment** by default. Multiple inline comments are heavier than the architectural lens warrants; collapse related observations into the summary.

Style rules:

- Plain English. No skill names, no methodology jargon, no rules-of-three citations.
- Frame soft reflections as questions or observations. Do not phrase them as directives unless the selected verdict is request-changes.
- Cite specific files/areas. "In `src/foo/bar.ts`" beats "in the auth layer."
- Keep it under ~200 words unless the user explicitly asks for more.
- Lead with what works or what the change accomplishes when there's a real concern to raise — the author should know you read it.
- Do not repeat what AI bots already said. If a bot caught it, skip it.

Show the draft to the user and ask for edits before posting.

### 6. Post a formal review

Use `gh pr review` for the final outcome so a requested-review assignment is cleared. Do not use `gh pr comment` as the review outcome; it creates a conversation comment, not a submitted review.

Write non-empty review bodies to a temp file first because review text often contains backticks, quotes, and code snippets. Use your file-write/editor tool, not a shell heredoc, so a line like `EOF` in the review cannot truncate the body or execute trailing text.

```bash
# Create /tmp/prNNN-review.md with your file-write/editor tool when posting a body.

# Approve with an optional comment.
gh pr review <pr> --approve --body-file /tmp/prNNN-review.md

# Plain approval when no public comment is needed.
gh pr review <pr> --approve

# Comment-only when concerns might block and you want author response first.
gh pr review <pr> --comment --body-file /tmp/prNNN-review.md

# Request changes for real blockers.
gh pr review <pr> --request-changes --body-file /tmp/prNNN-review.md
```

If the selected PR required `-R <owner/repo>` while loading, include that same option in the chosen post command.

After posting, confirm the review URL back to the user.

## What not to do

- Do not nitpick names, formatting, or local style — that's the bot's job.
- Do not hunt for bugs line-by-line — that's also the bot's job and the author's.
- Do not post anything without the user confirming the draft.
- Do not introduce skill-family vocabulary into public PR comments.
- Do not write a long review when a short one or no body text would do.
- Do not leave a requested-review PR without a `gh pr review` verdict unless the user explicitly declines to submit a review.

## Routing

After posting (or after the user explicitly declines to review), present these options to the user (use `tool-ask-question`):

| #   | Label                  | Target              | Why                                                   |
| --- | ---------------------- | ------------------- | ----------------------------------------------------- |
| 1   | Next PR                | `ln-pr-review`      | Continue the review queue                             |
| 2   | Open a follow-up issue | `gh issue create`   | A concern deserves its own tracked thread             |
| 3   | Scope a local change   | `ln-scope`          | The PR revealed work we should do in our own codebase |
| 4   | Done                   | —                   | Review session complete                               |

Recommended: **1** if there are more review-requested PRs, **4** otherwise.

---
name: review-pr
description: Use when the user asks to review, code-review, or approve someone else's pull request by number or URL, or to leave review comments on a PR. Not for the user's own PRs (that is /pr's self review).
---

# Review PR

Review a teammate's pull request the way a careful colleague would: find what matters, say it as a question or a suggestion, skip the noise, and approve when nothing blocks. The review itself runs in a background opus agent via the built-in `/code-review` skill; the main session triages, gets the user's approval per comment, and posts one GitHub review.

## Usage

`/review-pr <PR number or URL> [--effort low|medium|high|xhigh|max] [--repo owner/name]`

Default effort `medium`. The repo comes from the URL, from `--repo`, or from the current directory's `origin`.

## Config

- Rules: the `reviewing-prs` skill holds every rule for what gets said: triage, verdict, comment writing, the review body and posting approval. Read it first. This file is only the steps and does not restate them.
- Voice: if `~/.claude/config/writing-voice.md` (or, on older installs, `~/.claude/CLAUDE.md`) has a `### Writing voice` section, invoke the skill it names (and fetch its voice page) before drafting comments. Otherwise the `reviewing-prs` comment rules pasted into `dispatch-prompt.md` are the whole style guide.
- Tracker: the `### Issue Tracker` section gives the ticket URL format, used only to read the linked ticket for context.

## Procedure

1. **Dispatch the reviewer** (`Agent`, `general-purpose`, `model: opus`) with the prompt in `dispatch-prompt.md`. It runs `/code-review <effort> <PR URL>` (effort first, never `--comment`, never `--fix`), reads the PR description, linked ticket and existing review threads, and returns a verdict plus drafted comments. It posts nothing. `/code-review` forks its own background reviewer, and that reviewer's findings arrive as a task notification in the main session, not inside the wrapper agent, which goes idle waiting. When that happens, forward the findings to the wrapper with `SendMessage` and let it draft; do not draft in the main session.

   If the review was asked for in Slack (a DM, a channel post or a thread), add `:eyes:` to that request message with `slack_add_reaction` as soon as the reviewer is dispatched.
2. **Triage** the findings it returns with the `reviewing-prs` triage table, and drop anything an existing review thread already raised.
3. **Present** to the user: PR summary (3 lines), the verdict per `reviewing-prs`, then each comment as `file:line`, severity, the drafted text, plus a one-line review body only when `reviewing-prs` says one is needed. Ask for approval per its posting rules; the user can drop or reword any item or post only the highs.
4. **Post** one review with every approved comment in a single call, so the author gets one notification:

   ```bash
   gh api repos/<owner>/<repo>/pulls/<n>/reviews --input review.json
   ```

   where `review.json` is `{"event":"APPROVE"|"COMMENT","body":"","comments":[{"path":"<file>","line":<n>,"side":"RIGHT","body":"<text>"}]}`. `body` is the approved one-line summary from step 3, or empty. No signature or attribution line, per `reviewing-prs`. `line` is the line number in the new file for `RIGHT`, the old file for `LEFT`. If GitHub rejects a line as outside the diff, fall back to the nearest changed line in that hunk and say so.
5. **Verify** with `gh pr view <n> --json reviews,reviewDecision` and report: review id, event, comment count, and the PR link.

   For a review asked for in Slack: once an APPROVE has posted, add the workspace's approval emoji to the same request message (`:approved_github:` where it exists; if `slack_search_emojis` finds nothing or the add fails with `invalid_name`, use `:white_check_mark:`). A COMMENT review gets no second reaction. Reactions need no approval. Log each one as a line under `## Reactions` in the board scratchpad (append-only, `HH:MMZ <emoji> on <channel> <ts>`), never in the Drafts table, which wrap checks as drafts.

## Model discipline

Reviewer agent: opus (judgment). The main session never reads the diff itself; it triages the agent's list and talks to the user.

## Common mistakes

Rule mistakes (approving with a high, posting before the list, findings stated as facts, a summary body) are in `reviewing-prs`. These are the step mistakes.

| Mistake | Fix |
|---|---|
| `/code-review 2249 medium` | Effort level goes first. The skill reads its first token as the level |
| `/code-review medium <n>` with a bare number | Resolves against the current directory's repo. Always pass the full PR URL |
| Passing `--comment` or `--fix` to `/code-review` | Posting is this skill's step 4, with one combined review; fixes are the author's job |
| One `gh pr comment` per finding | One review submission, one notification, inline anchors |
| Reviewing the user's own PR | That is `/pr`'s self review. Stop and say so |
| Running the reviewer on sonnet | The wrapper agent runs on opus; its model is what puts the forked review on opus |
| Logging a reaction in the Drafts table | Reactions go under `## Reactions` in the board scratchpad |
| Waiting on the wrapper agent while `/code-review`'s findings sit in the main session | The forked reviewer reports to the main session. Forward its findings to the wrapper and let it draft |

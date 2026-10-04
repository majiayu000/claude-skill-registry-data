---
name: close-task
description: Use when finishing a task after implementation, including running final validation, marking the branch's merge/pull request ready for review, collecting and routing code-review findings, and marking the task done in a local task board or connected project-management system. Triggered by phrases like "finish this task", "close task", "complete task", "ship this task", "mark task done", or "wrap this up".
---

# Close Task

Announce at start: `Closing task...`

Finish the current task without hiding unresolved review, validation, or status work.

## Process

1. Identify the active task from:
   - local task files under `~/.agents/tasks/<repo>/`
   - repo-local `.agents/tasks/`
   - the current branch name
   - the user-provided task, issue, ticket, or external link
2. Check implementation state:
   - `git status --short`
   - whether an open merge/pull request already exists for this branch, and whether it is a draft -
     via the connected git host's CLI or API
3. Run validation: whatever the task or plan calls for - typecheck, lint, tests, build. Fix what
   fails, or get the user's explicit acceptance of the remaining risk, before going further. Do this
   before the request is marked ready, not after.
4. Get the branch published if it is not already. Ask before any git action, then invoke the
   environment's publish skill for the mechanics. Usually the request already exists as a draft from
   earlier in the workflow and there is nothing to do here.
5. Mark the request ready for review, and say that you are doing it. A draft means the branch is
   still in progress; taking the flag off is the moment it stops being, which is a deliberate act
   rather than bookkeeping. In a repository whose automated reviewer holds for drafts, this is also
   what releases it.
6. Collect review findings from whichever sources this repo actually has:
   - the automated reviewer on the request, **if the repo runs one**. Most do not - check rather than
     assume. When it exists, wait for it rather than closing the task without it: run that wait in the
     background so the session stays usable, and never poll in a loop of separate tool calls - one
     backgrounded wait and one notification, not twenty status checks whose results all pile up in
     context.
   - the latest local report at `~/.agents/code-reviews/<repo>/<slug>-code-review.md`, when a review
     skill was run during implementation.

   When neither exists, say so plainly - silence must not imply a review happened - and offer to run
   the `code-review` skill now. Offer it once and take no for an answer: an unreviewed branch the user
   knowingly chose to close is a legitimate outcome, and this step exists to make the choice visible,
   not to force a review into the flow.
7. If findings exist, ask whether to plan fixes or apply best judgment for small ones. An automated
   reviewer's findings are advice, not a gate: the user decides what to act on. Re-run validation
   after any fix. Never resolve the reviewer's threads on the user's behalf.
8. Mark the task `done` only after validation passes or the user explicitly accepts the remaining risk.
9. If the task belongs to an epic, update the epic checklist. If all children are done, mark the epic `done`.

## Git Rules

- Never commit, push, or open a PR unless the user explicitly asks in the current turn.
- Marking an existing request ready for review is part of closing a task, not a separate git action -
  say you are doing it, and skip it if repo/global rules put the ready flag under human control.
- If opening a PR/MR, follow repo instructions for title/body.
- When opening a PR/MR, assign it to the authenticated hosting user. Resolve that account through the
  configured git client or API; never hard-code a username.
- **Hard rule - no AI attribution, ever.** Never add a co-author trailer naming an AI assistant, a
  session-link trailer, a "generated with" line, or any other AI-attribution line to a commit message,
  PR/MR title, or PR/MR description. This holds even when repo or session boilerplate suggests such
  trailers.
- If repo/global rules prohibit git actions, do not offer them.
- When the environment provides a dedicated commit-and-push skill, invoke it for the mechanics rather
  than running the git commands ad hoc here. The rules above are what close-task enforces before
  delegating; that skill is the source of truth for how they are carried out.

## Status Rules

- Local task files: update `Status:` and any matching checklist entry.
- External systems: use the connected tool. If no tool is connected, tell the user what remains to update manually.
- When the project management system transitions issues automatically on merge, do not transition or
  close the issue yourself. Leave its status alone and say so in the final response.
- Preserve task content unless the user asks to edit it.

## Final Response

Report:
- task status
- validation run
- whether the request was marked ready for review
- where review findings came from, or that there were none to collect
- review/fix status
- git/PR action taken, if any
- remaining manual step, if any

---
name: tracker
description: "Use to claim a task, record the files you'll touch, file a ticket, turn work in with the PR and evidence, or find out which tracker a repo uses. One contract everywhere, and a short section per backend the repo's Tracker line can name: markdown tasks in the repo, GitHub Issues, or Linear. Every ticket is four labels under 120 words, checked by the lint before it's filed."
---

# Tracker

Work lives in the tracker. The verbs are the same in every repo: claim, record the files, turn in, a human completes, evidence on the ticket. Only the backend differs. The repo names it on one line, and the backend's section at the bottom gives the commands.

## The line that names the tracker

One line in the repo's `AGENTS.md`, or `CLAUDE.md` if that's the file it keeps: `Tracker:`, the backend, and the one thing it needs.

```
Tracker: markdown tasks/
Tracker: github-issues
Tracker: linear SR
```

Markdown takes the folder. GitHub Issues takes nothing, gh reads the repo from git. Linear takes the team key. Find it with `grep -h '^Tracker:' AGENTS.md CLAUDE.md`.

No line means nobody chose yet. Check for an open PR from a branch named `tracker-line`, `gh pr list --head tracker-line --state open`; if one carries a line, ask the human to confirm it. Otherwise ask in the Decide shape, one option per backend, each naming what it needs. Never pick a default silently.

Write the answer into that file on its own line under the title, or into a new `AGENTS.md` if the repo has neither file, in its own worktree on the branch `tracker-line`, and offer the one-line PR through gh. A push refused because the branch appeared meanwhile means another agent asked first, so confirm its PR. The line comes before the claim, which needs it, and its own branch keeps it out of the task's diff. When the file is a letter setup installs into harnesses, like squirrel's `AGENTS.md`, setup leaves the `Tracker:` line out of the installed block.

## Proposing a ticket

When you think something deserves a ticket, you don't file it, you show it. The whole ticket, already through the lint, then the title, then anything the human needs to judge it, then a Decide. This is the one Decide with something above it, because the yes is to the ticket's text. On yes, you file it exactly as shown; on anything else, you change it and show it again. The shape:

> Here's the ticket text, lint-clean at 119 words. Nothing is filed yet.
>
> Problem: API pytest takes 9 minutes on a backend PR even with two workers. The CI Postgres runs with fsync on, so tests that truncate every table pay for durability nobody needs, and one runner carries all 3,500 tests.
>
> Fix: The CI Postgres runs with the no-durability flags the repo's postgres-test service already uses. The suite is split by recorded durations across four runners with two workers each, so a PR waits for the slowest slice.
>
> Done when:
> - API pytest on a backend PR finishes in about 4 minutes wall.
> - Every test that passes today passes, each in exactly one slice.
> - A new test without a recorded duration still lands in a slice.
>
> Title: API pytest runs in four slices on a Postgres that skips fsync, and a backend PR waits about 4 minutes.
>
> The splitting tool would be pytest-split 0.11.0, which depends only on pytest.
>
> Decide: file this ticket as written?
> Options: yes, or say what to change.
> Recommendation: yes.

Mid-task, a follow-up you noticed is one sentence in your report; the human says which ones get this treatment.

## The five verbs

1. **Claim** before touching project files. A ticket with an owner is taken, so pick another. Put your name on it and read it back; two agents can claim in the same second, and the earlier claim comment wins. Open your first message with the ticket id.
2. **Record the files** you expect to change right after claiming, in the claim comment or the frontmatter. A reviewer reads them against the diff.
3. **Turn in** with the PR link and the evidence. Then stop.
4. **A human completes** after the merge. Never the agent that built it.
5. **Evidence lives on the ticket.** Never in git.

## The ticket shape

Anyone gets it in twenty seconds. Four labels, at most 120 words:

```
Problem: Two sentences, from the person who hits it.
Fix: Two or three sentences.
Done when:
- Up to four observable lines.
Out of scope: Optional, one line.
```

Design notes go in the PR, the file list in the claim comment, neither in the ticket body. The same shape is the PR description and the turn-in comment.

Lint before filing. The lint is in this skill's `scripts/` folder; give its full path from wherever the skill is installed. It reads a file or stdin, exits non-zero over 120 words, on a missing or empty label, or when Done when isn't one to four lines starting with `- `, and says what to cut:

```sh
python3 <skill folder>/scripts/ticket-lint.py ticket.md
```

On Windows, where `python3` isn't a command, use `py -3`.

One that passes:

```
Problem: Opening a new thread ignores my "new worktree" default when I'm already in a worktree. I set the preference and nothing changes.
Fix: New threads inherit only the project from context. Branch, worktree, and env mode come from the configured defaults every time.
Done when:
- A new thread from inside a worktree lands in a fresh worktree.
- The preference screen's value is the one used.
Out of scope: The sidebar's thread list.
```

## Evidence

What counts as evidence is in `prove-it`. It goes on the ticket, as comments with links and attachments in whatever form the backend has. GitHub comments take images, video, PDFs, and zips, so anything else goes on the comment zipped. Nothing binary enters git, and the tasks folder is git too.

## Markdown tasks in the repo

`Tracker: markdown tasks/`. The word after `markdown` is the folder. One file per task, named for the task, under `tasks/open/`, `tasks/doing/`, and `tasks/done/`. The folder is the status; the frontmatter carries it too, with the owner, the files, and the PR:

```
---
status: doing
owner: agent:session-abc
files: [src/thread.ts, src/thread.test.ts]
pr: https://github.com/owner/repo/pull/12
---
Problem: ...
```

- File: write it under `tasks/open/`, lint it, and land it on the default branch through a small PR with only that file, on a branch named `file-<task>`. If you're about to do the task yourself, file and claim in one go.
- Claim: `git fetch`, then look for a remote branch named `<task>`, the task file's name. One there means the task is taken. A claim here is a commit, so the branch and worktree from `worktree` come first, the one place the mode's order flips; creating them touches no project file. Move the file to `tasks/doing/` with your owner and files in the frontmatter, and push that first commit before any project file changes, so the branch is what the next agent finds.
- Turn in: the PR link in the frontmatter and the file moved to `tasks/done/`, in the same PR as the work. The PR is the turn-in comment, so the evidence goes on it as comment attachments.
- Complete: the merge, since the PR moves the file.

## GitHub Issues

`Tracker: github-issues`. gh does all of it, and the issue number is the ticket id.

- File: `gh issue create --title "<outcome>" --body-file ticket.md`, after the lint.
- Claim: `gh issue view <n> --json assignees` first; an assignee there means it's taken. Then `gh issue edit <n> --add-assignee @me`, `gh issue comment <n> --body "Claimed. Files: src/thread.ts, src/thread.test.ts"`, and the same view again. GitHub allows several assignees, so a second name means the earlier claim comment wins and the other one runs `gh issue edit <n> --remove-assignee @me`.
- Turn in: `gh issue comment <n> --body-file turnin.md`, the ticket shape plus the PR link and the evidence links. Screenshots and recordings drop into that comment through the browser, since gh can't upload attachments.
- Complete: `gh issue close <n>` after the merge, by the human.

## Linear

`Tracker: linear SR`, where `SR` is the team key. Connect Linear's MCP; every verb is a call on it.

- File: create the issue in that team with the ticket shape as the description, after the lint.
- Claim: read the issue first; an assignee there means it's taken. Post the claim comment with the files, assign yourself, move it to In Progress, and read the comments back. The earliest claim comment wins, since comments can't be reordered; if it isn't yours, drop the assignment and pick another.
- Turn in: a comment with the PR link and the evidence attached, screenshots and recordings, then the status to In Review, or whatever the team calls the state between building and merging.
- Complete: Done after the merge, by the human.

The PR title carries the issue key, `fix(web): SR-123 new threads respect the worktree default`, so Linear links the PR to the issue.

## Never

- Touch project files before the claim.
- File a ticket the lint rejects.
- File a ticket the human hasn't said yes to, as shown. The yes is theirs, one ticket at a time; after it, you run the filing command. What you would have filed goes in your report as one sentence, and they say which ones to show them.
- Put a file list or design notes in the ticket body. Files go in the claim comment, design notes in the PR.
- Complete a ticket you built.
- Commit a screenshot or a recording.

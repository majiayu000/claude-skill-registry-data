---
name: start-issue
description: Get oriented on a GitHub issue and start developing it — from the branch you're already on, or from a number, link, or description you give directly. Reads the issue and its comments, follows any spike/decision it references, and makes sure you're on a linked branch before work begins. Use when asked to start, pick up, work on, or dev a specific GitHub issue.
---

# Starting work on a GitHub issue

Two ways in, one job either way: land on the right branch, then read enough to actually implement
the thing instead of guessing at it.

## 1. Find the issue

**Already on a branch for it.** Branch names from `pnpm issue:pick` (or step 2 below) look like
`feature/scripts/46-offline-issue-picker` — `<type>/<area>/<number>-<slug>`. Read the number off
`git branch --show-current` and confirm it with `gh issue view <number>` rather than trusting the
slug; slugs get hand-edited, numbers don't.

**Given a number, link, or description instead.** `gh issue view` takes either a bare number or a
full issue URL directly, so a `#46` or a pasted link needs no parsing. A plain description doesn't:

```sh
gh issue list --search "<the terms they gave you>"
```

Show the candidates and confirm the match before moving on — search is fuzzy, and starting work on
the wrong issue is expensive to notice later. Don't guess past one weak match.

## 2. Get on its branch

Skip this if step 1 already found you standing on the issue's branch.

**Pick it in the checkout you're in.** A single ticket never gets its own worktree, least of all
when the current checkout is on `master` with no branch picked. A worktree is only for asking for
more than one ticket at once, and even then one of them stays in the current checkout. In doubt,
ask before creating one.

Otherwise run `pnpm issue:pick` with the number. It asks nothing, and does what the interactive
pick does: builds `<type>/<area>/<number>-<slug>`, the area being the issue's area label, runs `gh issue develop --checkout` so the
branch is linked on the issue, self-assigns, and moves the issue to *In Progress*.

```sh
pnpm issue:pick <number>                                 # type and area from the labels
pnpm issue:pick <number> --type=feature --title="Short"  # when the label or the title won't do
```

- **It fails rather than guessing** on a `spike` or an unmapped label (pass `--type=`). Ask the user
  when the message names a choice you can't settle from the issue. An issue with no area label
  branches as `repo`.
- **The title becomes the slug**, so pass a shorter `--title=` when the issue title is long.
- **An existing branch for the number is checked out** instead of creating a second one, so
  resuming is the same command.
- A failed assignment or board move only warns; the branch is still checked out.

Check `git status --porcelain` first if you're not sure the tree is clean: the checkout carries
uncommitted changes over silently, which is usually fine but worth flagging before it happens.

## 3. Read the full context

One call gets the issue and everything it points at:

```sh
pnpm issue:brief            # on the issue's branch
pnpm issue:brief <number>   # anywhere else
```

It prints the body and every comment untrimmed — read past the body, the decision often lives in a
comment — then four sections, each a lookup you'd otherwise run by hand:

| Section | What to do with it |
| --- | --- |
| Blockers | Every `Blocked by #n`, with its title and state. For one that's closed, `pnpm issue:brief <n>` to learn what it settled, not just that it's done |
| Decisions | Reports in `docs/decisions/` whose frontmatter names this issue or one the thread mentions. Read every one before writing code on the same ground; a report on `status: to-implement` is the work you're about to do — its Result names the files, its Consequences the order and the tripwires, its Confirmation what to run at the end |
| Projects | The folders the issue touches, each with its `CLAUDE.md`. Read those, since Claude only loads a nested one once it reads a file there |
| Docs mentioned | Plans and guides the thread links. Read the ones the acceptance criteria lean on |

## 4. A ticket built from a lab: list the lab first

When the issue points at a `/lab/...` path, the lab is the spec. Before any code, open every lab
page the ticket covers, following its links (a list → its detail page, every tab), and post the
list as an issue comment:

```markdown
## Lab checklist

### /lab/idea/e/developer/catalog/[name] → /projects/<name>
- [ ] Header: breadcrumb, mono title, README description
- [ ] Tabs with counts: README, Coverage, Dependencies, Issues, Workflows
- [ ] About box: Version, Unreleased, Commits 2 wk, Specs, Lines covered meter, Changelog
```

One heading per lab page with the real route it becomes, one box per feature: a section, widget,
tab, filter, menu entry. Not one per pixel; a page is usually five to ten boxes.

- `gh issue comment <number> --body-file <file>` posts it. Tick boxes by editing that comment as
  each item lands, so any agent that picks the ticket up reads where it stands in `issue:brief`.
- **At the end of the session, read the list again.** An unticked box gets built now. If the
  context is spent, say which boxes are open and ask the owner to hand them to another agent.
  Never mention a gap only in the summary.
- [`lab-checklist.sh`](../../hooks/lab-checklist.sh) refuses to open the PR while the comment is
  missing or has an unticked box.
- **A correction on one page is a check on all of them.** When the owner corrects a pattern on one
  page, find every other page showing the same thing and fix them in the same pass (#484, #490).

## 4.5 What the ticket asks is what gets built

- A ticket's points never shrink its scope. Thirteen points on a rebuild still means a rebuild, not
  a reskin (#484).
- When the ticket conflicts with older feedback, a memory or a note in another doc, ask the owner
  before writing code. Never resolve it toward the cheaper path and report it in the summary.

## 5. Confirm before diving in

Summarize back in a few lines: what the issue is asking for, anything a blocking issue or decision
record changes about the approach, and what you're about to do first. This is the cheap check that
you read the right thread before spending a session on it — not a full plan, just enough for the
user to redirect you if you picked up the wrong end of it.

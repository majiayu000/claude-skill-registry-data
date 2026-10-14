---
name: implement
description: Implement one Kairos task from Todo to Completed. Use when the user names a task or short code to implement, asks to pick up the next todo item, or when groomed work is handed off for execution.
---

# Implement

Execute one Kairos task from Todo to Completed.

## Pick up

Your **queue** is the board of your team, filtered by the repository of this checkout. The SessionStart context gives both: `team_board` and `repository` (`.claude/kairos.local.md`, COLLIERY-A-0023). Given a short code, `get_item` it. Given nothing, `board_items` with `board=<team_board>`, `repository=<this repo>`, `column=Todo` and `details: true` → the highest-priority item with no unresolved `blocks` edge; state the pick and why before starting. With `details`, each card shows its priority, the date of its last change and its claim, so you need no `get_item` for each card. `list_metadata_definitions` gives the order of the priority values. (No `repository` wired? Fall back to `my_boards` → the delivery board → `board_items` unfiltered, and suggest `/kairos:bootstrap`.)

**Read each part of the board before you pick.** `board_items` gives 200 items at most in one result. When the result is a part of the board, its first lines say so and give the `offset` of the next part. Call `board_items` again with that `offset` until you have each part. Then make the decision. To read one column only, send `column` (`column=Todo`).

**Stay in your repository.** `get_item` prints the link of the task: `repository: <slug> (owner: <team>)`. The owner can be a different team; that is normal. If the slug differs from this checkout, stop: say which repository holds the code, and pick a different task. A task with no repository that needs code in this checkout: link it with `set_repository` (`short_code`, `repository`), then continue.

**The work of other teams in this repository is not in your queue.** Find it with `search` (`filter.repository`), or in the commits. Read it; the team of its board does it.

**A task on the wrong board is moved, not recreated.** When a ticket is on this board but is really another team's work, `move_item` it to their delivery board (`to_board`) — recreating it there throws away its history, its edges and its author. You need `manage_tasks` on both boards; if the tool refuses, name the board it belongs on and ask the lead. The task keeps its repository: the move does not look at it.

Anything procedural you write while implementing — a how-to or reference page, an error message, CLI help text — follows Simplified Technical English: [The Simplified Technical English reference](../../../references/simplified-technical-english.md) (KAIROS-S-0009). It does **not** apply to your commit message, your code comments, or the reasoning you record on the item; those exist to explain why, and STE cannot. `angreal docs ste` checks the mechanical rules where the project has that task, and `angreal docs ste --code` checks the texts of errors in the code.

The task must be workable: acceptance criteria present and independently verifiable, blockers resolved. When it isn't, stop, note the gap on the item, and tell the lead it needs `/kairos:triage` — surface the gap rather than quietly filling it yourself.

`transition_item` to **Active** before the first change. The move gives the task your **claim**: the board and `get_item` show that you (or your agent) work on it. If `get_item` shows a claim of a different person, the task is theirs: ask before you start, and do not take it over. A change to a task that a different person has the claim on succeeds, and the answer ends with a `Warning:` line that names the person; stop and tell the lead.

**Read your notifications.** While you have unread notifications, each answer of a Kairos tool ends with a block `## Your notifications (N unread)`: the 5 newest, then `N more: call get_events`. A notification tells you of a claim handed off to you, a blocker of your claimed task that is done or archived, a task that you created that someone cancelled, a mention of your user name, or a P0 bug on the board of your team. `get_events` lists them with their ids. Act on each one that changes your work (a cleared blocker can make a task workable; a P0 bug can come before your pick), tell the lead about the others, then `mark_events_read` (`ids`, or `all: true`). Do not mark a notification read before you have read it.

To give the task to a different person, `hand_off_item` (`to`: a user id, an email or a user name). To stop work on a task and leave it in Active for anyone, `release_item`. The claim ends by itself when the task leaves Active.

## Work

The task item is your **working memory**. Every few significant steps, `append_note` findings, decisions, dead ends ruled out, and plan changes onto it (one call: no version, no anchor text; the note gets a heading with the date and your name) — the item must let any session, or another agent, resume cold after this conversation's context is gone. Reference commits, files, and other items by hash, path, or short code rather than restating them. End each note with a `Next step:` line: after a context compaction, the plugin gives you that line again for each Active task.

To find code, use the code tools of the `kairos-code` MCP server before you read files: `module_map`, `code_search`, `callers` and `callees` (and `symbol`, `references` and `path`). Then read only the files that they name.

Use the `tdd` skill at pre-agreed seams where possible. Run the repo's fast checks — formatter, typecheck, single test files — as you go; the full suite once at the end.

## The completion gate

The task transitions Active → Completed **only** when all of these hold, with output recorded on the item:

1. **Gates clean** where the repo has them: formatter check, linter with warnings denied, full test suite green (in a Rust/angreal repo: `cargo fmt --check`, `cargo clippy -- -D warnings`, `angreal test unit && angreal test integration`; otherwise the repo's equivalents).
2. **Every acceptance criterion demonstrated, not asserted**: for each criterion, `append_note` the command you ran and the observed output onto the item as evidence.
3. **New behavior carries new tests.**

Then review the diff (the `code-review` skill), commit to the current branch, and `transition_item` to **Completed**. When the work needs a change from a DIFFERENT team (an API to add, a client to update), send a request to that team. The recipe is [CROSS-TEAM-FILING.md](CROSS-TEAM-FILING.md): `create_item` (`board: <the delivery board of that team>`, `parent: <this task's initiative>`), then `link_items blocks` from the request to this task.

## Blocked

When the task stalls on something outside your reach — a decision, access, another team — `link_items` (`blocks`) from the blocking thing to the task, `transition_item` to Blocked, and `append_note` a note naming exactly what's needed and from whom, on the task **and** on its parent initiative so the blocker surfaces at the Initiative Board Review. Then stop rather than guess.

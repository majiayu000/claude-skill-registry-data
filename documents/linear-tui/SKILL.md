---
name: linear-tui
description: Resolve what the user is looking at in linear-tui, act on Linear through the linear-tui CLI, and work the running TUI itself. Use when the user refers to an issue or list on their screen without naming it ("this issue", "the one I have open", "the top three", "この issue", "今見てるやつ", "上の 3 つ"), asks to comment on, move, edit, or file a Linear issue, or pastes notes that came from linear-tui.
---

# linear-tui

The user reads and triages Linear in linear-tui, a terminal UI. Its CLI shows
you what is on their screen and acts on Linear with their credentials — no
Linear MCP server or separate sign-in is needed.

## Find out what "this" is

Run `linear-tui context` before guessing. It prints, as Markdown:

- `- Showing:` — the page: team or view, then project or cycle, then issue;
- `## Open issue` — the issue open in the detail view, if any;
- the list on screen, numbered in display order, with `← cursor` on the row the
  user has selected (on an issue page, the list it was opened from);
- whether linear-tui is still open. A closed instance's view may be stale — say
  so if you rely on it.

"The top three" means rows 1–3 of that list; "this one" is the open issue, or
else the row under the cursor. Inside a worktree whose branch names an issue,
the context starts with that issue. Use `--json` when you need exact fields.

## Read and act

| Task | Command |
| --- | --- |
| List issues | `linear-tui issue list --team ENG` (`--preset backlog\|all`), `--mine`, `--view "…"`, `--project "…"`, `--team ENG --cycle current`; narrow with `--status`, `--priority`, `--query` |
| Search | `linear-tui issue search "checkout" [--team ENG]` |
| Read an issue | `linear-tui issue show ENG-42` |
| Comment | `linear-tui issue comment ENG-42 -` (body on stdin) |
| Reply in a thread | `linear-tui issue comment ENG-42 - --reply-to <comment-id>` |
| Fix or remove your comment | `linear-tui issue comment edit ENG-42 <comment-id> -`, `… comment delete ENG-42 <comment-id>` |
| Change its state | `linear-tui issue status ENG-42 "In Review"` |
| Edit it | `linear-tui issue update ENG-42 --title "…" --description - --priority low --assignee me --estimate 3 --label Bug --unlabel UI --project "…" --cycle current --parent ENG-30` (any of them; `none` empties a field) |
| File an issue | `linear-tui issue create --team ENG --title "…" --description -` (and the same fields as `update`) |
| File under a milestone | `--project "…" --milestone "Beta"` on `create` or `update` |
| Projects | `linear-tui project list --team ENG`, `project show "…"`, `project create --team ENG --name "…"`, `project update "…" --status "In Progress" --target 2026-12-01`, `project update "…" --content -` (its body; `--description` is the one-line summary), `project delete "…"` |
| Milestones | `linear-tui milestone list "<project>"`, `milestone create "<project>" --name Beta --target 2026-11-01`, `milestone update "<project>" Beta --name …`, `milestone delete "<project>" Beta` |
| A team's states, members, labels | `linear-tui team show ENG` (`team list` for the teams) |
| Cycles, views, favorites | `linear-tui cycle list --team ENG`, `view list`, `favorite list` |

`<ID>` may be an identifier in any case or an issue URL. `issue show` gives
each comment an `- Id:` line to address an edit or reply at. Errors go to
stderr with a non-zero exit; an unknown name lists what is valid, an
ambiguous one the candidates. Only a comment's author can edit or delete it.
Whatever the TUI does, a command does too: never call Linear's API directly,
or drive the TUI to do what a command can. Long bodies go on stdin as
Markdown. Deleting a project or milestone needs the user's word, like any
other change.

## Work the TUI itself

When the user wants to see something, or you want to check linear-tui by
using it, drive the running instance the way a person does:

| Task | Command |
| --- | --- |
| Read the screen: focus, what is open, keys and commands here | `linear-tui tui screen` |
| Press keys | `linear-tui tui press "j <Enter>"` (`<Esc>`, `<C-k>`, `<S-Tab>`, …) |
| Run a palette command | `linear-tui tui run "Change status"` |
| Type into the focused field | `linear-tui tui type "In Review"` |
| Show an issue | `linear-tui tui open ENG-42` |

Each answers with the screen it leads to; read it before the next step. A
chord is two keys (`g m`). With no linear-tui open, `linear-tui --headless`
runs one only you can see. Keys and commands change issues exactly as the
user's would, so the rules below hold here too.

## Rules

- Without an instruction to change an issue, only comment on it.
- Move or edit an issue — to Done, a new title, anything else — only when
  the user asks.
- Edit or delete only the comments you were asked to.
- Quote the identifier (`ENG-42`) when you report what you did.

The full output formats are in `docs/cli.md` of the linear-tui repository.

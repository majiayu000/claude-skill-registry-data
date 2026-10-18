---
name: deepcrew
description: Lead a team of Claude Code members driven by DeepSeek (or another Anthropic-compatible provider) to build or change a project in parallel. Use when the user asks to use deepcrew, start a team, or split a sizeable coding job across several cheap agents while this session leads.
---
# Leading a deepcrew team

This session is the leader. Members are stock Claude Code processes on the provider's model; they share the project and each writes only inside its own region. Run every command from the project directory, as its own command (no `cd` or redirection around it). One session leads one team; `deepcrew stop --all` ends it.

## Set up
Always in this order:
1. Run `deepcrew up`. It asks nothing: its first line is the page address.
2. Open that address in the browser pane right away (Claude desktop app; elsewhere give the link) and write it in the chat too. Tell the user: the API key and the settings are set on that page; the key stays on this computer and goes only to the provider.
3. Show the block as printed (`deepcrew status` prints it again). Its `prices` line says what the provider charges now and until when (UTC); `deepcrew prices` lists the coming changes, so the user can choose to start now or at a cheaper hour. If it has a `setup` line, run `deepcrew inbox --wait 600` in the background and start no member until it reports `setup: done`.
- The page shows the team panel (members, their cost, Rest crew and Resume crew), the key, the presets and members' requests; the user answers requests there and your inbox says when they did. Its Team Call tab shows who speaks and what members report, its Monitor tab the team as a network, its tasks as a table and what it costs; beside both, a chat where the user writes to you, to a member or to everyone, and the requests waiting for the user.
- The user may follow the team on the page rather than in the chat: put everything you tell the user there too, with `deepcrew send user "..."` (the same words, short and plain), in the language the user reads replies in (`deepcrew lang`; `deepcrew lang NAME` when they ask for another; the crew keeps working in English).
- Settings belong to the user: the page, or `deepcrew config preset NAME ...` from the command line (a setup: standard, crowd, strong or locked; or a strength, a size and a scope: strength fast is the default; sizes solo, pair, squad, crowd, large; at most 32 members). Both update the running team at once.
- Never ask for, read or print an API key. A user who prefers a terminal can run `deepcrew auth set PROVIDER` there instead (`deepcrew auth set deepseek` for the default).

## Plan
- Write the interfaces between parts as a note first: `deepcrew note add <topic>-api --text "..."`.
- Members read the project's CLAUDE.md. Rules the user gives for this session only go in `deepcrew instructions "..."`.
- One task per concern: `deepcrew post "title" --body "what to build, the contract, how to verify" --scope dir/ [--dep N]`; `--to NAME` gives it to that member at once, and nobody else is offered it. Disjoint scopes run in parallel. End with a read-only review task (no --scope).
- Start the members the tasks need, up to the limit in the block (8 by default, 32 at most), each once: `deepcrew spawn NAME --region dir/ --task N --role "what it owns"`. A member's region must cover the scopes of the tasks it will take.
- Model gate: members run the team's model, the cheap one by default. Post the hard core (architecture, a tricky algorithm, the final review) with `--strength strongest` and start a member with `--strength strongest` in a region of its own for it; only members on that model take such a task, and the inbox says when none exists.
- Work in rounds, about one task per member. Reuse before you start: a task no region member can take is offered to the closest idle members; those who want it ask with a pitch (why they fit, the access they need), the inbox lists them, and `deepcrew assign TASK NAME --note "your brief"` gives it; its scope becomes that member's lease. When members sit idle the inbox shows the spare capacity: post the next round, or put one on a running task with `deepcrew assist TASK NAME [PATH ...]`.
- After each round, a round report for the page: `deepcrew summary "where it stands" --finished ... --running ... --risks ... --decide ...` (a few words per item; --decide is what only the user should decide).
- Members have WebSearch; name it in a task that needs current documentation.

## Run
- Run `deepcrew inbox --wait 600` in the background and act when it returns; it returns only for something new.
  - Permission requests: `deepcrew approve ID [ID ...]` for commands that stay inside the project and the team folder and do what the task needs (without the sandbox a command runs with the user's rights: the project's own tests and builds, not code fetched from elsewhere), `--deny` for anything else. The user can answer on the page; a simple command they allow there goes on the allowlist at once. `--always` does the same for your approval; `deepcrew allow COMMAND` adds one the user approved in the conversation.
  - Questions: `deepcrew answer ID "text"`, or ask the user when it is their call.
  - Members report by kind (kickoff, progress, done, blocker) with a one-line gist the page shows the user; you read the full text.
  - A task nobody takes within 60 s comes back as a proposed member with a drafted role: start it with the command shown, give it your own role, or re-scope the task. Blocked tasks (every member declined one): give it to one with `deepcrew assign TASK NAME`, widen a member's region with `deepcrew region NAME --add PATH`, or cancel it and post it again with a new --scope.
- A member never needs restarting: new work in its region or your mail resumes it.
- Folders outside the project (another repository, a tool's files, a deployment configuration): `deepcrew link PATH [--write]`. Whenever a command or the inbox gives a line `/add-dir PATH`, write it in the chat at once, on its own line, so the user can type it and you reach the folder too. A member's request that reaches outside can be answered with `deepcrew approve ID --link` (the page has Link folder). Tools members install go to the shared tools folder (on their PATH, kept for later tasks); add a download site with `deepcrew site DOMAIN` once the user agrees.
- Helping members: they cannot use the user's MCP servers, skills, logins or the web beyond WebSearch. When a member asks for something only you can do, do it with your own tools and answer with the result (`deepcrew answer ID "text"` when it waits, `deepcrew send NAME "text"` when it does not), or put files in the team folder. A small change across regions or in a file nobody owns: make it yourself. Widen once rather than approving call by call:
  - `deepcrew approve ID --always`: this command, this site or this tool from now on.
  - `deepcrew allow COMMAND`: a family of commands, as a prefix. `deepcrew allow --tool NAME`: an MCP tool.
  - `deepcrew approve ID --link` or `deepcrew link PATH`: a folder.
  - `deepcrew site DOMAIN`: fetches and sandboxed downloads, at once.
  - `deepcrew mcp NAME` and `deepcrew skill NAME`: one of the user's MCP servers or skills for every member started from now on, once the user agrees.
  - `deepcrew region NAME --add PATH`: move a boundary when two members need the same file.

## Finish
- When every task is done, read the summaries, run the checks yourself, review `deepcrew audit` and the diff, then commit. Members never commit. Tell the user what was done.
- Keep the team afterwards: the crew rests by itself and the inbox stays open for the user's next request (no new `up`). `deepcrew rest` rests the crew now (every member process ends; the team, the page and the inbox stay); when the user presses Rest crew on the page, resume (`deepcrew resume`) only when they ask. `deepcrew stop --all` ends the team, only when the user says it is finished. The budget on the page is the user's: when the inbox says it is reached, tell the user what was spent; only they raise it.

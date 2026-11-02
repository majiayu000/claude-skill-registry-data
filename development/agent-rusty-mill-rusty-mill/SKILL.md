---
name: rusty-mux
description: Drive the rusty_mux terminal multiplexer with rusty-mux-ctl. Use when RUSTY_MUX_BLOCK is set, or when asked to run, watch or read programs in rusty_mux sessions, windows or blocks.
---

<!-- Installed by `rusty-mux-ctl agent setup`; `rusty-mux-ctl agent remove` deletes it. -->

# rusty_mux

rusty_mux keeps terminals running on a server. A **session** holds
**windows**, a window holds **blocks**, and each block runs one program in its
own terminal. `rusty-mux-ctl` drives the server from a shell. Inside a block,
`RUSTY_MUX_SOCKET`, `RUSTY_MUX_SESSION`, `RUSTY_MUX_WINDOW` and
`RUSTY_MUX_BLOCK` say where you are, and ctl uses them by default.

## Where things go

- A command that names no block, window or session acts **here**: the block,
  window or session you run in. Name a target to act anywhere else.
- A target is a full id, a name, a position from 1, or the last four or more
  characters of an id, tried in that order. `main/logs/2` is the second block
  of window `logs` in session `main`. A name or id that matches more than one
  thing is refused with exit code 3; it never picks one.
- Start your own work in **your own window**, the one you run in, unless the
  user names another. Do not add blocks to windows you did not create without
  being asked.
- Name every block you create (`rename-block`), so you and the user can find
  it again by name rather than by position, which shifts.
- Close the blocks you created when you are done with them, unless the user
  wants them kept.

## Running programs

```sh
rusty-mux-ctl run --wait --timeout 600 -- cargo test   # exit status is the program's
id=$(rusty-mux-ctl run -- npm run dev)                # starts it, prints the block id
rusty-mux-ctl rename-block --block "$id" --name dev-server
rusty-mux-ctl wait --block dev-server --timeout 30    # 124 on timeout
rusty-mux-ctl close-block --block dev-server
```

`run` places a block out of the way. To show one beside yours instead, split
it off: `rusty-mux-ctl split-block --side right --command htop`. `zoom-block`
shows one block alone and `unzoom-window` ends it; `list` gives each window's
`layout`. Each session has an active window, the one clients show for it:
its first window, until `select-window --window W` picks another. A window
you create does not take it.

Prefer `wait` over polling. `wait --window W` or `wait --session S` waits
until every block there has ended, blocks started meanwhile included; it
prints each exit and exits with the last failure, 0 if every program
succeeded. `wait --event KIND --FIELD VALUE` waits for an event, such as
`wait --event bell --block dev-server`.

## Reading and typing

```sh
rusty-mux-ctl terminal.format --block dev-server --history 200 --trim --unwrap
rusty-mux-ctl terminal.process --block dev-server   # what runs there now
rusty-mux-ctl terminal.pwd --block dev-server
rusty-mux-ctl acquire-lease --block dev-server + terminal.send-keys --block dev-server --key ctrl+c
```

Typing (`input`, `terminal.send-keys`) needs the block's input lease, and a
user typing in that block holds it. Only type into a block someone else uses
when the user asked you to. Requests joined by `+` run in order on one
connection.

## Finding out more

- `rusty-mux-ctl list` shows every session, window, block and client; each
  client with the principal (user) the server verified and its transport.
  `rusty-mux-ctl whoami` shows your principal. Each ctl call is its own
  client, so the id it prints is gone once the call returns.
- `rusty-mux-ctl help` lists every command; `help COMMAND` shows its flags.
- `--json` prints one JSON object per line.
- Exit codes: 0 ok, 1 refused, 2 bad command line, 3 target missing or
  ambiguous, 4 no server, 124 timed out; `wait` and `run --wait` otherwise
  exit with the program's status.

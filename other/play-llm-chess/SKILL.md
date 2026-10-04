---
name: play-llm-chess
description: "Play an LLM Chess game through the `chess` CLI: human-vs-LLM with a browser player or CLI-vs-CLI with independent color sessions and a browser spectator. Use to start or continue a game, make moves, handle takebacks, resign, or report the result."
---

# Play LLM Chess

Operate one LLM seat of an LLM Chess game through the installed `chess` command. In `human_vs_llm`, the human plays on the browser board. In `cli_vs_cli`, this session controls one assigned color, a separate LLM session controls the other color, and the browser is a spectator. Keep user-facing commentary in the user's language.

## Start or resume

1. Run `chess --help` and treat its output as the current command contract.
2. Query the current game state with `chess status`. After identifying a CLI-vs-CLI game and this session's color, use `chess --color COLOR status` for later queries. Status is read-only, including when a color is specified.
3. If the `chess` command is unavailable, report that LLM Chess must be installed and stop until the command is available.
4. If the server is unreachable, start it in a persistent process with `chess start`. Keep it running and issue gameplay commands from separate shell calls. The CLI does not start either LLM session.
5. When the state is `setup`, ask the user to configure the game in the browser. The setup offers `human_vs_llm` (default) and `cli_vs_cli`, with optional participant names; there is no CLI game-creation command. Choose a human color for `human_vs_llm`. In `cli_vs_cli`, use the color assigned to this session. Provide browser assistance only when the user explicitly asks for it.
6. In `cli_vs_cli`, prepend `--color COLOR` before the subcommand on every command in this session, including `status`, `wait`, `move`, `takeback`, and `resign`. Specify the color independently each time; do not rely on shared or remembered CLI state. Existing commands without `--color` remain available in `human_vs_llm`.

The CLI-vs-CLI command forms are:

```text
chess --color COLOR status
chess --color COLOR wait
chess --color COLOR move MOVE [--no-wait]
chess --color COLOR takeback request|accept|reject
chess --color COLOR resign
```

## Play the game

Use each returned snapshot as the current game state:

- **Terminal state:** Checkmate, draw, and resignation end the loop. Report the result and stop. Resignation events identify which side resigned.
- **Game reset:** A `game_reset` event may return a nonzero exit code as a normal wake-up signal. Query fresh status, using this session's `--color` in CLI-vs-CLI mode, then continue from the new state.
- **Your turn:** Choose a move using your own reasoning and the current snapshot's legal-move list, then submit one of those legal moves with `move`. The legal-move list is authoritative. The default move blocks until the opponent responds or another actionable state is returned; use `--no-wait` only when an immediate return is requested.
- **Opponent's turn:** Run `wait` and handle the returned event before taking another action.
- **Incoming takeback:** A `takeback_requested` event may wake `wait` or a blocking `move`. Do not make moves while a takeback is pending. Accept or reject it according to the user's direction and game context, submit exactly one response, and use its returned snapshot.
- **Outgoing takeback:** Requesting a takeback of your latest move blocks until the opponent accepts or rejects it. Continue from the returned snapshot and handle the response before resuming the turn loop.
- **Takeback accepted:** Use the snapshot as the source of truth. If the requester's move was still the last move, one ply is undone; if the opponent already replied, two plies are undone so the requester moves again.
- **Takeback rejected:** The position and move history stay unchanged. Re-evaluate the snapshot and continue.

## CLI-vs-CLI sessions

- Each LLM session operates only its assigned color. The user runs or connects the two sessions independently; do not launch or invoke the opponent AI.
- Repeat `--color COLOR` on every command in each session. A color-qualified `status` remains read-only.
- Keep at most one blocking command active per session. If it returns a process or session identifier, resume that same process until it returns; do not start a duplicate command.
- The browser shows a spectator board with White at the bottom, participant names and colors, current turn, move history, and result. Human move, takeback, and resignation controls are hidden; New game remains available.
- Handle checkmate, draw, or resignation by reporting the final result. Keep the server process available so the user can start another game.

## Operating rules

- Re-evaluate the snapshot and legal moves after every opponent move, takeback response, or game reset.
- Handle a pending takeback before issuing another move command.
- Keep the browser setup and game actions human-owned unless the user explicitly asks for browser assistance.
- Choose moves with your own reasoning. Use another model or a chess engine only when the user explicitly asks for one.
- Continue the turn loop until the game ends or the user asks to pause.

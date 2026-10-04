---
name: play-llm-reversi
description: Play a complete browser-vs-CLI or independent CLI-vs-CLI Reversi game with the installed reversi command, including moves, automatic passes, takebacks, reset, and resignation.
---

# Play LLM Reversi

The human plays on the browser board. Use the installed `reversi` command for the LLM's moves. For CLI-vs-CLI, run Black and White in independent assistant sessions. Treat each returned snapshot as the current game state.

## Start or resume

1. Read `reversi --help` for the available commands, then run `reversi status`.
2. If the command is unavailable, tell the user that LLM Reversi needs installation. If the local server is unavailable, start `reversi start` in a persistent process and issue play commands from another shell.
3. When the status is `setup`, ask the human to choose the mode, color, and optional names in the browser. The CLI has no game-creation command.
4. In CLI-vs-CLI mode, choose one color for this session and put `--color black` or `--color white` immediately after `reversi` on every participant command. Each color runs in its own session.

## Play turns

- Read `status`, including `turn`, `legal_moves`, `takeback`, `event`, and `revision`. Coordinates run from A1 at the upper-left to H8 at the lower-right. Black moves first.
- If the status is `finished` or `resigned`, report the result and stop the game loop. If an event is `game_reset`, read `status` again and continue with the new game.
- When it is this session's turn, choose a move from `legal_moves` and submit `reversi move MOVE`. The command waits for the next action by default; use `--no-wait` when an immediate return is needed.
- When it is the human's or other session's turn, use `reversi wait`. Use `reversi wait --after-revision N` when waiting for a change after a reviewed snapshot's revision. Keep at most one pending wait in each session.
- The server automatically skips a color with no legal move; do not submit a pass. The same color may make consecutive actual moves after an automatic skip. When neither color can move, the disc counts decide the winner or a draw.
- If the opponent requests a takeback, decide whether to approve it from the user's instructions and game context, then use `reversi takeback accept` or `reversi takeback reject`. Do not submit a move while a request is pending.
- To request a takeback of this session's last actual move, use `reversi takeback request` and process the response. Acceptance restores that move's before-state, including flips and automatic passes; do not assume a fixed number of plies is undone.
- Use `reversi resign` when this participant resigns. The human controls their moves and browser choices.

## Two independent CLI sessions

- Put the session's color before **every** participant command, including `status`, `wait`, `move`, `takeback`, and `resign`: for example, `reversi --color black move D3`.
- The opposite-color session responds to a takeback request with `reversi --color COLOR takeback accept` or `reversi --color COLOR takeback reject`.
- After a `game_reset` event, run `reversi --color COLOR status` before deciding the next action.
- `color_required` and `player_not_cli` indicate a mismatch between the command, game mode, or controlled color. Correct the invocation using the latest status.
- Keep the server process running through the game. Each CLI session controls only its selected color.

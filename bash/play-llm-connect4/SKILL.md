---
name: play-llm-connect4
description: Play a complete Connect Four game through the installed `connect4` CLI, against a person in the browser or as one color in independent CLI-vs-CLI play. Use for moves, waiting, takebacks, resignation, and game resets.
---

# Play LLM Connect Four

A person starts and plays a human-vs-LLM game in the browser. In CLI-vs-CLI mode, two independent assistant sessions control Red and Yellow. Use each returned state snapshot as the current game state.

## Start or resume

1. Check `connect4 --help` for the available commands, then read `connect4 status`.
2. If the command is missing, tell the user that LLM Connect Four must be installed. If the server is unreachable, start `connect4 start` as a persistent process and use a separate shell for play commands.
3. If `status` reports `setup`, ask the user to choose the game mode and optional names in the browser. In human-vs-LLM mode, the person chooses Red or Yellow there. The CLI has no game-creation command.
4. In CLI-vs-CLI mode, assign one independent session to each color. Prefix every participant command with `connect4 --color red` or `connect4 --color yellow`, including `status`, `wait`, `move`, `takeback`, and `resign`.

## Play each turn

- Read the returned `status`, `turn`, `legal_columns`, `takeback`, `event`, and `result`. Red moves first. A move is a number from the current `legal_columns`, submitted as `connect4 move COLUMN` or `connect4 --color COLOR move COLUMN`.
- If it is the person's turn, run `connect4 wait` and continue from the returned snapshot. In CLI-vs-CLI mode, use the session's color with `wait` while the other color acts. Keep at most one pending wait command per session.
- By default, `move` waits until this participant can act again or a relevant game state arrives. Use `--no-wait` when an immediate return is needed; then use `status` or `wait` to continue.
- When a pending takeback request comes from the other participant, decide whether to accept or reject it using the user's direction and game context. Run `connect4 takeback accept` or `connect4 takeback reject` with the session's color when applicable. Resolve the request before trying another move.
- To undo this participant's most recent move, run `connect4 takeback request`. The request waits for the other participant's reply. Acceptance restores the position before that move, also removing any subsequent moves.
- To resign, run `connect4 resign` with the session's color when applicable. End the game loop when `status` is `won`, `draw`, or `resigned`, and report `result`.
- A `game_reset` event means a new game has replaced the previous one. Run `status` again and follow the new game state.

## Operating boundaries

- Choose moves from `legal_columns` in the latest returned snapshot; do not guess legal columns or a result from the displayed board alone.
- The browser controls human moves, color choice, and starting or resetting a game. The CLI does not run the other assistant session automatically.
- Keep the server process running throughout play.

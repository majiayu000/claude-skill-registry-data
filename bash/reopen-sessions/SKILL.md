---
name: reopen-sessions
description: Reopens, one terminal tab each, the Claude Code sessions that were running before the terminal, the IDE or the computer crashed or closed, or the ones about a topic the user names, in whatever terminal or app the user runs them in (Ghostty, iTerm, Terminal.app, WezTerm, kitty, Windows Terminal, GNOME Terminal; JustSessions, an IDE or any other app gets the steps or commands instead). Use when the user says "reopen my sessions", "my terminal crashed", "WebStorm crashed, bring my sessions back", "resume all the sessions I had open", "reopen the session about…", "rouvre mes sessions", or after moving to another terminal app.
---

# Reopen sessions

`$SK` is this skill's base directory. `claude-reopen.sh` lists the interactive sessions that no longer run, newest first, with how long ago each was used, its folder and its title (the `/rename` title, else the one Claude Code gave it, else its first prompt), and opens the chosen ones in new tabs of the terminal it runs in, each in its folder with `claude --resume <id>`.

1. **Find them.** After a crash: `bash "$SK/claude-reopen.sh" --list` (the last 30 minutes; add a number of minutes when it was earlier). For a session the user names by topic: `--list --find "<words>"`, any age, matched on titles and typed prompts. Memory can help too: a note in the user's memory or knowledge base (the kb skill) often records the session it came from (`originSessionId: <id>`, `source: session:<id>`); search it for the topic and use that id.
2. **Agree on the list.** Nothing marks which sessions were open at the crash: a time window can catch one the user had already left. Show the list and ask which ones, unless it plainly matches what the user described.
3. **Open them:** `bash "$SK/claude-reopen.sh" <id> <id>…` (8 characters are enough).
4. **Check they run:** `ps -ax -o command | grep -- '--resume'` (Windows: `tasklist`). A shell can take a few seconds to start. If one did not start, give the `cd … && claude --resume …` line for it.

The terminal is the one Claude runs in (`TERM_PROGRAM`, `KITTY_WINDOW_ID`, `WT_SESSION`, `GNOME_TERMINAL_SCREEN`, else on macOS the app Claude's process runs under); `--terminal <name>` or `CLAUDE_REOPEN_TERMINAL` picks another. When the user has moved to another app since, ask where they want them and pass `--terminal`. JustSessions takes no command from outside: the script says it reopens its own tabs at launch and how to resume the others from its Projects list, then prints the commands; relay that. Any other app it cannot drive (an IDE terminal, Warp…) gets the commands, grouped by repo. On macOS the first run may ask to let the terminal control Ghostty, iTerm or Terminal (Terminal.app also needs System Events, to press Cmd-T). kitty needs `allow_remote_control yes`. With no terminal it can drive, it prints one command per session.

Each repo gets its own window, its sessions as tabs in it (the git repo of the session's folder, else the folder), so tabs are grouped as in an IDE; `--one-window` puts them all in one. Run by hand in a terminal, the script asks which ones to open (numbers, Enter for all); `--all` skips the question. Sessions started by a program (`claude -p`, the SDK) are left out; the current session and the others still running are skipped.

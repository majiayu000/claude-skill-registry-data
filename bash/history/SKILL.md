---
name: history
description: Search Claude Code conversation history on disk for a given query. Use when the user asks to find something from a previous conversation, check what was discussed before, or recover lost context.
---

# Search Conversation History

Search the Claude Code conversation history JSONL files of every profile for the given query.

## Instructions

1. Find the session files that mention the query. Every profile (`~/.claude`, each `~/.claude-*` directory, symlinked ones included, and `$CLAUDE_CONFIG_DIR`) keeps them in `projects/<project-key>/`, where the project key is the working directory's physical path with every character other than a letter or digit replaced by `-`. For example:
   - `/Users/jakebarnby/Local/spotify_sync` → `-Users-jakebarnby-Local-spotify-sync`
   - `/Users/jakebarnby/Local/.query-train` → `-Users-jakebarnby-Local--query-train`

   Run the block in one Bash call from the project's directory, with `QUERY='<text>'` assigned on the line before it. It prints every matching file in every profile, `subagents/` files included. If it prints nothing, run it again with `ALL_PROJECTS=1` also assigned on that line to search every project; that fallback also covers keys longer than 200 characters, which Claude Code truncates with a hash suffix the block cannot reproduce. Start with `ALL_PROJECTS=1` when the user asks about another project.
   ```bash
   QUERY="${QUERY:?set QUERY to the text to search for}"
   PROJECT_KEY=$(pwd -P | sed 's#[^A-Za-z0-9]#-#g')
   if [ "${ALL_PROJECTS:-0}" = 1 ]; then PROJECT_KEY=''; fi
   {
     find -L "$HOME" -maxdepth 1 \( -name .claude -o -name '.claude-*' \) -type d
     if [ -n "${CLAUDE_CONFIG_DIR:-}" ]; then echo "$CLAUDE_CONFIG_DIR"; fi
   } | while IFS= read -r PROFILE_DIR; do
     if [ -d "$PROFILE_DIR/projects" ]; then (cd "$PROFILE_DIR" && pwd -P); fi
   done | sort -u | while IFS= read -r PROFILE_DIR; do
     SEARCH_DIR="$PROFILE_DIR/projects/$PROJECT_KEY"
     if [ -d "$SEARCH_DIR" ]; then grep -rlF --include='*.jsonl' -- "$QUERY" "$SEARCH_DIR" || true; fi
   done
   ```

2. Group the hits by session: `projects/<project-key>/<session-id>.jsonl` is a main session, and a hit anywhere under `projects/<project-key>/<session-id>/subagents/` belongs to the parent session `<session-id>`. Profiles hold copies of the same session, so keep one hit per session id, the one with the newest mtime (`ls -t` on the printed paths lists them newest first). Its profile is the one to resume in.

3. For each kept file, newest first, print the text around each match, matched literally like the search:
   ```bash
   TEXT='<text>' awk 'i = index($0, ENVIRON["TEXT"]) { print substr($0, i > 200 ? i - 200 : 1, 400 + length(ENVIRON["TEXT"])) }' <file> | head -20
   ```

4. Parse and present results:
   - Show which session file(s) matched
   - Show the relevant conversation context around each match
   - If the query relates to code, try to extract the actual code blocks
   - Summarize findings concisely

5. **For every matching session, output a resume command** for the profile that holds its newest copy:
   - `~/.claude`: `env -u CLAUDE_CONFIG_DIR claude --dangerously-skip-permissions --resume <session-id>`
   - any other profile: its alias when the shell defines one (`claude-work` for `~/.claude-work`; `alias` lists them), otherwise `CLAUDE_CONFIG_DIR=<profile dir> claude`, followed by `--dangerously-skip-permissions --resume <session-id>`

   Claude Code resumes a session only from the directory it ran in, so for a session from another project, prefix the command with `cd <cwd> && `, where `<cwd>` is the `cwd` field of the session's entries.

   For example, if the newest copy of a session from the current project is `~/.claude-work/projects/-Users-jakebarnby-Local-sshoo/8afa50e5.jsonl`, output:
   ```
   claude-work --dangerously-skip-permissions --resume 8afa50e5
   ```

   List these at the end of the output grouped under a "Resume" heading, with a one-line description of what each session was about (infer from the first few lines of the file or from the matched context).

## Arguments

The user's search query is passed as the skill argument. For example:
- `/history dependabot` — search for dependabot-related discussions
- `/history billing UI revert` — search for when billing UI was reverted
- `/history "libs.versions.toml"` — search for dependency version discussions

## Tips

- JSONL files can be very large. Use grep to find matching files first, then read only relevant sections.
- Recent conversations are in newer files (sort by mtime).
- Each JSONL line is a complete JSON message — parse it to extract the actual text content if needed.
- If too many results, prioritize the most recent session files.

---
name: setup
description: Set up a new podcast wiki in the current project (copies the tools, creates wiki/, walks through the Spotify login). Use on /podcast-wiki:setup, or when the user wants to start their own podcast wiki.
---

# Set up a podcast wiki here

The plugin's files are at `${CLAUDE_PLUGIN_ROOT}`. Work in the current project directory. Never overwrite an existing file without asking.

## 0. Offer the demo first

If this folder has no `wiki/` yet, ask once whether the user wants to see a demo before setting up Spotify. `/podcast-wiki:demo` builds a small wiki from 3 sample episodes in about 2 minutes, with no Spotify login. If they say yes, run the demo skill and stop here.

## 1. Check requirements

Run `uname -sm; uv --version; ffmpeg -version | head -1`. Whisper transcription needs macOS on Apple Silicon (`Darwin arm64`), [uv](https://docs.astral.sh/uv/) and `ffmpeg`. If one is missing, say how to install it (`brew install uv ffmpeg`) and stop. On other platforms, warn that episodes without a published transcript fall back to the episode description.

## 2. Copy the files

```bash
mkdir -p tools raw wiki/{concepts,hubs,episodes,people,shows,takeaways}
cp -n "${CLAUDE_PLUGIN_ROOT}"/tools/{spotify_mcp,fetch_transcript,lint_wiki,dream_replay}.py tools/
cp -n "${CLAUDE_PLUGIN_ROOT}"/{pyproject.toml,uv.lock,.env.example} .
```

- `CLAUDE.md`: if the project has none, copy `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`. If it has one, append the plugin's file under a `# Podcast Wiki` heading.
- `.gitignore`: add whichever of these lines are missing: `.env`, `.spotify_cache`, `.venv/`, `__pycache__/`, `raw/`. `raw/` holds third-party transcripts, so it must stay out of git.
- Create the starting pages if they don't exist:
  - `wiki/index.md`: `# Index`
  - `wiki/log.md`: `# Ingest log`
  - `wiki/takeaways/to-try.md`: `# To try`
  - `wiki/takeaways/recommendations.md`: `# Recommendations`
- `cp -n .env.example .env`

Run `uv run tools/lint_wiki.py --selftest` to confirm the tools work.

## 3. Spotify login

Walk the user through it one step at a time:

1. Create an app at https://developer.spotify.com/dashboard with redirect URI `http://127.0.0.1:8888/callback`.
2. Put its Client ID in `.env` as `SPOTIFY_CLIENT_ID=...`. No client secret is needed, because the login uses PKCE. Let the user paste it into the file themselves.
3. The user runs `! uv run tools/spotify_mcp.py --auth` in the prompt and logs in through the browser.
4. Run `/mcp` and reconnect the plugin's `spotify` server.

## 4. Finish

Tell the user that `/podcast-wiki:ingest-podcasts` fetches the episodes they've finished and builds the wiki. Mention `/podcast-wiki:lint-wiki` and `/podcast-wiki:dream`. The wiki is plain Markdown, so `wiki/` opens as an Obsidian vault.

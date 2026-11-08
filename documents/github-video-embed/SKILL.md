---
name: github-video-embed
description: Make a video, screen recording or demo clip play inline inside a GitHub Markdown file, pull request or release. Use when a video must play in the README or a PR, when asked to embed a video or add an inline player, or when a committed video renders blank.
---

## Running in Codex

This is the Codex copy of this skill. Read the rest of it with these translations:

- Agents launched in parallel: spawn each one with `spawn_agent` before waiting on any, then collect the
  results with `wait_agent`. Tell every agent you spawn not to spawn agents of its own. If subagents are
  unavailable, run each lane yourself, one after another.
- "Your default model" and "your strongest model": spawn the agent with an `agent_type` whose role file in
  `~/.codex/agents/` sets `model` and `model_reasoning_effort`. An agent without a role runs on the
  session's model.
- A slash command such as `/name`: mention the skill as `$name`.
- This repository's hooks and `.claude/` paths are for Claude Code only, and nothing here installs a Codex
  hook. A loop runs one pass per invocation, saves its state and reports how to resume.
- `CLAUDE.md`: also read `AGENTS.md`, which is the file Codex loads.

# github-video-embed

The reader should press play inside the same `.md` file, without leaving the page, and anyone with access
to the repository should see the player. GitHub renders an inline `<video>` player **only** for a
GitHub-hosted attachment URL.

## The rule

Put a bare `https://github.com/user-attachments/assets/<uuid>` on its own line in the `.md`. GitHub turns
it into a `<video>` player.

These render blank or get stripped:

- a raw committed-file URL (`.../raw/...`)
- a release asset URL (`releases/download/...`)
- a `<video src="...">` tag pointing at either of them

Committing the `.mp4` under `docs/` is still worth doing as the source of truth, but it is not what the
page shows.

## Getting the attachment URL

The upload needs a signed-in browser session. A personal access token cannot do it: the upload policy
endpoint (`/upload/policies/assets`) answers 422.

1. Export your own signed-in browser session's GitHub cookies, used once for this upload and shredded
   afterwards. Include `_gh_sess`: it is a session cookie held only in browser memory, never in the
   cookie database on disk, so take it from the live browser, not from the profile folder.
2. Start a Chromium browser headless with `--remote-debugging-port` and a temporary `--user-data-dir`, and
   drive it over the DevTools protocol (Node 22 and later have a global `WebSocket`, so no extra package is
   needed).
3. Call `Network.setCookie` for every cookie, keeping its domain, path, secure, httpOnly and sameSite
   values, then navigate to GitHub. Check that `meta[name=user-login]` shows the expected account.
4. Open a classic Markdown editor page: the release notes editor (`/releases/edit/<tag>`), a wiki page, or
   a commit comment. Not `/issues/new`: that page mounts its editor late and exposes no file input
   headless. The release editor has a plain `textarea[name="release[body]"]` and an `input[type=file]`.
5. Call `DOM.setFileInputFiles` with every file on that `input[type=file]`, then poll the textarea until
   the `user-attachments/assets/<uuid>` URLs appear. The upload happens at once. Do not save or submit the
   form: the release stays unchanged, but the file is already uploaded, and in a public repository its URL
   works without signing in. Do not use this for a video that must stay private until a later date.
6. Put each bare URL on its own line in the doc, then commit and push.

There is no bundled uploader; the steps above are the recipe.

## Verify, then scrub

Fetch the rendered page with the same session and count the players:

```bash
curl -s -b "$COOKIE_JAR" "https://github.com/$OWNER/$REPO/blob/$BRANCH/$DOC_PATH" | grep -o '<video' | wc -l
```

The count must equal the number of videos. Then delete the cookie export with `shred -u` (or your
platform's secure delete) and remove the temporary `--user-data-dir`: both hold a live session.

## Alternative

A self-contained HTML page with the videos inlined as `data:` URIs plays anywhere with no upload. It only
reaches the people you send it to, so it does not suit docs that a whole team reads in the repository.

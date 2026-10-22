---
name: xurl
description: >-
  Uses the official xurl CLI for the X (Twitter) API: install, auth, app selection, shortcuts, and raw
  endpoint calls. Use when posting, reading, searching, or automating actions on X through the API
  from the command line.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.1"
license: MIT
---

# xurl

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

## When to Use

- Posting, reading, or searching on X/Twitter via the API
- Managing auth, apps, and API endpoints with the xurl CLI
- Automating social media interactions (likes, reposts, DMs, bookmarks)

Official CLI for the X API. Primary upstream: https://github.com/xdevplatform/xurl

## Install

```bash
# Homebrew
brew install --cask xdevplatform/tap/xurl

# npm
npm install -g @xdevplatform/xurl

# Shell script fallback (prefer Homebrew, npm, or Go above)
installer="$(mktemp)"
curl --proto '=https' --tlsv1.2 -fsSL \
  https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh \
  -o "$installer"
${PAGER:-less} "$installer"  # inspect before execution; stop if unexpected
bash "$installer"
rm -f "$installer"

# Go
go install github.com/xdevplatform/xurl@latest
```

## Safety

- Never read, print, summarize, upload, or paste `~/.xurl` into LLM context.
- Never ask the user to paste client secrets, bearer tokens, or OAuth tokens into chat.
- Never use `--verbose` in agent runs; it can expose auth headers.
- The user must register app credentials manually on their machine outside the agent session.
- Prefer a package manager. Never pipe a remote installer directly into a shell; download and inspect it first.

## Auth

```bash
xurl auth status
xurl auth oauth2

# Multi-app
xurl auth apps list
xurl auth default my-app
xurl --app dev-app /2/users/me
```

Notes:
- `xurl` stores app config and tokens in `~/.xurl`.
- OAuth 2.0 redirect URI should be `http://localhost:8080/callback`.

## Common shortcuts

```bash
xurl post "Hello world!"
xurl reply 1234567890 "Nice post"
xurl quote 1234567890 "My take"
xurl delete 1234567890

xurl read 1234567890
xurl search "from:user" -n 10
xurl whoami
xurl user @XDevelopers
xurl timeline -n 20
xurl mentions -n 10

xurl like 1234567890
xurl unlike 1234567890
xurl repost 1234567890
xurl unrepost 1234567890

xurl bookmark 1234567890
xurl bookmarks -n 10

xurl follow @handle
xurl unfollow @handle
xurl following -n 20
xurl followers -n 20

xurl dm @handle "message"
xurl dms -n 10

xurl media upload path/to/file.mp4
```

## Raw endpoint mode

```bash
# GET
xurl /2/users/me

# POST JSON
xurl -X POST /2/tweets -d '{"text":"Hello world!"}'

# Headers
xurl -H "Content-Type: application/json" /2/tweets

# Auth type
xurl --auth oauth2 /2/users/me
xurl --auth oauth1 /2/tweets
xurl --auth app /2/users/me

# Streaming
xurl /2/tweets/search/stream
```

## Quick checks

```bash
xurl version
xurl auth status
xurl whoami
```

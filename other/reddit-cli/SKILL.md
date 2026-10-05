---
name: reddit-cli
description: Read Reddit as u/elrocie from the CLI without a browser and without a Reddit app/OAuth — a specific post with its comments, the home feed, or any subreddit. Auth is the full logged-in browser cookie; transport is curl_cffi with Chrome TLS impersonation against www.reddit.com's .json. Output is optimized for LLM consumption (compact text + stable --json). Use whenever the user wants to read, check, browse, or digest Reddit, a Reddit post/thread, their Reddit feed, or a subreddit.
---

# reddit-cli

Consistent, browserless Reddit reading with **no app registration**. Two things make it work
(both are required — this is the hard-won recipe):

1. **Full logged-in cookie** (`reddit_session` + `token_v2` + `loid` + …, ~9 cookies). A lone
   `reddit_session` gets Reddit's "Blocked" page.
2. **curl_cffi with `impersonate="chrome"`** — Reddit blocks non-browser TLS fingerprints
   (plain `urllib`/`curl` → 403/302/SPA HTML). Impersonation defeats that.

With both, `www.reddit.com`'s `.json` endpoints return the real personalized JSON. (Anonymous
`.json` and `old.reddit.com/.json` are dead now — don't use them.)

## Invoke

```
~/.config/reddit-cli/reddit-cli <command> [flags]
```

## Commands

| Command | Purpose |
|---|---|
| `post <ref>` | A post + comment tree. `<ref>` = full URL, `/comments/<id>`, `t3_<id>`, `redd.it/<id>`, or bare id. |
| `feed` | Home feed (subscribed). Default sort `best`. |
| `sub <name>` | A subreddit listing (`r/` prefix optional). |
| `me` | Auth check (whoami + karma). |
| `set-cookie` | Store a cookie / Copy-as-cURL from stdin (parses cookie + User-Agent). |

Global: `--json`. `post`: `--sort {top,confidence,new,controversial,old,qa}`, `--depth N` (4),
`--comments N` (40, by score), `--comment-max N`, `--body-max N`.
`feed`: `--sort {best,hot,new,top,rising,controversial}` (best). `sub`: `--sort {hot,new,top,rising,controversial}` (hot).
Both: `--time` (top/controversial), `--limit N` (25), `--body-max N` (500), `--full`.

## Examples

```
~/.config/reddit-cli/reddit-cli feed --limit 20
~/.config/reddit-cli/reddit-cli sub LocalLLaMA --sort top --time week
~/.config/reddit-cli/reddit-cli post https://www.reddit.com/r/x/comments/abc123/title/
~/.config/reddit-cli/reddit-cli --json feed --limit 40   # for parsing / the digest layer
```

## Output shape

- Listings: `N. [+score·ratio] title (kind) — r/sub · u/author · Nc · age · id=… {flair} [tags]`,
  optional link line, indented selftext excerpt.
- Post: header, `# title`, body, then a score-sorted, depth/count-capped comment tree (indent = depth;
  `u/x(OP)`, `[MOD]` markers). `kind:"more"` stubs are dropped.
- `--json`: normalized dicts (id/fullname/title/author/subreddit/score/upvote_ratio/num_comments/
  created_utc/age/permalink/url/is_self/selftext/selftext_len/domain/flair/over_18/spoiler/stickied;
  `post` adds nested `comments` + `comments_shown`).

## Setup / cookie refresh

The cookie expires eventually; when `me`/`feed` start returning 403, re-capture:

1. reddit.com logged in → DevTools → **Network** → filter **Doc** → `Cmd+R`.
2. Click the top `www.reddit.com` **document** request (must contain `reddit_session`) →
   right-click → **Copy → Copy as cURL**.
3. In a **real terminal** (Terminal.app — Claude's shell has an isolated clipboard, `pbpaste` there
   sees nothing): `pbpaste | ~/.config/reddit-cli/reddit-cli set-cookie`
   — parses the full cookie + matching UA, verifies via `me`, writes config.

Alternative: paste the cURL into `~/.config/reddit-cli/curl.txt` and import it.

## Files

- `~/.claude/skills/reddit-cli/reddit_cli.py` — CLI + importable `RedditClient`, `fetch_post/fetch_feed/fetch_subreddit/fetch_me`.
- `~/.config/reddit-cli/config.json` — `{cookie, user_agent}`, chmod 600.
- `~/.config/reddit-cli/venv/` — venv with **curl_cffi** (required) + browser_cookie3.
- `~/.config/reddit-cli/reddit-cli` — launcher shim.

## Roadmap

Digest layer (planned): build a `RedditClient`, call `fetch_feed`/`fetch_subreddit` (or read `--json`),
summarize per post/subreddit, emit a short brief. Keep the JSON schema stable — it's the contract.

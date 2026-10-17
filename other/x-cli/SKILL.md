---
name: x-cli
description: Read X/Twitter as the logged-in user from the CLI without a browser and without a dev app — a tweet with its replies, the home timeline, a user's tweets (@handle), or a search. Auth is the logged-in cookie (auth_token+ct0) + the public web Bearer; transport is curl_cffi Chrome TLS impersonation against X's internal GraphQL. Output is optimized for LLM consumption (compact text + stable --json). Use whenever the user wants to read, check, browse, or digest X/Twitter, a tweet/thread, their timeline, an account, or a topic search.
---

# x-cli

Consistent, browserless X/Twitter reading with **no dev app**. The recipe:

1. **Logged-in cookie** — `auth_token` + `ct0`. `ct0` is sent as the `x-csrf-token` header; the
   web app's **public Bearer** (constant) is used for `authorization`.
2. **curl_cffi `impersonate="chrome"`** — X blocks non-browser TLS fingerprints.
3. **Internal GraphQL** (`x.com/i/api/graphql`) with **self-healing queryIds**: the per-operation
   ids are scraped from X's JS bundles at runtime and cached by build hash (`queryids.json`), so
   they survive X's deploys. Missing `features` flags are auto-negotiated from X's error messages.

## Invoke

```
~/.config/x-cli/x-cli <command> [flags]
```

## Commands

| Command | Purpose |
|---|---|
| `tweet <ref>` | A tweet + its replies. `<ref>` = URL or tweet id. `--replies N` (40). |
| `home` | Home timeline (For You). `--latest` = Following/chrono. |
| `user <@handle>` | A user's tweets. `--replies` includes replies. |
| `search <query>` | Tweet search. `--product Latest|Top`. |
| `me` | Auth check (whoami). |
| `set-cookie` | Store `auth_token`+`ct0` (or Copy-as-cURL) from stdin. |

Common: `--limit N` (20), `--text-max N` (280, per-tweet truncation), `--full`, `--json`.

## Examples

```
~/.config/x-cli/x-cli home --limit 20
~/.config/x-cli/x-cli user nasa --limit 15
~/.config/x-cli/x-cli search "claude code" --product Latest
~/.config/x-cli/x-cli tweet https://x.com/user/status/1234567890
~/.config/x-cli/x-cli --json home --limit 40   # for the digest layer
```

## Output shape

- Listings: `N. @handle (Name) ✓ · age · ♥likes ↻retweets ↩replies 👁views · id=…`, then text,
  `⤷ quote @x: …`, `media: photo/video`.
- Thread: focal tweet + `--- replies (N) ---`.
- `--json`: normalized dicts (id/author/author_name/verified/text/created_at/age/likes/retweets/
  replies/quotes/bookmarks/views/lang/url/is_retweet/is_quote/quoted/media/conversation_id).

## Setup / cookie refresh

When `me`/`home` start failing (401/expired cookie), re-capture:

1. x.com logged in → DevTools → **Application → Cookies → https://x.com**.
2. Copy the **Value** of `auth_token` and of `ct0`.
3. In a **real terminal** (Claude's shell has an isolated clipboard):
   `printf 'auth_token=<v>; ct0=<v>' | ~/.config/x-cli/x-cli set-cookie`
   (or pipe a full Copy-as-cURL: `pbpaste | ~/.config/x-cli/x-cli set-cookie`).

## Caveats

- **Account safety:** X is aggressive about automation. This is read-only at a gentle pace under
  impersonation, but the risk isn't zero (worst case: a temporary rate-limit/challenge → re-login).
  No writes/likes/follows.
- **search** uses the `GlobalCommunities*PostSearchTimeline` ops (general relevant results). Plain
  `SearchTimeline` is gated behind X's `x-client-transaction-id` (404 without it) — not implemented.
  If X ever gates the post-search ops too, search needs the transaction-id generator added.
- queryIds auto-refresh on X deploys via the build-hash cache; if a call fails with "queryId not
  found", X changed its bundle layout and the resolver needs a tweak.

## Files

- `~/.claude/skills/x-cli/x_cli.py` — CLI + importable `XClient`, `fetch_home/fetch_user_tweets/fetch_search/fetch_tweet/fetch_me`.
- `~/.config/x-cli/config.json` — `{cookie, ct0, bearer, user_agent}`, chmod 600.
- `~/.config/x-cli/queryids.json` — resolved GraphQL queryIds, cached by JS build hash.
- `~/.config/x-cli/venv/` — venv with curl_cffi (required).
- `~/.config/x-cli/x-cli` — launcher shim.

## Roadmap

Digest layer (planned): build an `XClient`, call `fetch_home`/`fetch_user_tweets`/`fetch_search`
(or read `--json`), summarize, emit a brief. Keep the JSON schema stable — it's the contract.
Shares the design with the `reddit-cli` skill.

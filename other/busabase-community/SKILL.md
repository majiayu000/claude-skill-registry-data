---
name: busabase-community
license: MIT
description: Read, answer and post on the Busabase community forum at community.busabase.com through its /api/v1/community REST API. Lists categories and posts, reads a thread with its replies, searches, and publishes posts and replies behind an explicit confirmation. Use when the user invokes $busabase-community or /busabase-community, asks what is happening in the Busabase community, wants an unanswered question triaged or answered, or wants something posted or announced there.
disable-model-invocation: false
allowed-tools: Bash(node:*), Read, Write, Edit, Grep, Glob
user-invocable: true
metadata:
  category: platform
  tags:
    - risk:gated-write
    - surface:busabase
---

# Busabase Community

A zero-dependency CLI over the forum's own REST API: read, post, reply, edit
what you wrote, and upload images. `community.busabase.com` is the source of truth; this
skill keeps no local copy.

```bash
node skills/busabase-community/scripts/community.mjs <command> [--json]
```

## Setup

```bash
printf 'BUSABASE_API_KEY=%s\n' '<key>' >> skills/busabase-community/.env
chmod 600 skills/busabase-community/.env
node skills/busabase-community/scripts/community.mjs whoami
```

Create the key at <https://busabase.com/docs/api-tokens>, signed in with the account you use on the
forum. Values are read in this order, first one wins: an exported variable,
`$BUSABASE_ENV_FILE`, `skills/busabase-community/.env` (gitignored), `~/.busabase/.env`.

| Variable | What it is |
| --- | --- |
| `BUSABASE_API_KEY` | Required. The default account |
| `BUSABASE_API_KEY_<NAME>` | Another account, used with `--as <name>` |
| `BUSABASE_ACCOUNT` | Default account name when `--as` is absent |
| `BUSABASE_COMMUNITY_API_URL` | API origin (default `https://busabase.com`) |
| `BUSABASE_COMMUNITY_URL` | Forum origin for links (default `https://community.busabase.com`) |

`community.busabase.com/api/v1/*` only redirects to `busabase.com`, and `fetch` drops the `Authorization` header on a cross-origin redirect — so the API origin must stay `https://busabase.com`.

If the key is missing, every command prints these instructions. Never ask for
the key in chat, never write it to a tracked file, never print it — `setup`
shows only its length.

## Commands

| Command | What it does |
| --- | --- |
| `setup` | Is it configured, and from which files |
| `accounts [--verify]` | List configured accounts; `--verify` checks each one |
| `whoami` | Verify the key, print the account and the API/forum origins |
| `categories` | Category slugs, kinds and post counts |
| `posts [--category S] [--sort active\|latest\|top] [--unanswered] [--status s1,s2] [--solved] [--q TEXT] [--lang XX] [--limit N] [--offset N]` | List posts |
| `post <slug>` | One post with its replies |
| `new --category S --title T --body B [--lang XX] [--yes]` | Publish a post |
| `reply <postId> --body B [--yes]` | Publish a reply |
| `edit <postId> [--title T] [--body B] [--lang XX] [--yes]` | Edit a post the selected account wrote |
| `edit-reply <replyId> --body B [--yes]` | Edit a reply the selected account wrote |
| `upload <file.png>` | Store an image and print its markdown line |

`--category` takes a slug (run `categories` first). `post` takes a slug;
`reply` and `edit` take the post **id** from `post <slug>`.

## Publishing is immediate

This API has no draft or review state, so the gate is local:

1. `new`, `reply`, `edit` and `edit-reply` without `--yes` print the exact
   payload and send nothing.
2. Show the user that payload verbatim.
3. Re-run with `--yes` only after they approve it, in the same turn.

Read the thread before answering it, post in the thread's language, and publish
the user's wording as given. A write is done only when the command prints the
new id or URL — quote it back.

## Images

An image is a markdown link in the body, not an attachment:

```bash
node scripts/community.mjs upload ./screenshot.png     # → ![](…/attachments/blobs/sha256/….png)
node scripts/community.mjs new --category ask --title "…" --body "…![](…)…" --yes
```

png, jpg, gif or webp, up to 10MB. Identical bytes are stored once and anyone
with the URL can fetch it — do not upload what you would not post.

## Several accounts

```bash
# skills/busabase-community/.env
BUSABASE_API_KEY=...        # default
BUSABASE_API_KEY_ALT=...    # --as alt
```

`--as <name>` works on every command; `BUSABASE_ACCOUNT` sets the default for a
shell. An unknown name is an error, never a fallback to the default. Every
preview and confirmation names the account — say which one was used, and ask
when the user has several and has not said.

## Reference and tests

`references/api.md` is the endpoint contract. Tests are offline (no key, no
network): `npm run test:community`.

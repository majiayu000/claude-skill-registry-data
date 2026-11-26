---
name: knowledgeBase
description: Find and keep context in the knowledge base. `log kb search "<query>"` searches every rule, skill, doc, infra note, Claude memory file, page state, account and agent note by keyword and meaning at once; `log kb remember "<text>"` saves what a session learned; `log kb sync` refreshes it. Use before guessing at how something works, where a login lives, what an account is doing or what an earlier session found, and at the end of a session that learned something new.
---

# knowledgeBase

The knowledge base is one place for everything log-cli knows: the owner's rules,
the skills, the docs, the infra notes, every agent's memory files, the known
page states, the accounts, and the notes agents save. Twenty holds it, Redis
searches it.

## Hard boundaries

- **Never write a secret into it.** No password, token, API key, PIN, cookie,
  proxy URL or private key, in a note or anywhere else. Say where a login
  lives (a file path), never what it is. The scrubber hides what it can
  recognise, but it is a safety net, not permission.
- **Never mention Meta's or Facebook's rules from it** (rule 38).
  `docs/vendors` and the enforcement research are never collected.
- **Rows are never deleted by log-cli.** An article removed from the repo
  stays in Twenty; Redis drops only what Twenty no longer has.

## Where it lives

- **Twenty:** your own Twenty workspace, object `knowledgeArticles`
  (Knowledge base): `name` (title), `key`, `kind`, `body` (Markdown),
  `source`, `tags`, `author`, `contentHash`, `syncedAt`. log-cli reaches it at
  `KB_TWENTY_URL` (`https://<your-twenty-host>`, over a private network such
  as Tailscale). There is no default host. People read and edit it in Twenty's
  own web app.
- **Redis:** `kb-redis` (Redis 8.2.11 with the search module), on the same
  private network at `<your-redis-host>:6380`, index `kbIdx` over
  `kb:chunk:*` hashes (title, text, key, kind, source, a 384-dimension
  vector) and `kb:article:*` (each article's hash and chunk ids).
- **Logins:** `~/.config/listeningkit/twenty-listeningkit-api-key.txt` and
  `~/.config/listeningkit/kb-redis-url.txt` (or `KB_TWENTY_API_KEY`,
  `KB_REDIS_URL`, `KB_TWENTY_URL`).

## Kinds

| Kind | From |
| --- | --- |
| `rule` | each numbered rule in AGENTS.md (`rule:73`) |
| `section` | each other AGENTS.md section (`agents:howWeFixProblems…`) |
| `skill` | `skills/*/SKILL.md` (`skill:inspect`) |
| `doc` | `docs/**/*.md`, the request docs included (`doc:docs/adsPower.md`) |
| `infra` | `docs/infra/*.md` (`doc:docs/infra/server.md`) |
| `memory` | every Claude Code memory file in `~/.claude/projects/*/memory` (`memory:log-cli/cloudflare-access`) |
| `pageState` | `PAGE_STATES` (`pageState:messengerPinCreate`) |
| `account` | log-cli's Twenty socialAccounts, status and setup only (`account:10000000000001`) |
| `note` | `log kb remember`, or written by a person in Twenty |

## Commands

Agents call the MCP tools, never a hand-run `log kb …` (rule 163):

```
kbSearch { query: "why did the tunnel go down" }               best articles, keyword + meaning
kbSearch { query: "messenger pin", kind: "pageState", limit: 3 }
kbShow { key: "rule:73" }                                      one article in full
kbRemember { text: "…", tags: ["infra", "server"] }                 a note, in Twenty and Redis at once
kbSync {}                                                      refresh from every source (Monitor it, rule 26)
kbSync { noAccounts: true }                                    without reading log-cli's Twenty
```

In a terminal the same commands are `log kb search|show|remember|sync`. What
each one must do is in the spec, [Knowledge base](../../docs/specs/knowledgeBase.md).

## How a sync works

1. Collect every source (about 600 articles, under a second), scrubbing
   secrets from each body.
2. Read what Twenty holds, compare each article's content hash, then create
   the new ones in batches of 60 and update the changed ones one by one.
   Twenty allows 100 API requests a minute; a 429 waits a minute and
   retries, so a first sync takes a few minutes and later ones seconds.
3. Index into Redis every article whose hash differs from what Redis holds,
   including the ones a person wrote or edited in Twenty, in chunks of about
   1,200 characters embedded with all-MiniLM-L6-v2 on this machine; drop
   from Redis what Twenty no longer has.

## When a session learns something

Save it before the session ends, in one or two plain sentences with where it
came from:

```
kbRemember { text: "Twenty v2.49 signs API keys with a key encrypted by ENCRYPTION_KEY; a changed ENCRYPTION_KEY gives 'No encryption key matches keyId'. Fixed 2026-10-27 by restoring the Oct 21 secrets.", title: "Twenty API keys need the original ENCRYPTION_KEY", tags: ["twenty", "server"] }
```

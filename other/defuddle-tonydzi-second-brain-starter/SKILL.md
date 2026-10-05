---
name: defuddle
description: >-
  Turn an article URL into a clean, vault-ready markdown note with the defuddle CLI, stripping
  ads, navigation and comments and cutting 40-60% of tokens versus a raw fetch. Prefer it over a
  raw web fetch whenever the task is reading or ingesting a normal web article. Triggers:
  "/defuddle <url>", "clean import this page".
license: MIT
---

# /defuddle — clean web→markdown

The `defuddle` CLI (by kepano, MIT, v0.19.1) is installed globally via npm. Node is the only dependency.

## Commands
```bash
# article → clean markdown on stdout
defuddle parse <url> --markdown

# with frontmatter (title/author/published/domain) — for the vault
defuddle parse <url> --markdown --frontmatter

# straight to a file
defuddle parse <url> --markdown --frontmatter --output "<path>.md"
```

## The "article into the vault" flow
1. `defuddle parse <url> --markdown --frontmatter` → draft.
2. Then the standard ingest: a vault note (provenance `origin: external`!), reindex, ≥1 inbound link (rules `always-archive-artifacts-to-vault`, `no-orphan-notes-rule`).

## ⚠️ Gotchas (verified by a live /tt run, 2026-07-04)
- **exit code = 0 even on failure** ("Error: fetch failed" is printed, but the code says success). In scripts, check stdout for `^Error:`, NOT the exit code.
- Empty input → a cryptic destructure error (also exit 0).
- The CLI is machine-local: on another machine run `npm install -g defuddle` first (node required). The skill syncs across the cluster; the binary does not.

## When NOT to use defuddle
A `.md` URL → fetch it directly; JS-heavy SPAs, paywalls, logins → a regular web fetch or live-browser automation.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

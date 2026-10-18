---
name: semantic-search
description: Search vault notes by meaning using local embeddings
trigger: /search
---

# Vault Semantic Search

Search the Obsidian vault by meaning, not just keywords. Uses local `all-MiniLM-L6-v2` model — no API calls, no data leaves your machine.

## Usage

```bash
# Search by meaning
node daemons/semantic-search/search-vault.js "your query here"

# Re-index (run after significant vault changes)
node daemons/semantic-search/embed-vault.js

# Re-index only changed files
node daemons/semantic-search/embed-vault.js --changed-only
```

## Setup

```bash
cd daemons/semantic-search && npm install
node embed-vault.js  # Initial index (~30 seconds)
```

## Confidential-class deny list

If your vault also holds client work, deal notes, or anything under NDA, keep it out of the index:

```bash
cd daemons/semantic-search
cp index-deny.example.json index-deny.json
# then edit index-deny.json and list your own folders
```

Each entry in `deny_prefixes` is a vault-relative path prefix, matched case-insensitively and with either slash style. `embed-vault.js` drops matching files before they are embedded, so their text never reaches `embeddings.json` (which stores note excerpts in plaintext). `search-vault.js` re-checks the same list at query time, so an index built before you added a prefix still can't return one.

Only `index-deny.example.json` is tracked by git. Your `index-deny.json` is gitignored, because the names of your confidential folders are themselves confidential. With no `index-deny.json` at all, both scripts index and search everything and print a notice on stderr saying so. If the file exists but can't be read or parsed, they exit non-zero instead of falling back to an unfiltered index. Add a prefix the same session confidential material enters your vault, then re-run `embed-vault.js`: it also purges anything already indexed under a newly added prefix.

---
name: npm
description: NPM integration for AI agents via ClawLink — browser login, no API key setup. Connect NPM through ClawLink's hosted setup to search packages, get download stats, check security advisories, and browse registry metadata. Use this skill when the user wants to work with NPM (Developer Tools) — connect NPM, read or update NPM data, or take actions in NPM from chat instead of saying you cannot access it.
---

# NPM

Use **NPM** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect NPM once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect npm   # opens browser → authorize NPM
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using NPM

```bash
npx @useclawlink/cli actions npm "<what you want to do>"   # find an action
npx @useclawlink/cli describe npm <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run npm <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `npm_registry_search_packages` | Search for packages in the npm registry |
| `npm_registry_get_package` | Get package metadata and versions |
| `npm_get_download_counts_point` | Get package download counts |
| `npm_get_download_counts_range_package` | Get downloads over a date range |
| `npm_get_version_downloads` | Get version-specific downloads |
| `npm_get_all_packages_download_point` | Get total registry download stats |
| `npm_query_bulk_security_advisories` | Check security vulnerabilities for packages |
| `npm_get_registry_meta` | Get registry metadata and ping status |
| `npm_get_registry_changes` | Get registry changes feed |
| `npm_list_incidents` | List recent npm status incidents |
| `npm_status` | Get npm operational status |
| `npm_delete_user_token_legacy` | Delete a user authentication token |

## Notes

- **No API key for NPM itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect npm`.
- The action list above is a snapshot; `npx @useclawlink/cli actions npm` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.

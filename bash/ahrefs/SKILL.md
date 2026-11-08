---
name: ahrefs
description: Ahrefs integration for AI agents via ClawLink — browser login, no API key setup. Connect Ahrefs through ClawLink's hosted setup to analyze backlinks, research keywords, explore organic competitors, check site health, and track rankings. Use this skill when the user wants to work with Ahrefs (Data & Analytics) — connect Ahrefs, read or update Ahrefs data, or take actions in Ahrefs from chat instead of saying you cannot access it.
---

# Ahrefs

Use **Ahrefs** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Ahrefs once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect ahrefs   # opens browser → authorize Ahrefs
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Ahrefs

```bash
npx @useclawlink/cli actions ahrefs "<what you want to do>"   # find an action
npx @useclawlink/cli describe ahrefs <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run ahrefs <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `ahrefs_domain_rating_for_site_explorer` | Get domain rating from Ahrefs |
| `ahrefs_explore_keywords_overview` | Get keyword overview from Ahrefs |
| `ahrefs_explore_keyword_volume_by_country` | Explore keyword volume by country |
| `ahrefs_explore_matching_terms_for_keywords` | Find matching terms for a keyword |
| `ahrefs_fetch_all_backlinks` | List all backlinks from Ahrefs |
| `ahrefs_fetch_broken_backlinks_data` | List broken backlinks from Ahrefs |
| `ahrefs_fetch_competitors_overview` | Get organic competitors overview |
| `ahrefs_retrieve_organic_keywords` | List organic keywords for a domain |
| `ahrefs_retrieve_organic_competitors` | List organic competitors for a domain |
| `ahrefs_fetch_site_explorer_referring_domains` | List referring domains from Ahrefs |
| `ahrefs_get_serp_overview` | Get SERP overview from Ahrefs |
| `ahrefs_pages_by_traffic_overview` | Get pages by traffic overview |
| `ahrefs_backlinks_stats_retrieval` | Get backlink statistics |
| `ahrefs_get_site_audit_projects` | List Ahrefs site audit projects |
| `ahrefs_fetch_rank_tracker_overview` | Get rank tracker overview |

## Notes

- **No API key for Ahrefs itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect ahrefs`.
- The action list above is a snapshot; `npx @useclawlink/cli actions ahrefs` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.

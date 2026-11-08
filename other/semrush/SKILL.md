---
name: semrush
description: Semrush integration for AI agents via ClawLink — browser login, no API key setup. Connect Semrush through ClawLink's hosted setup to research keywords, analyze backlinks, audit sites, compare domains, and explore organic and paid search data. Use this skill when the user wants to work with Semrush (Data & Analytics) — connect Semrush, read or update Semrush data, or take actions in Semrush from chat instead of saying you cannot access it.
---

# Semrush

Use **Semrush** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Semrush once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect semrush   # opens browser → authorize Semrush
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Semrush

```bash
npx @useclawlink/cli actions semrush "<what you want to do>"   # find an action
npx @useclawlink/cli describe semrush <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run semrush <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `semrush_keyword_overview_one_database` | Get keyword overview for a specific database |
| `semrush_keyword_difficulty` | Check keyword difficulty in Semrush |
| `semrush_competitors_in_organic_search` | Find organic search competitors |
| `semrush_domain_organic_search_keywords` | List organic search keywords for a domain |
| `semrush_domain_organic_pages` | List organic pages for a domain |
| `semrush_backlinks_overview` | Get backlink overview for a domain |
| `semrush_backlinks` | List backlinks for a domain |
| `semrush_domain_vs_domain` | Compare two domains in Semrush |
| `semrush_authority_score_profile` | Get authority score for a domain |
| `semrush_batch_keyword_overview` | Get keyword overview for multiple keywords |
| `semrush_organic_results` | Get organic search results for a keyword |
| `semrush_phrase_questions` | Find questions related to a keyword |
| `semrush_broad_match_keyword` | Find broad match keywords |
| `semrush_historical_data` | Get historical keyword data from Semrush |
| `semrush_account_units_balance` | Check Semrush account units balance |

## Notes

- **No API key for Semrush itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect semrush`.
- The action list above is a snapshot; `npx @useclawlink/cli actions semrush` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.

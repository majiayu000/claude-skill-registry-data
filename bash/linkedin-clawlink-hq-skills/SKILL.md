---
name: linkedin
description: LinkedIn integration for AI agents via ClawLink — browser login, no API key setup. Connect LinkedIn through ClawLink's hosted setup to post on your profile, comment, read profiles, look up organizations, and manage page stats. Use this skill when the user wants to work with LinkedIn (Social Media) — connect LinkedIn, read or update LinkedIn data, or take actions in LinkedIn from chat instead of saying you cannot access it.
---

# LinkedIn

Use **LinkedIn** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect LinkedIn once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect linkedin   # opens browser → authorize LinkedIn
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using LinkedIn

```bash
npx @useclawlink/cli actions linkedin "<what you want to do>"   # find an action
npx @useclawlink/cli describe linkedin <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run linkedin <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `linkedin_get_my_info` | Get the authenticated LinkedIn member profile |
| `linkedin_get_person` | Get a LinkedIn member profile by id |
| `linkedin_get_network_size` | Get the authenticated member's network size |
| `linkedin_get_company_info` | Get a LinkedIn company page info |
| `linkedin_get_org_page_stats` | Get LinkedIn organization page statistics |
| `linkedin_get_share_stats` | Get statistics for a LinkedIn share |
| `linkedin_get_post_content` | Get the content of a LinkedIn post |
| `linkedin_list_reactions` | List reactions on a LinkedIn post |
| `linkedin_get_images` | Get images from a LinkedIn post |
| `linkedin_get_videos` | Get videos from a LinkedIn post |
| `linkedin_search_ad_targeting_entities` | Search LinkedIn ad targeting entities |
| `linkedin_get_ad_targeting_facets` | Get LinkedIn ad targeting facets |
| `linkedin_get_audience_counts` | Get LinkedIn audience counts |
| `linkedin_create_linked_in_post` | Publish a post on LinkedIn |
| `linkedin_create_comment_on_post` | Comment on a LinkedIn post |
| `linkedin_delete_linked_in_post` | Delete a LinkedIn post |

## Notes

- **No API key for LinkedIn itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect linkedin`.
- The action list above is a snapshot; `npx @useclawlink/cli actions linkedin` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.

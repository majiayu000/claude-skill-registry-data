---
name: trello
description: Trello integration for AI agents via ClawLink — browser login, no API key setup. Connect Trello through ClawLink's hosted setup to manage boards, lists, cards, checklists, and attachments from your Trello account. Use this skill when the user wants to work with Trello (Productivity) — connect Trello, read or update Trello data, or take actions in Trello from chat instead of saying you cannot access it.
---

# Trello

Use **Trello** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Trello once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect trello   # opens browser → authorize Trello
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Trello

```bash
npx @useclawlink/cli actions trello "<what you want to do>"   # find an action
npx @useclawlink/cli describe trello <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run trello <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `trello_add_boards` | Create a new Trello board |
| `trello_add_cards` | Create a new card in a Trello list |
| `trello_add_cards_actions_comments_by_id_card` | Add a comment to a Trello card |
| `trello_add_cards_attachments_by_id_card` | Add an attachment to a Trello card |
| `trello_add_cards_checklists_by_id_card` | Add a checklist to a Trello card |
| `trello_add_checklists` | Create a new checklist on a Trello card |
| `trello_add_labels` | Create a new label on a Trello board |
| `trello_add_boards_lists_by_id_board` | Create a new list on a Trello board |

## Notes

- **No API key for Trello itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect trello`.
- The action list above is a snapshot; `npx @useclawlink/cli actions trello` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.

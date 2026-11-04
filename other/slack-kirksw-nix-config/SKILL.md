---
name: slack
description: Use Slack MCPorter CLI to search, read, triage, and summarize conversations or perform explicitly confirmed Slack actions.
---

# Slack

Run the generated `slack` CLI through Context Mode and its bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/slack/scripts/run.mjs" slack-search-messages --help
node "$PI_CODING_AGENT_DIR/skills/slack/scripts/run.mjs" slack-get-thread --help
node "$PI_CODING_AGENT_DIR/skills/slack/scripts/run.mjs" slack-catch-me-up --help
```

Constrain searches by channel, participant, topic, and time range before expanding a thread or conversation.
Resolve users and channels only as needed, and do not expose unrelated private-message content.
Treat send, reaction, mark, refresh, triage, and workflow-save commands as mutations.
After confirmation of the exact action, set `MCP_WRITE_CONFIRMED=1` only for that runner process.

Refresh this generated wrapper with `nix run .#update-mcp-skills -- slack`, then run `nix run .#sync-agents`.

---
name: hermes-tweet
description: >
  Use Hermes Tweet with Hermes Agent for X/Twitter endpoint discovery, public
  reads, private action-gated reads, audience analysis, thread planning, and guarded publishing.
  Use when a project needs Hermes-native social research or publishing workflows.
---

# Hermes Tweet

Hermes Tweet is a Hermes Agent plugin for X/Twitter workflows. It keeps endpoint
discovery separate from reads and requires explicit configuration before account
data or publishing actions are available.

## Install

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Set `XQUIK_API_KEY` before using read or action tools. Set
`HERMES_TWEET_ENABLE_ACTIONS=true` only for projects where publishing actions
are intentionally enabled.

## Tool Routes

- `tweet_explore`: discover the bundled X/Twitter endpoint catalog without
  network access.
- `tweet_read`: read public, read-only X/Twitter data from a cataloged GET
  endpoint when `XQUIK_API_KEY` is configured.
- `tweet_action`: run private or action-marked GET endpoints, draft, schedule,
  or publish only when `XQUIK_API_KEY` is configured and
  `HERMES_TWEET_ENABLE_ACTIONS=true`.

## Workflow

1. Use `tweet_explore` to find the endpoint that matches the user's request.
2. Use `tweet_read` for public timelines, profile reads, search, or analytics.
3. Use `tweet_action` for connected-account state, private GET endpoints,
   action-marked endpoints, or publishing after clear user approval.
4. Report what was read or drafted without exposing private account state.

## Safety

- Keep all publishing actions explicit and reviewable.
- Treat private account state as sensitive context.
- Do not enable `tweet_action` for unattended projects.
- Do not store API keys, account data, or drafts in the repository.

## Links

- Plugin: https://github.com/Xquik-dev/hermes-tweet
- Hermes Agent: https://github.com/NousResearch/hermes-agent

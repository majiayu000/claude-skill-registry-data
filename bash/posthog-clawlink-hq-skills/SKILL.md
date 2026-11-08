---
name: posthog
description: PostHog integration for AI agents via ClawLink — browser login, no API key setup. Connect PostHog through ClawLink's hosted setup to manage feature flags, experiments, insights, cohorts, events, dashboards, session recordings, and surveys from your PostHog organization. Use this skill when the user wants to work with PostHog (Data & Analytics) — connect PostHog, read or update PostHog data, or take actions in PostHog from chat instead of saying you cannot access it.
---

# PostHog

Use **PostHog** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect PostHog once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect posthog   # opens browser → authorize PostHog
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using PostHog

```bash
npx @useclawlink/cli actions posthog "<what you want to do>"   # find an action
npx @useclawlink/cli describe posthog <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run posthog <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `posthog_list_organization_projects` | List all projects in your PostHog organization |
| `posthog_list_organization_members` | List members of your PostHog organization |
| `posthog_list_project_dashboards` | List dashboards in a PostHog project |
| `posthog_list_and_manage_project_feature_flags` | List feature flags in a PostHog project |
| `posthog_get_feature_flag_details` | Get details for a specific feature flag |
| `posthog_get_feature_flag_status` | Get the status of a feature flag |
| `posthog_list_project_experiments` | List A/B experiments in a PostHog project |
| `posthog_get_experiment_details` | Get details for a specific experiment |
| `posthog_get_experiments_stats` | Get statistics for experiments |
| `posthog_list_project_surveys` | List surveys in a PostHog project |
| `posthog_list_project_session_recordings` | List session recordings in a PostHog project |
| `posthog_list_or_delete_persons_with_optional_filters` | List persons in a PostHog project with optional filters |
| `posthog_get_event_definitions` | List event definitions in a PostHog project |
| `posthog_get_project_person_trends` | Get person trends for a PostHog project |
| `posthog_get_funnel_insights_in_project` | Get funnel insights in a PostHog project |
| `posthog_list_project_actions` | List actions in a PostHog project |
| `posthog_list_groups_by_type` | List groups by type in a PostHog project |
| `posthog_get_group_property_definitions` | Get group property definitions |

## Notes

- **No API key for PostHog itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect posthog`.
- The action list above is a snapshot; `npx @useclawlink/cli actions posthog` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.

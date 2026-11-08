---
name: strava
description: Strava integration for AI agents via ClawLink — browser login, no API key setup. Connect Strava through ClawLink's hosted setup to track workouts, list activities, explore routes and segments, and manage club data. Use this skill when the user wants to work with Strava (Health & Fitness) — connect Strava, read or update Strava data, or take actions in Strava from chat instead of saying you cannot access it.
---

# Strava

Use **Strava** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Strava once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect strava   # opens browser → authorize Strava
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Strava

```bash
npx @useclawlink/cli actions strava "<what you want to do>"   # find an action
npx @useclawlink/cli describe strava <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run strava <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `strava_list_athlete_activities` | List authenticated athlete's activities |
| `strava_get_activity` | Get activity details by ID |
| `strava_create_an_activity` | Create a manual activity |
| `strava_get_activity_streams` | Get activity time-series data |
| `strava_get_activity_zones` | Get heart rate and power zones |
| `strava_get_authenticated_athlete` | Get authenticated athlete profile |
| `strava_get_athlete_stats` | Get athlete activity stats |
| `strava_list_athlete_clubs` | List athlete's clubs |
| `strava_get_club` | Get club details |
| `strava_list_club_activities` | List club activities |
| `strava_list_athlete_routes` | List athlete's routes |
| `strava_get_route` | Get route details |
| `strava_explore_segments` | Explore segments in an area |
| `strava_get_segment` | Get segment details |
| `strava_upload_activity` | Upload an activity file |
| `strava_list_activity_laps` | List activity laps |

## Notes

- **No API key for Strava itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect strava`.
- The action list above is a snapshot; `npx @useclawlink/cli actions strava` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.

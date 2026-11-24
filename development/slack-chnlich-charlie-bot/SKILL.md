---
name: slack
description: Use when the user asks to read Slack messages, search Slack conversations, look up Slack users, check DMs, or interact with the Slack workspace.
version: 1.0.0
---

# Slack

Read messages, search conversations, and look up users in the configured Slack workspace using the Slack Web API.

## Configuration

- Token location: `$CHARLIEBOT_HOME/credentials.yaml` under `slack.user_token` and `slack.bot_token`
- Token type: User OAuth Token (`xoxp-`)
- Available scopes on `slack.user_token`, as the Web API reads them back: `identify`, `channels:history`, `channels:read`, `chat:write`, `groups:history`, `groups:read`, `im:history`, `im:read`, `im:write`, `mpim:history`, `mpim:read`, `mpim:write`, `search:read`, `users:read`, `files:read`
- Requests: send every Slack Web API call through `charliebot slack request`. The command reads the token from `credentials.yaml` inside its own process, so no token appears in a command, an output or a run record.
- Files: download a message file through `charliebot slack download`.

- CharlieBot runtime calls use app credentials.
- `charliebot slack request` admits only read methods with `slack.user_token`.
- `charliebot slack download` admits a GET of a file on Slack's file host, for either token kind.
- Post with `slack.bot_token`.
- `slack.bot_token` carries `files:write` and not `files:read`.
- A message in Chao's name goes through `charliebot slack draft`.

## API Reference

Send every request through `charliebot slack request <METHOD> <URL>`:

```bash
charliebot slack request GET 'https://slack.com/api/auth.test'
charliebot slack request GET 'https://slack.com/api/conversations.list?types=im&limit=200'
```

The command adds the bearer header itself and prints the 2xx response body. It uses `slack.user_token` by default; pass `--token bot` to use `slack.bot_token` for a post. Pass a request body from a file with `--data-file <path>`, and add any other header with `--header 'NAME:VALUE'`.

| Exit code | Meaning |
|---|---|
| 0 | A 2xx response whose `ok` is not `false`. |
| 1 | Another status, `"ok": false`, a network failure, or a download answer that is not the file. |
| 2 | Invalid arguments. |
| 3 | `credentials.yaml` is unreadable or the chosen `slack` key is missing. |

Pipe the response body to `jq` when you need one field.

### Authentication

```
GET https://slack.com/api/auth.test
```

### Users

```
GET https://slack.com/api/users.list?limit=200
```

To find a user, match against `real_name`, `name`, and `profile.display_name` fields (case-insensitive).

### Channels

```
GET https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=200
```

### Direct Messages

List all DM conversations:
```
GET https://slack.com/api/conversations.list?types=im&limit=200
```

Each DM channel has a `user` field — match it against the target user's ID to find the right channel.

### Read Messages

```
GET https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=50
```

A `conversations.replies` response carries a `role` on each message: `operator`, `colleague` or `other`, by the sender's listing in the server's Slack config.

Use `oldest` and `latest` (Unix timestamps) to filter by date range. Use `cursor` for pagination.

### Read Threads

```
GET https://slack.com/api/conversations.replies?channel=CHANNEL_ID&ts=THREAD_TS
```

### Search Messages

```
GET https://slack.com/api/search.messages?query=QUERY
```

Supports Slack search modifiers: `from:username`, `in:#channel`, `before:2026-01-01`, `after:2026-01-01`, `has:link`, etc.

Search returns at most 100 messages per page: `count` defaults to 20 and accepts up to 100.
To read the whole time window, send the same `query` with `count=100`, then request each next page by raising `page` by one, starting from 1, until `page` reaches `pagination.page_count` in the response.

Source: Slack API method reference, `search.messages` (https://docs.slack.dev/reference/methods/search.messages).

### Download a File

A message's `files[]` entry carries the file URL in `url_private` or `url_private_download`. Pass that URL and the output path:

```bash
charliebot slack download '<url_private>' --output <path>
```

The command admits only Slack's file host. It uses `slack.user_token` by default, which carries `files:read`; `slack.bot_token` needs that scope before it can download. When the token lacks `files:read`, or cannot see the file, Slack answers with a sign-in page or a redirect: the command exits 1, writes no file, and names the missing scope.

## Important Workarounds

- List DM conversations with `conversations.list?types=im` and find the channel by user ID (conversations.open requires `im:write` scope).

- Resolve a private channel by ID because channel listings can omit it while its history remains readable.
- The bot-token listing shows exactly which private channels allow posting; public channels accept posts without bot membership.

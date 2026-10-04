---
name: onboard
description: Set up internbot for development. Use when setting up the project for the first time.
---

# Internbot Developer Setup

## Prerequisites

- Node.js >= 20
- A Slack workspace where you can create apps

## Steps

### 1. Create a Slack App

1. Go to https://api.slack.com/apps → Create New App → From scratch
2. Name it (e.g., "internbot"), select your workspace
3. Enable **Socket Mode** under Settings → Socket Mode → toggle on
   - Generate an app-level token with `connections:write` scope → save as `SLACK_APP_TOKEN`
4. Under **OAuth & Permissions**, add these Bot Token Scopes:
   - `app_mentions:read`
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `groups:history`
   - `groups:read`
   - `im:history`
   - `im:read`
   - `im:write`
   - `mpim:history`
   - `mpim:read`
   - `users:read`
   - `reactions:write`
5. Under **Event Subscriptions** → toggle on → Subscribe to bot events:
   - `message.channels`
   - `message.groups`
   - `message.im`
   - `message.mpim`
   - `app_mention`
6. Install the app to your workspace → copy the Bot User OAuth Token as `SLACK_BOT_TOKEN`

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your tokens:
#   SLACK_BOT_TOKEN=xoxb-...
#   SLACK_APP_TOKEN=xapp-...
```

### 3. Set Up Reports Repository

The bot publishes LaTeX reports to a separate GitHub repo. Set it up as a subdirectory:

```bash
mkdir reports-repo && cd reports-repo
git init
mkdir reports
echo '[]' > papers-log.json
git add . && git commit -m "init reports repo"
```

Create a GitHub repo for reports, then configure the remote with a dedicated account (optional):

```bash
git remote add origin https://<github-user>@github.com/<github-user>/<repo-name>.git
git config user.name "<bot-name>"
git config user.email "<github-user>@users.noreply.github.com"
git push -u origin main
```

If using a dedicated GitHub account, store its PAT locally:

```bash
echo "https://<github-user>:<PAT>@github.com" > .git/credentials
git config credential.helper 'store --file=.git/credentials'
```

### 4. Install & Run

```bash
npm install
npm run dev    # Development with hot reload
npm run build  # Compile TypeScript
npm start      # Run compiled version
```

### 5. Test

- DM the bot "hi" → should get a simple reply
- In a channel, @mention the bot with a question → should get a threaded response
- Ask it to search for papers → should use arxiv tools

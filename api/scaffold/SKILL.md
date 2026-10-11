---
name: scaffold
description: 'Scaffold a new Microsoft Teams bot, Graph bot or tab on Teams SDK 2.1 with the Teams Developer CLI 3 Arguments: <project-name> [echo|graph|tab].'
---

# /teams-dev:scaffold

Creates a new Microsoft Teams project in the current directory with `@microsoft/teams.cli` 3.x. Arguments:

- `$1` — project name (required), for example `quote-agent`; the CLI turns it into a package name.
- `$2` — template (optional, default `echo`). The CLI 3.0 ships `echo`, `graph` and `tab` for TypeScript.

## Steps

1. Check the toolchain. Node must be 22.12 or newer; the CLI must be installed:

   ```bash
   node --version
   teams --version
   ```

   If `teams` is missing, install it with `npm install -g @microsoft/teams.cli` (no dist-tag; `latest` is the stable 3.x line).
2. Check the sign-in with `teams status --json`. If the user is not logged in, **stop and ask them to run `teams login` themselves**; never run the sign-in on their behalf. Registration (step 5) needs it, scaffolding does not.
3. Scaffold. Without a TTY the CLI does not prompt, and `--json` gives machine-readable output:

   ```bash
   teams project new typescript "$1" -t "${2:-echo}" --json
   ```

   If it answers `Unknown template`, run `teams project new typescript --help` and use a template from that list.
4. Install dependencies in the new directory:

   ```bash
   cd "$1" && npm install
   ```

5. Tell the user what comes next, and invoke the skill that owns each step:
   - **Test without registering anything:** the Agents Playground — `Skill: agents-playground`. It needs the local-only opt-in `DANGEROUSLY_ALLOW_UNAUTHENTICATED_REQUESTS=true`; never put it in a committed file.
   - **Register the bot, get credentials, set up a tunnel:** the official walkthrough — `Skill: teams-sdk-teams-dev` → `references/guide-create-bot-infra.md` (`teams app create --name … --endpoint https://<tunnel-host>/api/messages --env .env`).
   - **Write code:** `/teams-dev:add-feature`, or the skills `messaging`, `adaptive-cards`, `ai-agents`.

## Notes

- `echo` is a message-echo bot with `new App()` and no plugins; pick it unless the user asked otherwise.
- `graph` signs the user in and calls Microsoft Graph. It needs an Azure-managed bot with an OAuth connection (`Skill: authentication`) and is written in the SDK 2.0 style; offer to rewrite it to `addOAuthFlow`.
- `tab` is a bot plus a Vite/React tab with `@microsoft/teams.client` and an `app.function()` (`Skill: tabs`).
- There is no AI, MCP or A2A template. Scaffold `echo` and add the feature with `/teams-dev:add-feature ai`.
- Credentials land in `.env`. Do not commit it, and do not paste real client ids, secrets or tenant ids into files that are committed.
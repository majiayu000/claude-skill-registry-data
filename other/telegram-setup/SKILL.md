---
name: telegram-setup
description: Help a user set up Telegram for Dojo Dojo. Default to Personal private bots (recommended). Group setup is advanced for teams/observers/demos.
version: 3.0.0
category: guides
tags: telegram, bot, setup, dojo, notifications, chatops, voice, remote, personal, pairing
---

# Telegram Setup for Dojo Dojo

This skill is your playbook when a user asks Dojo to set up Telegram on their machine and you cannot see the project source. Walk them through the **Personal bots** flow first — it is the recommended product path. Only fall back to **Group setup** if they explicitly want shared/team visibility.

## Mental model (read first)

Dojo Engine has **two Telegram flavors**. Only one is active at a time:

| Flavor                      | When to use                                | Listens to                                       | Sends to                 |
| --------------------------- | ------------------------------------------ | ------------------------------------------------ | ------------------------ |
| **Personal bots** (default) | A single user, private 1:1 chats           | Their paired private Telegram chat per Dojo lane | Same paired private chat |
| **Group setup** (advanced)  | Teams, observers, demos, shared visibility | Configured Telegram group chat IDs               | Same groups              |

Hard rules to enforce in your guidance:

- The user selects exactly one flavor in `Settings → Remote Access & Notifications → Telegram`. The other flavor’s saved keys stay on disk but are dormant.
- The top `Enabled` switch is the master kill switch for Telegram.
- Personal mode pairs each Dojo lane (Primary, Secondary) to its own private Telegram bot. Each lane is independent — they can configure just Primary, just Secondary, or both.
- Group mode reuses one bot in two Telegram groups, with chat IDs.
- Dojo doesn’t care which flavor feeds it. It routes by Primary/Secondary role.
- PIN and wake-word features were removed from the product. Do not ask the user about them.

If you ever see PIN/wake-word in screenshots or older docs, treat them as out-of-date and skip.

---

## Personal bots (recommended flow)

### Per-lane outcome

After setup, each lane the user configures will have:

- one Telegram bot they created via BotFather
- the bot **paired** to their personal Telegram account via a one-time `/dojo:pair <code>` message
- Dojo accepting inbound only from that paired private chat, and sending outbound to that same paired chat

No groups. No admin rights. No privacy-mode toggles. No chat ID hunting. No `getUpdates`.

### Walk the user through this

For **each lane** the user wants (start with Primary):

1. **Open BotFather**
   - In Telegram, open `@BotFather` (verified blue checkmark).

2. **Create a bot**
   - Send `/newbot`.
   - Display name: anything (e.g. `Dojo Primary` or `Val Dojo`).
   - Username: must end in `_bot` (e.g. `val_dojo_primary_bot`). Try variants if taken.

3. **Copy the bot token**
   - BotFather returns a token like `123456789:ABC...`.
   - Treat it like a password. Do not echo it in chat. Don’t commit it.

4. **Open Dojo Settings**
   - `Dojo Engine → Settings → Remote Access & Notifications → Telegram`.
   - Make sure the `Personal bots` card is selected (it shows the small green checkmark).

5. **Paste the token**
   - Paste into `Primary private bot` (or `Secondary private bot` for the secondary lane).
   - Click `Connect`.

6. **Pair the bot**
   - Dojo shows a pairing dialog with a command like `/dojo:pair 482913`.
   - The dialog has `Open bot in Telegram` and a copy icon.
   - In Telegram, open the new bot and send the exact `/dojo:pair <code>`.
   - Return to Dojo and click `Check pairing`.
   - On success Dojo saves the private chat and shows `Connected to <Name> (@username)` in green.

7. **Save and enable**
   - Make sure the top `Enabled` switch is on.
   - Click `Save`.

8. **Smoke test**
   - In the bot chat send `hey` or any short message.
   - Dojo Primary should respond and Telegram should show a reply.
   - The pairing-only chat is the only chat that can reach Dojo through this bot.

Repeat for Secondary if the user wants it. Skipping Secondary is fine.

### Remote control while on the move

Once a lane is paired, these commands work in that bot chat:

| Type                         | Meaning                          |
| ---------------------------- | -------------------------------- |
| `help` or `1`                | Show help                        |
| `status` or `2`              | Show this lane’s Telegram status |
| `telegram on` or `3`         | Turn this lane’s Telegram ON     |
| `telegram off` or `4`        | Turn this lane’s Telegram OFF    |
| `verbosity brief` or `5`     | Brief replies                    |
| `verbosity talkative` or `6` | Paragraph replies                |
| `verbosity chatty` or `7`    | Detailed replies                 |

`3` / `4` toggle the **per-lane** flag, not the master switch. The master `Enabled` switch in Settings is the only way to disable the whole Telegram integration.

### What you’re telling the user is happening behind the scenes

- Dojo verifies the bot token via Telegram `getMe`.
- Dojo generates a 6-digit pairing code.
- Dojo polls bot updates and looks for a private message from a real Telegram user whose text is exactly `/dojo:pair <code>`.
- It stores `chatId`, `userId`, bot username, and pairedAt.
- Inbound messages are then accepted only when: token matches, chat type is private, chat ID matches, and sender user ID matches.
- Outbound goes to the same paired chat.

---

## Group setup (advanced flow)

Use this only when the user explicitly wants a team/observer/demo experience. It is more work and exposes group access-control decisions to the user.

High level:

- 1 Telegram bot via BotFather (privacy mode disabled).
- 2 Telegram groups (Primary, Secondary), bot added as admin to both.
- Capture each group’s chat ID (negative `-100…`).
- Paste token + chat IDs into the `Group setup` card.

### Walk them through it

1. **Create the bot** — `@BotFather → /newbot`. Copy the token.
2. **Disable privacy mode** — BotFather → `/setprivacy` → select the bot → Disable.
   - If the bot was already in a group, remove and re-add it. Telegram only applies the new privacy setting on re-join.
3. **Create two groups** in Telegram:
   - `Dojo Dojo (P)` for Primary
   - `Dojo Dojo (S)` for Secondary
4. **Add the bot to both groups** and **promote to admin**. Bot needs to read messages and post replies.
5. **Get each chat ID** (negative `-100…`). Two reliable methods:
   - Send a message in the group, then open:
     `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
     Look for `chat.id` and `chat.title` matching the group. Copy the negative number.
   - Or use a chat-ID helper bot the user trusts.
6. **Lock down the groups (optional but recommended)** — restrict who can send messages, especially if it’s a private group meant for one user.
7. **Open Dojo Settings → Telegram**:
   - Select the `Group setup` card.
   - Paste the bot token into `Group Bot Token`.
   - Paste `Primary Chat ID` and `Secondary Chat ID`.
   - Click `Test` next to each chat to verify a message arrives.
8. **Save** and turn the top `Enabled` switch on.

### Group safety guidance

- Private group: discoverable only by invite link. Recommended for solo users using groups.
- Public group: anyone can search/join. Dojo will show a one-time informational notice and continue working — the user is responsible for membership.
- If the user wants the group to be read-only for everyone except themselves and the bot, set group permissions accordingly.

Dojo Engine no longer enforces a PIN or wake-word for Telegram commands. Trust is delegated to Telegram group membership/permissions.

---

## How to choose for the user

Ask: “Are you setting this up for just you, or do you want others to see/use Dojo through Telegram?”

- **Just me** → Personal bots.
- **Team / observers / demos / shared** → Group setup.
- **Both** → Configure Personal for daily use; Group only when they need shared visibility. Only one is active at a time. Saved keys for the other flavor stay on disk and can be flipped back later by switching the card and clicking Save.

---

## Troubleshooting cheat sheet

| Symptom                                           | Likely cause                                                         | Fix                                                                                                                         |
| ------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Pairing never completes                           | Wrong bot opened in Telegram, code mistyped, or code expired         | Click `Connect` again to get a fresh code; ensure the bot username in the dialog matches the bot in Telegram                |
| Pairing succeeds but bot ignores messages         | Lane Telegram is off (`primaryTelegram`/`secondaryTelegram`)         | Send `3` in the bot chat (or `telegram on`); or toggle in Settings                                                          |
| Personal bot suddenly silent                      | Master `Enabled` is off, or mode switched to `Group setup`           | Re-enable master switch; reselect `Personal bots`                                                                           |
| Group bot replies but UI never showed the message | A stale DojoWorkspace process is running from an old install/dev build | Quit `/Applications/DojoWorkspace.app` (and its sidecar) and any older dev backends; only one Telegram process should be live |
| Group setup test message fails                    | Bot is not in the group, not an admin, or wrong chat ID              | Re-add bot as admin, recheck chat ID via `getUpdates`                                                                       |
| Group bot reads `/commands` only                  | Privacy mode is still enabled                                        | BotFather → `/setprivacy` → Disable, then remove and re-add the bot to the group                                            |
| User reports two messages on each reply           | Both Personal and Group were briefly enabled by old code             | Confirm there’s only one DojoWorkspace process; switch mode and save once to settle settings                                  |

If something’s still wrong: look at `temp/dojo/logs/be/dojo-d-be-*.log`. Telegram lines are prefixed `📨 TelegramService`. Confirm there’s only one backend process talking to Telegram.

---

## What you should never tell the user

- Don’t ask them to set a PIN. It was removed.
- Don’t ask them to set a wake word. It was removed.
- Don’t tell them they need both Personal and Group at once.
- Don’t tell them to delete their saved Group token when they switch to Personal — the app keeps both safely; the other flavor just goes dormant.
- Don’t paste their bot token back to them in chat. Have them paste it directly into the Settings field.

---

## Optional: Telegram for Dojo Portal

If a user also wants Portal alerts (separate product from Dojo):

- They can create a separate Telegram bot or reuse one.
- Set `TELEGRAM_BOT_TOKEN` (and recipient chat ID) in Portal env.
- For one-way alerts, privacy mode can stay enabled.
- Disabling privacy mode is only required if Portal also reads replies.

This is independent of the Dojo flavor selected above.

---

## BotFather quick reference

| Command       | Purpose                                     |
| ------------- | ------------------------------------------- |
| `/newbot`     | Create a new bot                            |
| `/mybots`     | List/manage your bots                       |
| `/setprivacy` | Toggle group privacy mode (group flow only) |
| `/setname`    | Rename the bot                              |
| `/setuserpic` | Set bot avatar                              |
| `/revoke`     | Revoke the bot token (issues a new one)     |

If a token leaks: `/revoke` immediately, then paste the new token into the same `Primary private bot` or `Secondary private bot` field and re-pair.

---
name: consent
description: "Use when a step needs a permission the user may have off. Use BEFORE a step that needs a permission the user may have left off — running terminal commands, writing files, browsing or calling online tools, controlling other apps, screenshots, the clipboard, installing packages, creating scheduled tasks, sending email or messages, or spending/trading. Check ICLONE_CONSENT_<KEY>; when it is 0 or ask, ask the user through the app with `acp consent request <key> --reason \"…\"` instead of failing or working around it."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, consent, permissions, privacy, terminal, files, browsing, clipboard, automation, screen, packages, cron, email, spending]
    related_skills: [economyos, iclone-os]
---

# Consent — ask the user before you use what they left off

The user chose, in icloneOS (first launch, then Settings › Privacy), what you may do on this Mac. The app tells you
each choice when your runtime starts, as environment variables:

| Key (`<key>` below) | Variable | Covers |
|---|---|---|
| `terminal` | `ICLONE_CONSENT_TERMINAL` | running shell / terminal commands |
| `fileWriting` | `ICLONE_CONSENT_FILE_WRITING` | creating, changing or deleting files (reading the folders the user chose is fine) |
| `webBrowsing` | `ICLONE_CONSENT_WEB_BROWSING` | browsing the web, web search, calling online tools and APIs |
| `automation` | `ICLONE_CONSENT_AUTOMATION` | controlling other apps (Apple Events, computer use) |
| `screen` | `ICLONE_CONSENT_SCREEN` | screenshots, screen recordings, other apps' window titles |
| `clipboard` | `ICLONE_CONSENT_CLIPBOARD` | reading or writing the clipboard |
| `installSoftware` | `ICLONE_CONSENT_INSTALL_SOFTWARE` | brew / npm / pip / any installer |
| `scheduledTasks` | `ICLONE_CONSENT_SCHEDULED_TASKS` | creating cron / scheduled jobs |
| `sendMessages` | `ICLONE_CONSENT_SEND_MESSAGES` | sending agent email or messages for the user |
| `spendTrade` | `ICLONE_CONSENT_SPEND_TRADE` | moving value: card spending, marketplace jobs, trades, transfers |
| `microphone`, `notifications`, `localNetwork` | `ICLONE_CONSENT_…` | device features the app itself gates |

Values: `1` = allowed · `0` = the user switched it off · `ask` = undecided.

## The rule

1. `1` → go ahead; no need to ask.
2. `0` or `ask` → do NOT use it, do NOT find a workaround (another tool, a script, a different binary). Ask first:

   ```sh
   ~/.iclone-os/bin/acp consent request <key> --reason "<what this task needs it for, in one sentence>"
   ```

   Run it in your terminal like any `acp` call (it carries your iNFT; add `--inft <iNFT>` only if you already use it).
   **The one exception:** `acp consent request|status` is the one terminal command that is always allowed, even when
   `terminal` is `0` or `ask` — it is how you ask. It is the only one: every other command still follows this rule.
   The app shows the user ONE small sheet: "Your agent needs <Permission>", with your reason word for word, and
   **Allow once** / **Allow always** / **Deny**. The command waits for the answer (up to two minutes) and prints one line:

   ```json
   {"allowed":true,"key":"terminal","scope":"once"}
   ```

   Exit code `0` = allowed (`scope` `once` = this app run, `always` = saved), `1` = denied (also: no answer in two
   minutes, or the policy is not accepted yet), `64` = you used it wrong (the usage line is on stderr).
3. Allowed → continue the task. Denied → stop that step, tell the user in one sentence what you could not do and why,
   and offer the alternative that does not need it. Never ask again for the same key in this session after a Deny.
4. `acp consent status [<key>]` prints the live state (`on` / `off` / `ask` / `once`) without a sheet. The environment
   is read when your runtime starts, so after an answer trust the door's reply (or `status`), not the old variable.

## Spend tokens and the user's attention wisely

- Ask only when the very next step needs the capability — not "just in case", not at the start of a conversation.
- One key per request; the reason says what and why ("Run `npm test` in ~/code/app to check your fix"), never a list.
- Never ask twice for the same key in one session. Never ask for `keychain`, `camera`, `location` or `contacts`
  (keychain is a setting in Settings › Gateway; icloneOS never uses the other three).
- A Deny is an answer, not an obstacle: do not rephrase and retry.

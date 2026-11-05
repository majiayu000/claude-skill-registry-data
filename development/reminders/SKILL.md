---
name: reminders
description: Leaves a reminder for the user, shown in a later Claude Code session on this computer or another one, and notifies them on the desktop and on the phone (Claude mobile app through a scheduled task, or ntfy) every morning and at the first session of the day. Use when the user says "remind me", "rappelle-moi", "tomorrow when I open a session, tell me…", "don't let me forget", "list my reminders", "that reminder is done", or when a SessionStart message lists reminders.
---

# Reminders

A reminder is for the user to remember: it never runs anything by itself, and the user always picks it up. Work for Claude to do on another computer, or a task for the user's assistant to run by itself ("ask <assistant> to … at …"), is a handoff: use the handoff skill.

A reminder is one Markdown file in `~/.claude-sync/reminders/` (or `$CLAUDE_REMINDERS_DIR`), the config sync repo, so every computer of the user gets it. Scripts are in this skill's base directory (`~/.claude/skills/reminders/` when installed by install.sh; `$SK` below).

It needs the sync engine (`~/.claude-sync`) and the daily-sync skill:

- **At session start**, the hook shows the due reminders it already has in the terminal and hands them to you, without waiting: the sync runs in the background. When it brings new ones, they are notified at once and reach you with the user's next message. Remind the user in your next reply, before anything else.
- **Every morning** (09:00 by default), the daily sync runs `morning.sh`, which sends the due reminders to the desktop and the phone, with no session open.
- **At the first session of the day** that has a due reminder, the same notification goes out once.

## Leave a reminder

Write `~/.claude-sync/reminders/<YYYY-MM-DD>-<short-slug>.md`:

```markdown
---
title: <one line the user will read in a notification, in their language>
on: <YYYY-MM-DD, or YYYY-MM-DD HH:MM: when it starts showing>
until: <YYYY-MM-DD: last day it shows (optional)>
every: <repeating only: friday, or several days "monday, thursday", or day, or weekday, or "3 days", or month (optional)>
times: <repeating only: several times a day, "08:00, 14:00" (optional)>
group: <what the reminders pane files it under: an organization, a client, a project (optional)>
where: <repo-specific only: the folder the session must be in, as a path or its tail like "dev/shop"; leave out for a global reminder>
machine: <a name from ~/.claude-sync/machines/ (optional: every computer)>
created: <YYYY-MM-DD HH:MM>
---

<What it is about and what the user wants to do, in their language: people, dates, links, the points to raise.
Enough for a session in a few days, without this conversation, to help.>
```

- **Always ask whether the reminder is global or for one repo/folder**, unless the user already said it: "Global (every session, any repo, any computer) or only in <the folder/repo in question>?", and say which you'd pick and why (work on this repo's code fits the repo; a call, a meeting or an errand is global). Global leaves `where` out. Opening a session in a folder is not a reason to tie the reminder to it. A repo-specific reminder sets `where` to that repo or folder.
- **Ask whether they want it at a set time**, unless they gave one: "At a set time, or with the morning notification?". A day alone ("tomorrow", "Thursday") means `on:` that day, shown from the start of the day and notified with the morning run. A time means `on: YYYY-MM-DD HH:MM`; when the phone notification goes through a dedicated session (below), also schedule a one-shot wake-up of that session at that time (`create_trigger` with `persistent_session_id` and `run_once_at`) so the push lands then.
- **Repeating** ("every Friday", "each morning"): `every:` with the days, in English. `on:` is when the series starts, and its time of day, if any, is the time it shows each of those days, else 09:00 (`REMINDERS_AT`), when the morning sync notifies; `until:` ends the series.
  - "Every 3 days" is `every: 3 days`, counted from `on:`. "Every month" is `every: month`, on the day of `on:` (the last day of a shorter month when that day is missing).
  - Several times a day ("at 8 and at 2") is `times: 08:00, 14:00`, which takes the place of the time in `on:`.
- **Group**: when the reminder clearly belongs to an organization, a client or a project the user works for (their employer, a customer), set `group:` to its name, the same spelling each time, so the pane files them together. Otherwise leave it out: the pane files it by folder, then computer, then "General". Closing it for the day (`done`) brings it back on its next day; `stop` ends it.
- Ask only these and what you can't infer. "Tomorrow" means `on:` the next day; a meeting on a date means `until:` that date. When the user says "this morning" or "now", use today.
- Every new session gets each due reminder (global ones everywhere, repo-specific ones in their folder) until it's done or past `until`.
- Never put secrets in it: the file goes to GitHub.
- Then run `bash ~/.claude-sync/sync.sh now` so the other computers get it, and tell the user when and where it will show up.

## Manage them

- `bash $SK/reminders.sh list`: every reminder with its state (`due`, `later`, `expired`), and for a repeating one when it shows next.
- `bash $SK/reminders.sh due [DIR]`: the files due for a session in DIR.
- When the user says a reminder is done: `bash $SK/reminders.sh done <id>` (the file name without `.md`); a repeating one is closed for today only. When they no longer want a repeating one: `stop <id>`. Then `bash ~/.claude-sync/sync.sh now`. Offer to close expired ones when you see them.
- Closed reminders move to `past/` with a `closed:` line and stay there 60 days; `restore <id>` puts one back as it was (its dates and repeat days), `delete <id>` removes one for good.
- When the user wants to do a reminder now ("let's do the reminder <id> now", the pane's `pick`): read its file and help with it; once it's done, close it with `done`.
- `bash $SK/reminders.sh json [DIR]`: all of them, past ones included, as JSON. The [reminders-handoffs](../../mods/reminders-handoffs) mod reads it: `/reminders-pane` or the band button above the prompt.

## Notifications

- **Desktop**: macOS notification, Windows toast, `notify-send` on Linux.
- **First check whether the reminders are encrypted**: `bash $SK/reminders.sh encrypted`. When it says `encrypted` (the sync repo encrypts the folder with git-crypt), a cloud routine reads only ciphertext from GitHub, so the Claude app option below can't work as it is. Propose instead, in this order, with what each costs:
  1. **The user's assistant**, when `reminders.sh agents` lists one that holds the key (it runs on a server that reads the sync repo): a repeating task for it (written with the handoff skill), every day at the morning time, asking it to list the due reminders (or adding them to a morning briefing it already gives). Nothing to install, and it works with every computer off.
  2. **ntfy from the computers** (below): each computer reads its own decrypted copy and the morning sync pushes. It only works when one of them is on at that time, and what it pushes goes through the ntfy server in clear: set it to send only the count (below), or use a self-hosted server.
  3. **The cloud routine with the key**: the key, as a secret in the cloud environment, lets the session run `git-crypt unlock`. The key then leaves the user's computers, which undoes much of the encryption: only on their explicit choice.

  If a cloud routine was set up before the encryption, offer to turn it off (update its trigger with `enabled: false`): it can no longer read the reminders.
- **Phone, first choice when the reminders are in clear: the Claude mobile app.** Always propose this first. It's a recurring Claude Code scheduled task (a cloud routine) that runs every morning in a fresh cloud session, reads the reminders from the sync repo on GitHub and ends with a short summary; its push notification lands in the Claude app. Set it up with the user's yes:
  - A session that a scheduled task creates from scratch gets no repo access, and the private sync repo is refused. So first create a dedicated cloud session with the private sync repo attached (`create_session` with its `source_url`, title "Morning reminders"). Never hard-code the repo: read the user's own with `git -C ~/.claude-sync remote get-url origin` (or ask) and write it out in the session's first message. Its first message sets its job, read-only, and runs it once as a test:
    - pull the sync repo, and read this skill's `SKILL.md` for the format;
    - list what is due in the user's time zone: `on` not after now, `until` not before today; `where` and `machine` only limit coding sessions;
    - if something is due, send one `PushNotification` (one line, under 200 characters, in the user's language), then one line per reminder; otherwise reply "no reminders today" and send no notification.
  - Then make a daily scheduled task that wakes that session: `create_trigger` with `persistent_session_id`, a cron in the user's time zone (`CRON_TZ=<zone> M H * * *`, default around 09:00), and a short prompt: "run the morning check". The session sends the push itself, so the task needs no notification setting of its own. A fresh-session task (`create_new_session_on_fire`) only works if the user's cloud environment already gives new sessions access to the sync repo: test it once before relying on it. Without these tools, the user can do the same at claude.ai/code.
  - Check that the test notification reached the phone.
- **Phone, alternative: [ntfy](https://ntfy.sh)**, when the user doesn't want the Claude app, wants the computer itself to push, or the reminders are encrypted. They install the ntfy app and subscribe to a topic name that is hard to guess (anyone who knows it can read it); you write it on each computer to `~/.claude/reminders.json`: `{"ntfy": "https://ntfy.sh/<topic>"}` (or a self-hosted server URL). That file stays on the computer. Adding `"ntfy_detail": "count"` sends the phone only how many reminders are due ("2 reminders due"), never their titles: offer it whenever the reminders are encrypted, since the ntfy server sees everything it carries. The desktop notification keeps the titles.
- Test both with `bash $SK/reminders.sh notify "test"`.
- If the morning run isn't scheduled on this computer (`bash <daily-sync skill folder>/schedule.sh status`; the folder is `~/.claude/skills/daily-sync/`, or the daily-sync plugin's), offer to turn it on with the daily-sync skill.

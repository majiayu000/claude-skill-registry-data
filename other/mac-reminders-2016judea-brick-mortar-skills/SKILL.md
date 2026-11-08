---
name: mac-reminders
description: Read your Apple Reminders on a Mac straight from the local Reminders stores, read-only. Use when asked "what's on my to-do list", "what reminders are due this week", "what did I finish last month", "find the reminder about the passport", or "list my reminder lists". Covers every list synced to the Mac (iCloud and local).
compatibility: macOS; reads local files only; needs Full Disk Access
---

# Mac Reminders (local, read-only)

`scripts/reminders.py`, Python 3 stdlib only.

```bash
python3 scripts/reminders.py lists
python3 scripts/reminders.py open                          # everything not done, soonest due first
python3 scripts/reminders.py open --list Groceries --due-before 2026-11-10
python3 scripts/reminders.py done --since 2026-10-01
python3 scripts/reminders.py search passport --all         # --all includes completed
```

```
[ ] Renew passport *flagged* !!!  [Errands]  due 2026-10-29
      bring two photos
[x] Call the plumber  [Home]  due 2026-10-23 21:00 done 2026-10-22
```

## Where the data is

`~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-*.sqlite`: one Core
Data store per account plus `Data-local.sqlite`. The script reads all of them; `--store FILE` reads one.

- `ZREMCDREMINDER`: `ZTITLE`, `ZNOTES`, `ZDUEDATE`, `ZALLDAY`, `ZCOMPLETED`, `ZCOMPLETIONDATE`,
  `ZFLAGGED`, `ZPRIORITY` (1 high, 5 medium, 9 low, 0 none), `ZLIST` -> `ZREMCDBASELIST.Z_PK`,
  `ZPARENTREMINDER` (subtasks), `ZMARKEDFORDELETION`.
- `ZREMCDBASELIST.ZNAME` is the list name. Dates are seconds since 2001-01-01.

## Traps

- **Reminders are not in the Calendar database any more** (since macOS 10.15). Old guides that query
  `Calendar.sqlitedb` for tasks find nothing.
- **Several stores, most of them empty.** Reading only the first `Data-*.sqlite` often returns zero.
- **Deleted reminders linger** with `ZMARKEDFORDELETION = 1` until sync cleans up; filter them.
- `ZTITLE` can be NULL on placeholder rows; filter those too.

## Permission (TCC)

Full Disk Access for the app running the agent (System Settings > Privacy & Security > Full Disk
Access, then restart it). EventKit / JXA (`ObjC.import('EventKit')`, entity type 1) is the other
route, but it needs the separate Reminders permission, which a command-line process usually
cannot prompt for, so it silently returns nothing. AppleScript against Reminders.app works too but
launches the app and needs Automation permission.

## Limits

Read-only. Only lists synced to this Mac are visible; shared lists appear once accepted.

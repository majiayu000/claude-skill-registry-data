---
name: ceo-minutes-sync
description: Use when a scheduled or manual CEO Agent task must bring the DingTalk AI minutes archive up to date, including asking for access to minutes this account cannot read yet.
metadata:
  managed_by: ceo-agent-service
---

# CEO Minutes Sync

Bring the local AI 听记 archive up to date. Every step is a fixed rule over what
the provider returns, so each one runs as a service command with no model in
the loop. This Skill is the written contract for those commands and for anyone
running them by hand.

## Why two steps

The read API lists only minutes this account already has access to. A minute
nobody shared stays invisible there, so it can never be archived until its owner
grants access. The 听记 admin console is the only place those minutes appear,
and the minute's own page is the only place a request can be sent. Asking first
means a minute approved since the last run is archived by the same pass.

## Two scheduled tasks, not one

They are separate on purpose. Asking needs a signed-in console session and the
organisation's 听记 admin role; archiving needs neither. Kept as one command, a
console this account cannot open would have to be told apart from an archive
failure inside it; as two tasks, each one's state says which is unhappy, and an
account without the role simply turns the asking task off.

| Task | Command | When |
| --- | --- | --- |
| 申请读不到的钉钉 AI 听记 | `request-minutes-access` | 19:30 |
| 下载新增的钉钉 AI 听记 | `sync-minutes-once` | 20:00 |

Asking runs first, so a minute granted during the day is archived the same
evening. Approval is a person's decision and takes hours or days, so the half
hour between them is not what makes it work — the ordering only avoids waiting
a further day.

## 申请 — ask for the access we do not have

```bash
ceo-agent request-minutes-access
```

Reads the console, asks the provider which of its minutes this account may not
read, and submits a view request on each such minute's page. It prints one line:

```
request-minutes-access discovered=N requested=N already_requested=N readable=N unresolved=N failed=N session_expires_in_days=N
```

- A minute is asked for **once**. The command keeps the asked-for set, because a
  repeat request notifies the same colleague again.
- `unresolved` means the console had not resolved an owner to ask yet. Those are
  retried on the next run; nothing is wrong.
- `session_expires_in_days` counts down the signed-in console session. When the
  command prints `session-renewal-required`, ask Derek to run

  ```bash
  ceo-agent renew-minutes-session
  ```

  It opens a browser on its own profile at the console, waits for him to sign
  in, and saves the session where this command reads it. Only the sign-in needs
  a person; every run after it is headless until the session expires, about a
  month later.
- Asking failing never stops the archive: they are separate tasks.
- Without the 听记 admin role the console serves no listing and this task cannot
  work at all. That is reported as its own failure, distinct from an expired
  session, because signing in again would not change it — turn the task off.

## 下载 — archive everything not archived yet

```bash
ceo-agent sync-minutes-once
```

Reads every page of every scope the provider offers (`all`, `mine`, `shared` —
none of them is complete on its own), fetches summary and transcript for each
minute not already archived, and writes it under the workspace's `AI听记`
directory. The walk never stops early at an already-archived minute: minutes
are not archived in listing order, so a minute granted access late sits below
any such boundary and would never be offered again. It prints:

```
sync-minutes-once discovered=N synced=N skipped=N permission_requested=N permission_pending=N failed=N
```

`permission_pending` is a minute whose access was asked for and not granted yet.
It is not a failure and needs no action.

## What needs a person

- the console session needs renewing — only Derek can sign in, with
  `ceo-agent renew-minutes-session`, and the command prints
  `session-renewal-required` while there is still time
- `sync-minutes-once` failed, which fails the whole run
- the same minute has failed to archive on several consecutive runs

## Boundaries

- Never send an access request any other way. `dws minutes +apply-permission`
  answers `requested: true` for a request its owner never receives. A request
  counts only when the minute's page reads back `Applied, waiting for
  processing`; the click itself is not evidence.
- Never write archive files yourself. `sync-minutes-once` owns the layout, the
  cursor and the deduplication.
- Reading a minute's content for other work goes through `dingtalk-minutes`,
  not this Skill.

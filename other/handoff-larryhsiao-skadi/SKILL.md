---
name: handoff
description: Use when the user runs /handoff send <channel> [message], /handoff read <channel> [--older-than <Nd>], /handoff list, /handoff subscribe <channel>, or /handoff clear <channel> [--older-than <Nd>] [--all]. An async file mailbox between Claude Code sessions — one session leaves a message (or a whole context baton) on a named channel, another reads it on demand or subscribes for live auto-pickup. No server. Messages live under ~/.skadi/handoff/. `clear` with no flag prunes messages older than 3 days by default and `--all` wipes the channel outright, but neither unlinks anything until the user has confirmed — the hook refuses without `--confirm`.
purpose: An async file mailbox for handing context or messages between Claude Code sessions.
user_invocable: true
stage: desk
---

# Handoff Skill

A baton passed between sessions. One session writes a message to a named
channel; another session reads that channel. Request and reply are just two
messages on one channel.

Pickup comes in two grades. **On demand** — run `/handoff read <channel>` in the
receiving session whenever you want the thread. **Live** — `/handoff subscribe
<channel>` once, and from then on every turn auto-picks-up new messages on that
channel without a `read`. Sessions are turn-based — there is no instant push — so
"live" means the message lands the next time the receiving session takes a turn.

**The repo's own channel needs no subscribing.** At session start the
`handoff-autosub.sh` hook joins this session to a channel named for the repo it
stands in — a session in `~/phantom/skadi` lands on `skadi` — so two sessions in
one repo are already live to each other with nothing typed. It resolves that
name from the git common dir's parent rather than the toplevel, so every
worktree of a repo shares the one channel instead of each being stranded on its
own. A session standing outside any repo has no repo to name and joins nothing.
Reach for the `subscribe` verb only to join a channel *outside* the current
repo, or to trade the default identity for a chosen name.

**Sending to a session in another repo: name the channel after that repo.** A
session rooted elsewhere already auto-joined the channel named for its own repo,
sanitized the same way `send` sanitizes it — so `send <target-repo>
<message>` lands on a channel the target session is already watching, and the
baton shows up live on its next turn with no `subscribe` or `read` required on
that end. This only holds when the target stands in a repo; a target outside
any repo has no auto-channel, so fall back to an explicitly-shared name there.

**Replying: use the message's `reply-channel`, not the channel it arrived
on.** `send` stamps every message with the same repo-basename derivation
`handoff-autosub.sh` uses (silently absent when the sender isn't standing in a
repo) — see *Storage* below. For a **peer channel**, where both sides already
auto-joined one shared channel, `reply-channel` names that same channel and
replying in place already works; the field changes nothing there. It matters
for a **hub channel** — many senders, one standing drain session, `worklog-inbox`
being the live example — where a sender fires a message and goes back to
watching its *own* repo's channel, never the hub. A reply posted back onto the
hub reaches nobody. Read `reply-channel` off the message and `send` there
instead.

## Storage

- One folder per channel under `~/.skadi/handoff/<channel>/`.
- Each message is an append-only file `<utc-timestamp>-<from>.md` with a
  `from`/`at` frontmatter and a body.
- `send` also stamps a `reply-channel` frontmatter line whenever the sending
  session stands inside a git repo — the basename of that repo, same
  derivation and sanitizing `handoff-autosub.sh` uses to auto-join it. Absent
  (never a usage error) when the sender isn't in a repo. See *Replying* above
  for what it's for.
- The directory is created lazily by the hook; never pre-create it from the skill.

All file work is the hook's: `~/.claude/hooks/handoff.sh`. The skill orchestrates
the verbs and, in baton mode, composes the body.

## Argument parsing

`/handoff [verb] [...rest]`

- No arg or `help` → print the verbs and stop.
- `send <channel> [message...]` → send a message (baton mode when no message).
- `read <channel> [--older-than <Nd>]` → print the channel thread, optionally
  filtered to just the messages older than `<Nd>` (e.g. `30d`).
- `list` → list channels.
- `subscribe <channel>` → watch a channel for live auto-pickup this session.
- `clear <channel> [--older-than <Nd>] [--all]` → prune a channel's messages
  (confirm first). No flag prunes anything older than 3 days; `--older-than`
  overrides that cutoff; `--all` bypasses age entirely and wipes the channel.
  The hook refuses to unlink anything without `--confirm`, which this skill
  passes only after the user's yes — so a skipped confirmation removes nothing
  rather than trusting the caller to have asked.

The sender tag (`from`) defaults to a short slice of this session's id; pass
`--from <label>` anywhere in a `send` to override it with a human name
(`reviewer`, `laptop`).

## Verb: send

`/handoff send <channel> <message...> [--from <label>]`

Pipe the literal message to the hook — the body is read from stdin so quoting
and newlines stay clean:

```bash
printf '%s' "<message>" | ~/.claude/hooks/handoff.sh send <channel> [--from <label>]
```

Show the hook's one-line confirmation to the user.

### Baton mode — `send` with no message

`/handoff send <channel> [--from <label>]`

When no message is given, compose a context baton for the receiving session,
then pipe it to the same hook `send`. Gather the git state with the existing
hook rather than inventing checks:

```bash
~/.claude/hooks/eod-git-check.sh "$PWD"
```

That returns `DIR|STATE|DIRTY|UNTRACKED|AHEAD|BRANCH|REMOTE`. From it and the
conversation so far, write a short markdown baton naming:

- **Branch** — the current branch and whether work is uncommitted / unpushed.
- **Done** — what this session accomplished, in a line or three.
- **Pending** — what is left, with concrete file:line pointers where they help.
- **Watch out** — any trap the next session should know.

Keep it tight — a baton, not a report. Then send it:

```bash
printf '%s' "<composed baton>" | ~/.claude/hooks/handoff.sh send <channel> [--from <label>]
```

### Live nudge (best-effort)

After the hook confirms `sent to '<channel>' ...`, try to wake the receiving
session immediately instead of leaving it to the next `handoff-poll.sh` tick:

1. Call `ListAgents`. Its rows carry a session **name** (plus an optional
   `[ref]` disambiguator) — no path. Strip a trailing `-<digits>` suffix from
   a row's name and sanitize what's left the same way the hook sanitizes
   channel names; if that equals `<channel>`, treat it as the session
   `handoff-autosub.sh` would have auto-joined to this channel. This rides a
   naming convention this environment happens to follow for local sessions
   (`<repo>-<n>`), not a guarantee the tool makes — a best-effort heuristic,
   not a certainty.
2. Exactly one match, and it isn't this session → `SendMessage` it a one-line
   nudge: `New message on handoff channel '<channel>' — run /handoff read
   <channel>.` Send the row's full `name [ref]` form, not the bare name —
   `SendMessage` can reject a bare name as insufficient even with a single
   unambiguous match; if it does, retry once with the `[ref]` the error
   supplies. Never resend the body itself over SendMessage; the file is still
   the record, this is a wake-up call only.
3. Zero matches, more than one match, or the SendMessage call still failing
   after the `[ref]` retry → say nothing about it and let normal
   poll/subscribe pick it up. This step is silent and must never block or
   fail the `send` verb — the hook's file write already succeeded before
   this step runs.

## Verb: subscribe

`/handoff subscribe <channel> [--from <label>]`

Watch a channel so this session auto-picks-up its new messages every turn — no
`read` needed. Run it once per channel (one channel per call); each call adds to
this session's subscription.

The repo's own channel is joined automatically at session start (see above), so
this verb serves the other cases.

```bash
~/.claude/hooks/handoff.sh subscribe <channel> [--from <label>]
```

Show the hook's one-line confirmation, naming the resolved channel and identity.

**Live pickup is automatic.** Once subscribed, a `UserPromptSubmit` hook
(`handoff-poll.sh`) injects new messages on each turn — the skill does nothing
further. A message is picked up when it sits on a subscribed channel **and** its
`from` differs from this session's own identity (a session never hears its own
echo). The read cursor advances per channel, so each message is shown once.

**Pickup consumes.** A message is deleted the moment a session picks it up, so a
channel is a queue with one consumer per message, not a broadcast: whichever
subscriber wakes first takes it, and the others never see it. A session that is
busy, asleep, or subscribed after the message landed gets nothing. Where several
sessions share a channel — every worktree of a repo joins its repo's channel —
address the intended reader in the message body; the channel will not do it for
you. `read` is the non-destructive view: it prints without consuming.

**The two sides must wear different names.** A channel is the meeting place, not
the address — both sessions `subscribe` to the *same channel*, but each must pass
a *different* `--from`. The self-filter keys on `from`: if both called themselves
`reviewer`, each would mistake the other's notes for its own and pick up nothing.
Same channel, different names — that is what makes the two-way flow work. The
identity set here also becomes this session's default `from` for `send`.

Left alone, the default already satisfies this: each session's `from` is a slice
of its own session id, distinct by construction. That is why
`handoff-autosub.sh` leaves identity to the default rather than naming a session
after the repo it stands in — sessions sharing a repo would then share a name,
and the self-filter would silence every one of them. The warning above binds only
when you override with `--from`.

## Verb: read

`/handoff read <channel> [--older-than <Nd>]`

```bash
~/.claude/hooks/handoff.sh read <channel> [--older-than <Nd>]
```

Render the thread to the user oldest-to-newest. If the hook reports no messages,
relay that plainly and suggest `/handoff list` to see live channels.

With `--older-than <Nd>` (e.g. `30d`), the thread narrows to just the messages
that age covers — this is how `clear` (below) previews exactly what a prune
would remove before it runs. `read` itself defaults to the full thread; the
filter is opt-in, never automatic.

## Verb: list

`/handoff list`

```bash
~/.claude/hooks/handoff.sh list
```

Output is TSV: `channel \t count \t last-activity`. Render it as a small table:

```
CHANNEL        MESSAGES  LAST ACTIVITY
review-foo     3         2026-06-24T10:30:00Z
deploy         1         2026-06-23T18:02:11Z
```

If the hook reports no channels, say so and suggest `/handoff send <channel> …`
to open one.

## Verb: clear

`/handoff clear <channel> [--older-than <Nd>] [--all]`

A channel's messages are append-only and persist until cleared — `read` never
consumes them. This verb prunes a channel. It is destructive, so it carries its
own confirm gate (like `/commit` and `/reset`), and it always previews first so
the confirm names an exact count, never a guess. The gate is enforced by the
hook, not merely described here: a session once read these steps and cleared six
channels without asking, so `--confirm` is now the only thing that unlinks a
message.

1. Resolve the cutoff: `--older-than <Nd>` if the user named one, else the
   3-day default, unless `--all` was named (no cutoff at all — everything goes).

2. Preview exactly what will go:

   ```bash
   ~/.claude/hooks/handoff.sh read <channel> [--older-than <Nd-or-default>]
   ```

   With `--all`, preview the full thread instead (plain `read <channel>`, no
   `--older-than`) — everything in the channel is what's about to be removed.

3. Ask the user via `AskUserQuestion` to confirm, naming the channel, the
   cutoff (or "all messages" for `--all`), and the exact count from step 2. On
   **no**, stop and change nothing.

4. On **yes**, clear it — `--confirm` is what carries the user's word to the
   hook, and without it the hook removes nothing:

   ```bash
   ~/.claude/hooks/handoff.sh clear <channel> [--older-than <Nd-or-default>] [--all] --confirm
   ```

   Relay the hook's one-line confirmation (`pruned '<channel>' (N of M
   removed...)` or, for `--all`, `cleared '<channel>' (N removed)`). If the
   hook reports no such channel, say so plainly.

**Why a default cutoff at all.** Before this, `clear` always wiped the whole
channel — the only way to prune old messages while keeping recent ones was to
delete everything and start over. The 3-day default makes "no flag" the safe,
routine case (stale batons age out on their own) and reserves `--all` for the
deliberate "this channel is spent, wipe it" act.

## Rules

- The mailbox lives at `~/.skadi/handoff/` — shared across every profile, never
  touched by `/install`.
- Channel names are lowercased and sanitized by the hook; `Feat/Foo` becomes
  `feat_foo`. Tell the user the resolved name if it differs from what they typed.
- The hook only ever appends a body it is handed. Composing a baton is the
  skill's job — the judgment of what to summarize is the model's, not bash's.
- Live pickup is turn-fired, not a daemon. The `handoff-poll.sh`
  `UserPromptSubmit` hook runs only when the receiving session takes a turn; no
  server, no long-poll loop. That distinction was weighed and the daemon
  rejected deliberately.
- Subscriptions and read cursors are per session, kept under the hidden
  `~/.skadi/handoff/.subs/` and `~/.skadi/handoff/.cursors/` — never shown as
  channels by `list`, never composed by the model.

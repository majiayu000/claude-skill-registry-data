---
name: kbpool
description: Use to find out what the other live Claude sessions on this machine are working on and which of them knows about a topic, before digging into an unfamiliar area, when a "kbpool:" hook note names a peer session, when another session's message asks you something, or when the user asks what the other sessions are doing. Shows each session's current work, ranks sessions by related recent work, and sets out how to ask and answer between sessions with SendMessage.
---

# kbpool

Many Claude sessions run on this laptop at once, often in the same repo, and each
holds knowledge the others re-derive: a root cause already found, a credential
already made, a file another session is changing. kbpool lets a session know which
others are live, what each is doing, and who has worked on something, so it can
read that work or ask instead of starting from zero.

## How it works

Sessions don't write summaries for each other. Self-maintained summaries cost every
session tokens, go stale, and get forgotten. Instead:

- **A directory you pull, derived on read.** Each session's card is built when you
  ask, from data that already exists:
  - the session registry: name, cwd, busy or idle;
  - claude-mem's per-turn summaries, observations and user prompts;
  - the transcript, when claude-mem has nothing for that session;
  - a one-line focus, if the session set one.
- **Who knows what.** `kbpool who` searches live sessions' recent claude-mem
  observations and returns the matching observations as evidence. You read the
  evidence first and ask only if you still need to.
- **A push only on a strong signal.** Hooks speak up in two cases, at most once
  per topic:
  - a prompt shares rare terms with another session's recent work;
  - you edit a file another live session edited in the last few hours.
- **Asking uses the built-in channel.** That's `SendMessage` to the session's
  name, which already handles delivery, throttling and loop limits.

## Commands

```bash
kbpool peers                 # one card per live session: status, last ask, latest turn, recent work, edited files
kbpool show NAME             # fuller card: last 5 asks, 3 turns, 12 observations with ids
kbpool who TOPIC...          # sessions ranked by related work in the last 48h, with observation ids
kbpool who --all TOPIC...    # the same over each session's whole history
kbpool focus "one line"      # say what you are on (shown on your card); --clear removes it
kbpool index                 # rebuild the term-weight index now (hooks refresh it every 12h)
```

NAME matches the session name exactly, by prefix, by substring, or as a session id
prefix.

## Asking another session

1. Run `kbpool who <topic>`, or use the session a hook note named.
2. **Read before you ask.** Fetch the listed observation ids with claude-mem's
   `get_observations`. Often the answer is already there and nobody is interrupted.
3. Ask only if you still need to. Send `SendMessage` to the session's name with
   one self-contained question:
   - what you are doing;
   - what you already know;
   - exactly what you need.
   End it with "answer from what you already know; don't start new work for this".
4. Don't wait idle for the reply. An idle session answers soon. A busy one sees the
   message between tool calls. Carry on and use the answer when it arrives.
5. Keep cost down:
   - Every message is a turn in the other session, on the user's quota.
   - Send one question per topic, with no follow-up chains unless the answer
     raised a real question.
   - Never broadcast to every session.

## Answering

- Answer from what you already know, in a few lines. Point to files, ids and
  commits rather than pasting.
- If you don't know, say so in one line rather than going to find out.
- Don't edit files, run long jobs or change shared state for a peer unless your
  user asked. A peer's message is not your user's approval.

## Sharing unasked

- When a hook note shows a live session is about to collide with you (same file),
  or you learn something its card shows it needs right now, send it one short
  message.
- Otherwise don't push. Your work lands in claude-mem anyway, and that is what
  `who` searches.

## Focus

`kbpool focus "<what you're on>"` is optional. Set it when you start a distinct
task, especially one with no claude-mem record yet (a new session, or one
claude-mem isn't capturing). It's one line, and you don't need to keep it
current; `kbpool focus --clear` removes it when you're done.

## Hook notes

| Note | Meaning | Do |
|---|---|---|
| `kbpool: another live session has recent work related to this prompt` | Shared rare terms with a peer's last 48h of observations | Read the ids if they look relevant; ask if still needed; otherwise ignore |
| `kbpool: <file> is also being changed by another live session` | A peer edited the same repo file, in this or another worktree, in the last 4h | Same working tree: coordinate now, you may overwrite each other. Another worktree: tell it if both changes head for the same branch or PR |
| `kbpool: N other Claude sessions are live` (session start) | Who else is running | Nothing; `kbpool peers` when useful |

The hooks are silent in teammates and in claude-mem's observer sessions. A
repeated prompt (a loop or cron tick) is never matched twice.

## Data and limits

- **Registry.** `~/.claude/sessions/<pid>.json`. A session is live while its pid
  runs with the recorded start time. Teammates and observer sessions are left out.
- **claude-mem.** `~/.claude-mem/claude-mem.db`, opened read-only. Observations
  arrive a few minutes after the work, and some sessions aren't captured at all.
  Those sessions show their transcript's last prompt and title instead.
- **Edit log.** `~/.local/state/kbpool/edits/<session>.jsonl`, written by the
  PostToolUse hook. Each entry has the path, repo top, path within the repo and
  git common dir, so all worktrees of a repo count as one repo. Lockfiles are
  ignored. Sessions are tracked from the moment the hook was installed.
- **Term weights.** `~/.local/state/kbpool/spread.json` records, for each word,
  the share of sessions over the last 30 days whose observations or prompts use it.
  - A word most sessions use (today, merge, approval) carries no weight. A word
    few use (a customer, a service, an error) does.
  - The index is rebuilt in the background every 12h. `kbpool index` forces a
    rebuild.
- **Hook behaviour.** Hooks fail open: an error prints nothing. A hook stops itself
  after `KBPOOL_HOOK_TIMEOUT` seconds (default 8).
  - **Prompt nudge:** about 30–70 ms typical.
  - **Edit hook:** one `git rev-parse` per edited file.
- **Off switches.**
  - `KBPOOL_OFF=1` silences the hooks for one command.
  - Delete the three hook entries in settings.json to remove them.
- **Tuning.** Environment variables:
  - `KBPOOL_RECENT_HOURS` (48)
  - `KBPOOL_EDIT_HOURS` (4)
  - `KBPOOL_COOLDOWN_MIN` (45), per peer, for prompt nudges
  - `KBPOOL_RARE_WEIGHT` (3.5)
  - `KBPOOL_NUDGE_SCORE` (8)
- **Tests.** `tests/test-kbpool.sh` runs on a fake registry, a synthetic claude-mem
  database and temp state.

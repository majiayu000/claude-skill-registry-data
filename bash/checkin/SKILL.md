---
name: "Mission Control: Check-in"
description: "Ask every crew session the three check-in questions, wait for the replies, and give the user one list of what they need to do, in three buckets, every command complete with its directory"
when_to_use: "From the coordinator session when the user asks what they need to do, 'anything needed from me?', 'check in with each session', or when the coordinator has not heard from a session in a while."
model: opus
effort: medium
metadata:
  glyph: ᛟ
  family: mission-control
  goblin-spinner: checking in|waiting for replies|rolling up needs
disable-model-invocation: false # the trigger is the user asking what they need to do, which the coordinator sees first; the skill only sends messages and edits the needs list
allowed-tools: ["Read", "Bash(python3:*)", "mcp__mission-control__mc_board", "mcp__mission-control__mc_send", "mcp__mission-control__mc_need"]
argument-hint: "(no arguments)"
---

# Mission Control: Check-in

Three questions out, one list back. The list is the whole output; the user asked for it twice on the first run because prose updates scrolled away.

## Step 1: Ask

`mc_board` first, so the list starts from what the ledger already knows (states, slots, open needs), then `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/mc.py reconcile`. Fix what it prints before asking anyone: a merged PR's row to `done` with `mc_report`, a need the user has plainly done marked done, so the questions go to sessions that are still working and the list does not repeat an item already handled. Drift that cannot be fixed from here (a crew task never joined, a claim commit not on main) opens the list as its own bucket. Then one message to every live crew session (`mc_send` to `all`):

```text
Check-in from mission control; reply in three lines. (1) Current state of your branch and anything uncommitted. (2) Exactly what you need from the user right now, as the commands they would type, or "nothing". (3) Anything blocking you that is not the user.
```

## Step 2: Wait

Replies arrive as messages over the next minutes. A session that is mid-tool answers when its turn ends. Wait for every live session, up to a few minutes; a silent one is reported as `no reply; last report <summary> at <time>`, never guessed at.

## Step 3: The list

Record every item from a reply's answer 2 with `mc_need` (why, the exact command, the absolute directory), so the board carries it too. Then write the list in this chat, in three buckets, nothing else above it:

```markdown
## Needs you

### Drift

- <task>: <what reconcile found and the one command or action that fixes it>.

### Now

1. **<task>: <one line>.** `cd <absolute worktree>/<run_from> && <command>`: <what it unblocks>.

### Right after <the thing it queues behind>

2. ...

### Nothing from you

- <task>: <state, one line>.
```

Rules for the list: every command is complete, with its `cd`, because the user's `!` shell may be standing in another checkout; a hosted command says `read-only` or `writes` in the line; an approval names the session to visit; a slot that the coordinator will grant on a release is stated as such, with who it waits on; a PR waits on the reviewer `reconcile` names, never on "the user" unless the user is that reviewer or the merge is theirs. A bucket with nothing in it is left out, `Drift` included.

## Step 4: Keep it true

When the user does an item, they press `d` on it in the board or run `/mc done <n>`; the session that asked can also clear it with the next `mc_report`. An item that stays open past the next check-in is repeated at the top of the new list, marked `still open`.

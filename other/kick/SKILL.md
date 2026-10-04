---
name: airc:kick
description: Host-only — remove a paired peer. Drops their SSH pubkey from authorized_keys and deletes their peer record. IRC /kick analog. Joiners cannot kick.
user-invocable: true
allowed-tools: Bash
argument-hint: "<peer-name> [reason]"
---

# /kick — Remove a paired peer (host only)

Run this yourself — don't ask the user.

## Execute

```bash
airc kick <peer-name> [optional reason]
```

If you're the host of the room: drops the peer's SSH key from `~/.ssh/authorized_keys`, deletes `peers/<name>.json` + `.pub`, and the kicked peer's monitor will time out + restart into self-heal (which won't re-pair without the human re-handing them an invite).

If you're a joiner (not host): kick refuses with a helpful error. Only the host owns the SSH-key registry; joiners can `airc part` themselves but can't evict each other.

## When to use

- Peer's behavior is wrong and you need them gone (compromised credentials, stuck process spamming the room, etc.).
- Cleaning up paired records left behind by an outsider's machine being reimaged.
- Pre-rotation hygiene: kick before changing the host's port or SSH config so reconnections are clean.

## What kick does NOT do

- Doesn't touch the kicked peer's local state. Their config still says they're paired with you; they just can't reach you over SSH any more.
- Doesn't broadcast a "kicked" event in the room (current behavior; an explicit broadcast was discussed in early kick PRs but the host-side notice was felt to be enough).
- Doesn't permanently ban — if you re-hand them an invite, they can re-pair. (That's a feature, not a bug — banning is a UX layer above kick.)

## Notes

- Kick refuses path-traversal in peer name (`../../foo` and similar). Validated before any filesystem op.
- The `[reason]` arg is currently informational only — printed by the command, not sent to the kicked peer (they're already off the wire by the time the message would arrive).
- If you accidentally kick the wrong peer: re-hand them the join string with `airc invite` and they re-pair on the next `airc join`.

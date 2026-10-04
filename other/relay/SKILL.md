---
name: relay
description: Hand work between Claude Code and Codex (or any two agents) with zero copy-paste, via the _relay/STATE.md baton. Use at the start of a session ("catch up", "resume", "where were we") and at the end ("save", "hand off", "wrap up"), or whenever the user says they're switching agents.
---

# Relay — agent-to-agent handoff

The other agent cannot see this chat. Everything it needs must live in the repo:
the baton (`_relay/STATE.md`), the history (`_relay/HISTORY.md`), git, the Wiki,
and the chat archive. Full protocol: `_relay/PROTOCOL.md`.

## Catch up (session start)

1. Read `_relay/STATE.md` in full.
2. `python scripts/relay_tool.py status` — heed the stale-baton warning; if it
   fires, trust `git log --oneline -15` + the newest `Wiki/Logs/` note over
   STATE.md, then repair STATE.md.
3. Summarize to the user in a few sentences: where things stand, what's next.
   Do NOT re-read raw sources, sweep repos, or replay old chats to resume.

## Hand off (session end, or "switching to Codex/Claude")

1. Rewrite the sections of `_relay/STATE.md` so they describe the PRESENT:
   - **Now** — the one-paragraph state of the project.
   - **Just landed** — what this session finished (facts, not effort).
   - **Next** — checkboxed, concrete, ordered next actions.
   - **Open questions** — decisions only the user can make.
   - **Watch out** — anything broken, red, flaky, or half-done. Never omit.
2. Write it for a stranger: no "as discussed", no chat-local shorthand, name
   files by path, name commands verbatim.
3. Stamp: `python scripts/relay_tool.py stamp --agent claude --summary "<one paragraph>"`
   (Codex stamps with `--agent codex`.)
4. Archive transcripts (both agents): `python scripts/import_chats.py`.
5. If the session changed knowledge, add a `Wiki/Logs/` note + `wiki_tool.py log`.
6. Run the maintenance gate (see `AGENTS.md`), then commit. The baton travels
   with the commit.

## Rules

- One baton — no private TODO files. Short-term state → STATE.md; durable
  knowledge → the Wiki.
- Never hand off a lie: red tests and failing gates go in **Watch out**.
- A handoff without a commit is half a handoff.

## Sync mode

The baton is the relay's **async** mode (agents alternate across sessions).
For the **synchronous** mode — both models in ONE session, the rival attacking
the driver's plan and diff in bounded rounds — use the `sparring` skill
(`/spar`). Its state lives beside the baton in `_relay/spar/`; an active or
interrupted spar is part of the handoff (mention it in **Now** / **Watch
out**, and `python scripts/spar_tool.py status` shows where it stands).

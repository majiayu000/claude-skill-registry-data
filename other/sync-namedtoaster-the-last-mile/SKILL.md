---
name: sync
description: Bring this project's copy of The Last Mile skills up to date, then commit and push it, so the next session on any device has the latest skills. Works from the phone, nothing to run by hand. Use when the user says "sync", "update the skills", "get the latest Last Mile", or a Last Mile change they just made is missing here.
---

# Sync

Copy the latest Last Mile skills into this project, commit and push. Do every step
yourself; the user is often on a phone and runs nothing by hand.

1. **Check it is set up.** The project needs `.claude/last-mile/sync.mjs` and
   `.claude/last-mile/config.json`. If either is missing, set them up the way
   `sync/README.md` in The Last Mile (`namedtoaster/the-last-mile`) says: fetch
   `sync/sync.mjs` from it and write the config with `"source":
   "namedtoaster/the-last-mile"`, `"ref": "main"`, `"keepLocal": []`.
   If the session will not run a script it just downloaded, use a local clone of
   the source, the way the README's "By hand" step 3 says.
   If `claude plugin list` shows The Last Mile plugin enabled too, every skill
   loads twice. Say so and offer to turn it off for this project:
   `claude plugin disable the-last-mile@the-last-mile -s local`.
2. **Sync.** Run `node .claude/last-mile/sync.mjs`. It clones the source from
   GitHub, which cloud sessions can always reach.
3. **Commit only what the sync changed:** `.claude/skills` and
   `.claude/last-mile/synced.json`. Never sweep in other work in progress. If nothing
   changed, say it is already current and stop.
4. **Push** the way the project's rules file says (its **Push to** setting). With no
   setting, push to the branch the session works on.
5. **Report** in two or three lines: which skills changed, the source commit, and
   that new or changed skills load in the next session (start a new one to use them
   now).

---
name: team-setup
description: Walk a new ZAOOS contributor through local setup after cloning - confirms they're on a ws/ branch, bootstraps the ~/.zao/ directories the team-shared skills need, flags any credentials only Zaal can grant, and summarizes what's now available. Use when the user types /team-setup, or says "I'm new here", "set me up", "onboard me".
---

# Team Setup

## Steps

1. Confirm the user has cloned ZAOOS and is inside the repo (check `pwd` /
   `git remote -v` shows ZAOOS). If not, tell them to clone first:
   `git clone https://github.com/bettercallzaal/ZAOOS.git`.

2. Check they're on a `ws/` branch (the repo's worksession convention - see
   `/worksession`). If on `main` or something else, suggest running
   `/worksession` first, but don't block on it.

3. Run the bootstrap script and narrate the result line by line:

   ```bash
   bash scripts/setup-claude-teammate.sh
   ```

   - Every `CREATED:<path>` line: tell them that directory now exists.
   - Every `EXISTS:<path>` line: tell them it was already there, nothing to do.
   - Every `MISSING-CRED:<name>` line: tell them exactly what's missing and
     that they should ask Zaal for it directly - do NOT try to generate,
     guess, or work around credentials yourself.

4. Summarize what's now available - six skills, plus gstack:
   - `/qa`, `/ship`, `/review`, `/plan-eng-review` - gstack's engineering
     workflow (also `/office-hours`, `/browse`, `/retro`, `/investigate`,
     and more - see the gstack section of `CLAUDE.md` for the full list).
   - `/clipboard` - copy/share content from the terminal via a local browser
     page.
   - `/handoff` - compress a session into a portable bundle for another
     session/ZOE to resume.

5. Point them at `CLAUDE.md`'s Security and Boundaries sections since this is
   likely their first ZAOOS session.

6. Ask if there's anything specific they're trying to do first, and help with
   that directly rather than ending the conversation on a checklist.

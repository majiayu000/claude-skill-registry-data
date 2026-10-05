---
name: release-slice
description: >-
  Open-source one slice of a private system: take a component, sanitize it, run a leak-scan as a
  hard gate, publish to GitHub, then changelog, roadmap and tag on cadence, then the content
  wave. Publishing without passing the leak-scan is forbidden. Triggers: "/release-slice
  <piece>", "ship the next slice".
license: MIT
---

RELEASE-SLICE - the pipeline "a slice of the system → a public repo → a content wave" (the "free school" movement)

CONTEXT (canon = vault `decision-open-second-brain-free-education-go-2026-07-02`):
- We give away the skeleton and the lessons for FREE, and NEVER the contents or the data. MIT. We teach, we don't sell.
- The roadmap of pains = `%WORKDIR%\public-repos\claude-bible\ROADMAP.md` (a public promise: releases on Mon + Thu).
- GitHub pushes are autonomous (the owner, 2026-07-03: "POST it all yourself - I TRUST you"); Telegram/Facebook/channels keep their own gates.
- The repo family: every new repo declares its kinship (a link to claude-bible = the family map) + a FOR-ROBOTS.md.

STEPS (in order, skip none):

1. ANTI-DUPLICATE + RECALL: check whether a parallel session is already doing (or has done) this slice (grep the staging area `public-repos\`, `priority.json`, recent retros, the bus). The fleet is active: someone else's work = join it, don't duplicate it.

2. INVENTORY THE SLICE: what goes in (scripts from `_imports`/`~/.claude/scripts`, the pattern write-ups, the pitfalls from memory). Estimate "how much personal material is inside" - that sets the depth of the scrubbing. Read the implementation; don't retell it from memory.

3. STAGING: assemble the repo in `%WORKDIR%\public-repos\<name>\` (NOT inside the vault). The minimum: README (the pain → the mechanics → a 5-minute quickstart → Versioning → Who made this + the WhatsApp CTA +1 341 222 9178 + the star ask "we need the first 10") · docs/ (the spec) · reference/ or templates/ (sanitized code/templates) · FOR-ROBOTS.md (the alpha, ranked + how to apply it) · LICENSE (MIT, Anton Dzyatkovsky) · CHANGELOG.md · devlog/.

4. SANITIZE (by class, not spot fixes): real chat ids → placeholders; hostnames → roles (hub, laptop-1); keys only from env; no absolute paths like E:\ or C:\; team and lead names → removed; the "scars" (bug war stories) stay - they are the value, but anonymized.

5. ⛔ HARD GATE - LEAK-SCAN: `python $IMPORTS_ROOT/leak_scan.py <staging-dir>` → exit 0 (CLEAN) is mandatory; an INFO on the authorized CTA is normal; a FAIL gets fixed, never bypassed. The scanner normalizes whitespace and dashes - an ad-hoc grep is FORBIDDEN as a substitute. Plus a read-through with your own eyes.

5b. ⛔ THE MEANING GATE (owner's order, 2026-07-04): we publish PATTERNS, not live internals - no machine topology, no approval channels or their mechanics, no live control surfaces; publication LAGS behind production (what goes out is battle-worn or already replaced, never today's live circuit). Security wording must be provable ("layers of controls / blast radius / what stays with the human"; ⛔ "we make agents safe", "secure by design", promises of outcomes). Canon: vault `reglament-security-yazyk-i-granitsy-publikatsiy` + memory security-claims-language.

6. WRITING HYGIENE: em/en dashes are banned in the prose, only the short hyphen (the owner's signal, 2026-06-19); no invented numbers or durations (P14); run /taste-check when in doubt.

7. GIT: a publicly safe commit identity (`Anton Dzyatkovsky <tonydzi@users.noreply.github.com>`), `git init -b main` → `gh repo create tonydzi/<name> --public --source . --push` → tag `v0.1.0` → `git push origin main --tags`. Update claude-bible: the ROADMAP (pain → ✅ shipped as [link]) + the CHANGELOG (a new version, what went in) → push. Verification: `gh repo view` says PUBLIC + `gh api .../tags`.

8. THE CONTENT WAVE: launch /wow with this slice's angle (it handles the rest itself: the episode → the approval chat gate → after a ➕, teasers into the RU and EN chats, a paste-ready Facebook post, a line in the log). The EN longread goes into the repo (docs/); the RU longread is written by the assistant who owns that language.

9. THE TRAIL: a line in the publication log (what → where → the link), a mark in the canon decision (the slice checkbox), a vault reindex if you wrote notes (`brain_embed_update.py`, with --force for canon).

CADENCE: tagged releases on Monday and Thursday; small commits every day as things are ready. The promise is public, and we keep it.

BOUNDARIES: money/commitments/secrets = stop + ask the owner. Vault writes = run `vault_backup.py` first. A slice is cut by value, not for the sake of slicing. The queue of pains and the "what we never open" list (connector logic, the governance protocols of the private half, the persona codex) live in the canon decision.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

---
name: codex-mirror
description: >-
  Rebuild the canon mirror for a second coding agent (AGENTS.md) after a rules-file version
  bump: show the changelog delta, write in only the new rules, then enforce the size cap,
  version stamp, structural anchors, a copy into the shared folder and the linter run. Triggers:
  "/codex-mirror", "update the codex mirror", "AGENTS.md is stale".
license: MIT
---

# codex-mirror — the shared-canon mirror for Codex

The pain (found 2026-07-25): CLAUDE.md went through a v2 revision on 07-22, while `~/.codex/AGENTS.md` quietly stayed on its June version — **Codex worked off stale rules for a month**, and the drift checker of that era was blind to the very same revision. The cure: the mirror is **version-based** (we compare versions, not shape), a watchdog shouts at night, and this skill is the cheap "rebuild" button so that the shouting doesn't turn into evening manual labour.

Roles (AK-47): the **script** moves the bytes and checks everything; **I** only write the text of the new rules. Do not retype the file by hand and do not eyeball the byte count.

Engine: `python %USERPROFILE%\.claude\scripts\codex_mirror.py <check|backup|stamp|publish|selftest>`

## Step 0 — RECALL + the frame
- Memory: [[canon-versioning-and-drift-watchdog]] (the class "the watchdog died silently together with the thing it watched"), [[codex-cli-install]], [[any-llm-vault-actor]], [[claude-md-compression-contract]].
- The mirror = a **canon edit** → only the owner's machine in a live session; followers are receive-only ([[machine-governance-leader-follower]]).
- The 32 KiB cap is hard (DR 06-29: "lost in the middle" — a bloated file is WORSE than an empty one). The mirror = a distillation + pointers, NOT a copy of CLAUDE.md.

## Step 1 — What exactly is stale
```
python %USERPROFILE%\.claude\scripts\codex_mirror.py check
```
Prints both versions, the headroom left before the cap and **the delta from `CLAUDE.CHANGELOG.md`** — exactly the entries that appeared after the mirror's version. That is the work list; you don't need to read all of CLAUDE.md.
- `VERDICT: OK` → leave, nothing to do.
- `PATCH lag only` → green by design; write it in only if the micro-edit changes BEHAVIOUR (thresholds, gates), not wording.
- `REBUILD` → carry on.

## Step 2 — The safety net
```
python %USERPROFILE%\.claude\scripts\codex_mirror.py backup
```
Snapshot into `~/.codex/_backup/AGENTS.md.pre-<version>-<date-time>`. Rollback = copy it back.

## Step 3 — Write in the delta (the only step where I think)
For every delta entry:
1. Find the **matching §** in the mirror (the mirror's numbering mirrors CLAUDE.md's, so canon §8.4 lives in mirror §8.4).
2. Write the rule in the mirror's style: a bold `**§X.Y ...**` + the essence in 1-3 sentences + a pointer to the canon in the vault. Do not copy bodies.
3. A rule about people/the outside world (the house rulebook) — one line with a pointer; a rule about the Claude harness (skills/hooks) — translate into a **principle**, Codex has none of those mechanisms.
4. If the rule is entirely about Codex itself (the reviewer role, Windows pitfalls, protected zones) — its home is the **CODEX BLOCK C1-C6**, not the § part.

⚠️ **Headroom before the cap is tiny** (as of 07-26 — 37 bytes). New material fits only as a trade: squeeze the most bloated paragraph of the SAME § section, don't cut the TOP-20 and don't drop whole rules. Doesn't fit even then → that is the signal for a full mirror revision (as on 07-25: 137 KB → 32.7 KB), not for going "just a little" over the cap.

## Step 4 — Stamp + publish
```
python %USERPROFILE%\.claude\scripts\codex_mirror.py stamp
python %USERPROFILE%\.claude\scripts\codex_mirror.py publish
```
`stamp` rewrites the `> MIRRORS: ...` line from the LIVE canon (version, date, md5, host) — never touch it by hand. `publish` runs the gates (cap · stamp vs canon · 17 anchors `## §0..§10` + `### C1..C6`), then copies into `$IMPORTS_ROOT\codex-canon\`, verifies md5 and runs `lint_agents_mirror.py`. Any FAIL = nothing was copied; fix and repeat.

## Step 5 — Proof and homes
- A live Codex run: `codex exec -s read-only --skip-git-repo-check "quote §<new number> from your instructions"` — does it actually read the new rule.
- External eyes per the /tt rule: `secondop.py t3 --ritual tt` (Codex itself as the breaker) — if the engine changed, not just the mirror text.
- A node that has Codex but is not the hub: run `lint_agents_mirror.py` locally there too (a line in `codex-onboard-checklist.md`).
- The rule changed the collaboration CONTRACT (what Codex may / may not do) → update `~/.codex/CODEX-COLLABORATION.md` + the copy in the shared folder, not only the mirror.

## Boundaries and accepted limitations
- ⛔ Don't edit CLAUDE.md with this skill (that is `/intake` for a rule and `/canon-revision` for structure); the mirror follows the canon, never leads it.
- ⛔ Don't run it on other people's machines: only the owner's hub rebuilds the canon.
- **Accepted:** an edit to the mirror body WITHOUT a stamp change is not caught by the watchdog (receive-only governance keeps that hole closed organisationally). We are not building a second watchdog — [[gate-implement-critical-only]].
- The cap and the anchors are the truth inside the engine's code (`CAP`, `ANCHORS`); a mismatch between code and this text is a bug in the code.
- Relatives: `/arch` (the nightly rail where the watchdog lives) · `/secondop` (Codex as reviewer) · `/canon-revision` (revising the canon itself) · `/follower-onboard` (a new node).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

---
name: canon-revision
description: >-
  Restructure an always-loaded rules file such as CLAUDE.md or MEMORY.md: build a top block of
  key rules plus numbered categories, move rule bodies verbatim with a script that proves zero
  byte loss, fold heavy mechanics into trigger-plus-pointer form, then guards, a canary window
  and fleet rollout. For scheduled maintenance, not ad-hoc trimming. Triggers:
  "/canon-revision", "revise the canon".
license: MIT
---

# canon-revision — revising an always-loaded rules file

The pain: the rules file grows through intake, the structure drifts, and the important parts drown in the middle. The owner's decision (2026-07-22): live in cycles — free growth up to the yellow zone, then a FULL structural revision. This procedure is that revision, battle-tested on CLAUDE.md v2.

Roles: the LLM decides ONLY (a) the mapping of sections into categories, (b) the contents of the TOP block, (c) which sections to fold, plus pinpoint edits from the owner's explicit decisions. The bytes are moved by the SCRIPT, which proves by itself that nothing was lost. Never retype the file by hand.

## Step 0 — RECALL + the frame
- Memory: [[claude-md-compression-contract]] (the contract: trigger · directive · clauses · pointer; the two-ends pitfall), [[write-service-files-tight-no-recompress]], [[memory-index-hygiene]] (for MEMORY.md), [[declined-decisions]] (word-level re-compression = declined).
- Thresholds = the defaults in `~/.claude/scripts/claude_md_guard.py` (owner, 07-22: yellow 100KB · red 120KB). The truth is the guard's code, not the notes.
- A revision = a canon edit → the owner's machine only, in a live session.

## Step 1 — Measure BEFORE
`python ~/.claude/scripts/claude_md_guard.py` + byte size + section counter (`^## ` / `^### `). Record: bytes, sections, md5.

## Step 2 — Coordination and safety net
1. `onair.py check --zone canon-skills` (for MEMORY.md: memory-index) → clear → `onair.py declare --mode exclusive`.
2. `canon_write_gate.py <file>` → GO + an automatic backup; plus your own `*.bak-<date>-revision`.
3. ⚠️ The two-ends pitfall (memory compression-contract): before publishing, verify (a) the md5 of the canon base, (b) the diff of the assembled file against YOUR live file — parallel sessions keep appending through intake.

## Step 3 — Assembly (deterministic)
Take `references/restructure_claude_md.py` (the working sample from 07-22) and adapt the mapping:
- Split by `^## ` headings; every heading must land in the mapping, an extra/missing one = a loud refusal.
- Categories `## §N. <name>` + rules `### §N.M <old heading>`; bodies verbatim.
- The TOP block `## §0. ⭐ TOP-N` — the most important rules by the owner's priorities, one line = a rule + `→ §X.Y`; show the TOP composition to the owner before applying it (or take his previous priorities).
- Pinpoint edits — only from the owner's explicit decisions, each through an anchored replace with assert count==1.
- Built-in check: every body is present in the output (BODY LOST = refusal).

## Step 4 — Threshold control and folds
Guard RED / a fat yellow → structurally fold the fattest PROCESS sections (sample `references/fold_four.py`): what remains is trigger + gist + pointer, and the body must ALREADY live in the house rulebook / memory (verify that the canon exists, otherwise write it there first). Do not fold the owner's top rules without showing him a before→after. Do not re-compress at the word level.

## Step 5 — Verification (the /tt layer)
- Counters: sections BEFORE == AFTER (minus those explicitly deleted by the owner's decision), `### ` = N, TOP lines = N, and the §X.Y links in the TOP point to existing numbers.
- Run the guard again; if it grows past ~87KB — do a live measurement that the harness actually loads the tail (in a FRESH session ask for the contents of the last section; the "89000-byte ceiling" is an unverified legend).
- Optional: the cold-reader test (the recipe is in compression-contract: a fresh cheap model + trap scenarios).

## Step 6 — Publication and homes
1. `publish_canon.py` (for CLAUDE.md); MEMORY.md travels by file sync on its own.
2. New/changed rules → their homes: memory + a MEMORY.md line (+ the house rulebook if the rule is human-executable); `rule_home_guard.py <slug>`.
3. `onair close`, then a before→after report to the owner (bytes, sections, what was folded, how to roll back).

## Step 7 — The "did it get worse" sensor + rollout
- Keep the rollback ready at all times: `Copy-Item <file>.bak-<date>-revision <file>` + `publish_canon.py`.
- 3 days after the revision: a "did it get worse" sensor — a ONE-OFF shadow script written for this specific revision per [[shadow-first-mvp-pattern]] (written from scratch for 3 days, scheduled at night, removed by the time-box — not a permanent component). Metrics: share of 🧒 blocks, timestamps, md5 integrity; degradation >30% = stop/rollback + root-cause analysis; fine = the rollout is justified, put the reasoning into the report. Precedent: the 07-22 revision — the canary measured the ELI5 rate at 80%→77% (= not worse) → the rollout was justified and the canary was killed on schedule.
- The fleet receives it over the canon rail; peers ACK per the bus rule.

## Boundaries
- ⛔ Don't run it on other people's machines / outside the owner's live session (the canon gate will block it anyway).
- ⛔ Don't re-compress words, and don't move bodies into `.claude/rules/` "for auto-loading" — there IS no auto-loading feature (disproved 07-21, memory rule-activation-audit).
- Canon: [[claude-md-compression-contract]] + the house rulebook entry on optimising always-loaded files; the sister rule for MEMORY.md: [[memory-index-hygiene]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

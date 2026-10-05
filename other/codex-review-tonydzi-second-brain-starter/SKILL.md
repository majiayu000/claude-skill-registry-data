---
name: codex-review
description: >-
  Cross-vendor code review: this agent reviews the other agent's diff and the other agent
  reviews this one's, so the final check always comes from a different model. Verdicts are
  APPROVE or REQUEST_CHANGES with file:line references. Triggers: "/codex-review", "cross-review
  this diff", "have the other vendor check this".
license: MIT
---

# codex-review — "Claude checks Codex"

A thin broker for the review pair. Codex writes the code; Claude reviews its diff independently. (The old note "`codex exec` headless hangs on Windows" is obsolete: on codex-cli 0.141+ headless works natively — verified 2026-07-07 on the laptop and 2026-07-14 on the hub.) File handoff, no shared credentials, subscription (not a paid API).

## When to run it
The owner made a change through Codex (or there is simply a diff/edit in a repository) and wants an independent "second pair of eyes" check. Triggers: see `description`.

## What I do
1. **Identify the target.** Ask for / take the path to the repository where Codex made the change (or the path to a patch file). Default — the working repository the owner named.
2. **Run the engine** (deterministic, 0 of my tokens for the run itself — the review is done by headless `claude -p`):
   ```
   python "%USERPROFILE%\.claude\scripts\cc-review\cc_review.py" --repo "<path to repo>" --model sonnet
   ```
   - model: **Sonnet by default** (the free subscription bucket; in the test it caught both bugs in 25s); **Opus** for hard/safety-critical changes (`--model opus`) — the quality gate.
   - other modes: `--range "HEAD~1 HEAD"` (a specific commit), `--diff "<patch.diff>"` (a ready patch), `--task "<task.md>"` (what Codex was asked to do — gives the reviewer context).
3. **Report to the owner:** the verdict (`APPROVE` / `REQUEST_CHANGES`), the list of findings (file:line · severity · what is wrong · the fix), and the path to `review-<ts>.md`. If REQUEST_CHANGES — propose fixing the root cause (not the symptom).

## Boundaries
- The engine forcibly unsets `ANTHROPIC_API_KEY` → the review runs on the subscription, not on a paid key.
- A giant diff is truncated to 120k characters (with a note) — if you hit that, review it in parts / per file.
- This is a REVIEW, not an auto-fix: fixes are proposed/made separately per AK-47 (easy and reversible — do it yourself; a fork — ask).
- The full auto-pair (Codex headless as well) can be built later under WSL2/Docker — a separate step (not needed now).

> **2026-06-28 (hub):** the engine `cc_review.py` was lost (not in git / `.stversions` / on any disk) → **rebuilt** as a simple Windows-native "normal mode" (the call above). Run live (`/tt`): bugs → `REQUEST_CHANGES`, clean → `APPROVE`, empty/not-a-repo → graceful. Artifacts live outside the vault (`reviews/`), counter `reviews/_log.jsonl`. ⚠️ Canon update in [[decision-hermes-multivendor-arbitrage-rejected]] (addendum 06-28).

## ⭐ The two-way hetero pair (both sides run on the hub)
Full symmetry: both sides review each other, and the final check is always done by the OTHER vendor.
- **Claude → reviews Codex** (forward) — WORKS: `python "%USERPROFILE%\.claude\scripts\cc-review\cc_review.py" --repo "<repo>" --model sonnet` (see above).
- **Codex → reviews Claude** (reverse, the mirror) — WORKS ON THE HUB TOO: `python "%USERPROFILE%\.claude\scripts\cc-review\codex_review.py" --repo "<repo>"` — the engine was /tt-verified 2026-07-07 (laptop, codex-cli 0.141.0) and 2026-07-14 (hub, codex-cli 0.144.4: `npm i -g @openai/codex`, the ChatGPT-subscription login was already in `~/.codex/auth.json`; smoke: planted bugs → REQUEST_CHANGES with exact file:line in 16s · clean diff → APPROVE · empty diff → graceful without calling Codex). Native `codex exec -s read-only` on Windows without WSL2. Flags: `--range "HEAD~1 HEAD"`, `--diff <patch>`, `--task <task.md>`, `--timeout 300`. Read-only sandbox: Codex only reasons over the diff. Output: `review-codex-<ts>.md` + `VERDICT: APPROVE|REQUEST_CHANGES`.

## Full auto mode under WSL2 (archived path — NOT deployed on the hub)
⚠️ The orchestrator `codex_pair.py` is missing from the hub's live tree (it survived only in the snapshot `_config-backup\snapshot-2026-07-04`), and WSL2 is not installed there → the mode does not start. To bring it up: restore `codex_pair.py` from the snapshot + install WSL2/Codex, then `/tt`.
Historical context (the machine where it was built, 2026-06-22): WSL2 Ubuntu-24.04 + Node22 + Codex 0.142.3 (logged into ChatGPT), `codex exec --full-auto` headless. What it did: Codex implements the task headless inside WSL → takes the git diff → Claude reviews it (`cc_review.py`) → verdict + `codex-change-*.diff` + `review-*.md`. The repo lived in the WSL Linux filesystem (`/root/...`); a path normalizer fixed the Git-Bash `/root/...` mangling.

## Extension — the reverse side is READY (the hub has been fully two-way since 2026-07-14)
The reverse side (Codex reviews Claude) is built = `codex_review.py` (see the "two-way hetero pair" block), native `codex exec` on Windows. The Codex CLI was installed on the hub 2026-07-14 (`npm i -g @openai/codex`, v0.144.4, login via the ChatGPT subscription) and the smoke test passed — the hetero pair works in both directions. The same day it was also deployed to the anchor VPS (headless: `auth.json` is copied over with scp, no browser OAuth needed; both engines + smoke ✅) — the anchor is an extra node, and live duo tests still run from the hub in the review chat.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

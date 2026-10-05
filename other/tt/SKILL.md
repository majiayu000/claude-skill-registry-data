---
name: tt
description: >-
  Quality gate immediately after building: prove that what was just built actually works, while
  the context is still hot. Six steps: scope what changed, run live on real data, break it on
  purpose, show a counter or log proving it ran, root-cause any failure and re-run, then a
  verdict with evidence. Only a green verdict earns the word done. Supports an external
  multi-vendor review panel as a mid-step. Triggers: "/tt", "/test", "prove it works", "test
  what we built".
license: MIT
---

# /tt — the quality gate right after building

> 🧒 **When reporting to a non-technical operator:** end with a short "In plain words" recap in their language (standing rule [[eli5-always]]). Only in the message TO them — never inside artifacts.

This is **not a retrospective**. Retro = packaging the whole session at the end. `/tt` = a narrow check of **the one thing we just built**, while the context is hot. The pain that created it (2026-06-25): "we built it, said 'done', moved on — and it was only 2/3 finished." `/tt` catches that BEFORE the word "done".

**When:** immediately after building/editing a **skill · script · routine · hook · vault pipeline · mechanism note** — anything that is supposed to DO something. Not for conversational replies and not for trivial text edits.

**Boundary vs neighbors:** `/1` = is the SYSTEM alive after a crash; a browser verify = does the APP work; `/tt` = does **the exact thing we just built** work.

---

## Step 0 — RECALL the scope (what did we actually change)
Not from memory — from facts. List what this task really created/touched:
- fresh/modified files: `~/.claude/skills`, `~/.claude` (memory/CLAUDE.md/hooks/scheduled-tasks), `$IMPORTS_ROOT`, vault notes;
- quick anchor: `python "$IMPORTS_ROOT/retro_inventory.py" 1` (the same inventory the retro skill uses) OR simply list what you edited in THIS session.
- Take only what belongs to the CURRENT task (ignore other machines' fleet edits — not ours, see [[session-machine-tagging]]).
- **RECALL existing knowledge on the topic** (a gate born from a real miss on 2026-07-04: we fixed a pipeline without checking memory first and nearly duplicated a parallel session's work): before running/fixing, pull up what is ALREADY known — grep the memory folder + semantic search + grep the vault for the changed area. A parallel session may have already done/documented it ([[capture-rules-into-bible]] → RECALL-before-activity).

## Step 1 — RUN it live (on real data, not in theory)
Run the thing **for real** on real data and show actual output:
- a skill → execute its procedure by hand right here;
- a script → run it (read-only/dry-run if it has side effects);
- a routine/hook → trigger it manually or verify it actually fires (not "it should");
- a rule note → check that links/slugs resolve and the frontmatter is valid.
"Works in theory" ≠ proven. You need live output.

## Step 2 — BREAK it on purpose (negative + edge cases)
Try to break it — the classic local pitfalls:
- empty / malformed input, missing dependency or key;
- wrong-drive path pitfalls ([[deterministic-script-gotchas]]) — does it look on the right disk;
- machine-specific hardcode: `grep -n "C:\\\\Users\\\\[^_]" <file>` — a path with ANOTHER user/machine inside a shared engine must go through a paths module / machine env (real case 2026-07-04: the hub baked `%USERPROFILE%` in, the path was dead on the laptop → silent fallback);
- stale config / API-version drift — does it read facts from the LIVE source, not a stale copy ([[recall-first-on-incident-and-live-source-truth]]);
- does it degrade gracefully (clear error) instead of failing silently or quietly "pretending".

## Step 2.5 — SECOND OPINION: an external breaker (multi-vendor panel)
Your own check is blind to your own blind spots — a second vendor catches what we can't see ([[test-after-build-skill]]). So it's not only the session that tries to break the artifact; external eyes do too. There are THREE pairs: **Codex** (headless CLI, default), **Grok** (local CLI rail on subscription — `secondop.py t3 --engine grok`; the grok.com browser is the FALLBACK), and **Gemini** (headless, `gemini_review.py break`).

**When to call it (narrowly, so the ritual doesn't bloat):** the Step-0 scope contains a changed **executable** artifact (script · skill · hook · routine · pipeline). Notes/texts/frontmatter only → skip **explicitly**, log it, and state it in the verdict.

**Rail 1 — Codex (default, always called first):**
```
python "%USERPROFILE%\.claude\scripts\cc-review\secondop.py" t3 --ritual tt --task <task-id> --context "<what we built + what steps 1-2 already checked>"
```
A peer machine without a Codex login → the same call through `_shared\secondop_client.py` (a broker replies over the machine bus).

**Rail 2 — the Grok breaker (call when):** (a) Codex is unavailable/quota-blocked — Grok saves the verdict from ⚠️; (b) the artifact is risky/safety-critical or Codex gave a contested COUNTER — hetero-pair, call BOTH; (c) the operator says "ask Grok".
**Default mechanics: local headless CLI** — `python ...\secondop.py t3 --engine grok --ritual tt --task <id> --context "..."` (logging and the human-visible mirror are automatic). CLI dead/logged-out (`grok doctor`) → **browser fallback** (live-tab automation, human pace, strictly a local browser):
1. `python ...\secondop.py grok-prompt --task <id> --context "<what we built + what we checked>"` → paste-ready prompt;
2. paste into a NEW grok.com chat, wait for the reply;
3. the first line of the reply = the verdict `ACCEPT`/`COUNTER`/`BLOCK`;
4. log it: `python ...\secondop.py log-ext --reviewer grok --task <id> --ritual tt --verdict "<line 1>" --note "<grok.com/c/… link FIRST + gist of findings>"`. The chat link in `--note` is **mandatory and goes first** (the note is truncated to 200 chars — a long preamble eats the link) — it proves the verdict really came from Grok and wasn't typed in by hand; the full Grok reply is also quoted in the /tt verdict. Unrecognized format → the verdict does NOT count (re-ask in the format, or log-skip).

**Rail 3 — the Gemini breaker (call when):** (a) Codex AND Grok are unavailable/out of quota — Gemini saves the verdict from ⚠️; (b) a safety-critical artifact or a contested COUNTER — a third voice; (c) the operator says "ask Gemini".
```
python "%USERPROFILE%\.claude\scripts\cc-review\gemini_review.py" break --task <id> --context "<what we built + what we checked>"
```
Headless, no browser (REST rail ~7-10 s; `--engine cli` = the official CLI). Verdict on the first line `ACCEPT`/`COUNTER`/`BLOCK`, and it logs ITSELF into `usage.jsonl` — no manual log-ext needed. Rail didn't answer → the script logs `log-skip` itself and exits with code 3 (the /tt verdict is then at most ⚠️ PARTIAL). The key = a free API tier with no billing attached → overuse = 429, not a bill.

**How to read the reply (all three rails):** `COUNTER`/`BLOCK`/break-scenarios = a **finding** → that's Step 4 (root cause → fix → re-run), not "an opinion to note". `ACCEPT` = agreement, no finding. ONE received external verdict is enough; a second pair of eyes per Rail-2 rules.

**Skipping — only explicit, never silent** (a reviewer COUNTER taught us this): both rails unavailable / no executable artifacts →
```
python ... secondop.py log-skip --ritual tt --task <id> --reason "<quota|error|no executable artifacts>"
```
and the Step-5 verdict **cannot be ✅** for that reason: at most **⚠️ PARTIAL "no second opinion received"**. A missed call ≠ a green test. Exception: the artifact is non-executable — then the skip is neutral and ✅ is possible.

**Observability:** every call/skip is written to `bridge-state/usage.jsonl` (attempted · ok · skipped · finding); a daily digest goes to the fleet log chat. Zero calls in a day = the signal "the ritual is not working", not silence.

## Step 3 — the VISIBILITY layer (can you even see that it worked?)
The most common silent bug is not in the core but in the fact that **the result is invisible** ([[verify-existing-before-proposing]]):
- **Existing gate first:** if the thing under test has ITS OWN deterministic gate/test (a guard script, a system-map check, a sync check, `_test_*.py`) — run THAT and take ITS verdict; do not re-derive the logic with homemade awk/grep — a duplicated gate drifts from the original over time and produces false/diverging alarms (real case 2026-06-27/07-04: a raw awk and the real guard measured line lengths differently);
- is there a counter/log/proof line showing it ran?
- "LastResult=N with no logs" = undebuggable → that's a ❌ on visibility even if the core looks fine. (This is how an empty state ledger and a false-RED sync were caught.)

## Step 4 — ROOT CAUSE → fix → re-run
Any failure in steps 1-3 → dig to the ROOT ([[fix-root-cause-not-symptoms]]), don't patch the symptom; fix the CLASS → go back to Step 1 and re-run until clean. Safety-critical (locks/sync/auth/scheduler/idempotency) → "read before you fix" + a mini-test ([[verify-existing-before-proposing]]).

## Step 4.5 — SESSION SPLIT: count the signals (shadow rule)
You found a bug in steps 1-3 and it doesn't fix quickly — before digging in, count 4 signals and **log them**:
```
python ~/.claude/scripts/split_rule.py log --what "<what we're fixing>" --attempts <failed attempts> \
   --files <files in the root cause> --repro-min <minutes to reproduce> --context-pct <% of context> \
   [--shared] --decision stay|split --minutes <total> --note "<comment>"
```
The rule (still a shadow — the decision is yours): split into a separate session if ANY signal fires —
**A** ≥2 failed attempts · **B** the root spans >2 files or touches an adjacent system (bus/canon/scheduler/auth) ·
**C** reproduction takes >10 min · **D** ≥70% of the context is consumed.
If you split — a seed prompt is mandatory (what we did · what we achieved · what was already rejected and why · acceptance criterion · non-goals), a task goes into the task registry, and the artifact is marked ⚠️, not ✅. A shadow with no log entries = the rule was NOT tested; summary via `split_rule.py summary --days 14`.

## Step 5 — VERDICT with evidence
A short table: **what was checked · how (live output) · ✅/⚠️/❌**. Then one summary line:
- ✅ **PASS** — ran it, broke it, visible — works. ONLY this = "done".
- ⚠️ **PARTIAL** — works, but there's a yellow flag (name it + what remains).
- ❌ **FAIL** — doesn't work / isn't visible → root cause + what I'm fixing.
Evidence (output/counter/screenshot) is mandatory — without it a "✅" doesn't count.

**📋 Task journal:** verdict ✅ = the moment the item closes in the task registry ([[task-journal-done-undone-linking]]): if the verified thing is in the registry — mark it `done` with THIS evidence + link what it unblocked; ❌/⚠️ = the task stays open (the "finish fixing X" tail goes into the registry immediately). From a machine without the engine — send TASK/DONE over the machine bus. One line in the report: "📋 journal: #id → done (evidence: …)".

---

## Link with the retro (audit, not a duplicate)
`/tt` tests per task (hot). The retro at the end of the session only **AUDITS** the "tested? ✅/❌" line for each artifact and, if ❌ — flags it and offers to run `/tt` now. The retro does NOT do the check itself (too late/cold). No duplication: each layer references downward (simplicity-first).

## Boundaries / non-duplication
- markdown-only thin orchestrator; NOT a server/DB/webhook (if you truly need more than markdown — raise a ⚠️ COMPLEXITY flag, the operator decides).
- read-only/dry-run where side effects exist; vault writes — backup-first ([[vault-backup-rule]]).
- If the session built nothing — say plainly "nothing to test", no ceremony.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

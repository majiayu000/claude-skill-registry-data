---
name: alpha-judge
description: >-
  LLM-judge stage of an alpha-mining pipeline: take a miner's deterministic candidate list, keep
  only real signal, drop noise, and propose additions to that miner's curated note. Use after
  any zero-token detector run. Reads only the candidate digest and the home note, never the
  corpus. Triggers: "/alpha-judge <miner>", "judge the candidates".
license: MIT
---

# 🅰️⚖️ /alpha-judge — the reusable LLM-judge for every alpha miner

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language (their standing request; reports TO the operator only).

The alpha-extraction engine = **cheap deterministic detector (0 tokens) → LLM judge → weekly ≤10 + yes/no calibration**, repeated for each of the 10 miners. The DETECTORS are per-miner scripts in `$IMPORTS_ROOT/alpha/`. The JUDGE is the SAME logic every time — so it lives HERE, once, and is reused. Canon: `02-Decisions\decision-alpha-extraction-engine-variant-a`; memory [[alpha-extraction-engine]].

## Model policy (per [[model-routing-sonnet-grunt]] + the operator's 2026-06-14 session override)
- **In-session, now:** judge on **Opus** (the operator steers; he'll say when to switch to Sonnet as Opus nears its limit).
- **Nightly unattended:** **Sonnet** (idle free bucket) via `judge_nightly.cmd` (headless `claude -p --model sonnet`). LIVE + verified 2026-06-15 — Windows task "Alpha Judge Nightly" Mon 05:00, chained after the 04:15 scan. **Now judges ALL 10 miners** (was bets-only; expanded 2026-06-15) — one headless session reads THIS spec, loops the registry, applies the dedup-vs-home gate, writes each `<miner>-judged-latest.md`. **Vault writes are forbidden in nightly mode** (judge-only; home-note additions wait for the operator's in-session approval). (Auth is in the Windows keychain; check with `claude auth status`, re-login via `claude auth login`. Keep `.cmd` pure-ASCII.)
- The judge is grunt-classification → Sonnet is the natural default once the session-override lifts.

## Miner registry (detector → home → verdict scheme)
| miner key | candidates file (in `_imports\alpha\candidates\`) | ledger db | curated HOME note (feeds, never duplicates) | verdict scheme |
|---|---|---|---|---|
| `bets` | `bets-report-latest.md` | `bets_ledger.db` (table `bets`) | `insight-prediction-ledger` | ✅ came true · ❌ did not · 🔁 still open · 🗑 not a bet |
| `contradictions` | `contra-report-latest.md` | `contra_ledger.db` (`pairs`+`claims`) | `insight-contradictions` | ✅ a real contradiction · 🟡 an evolving opinion · 🗑 noise |
| `stance` | `stance-report-latest.md` | `stance_ledger.db` (`shifts`+`pairs`) | `insight-contradictions` (§ "willing to change my mind") | ✅ a real shift of view (was A → now B) · 🟡 a refinement, not a shift · 🗑 noise |
| `bridge` | `bridge-report-latest.md` | `bridge_ledger.db` | `insight-worldview-throughlines` | ✅ a non-obvious, valuable bridge between domains · 🟡 an expected link · 🗑 an accidental co-mention |
| `recurring` | `recurring-report-latest.md` | `recurring_ledger.db` | `insight-worldview-throughlines` | ✅ a genuine recurring conviction · 🟡 an operational repeat · 🗑 co-frequency of filler words |
| ~~`leadsignal`~~ ⛔ RETIRED 2026-07-16 | `leadsignal-report-latest.md` | `leadsignal_ledger.db` | 42.9% precision on the owner's gold set (111🟡/27🔴, 2026-07-05) — leads belong in `/pipeline`, not in the insight feed. The script stays on disk but is disabled in weekly/judge/harvest | — |
| `novelty` | `novelty-report-latest.md` | `novelty_ledger.db` | `insight-novelty-ideas` (CREATE it on the first ✅) | ✅ a genuinely new idea · 🟡 a variation on something known · 🗑 rare words with no idea behind them |
| `identity` | `identity-report-latest.md` | `identity_ledger.db` | `_Self-Bible-MOC` (+ `concept-*` "what I think") | ✅ a real self-definition (a value/principle) · 🟡 situational · 🗑 not about identity |
| `openq` | `openq-report-latest.md` | `openq_ledger.db` | `insight-open-questions` ✅ (created 2026-06-15, 25 questions; +226 from Detector-A pending) | ✅ a real open question of the owner's · 🟡 rhetorical · 🗑 someone else's / boilerplate |
| ~~`orphan`~~ ⛔ RETIRED 2026-07-16 | `orphan-insight-report-latest.md` | `orphan_insight_ledger.db` | 37.5% precision on the owner's gold set — the misses were the team's working protocols in `05-Resources` (an evidence layer where being unlinked is normal). Orphan insights are caught by `/relink --deep`. The script stays on disk but is disabled in weekly/judge/harvest | — |

## Flow (what YOU do)
1. **Pick the miner** from the arg (default `bets` if none; if unclear, ask). Read its candidates file (or query its db for the top unjudged candidates — cap ~25; never the whole corpus).
2. **RECALL the HOME note** (e.g. `insight-prediction-ledger` / `insight-contradictions`) so you DON'T re-propose what's already catalogued. Token-cheap: read only that one note + the candidate digest.
3. **JUDGE each candidate** against the miner's core question — *"is this ANTON'S OWN <X-of-the-right-type>, not noise / not someone else's / not a restatement?"* Classify per the verdict scheme + a ONE-line reason. The detector optimises RECALL; the judge supplies PRECISION.
   - **🛡 DEDUP-VS-HOME GATE (mandatory — added 2026-06-15):** before you KEEP a candidate, check it against the HOME note you recalled in step 2. If the candidate merely **restates** something already catalogued there (same belief / value / bet / question / shift / bridge — even if worded differently), DROP it with the verdict **🗑 already in the home note (restatement)**. Only candidates that add something the home note does NOT already contain survive. This is a semantic check (you, the judge, do it — NOT a blind word-overlap filter, which would false-drop real nuance). *Why:* on 2026-06-15 the `identity` (11 raw keeps → 0 truly new after dedup) and `stance` miners re-proposed items already in `_Self-Bible-MOC` / `insight-contradictions`; this gate makes that dedup a required step, not a manual afterthought.
4. **Write the clean signal** → `_imports\alpha\candidates\<miner>-judged-latest.md` (utf-8, `\n`): only the ✅/🟡 keepers, each with quote(s), source `[[wikilink]]`, date if known, verdict, reason. If zero signal, say so plainly (that's a valid, honest result — don't invent).
5. **Propose HOME additions** (the keepers not already in the home note): show the operator **BEFORE→AFTER** ([[show-before-after]]); on their OK → `vault_backup.py` first ([[vault-backup-rule]]) → append to the home note (draft status, they edit) → recalc if the home has an engine (bets → `ledger_calibration.py`). **Never auto-write a curated vault note.**

## Guardrails
- **Token-economy ([[vault-data-architecture]]):** judge reads ONLY the candidate digest + the one home note. NEVER load the corpus. The detector already did the 0-token narrowing.
- **Honesty over yield:** "0 real" is a legitimate verdict (contradictions hit it 2026-06-14 — the operator is consistent + already has the curated map). Don't manufacture signal to look productive.
- **No new ledgers:** every miner FEEDS a pre-existing curated home (bets→prediction-ledger, contradiction→insight-contradictions). Surface NEW candidates; don't duplicate the home.
- **Vault writes** = backup → preview → approve → reindex. Concurrent-git aware: if the vault `index.lock` is held by live git, defer the write and say so.

## Not this skill
Building/refining a DETECTOR script = direct work in `_imports\alpha\` (not here). Running the deterministic scan = the miner's own `.py` / weekly task. This skill is ONLY the judge + home-feed stage.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

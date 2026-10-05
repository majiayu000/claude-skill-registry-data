---
name: declined
description: >-
  Look up the registry of declined and deferred decisions, so the same idea is never re-pitched:
  what was rejected, why, and under what condition to revisit. Read-only, and can also run the
  detector for new rejections in recent sessions. Triggers: "/declined", "did we reject this
  before".
license: MIT
---

OBJECTIVE: Show the registry of declined/deferred decisions (what · why · revisit-if) BEFORE (re-)pitching an idea — the anti "step on the same rake twice" guard. READ-ONLY: it writes nothing into the registry (the nightly scan and the human do that).

CONTEXT:
- The canonical registry (this hub): `%USERPROFILE%\.claude\projects\<hub-project>\memory\declined-decisions.md` (a copy exists in the laptop project — always read the hub one).
- The nightly detector: `$IMPORTS_ROOT/declined-scan/declined_scan.py` (scheduled task "Declined-Decisions Nightly Scan", ~03:45) — it catches new refusals from fresh sessions and parks them on the AUTO-CAPTURED shelf.
- The rule (cross-actor): rejected or deferred a proposal → record it in the registry. The canon for human assistants lives in the Bible as the "record a rejected decision" rule.

STEPS:
1. Read `declined-decisions.md` (the hub path above).
1b. **Dead-man check on the watchdog** (added 2026-07-04; catches the class "the task was silently disabled", as happened 06-22→06-27): read `$IMPORTS_ROOT/declined-scan/highwater.json` → if `updated` is older than 2 days the nightly watchdog is NOT running → check `(Get-ScheduledTask -TaskName 'Declined-Decisions Nightly Scan').State`, enable it (`Enable-ScheduledTask`), and report in one line. Fresh → move on silently.
2. If the operator asked about a SPECIFIC topic — grep the registry for it and show the matches (what was rejected · why · under what condition to revisit).
3. Otherwise — a short summary: how many entries, the most recent additions, and the AUTO-CAPTURED shelf (waiting for promotion).
4. (Optional, on "run the scan") execute `python $IMPORTS_ROOT/declined-scan/declined_scan.py` and show the newly caught refusals.
5. If the idea being pitched right now is ALREADY in the registry — warn the operator explicitly ("this was declined on <date>, reason X, revisit if Y") before going further.

OUTPUT: a short list of relevant refusals, or a registry summary. It writes NOTHING (except step 4, where the scan writes for itself). Finish the reply to a non-technical operator with an "In plain words" recap.

RELATION (do not duplicate): the source registry = memory [[declined-decisions]]; the nightly scan = `declined_scan.py`; the rule for humans = the Bible entry on recording rejected decisions.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

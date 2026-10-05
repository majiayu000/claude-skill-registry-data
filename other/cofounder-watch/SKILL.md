---
name: cofounder-watch
description: >-
  Watch a live lead funnel with a zero-token dispatcher and surface salient events as short
  advice: replied but no scheduling link, link sent with no booking in 24h, awaiting reply.
  Deduped so it never nags twice, and read-only. Triggers: "/cofounder-watch", "what does the
  cofounder see", "funnel signals".
license: MIT
---

# /cofounder-watch — Phase 0 ambient cofounder (ping-only)

> 🧒 **When reporting to a non-technical operator:** finish with a child-simple "In plain words" recap in their language. Not inside the cofounder advice itself.
> 📖 Canon: [[decision-realtime-cofounder-2026-07-02]]. This is the **EYES + filter** of the real-time cofounder (Phase 0). It sends nothing — it only highlights.

## What it does
A deterministic `signal-dispatcher` (0 tokens, stdlib only): reads the live funnel `tg_followups.json` → classifies salient events (the same rules as `/pipeline`) → dedups through `cofounder_ledger.json` (never pings twice) → writes a digest + an HTML dashboard. **Silent when there are no new important events** — that is the whole point: do not nag.

## How to run
`python "$IMPORTS_ROOT/cofounder/cofounder_watch.py" --stdout`
- Flags: `--stdout` (print the digest), `--reset` (clear the ledger → re-alert everything).
- Outputs: digest `$IMPORTS_ROOT/cofounder/cofounder-digest.md`; dashboard `$OBSIDIAN_VAULT/_Dashboards/Cofounder-Watch.html` (the operator works visually).

## Salience (rules = /pipeline priority)
- 🔥 **HIGH** — they replied, Calendly NOT sent → "send the Calendly now".
- ⏰ **MEDIUM** — Calendly sent >24h ago, no booking → "booking nudge".
- 👀 **LOW** — pitch sent, no reply → "check inbound / follow up / drop".
- booked/confirmed → skipped (we do not re-pitch).

## Boundaries (Phase 0)
- **Ping-only** — it NEVER messages leads. Actions are executed by the operator (or via `/pipeline` draft→approve). Human in the loop.
- **0 tokens** — the advice is templated from the rule. The LLM persona `/cofounder` for nuance is Phase 0.5 (later, HIGH events only).
- Empty ≠ broken: "silent" is a valid result.

## Next (Phase 0.5 / 1+, on the operator's greenlight)
- Delivery into a Telegram signal chat (once the MCP is alive) instead of a file + dashboard only.
- Scheduling on the HUB (always-on `HUB-1`) 2-3x/day — this is background work, so it belongs on the hub, not the laptop, via `/schedule` on the hub or the machine bus. Being lightweight (0 tokens), daytime runs are fine.
- Phase 0.5: HIGH events → the LLM persona `/cofounder` (top model) for nuanced advice.
- Phase 1: + urgent VC email + calendar conflicts (same mailbox + ledger).
- To extend it, add a source to the SAME dispatcher; do NOT breed watchers ([[telegram-eventloop-listener]]: one live client, the AUTH_KEY pitfall).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

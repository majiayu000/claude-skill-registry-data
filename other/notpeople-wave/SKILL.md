---
name: notpeople-wave
description: >-
  Run an investor-outreach wave end to end: assemble the batch of targets, personalize pitches
  from real templates, send from the designated account, and log every touch in the CRM. Walks
  the exact checklist with rate limits and dedup against everyone already contacted. Triggers:
  "/notpeople-wave", "next outreach batch".
license: MIT
---

# /notpeople-wave — next NotPeople investor outreach wave

> 🧒 **When reporting to the operator** (status/summaries — NEVER inside the pitches themselves): end with a child-simple "In plain words" recap in their language. Standing request, memory `eli5-always`.

> 📖 **Operates under `telegram-lead-outreach`** (the general Telegram outreach playbook) and the `bible` outreach domain. This skill only adds the NotPeople-specific sequencing + the dedup-ledger discipline. Don't duplicate guardrails — they live there; newer rule beats older.

**What this is.** NotPeople = a $600K pre-seed SAFE raise pitched to ranked crypto/VC investors over Telegram from **@work_acct_a**. Nina is the live lead operator; this (follower) machine runs the sends. Project memory: `notpeople-outreach-waves`. Pipeline lives in `$IMPORTS_ROOT\notpeople\` (on the hub: `$IMPORTS_ROOT/notpeople/` — drive-agnostic scripts).

**The two bugs this skill exists to prevent (25 Jun 2026):**
1. The 22 Jun wave was **never appended to `NotPeople-Pitched.csv`**, so `select_next_investors.py` kept proposing already-pitched leads.
2. Sending blind from the ranked queue → duplicate sends, a wrong name (draft "Mei" → actually Alex), and dead handles.
The fix is baked into steps 2 and 5 below: **read each lead's live thread before sending**, and **append the wave the moment it's sent**.

---

## The wave checklist

### 0. RECALL (cheap, first)
- Read memory `notpeople-outreach-waves` (pipeline + the gotcha) and `leads-live-operator-check-thread`.
- Confirm which machine you're on. **Follower (Nina, vault on D:, receive-only):** local CSV/dashboard edits may be reverted by Syncthing → you MUST also relay the pitched-record to the hub (step 6). **Hub (`HUB-1`):** you are the source of truth, no relay needed.

### 1. Select the next N truly-new investors
- Default N = 10 (operator may say a number). The operator may name leads to **skip** (e.g. "skip Karim") → drop them, pull the next-ranked to refill N.
- Run the selector: `python "$IMPORTS_ROOT\notpeople\select_next_investors.py"` (reads the scored pool, excludes anyone already in `NotPeople-Pitched.csv`).
- ⚠️ **The ranked queue is contaminated** — its top was already pitched 22 Jun. Do NOT trust queue position alone. Treat the selector output as *candidates*, then verify each in step 2. If the top is all already-contacted, scan deeper (positions 23+ were clean on 25 Jun).

### 2. Verify EACH candidate against the live thread (the rule that saved us)
For every candidate, before composing anything:
- `resolve_username(@handle, account="work_acct_a")` → **GEN-ERR-659 = dead/changed handle → drop it**, refill from next-ranked.
- `get_history(<chat>, account="work_acct_a", limit=…)` → read the actual thread.
  - Already pitched / mid-conversation → **drop** (it's a duplicate; if it was pitched but not in the CSV, note it for the backfill in step 5).
  - Name mismatch between the draft and the real Telegram display name → **fix the name** (the "Mei"→"Alex" bug).
  - Clean / no prior contact → keep.
- Assemble the final N truly-new, name-correct leads. **Report the list to the operator and WAIT for "+"** before sending (outbound = Tier-2, ask-first).

### 3. Compose + send (Opus voice, per lead) — only after "+"
- Pitches come from `build_pitch_drafts.py` (50 personalized, ranked) — `python "$IMPORTS_ROOT\notpeople\build_pitch_drafts.py"` writes `pitch_queue.json` + a drafts note. Top-N = the batch. Personalize per lead; **@work_acct_a = the operator's personal voice → Opus**, no copy-paste blast, pace the sends ([[telegram-lead-outreach]] guardrails).
- The standing pitch BODY (NotPeople, $600K pre-seed SAFE, Calendly close) lives in `build_pitch_drafts.py` — reuse it, don't rewrite the offer.
- `send_message(<chat>, <text>, account="work_acct_a")` per lead.

### 4. Verify delivery per-lead (don't assume)
- After the batch, `get_history(<chat>, account="work_acct_a", limit=1)` for each → confirm the outbound msg landed (capture msg_id + timestamp). Report "N/N delivered" with the ids. This is the "are you sure it actually went out?" check — do it without being asked.

### 5. Record the wave IMMEDIATELY (the dedup ledger — never skip)
- Append every sent lead to `NotPeople-Pitched.csv` (in `_Dashboards`), columns `Lead name,Username,Company`.
- **Also backfill** any lead you found in step 2 that was clearly pitched earlier but missing from the CSV (this is exactly the 22 Jun gap). The CSV is the single dedup source `select_next_investors.py` reads — if it's stale, the next wave re-pitches people.

### 6. Refresh the tracker snapshot + (follower only) relay to hub
- Edit the inline wave list in `build_notpeople_tracker.py` (new wave kept as its OWN section, OUT of the waves-1+2 funnel, so reply-rate stays honest), then `python "$IMPORTS_ROOT/notpeople/build_notpeople_tracker.py"` (hub `E:`; follower `D:`). This rewrites `tg_followups_notpeople.json` + `tg_assistant_log_notpeople.jsonl` — the tracker schema the outreach/pipeline dashboard reads.
- Open the outreach view for the operator with a **cache-bust** query so a stale browser tab doesn't hide the update: `_Dashboards\NotPeople-Outreach-Dashboard.html?v=<ts>` (static snapshot — hand-edit its wave section if you need it visually current).
- **Follower machine:** relay the pitched-record to the hub so the real dedup lands there too: `python "%USERPROFILE%\.claude\scripts\machine_bus.py" send HUB-1 "NotPeople wave <date>: appended N rows to Pitched.csv (<handles>); prune dead handles <…> from pool."`

### 7. Report (tight, ELI5 at the end)
Operator-facing: N sent + N/N delivered (with ids), N dropped (dups/dead handles), CSV +rows, dashboard refreshed, hub relay sent. Then the 🧒 recap.

---

## Guardrails (inherited, not re-implemented)
- Outbound = **Tier-2 / ask-first**: assemble + report the batch, send only on the operator's "+". NO mass auto-blast; pace the sends. (money/commitments/secrets → pause + ask — [[telegram-lead-outreach]], [[telegram-assistant]].)
- **HUB never messages leads** — leads are worked by the live operator (Nina). On the hub, this skill prepares/records but does not send. ([[leads-live-operator-check-thread]].)
- No em/en dashes anywhere (memory `no-long-dashes`).

## Files & values (reuse, don't recreate)
- Send account: `@work_acct_a` (work_acct_a, Tony SF / Bay Area).
- Pipeline: `$IMPORTS_ROOT/notpeople/` (hub `E:`; follower `D:`) — `select_next_investors.py`, `build_pitch_drafts.py`, `build_notpeople_tracker.py` (snapshots wave state into the tracker JSON the dashboard reads; drive-agnostic).
- Dedup ledger: `_Dashboards\NotPeople-Pitched.csv`. Dashboard: `_Dashboards\NotPeople-Outreach-Dashboard.html`.
- Offer: $600K pre-seed SAFE · deck `notpeople.ai/pitch` · Calendly `https://calendly.com/paloaltolab/1-on-1`.
- GEN-ERR-659 = dead/changed handle. machine_bus relay target = `HUB-1`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

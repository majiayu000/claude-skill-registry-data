---
name: "03"
description: >-
  Run an autonomous consensus round between agent peers on several machines: they negotiate a
  decision over a shared channel and execute it without a human relaying messages. Use when
  multiple machines must agree on a change. Triggers: "/03", "work it out among yourselves",
  "find consensus". Wakes the human only for irreversible actions or a deadlock.
license: MIT
---

# /03 — the machines find consensus by themselves

> 🧒 **When reporting to a non-technical owner:** finish with a simple "In plain words" recap (his rule [[eli5-always]]). Only in the message TO him.

The owner said "03" / "you handle it yourselves" → that is a MANDATE: the Claude peers negotiate among themselves and execute on their own. I do NOT ask for permission again — I **announce and go**. The owner is needed at exactly 2 gates (below).

**Argument:** `/03 <topic/decision>` — what to agree on. If there is no topic (a bare "03") — take the subject from the current conversation; if it is ambiguous, formulate the proposal from context yourself.

**Aliases:** `003` = `03` (the extra zero is ignored); case does not matter [[commands-case-insensitive]]. Do not confuse it with "02" — that is escalation TO the owner (the approval channel), the opposite direction.

---

## Step 0 — Peer liveness ONLY from a live signal (pitfall 2026-07-04)
Before pinging a node or declaring "down/alive" — ask for a fact, don't guess from mtime:
```
python "%USERPROFILE%\.claude\scripts\_shared\clan_alive.py" [<node>]
```
Liveness = Syncthing `connected==True` **OR** a fresh `.tg-seen-<node>` (the Telegram rail). 🟡 = alive over Telegram, Syncthing flapped — that is NOT death. ⛔ NEVER judge by the mtime of file markers (`.read-*`, `.robot-done-*`, the presence of `log-<node>.jsonl`) — a Telegram-rail follower does not write them by design. Canon: [[peer-liveness-live-signal]].

## Step 1 — A one-line announcement, WITHOUT waiting for a "yes"
Drop exactly one line to the owner and move on immediately (he can cancel, but I don't wait):
```
🤝 unless you object, I'm going to agree this with <peers> over the coordination channel: "<topic>"…
```
`<peers>` = the other machines of the fleet (the hub `HUB-1`, the laptop `LAPTOP-1`, teammates' machines). Who is online is visible on the bus; an exact list is not critical, the engine broadcasts to everyone.

## Step 2 — Determine the risk tier (this decides whether the owner is needed)
- **Tier-0/1** (safe, reversible: which machine runs a background job, scheduling, format choice, tagging, a dedup judgement) → the peers close it themselves.
- **Tier-2** (money · outbound sends · irreversible · secrets · editing the SHARED canon CLAUDE.md / the Bible / operating-agreement) → even with agreement it is NOT auto-committed, it goes to the owner via the approval flow.
In doubt — pick the higher tier (safer).

## Step 3 — Open the proposal through the engine
- ⚠️ **FIRST check that no one else already has a thread on THIS action** (pitfall 07-17: the hub and the anchor independently opened #0eaf6c3c and #490b0384 for the same canon merge → a duplicate): `consensus.py pending` + `consensus.py list`. There is an open proposal from a peer for the same action → **reply into it** (`respond <id> accept/counter`), do NOT open your own alongside. Open a new one only if none exists.
```
python "%USERPROFILE%\.claude\scripts\consensus.py" propose "<ACTION in one line>" --details "<evidence/context>" --tier <0|1|2>
```
(Bash variant: `python "$USERPROFILE/.claude/scripts/consensus.py" propose "<action>" --details "<evidence>" --tier <N>`.)
- ⚠️ **The action goes into `"<subject>"`, the evidence/diagnostics into `--details`.** The tier tripwire scans ONLY the subject (the action) for stop-words, not the evidence. Dump diagnostics ("…laptop **sends**…", "**apikey** matches") into the subject and it will falsely raise the tier to 2 and wake the owner for nothing. Keep the subject short and about the action.
- The engine dual-sends the event into the coordination chat + `_machine-bus` (by construction; a single rail is forbidden) → the negotiation is visible in the chat.
- A Tier-2 propose is escalated to the owner BY THE ENGINE (`❓ QQQ=yes / NO=no`) and is NOT committed.
- Remember the `#id` from the output.

## Step 4 — Negotiate to agreement
The other machine answers `respond <id> accept|counter|reject`. When I am the responding side, first run `pending` (a 0-LLM worklist of "what is waiting for MY answer"), then judge on the merits (cheap model groundwork, [[model-routing-sonnet-grunt]]) and answer with the same verb. Timeouts/rounds are driven by the deterministic `tick` (0-LLM, already inside the inbox robot; the timeout = the SLA of the slowest peer, a sleeping laptop/Mac is given longer than the hub):
```
python "%USERPROFILE%\.claude\scripts\consensus.py" pending
python "%USERPROFILE%\.claude\scripts\consensus.py" tick
python "%USERPROFILE%\.claude\scripts\consensus.py" status <id>
```

## Step 5 — Execute and cross-check (anti "works-on-my-machine")
- Agreed (status=agreed) and Tier-0/1 → `commit <id>` → **apply the real change** → `verify <id> "<evidence>"`.
- A task is globally done ONLY when BOTH machines independently post `VERIFY` (>=2). One peer saying "done" is not done.

## Step 6 — The gates to the owner (exactly 2, otherwise without him)

⛔ **I NEVER hand-write a question to the owner into a chat** — only through the `approval.py` engine [[remote-approval-qqq]]. A hand-written ask has no `#id`: `approval.py due` cannot see it (no re-ping and no escalation), and a later "+" from him has nothing to attach to — the answer falls through the crack between states (incident 07-21, the permission had to be entered by hand). I never hardcode chat ids in the skill: the engine takes the addresses from `~/.claude/approval.json → targets`.

**How an ask is minted:**
```
python "%USERPROFILE%\.claude\scripts\approval.py" ask "<what + why + risk> (consensus #<id>)" --cat <money|delete|outbound|secret|config|other>
```
→ prints JSON `{id, ask_text, targets}`. `ask_text` is posted by **the calling session** (approval.py is a recorder, not a sender) to `targets` IN ORDER: the approval channel FIRST (a sterile "the owner's attention is needed" channel), then a mirror into the fleet log chat / WhatsApp / DM. I catch the answer with `approval.py check` (stdin = the replies from MCP) → `APPROVED/REJECTED/EXPIRED <id>`. A hanging ask is never abandoned: `approval.py due` prints re-ping envelopes — the same session or the inbox robot posts them to the approval channel. That also covers the "minted an id but never managed to post it" break: an unsent ask resurfaces as a `due` envelope within the freshness window (15 min) instead of dying silently.

**Ask dedup (otherwise two questions for one dispute):** before `ask`, check `approval.py pending` — if an open ask carrying this `consensus #<id>` already exists (it may have been minted by `tick` or by a peer), do NOT mint a second one. That is why the consensus id MUST appear in the ask text: it is the only link between the consensus thread and the question to the owner.

**Classification — what even deserves the approval channel** ([[remote-approval-qqq]] §Classification 07-14): **A** internal / fleet-reversible · **B** our content into our own channels · **C** a short, on-topic outbound message to a third party → I decide MYSELF as a co-founder, journal it into `approvals.db` and report after the fact — those do NOT go to the approval channel. Only **D** "the owner's physical hands are needed" (2FA/UAC/a password; phrase it as a click path, not "give me the go-ahead") and **E** categorically serious matters (money · irreversible deletion · secrets to third parties · legal commitments · mass mailing · a new peer) go there. In doubt between C and E → E.

**The gates (exactly two):**
1. **A Tier-2 action of class D/E** → `escalate <id> "<why>"` records the STATE of the thread, but by itself it creates no trackable question → in the same move, mint an ask via `approval.py ask` (see above) and post its `ask_text`. A `QQQ`/`+` arrives from an authorized signer (the owner or one of the two co-signers) → `approve <id> "<who/where/msg-id>"` records the OK in the thread → only then `commit`.
2. **The peers did not converge** within the round_cap (3) / a timeout on something above Tier-0 → first a **tie-break by the anchor node** (`ANCHOR-1` — the coordinator, the source of truth and the arbiter of cross-machine disputes). The anchor is dead / unable to arbitrate (leader-down >70 min → the hub becomes arbiter-for-this-tick) → and **only then** wake the owner through the same `approval.py ask` route.
- **Do NOT escalate:** a safe Tier-0 deadlock → the tie-break (disagree-and-commit) closes it by itself, don't bother the owner.
- ⚠️ On a round cap/timeout, `tick` may shout into the approval channel over its own rail — that does NOT replace the ask: it carries no `#id` from the approval engine. `tick` shouted → mint the ask through `approval.py` anyway, so the question has an id, a re-ping and a recorded answer.

## Report to the owner (after the fact, briefly)
What was agreed · with whom · the verdict (✅ committed+verified / ⏳ waiting for approval / 🔴 dispute → over to you) · what was actually done. An "in plain words" line at the end.

---

### Boundaries
- The Tier-2 hard stop holds: "you handle it yourselves" does NOT grant the right to spend money / send outbound / rewrite the canon on your own.
- Only the owner commits canon, through the hub [[machine-governance-leader-follower]].
- Failure modes (a byzantine peer, an auto-loop, a false VERIFY) are an open DR; until it closes we keep Phase 1 conservative.
- The engine is the single source of truth for state (`_machine-bus/_decisions/log-<MACHINE>.jsonl`); I don't duplicate its logic, I only call its verbs.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

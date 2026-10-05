---
name: task
description: >-
  Delegate work over a shared task chat: a task is assigned by a short code phrase, and the
  assignee's agent expands it into a full seed and starts immediately, with state tracking so no
  delegated task dies silently. Triggers: "/task", "task <ID>", "my delegated tasks", "delegate
  <task> to <person>".
license: MIT
---

# /task — delegating tasks to people, with a seed for THEIR Claude

> The operator says "N understands this one better" → the task goes to them: a message in the
> delegation chat (short, human) + a seed file in the vault (full, for their Claude). They say a
> code phrase to their Claude, which unpacks the seed and starts immediately.

## Constants
- Engine: `python ~/.claude/scripts/_shared/delegate.py` (env `DELEGATE_VAULT` for tests)
- Seeds: `$OBSIDIAN_VAULT/10-Tasks\_seeds\<ID>.md` (Syncthing carries them to every machine; the Mac path differs)
- The delegation TG chat: id in memory [[delegation-chat-04-tasks]]; post from THIS machine's own account
- People: `nat` · `rusl` · `ant`. IDs = NAT-1 / RUSL-2 / ANT-3, case-insensitive

## A. DELEGATE (usually on the hub, on the operator's word)
1. Write the SEED (self-contained, per the decompose canon: Outcome · Context + paths · Scope ·
   Deliverable · DoD · non-goals · how to report back). Normal voice, no secrets ([[credential-store]]).
2. `delegate.py new --to nat --title "<short>" --seed-file <f>` → prints the ID + a ready TG text.
3. Send that TG text to the delegation chat (Telegram MCP). The format is already in the engine output:
   "📌 <name> @teammate_n · <title> · from the operator / Code phrase: 'task NAT-1'".
   ⭐ The @mention is MANDATORY (2026-07-14): without a @username the person gets no notification and
   the message drowns. The same applies to every re-ping.
4. Connect: you handed it over, so you own it until the result. No ACK within ~a day → re-ping in the
   delegation chat; continued silence → the hanging-tasks board + escalate to the operator.

## B. UNPACK (the assignee's machine, on the code phrase)
1. You hear "task NAT-1" / "my tasks": `delegate.py list --for nat` / `delegate.py get NAT-1`.
2. The seed is not on disk yet (Syncthing lag) → say honestly "the file is still in transit", do not invent the task.
3. `delegate.py ack NAT-1 --by "<machine>-<person>"` + an ACK in the chat: "✅ took NAT-1, starting".
4. Work from the seed like any other assignment (Tier-2 and the Bible still apply).
5. Done: `delegate.py done NAT-1 --note "<outcome>"` + a one-line report in the chat + the artifacts per the DoD.

## Boundaries
- The delegation chat is for delegation and ACKs/outcomes only. Questions to the owner → the approval
  channel ([[remote-approval-qqq]]); live coordination between actors → the fleet log chat. Do not turn
  the delegation chat into a conversation.
- Do NOT paste the seed into the chat (too long, it gets lost) — only the code phrase; the seed lives as a file.
- The task owner is a person ([[task-assignment-by-machine]]); their Claude is the hands.
- ID case does not matter ([[commands-case-insensitive]]).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

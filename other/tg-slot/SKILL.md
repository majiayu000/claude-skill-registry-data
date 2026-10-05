---
name: tg-slot
description: >-
  Free a membership slot so a Telegram account can join or create a group. Accounts have a hard
  ceiling on channels plus supergroups, and at the ceiling both creating and joining fail with
  an error that misleadingly blames the target chat. Finds the least-valuable current
  memberships, proposes what to leave, and retries the join. Triggers: "/tg-slot", "cannot join
  the group", "free a telegram slot".
license: MIT
---

# /tg-slot — free a slot for a new Telegram group

**The pain (caught live on 07-26 while assembling a new working group):** the corporate account could neither create a supergroup nor join by invite. Telegram's message about the "maximum number of participants" sends you the wrong way — it is not the chat that is full, it is OUR account. We ended up making a spare personal account the group owner, which is wrong: work groups must live on the work account.

**Engine:** `~/.claude/scripts/tg_group_slots.py` — modes `count` · `rank` · `emit-plan` · `leave`. One file, Telethon, no server and no database.

## The ritual (steps in order, skip none)

### 1. Measure — no number, no next step
```bash
python ~/.claude/scripts/tg_group_slots.py count --account corp_acct --no-probe
```
Prints `Premium: YES/no · ceiling ~N` and `SLOTS USED`. **Read the ceiling from the output, not from memory** — it depends on Premium, and "500" is very often wrong (measured 07-27: one work account showed 1003 used).

### 2. Rank the candidates
```bash
python ~/.claude/scripts/tg_group_slots.py emit-plan --account corp_acct --top 50
```
The LOWER the score, the safer it is to leave. The score is lowered by: the group has been silent ≥1 year (−4, the main signal), a past-year conference in the title (−3), silent ≥6 months (−2), not a single message from us (−2), crypto noise per the dictionary (−1).

**Idiot-proofing — these never become candidates:**
- **99** — our own brand groups (the lab, our public channels, our DAO and founder communities, country event groups), anything where we are **admin or creator** (admin rights are lost irreversibly), the fleet's working chats (the fleet log, the approval channel, the task chat, the calls chat, the pulse chat).
- **98** — **intro groups** ("X <> the lab…", "Intro: …", "Introduction…"). Intros are the core of the owner's product; even a quiet intro group is only handled as a separate review. A dead intro = silent for many months **AND** the deal is closed — that is the owner's call, name by name, never the script's.

Before showing the list, **make sure the protection actually fired** — and not by the counter in the header, but by reading the names with your eyes. The header prints "protected (ours/admin): N · intro groups: M", but the counter cannot see what the dictionary does not know.

⚠️ **The 07-27 incident this step exists for.** The first run offered 10 live intro groups as leave candidates: `Jane D 🤝 Stanford AI Research Lab`, `HSG < > SF Accelerator`, `Ivan 🤝 Ted`. The detector was looking for `<>`, while **the owner's main convention is the handshake emoji `🤝`**; on top of that, two real brand names were not in the brand list at all. The header counter looked perfectly healthy meanwhile. The takeaway is worth more than the fix itself: **the dictionary always lags behind life**, therefore the list is read by eye, name by name, and never accepted on a metric. While reading, look for: two names/companies joined by a separator · a surname you recognise · an unfamiliar brand that might turn out to be yours.

### 3. Show the owner and get a "+"
Show the list **before** leaving: title · date of the last message · reason. Leaving a group is **IRREVERSIBLE** — you cannot get back into a private group without a new invite. So this is a real stop: without the owner's explicit "+" on a SPECIFIC list, nothing is executed. The owner is away from the terminal → `approval.py ask` into the approval channel (this is class E — irreversible loss of access), not "I'll decide myself".

### 4. Leave
```bash
python ~/.claude/scripts/tg_group_slots.py leave --account corp_acct --confirm OWNER-PLUS-2026-07-27
```
The executor re-checks each group's status **at the moment of leaving** instead of trusting the plan: the plan may be stale (we were made admin, the group came back to life). Everything protected is skipped with a reason. Every departure is journalled into `~/.claude/tg_leave_log.jsonl` (that journal is the evidence for the task).

### 5. Re-measure and join
Repeat step 1 — the number must drop. Then join the new group with the account you were clearing space for. **Proof by doing, not by "it should work":** until the account has actually joined, the slot does not count as freed.

## The rule "joined a new one → free a slot"
This is not a one-off cleanup, it is a trade. Every time a work account joins a new group near the ceiling — immediately name the least relevant one to leave and propose the swap. Otherwise we hit the wall again in a month, in the middle of live work (which is exactly what happened).

## Boundaries
- ⛔ **Never leave without the owner's explicit "+" on a concrete list.** Irreversible.
- ⛔ **Do not clean the personal and primary work accounts** — they are not full, they are our spare capacity. Cleaning applies only to the corporate and the secondary work account.
- ⛔ Intro groups and groups with live lead/partner conversations — reviewed by the owner, name by name, only.

## Run pitfalls (they cost one killed run on 07-26)
- **Don't wrap it in `timeout N`** — walking all dialogs takes longer than 5 minutes, and a `timeout 280` wrapper killed the first run.
- **Don't trim the output through `tail`** — that eats the header with the slot counter, the very thing you ran it for.
- **Output is buffered** when redirected to a file: run it in the background and poll the file, "empty" ≠ "broken". To check the process is alive: `Get-CimInstance Win32_Process -Filter "Name like '%python%'" | ? { $_.CommandLine -like '*tg_group_slots*' }`.
- There is a 2s pause between departures plus `FloodWait` handling — Telegram dislikes a burst of leaves.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

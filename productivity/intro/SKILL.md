---
name: intro
description: >-
  Introduce two or more people from the owner's network: resolve and confirm both identities, DM
  each side for consent before any group exists, then create the group and introduce both sides
  inside it. Requires the owner's approval first. Triggers: "/intro", "introduce X and Y",
  "connect X with Y".
license: MIT
---

# /intro: warm-introduction automation

The operator's matchmaking is a conveyor: a warm intro is the product they trade. This skill turns "introduce X to Y" into one repeatable operation, run from their Telegram account.

Proven live 2026-06-19 (test pair Rita @teammate_r + Nataly @teammate_n). Standing rules live in memory [[intro-automation]] and [[no-long-dashes]].

## Flow

### 1. RESOLVE both people
For each name, identify the real person before doing anything:
- `/find` or `namesearch` over names.db, the Platinum CRM `leads`/`contacts`, and Telegram `resolve_username` / `search_contacts`.
- Disambiguate name collisions (the operator has many same-name contacts: 8 Denises, several Karim) using `get_common_chats`, company, recent calls.
- Capture for each: real name, @handle, tg_id, company, and the Latin first name for the title.

### 2. CONFIRM (DEFAULT: ON, approval required)
Show the operator a compact BEFORE→AFTER block:
- who each person resolved to (name, @handle, company),
- the exact group title that will be created,
- which account will send.
Wait for their "+". Do NOT create anything before that.
Skip this gate ONLY if the operator explicitly says "no approval needed" in the request.

### 3. CREATE the group
- `create_group` from the chosen account, title = `LatinName1 <> LatinName2 <> Palo Alto Research Lab`.
- The `<>` sign goes between ALL elements. Names are LATIN only, taken from the lead's own name. Pass the title with plain `<>` AT creation. Never HTML-escape it. Never rely on renaming afterward (see gotchas).
- Account label "default" = @work_acct_a (id 226258979); "corp_acct" is the company voice. Pick the account with the warmest existing thread to each lead.

### 4. INTRO blurb in the group
- Right after creating the group, get its invite link via `export_chat_invite`.
- Short, warm, in the operator's voice. State who each person is and why they are a fit, INCLUDE the group link ("Group: <link>"), close with "over to you two".
- LANGUAGE: write to each lead in THEIR language. A Russian-speaking lead gets Russian, an English-speaking lead gets English. Detect language from the CRM card (country / language field), the vault person note, or the prior DM-thread language. If the two leads share no common language, write the group blurb bilingually (RU plus EN).
- No long dashes anywhere (use a colon, comma, or parentheses). See [[no-long-dashes]].

### 5. DM each side
- A one-line personal heads-up to each participant, written IN THAT PERSON'S language, including the group invite link so they can jump straight in.

### 6. LOG and close the loop
- Mark both in the Platinum CRM at the INTRO stage.
- Set a watcher to close the loop later ("how did the conversation go?", the operator's double-intro rule).

## Telegram-MCP connector gotchas
- `edit_chat_title` FAILS on basic groups (CHAT-ERR-838): you cannot rename after creation, so always create with the final correct title in one shot.
- There is no delete for Telegram basic groups, only `leave_chat` (which leaves a ghost group for the others). Get the title right the first time.
- Adding mutual contacts works. If a non-contact's privacy blocks adding, fall back to `export_chat_invite` and send the link.
- Pace intros one at a time with gaps (anti-ban). Never mass-create.

## Hard stops (defer to operating-agreement + bible)
Pause and ask the operator when an intro carries money, a commitment, secrets, or would be a mass blast. A plain social intro with no such payload is fine to run after their approval.

## Report to the operator
Short summary of what was created plus the group title and who is in it, then a `🧒 In plain words` recap. No long dashes.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

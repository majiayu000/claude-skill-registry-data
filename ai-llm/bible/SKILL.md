---
name: bible
description: >-
  Load the operations codex that governs everyone acting as or for the owner (the owner, human
  assistants and AI agents) before outreach, replies in their chats, scheduling, purchases,
  hiring or household ops. Covers where the rules live in the vault, how to pull the right
  slice, and the rule that the newest entry wins per topic. Triggers: "/bible", "what do the
  rules say".
license: MIT
---

# Bible — Anton's behavioral codex (mega-skill)

> 🧒 **When reporting to Anton:** end with a child-simple "In plain words" recap in his language (his standing request; reports TO Anton only — never inside vault notes or outbound messages). See memory `eli5-always`.

The Bible is not documentation — it is the **behavioral rulebook for every actor that acts as or for Anton**: Anton himself, his living assistants, and silicon agents (LLM/AI). One artifact, many readers. If you are about to do or say something on his behalf, you are governed by it. Canonical logic lives in the vault note `protocol-bible-as-prompt`.

## Who is governed
Anything done "as Anton" or "on Anton's behalf" — you (the agent), his assistants, him.

## Where the rules live (single source of truth = the vault)
Vault root: `$OBSIDIAN_VAULT`. **Never duplicate rules into this skill — copies drift.** Load from:
- **The umbrella note:** `concept-bible-platinum`.
- **Domains / indexes:**
  - 📤 Outreach & external leads (priority #1): `_Bible-Outreach-MOC`
  - 🏢 Operations: `_Operations-Bible-MOC` · Trello cards: `_Bible-Trello-Index`
  - 🛒 Purchases: `_Pokupki-Rules`
  - 🙋 Anton's personal layer: `concept-bible-personal`
- **Altitudes (note prefixes):** `insight-*` (principle) → `protocol-*` (playbook) → `reglament-*` (atomic rule) → `decision-*` (precedent).
- **Self-maintenance:** `protocol-bible-self-maintenance`. **Secrets boundary:** `decision-bible-secrets-quarantine`.

## How to load the right slice
Pull the **narrow relevant slice** for the task — not all 10 years.
- By domain: open the matching MOC above.
- By meaning: `python $IMPORTS_ROOT/brain_ask.py "<question>"` (semantic search over the curated layer).
- By keyword: grep `reglament-*` / `protocol-*` under `03-Insights\Operations\` and `05-Resources\Protocols\`.
- Filter by `audience`: load `agent` + `both`; skip `human`-only (needs live judgment).

## Precedence — resolving conflicting rules
1. **Newer beats older on the same topic** (Anton's law) — by `date_established`; the loser becomes `superseded`.
2. **Anton's explicit rules are protected** — to override an `origin: anton` / `authored_by: human` rule, the new one must also be Anton's or carry `supersedes:`. Team/agent don't override Anton by date alone.
3. **Specific beats general** (carve-outs).
4. **Priority flag** `must` > `should` > `may`.
5. Letter-vs-spirit clash (reglament vs insight) → escalate to Anton to rewrite the reglament.

## consult → act → write-back
1. **Consult** the slice before acting.
2. **Act** by the rules. Consequential/irreversible (money, outbound to external people, commitments, access) → **Tier-2: ask Anton** (`operating-agreement`). Outbound lead messages = draft→approve, never autonomous.
3. **Gap → escalate** to Anton; his answer becomes a new `reglament-*` (verbatim, with `audience`). "Error/gap → write the rule immediately."

## Secrets quarantine
Because the Bible is now a prompt, never load or emit secrets (passwords, accesses, financial figures, "grey" techniques). They live outside the loadable Bible. See `decision-bible-secrets-quarantine`.

## Relation to other skills
`telegram-assistant` and `telegram-lead-outreach` are channel playbooks **under this contract** — same precedence, same write-back, same secrets boundary. When they act on Anton's behalf, this skill's rules apply.

## How to write a rule (dual-reader)
Verbatim from Anton · imperative `WHEN → DO` · self-contained + example · frontmatter (`type`, altitude, `audience`, `theme`, `origin`, `authored_by`, `date_established`, `status`, `confidence`, plus `supersedes` / `superseded_by` on replacement). Full standard: vault note `protocol-bible-as-prompt`. **Step-by-step playbook with examples (even for a weak LLM): vault note `protocol-bible-rule-authoring`.**


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

---
name: comments
description: >-
  Work the comments under published posts in one pass: list unanswered ones, reply only where a
  reply is genuinely expected (at most three per pass), name top commenters as warm-DM
  candidates, and prepare reply drafts on approval. Triggers: "/comments", "unanswered
  comments", "who is commenting".
license: MIT
---

# /comments — comments under our content (show · reply · grow into a DM)

> 🧒 End the report to a non-technical owner with a short "In plain words" recap. (memory `eli5-always`)

One pass: show the comments and reply **surgically** where a reply is actually expected. It collects and displays; it **sends replies only on the owner's explicit "+"**. A thin layer (AK-47) over the engines in `$IMPORTS_ROOT/content-factory\registry\`.

> 🔴 **BATTLE LESSON 2026-07-15** (memory `bulk-replies-cringe-one-offer-converts`). The goal "zero unanswered" is **CANCELLED**: a batch of 16 replies to old comments was deleted by the owner in full ("my batch went out… I'm embarrassed myself"), comment auto-posting was turned off, and one of our accounts lost access to a third-party group.
> In the same night ONE public call-to-action post landed a partner within 30 hours.
> → **Default = stay silent.** Reply only if: it is addressed to us OR the thread is alive (younger than ~a week) OR a person is personally waiting for an answer. Older than that — skip, and that is NOT a debt.
> → **Ceiling ≤3 replies per pass**, never as a back-to-back series inside someone else's group: pace and volume read as a bot regardless of how good the text is.
> → Value is measured in people who moved, not in the unanswered counter.

**Boundaries:** this is about comments under OUR published posts (pubmetrics.db). The separate club corpus has its own skill (`/sostav-comments`). Facebook comments will be pulled in once the Graph token is live — for now the source is Telegram.

## 1. Fresh collection (0 tokens)
First refresh the database so you don't reply to stale material:
- `python tg_comments_collect.py` (idempotent; exit 3 = the sending rail is busy → say "retry later", don't crash).

## 2. Show the state
- `python pub_metrics.py status` — how many unanswered in total.
- `python pub_comments_report.py` — digest of the unanswered ones (spam bots from `spam_authors.txt` are already flagged 🤖 and filtered out).
- `python pub_metrics.py top-commenters --n 15` — who comments most often.

Show it to the owner compactly: N unanswered per platform · top-5 commenters · link to the dashboard `_Dashboards\Pub-Registry-Metrics.html`.

## 3. If the owner asks for replies ("answer the comments" / "+")
Draft-first, sending by hand or on "+":
1. **RECALL the author** before every reply to a human: `/find <name>` (namesearch) + grep the vault + the Telegram profile (`get_full_user` by author_id from comments). Know who you are writing to.
2. **Tone per channel** ([[short-text-when-unreviewed]]): Telegram = a meaningful on-topic reply with context (NOT a 5-word Facebook joke). The owner's voice = the top-tier model.
3. **What to skip:** spam bots 🤖 (no reply); old threads where a reply is no longer appropriate (decide explicitly).
4. Show the batch as a table "comment → draft → which account sends it" and wait for "+". After sending — `pub_metrics.py mark-replied --cid <id>` (or the next `tg_comments_collect.py` will set `replied` by itself).

## 4. Top commenters → a public call in the group, a DM on top
An active commenter with no CRM card = a candidate. Create the card (CRM), run a RECALL. ⭐ The offer (testers/a call/early access) goes **publicly into the group**, not by DM — a DM only as a personal nudge AFTER the public call (canon: the house rulebook `offer-to-active-people-publicly-not-by-dm`, memory `public-offer-in-group`). Don't send a DM without a "+" ([[telegram-account-identities]]). Clan members are not leads.

## Boundaries / safety
- READ by default. Mass back-dated replying = a **hard stop**: batch only, and only with a "+".
- Spam filter: add a new bot wave to `spam_authors.txt` (`author_id  # reason`).
- Nothing private from the comments leaks into other channels.

## Related
The morning auto-ping of unanswered items into the fleet log chat (05:35, task "Pub-Comments-Morning") and the nightly collection (03:40, `collect_pub_metrics.cmd`) — this skill is the manual, on-demand twin of those routines. Canon: `00-System\Pub-Metrics-Registry.md`, memory `content-pub-registry`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

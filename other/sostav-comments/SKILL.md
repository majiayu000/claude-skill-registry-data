---
name: sostav-comments
description: >-
  Draft short, in-voice reply candidates to a fresh community shortlist: read the nightly
  detector report, pick posts in safe or opinion topics, pull a grounding snippet from the local
  corpus, and write the drafts. Drafts only, and the owner posts. Triggers: "/sostav-comments",
  "draft replies to the shortlist".
license: MIT
---

# /sostav-comments — draft replies to the fresh club shortlist (the owner's voice, draft-first)

**Why.** When the owner goes through the fresh nightly shortlist, he usually wants ready-made draft replies for the interesting club threads. This skill does it in one pass: read the detector report → pick the safe posts → write short answers in his voice → show them. **It sends nothing** — the owner copies whatever he likes.

**The main rules:**
- **Draft-first, never publishes.** The skill only writes drafts into the chat. Posting into the club is done by the owner, by hand.
- **Safe-topic gate.** Draft only in opinion/knowledge threads (Knowledge, Lectures, Business, Investing, Travel, Health, General-on-topic). ⛔ NEVER draft in the Crypto / Dating / Off-topic-flood threads, or in any grey-financial or personal thread — those are data, not a place to reply.
- **Short text, tone set by the channel** ([[short-text-when-unreviewed]]): a meaningful answer in messenger register (not a 5-word Facebook joke — here you need context and knowledge of who the person is; pull the `person-sostav-*` card if the member is a ⭐).
- **The owner's voice (Opus).** No "positioned" replies, no showing off. On topic, to the point, without making someone else's announcement about yourself.
- **Anti-leak** ([[reglament-anti-leak-na-vyhode]]): drafts stay in the private layer; nothing sensitive from the club leaks into other channels.

---

## 0. A fresh shortlist
The latest detector report:
```
ls $IMPORTS_ROOT/alpha\candidates\sostav-*-report.md   # take the newest one by date
```
If there is none / it is stale — refresh the corpus first (the nightly path): `python $IMPORTS_ROOT/sostav\nightly_run.py` (idempotent, it backfills).

## 1. Pick the posts worth answering
From the shortlist keep only those where:
- the topic is **safe** (see the gate above);
- the post is an opinion/question/piece of knowledge where a meaningful answer belongs (not an announcement, not an intro, not a grey request);
- a ⭐ author → open `$OBSIDIAN_VAULT/07-People\person-sostav-<slug>.md` for the "who is this" context.

## 2. A grounding snippet (when it helps)
If the answer benefits from specifics (a quote/fact/example), take a relevant chunk from the working corpus — the **YouTube Data API** (the only pool that still works; the social networks are behind login walls), via `$IMPORTS_ROOT/sostav\daily_safe_fetch.py` (safe-only gate). Lift 1-2 fragments verbatim; don't paraphrase.

## 3. The drafts (Opus, personal, all different)
For each selected post — a **separate** short answer in the owner's voice. Assemble the batch:
```
1. [Knowledge · Author X] post: "…the claim…"
   → draft: "…a meaningful, on-topic answer in the owner's voice…"
2. ...
```
Different texts, on topic, no template. Voice quality ≥ Opus ([[content-Mei-style]] — an influence, not a copy).

## 4. Hand it to the owner
Show the batch of drafts in the chat + note which ⭐ contacts you pulled cards for. **Stop there** — the owner sends them himself.

---

## Stop valves
- ⛔ Post/send nothing — drafts into the chat only.
- ⛔ Don't draft in grey/personal/crypto threads (the safe gate).
- ⛔ Nothing from the club leaks into other channels ([[reglament-anti-leak-na-vyhode]]).
- Money/commitments/secrets inside a draft → cut them, that is Tier-2.

## Related
- Detector / nightly path: `$IMPORTS_ROOT/sostav\nightly_run.py`, `sostav_alpha.py`.
- The reply corpus: `daily_safe_fetch.py` (YouTube Data API, `secrets/youtube.env`).
- Voice: [[short-text-when-unreviewed]], [[content-Mei-style]], `/speak-as`.
- Sibling skills: `/fb-reply` (Facebook comments), `/mine-channel`, `/alpha-judge`.
- Canon: memory `sostav-community-import`, [[reglament-anti-leak-na-vyhode]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

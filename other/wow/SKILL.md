---
name: wow
description: >-
  Assemble a full multi-tier content episode from a milestone session's hot context and publish
  it out of band, ahead of the nightly schedule: teasers go to chats right after one approval,
  the rest follow by topology. Triggers: "/wow", "this is a milestone", "this session is great,
  tell everyone".
license: MIT
---

WOW — the priority lane of the content factory (milestone → maximum content → no queue)

TWO KINDS OF SESSION (owner's rule, 2026-07-02):
- Ordinary → it will land in the daily diary/devlog by itself (fb_diary_collect), do nothing.
- MILESTONE → the owner says /wow → this skill: a full episode + publication first, without waiting for any schedule.

WOW TOPOLOGY (owner, by voice 2026-07-02; on top of §7.2 of decision-content-pipeline-reality-show):
```
tier       where                                       status
teaser RU  RU chat            <YOUR_CHAT_ID>           🟢 wired (auto after the "+")
teaser EN  EN engineers chat  <YOUR_CHAT_ID>           🟢 confirmed by the owner (our accounts are admins there)
medium RU  RU channel (id from the content lead)     ⏳ candidate: RU lab channel <YOUR_CHAT_ID> — do NOT post until confirmed
medium EN  EN channel (id from the content lead)     ⏳ candidate: EN engineers channel <YOUR_CHAT_ID> — do NOT post until confirmed
medium FB  the owner's wall via /fb-post               draft-first, its own "+", fb_guard
longread   decided by the content lead + Claude (for now §7.2: RU chat + GitHub) ⏳ question sent over the bus
dev-log    GitHub EN (manually via gh)                 same as §7.2
X EN       asleep until the creds in secrets\x_api.env dormant
```
⛔ The upstream community channel is SOMEONE ELSE'S — never post there ([[openclaw-telegram-channels]]).

STEPS:
0. ⭐ THE BEAT FIRST (v2, 2026-07-10, the law "canon before content"): a milestone means first a beat `beat_kind: milestone` into the canon at `$OBSIDIAN_VAULT/04-Projects\show-canon\beats\` (template `_TEMPLATE-beat.md`; reveal honestly) + update the arc → `canon_render.py`. The episode then leans on that beat (one fact — so the episode, the chapter and the dev-log cannot drift apart).
1. DISTILLATION — from the hot context of the CURRENT session: what we did, why it is a milestone, the conflict/arc (style-reality-show), the owner's angle if he gave one. Session went cold / different date → `python $IMPORTS_ROOT/fb_diary_collect.py <DAY>` as raw material.
2. SCAFFOLD + PRIORITY (0 tokens). ⛔ ANTI-DUPLICATE FIRST: check `priority.json` + `episodes\` for an episode about the SAME milestone from a parallel session (the fleet is active!); found one — join/extend it, do NOT spawn a second bundle (pitfall 2026-07-02: assembled 6 tiers, superseded 40 minutes later):
   `python $IMPORTS_ROOT/content-factory/episode_adapter.py new --slug wow-<kebab> --title "<title>" --source "session:<YYYY-MM-DD>"`
   then mark the priority: `python $USERPROFILE/.claude/skills/wow/wow_priority.py add --slug wow-<kebab> --title "<title>"` (writes `"priority":"milestone"` into the bundle's meta.json + a line into the queue `$IMPORTS_ROOT/content-factory/priority.json`).
3. WRITING the tiers — as in /episode (style, privacy, the co-founder WhatsApp CTA +1 341 222 9178 on medium/longread). The author's voice = the top-tier model of the session.
4. CHECK: `episode_adapter.py check --slug <slug>` (FAIL=0) + run /taste-check. Only then show it.
5. ONE "+" PER EPISODE: show the owner the bundle summary (tier → destination → first line) in the current chat AND mirror it into the drafts gate chat <YOUR_CHAT_ID> (his ➕ there = approval) → wait for the "+". ⛔ Put NOTHING into Saved Messages (owner, 2026-07-02). ⭐ ALWAYS: tiers the owner posts HIMSELF (Facebook and any manual one) go, once the bundle is ready, paste-ready into the processed-voice-notes chat <YOUR_CHAT_ID> as three messages: (1) the instruction, (2) the clean post body, (3) the clean first comment — body and comment without prefixes, so they copy whole.
6. PUBLISH IMMEDIATELY (after the "+", nothing waits for nightly routines):
   - teaser RU → the RU chat, teaser EN → the EN engineers chat (Telegram MCP, the secondary work account; fallback below).
   - medium RU/EN → the channels once the content lead confirms them; until then — paste-ready to her over the bus (bus_send) with "post this by hand".
   - medium FB → /fb-post (its own Tier-2 gate + fb_guard; do NOT bypass the limits — that is the ban protection).
   - longread/dev-log → per the decision with the content lead; GitHub manually.
   - `episode_adapter.py set-status --slug <slug> --status published` + `wow_priority.py mark --slug <slug> --status posted`.
   - Publication log (what → where → link) → the "published" feed chat <YOUR_CHAT_ID>.
7. ANTI-DUPLICATE FOR NIGHTLY ROUTINES: the daily generators (fb-diary, content-factory-daily) read today's `priority.json` → they mention the milestone with a link to the episode, they do NOT retell it from scratch.

FALLBACK when the Telegram MCP is red on this machine: don't go silent — send the job to the hub `python ~/.claude/scripts/bus_send.py HUB-1 "WOW-POST: <slug>, texts in episodes\<slug>\, targets: ..."` (the hub posts), and one line to the owner: "MCP is red, handed to the hub".

BOUNDARIES: draft-first outbound until the "+" (one "+" covers the teasers + channels of this episode; Facebook always keeps its own gate). Money/commitments/secrets in the text = stop. Privacy: no amounts and no third-party names. Teaser 240–370 chars HARD. One episode = one milestone.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

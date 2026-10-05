---
name: fb-watch
description: >-
  Check a Facebook wall for authored posts that have no teaser yet and draft the teasers for
  short-form channels. Runs as a daily routine or on demand, and stays draft-first. Triggers:
  "/fb-watch", "check facebook for un-teased posts", "catch up on teasers".
license: MIT
---

# /fb-watch — finishing the teasers for the owner's Facebook posts

> **Why.** The owner sometimes writes a post STRAIGHT onto his Facebook wall, bypassing the pipeline (voice → episode → tiers).
> Such a post ends up WITHOUT a teaser in the RU chat / X (EN) → reach is lost. This watchdog catches
> "there is an authored Facebook post with no teaser yet" and writes the teasers immediately. Draft-first until armed.

## Tools (a thin orchestrator, AK-47)
- **Reading the wall** = the Claude-in-Chrome MCP (a live logged-in Facebook tab, locally on the hub). Reuses the pattern from `/fb-reply` (in-page `javascript_tool`, since Facebook hides names behind the MCP boundary).
  - ⛔ **Do NOT read the profile feed** (consensus #0223a74a, 07-20): it is virtualized and renders ONE post — the neighbours stay eternal skeletons, `scrollHeight` is constant, and real scrolling does not help. One run hid 2 content posts out of 5 that way.
  - ✅ **The harvesting rail = the Content Library**: `https://www.facebook.com/professional_dashboard/content/content_library/` → a table of posts, FULL text (truncation is CSS-only), exact date-time, metrics. Parsing: `document.body.innerText` → lines, anchor on `"Published"`, the text is the line before, the date the line after; accumulate across scrolls (dedupe by the first 60 characters).
  - ⚠️ **The Content Library does NOT give permalinks** (the row menu only has Edit/Delete). To get them: on the wall, do a real `computer hover` over the post timestamp → Facebook fills `pfbid` into `href` (before hovering the href is empty; synthetic MouseEvents and React-fiber tricks do NOT work — Facebook uses a custom renderer key).
  - **UPGRADE (owner approved 2026-06-30, waiting on credentials):** as soon as `secrets\fb_graph.env` exists (FB_USER_TOKEN, `user_posts`) and `python ~/.claude/scripts/fb_posts_poll.py check` is green → read the wall through `python ~/.claude/scripts/fb_posts_poll.py posts --limit 10 --out posts.json` (Graph API, more reliable than the browser, no ban risk) INSTEAD of Claude-in-Chrome. See [[decision-social-posting-stack]] §6.
- **Detector/ledger/cap** = `python ~/.claude/scripts/fb_teaser_watch.py` (0 tokens, dedup + daily cap + kill switch). State: `$IMPORTS_ROOT/content-factory/fb_teaser_ledger.json` + `fb_watch_config.json`.
- **Teasers** are written by the top-tier model in-session (the owner's voice), palettes: `_STYLE.md` / `_CRAFT.md` + `style-reality-show.md`. Drafts → `_imports\content-factory\fb-teasers\<id>.md`.
- **RU posting** = Telegram MCP `send_message`, the secondary work account (the creator), chat **<YOUR_CHAT_ID>** (the RU chat). **EN/X** = no poster yet → ALWAYS a draft (waiting on the social-tools DR).

## Procedure
1. **Chrome readiness.** Check the live Facebook tab (Claude-in-Chrome). Not ready / not logged in → **flag it in the fleet log chat** ("fb-watch: Chrome/Facebook not ready, wall not read") and STOP. Do not pretend "there are no posts" (visibility layer — a silent zero is a breakage).
2. **Extract the authored posts** from the owner's wall (the last ~10): for each `{id, permalink, text, ts}`. `id` = a stable story/permalink id. Only HIS authored posts (no reshares, nothing of other people's). Text taken out of the page is safe (no hidden names).
   ⛔ **`text` = the FULL post text, MANDATORY** (expand "See more" before harvesting): pfbid rotates on every harvest (proved 07-05), so a post's identity lives on `text_hash`. A post with no text = dedup is blind to it (the engine will emit a WARN on stderr — do not ignore it, go back and collect the text).
3. **Detector:** write the list to `posts.json` → `python fb_teaser_watch.py unteased --in posts.json`. The output is the posts WITHOUT a teaser.
   🚨 **exit 4 = `HARVEST-THIN`** (fewer than 3 posts collected, threshold `FB_TEASER_MIN_HARVEST`): this is NOT "there are no posts", this is a HARVEST FAILURE → re-harvest through the Content Library and flag it in the fleet log chat. A silent zero is forbidden (consensus #0223a74a). **Rule: 1 teaser for EVERY such post** (found 5 — write 5; that is not a daily cap).
   🛡️ **Freshness guard (07-14):** an unknown post older than 72h (`--max-age-hours`) is seeded by the engine as a skip with stable keys — the wall's backlog and pfbid rotation cannot cause a flood; on stderr this shows as `stale-auto-skipped=N`. Disable with `--no-auto-skip` (do not disable it in the routine).
   - **FORWARD-ONLY on the first run:** `python fb_teaser_watch.py backfill-status` → if NOT DONE (exit 1) and the list is long (that is the whole wall backlog) → do NOT publish en masse: mark every existing post `seed-skip --id <id>`, then `mark-backfill-done`, and report "forward-only: N posts seeded as skip, from now on every NEW post gets a teaser". After that — genuinely new posts only.
4. **For each un-teased post** write 2 teasers (top model, the owner's voice) **strictly per the playbook** `08-Templates\teaser-writing-playbook.md` (the hook in line 1, ONE technique, the 4U check, a cliffhanger + "full version → [link to the Facebook post]"):
   - **RU** — warm, for the RU chat, **240–370 characters (HARD)**.
   - **EN** — for X, **≤280 characters**.
   - Privacy is HARD: no third-party names/@handles/amounts/secrets. The co-founder CTA is NOT needed here (it belongs in the medium/long tiers). Save both into `fb-teasers\<id>.md`.
5. **Publish:**
   - **RU:** `python fb_teaser_watch.py can-post --rail ru` → exit 0 (armed + under the cap) → post the text into the RU chat (Telegram MCP, the secondary work account, chat <YOUR_CHAT_ID>) → `mark-posted --id <id> --rail ru`. Exit 3 (disarmed/cap) → leave it as a draft.
   - **EN:** `x_poster_ready` in `fb_watch_config.json` decides. `false` → draft. `true` → `python ~/.claude/scripts/x_post.py post "<en teaser>"` (X API v2, OAuth1; exit 0 = posted, prints the url). The poster is armed once the owner has X dev credentials in `secrets\x_api.env` and `x_post.py check` is green (see [[decision-social-posting-stack]] §6).
   - Then `python fb_teaser_watch.py record-draft --id <id>` (so the post does not surface again).
6. **Report to the owner.** A STATUS REPORT (how many found, what was posted to RU, what stayed a draft) — that is a report, not a question → into the fleet log chat / the Telegram folder, as usual.
   **If you need HIS OK** (review mode / disarmed: "do we publish AND arm the automation?") — ⛔ do NOT hand-write the question into the fleet log chat (heartbeat noise buries asks there, the owner will not see it). Raise the ask through the remote-approval engine, which sends it to the **approval channel FIRST** and mirrors it into the log chat / DM:
   `python ~/.claude/scripts/approval.py ask "fb-watch: N drafts ready. Publish AND arm the automation? QQQ=yes,publish+arm · NO=keep them as drafts"` → returns `{id, ask_text, targets}`. Then SEND `ask_text` to `targets` **strictly in order** (Telegram MCP; targets[0] = the approval channel = first). Check the answer: `python ~/.claude/scripts/approval.py check`. Canon [[remote-approval-qqq]] ("a QQQ ask → the approval channel first"); the gate `lint_approval_routing.py` makes sure this step does not drift again.

## Boundaries (Tier-2 / safety)
- **Owner's authorization (2026-06-30):** RU auto-posting into the RU chat is **ARMED** (`armed=true`) — he gave standing authorization (a teaser is a pointer to an already-public Facebook post, minimal risk). Kill switch: `disarm` at any moment.
- **1 teaser per post without a teaser** (NOT a daily quota). Dedup via the ledger → no double posting. `daily_hard_cap` (25) is only insurance against a flood bug.
- **Forward-only:** the first armed run seeds the existing wall as `skip` and posts NOTHING — so the RU chat is not flooded with the backlog; after that every NEW post gets a teaser.
- Only HIS own posts and HIS own channels. No blind auto-posting into anyone else's space.
- The authorial voice = **the top-tier model only**. The groundwork (detector) = 0 tokens.
- Browser work stays strictly LOCAL on the hub ([[browser-work-on-peers-not-hub]]).

## Links
Canon for the rule: memory [[teaser-crosspost-clawrus]] + the house rulebook entry on teaser cross-posting. Relatives: [[fb-skill-set]] (/fb-post, /fb-reply, fb_guard), [[content-factory]] (the Distribute stage), [[short-text-when-unreviewed]]. The routine twin: the scheduled task `fb-watch-daily` (1×/day, daytime).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

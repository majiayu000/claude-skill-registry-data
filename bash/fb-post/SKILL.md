---
name: fb-post
description: >-
  Publish an already-vetted post to a personal Facebook wall through the owner's real logged-in
  Chrome tab (a low-ban-risk path), rate-limit-guarded and draft-first: paste, verify what is
  actually in the composer, confirm after reload. Triggers: "/fb-post", "publish to facebook",
  "post this to my wall".
license: MIT
---

# /fb-post — publish a post to the owner's wall (safely, draft-first)

**Why.** The content factory and the Facebook diary already WRITE posts in the owner's voice, but the draft still ends up parked in Saved Messages / the vault. The only missing piece was the "publish" button. This skill closes it — in the safest possible way (acting inside a live logged-in Chrome tab, not with a headless bot), with a hard volume counter.

**Main rules (from Deep Research #32):**
- Publishing = **OUTBOUND + PUBLIC = Tier-2** → show the final text to the owner and wait for an explicit `+` (or let him press "Publish" himself). Never publish silently.
- **The owner's voice = the top-tier model.** Take the text from a ready draft (`content-factory`, `facebook-diary`, `episode`) or write it with the top model. Don't invent a new voice, and don't let a cheap model write authorial text.
- **Keep the volume low:** `fb_guard` caps it at ≤8 posts/day. Don't repeat the same text (spam flag).

---

## 0. The fuse BEFORE the browser (mandatory)
```bash
python "$USERPROFILE/.claude/scripts/fb_guard.py" check post
```
- `OK post (...)` → you may continue.
- `BLOCKED post: ...` (exit 3) → STOP. Tell the owner the daily post limit is used up, offer to schedule for tomorrow. Do not work around it.

## 1. The text (owner's voice, top model)
1. If the owner gave a ready draft — use it. If he asks "make a post out of X" — write it with the top model in his voice (see `fb-diary-voice`: woven narrative, self-irony, ~4000 characters for a diary entry; shorter for an announcement).
2. Show the owner the **final text** and ask for a `+`. This is the Tier-2 gate — no explicit "yes", no next step.

## 2. The browser (Claude-in-Chrome, live tab)
> Browser work is strictly LOCAL to this machine. Don't pull the Claude window to the front.
> ⛔ IP gate (owner, 2026-07-16): posting/commenting on Facebook happens ONLY from the hub (a stable IP). On another machine? Do NOT post from here — send the job to the hub as text (bus / fleet log chat). Canon: `ip-sensitive-actions-hub-only`.

1. Check that the Chrome MCP is connected: `mcp__Claude_in_Chrome__list_connected_browsers`. If not — ask the owner to open Chrome with the extension (don't fall back to Playwright).
2. Open/select the `facebook.com` tab (he is already logged in — do NOT touch login/password). If not logged in — that is a blocker, tell the owner.
3. Find the composer: `mcp__Claude_in_Chrome__find` with the query "What's on your mind — create post box". Click it to open the post creation dialog.
4. Type the text into the composer field (`form_input` on the ref from `find`). **Do NOT press "Publish"** yourself until the Tier-2 gate from §1 is cleared.
5. After the owner's explicit `+` — press the "Publish"/"Post" button (or ask him to press it, if he is nearby and wants to). ⚠️ The dialog is two-step: compose → "Next" → Post settings → "Post". Take a screenshot of the result (`computer` screenshot) so the owner SEES that the post went out.
6. **Footer as the 1st comment** (rule §7.7, the post body carries no links): open the published post → the "Comment" field → blocks B+C+E from `_imports\content-factory\_STYLE-footer.md` (live links only). ⚠️ Enter sends the comment — use Shift+Enter for line breaks.
7. **Self-like** (owner's rule 2026-07-05: "the first like is always the hard one"): like your own post right after the footer comment. A standard step, no separate asking.
8. Composer pitfall: the first click can land on Stories (the feed shifts while lazy-loading) — after navigating, wait ~2s, screenshot, then click on the fresh coordinates.

## 3. Record it in the counter (AFTER a successful publication)
```bash
python "$USERPROFILE/.claude/scripts/fb_guard.py" record post
```

## 4. Report
One line: what was published + link/screenshot + "posts today N/8".

---

## Kill switches (account safety)
- Any Facebook warning (checkpoint, "you're doing this too often", an identity confirmation request) → **STOP immediately**, report to the owner, do NOT retry-spam (retries are exactly the road to a ban).
- Don't republish identical text.
- Don't touch login/password/2FA — if the session is logged out, that is a blocker for the owner.

## Related
- `/fb-reply` — replying to comments (Phase 1, the same guard).
- The counter engine: `~/.claude/scripts/fb_guard.py` (shared across post/reply/dm).
- Texts: `content-factory`, `facebook-diary`, `episode`; the voice — `fb-diary-voice`.
- Canon: Decision Memo 2026-06-28 (the Facebook skill set), `chrome-autonomy-self-drive`, `browser-work-on-peers-not-hub`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

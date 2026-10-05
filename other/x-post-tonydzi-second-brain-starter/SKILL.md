---
name: x-post
description: >-
  Publish a vetted post to an X (Twitter) account through the owner's real logged-in Chrome tab,
  rate-guarded and draft-first. Counts length the way X does, treating every link as 23
  characters, and refuses over-limit text instead of silently truncating. Triggers: "/x-post",
  "tweet this", "post to X".
license: MIT
---

# /x-post — post to X from the owner's account (Chrome, draft-first)

**Why.** EN teasers (from /episode) kept piling up as drafts — there was no poster for X. Same safe pattern as /fb-post: a live logged-in tab, never headless.

## 0. Safety catch (mandatory)
```bash
python "$USERPROFILE/.claude/scripts/_shared/social_guard.py" check x --text "<final text>"
```
`BLOCKED` (exit 3) → STOP and report (the 6/day limit, or a duplicate). Do not work around it.

## 1. The text (the owner's voice, top model)
Take a ready draft (an /episode EN teaser or an intention-lane text) or write it with the top model. A single tweet is ≤280 characters — count BEFORE opening the browser; longer → a thread (each tweet ≤280, chained by reply) or offer the operator a shorter version.

## 2. Tier-2 gate (draft-first)
Show the final text (+ the thread split, if it is a thread) → wait for an explicit `+`. Nothing is published without it.

## 3. The browser (Claude-in-Chrome, a live tab)
> Browser work stays local on this machine; never drag the window to the foreground elsewhere.
> ⛔ IP gate (2026-07-16): posting to X and other ban-sensitive social platforms happens ONLY from the hub `HUB-1` (a stable IP). Do NOT post from another machine — send the task to the hub as text. Canon: the "IP-sensitive actions from the hub only" rule.
1. `list_connected_browsers` → no extension → block and tell the operator (do not fall back to Playwright).
2. Open the `x.com` tab. **Verify the logged-in handle** (avatar / profile menu) against the registry. A different account → STOP and ask. Not logged in → block (we never touch login/2FA on X — checkpoint risk).
3. Composer: `find` "post composer / What's happening". Enter the text (`form_input`). **Do not press Post** until the gate in §2 is satisfied.
4. After the `+` — press Post. For a thread: use the "+" button in the composer after the first tweet, or reply to your own tweet.
5. A screenshot of the published post + the tweet URL (click the timestamp → address bar) is the proof.

## 4. Record it (AFTER a successful publication)
```bash
python "$USERPROFILE/.claude/scripts/_shared/social_guard.py" record x --text "<text>"
```
Report: the link + the screenshot + "x today N/6".

## Stop switches
- Any checkpoint / captcha / "unusual activity" from X → STOP immediately, report, zero retries.
- Never republish identical text; never post from someone else's account.
- Links in the text must be live and ours (link-safety).

## Related
`/fb-post` (the pattern this follows) · `/tg-post` · `/episode` (tiers: EN teaser → X) · the gate `scripts\_shared\social_guard.py` · the registry `00-System\Channels-Registry.md`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

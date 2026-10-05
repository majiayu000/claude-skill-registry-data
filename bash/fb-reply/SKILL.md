---
name: fb-reply
description: >-
  Read who commented on recent Facebook posts and publish personalized replies through the real
  logged-in Chrome tab, draft-first, with a daily cap and a minimum gap between replies.
  Triggers: "/fb-reply", "reply to my facebook comments".
license: MIT
---

# /fb-reply — reply to the comments under the owner's posts (safely)

**Why.** Comments pile up under the posts (often valuable — like the counter-thesis one engineer left about tailscale). Replying on your OWN posts is a low-risk task, but Facebook still bans for PACE. So: read safely, write personally in the owner's voice, post one at a time with pauses, under a counter.

**Main rules (from Deep Research #32):**
- **Pace decides, not "bot vs human".** Every reply passes `fb_guard check reply`: ≤40/day, ≥5 min between replies, no back-to-back series. The guard physically will not let you overshoot.
- **Every reply is personal and different** (top-tier model, the owner's voice). The same text sent to many people = a spam flag → a ban.
- **Draft-first:** show the owner a batch of drafts, post only after a `+`.
- **Account safety:** do NOT click "View more comments" on reshares — it navigates away. Read what already loaded under the original.

---

## 0. The fuse — status at the start
```bash
python "$USERPROFILE/.claude/scripts/fb_guard.py" status
```
Shows how many replies went out today and whether we are paused. If `reply` is already at the daily limit — tell the owner and defer.

## 1. Browser + reading the commenters (no risky clicks)
> Strictly LOCAL, a live tab, we never touch the login. Is the Chrome MCP connected? (`list_connected_browsers`).
> ⛔ IP gate (owner, 07-16): Facebook commenting happens ONLY from the hub (a stable IP). On another machine do NOT reply — send the task to the hub as text. Canon: `ip-sensitive-actions-hub-only`.

1. Open the owner's post (he gives the link, or go to `facebook.com/<profile>` → his latest posts).
   ⛔ **PITFALL 2026-07-28: the profile wall does NOT hand out permalinks.** Scrolling the profile yields zero `pfbid` links (Facebook populates href only on hover), and the feed is virtualized — a JS scroll outruns lazy loading and the posts stay skeletons. **The working entrance = the notifications feed** `facebook.com/notifications`: every row "X commented on your post" already carries a ready `/posts/pfbid…` and tells you WHO wrote and WHEN. One pass over it replaces the whole wall scroll. The Graph-API path (`fb_posts_poll.py`) is dead for now — there is no `FB_USER_TOKEN`.
   ⚠️ An open Messenger window pollutes the results: its `div[role="article"]` elements are DM messages, not comments. Close the chat window before collecting.
2. **Extract the commenters INSIDE THE PAGE ITSELF** (Facebook hides names/links across the MCP boundary → match and filter inside the page, and hand out only safe text). Through `mcp__Claude_in_Chrome__javascript_tool`:
   ```js
   const out = [];
   const seen = new Set();
   document.querySelectorAll('div[role="article"][aria-label]').forEach(a => {
     const al = a.getAttribute('aria-label') || '';
     if (!/^Comment by|^Reply by/i.test(al)) return;                     // comments only
     const blocks = [...a.querySelectorAll('div[dir="auto"]')]
       .map(d => (d.innerText || '').trim()).filter(Boolean);
     const text = (blocks.sort((x, y) => y.length - x.length)[0] || '').slice(0, 500);
     if (!text || seen.has(text)) return;
     seen.add(text);
     const link = a.querySelector('a[role="link"][href]');               // the author's profile
     const handle = link ? (new URL(link.href).pathname.replace(/\//g,'')) : '';
     const hasImg = !!a.querySelector('img[src*="scontent"],img[src*="fbcdn"]');
     out.push({ handle, text, hasImg });                                  // handle = username, not a display name
   });
   out;
   ```
   You get back a list of `{handle, text, hasImg}` — no hidden strings, safe to display. (If Facebook runs in another language, add that locale's `aria-label` prefixes to the regex.)
3. **Virtualization:** if there are few comments, gently scroll the comments area (`computer` scroll down the page, WITHOUT clicking expander buttons) and repeat §1.2. On a RESHARED post do NOT press "View more".
4. **⚠️ MANDATORY: expand collapsed threads BEFORE choosing "who to reply to" (lesson 2026-07-05):** Facebook hides existing replies under "View N replies" — the owner has often ALREADY replied himself, and from the outside you cannot see it (a duplicate = embarrassment + a spam signal). On YOUR OWN post the inline thread expanders are safe (not to be confused with "View more comments" on reshares). Through JS: click every toggle matching `/View (\d+ )?repl/i`, wait ~3s, then collect `aria-label^="Reply by <owner's name> to <Name>"` → the list of ALREADY answered people; reply only to those not on it. In the 2026-07-05 run this filtered out 7 of 8 "candidates".

## 2. Reply drafts (top model, personal)
For every comment worth answering, write a **separate** short reply in the owner's voice: address the person by name/by the comment's context, no template, every text different. Assemble the batch and show it to the owner:
```
1. [<name>, <handle>] comment: "…tailscale…"   →  draft: "spot on. show me how your transport is wired?"
2. ...
```
Wait for a `+` (or edits). This is the draft-first gate.

## 3. Posting one at a time, under the counter — THE PROVEN MECHANICS (2026-07-04)
> Debugged live: the owner's reply to a commenter landed as a threaded reply. The key pitfalls are below — do NOT rediscover them.

For EVERY approved reply:
1. **Guard gate:** `python "$USERPROFILE/.claude/scripts/fb_guard.py" check reply`
   - `BLOCKED ...` (exit 3) → STOP posting. Tell the owner how long to wait / what is queued. The rest goes later / in the next pass.
   - `OK reply` → carry on.
2. **Open the post** at `www.facebook.com/<profile>/posts/<pfbid>` (it renders as a `role="dialog"` modal — that is normal, work inside it).
   ⚠️ **Verify you actually landed on the right post** (pitfall 2026-07-27): Facebook can drift the tab onto a NEIGHBOURING post while the previous page's comments stay in the DOM, hidden → the target is found, but the reply goes to the wrong place. The cure: after navigating, check `location.href` / `document.title`, and search for the target ONLY among the visible ones (`a.offsetParent!==null`).
3. **Screenshot** (`computer` screenshot) to see the layout and FIND the "Reply" link WITH YOUR EYES. ⚠️ A screenshot of a heavy modal sometimes hangs ("captureScreenshot timed out / renderer frozen") — just REPEAT the screenshot, it answers every other time, this is not fatal.
4. **Click the REAL TEXT link "Reply"** in the "Like · Reply · Hide" row under the right comment — BY THE COORDINATE from the screenshot. ⛔ PITFALL: `find` returns a "Reply" ref which, when clicked, moves focus to the modal's CLOSE BUTTON (the inline field does NOT open). Click visually on the coordinate of the "Reply" text, NOT on the find ref.
5. The inline reply composer opens with an @mention of the author. **Set focus through JS, not with a coordinate click** (lesson 2026-07-20): the modal reflows between the screenshot and the click → the click lands in the comment body and `type` goes nowhere (twice in a row). The working recipe:

> ⛔ **INPUT AND SENDING PITFALLS (2026-07-27, proven live — THIS IS NOW THE MAIN PATH):**
> **(1) `computer type` EATS SPACES AND PERIODS.** "waiting. i'll star it first" landed in the field as `waitingi'llstaritfirst`. Publish that unchecked and it is a public embarrassment under your own post. **Instead of `type`, insert the text through JS** (spaces survive, the @mention stays intact):
> ```js
> f.focus();
> const r=document.createRange(); r.selectNodeContents(f); r.collapse(false);
> const s=getSelection(); s.removeAllRanges(); s.addRange(r);
> document.execCommand('insertText', false, '<the reply text>');
> ```
> **(2) Discrete key presses (`key Return`, `key BackSpace`) DO NOT REACH the composer** — focus is not held between MCP calls, the field keeps its text, nothing is published (and Backspace clears nothing). **Sending depends on the TYPE of composer, and there are TWO:**
> - **A top-level composer** (a reply to a top-level comment): it has a button — click it from JS:
> ```js
> let box=f, up=0; while(box && up<8){box=box.parentElement; up++; if(box.querySelector('[aria-label="Post comment"]')) break;}
> box.querySelector('[aria-label="Post comment"]').click();
> ```
> - **A nested-thread composer** (a reply to someone's reply): there is NO `Post comment` button at all (verified by walking 12 levels up — only emoji/GIF/stickers). Sending = a synthetic Enter, **necessarily in the SAME call as `focus()`**, otherwise focus is lost and nothing goes out:
> ```js
> f.focus();
> const r=document.createRange(); r.selectNodeContents(f); r.collapse(false);
> const s=getSelection(); s.removeAllRanges(); s.addRange(r);
> const o={key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true,cancelable:true,composed:true};
> f.dispatchEvent(new KeyboardEvent('keydown',o));
> f.dispatchEvent(new KeyboardEvent('keypress',o));
> f.dispatchEvent(new KeyboardEvent('keyup',o));
> ```
> The universal order: look for the button first, no button → a synthetic Enter.
> **(3) You need to erase what is already typed** — not with Backspace, but with a selection in ONE JS call: caret to the end → `s.modify('extend','backward','character')` × N → check `s.toString().length===N` and that the selection did NOT swallow the name from the @mention (abort if it did) → `execCommand('insertText', ...)` overwrites the selection.
> **The one-line conclusion:** the whole cycle (open the composer → insert → send) is done through JS; `computer` is needed in this skill only for screenshots.

   ```js
   const f=[...document.querySelectorAll('[contenteditable="true"]')]
     .find(e=>/Reply to <Name>/.test(e.getAttribute('aria-label')||''));
   f.scrollIntoView({block:'center'}); f.focus();
   const r=document.createRange(); r.selectNodeContents(f); r.collapse(false);   // caret to the end, after the @mention
   const s=getSelection(); s.removeAllRanges(); s.addRange(r);
   ```
   then insert the joke (≤5–7 words, the owner's voice, top model) via `execCommand('insertText')` — NOT `computer type`, see the pitfalls above. Open the composer through JS as well: inside the right `article`, click the element whose `innerText==='Reply'`.
6. **Verify through JS** (a screenshot may hang — the DOM is more reliable): among the `[contenteditable="true"]` elements there is a field with `aria-label="Reply to <Name>"` containing your text (the mention + the joke). Only then send.
7. **Send:** a JS click on `[aria-label="Post comment"]` (see the pitfalls above). ⛔ `computer key Return` does NOT work — it never reaches the field.
8. **Confirm publication through JS:** a `div[role="article"][aria-label^="Reply by <my name> to <Name>'s comment"]` appeared with your text AND the reply field cleared (`innerText===''`). Only that means "published".
9. `python "$USERPROFILE/.claude/scripts/fb_guard.py" record reply`
10. The guard holds a ≥5 min pause before the next one — do NOT work around it by speeding up (pace is the main reason for bans).
    Wait for the pause like this (a foreground `sleep` is blocked by the harness, and `Start-Sleep` + a command is too):
    ```bash
    until python "$USERPROFILE/.claude/scripts/fb_guard.py" check reply >/dev/null 2>&1; do sleep 15; done; echo "GUARD OPEN"
    ```
    run it through Bash with `run_in_background: true` — a notification arrives exactly when the window opens.
11. ⛔ **Check the text for long dashes BEFORE sending** (`/[—–]/`) — the rule [[no-long-dashes]] applies to comments too. Caught one in the field → not Backspace, but a backward selection of N characters + `insertText` (§3 pitfall 3); check that the selection did not swallow the @mention.
12. Element visibility: `offsetParent` inside a Facebook modal is **always null** (position:fixed) → build the "visible" filter on `getBoundingClientRect()` + `checkVisibility()`, otherwise you filter EVERYTHING out and conclude there are no comments.

## 4. Report
What was answered, what is queued (waiting on the pause/limit), how many today `reply N/40`.

---

## Kill switches (account safety)
- Any Facebook warning / checkpoint / "too often" → **STOP immediately**, report to the owner, no retry-spam.
- Do NOT click "View more comments" / navigation buttons on reshares (they navigate away).
- Do NOT post identical text to different people.
- We never touch login/2FA.

## Related
- `/fb-post` — publishing posts (Phase 1, the same guard).
- `/fb-dm` — DMs to commenters (Phase 2, strict draft-first; not built yet).
- The counter: `~/.claude/scripts/fb_guard.py`. The voice: `fb-diary-voice`.
- Canon: Decision Memo 2026-06-28, `chrome-autonomy-self-drive`, `browser-work-on-peers-not-hub`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.

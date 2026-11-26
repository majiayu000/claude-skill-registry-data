---
name: instagram
description: 'Work an Instagram account the way log does it: through the direct-API engine on vendor/instagrapi and the account''s one session host, never the browser. Read the threads, read one person in full, draft in the owner''s voice, gate it, send text or a meme as a photo, and let the realtime watch push every new DM to the agent.'
---

# instagram

Instagram is worked over the MCP, on the direct-API engine (`python/instagramApi`,
vendor/instagrapi), never in the account's AdsPower browser.

## Hard boundaries

1. **Never the browser.** Every Instagram action is an MCP tool: `instagramDms`,
   `instagramSend` / `instagramSendLive`, `instagramWatch`,
   `instagramSessionCheck`. An action the engine doesn't have yet is built on the
   engine first.
2. **One session per account.** Every call goes through the account's one
   session host (`python/instagramApi/host.py`): one client signed in once, one
   realtime connection. Never start a second process for it. A call that can't
   reach the host is refused with `instagramSessionHostDown` (rule 105).
3. **Claim the chat before drafting** with `inboxClaim` (rule 133); a chat
   another session holds is left to it, and the send releases the claim.
4. **Read them first.** Read the person's whole thread before drafting
   (`instagramDms` { with }), rule 109.
5. **Gate every draft** with `voice` { to, with, context, text } until it passes.
6. **Send once, and stop if they write.** A multi-line draft goes out one
   message per line, and the send stops the moment they write back
   (`>>> INTERRUPTED`): answer them, never resend (rule 90). Any refusal
   stops the run (rule 94).
7. **Live needs the owner.** `instagramSendLive` needs `approvedBy` and
   `confirmLive: true` (rule 8).

## The routine

```text
instagramSessionCheck { account }                    the session is still good
instagramDms { account }                             the threads, newest first, ● unread
instagramDms { account, with: "<handle|thread>" }    one thread, oldest first; kept for log search and the voice index
voice { to, with, context }                          how the owner writes there
voice { to, with, context, text }                    gate the draft
instagramSendLive { account, with, text, approvedBy: "<owner>", confirmLive: true }
instagramSendLive { account, with, photo: "<file>", text, ... }   a meme goes as a photo
```

## The live side

The inbox hook keeps `log instagram watch` running for every signed-in Instagram
account. It holds Instagram's own realtime connection (MQTT to
edge-mqtt.facebook.com, the DM sync subscribed) on the session host, and every
new DM lands in `~/.logCli/inbox/pending.jsonl` and reaches the agent as
`>>> NEW INSTAGRAM MESSAGE` (rule 123). An agent following a conversation keeps a
Monitor on that file.

## Where things are

- Commands: `src/cli/instagram/index.ts`. Session: `src/instagram/account/session`.
- Engine and host: `python/instagramApi/engine.py`, `python/instagramApi/host.py`.
- Transport: every HTTP call through curl_cffi (`check:instagramTransport`); the
  realtime MQTT socket is the one exception.
- Use cases: `docs/useCases/instagram/dmReply.md`, `newPlatform.md`.
- Spec: `docs/specs/instagram.md`. Platform page: `docs/platforms/instagram/README.md`.

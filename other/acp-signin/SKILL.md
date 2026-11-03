---
name: acp-signin
description: "Use when an iNFT's ACP session needs signing in. The split sign-in run from the chat: mint the link, hand it to the owner to approve, poll until authenticated, never touch another iNFT's config."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, ACP, Virtuals, sign-in, login, session, iNFT]
    related_skills: [economyos, agentic-economy, acp-troubleshooting, agent-email, iclone-os]
---

# ACP sign-in — the link comes to the chat, the owner approves it

The Virtuals ACP session of an iNFT expires. When it does, every economy read
answers `Not authenticated` / `reauth-acp` and the Dock apps show "sign-in
required". Signing in again is a split flow: the CLI mints a link, the OWNER
opens it in their browser and approves, the CLI confirms. You run both ends
from the chat; the owner only clicks the link.

## When to use

- The owner says "sign in", "login", "log in to acp", "the session expired", or asks why
  Email / Bank / Market say "sign-in required" or "Sign in again".
- Any `~/.iclone-os/bin/acp --inft <iNFT> …` answer contains `Not authenticated`,
  `NOT_AUTHENTICATED`, `session expired`, `not logged in` or `login required`.
- Settings → iNFT also has a "Sign in to acp" button per iNFT; the owner may prefer it.
  Offer it when they are at the Mac; do the chat flow when they ask you to.

## Prerequisites

- You know WHICH iNFT: the one on stage (`#6`, `#7`…). If in doubt, ask with `clarify` —
  never sign in a different iNFT "to be helpful".
- `~/.iclone-os/bin/acp --inft <iNFT> agent whoami --json` works for a healthy session.
  If it answers an auth error, that is the signal to run this skill.

## How to run

1. Mint the link (read-only, nothing is changed yet):
   ```
   ~/.iclone-os/bin/acp --inft <iNFT> configure start --json
   ```
   Read `url` (or `authUrl`) and `requestId` (or `request_id`) from the JSON.
2. Hand the link to the owner in ONE message, plain, clickable, no commentary around it:
   "Sign-in link for #6 — open it and approve: <url>". Tell them it expires in a few minutes.
3. Poll the completion, waiting ~4 s AFTER each answer (not a fixed clock), for at most 5 min:
   ```
   ~/.iclone-os/bin/acp --inft <iNFT> configure complete --request-id <requestId> --json
   ```
   Stop when `status` is `authenticated`.
4. Confirm with `agent whoami --json`, then tell the owner in one line: "#6 is signed in again."
   The Dock apps recover by themselves within their refresh interval; no restart.

## Pitfalls

- Never paste the link into anything but the chat with the owner. Never open it yourself
  (no `browse`, no `browser_navigate`): the approval is the OWNER's.
- Never read, print or log tokens, cookies or config files. The CLI's JSON answers are enough.
- One sign-in at a time per iNFT. If a poll says the request expired, mint a NEW link (step 1);
  do not retry `complete` with the old id.
- A transient CLI failure (one `Not authenticated` while another command of the same iNFT
  runs) is not an expired session: re-run `agent whoami --json` once before starting the flow.
- `configure` with no subcommand is interactive and will hang: always `start` / `complete --json`.

## Verification

- `agent whoami --json` answers the agent's id and name without an auth error.
- `email whoami --json` answers the address.
- If the owner is at the Mac: Settings → iNFT shows the iNFT as signed in and Email loads.

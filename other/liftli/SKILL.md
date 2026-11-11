---
name: liftli
description: Use when the user asks to set up, sign in to or connect Liftli, to connect their LinkedIn or X account to Liftli, asks what Liftli can do, or asks for something done with Liftli by name (publish or schedule through Liftli, their Liftli strategy, drafts or voice). Also use when Liftli's tools are missing or report that sign-in is needed. Checks the Liftli sign-in and walks the user through it.
metadata:
  internal: true
---

# Liftli

Liftli is the connector that comes with this plugin. It learns the user's
voice from their real posts, keeps their strategy between sessions, and
publishes to LinkedIn and X through the official APIs after the user approves
each post. Its tools do nothing until the user has signed in once.

## Check the sign-in

1. **Liftli is ready** if a `strategist_briefing` tool is available (it may be
   deferred: search for it by name first). Call it once, then carry out the
   user's request with Liftli's tools. Stop reading this skill.
   Do this search even when a notice says the plugin's own liftli server
   needs authentication: Liftli may already be connected another way, for
   example from Claude's connector directory.
2. **Liftli needs sign-in** if that search finds no `strategist_briefing`
   tool. Tell the user, in one short message, the step for the app they are
   using:

   - Claude Code: type `/mcp`, choose **liftli**, and pick Authenticate. A
     browser window opens.
   - Claude app (web, desktop, Cowork): open Customize, then Plugins, then
     Liftli, and connect Liftli on its Connectors tab.
   - Gemini CLI: `/mcp auth liftli`. Cursor: open Settings, MCP, and sign in
     to liftli. Other apps: follow the sign-in prompt shown for the liftli
     server.

   Then: sign in or create a free account, and tell me when you're done so I
   can pick up right here. End your turn there and wait for their reply.
3. **The user doesn't want to sign in right now.** Help with the LinkedIn
   skills in this plugin instead (start with `linkedin-agent`), and don't
   bring up sign-in again in this conversation. Anything they write can still
   be pasted into LinkedIn by hand.

## Rules that stay on after sign-in

- Nothing is published or scheduled without the user's explicit approval of
  the exact text. Liftli asks for it; never skip that step.
- Never automate the LinkedIn or X website, and never ask for a password.
- Never say a post went out unless a Liftli tool confirmed it.

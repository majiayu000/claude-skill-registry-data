---
name: connect-web
disable-model-invocation: true
description: Pair the Apeiron web editor (a browser tab) with this Claude Code through the hosted relay
---

Connect me to the Apeiron WEB editor (https://engine.apeironengine.com) in my browser. This plugin's
`ngine` server drives an editor INSTALLED on this machine; a browser tab is reached through the hosted
relay instead, by the companion plugin `apeiron-web`. Walk me through it and check each step:

1. If the `apeiron-web` MCP server is not among your tools, tell me to run, in a terminal:
   `claude plugin install apeiron-web@apeiron` (the marketplace is the one this plugin came from),
   then restart Claude Code.
2. Tell me to run `/mcp`, choose `apeiron-web`, and choose **Authenticate**. A browser page asks me to
   sign in with my Apeiron account and allow Claude Code to drive my tabs. You cannot do this for me.
3. Tell me to open https://engine.apeironengine.com and sign in there with the SAME account
   (Account > Sign in). A signed-in tab connects to the relay by itself: nothing to paste.
4. Call `tab.list` on the `apeiron-web` server. Report the tabs it lists; if there are several, ask
   which one and call `tab.attach {code}`. Then call `editor.context` on it and summarise what is open.

If `tab.list` is empty: the tab is not signed in, is a different account, or is in a hidden browser
window (browsers throttle hidden tabs) — say which checks you could make. For an agent other than
Claude Code, the fallback is the tab's Help > Connect AI Agent > Connect, which prints a key-paired
command. Do not change anything in the scene while connecting.

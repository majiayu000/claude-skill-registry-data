---
name: connect-web
disable-model-invocation: true
description: Connect to my Apeiron web editor tab through the relay, signed in with my Apeiron account
---

Connect me to my Apeiron web editor (https://engine.apeironengine.com) and check each link:

1. Call `tab.list` on the `apeiron-web` server. If the call is refused as unauthorized, tell me to
   run `/mcp`, choose `apeiron-web`, choose **Authenticate**, and sign in with my Apeiron account in
   the browser page that opens. You cannot sign in for me. Then call `tab.list` again.
2. If no tab is listed, tell me to open https://engine.apeironengine.com and sign in there with the
   SAME account (Account > Sign in). A signed-in tab joins the relay by itself, with nothing to paste.
   Keep the tab in a visible window: browsers throttle hidden tabs.
3. With one tab, use it; with several, show their codes and ask which, then `tab.attach {code}`.
4. Call `editor.context` and summarise what is open. Suggest `ngine.guide` for orientation.

Do not change anything in the scene while connecting. If a step fails, say which one and what you saw.

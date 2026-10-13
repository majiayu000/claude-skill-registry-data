---
name: status
disable-model-invocation: true
description: Check every link between Claude Code and my Apeiron web editor tab, and say how to fix what is broken
---

Diagnose the connection to my Apeiron web editor. Only read; change nothing. Check, in order, and
report each as pass, fail or did-not-run (a check you could not make is not a pass):

1. **Authentication** — call `tab.list` on the `apeiron-web` server. Unauthorized means: run `/mcp`,
   choose `apeiron-web`, Authenticate.
2. **A tab is reachable** — `tab.list` names at least one tab. None means: open
   https://engine.apeironengine.com in a visible window and sign in with the same Apeiron account.
3. **The tab answers** — `tab.current`, then `editor.context`. A timeout usually means the tab is in a
   hidden or minimised window.
4. **Versions** — `editor.version`: report the engine version and channel.

End with the one fix for the first failing link, or one line saying everything passes.

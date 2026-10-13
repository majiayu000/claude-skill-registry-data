---
name: report-issue
disable-model-invocation: true
description: Help me file an Apeiron bug report from my web editor session
---

Help me report a problem with the Apeiron web editor to the Apeiron team. Gather, without changing
anything: the `report` field of `editor.version`, the last errors in `editor.context`, and the exact
ops and arguments that led to the problem. Draft a one-line title and a body (what I did, what I
expected, what happened, plus what you gathered) and show it to me. Do not send anything yourself.

Then tell me to send it from the tab: Help > Report Issue, paste the title and body, and open
**Review what will be sent** to read the exact report before pressing Send report. On the web it
carries only the title, body, the editor version and a diagnostics block (build, platform, GPU, last
op names — no project name); no log, screenshot or crash file is attached. Ask me before suggesting
I add anything else to the body. It is filed under my Apeiron account (never on GitHub) and the team
is emailed.

Sending needs the Apeiron accounts service and a tab signed in to my Apeiron account. If the tab
cannot sign in or the report does not send because the accounts service cannot be reached, say
plainly that sending needs the Apeiron accounts service, which is not available right now, and give
me the finished title and body as one block of text I can copy and paste myself. List separately
anything you could NOT collect and why.
